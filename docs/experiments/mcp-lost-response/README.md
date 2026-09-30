# Lost-response retry diagnostic

This is a two-case harness for MCP `tools/call`. In both cases a tool commits an
effect, its first response is lost, and the application retries with a fresh
JSON-RPC request ID. The unkeyed tool calls the effect boundary twice. The
keyed tool suppresses the second effect in its application layer.

The harness owns a loopback effect sink. It counts POSTs to `/effect` outside
the adapter process. The adapter's printed effect count is ignored.

Run it against the included Python SDK adapter:

```sh
uv run --with mcp==2.2.0 --with mcp-types==2.2.0 --no-project \
  python experiments/mcp-lost-response/run.py \
  python experiments/mcp-lost-response/mcp_sdk_adapter.py
```

Or run it against another adapter:

```sh
python3 experiments/mcp-lost-response/run.py python3 /path/to/adapter.py
```

The adapter receives `cases.json` and a case ID as arguments. It reads
`PROBITY_EFFECT_URL` and sends `{"operationKey":"operation-1"}` to that URL
when the tested tool commits its external effect. It prints one JSON object on
the last line of stdout:

```json
{"requestIds":[2,3],"firstResponseLost":true,"retrySource":"application","protocolVersion":"2025-11-25"}
```

The first response must be dropped after the effect call returns. The retry
must come from the application, not an assumed SDK retry. The adapter must use
the same tool arguments on both attempts. The runner checks the two IDs and
the effect sink's count: 2 for the unkeyed case and 1 for application dedup.
Use a separate process for the tested tool if the SDK needs one.

This is a diagnostic for the scenario in [MCP issue #3394](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3394).
The issue's [published Python reproduction](https://github.com/arjun2075/mcp-b1-lost-response-repro/tree/6373793aed3c98c281d6fa695afe9fb6fa541586)
and an independent rerun reported the same counts. Our separate adapter runs
the MCP Python SDK 2.2.0 against this external sink; its [recorded run](recorded.json)
counted 2 and 1. No other SDK or transport has been run with this harness.
The MCP specification does not currently require either effect count. A failed
case means the adapter diverged from the declared scenario; it is not an MCP
conformance failure.

The sink only observes effects routed through its URL. It cannot prove that
no other effects occurred. The adapter reports request IDs and response loss;
the runner does not observe those wire events independently. An adapter that
routes its actual tool effect elsewhere invalidates the measurement.

Run the harness tests:

```sh
python3 -m pytest experiments/mcp-lost-response/test_run.py -q
```
