# Independent evidence for AI agent actions

When an AI agent does something that matters, who can check what happened without taking the word of the party that ran it? This repository is the working framework for that question. Its centre is an atlas of agent assurance: seven layers that make claims about agents (identity and authorization, policy and runtime control, containment, tracing, receipts and transparency, evaluation, and governance and standards), what a working instance of each layer establishes, what it cannot establish on its own, and what falls between the layers.

Every number, date and status the framework prints has a row in a claim ledger, with its source, the time it was read, a command that re-derives it, and the limit of what it means.

## What is here

| path | what it is |
|---|---|
| `data/atlas.toml` | The atlas as data: the layers, the named projects and standards with their measured sizes, the mechanisms classified by who writes their record, and the seams between layers. Every atlas fact is written here and only here. |
| `CLAIMS.md` | The claim ledger. |
| `tools/rederive.py` | Re-derives every automatable row of the claim ledger and prints the recorded and the current value side by side. |
| `data/versions.toml` | The version ledger: every artifact, its version, date and status. The build adds the SHA-256 of each artifact's source. |
| `src/lab.md`, `data/lab-register.json` | The Probity Open Evidence Lab protocol, intake/correction routes and retained run register. |
| `tools/check_lab.py` | Checks register artifact hashes and measured-field bindings before the site builds. Review of claim meaning and operational independence remains explicit. |
| `tools/build.py`, `tools/template.html`, `assets/site.css` | The site build: Markdown to HTML with pandoc, failing on any warning. |
| `tools/gen_atlas.py`, `templates/atlas.md.in` | Renders the atlas page from `data/atlas.toml`. |
| `tools/check_links.py` | Checks every internal link and anchor and, with `--external`, every external URL. |
| `docs/` | The built site, for GitHub Pages to serve from this directory. |

## Release rule

Each artifact has its own release contract, and an artifact is added here when it passes that contract, not before. The version ledger lists every artifact of the framework; one that has not passed yet is shown there as held. The experiment draft retains the local PEER pilot, an immutable APS/PriorSeal fixture record, a source-pinned AGT transcript-byte result, and the public observer declaration-to-admission demo with its original CI bundle and replay controls. Separately reproduced below-agent observation and independent history remain registered designs without a qualifying result. The essay, runnable verifier demonstration and twelve-month series plan remain held.

## Re-derive and build

```sh
python3 tools/rederive.py            # recorded vs current value for every automatable claim; no credentials
python3 tools/rederive.py --strict   # exit 1 if any value moved or could not be read
python3 tools/gen_atlas.py           # render the atlas page from data/atlas.toml into src/atlas.md
python3 tools/build.py               # build docs/ (pandoc 3.x); any pandoc warning fails the build
python3 tools/build.py --check       # fail if docs/ differs from what the sources give
python3 tools/check_links.py --external
```

A read that fails is printed as `UNREAD` with its reason and is never counted as unchanged. GitHub's unauthenticated API allows 60 requests an hour, which covers one run; set `GITHUB_TOKEN` to raise the limit.

The `observer-admission` CI job checks the original pinned observer demo and the
retained signed bundle on every push and pull request. Reproduce it using the
E6 commands in `src/experiments.md`. It requires the exact source blobs, Python
3.12.14 and cryptography 46.0.7, and refuses changed authority, signed-claim
tampering and a second admission. The result remains an author-produced
same-operator PEER/artifact fixture.

The [Open Evidence Lab](https://probityai.github.io/agent-evidence-atlas/lab.html)
accepts pinned run submissions through the repository's evidence-run issue form
and corrections through the evidence-correction form. Its initial E6 record
retains the fixture's limits. Host-project CI dependence and independently
operated witnesses are separate evidence claims; listing a record supplies no
membership or endorsement. Run `python3 tools/check_lab.py` to check its local
integrity and measured-field bindings.

## The public code the framework uses

- [agent-evidence-vocabulary](https://github.com/probityai/agent-evidence-vocabulary): what an evidence claim means, and what it withholds.
- [agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors): a conformance corpus and reference verifier.
- [agent-evidence-admission](https://github.com/probityai/agent-evidence-admission): policy rules that turn verified evidence into a deployment decision.
- [jcs-admit](https://github.com/probityai/jcs-admit) and [dsse](https://github.com/probityai/dsse): Rust crates for canonical JSON and the signature envelope, published on crates.io.

The paper behind the framework is *Three Jobs, Not One* ([doi:10.5281/zenodo.21935891](https://doi.org/10.5281/zenodo.21935891)).

## Author

Sankalp Gilda.
