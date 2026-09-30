---
title: "Experiments: evidence, effects and bytes"
subtitle: "A PEER pilot, pinned decision-call and byte experiments, and two registered observer designs"
status: "Draft 0.2, 30 September 2026. The retained pilot and two fixture experiments have results; they do not establish below-agent observation or independently operated custody."
description: "A snapshot-gap pilot, APS/PriorSeal fixture outcomes and limits, and a source-pinned AGT transcript-byte reproduction."
toc: true
---

The [atlas's open cell](atlas.html#the-open-cell) asks whether a record of an agent action comes from a vantage the agent cannot control, whether its evidence binds to the actual effect, and what was missed. A signature and an offline verifier answer questions about retained bytes. They do not answer who could alter or omit the underlying observations. These experiments keep those questions separate.

## E1. PEER pilot: the snapshot gap

The local `agent-evidence-observer` prototype mediates one file replacement, commits to the before-state, signs a bounded result, and checks a hash-chain head under a second key. It does not isolate an agent. Its own record says `witnessScope: PEER` and `unmediatedEffects: not-established`. The two keys are controlled by one local operator.

I ran [the exact pilot script](experiments/observer-vantage/run.py) against the package source identified by SHA-256 `273e4985cb4de671145bcd55ef85545be213e8520f766ab7692e9d05edae60d1`. The [recorded machine result](experiments/observer-vantage/recorded.json) contains three scripted intervals. This source is a local prototype awaiting a public repository; an outside reader can inspect the pilot script and result now, but cannot independently rerun the same package revision until those source bytes are published. The result is a local measurement, not a claim of independent reproduction.

| interval | deliberately attempted effect | observed result | inference |
|---|---|---|---|
| Brokered write | A script says "no write," then asks the broker to write once and repeats the same request ID | One accepted write, one replayed request, offline verification passed, `PEER`, `noDetectedGap=true` | The retained broker record contradicts that *scripted* self-report. No unmodified agent or independent witness was tested. |
| Durable bypass | The same process writes directly to the workspace and leaves the bytes there | The direct write succeeded; the next snapshot reported `workspace changed outside the broker`. Verification against the current workspace refused the stale root. | The observer can detect this particular durable divergence, but did not prevent it. |
| Transient bypass | The same process creates a file and removes it before the next snapshot | The direct write succeeded; `knownGaps=[]`, `noDetectedGap=true`, and offline verification against the restored workspace passed. | A snapshot-only check can miss an effect that leaves no final byte difference. `noDetectedGap` is not complete coverage. |

The population for this pilot is three scripted intervals: one brokered write plus its retry, one durable direct write, and one transient direct write. The broker's declared coverage population is calls with valid request IDs. The direct effects are **outside** that denominator. There is no sample of live agents, tool calls, reads, network effects, file modes, concurrent races, hostile host operators, or independent witnesses. The only tested observation point is the sequential file-tree snapshot at a broker call or seal. The test deliberately controls both sides; its contradiction is a counterexample to a claim of complete coverage, not a measured detection rate in deployment.

To re-run after obtaining the matching observer source, create its Python 3.12+ environment with the dependencies in its `pyproject.toml`, then use:

```sh
/path/to/observer/.venv/bin/python experiments/observer-vantage/run.py \
  --observer-root /path/to/agent-evidence-observer > /tmp/observer-pilot.json
diff -u experiments/observer-vantage/recorded.json /tmp/observer-pilot.json
```

The script hashes the package metadata and every `src/probity_observer/*.py` file before importing the package. A different digest is a different implementation, even if the three outcomes match. It prints no ephemeral signing keys or timestamps. The claim ledger records this run and its limits as E-01 through E-03.

## E2. Below-agent observation: registered design, no result

**Hypothesis.** Under a pinned launch configuration, a host broker unavailable to the agent records every accepted or denied file replacement through one declared channel. A direct attempt to alter the watched tree, observer process, key, or journal fails. If any channel loses its record, the result becomes incomplete instead of an absence claim.

**Unit and denominator.** One launch interval is the unit. Before each interval, pin the agent image and policy digests, authority, allowed path scope, observer build/configuration, initial tree root, nonce, and observer key. Report counts for attempted, accepted, denied, replayed, dropped, and unresolved requests. Record the paths and privileges reachable by the agent as part of the denominator. Do not convert "no event seen" into "no effect" when reachability or liveness is unknown.

**Interventions and controls.** Run the same workload under (a) the current PEER prototype as a negative control and (b) a host-side isolation boundary whose configuration is published. Exercise a normal write, a false self-report, direct workspace write, key read, process signal, alternate channel, path traversal or symlink, lost response retry, broker death, and a missing event. Retain failed and null runs. The agent must not choose the observer's key, journal, commitment, or before-root. A separate operator reproduces one live interval and pins the key independently.

**Primary outcomes.** For each attempted effect, report its raw trace, broker decision, resulting durable bytes, record, refusal or gap, and verification result. The threshold to claim a *bounded below-agent file-write observation* is a demonstrated inability of the tested agent to address the observer and watched tree except through the broker, no missing record for the tested channel, and a signed prior commitment bound to that interval. A single escaped effect or missing record blocks that claim. This does not establish all filesystem effects, all agent actions, or host-operator honesty.

This experiment has **zero isolated-agent runs** and no measured overhead. The [observer acceptance criteria](https://github.com/probityai/agent-evidence-vectors/blob/main/spec/predicates/observed-effect.md) are a target for the record format; the local prototype does not emit a conformant Observed Effect statement.

## E3. Separately witnessed history: registered design, no result

**Hypothesis.** A witness run by a separate principal, with a pinned key and retained highest head, detects deletion, reorder, replay, divergent heads, and an absent committed interval when shown inclusion and consistency evidence. A second key held by the same operator cannot establish that property.

**Unit and denominator.** One committed interval and its checkpoint pair, plus each attempted history mutation. Publish the witness operator boundary, retention policy, head pinning method, hash/signature profile, and every accepted or refused fork attempt. Test honest append, truncation, two conflicting suffixes, withheld interval, witness unavailability, and key substitution. An offline consumer with an independently pinned head must reproduce refusals. Report mutation count, detected count, undecidable count, and time/space overhead; never recode an unavailable witness as success.

There are **zero separately operated witness runs**. The local PEER pilot's second key is a protocol test only. The witness experiment will remain unclaimed until a separately operated history and a second reproducer exist.

## E4. APS/PriorSeal E2: decision evidence and exact-call fixtures {#aps-priorseal-e2}

The [immutable run record](https://github.com/probityai/agent-evidence-vectors/tree/00f5acab880bffc5ee8fe124f3a015d3ed970514/interop/aps-priorseal-e2-2026-09-30) checks APS decision evidence against PriorSeal's exact-call examples. Its checker imports no APS or PriorSeal implementation. It uses draft-pidlisnyi-aps-03, the fixture documentation, pinned public test keys, and a fixed reference time of `2026-09-19T10:05:00.000Z`. Implementation independence does not establish independent custody of an action observation.

The fetch script pins 31 files from APS `948f99b85343bef2c6fa677c8543965caacfc087` and PriorSeal `d749d2691c3e6be139de4020e7b27cdafca2c428`. [RESULTS.json](https://github.com/probityai/agent-evidence-vectors/blob/00f5acab880bffc5ee8fe124f3a015d3ed970514/interop/aps-priorseal-e2-2026-09-30/RESULTS.json) contains 96 rows, one per claim per input: 86 `pass`, four `fail`, and six `not-exercised`. These are fixture outcomes, not a deployment success rate. The four failures are the denied APS dispatch, the expired APS reference-time check, and the over-limit pair's call-value and per-action-cap checks.

| claim | within-limit pair | over-limit pair |
|---|---|---|
| APS decision-ref correlation | pass | pass |
| Exact call against the supplied observation | pass | fail: intent value 1e15, observation value 6e15 |
| APS per-action cap, using the checker's declared asset mapping | pass | fail: 6e15 exceeds 5e15 |
| PriorSeal principal, acceptance and receipt signatures | not-exercised: out_of_scope | not-exercised: out_of_scope |

The report's 22 recomputable values agree, and three quoted fixture values agree. Report assertions about PriorSeal receipt validity remain unexercised. [SPEC-GAPS.md](https://github.com/probityai/agent-evidence-vectors/blob/00f5acab880bffc5ee8fe124f3a015d3ed970514/interop/aps-priorseal-e2-2026-09-30/SPEC-GAPS.md) records the missing written PriorSeal signing profile, hash constructions recovered by trial, and the checker's mapping from APS spend units to the PriorSeal asset. No result evaluated by this checker differs from the producer's stated outcome.

[NEGATIVES.json](https://github.com/probityai/agent-evidence-vectors/blob/00f5acab880bffc5ee8fe124f3a015d3ed970514/interop/aps-priorseal-e2-2026-09-30/NEGATIVES.json) records five variants and two controls:

| variant or control | measured outcome |
|---|---|
| Invalid APS signature | Decision signature fails; dependent composition claims become void |
| Re-signed APS receipt with an unpinned key offered by adjacent keys.json | Decision signature fails under the checker's pinned configuration |
| Altered authorization with unchanged hashes | Intent-hash consistency fails |
| Altered authorization with every carried intentHash recomputed | Survives at the targeted PriorSeal signature claim, which is unexercised; exact-call comparison changes to pass, while the cross-check against APS requested_call changes to fail |
| Unbound decision_ref, paired with the narrow APS case | Correlation fails on both payments |
| Changed issued_at without re-signing | Receipt identifier and signature checks fail |
| Re-serialization with unchanged JSON value | No state changes |

The surviving rehashed variant is not a whole-case acceptance: the APS cross-check still refuses it. It demonstrates the precise limit of this checker at an unexercised principal-signature claim. The fixtures do not establish chain execution, live authorization currency, live revocation, decision-level single use, cumulative spend, independently operated custody, or production usage.

To reproduce, check out the immutable vectors revision above and run the commands in its [README](https://github.com/probityai/agent-evidence-vectors/blob/00f5acab880bffc5ee8fe124f3a015d3ed970514/interop/aps-priorseal-e2-2026-09-30/README.md). The checker pins agent-evidence-vectors 0.15.0 and pycryptodome 3.23.0; mutation generation additionally pins cryptography 44.0.2. The corpus package supplies byte and Ed25519 primitives, not APS or PriorSeal policy decisions. The ledger records the outputs and ceilings as E-05 through E-07.

## E5. AGT TRACE transcript bytes: a source-pinned reproduction {#trace-transcript-bytes}

The [runner](experiments/trace-transcript/run.py) calls the real AuditEntry, MerkleAuditChain, and both AGT session mappers at [AGT 60931ce](https://github.com/microsoft/agent-governance-toolkit/tree/60931ce0c65db144032cdc8e8f342c66cbb1201c). Before import, it verifies each retrieved source against its exact Git tree blob. Its byte oracle is [rfc8785.py 655cbe0](https://github.com/trailofbits/rfc8785.py/tree/655cbe02b8761208e3f4cc49e879ab1e328a7dca). IDs, times and contexts are fixed. The [recorded result](experiments/trace-transcript/recorded.json) includes all six inputs, digests, source SHA-256 values, Python 3.12.14, and Pydantic 2.13.5.

| AuditEntry.data input | model equals sink | model equals RFC 8785 | sink equals RFC 8785 |
|---|---|---|---|
| ASCII strings | yes | yes | yes |
| U+00E9 value | no | yes | no |
| U+E000 and U+10000 keys | no | no | no |
| Float 1.0 | yes | no | no |
| Negative zero -0.0 | yes | no | no |
| Float 0.000001 | yes | no | no |

The sink escapes non-ASCII characters while the model emits UTF-8 characters. Both sort keys by Unicode code point and use Python's number spelling; RFC 8785 requires UTF-16 code-unit ordering and ECMAScript number serialization. A JSON-value match therefore does not establish a transcript-byte match. These results concern the pinned AGT implementation's transcript hash, not the current TRACE library's separate reverse adapter or an entire protocol-conformance claim.

```sh
uv run --no-project --python 3.12.14 --with pydantic==2.13.5 \
  python experiments/trace-transcript/run.py > /tmp/trace-transcript.json
diff -u experiments/trace-transcript/recorded.json /tmp/trace-transcript.json
```

The runner also accepts `--source-dir` for an offline rerun from cached source blobs; it checks the same immutable pins. This experiment signs no record and executes no live agent. It establishes byte disagreements on the selected inputs, with no measured claim about effect capture, coverage, custody, or production failures. The ledger records its provenance and results as E-08 and E-09.
