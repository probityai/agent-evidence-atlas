---
title: "Experiments: who can observe an agent effect?"
subtitle: "A measured PEER pilot and two registered tests for the missing vantage and history"
status: "Draft 0.1, 29 September 2026. One local prototype pilot is measured; no below-agent or independent-operator run has occurred."
description: "Reproducible pilot of a brokered write, durable bypass and transient bypass, with the next two observer experiments registered before data collection."
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
