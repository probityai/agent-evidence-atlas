---
title: "Probity Open Evidence Lab"
subtitle: "A public protocol and run register for checking specific agent-evidence claims"
status: "Protocol draft 0.1, 1 October 2026. The initial register contains the measured E6 author fixture. External CI adoption and independently operated custody require their own evidence."
description: "Submit pinned agent-evidence runs, hostile controls, field-level comparisons and correction records to a public register."
toc: true
---

Maintainers can use this protocol to submit a verifier run, a host-project CI integration, or an observer/witness experiment. Each record names its contract, retained inputs, implementation and operators, and reports what passed, failed or remained untested. Probity maintains this register. A listed result makes no membership, endorsement or adoption commitment on behalf of another project.

[Submit a run](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-run.yml) or [report a correction](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-correction.yml). The forms request the evidence needed for review. The [machine-readable register](lab/register.json), [experiments](experiments.html) and [claim ledger](claims.html) retain the supporting records.

## Start with a run that exists

The first register entry is [E6: observer declaration, admission and replay](experiments.html#observer-consumer-admission). It joins one prior declaration, one brokered durable file effect, signed history and a persisted consumer admission. Replaying the interval, changing consumer authority and altering a signed claim all refuse with exact reasons and unchanged consumer state.

| item | retained evidence |
|---|---|
| Observer implementation | [Exact revision 8562c25fb7ec97596ea9d0297c495340298914b6](https://github.com/probityai/agent-evidence-observer/tree/8562c25fb7ec97596ea9d0297c495340298914b6) |
| Checked source bytes | [Git blob pins](experiments/observer-admission/source-pins.json) and per-source SHA-256 values in the [result](experiments/observer-admission/recorded.json) |
| Original CI artifact | [Provenance and file manifest](experiments/observer-admission/provenance.json); original archive SHA-256 `bcc22cd27b1f9404e961f7329770620994a76348d085b7b711ab586986493892` |
| Actual runs | [Original PR-tree run](https://github.com/probityai/agent-evidence-observer/actions/runs/36808961399) and [exact-main run](https://github.com/probityai/agent-evidence-observer/actions/runs/36825509807) |
| Execution and comparison | [Atlas runner](experiments/observer-admission/run.py), [complete recorded outcomes](experiments/observer-admission/recorded.json), and the E6 procedure |
| Claim ceiling | Author-produced same-operator fixture; `PEER`; `evidence_vantage: artifact`; unmediated effects and independent custody remain unestablished |

On Linux, use the actual checked-in runner and retained bytes:

```sh
git clone https://github.com/probityai/agent-evidence-atlas atlas
cd atlas
git checkout --detach 91a0759e459acee8355e2f9aba34f8e80d19e038
git clone https://github.com/probityai/agent-evidence-observer .observer-source
git -C .observer-source checkout --detach 8562c25fb7ec97596ea9d0297c495340298914b6
uv run --no-project --python 3.12.14 --with cryptography==46.0.7 \
  python experiments/observer-admission/run.py --observer-root .observer-source \
  --bundle experiments/observer-admission/retained \
  --manifest experiments/observer-admission/provenance.json \
  --expect experiments/observer-admission/recorded.json
uv run --no-project --python 3.12.14 --with cryptography==46.0.7 \
  python experiments/observer-admission/run.py --observer-root .observer-source \
  --output /tmp/observer-admission-new \
  --expect experiments/observer-admission/recorded.json
```

The output directory must be empty. Source blobs are checked before private-copy import. The first command checks the original artifact's exact retained bytes; the second generates new keys and signatures and requires the same complete semantic outcomes. Running this fixture in another CI system supplies a new execution record. An independently operated witness still needs a separately justified operator and trust boundary.

The E6 implementation, demo and retained expected outcomes were available to the atlas runner. This is a retrospective fixture comparison; it does not establish an answer-blind replication or a result frozen before expected-answer comparison.

## Choose the claim you are submitting

These are separate claims. A submission may establish more than one, with separate evidence for each.

| claim | evidence needed | ceiling |
|---|---|---|
| Retained-byte integrity | Raw input bytes, retrieval record, algorithm, digest, byte size and verification outcome | Identifies a representation; does not establish execution, authority or an effect |
| Verifier behavior on a fixture | Pinned contract and reader, explicit mapping, complete input/result manifests and hostile controls | Applies to the selected inputs; implementation independence and operator independence are separate |
| Host-project CI dependency | A host-owned workflow at an exact commit imports or invokes the pinned package/adapter, a completed host run, retained outputs, and a maintainer-owned merge or dependency decision | A fixture rerun, development-only byte library and production runtime dependency are different uses; record the actual use |
| Observed bounded effect | Prior authority, actual effect bytes or service observations, observer reachability boundary, coverage denominator, gaps and failure behavior | Covers only the declared channel and interval |
| Independent witness or consumer operation | Named producer, runner, policy owner and key custodians; how the consumer acquired keys/head outside the candidate bundle; retained history and evidence of separate operational control | Separate signing keys, repositories, containers or directories alone do not establish custody independence |

Use claim-level results: `pass`, `fail`, `unknown`, `not-exercised` or `out-of-scope`. State the rule producing each result. Unsupported checks and unavailable observations remain visible. A signature verdict, service correlation, policy admission and observed effect must have separate fields even when their outcomes agree.

## Submit a reproducible evidence packet

1. **Fix the question before scoring.** Name the exact specification/profile revision, claim and expected scope. Pin the producer, reader/adapter, configuration, policy and input manifests. Identify any local interpretation of an unresolved contract. Record who chose the keys and witness head, and when.
2. **Preserve the delivered evidence.** Retain the original byte stream, its SHA-256, length, media type and immutable source. Record retrieval failures. Keep any normalized or redacted derivative separately, with its own digest and an explanation of what changed. Never substitute a reserialized document for a raw-byte integrity check.
3. **Record the roles and exposure.** Name the implementation author, runner, policy owner, signer and custodian for each claim. State whether they share operational control. Record which producer code, expected files, README outcomes or earlier answers the reader author and runner knew. Expected-file-blind is narrower than answer-blind.
4. **Execute the positive and hostile cases.** Retain commands, runtime/dependency pins, stdout, stderr, exit status, every attempted case and its denominator. Report missing, partial, failed and unscored checks. Do not infer a zero effect count from missing records.
5. **Freeze results before comparison.** Commit or publish the complete raw report and manifest, then publish the expected-answer comparison in a separate revision. Supply both immutable links and their order. If answers were already known, say so; freezing a report does not undo that exposure. A report signature binds the report bytes and signer, without upgrading the observations' custody.
6. **Submit the packet.** Use the run form and link the retained files. A maintainer review records the supported claims, ceilings and unresolved gaps. A register addition is proposed by pull request with its reviewed evidence links; the intake issue remains the public discussion and decision trail.

For a live capture, classify each gap as unsupported behavior, instrumentation gap, interpretation/guidance gap, missing convention, or unavailable evidence. Keep the raw capture and mapping with the gap. A proposed fix needs a later run showing what changed.

## Controls a reviewed result must survive

Select controls for the submitted claim and explain any that do not apply. Keep the positive control and all refused, failed or unknown controls in the record.

| claim under test | required discriminating control |
|---|---|
| Fixture reader | An accept-all or naive adapter must fail at least one declared negative; missing and out-of-scope cases cannot silently pass |
| Representation integrity | Change an octet; reserialize unchanged JSON; omit the digest; supply an unsupported algorithm or unavailable retrieval. Report each according to the pinned raw-byte contract |
| Authority or signature | Change the declared scope/operation, substitute an untrusted key, or alter signed bytes. Supply the exact refusal and unchanged prior consumer state where that state is part of the contract |
| Admission/history | Replay after persistence, truncate or fork history, omit a committed interval, or reset/roll back the consumer store. Report which trust assumptions make rollback detectable |
| Bounded effects | Exercise a bypass and missing observation relative to the declared channel. Retain the effect or attempted effect, record liveness and coverage gaps, and refuse an absence claim when coverage is unknown |
| Claimed independent operation | Attempt candidate-supplied trust replacement and publish who can address or replace the observer, keys, journal and retained head |

Passing these selected controls is a result for that contract and run. The register records their count and scope; it does not treat a test score as a production guarantee.

## Review, rejection and correction

A submission starts as **submitted**. Review can classify individual claims as **supported with stated limits**, **needs evidence**, **unsupported** or **out-of-scope**. These review states are separate from the measured pass/fail outcomes. Only a reviewed pull request changes the register. There is no automatic certification or promotion to independent custody.

Review returns an explicit missing field, unresolved rule, counterexample or evidence mismatch. Changed source bytes without a new revision, missing raw outputs, answer-key exposure described as blind, an accept-all control that succeeds, bundled keys described as independently pinned, and missing observations counted as success block the affected claim. A useful failed or partial run can still be retained as a gap record.

Use the [correction form](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-correction.yml) with the record ID, challenged claim, immutable counterevidence and proposed correction. A corrective pull request marks the affected claim disputed or superseded, links the replacement record and preserves the original result and review trail. Do not rewrite an old run to look like the corrected experiment. Scope or contract disagreements remain named until the relevant specification owner resolves them.

## Connections to current upstream work

The [AAIF execution-plan proposal at 99d72c8](https://github.com/aaif/wg-observability-and-traceability/blob/99d72c8484ac82f2c7128f2cb3b09e2971f8f234/working-documents/AGENT-BEHAVIOR-TRACE-MODEL-EXECUTION-PLAN.md) puts agree, evidence, interpret and contribute in sequence, with actual captures and an observed-gap register guiding later work. This lab uses that evidence-first sequence for its own submissions. [PR #60](https://github.com/aaif/wg-observability-and-traceability/pull/60) is a proposed direction; it does not commit AAIF or any agent to this lab.

The [Gemara evidence proposal at a3016f4](https://github.com/gemaraproj/gemara/blob/a3016f4ddadda4e2d4a68ab353ce430fdb62b6bf/evidence.cue) defines a citation digest over the full octet stream delivered, including a required SHA-256 support floor. Coordinates and entry IDs are lookup hints, rather than digest inputs. Its citation-integrity outcomes are `verified`, `integrity-failure` and `unverifiable`; absence of a digest makes no integrity claim. These are byte-integrity results, separate from the claim-level outcomes above. [PR #507](https://github.com/gemaraproj/gemara/pull/507) remains a pinned proposal here. A raw-octet adapter run is an open contribution route, with no completed lab result or Gemara commitment claimed.

The initial E6 record exercises the existing observer contract. Future records can connect these proposed upstream contracts only after their exact rules, inputs and measured limits are supplied. The register records adoption when a host project owns and retains the dependency run, and records independent operation only when its distinct trust requirements are demonstrated.
