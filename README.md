# Independent evidence for AI agent actions

An atlas of agent assurance, with a claim ledger that re-derives every number it prints.

It is for evaluators, standards authors and regulators who need to know what an agent's record can show without trusting the party that ran the agent.

The atlas covers seven layers that make claims about agents: identity and authorization, policy and runtime control, containment, tracing, receipts and transparency, evaluation, and governance and standards. For each it says what a working instance establishes, what it cannot establish alone, and what falls between the layers. Every number, date and status has a row in [CLAIMS.md](CLAIMS.md) with its source, the time it was read, a command that re-derives it, and the limit of what it means.

## Quick start

Pin the repository to a commit and re-derive the ledger. It needs Python 3.11 or later and no credentials:

```sh
git clone https://github.com/probityai/agent-evidence-atlas && cd agent-evidence-atlas
git checkout 4b6cc7e58571175b998a16170437f31df8483351
python3 tools/rederive.py
```

It prints the recorded and the current value of each row, then a count. On 2 October 2026 it printed, in part:

```text
re-derived at 2026-10-02T11:04:50Z
CHANGED  A-stars modelcontextprotocol/modelcontextprotocol recorded '9355' current '9361'
CHANGED  A-stars open-policy-agent/opa                recorded '12297' current '12304'
same     A-39d                                        recorded 'open' current 'open'
same     I-01                                         recorded 'v6 2026-08-14' current 'v6 2026-08-14'
9 of 34 unchanged; 0 could not be read
```

Star counts move daily, so your counts will differ. A row that cannot be read prints as `UNREAD` and is never counted as unchanged; `--strict` exits 1 on any moved or unread value.

Check retained run records locally with `python3 tools/check_lab.py --list`. To read one record in an automated job, use `python3 tools/check_lab.py --record E6-observer-admission --json`. The checker validates the complete register before emitting output, which includes the record's original results, roles, review state and limits.

## Status

Version 0.6-draft, 1 October 2026 (`VERSION`). Each artifact carries its own version and status in [data/versions.toml](data/versions.toml); one that has not passed its release contract is listed as held.

## Docs

| Page | What it covers |
|---|---|
| [Site](https://probityai.github.io/agent-evidence-atlas/) | The framework, the atlas and the version ledger |
| <a name="what-is-here"></a><a name="release-rule"></a><a name="re-derive-and-build"></a>[Working in the repository](https://probityai.github.io/agent-evidence-atlas/repository.html) | What each file is, the release rule, and the build and re-derive commands |
| [Experiments](https://probityai.github.io/agent-evidence-atlas/experiments.html) | The registered experiments and their results |
| [Open Evidence Lab](https://probityai.github.io/agent-evidence-atlas/lab.html) | Submitting a pinned run or a correction |
| [Claim ledger](https://probityai.github.io/agent-evidence-atlas/claims.html) | Every claim with its source and re-derive command |

<a name="the-public-code-the-framework-uses"></a>The public code the framework uses: [agent-evidence-vocabulary](https://github.com/probityai/agent-evidence-vocabulary) (what an evidence claim means), [agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) (a conformance corpus and reference verifier), [agent-evidence-admission](https://github.com/probityai/agent-evidence-admission) (policy rules that turn verified evidence into a deployment decision), and the Rust crates [jcs-admit](https://github.com/probityai/jcs-admit) and [dsse](https://github.com/probityai/dsse). The paper behind it is *Three Jobs, Not One* ([doi:10.5281/zenodo.21935891](https://doi.org/10.5281/zenodo.21935891)).

<a name="author"></a>Author: Sankalp Gilda.
