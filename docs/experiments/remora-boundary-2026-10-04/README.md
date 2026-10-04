# REMORA execution-boundary run records

This packet holds the run records for REMORA's three frozen execution-boundary contracts, read by the separate reader in `probityai/agent-evidence-vectors`. The producer bytes are REMORA `fe324dd734734d9227aa894330ac52c2bb916b94`. The reader ran at `308c5b4401b18d42ed73dea80459375932e6b8e8`, the merge of the reviewed head `bf294ec7d01033cd967f45a0eb6b65c5b50ecc56`; the reader files and workflow are byte-identical between the two.

| Contract | Package digest | Claim | Cases | Result per case |
|---|---|---|---|---|
| `exact-call-binding-v1` | `sha256:48dd143c4e4f50d69063df8e2a2993a5d240a50d81dc4330b225015ea432c77c` | `exact_call_binding` | 13 | 11 `ESTABLISHED`, 2 `NOT_ESTABLISHED` (unsigned, tampered) |
| | | `single_use_authorization` | 2 | 2 `ESTABLISHED` |
| `fresh-authority-v1` | `sha256:234c57d0ed79b0cd87e702b2efbc52e99af1c619bd7fed2aef7be5c14964b691` | `fresh_authority_at_dispatch` | 14 | 13 `ESTABLISHED`, 1 `NOT_ESTABLISHED` (unsigned lease) |
| `effect-evidence-v1` | `sha256:26c437c65a5c3890a0672845dd9e1e54b03c38ae5f05a6fbe7131402b952034c` | `effect_state_distinction` | 12 | 12 `ESTABLISHED` |

All 41 case results equal the fixture expectations and REMORA's eight author-run records at the same revision. No case is `CONTRADICTED`. The same run also passed 13 additional cases, 8 malformed-input refusals, 9 source mutations and 20 Verify decisions.

Each contract's `external-run-record-v1` is extracted unchanged from the reader's native output: [exact-call-binding-v1](exact-call-binding-v1.external-run-record-v1.json), [fresh-authority-v1](fresh-authority-v1.external-run-record-v1.json), [effect-evidence-v1](effect-evidence-v1.external-run-record-v1.json). Each states `SECOND_IMPLEMENTATION`, operator `EXTERNAL` and `NOT_INDEPENDENT`, as the pinned reader emits them. Under REMORA's lifecycle rule that supports `REPRODUCED`, not `EXTERNALLY_VERIFIED`.

What the reader recomputed: each package digest from its manifest, the SHA-256 of every producer input it reads, every case outcome from the fixture inputs, and test-key HMAC signatures it creates and checks itself. What it only read: the `reference_verifier.py` digest (the file is not retained or executed), fixture premises such as observation completeness, and the expected outcomes it compares against. The effect `hash` rule stays unsupported until the contract defines its preimage; no frozen case uses it.

Both original Actions archives from [run 37232420650](https://github.com/probityai/agent-evidence-vectors/actions/runs/37232420650) are retained, for CPython 3.13.15 and 3.14.7. Their member inventories are in [provenance.json](provenance.json). Run the data-only check:

```sh
python3 validate_capsule.py
```

It authenticates every archive member, recomputes the three package digests from the retained producer bytes, derives [report.json](report.json) from the native output, requires the two interpreters to agree on every case outcome, and requires the three extracted records to equal the originals. It does not run the reader. The installed replay is in the [reader README](https://github.com/probityai/agent-evidence-vectors/tree/308c5b4401b18d42ed73dea80459375932e6b8e8/interop/remora-boundary-readers).

Probity wrote the reader and operated the run. These records establish no production safety, no authority over REMORA decisions, no independent effect custody and no lifecycle change; the producer's review decides how REMORA records them.
