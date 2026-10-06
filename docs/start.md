# Choose a project

Start with the task you need.

Vectors tests how a verifier behaves. Verify checks a supplied claim against evidence bytes.

Use the catalog ID when selecting a tool or profile in a structured record. Repository names and display labels can differ from that ID.

| Task | Project |
|----|----|
| Evaluate admission policies or reserve cost before dispatch | [Probity Admission](#admission) |
| Run an APS refund example with safe retries | [Probity APS refund example](#aps-refund-retries) |
| Choose a tool or inspect recorded claims and retained runs | [Probity Atlas](#atlas) |
| Sign and verify DSSE envelopes in Rust | [dsse](#dsse) |
| Read selected retained Inspect execution profiles | [Probity native Inspect reader](#inspect-native-reader) |
| Admit and canonicalize JSON in Rust | [jcs-admit](#jcs-admit) |
| Check published MintID trace records | [Probity MintID trace reader](#mintid-trace-records-v2) |
| Record file actions or check native delegation evidence | [Probity Observer](#observer) |
| Test a verifier against conformance cases | [Probity Vectors](#vectors) |
| Install a pinned verifier and check an evidence claim | [Probity Verify](#verify) |
| Use shared definitions for agent evidence claims | [Probity Vocabulary](#vocabulary) |
| Check a selected run against retained witness anchors | [Probity witnessed run selection](#witnessed-run-selection) |

<a id="admission"></a>

## Probity Admission

Component ID: `admission`.

Provides OPA, Kyverno and policy-controller rules, plus a pre-call budget reservation API and CLI for bounded local workloads.

Draft. [Quickstart and source](https://github.com/probityai/agent-evidence-admission/blob/bbff435d11a7c0ec9bc0e8e65e6d8fc40c10b671/README.md)

<a id="aps-refund-retries"></a>

## Probity APS refund example

Profile ID: `aps-refund-retries`. Component ID: `observer`.

Runs a local APS refund example that ties retries to approved actions and retains records for a separate reader.

Prototype. [Quickstart and source](https://github.com/probityai/agent-evidence-observer/blob/753932b42b00ab8257396112c529f840396f0ce7/docs/APS-REFUND-RETRIES.md)

<a id="atlas"></a>

## Probity Atlas

Component ID: `atlas`.

Provides task-based project navigation, agent assurance documentation and an Open Evidence Lab run register.

Draft. [Quickstart and source](https://github.com/probityai/agent-evidence-atlas/blob/48b9648a277bc5177f9dce290551f385c6df2ba1/README.md)

<a id="dsse"></a>

## dsse

Component ID: `dsse`.

Signs and verifies DSSE envelopes with explicit threshold and key handling.

Released. [Quickstart and source](https://github.com/probityai/dsse/blob/35e418022b19bebedec13ebb4c31bc43b1c70caf/README.md)

<a id="inspect-native-reader"></a>

## Probity native Inspect reader

Profile ID: `inspect-native-reader`. Component ID: `observer`.

Reads selected retained Inspect execution profiles offline, preserving errors and unstarted attempts. Inspect accepted the catalog entry; its live listing was awaiting publication on October 5, 2026.

Prototype. [Quickstart and source](https://github.com/probityai/agent-evidence-observer/blob/71ac0b2126473316655184235000647a6dd0f5cf/docs/NATIVE-CONSUMER-CI.md)

<a id="jcs-admit"></a>

## jcs-admit

Component ID: `jcs-admit`.

Checks raw JSON input before producing its RFC 8785 canonical form.

Released. [Quickstart and source](https://github.com/probityai/jcs-admit/blob/fb32a68aa2772e51cee32bc14835075d88af3953/README.md)

<a id="mintid-trace-records-v2"></a>

## Probity MintID trace reader

Profile ID: `mintid-trace-records-v2`. Component ID: `jcs-admit`.

Reads published MintID trace records after raw JSON admission and checks source-bound evidence and actor attribution.

Prototype. [Quickstart and source](https://github.com/probityai/jcs-admit/blob/fb32a68aa2772e51cee32bc14835075d88af3953/interop/mintid-trace-records-v2/README.md)

<a id="observer"></a>

## Probity Observer

Component ID: `observer`.

Records brokered file actions with signed packets and history, and reads selected native delegation evidence offline.

Prototype. [Quickstart and source](https://github.com/probityai/agent-evidence-observer/blob/753932b42b00ab8257396112c529f840396f0ce7/README.md)

<a id="vectors"></a>

## Probity Vectors

Component ID: `vectors`.

Provides conformance cases and reference verifiers for selected agent evidence formats.

Released. [Quickstart and source](https://github.com/probityai/agent-evidence-vectors/blob/44042ae1a8cbde9444e8ea24e6690a7e773af65b/README.md)

<a id="verify"></a>

## Probity Verify

Component ID: `verify`.

Checks supplied evidence bytes through claim-specific offline adapters. Its README links to source-pinned installation and checked task recipes.

Unreleased. [Quickstart and source](https://github.com/probityai/probity-verify/blob/437e484bd81e3d1eb1b9ad7230124a434a7a0ef6/README.md)

<a id="vocabulary"></a>

## Probity Vocabulary

Component ID: `vocabulary`.

Defines versioned terms and crosswalks for claims about agent execution.

Released. [Quickstart and source](https://github.com/probityai/agent-evidence-vocabulary/blob/4029a7801e0ec61a9818fd1e6c1cbd236e2c82bc/README.md)

<a id="witnessed-run-selection"></a>

## Probity witnessed run selection

Profile ID: `witnessed-run-selection`. Component ID: `observer`.

Checks a supplied run against consumer-retained witness anchors, plan and control pins, and execution closure.

Prototype. [Quickstart and source](https://github.com/probityai/agent-evidence-observer/blob/d53776c7b783abbce42a3422f56ed390dfedd2f2/docs/WITNESSED-RUN-SELECTION.md)

<a id="run-and-share-a-check"></a>

## Run and share a check

The [Open Evidence Lab](lab.md) holds replayable runs and accepts new results and corrections. For scripted lookups, use the [automation guide](automation.md).

[HTML view](start.html) | [Agent guide](llms.txt)
