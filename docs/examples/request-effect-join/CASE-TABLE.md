# A changed call and a later changed file

`giskard09` selected [execution-join-ref-v1](https://github.com/giskard09/argentum-core/blob/f4d989052bb3a61691b1b156cd6dd655793fea4f/docs/spec/execution-join-ref-v1.md)
for [the Lab's request/effect case](https://github.com/probityai/agent-evidence-atlas/issues/49#issuecomment-6072781535).
This table freezes the two situations separately so a producer, reader and file-effect observer can compare the same cases.

The producer's selected contract owns its identifier and failure-code semantics.
The cases below are our proposed experiment inputs, not a new version of that contract or a completed native run.

| Case | Decision and dispatch | Effect and later observation | Expected distinction |
| --- | --- | --- | --- |
| Unchanged approved call | The permit covers the exact dispatched path, identity, tool and arguments. | The recorded write matches that attempt. No later observation is supplied. | Establish the supported join, with later state unassessed. |
| Rewrite before dispatch | The permit covers the original call; the runtime dispatches changed arguments without a covering decision. | Whether a later file happens to match is separate. | `EFFECTIVE_CALL_REBINDING_FAILED`, the selected contract's invariant 6. A tidy internal chain cannot repair the missing approval. |
| Approved rewrite | The runtime obtains a decision covering `effective_action_ref` before dispatch. | The write matches the newly authorized attempt. | Assess the effective call under its own covering decision. Keep the original request and rewrite visible. |
| Later changed file | The original dispatch and recorded write match their covering decision. | A fresh read later sees different bytes. | Preserve the original result. Report the later difference separately. `POST_COMMIT_DIVERGENCE` is a proposed new observation code, not an adopted verifier result. |
| Changed evidence preimage | A claimed reference no longer recomputes from its supplied preimage. | This does not establish a later external change. | `DIGEST_MISMATCH` keeps the selected contract's digest meaning. |
| Missing later observation | A supported original join is supplied. | No fresh file read is supplied. | Keep later state unknown. Do not infer that the file remained unchanged. |

## What to retain for a run

Retain the original and effective preimages, covering decisions, attempt identity and original terminal output.
For a later read, retain its own target, bytes, time and observer identity.
Keep the producer's original result beside the reader's comparison; a later observation must not rewrite it.
Missing material stays missing rather than being filled from a current configuration.

The proposed post-commit observation needs an explicit consumer decision before promotion:
does it describe a changed resource, or does it reject a claim that the current state still matches?
Either way, it must not turn an earlier matching committed action into a false digest failure.

## Target coverage is another relationship

For a target-binding reader, freeze `declared_target`, `hashed_action_target` and
`executor_configured_target` as separate fields in the experiment's projection.
These are experiment field names, not aliases for a producer's native schema.

| Projection | Reader boundary |
| --- | --- |
| Hashed target absent | Target coverage is not established. |
| Hashed target differs from declared target | The declared/action relationship conflicts and must refuse. |
| Hashed target equals declared target; executor is configured for another target | The first relationship can pass. Actual dispatch remains a separate executor observation. |

Do not attribute an executor-only divergence to a reader that never observes dispatch.
Likewise, an executor configuration is not proof of where an actual request went.

## Open contributions

Bring the pinned producer verifier and vectors, run the same cases with another reader,
or retain a file-effect observation. We maintain the case table and the comparison we contribute.
Case authors, implementation authors and run operators receive separate credit.
The [approved SQL example](../approved-sql/README.md) already exercises the parallel distinction
between a matching recorded commit and a later state difference.

## Producer verifier run

`giskard09` published a verifier and nine vectors for these cases at
[`execution-join-ref-remora-bridge@f900615`](https://github.com/giskard09/execution-join-ref-remora-bridge/tree/f900615),
derived from a run of the REMORA effect bridge. We reran `python3 verify.py vectors.json` at that commit
on CPython 3.13.15; all nine checks passed with these outcomes:

| Vector | Outcome |
| --- | --- |
| AR-00 | `AUTHORIZED_EFFECTIVE_CALL` |
| AR-01, AR-02, AR-03 | `EFFECTIVE_CALL_REBINDING_FAILED` |
| AR-04 | `NOT_MODELED` (the policy/context digest is outside the `action_ref` preimage) |
| AR-05 | `POST_COMMIT_DIVERGENCE` (proposed code; original result preserved) |
| APPROVED-REWRITE | `AUTHORIZED_EFFECTIVE_CALL` |
| CHANGED-PREIMAGE | `DIGEST_MISMATCH` |
| MISSING-OBSERVATION | `LATER_STATE_UNKNOWN` |

Another reader can run the same nine vectors and add its outcomes beside these.
