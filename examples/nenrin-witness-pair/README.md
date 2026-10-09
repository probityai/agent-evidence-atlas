# Read a signed witness pair

These two records fetched the same agent card and walked different endpoints.
This second reader verifies each record under a separately pinned key and checks
the signed URL exactly. It is written from the record format, without the producer reader.

| Requested target | Record A: `/a2a` | Record B: `/mcp` |
| --- | --- | --- |
| `https://gate.horizonshield.dev/a2a` | matches | refuses |
| `https://gate.horizonshield.dev/a2a/` | refuses | refuses |

A reports seven true assertions and one unevaluated assertion. B reports four true
and four unevaluated assertions. Both records contain eight assertions. The reader
keeps each true, false and null value; it does not turn `7/7` or `4/4` into eight passes.

Install the pinned environment, then run the complete retained check:

```sh
uv sync --locked --group dev
bash scripts/run-gate.sh
```

`gate-results` contains the actual exits, signature/target reads, tests and coverage.
The CLI recipe for one record is in the [input contract](docs/INPUT-CONTRACT.md).

Credit to Pavlo (`pipavlo82`) and `kuangmi-bit` for the witness records, and Horizon
Shield for supplying the pair. Probity owns this reader. Current key verification
and reported assertion values stay separate from card signatures, response correctness,
historical key control and timestamp proofs. Those details are in the [source map](docs/SOURCE-MAP.md).
