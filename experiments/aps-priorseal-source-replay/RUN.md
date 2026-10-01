# APS and PriorSeal source replay

This is Probity's October 1 reproduction of the pinned Frequency review adapter. It checks that the adapter read the APS owner fixtures at their declared commit, that PriorSeal's copy matches all 17 declared fixture files, and that a fresh run gives the recorded claim results. It also retains failed runs for a changed copy, missing owner, omitted owner argument and stale report.

The verifier here is the [Frequency review adapter](https://github.com/altrudev/Frequency-Federation-Review/tree/4162622af24c94efb843f53aa27940ffd1256ad6/capsules/aps-priorseal-v0.1), executed without modification. This reproduction is distinct from [Probity's earlier independent E2 checker](https://github.com/probityai/agent-evidence-vectors/tree/00f5acab880bffc5ee8fe124f3a015d3ed970514/interop/aps-priorseal-e2-2026-09-30), which did not exercise the PriorSeal signature checks. The two results answer different questions.

## Inputs and result

| Input | Revision or SHA-256 |
| --- | --- |
| Frequency review capsule | `4162622af24c94efb843f53aa27940ffd1256ad6` |
| Adapter `verify.mjs` | `5f5cc203c921ecd576b81ee5d22063d39efc3ec74cc0b3aa75d1e41916e5cad3` |
| Adapter lockfile | `2ca396b3f9b357f5a79e3c6ff7d6dbd9d33ee179c5132792608a8e330e014c7a` |
| APS owner fixtures | `aeoess/agent-passport-system@948f99b85343bef2c6fa677c8543965caacfc087` |
| PriorSeal copied fixtures and observations | `imokokok/PriorSeal@d749d2691c3e6be139de4020e7b27cdafca2c428` |
| Owner and copy manifest | `2bf365bc9124ecfc943d5be86c34e8e0cacd51a5929b8d0c906e633a017231f9` |

The clean run produced 14 `ESTABLISHED`, 3 `CONTRADICTED` and 5 `NOT_ESTABLISHED` claims. The three contradictions are the expired decision's validity at the fixed reference time and the over-limit observation's exact-call and cap checks. The five unresolved claims cover live-chain execution, decision single use, live currency enforcement, an independently operated witness and production adoption. The declared positive and over-limit observations are producer fixtures. The adapter's Ed25519 and EIP-712 signature checks validate bytes against its preselected public test keys. They do not establish the real-world identity or custody of those keys, a chain effect, or independent observation.

Changing a copied fixture byte exits 1 without a report. An absent owner root exits 1 without a report; omitting `--aps-owner` exits 2. A failed run does not remove a report already at the output path. The replay therefore accepts a result only if the process exits zero **and** the output path was absent before the run and exists afterward.

## Run from clean checkouts

Use Node.js 20 or later, npm and Git. From this repository's root:

```sh
replay_dir=$(mktemp -d)
git clone https://github.com/altrudev/Frequency-Federation-Review.git "$replay_dir/capsule"
git -C "$replay_dir/capsule" checkout --detach 4162622af24c94efb843f53aa27940ffd1256ad6
git clone https://github.com/aeoess/agent-passport-system.git "$replay_dir/aps"
git -C "$replay_dir/aps" checkout --detach 948f99b85343bef2c6fa677c8543965caacfc087
git clone https://github.com/imokokok/PriorSeal.git "$replay_dir/priorseal"
git -C "$replay_dir/priorseal" checkout --detach d749d2691c3e6be139de4020e7b27cdafca2c428
(cd "$replay_dir/capsule/capsules/aps-priorseal-v0.1/adapter" && npm ci --ignore-scripts --no-audit --no-fund)
node experiments/aps-priorseal-source-replay/run.mjs \
  "$replay_dir/capsule" \
  "$replay_dir/aps" \
  "$replay_dir/priorseal" \
  "$replay_dir/result"
```

`result` must not exist before the command. `run.mjs` checks the Git revisions, adapter and lockfile, manifests, payment inputs and producer report by digest before it starts the adapter. It runs the adapter self-test and five cases, then checks all 22 claim states and writes `clean.json`, `receipt.json` and the stale-output control in the new output directory. The failed controls create no new report. Keep the generated directory out of Git; the public package contains no copied third-party implementation, fixtures or full adapter report.

`recorded.json` contains the SHA-256 of one locally generated report. The adapter includes a generation time, so a fresh run's report digest changes; the replay compares claim results and case outcomes, not that historical digest. The runner pins the adapter source and lockfile, while the documented `npm ci` installs dependencies. It does not independently attest the installed `node_modules` tree or Node runtime bytes.

The dedicated GitHub workflow repeats this procedure with Node 20 when this experiment changes. It retains only Probity's `receipt.json` as a CI artifact; the source checkouts and full generated adapter report stay within that job.

## Limits and next decisions

This is a local technical review of public producer fixtures, with the Frequency adapter's expected claims visible before the run. It is not answer-blind, an independent second verifier, the federation's formal pilot, mutation adequacy, commercial use, approval to publish a formal result, outside-operator custody or host-project adoption. A formal run needs its separately confirmed scope. The planned authenticity and decision-binding mutations need discriminating fixtures and a separate adequacy decision. An actual action/effect pilot needs an externally selected trust policy, live observation and a consumer decision bound to the observed bytes.

The capsule's [review-only notice](https://github.com/altrudev/Frequency-Federation-Review/blob/4162622af24c94efb843f53aa27940ffd1256ad6/REVIEW-ONLY-NOTICE.md) permits technical review and reproducibility assessment, but withholds commercial incorporation and redistribution of modified or derivative Frequency implementations. This runner invokes that repository by reference. It copies none of its implementation or fixtures and makes no partnership or endorsement claim. The APS fixtures are from an Apache-2.0 repository; PriorSeal's repository uses MIT. Their own notices govern their bytes.
