---
title: "Claim ledger"
subtitle: "Every number, date, status and quotation on this site, with its source, when it was read, how to re-derive it, and what it does not mean"
status: "Draft, version 0.4, 29 September 2026. Star counts were refreshed at 2026-09-27 11:49 UTC by tools/refresh_stars.py; earlier automatable rows were last re-derived at 2026-09-27T09:52:44Z. The experiment pilot was run on 2026-09-29. Each value keeps its read time."
description: "The source, read time, re-derive command and limit for every claim on the site."
---

## How to use this ledger

- **Re-derive the automatable rows** with `python3 tools/rederive.py` from the repository root. It needs no credentials, prints the recorded and the current value for each row, and prints `UNREAD` with a reason when a source cannot be read; an unread row is never reported as unchanged. `--strict` exits 1 on any change.
- **Read times** are UTC, and each read cell states its row's cadence: star counts, pull-request states and link checks 7 days, standards and project statuses 30 days, while published versions and dated events do not expire. `data/claim_cadence.toml` holds the cadence of every row. When a row's read date plus its cadence has passed, this page marks the row stale as it loads. [With scripts off, compare each read date with its cadence.]{#stale-count}
- **Captures.** Every web page cited was saved when it was read. The capture log records URL, HTTP status, UTC time and SHA-256 for each one.

Each row's identifier starts with the letter of the page it covers: `A` for the atlas, `I` for the home page, `E` for the experiments, and `L` for the site's links. Rows that cite a local unpublished source say so; they are not independently reproducible until those exact source bytes are published.

## Atlas

| id | claim as printed | source | read (UTC) | re-derive | limit |
|---|---|---|---|---|---|
| A-03 | WIMSE: active working group; seven working-group drafts, including an AI identity management draft | IETF Datatracker, WIMSE documents page | 2026-09-27 00:47 | open <https://datatracker.ietf.org/wg/wimse/documents/> | Working-group drafts are not standards |
| A-04 | RFC 8693 is a Proposed Standard; OAuth 2.1 is a working-group draft | RFC Editor info page; Datatracker `draft-ietf-oauth-v2-1` (revision 16) | 2026-09-27 00:47 | open both pages | Standards-track status, not deployment |
| A-05 | MCP authorization specification version 2026-07-28 states that authorization is optional | modelcontextprotocol.io, authorization page: "Authorization is OPTIONAL for MCP implementations" | 2026-09-27 00:47 | open the page | Applies to that specification version |
| A-45 | The OpenID Foundation writes that identity rooted in one infrastructure does "not naturally extend across organizations that do not share visibility or control over infrastructure" | OpenID Foundation, *Identity Management for Agentic AI* (October 2025), <https://openid.net/wp-content/uploads/2025/10/Identity-Management-for-Agentic-AI.pdf>; the full sentence gives an example in parentheses | 2026-09-27 01:50 | open the PDF and search the quoted clause | The foundation's analysis of cross-organization identity, not a test |
| A-06 | Open Policy Agent: CNCF Graduated (2021); 12,278 stars | cncf.io; GitHub API | 2026-09-27 00:47; 11:49 | `rederive.py` A-stars | Maturity level and attention, not adoption or quality |
| A-07 | Kyverno: CNCF Graduated (2026-03-16); 8,187 stars | cncf.io; GitHub API | 2026-09-27 00:47; 11:49 | `rederive.py` A-stars | Maturity level and attention, not adoption or quality |
| A-09 | agentgateway: a Linux Foundation project, per its README; 5,059 stars | the project's README; GitHub API | 2026-09-27 00:56; 11:49 | `rederive.py` A-stars | Foundation status is the project's own statement; the CNCF project URL returned 404 |
| A-stars | Every GitHub star count on the atlas (25 entries that name a repository) | GitHub API `repos/<owner>/<repo>` | 2026-09-27 11:49, recorded as `stars_read` in `data/atlas.toml` | `python3 tools/rederive.py` reads every entry with a `repo` in `data/atlas.toml`; `python3 tools/refresh_stars.py` rewrites them all with one read time | Stars measure attention, not quality or use |
| A-16 | OpenTelemetry: CNCF Graduated (2026-05-11); generative-AI and agent-span conventions marked "Development" | cncf.io; the conventions' own Markdown in `open-telemetry/semantic-conventions-genai` | 2026-09-27 00:47; 00:51 | open both | "Development" is the conventions' own stability label |
| A-18 | in-toto: CNCF Graduated (2025-02-10); attestation specification v1.2 | cncf.io; the specification README ("Latest version: v1.2") | 2026-09-27 00:47; 00:49 | open both | Maturity level and a specification version, not adoption |
| A-19 | Sigstore: an OpenSSF project | openssf.org project list | 2026-09-27 00:52 | open the openssf.org project list | The OpenSSF page read does not show a maturity stage |
| A-20 | RFC 9943 and RFC 9942: Proposed Standards, June 2026 | IETF Datatracker, SCITT documents page | 2026-09-27 00:47 to 00:52 | open the page | Standards-track status, not deployment |
| A-21 | C2PA: a Joint Development Foundation project; specification 2.4 current | spec.c2pa.org specifications index | 2026-09-27 00:49 | open the page | Governance and a version, not adoption |
| A-22 | RFC 9162: Experimental (2021) | RFC Editor | 2026-09-27 00:47 | open <https://www.rfc-editor.org/info/rfc9162> | Experimental status, as the RFC itself states |
| A-23 | RFC 8785: Informational | RFC Editor | 2026-09-27 00:47 | open <https://www.rfc-editor.org/info/rfc8785> | Informational status; it defines no requirement |
| A-24 | Inspect: developed by the UK AI Security Institute and Meridian Labs | inspect.aisi.org.uk | 2026-09-27 00:47 | open the page | Authorship as the project states it |
| A-25 | METR: a research nonprofit that measures whether and when AI systems might pose catastrophic risks | metr.org/about: "a research nonprofit that scientifically measures whether and when AI systems might threaten catastrophic harm to society" | 2026-09-27 00:47 | open the page | Paraphrased on the atlas; quoted here |
| A-26 | NIST CAISI runs an AI Agent Standards Initiative | nist.gov/caisi and the initiative page | 2026-09-27 00:47; 00:54 | open both | The program's existence, not its output |
| A-27 | MLCommons AILuminate covers 12 hazard categories | mlcommons.org/ailuminate: "assesses genAI across 12 hazard categories" | 2026-09-27 00:47 | open the page | The benchmark's scope as its publisher states it |
| A-28 | OWASP AI Testing Guide: version 1 published November 2025 | the project page: "Version 1 Published", 26 November 2025 | 2026-09-27 00:47 | open the page | An OWASP Incubator project |
| A-29 | CEN-CENELEC lists the AI Act harmonised standards as under development | cencenelec.eu AI topic page: "Key Standards Under Development" | 2026-09-27 00:47 | open the page | The JTC 21 dashboard returned HTTP 500 and supports nothing here |
| A-30 | EU AI Act: in force; consolidated version of 27 July 2026 | EUR-Lex: "In force ... Current consolidated version: 27/07/2026" | 2026-09-27 00:47 | open the EUR-Lex page | Legal status and the consolidated text's date; applicability dates differ by article |
| A-31 | NIST AI RMF 1.0: voluntary; under revision | nist.gov: "intended for voluntary use"; "being revised" | 2026-09-27 00:47 | open the page | Status as NIST states it |
| A-32 | NIST AI 600-1 published July 2024 | nist.gov publication page (2024-07-26) | 2026-09-27 00:47 | open the page | Publication date only |
| A-33 | California SB 53: Chapter 138, Statutes of 2025 | leginfo.legislature.ca.gov bill status | 2026-09-27 00:47 | open the page | Enactment, not enforcement |
| A-34 | AEF-1: minimum operating conditions for independent third-party evaluation, version 1 | aievaluatorforum.org: "Version 1, updated December 4, 2025" | 2026-09-27 00:58 | open the page | The document's own scope; signatories are not verifiers |
| A-35 | OWASP Top 10 for Agentic Applications: 2026 edition, December 2025 | genai.owasp.org resource page, dated 9 December 2025 | 2026-09-27 00:47 | open the page | An edition and its date, not adoption |
| A-36 | Agentic AI Foundation: announced December 2025; working groups include identity and trust, and observability and traceability | Linux Foundation press release (2025-12-09); aaif.io | 2026-09-27 00:47 | open both | Announced structure, not output |
| A-37 | My vocabulary, conformance corpus and admission rules, and two Rust crates | GitHub; crates.io | 2026-09-27 00:44 | open each link on the atlas | Existence and placement, not use by others |
| A-38 | vocabulary v0.3.0; vectors v0.13.0 with 817 vectors in 13 corpora; admission has no release; jcs-admit 0.1.0; dsse 0.1.0 | GitHub tags; PyPI; the 13 `MANIFEST.json` files at tag v0.13.0; crates.io | 00:44 to 00:46; vector total 2026-09-27 01:16 | `rederive.py` A-38a to A-38f | The vector count is the sum of manifest members at the tag, including 13 members of one corpus marked `proposed`; the repository's main branch is ahead of the tag |
| A-38q | Quotations "These rails evaluate an already-verified statement. They do not verify one." and "Implements the envelope and nothing else" | the agent-evidence-admission and dsse READMEs, main branch (commits 1ded5b8 and 83e0477) | 2026-09-27 00:44 | read each README | Quoted from each README at the read time; a README can change |
| A-39 | Three contributions and their states: two pull requests open and unmerged, and one individual Internet-Draft, as listed on the atlas | GitHub API for each pull request; IETF Datatracker for the draft | 2026-09-27 00:41 to 00:42 | `rederive.py` A-39d and A-39f; Datatracker page for the draft | "Open" says nothing about the likelihood of merge |
| A-41 | The one-line description of each named project | each repository's own GitHub description, paraphrased; foundation membership from the project's site or README | 2026-09-27 01:31 | `gh api repos/<owner>/<repo> --jq .description` | Paraphrase; the repository's wording governs |
| A-42 | The mechanism table's "writer" column (self, peer, external) | the atlas's own classification, using the witness-scope terms of agent-evidence-vocabulary | 2026-09-27 | read `data/atlas.toml` | A reading of a typical deployment, stated as such on the page; a given deployment can differ |
| A-43 | Corpus member counts and splits (275; 232; 61; 52; 34; 34; 32; 27; 26; 15; 13; 8; 8) | each corpus's `MANIFEST.json` at tag v0.13.0 | 2026-09-27 01:16 | `rederive.py` A-38c for the total; `git show v0.13.0:<corpus>/MANIFEST.json` for each | Counts at the tag, not on the main branch |
| A-44 | OECD.AI catalogue listing; W3C mailing-list post of 12 September 2026 | the two pages, captured | 2026-09-27 01:23 | open both | A listing is not an endorsement |
| A-40 | None is merged or adopted as of the read | the same reads | 2026-09-27 00:42 | the same | Merge state only; a merge would not be adoption |

## Home page

| id | claim as printed | source | read (UTC) | re-derive | limit |
|---|---|---|---|---|---|
| I-01 | *Three Jobs, Not One*: Zenodo version 6, published 14 August 2026 | Zenodo API, record 21935891 | 2026-09-27 01:16 | `rederive.py` I-01 | The deposit's version, not a peer-review status |
| I-02 | GEM 2026 paper by Sankalp Gilda and Shlok Gilda | Crossref, DOI 10.18653/v1/2026.gem-main.80 | 2026-09-27 01:10 | `curl https://api.crossref.org/works/10.18653/v1/2026.gem-main.80` | Publication, not reception |
| I-03 | The atlas names 45 projects and standards and 18 mechanisms | `python3 tools/gen_atlas.py`, which prints the counts | 2026-09-27 17:09 | the same command | Counts of named entries, not of the field |
| I-04 | Releases and labels of the five repositories: vocabulary v0.3.0, draft; vectors v0.13.0, published; admission no release, draft; jcs-admit and dsse 0.1.0, published | releases as A-38; labels as the atlas's artifact table in `data/atlas.toml` | 2026-09-27 11:49 | `rederive.py` A-38 | A label is this site's reading of the repository's own status, not a maturity rating |
| I-05 | Versions, dates and statuses of the site's own artifacts | `data/versions.toml`, rendered on the version ledger page | 2026-09-29 | read the file | The site's own record of itself |
| I-06 | The claim ledger's rows are re-checked on every weekly re-derive | `.github/workflows/site.yml`, job `rederive`, schedule `17 6 * * 1` (Mondays 06:17 UTC), running `python3 tools/rederive.py --unread-fails` | 2026-09-27 19:29 | read the workflow file | Only the automatable rows are re-read; rows whose re-derive is a procedure are checked by hand |
| I-07 | Experiment draft 0.1 has one local three-interval PEER pilot; two registered designs have no result; three other pieces remain held | `src/experiments.md`; `experiments/observer-vantage/recorded.json`; `data/versions.toml` | 2026-09-29 16:45 | read those three files and run the pilot as E-01 | The local package source is unpublished; the pilot does not demonstrate an independent vantage |
| I-08 | The home page states the proposed action-assurance consumer contract; no end-to-end conformance is claimed | `src/index.md` | 2026-09-29 | read the action-assurance section | Component corpora and the local PEER pilot do not establish this full contract |

## Experiments

| id | claim as printed | source | read (UTC) | re-derive | limit |
|---|---|---|---|---|---|
| E-01 | Three scripted intervals: brokered write one accepted and one replay, offline verified at `PEER`; durable direct bypass succeeded and produced a known gap; transient direct bypass succeeded, was removed before snapshot, and produced `knownGaps=[]` and `noDetectedGap=true` | [`experiments/observer-vantage/recorded.json`](experiments/observer-vantage/recorded.json) from [`run.py`](experiments/observer-vantage/run.py) against local `agent-evidence-observer` source | 2026-09-29 16:45 | Run the exact command in `experiments.html` with observer source digest E-02, then `diff -u` the result | Local scripted counterexample, not a live agent or a detection rate; no independent rerun until the package source is public |
| E-02 | The pilot used observer package metadata and Python sources with SHA-256 `273e4985cb4de671145bcd55ef85545be213e8520f766ab7692e9d05edae60d1` | `source_digest()` in `experiments/observer-vantage/run.py`; recorded JSON | 2026-09-29 16:45 | Run `run.py --observer-root` as in the experiment page and compare `observerSourceSha256` | Source tree is local and unpublished at this read; a digest makes a later comparison possible but cannot supply the bytes |
| E-03 | The pilot's two signing keys were held by one process; there were zero isolated-agent and zero separately operated witness runs | The pilot script, the local observer `README.md`, and `src/experiments.md` | 2026-09-29 16:45 | Inspect `make_interval()` in the pilot and the E2/E3 sections; request external run evidence before promoting a claim | A tested key distinction is not an operator or privilege boundary; the zero counts describe this pilot only |
| E-04 | E2 and E3 are registered designs without result or overhead measurement | `src/experiments.md` sections E2 and E3 | 2026-09-29 16:45 | Inspect the designs and the version ledger's draft status; later compare raw run bundles and deviations with this source digest | Registration fixes a proposed protocol; it does not validate its feasibility or claim independent evidence |

## Links

| id | claim | how it was checked | read (UTC) | limit |
|---|---|---|---|---|
| L-01 | Every internal link and anchor on the site resolves, and every link to the site's own published address names a page that was built | `python3 tools/check_links.py` | 2026-09-27 09:40 | Checks the built `docs/` directory |
| L-02 | Every external link answers 2xx, except links on hosts that refuse automated reads, each of which has its own row in this section | `python3 tools/check_links.py --external`; crates.io, doi.org and GitHub file links are checked through the same resource's API | 2026-09-27 09:40 | A 2xx answer shows a page exists, not that it still says what the claim quotes |
