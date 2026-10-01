---
title: "Independent evidence for AI agent actions"
subtitle: "When an AI agent does something that matters, who can check what happened, without taking the word of the party that ran it?"
status: "Version 1.5, 1 October 2026. Each artifact below carries its own version and status. Released artifacts and labelled drafts are linked; the rest are named without a link."
description: "Sankalp Gilda's working framework on independently checkable evidence for AI agent actions: an atlas of agent assurance, a claim ledger and the public code behind them."
---

I work on a pair of questions: what evidence should exist after an AI agent takes a consequential action, and who decides whether that evidence is enough. Independent evaluators, regulators and the parties an agent affects all need an answer that does not reduce to the account of the company that ran the agent.

Where a piece has not been released, the [version ledger](versions.html) says so, and it records what changed in each piece and when.

| artifact | what it is | version | date | status |
|---|---|---|---|---|
| [Probity Open Evidence Lab](lab.html) | Run register, reproducible E6 starting point, evidence submissions, hostile controls and correction protocol | 0.1 | 2026-10-01 | [draft]{.label .draft} |
| [Atlas](atlas.html) | Seven families, 45 named projects and standards, 18 mechanisms, and pinned signature, transcript-byte and consumer-admission limits | 0.4 preview | 2026-10-01 | [draft]{.label .draft} |
| [Claim ledger](claims.html) | The source, read time, re-derive command and limit behind the numbers, dates and statuses on this site, re-checked on every weekly re-derive | 0.7 | 2026-10-01 | [draft]{.label .draft} |
| [Version ledger](versions.html) | Each artifact's version, date and status, beside a digest of the source it was built from, updated with every build | site build 0.5 | 2026-10-01 | [draft]{.label .draft} |
| [Experiments](experiments.html) | The PEER pilot, APS/PriorSeal limits, AGT byte reproduction, pinned observer admission/replay and two registered designs | 0.3 | 2026-10-01 | [draft]{.label .draft} |
| [*Three Jobs, Not One*](https://doi.org/10.5281/zenodo.21935891) | The paper behind the framework: why policy, containment and evidence are separate jobs, each needing its own mechanism | Zenodo version 6 | 2026-08-14 | [published]{.label .published} on Zenodo |

Three more pieces are in preparation, each held until it passes its release checks: an essay on what independent evaluators should verify, a runnable verifier demonstration, and a twelve-month series plan. The [experiment draft](experiments.html) adds source-pinned decision-call, byte and consumer-admission results to the local PEER pilot. Separately reproduced below-agent observation and independently operated history remain registered designs without a qualifying result.

## The public code

Three repositories and two Rust crates hold the reference work the atlas draws on.

| repository | release | status | what it holds |
|---|---|---|---|
| [agent-evidence-vocabulary](https://github.com/probityai/agent-evidence-vocabulary) | v0.3.0 | [draft]{.label .draft} | What an evidence claim means, and what it withholds |
| [agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) | v0.16.0 | [published]{.label .published} | A conformance corpus and reference verifier |
| [agent-evidence-admission](https://github.com/probityai/agent-evidence-admission) | no release yet | [draft]{.label .draft} | Policy rules that turn verified evidence into a deployment decision |
| [jcs-admit](https://crates.io/crates/jcs-admit) and [dsse](https://crates.io/crates/dsse) | 0.1.1 on crates.io | [published]{.label .published} | Rust crates for canonical JSON and the signature envelope |

## Agent action assurance

The proposed consumer contract joins the checks an operator needs before relying on an agent's action: authority, exact-call admission, invocation, observed effect, vantage and coverage, signed bytes, history, and the consumer decision. Its first test is a file write retried after a lost response. The negative cases include a duplicate effect, a missing interval, and a transient bypass that a final snapshot misses.

This is a proposed end-to-end requirement, not an end-to-end conformance result. The corpora test parts of it. The retained PEER pilot demonstrates a snapshot failure. The [pinned observer admission demo](experiments.html#observer-consumer-admission) now joins a prior declaration, one brokered durable effect, signed history and a persisted consumer decision; its replay, changed-authority and signed-claim controls refuse. This author-produced artifact has no separate witness or consumer operator. The next qualifying result still needs a producer outside the agent's reach and an independently operated consumer replay.

## Peer-reviewed work

Sankalp Gilda and Shlok Gilda, "Position: Evaluation Scores Are Perishable Knowledge Claims", Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM), 2026. [doi:10.18653/v1/2026.gem-main.80](https://doi.org/10.18653/v1/2026.gem-main.80)
