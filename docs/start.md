# Choose a project

Start with the task you need.

Vectors tests how a verifier behaves. Verify checks a supplied claim against evidence bytes.

| Task | Project |
|----|----|
| Evaluate admission policies or reserve cost before dispatch | [Probity Admission](#admission) |
| Choose a tool or inspect recorded claims and retained runs | [Probity Atlas](#atlas) |
| Sign and verify DSSE envelopes in Rust | [dsse](#dsse) |
| Admit and canonicalize JSON in Rust | [jcs-admit](#jcs-admit) |
| Record file actions or check native delegation evidence | [Probity Observer](#observer) |
| Test a verifier against conformance cases | [Probity Vectors](#vectors) |
| Install a pinned verifier and check an evidence claim | [Probity Verify](#verify) |
| Use shared definitions for agent evidence claims | [Probity Vocabulary](#vocabulary) |

<a id="admission"></a>

## Probity Admission

Provides OPA, Kyverno and policy-controller rules, plus a pre-call budget reservation API and CLI for bounded local workloads.

Draft. [Quickstart and source](https://github.com/probityai/agent-evidence-admission/blob/bbff435d11a7c0ec9bc0e8e65e6d8fc40c10b671/README.md)

<a id="atlas"></a>

## Probity Atlas

Provides task-based project navigation, agent assurance documentation and an Open Evidence Lab run register.

Draft. [Quickstart and source](https://github.com/probityai/agent-evidence-atlas/blob/89aea5fd58850247da3aab9e0e539c20625de35b/README.md)

<a id="dsse"></a>

## dsse

Signs and verifies DSSE envelopes with explicit threshold and key handling.

Released. [Quickstart and source](https://github.com/probityai/dsse/blob/fa96f343623a520c38cb213c1315ee9bfa1bb3c0/README.md)

<a id="jcs-admit"></a>

## jcs-admit

Checks raw JSON input before producing its RFC 8785 canonical form.

Released. [Quickstart and source](https://github.com/probityai/jcs-admit/blob/b3ecf0a36d6e72eef1ee808678811f42787f2c23/README.md)

<a id="observer"></a>

## Probity Observer

Records brokered file actions with signed packets and history, and reads selected native delegation evidence offline.

Prototype. [Quickstart and source](https://github.com/probityai/agent-evidence-observer/blob/1ec93df92b49239175147c2b9f3ccda87a090cd1/README.md)

<a id="vectors"></a>

## Probity Vectors

Provides conformance cases and reference verifiers for selected agent evidence formats.

Released. [Quickstart and source](https://github.com/probityai/agent-evidence-vectors/blob/308c5b4401b18d42ed73dea80459375932e6b8e8/README.md)

<a id="verify"></a>

## Probity Verify

Checks supplied evidence bytes through claim-specific offline adapters. Its README links to source-pinned installation and checked task recipes.

Unreleased. [Quickstart and source](https://github.com/probityai/probity-verify/blob/437e484bd81e3d1eb1b9ad7230124a434a7a0ef6/README.md)

<a id="vocabulary"></a>

## Probity Vocabulary

Defines versioned terms and crosswalks for claims about agent execution.

Released. [Quickstart and source](https://github.com/probityai/agent-evidence-vocabulary/blob/8c80579ae613d7ae07982321e13a6091c402b2a8/README.md)

<a id="run-and-share-a-check"></a>

## Run and share a check

The [Open Evidence Lab](lab.md) holds replayable runs and accepts new results and corrections. For scripted lookups, use the [automation guide](automation.md).

[HTML view](start.html) | [Agent guide](llms.txt)
