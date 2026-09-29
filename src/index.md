---
title: "Independent evidence for AI agent actions"
subtitle: "When an AI agent does something that matters, who can check what happened, without taking the word of the party that ran it?"
status: "Version 1.2, 29 September 2026. Each artifact below carries its own version and status. Released artifacts and labelled drafts are linked; the rest are named without a link."
description: "Sankalp Gilda's working framework on independently checkable evidence for AI agent actions: an atlas of agent assurance, a claim ledger and the public code behind them."
---

I work on a pair of questions: what evidence should exist after an AI agent takes a consequential action, and who decides whether that evidence is enough. Independent evaluators, regulators and the parties an agent affects all need an answer that does not reduce to the account of the company that ran the agent.

Where a piece has not been released, the [version ledger](versions.html) says so, and it records what changed in each piece and when.

| artifact | what it is | version | date | status |
|---|---|---|---|---|
| [Atlas](atlas.html) | Seven families of mechanisms that make claims about agents (identity, policy, containment, observation, records, evaluation, governance), 45 named projects and standards, 18 mechanisms classified by who writes their record, and what none of them establishes alone | 0.1 preview | 2026-09-27 | [published]{.label .published} |
| [Claim ledger](claims.html) | The source, read time, re-derive command and limit behind the numbers, dates and statuses on this site, re-checked on every weekly re-derive | 0.4 | 2026-09-29 | [draft]{.label .draft} |
| [Version ledger](versions.html) | Each artifact's version, date and status, beside a digest of the source it was built from, updated with every build | site build 0.2 | 2026-09-29 | [draft]{.label .draft} |
| [Experiments](experiments.html) | A three-interval local PEER pilot that exposes a missed transient effect, plus registered tests for below-agent observation and independently witnessed history | 0.1 | 2026-09-29 | [draft]{.label .draft} |
| [*Three Jobs, Not One*](https://doi.org/10.5281/zenodo.21935891) | The paper behind the framework: why policy, containment and evidence are separate jobs, each needing its own mechanism | Zenodo version 6 | 2026-08-14 | [published]{.label .published} on Zenodo |

Three more pieces are in preparation, each held until it passes its release checks: an essay on what independent evaluators should verify, a runnable verifier demonstration, and a twelve-month series plan. The [experiment draft](experiments.html) publishes the local PEER pilot and two designs while withholding any claim of below-agent observation or independent history.

## The public code

Three repositories and two Rust crates hold the reference work the atlas draws on.

| repository | release | status | what it holds |
|---|---|---|---|
| [agent-evidence-vocabulary](https://github.com/probityai/agent-evidence-vocabulary) | v0.3.0 | [draft]{.label .draft} | What an evidence claim means, and what it withholds |
| [agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) | v0.13.0 | [published]{.label .published} | A conformance corpus and reference verifier |
| [agent-evidence-admission](https://github.com/probityai/agent-evidence-admission) | no release yet | [draft]{.label .draft} | Policy rules that turn verified evidence into a deployment decision |
| [jcs-admit](https://crates.io/crates/jcs-admit) and [dsse](https://crates.io/crates/dsse) | 0.1.0 on crates.io | [published]{.label .published} | Rust crates for canonical JSON and the signature envelope |

## Agent action assurance

The proposed consumer contract joins the checks an operator needs before relying on an agent's action: authority, exact-call admission, invocation, observed effect, vantage and coverage, signed bytes, history, and the consumer decision. Its first test is a file write retried after a lost response. The negative cases include a duplicate effect, a missing interval, and a transient bypass that a final snapshot misses.

This is a proposed end-to-end requirement, not an end-to-end conformance result. The current corpora test parts of it. The [experiment](experiments.html) demonstrates a snapshot failure under a PEER prototype; it has no isolated agent or separate witness operator. The next result needs both a producer outside the agent's reach and an independent consumer replay. A gate pass or a signed receipt can then be checked alongside the effect it purports to govern.

## Peer-reviewed work

Sankalp Gilda and Shlok Gilda, "Position: Evaluation Scores Are Perishable Knowledge Claims", Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM), 2026. [doi:10.18653/v1/2026.gem-main.80](https://doi.org/10.18653/v1/2026.gem-main.80)
