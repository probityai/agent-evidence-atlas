---
title: "Claim ledger"
subtitle: "Every number, date, status and quotation on this site, with its source, when it was read, how to re-derive it, and what it does not mean"
status: "Version 0.2, 27 September 2026. Automatable rows were last re-derived at 2026-09-27T09:42:25Z: 23 of 54 unchanged; the other 31 are star counts that had moved by between one and ten since the original read. The pages keep the value as read, with its read time."
description: "The source, read time, re-derive command and limit for every claim on the site."
---

## How to use this ledger

- **Re-derive the automatable rows** with `python3 tools/rederive.py` from the repository root. It needs no credentials, prints the recorded and the current value for each row, and prints `UNREAD` with a reason when a source cannot be read; an unread row is never reported as unchanged. `--strict` exits 1 on any change.
- **Read times** are UTC. A row older than its cadence is stale: star counts and pull-request states have a 7-day cadence, standards statuses 30 days, and published versions and dated events do not expire.
- **Captures.** Every web page cited was saved when it was read. The capture log records URL, HTTP status, UTC time and SHA-256 for each one.

Each row's identifier starts with the letter of the page it covers, and each page has its own section below: `A` for the atlas and `L` for the site's links. A page's section is added with the page.

## Atlas

| id | claim as printed | source | read (UTC) | re-derive | limit |
|---|---|---|---|---|---|
| A-01 | SPIFFE and SPIRE: CNCF Graduated (August 2022) | cncf.io project pages for SPIFFE and SPIRE | 2026-09-27 00:47 | open <https://www.cncf.io/projects/spire/> | Maturity level, not adoption |
| A-02 | SPIRE repository: 2,558 stars | GitHub API `repos/spiffe/spire` | 2026-09-27 00:40 | `tools/rederive.py` A-stars | Stars measure attention, not quality or use |
| A-03 | WIMSE: active working group; seven working-group drafts, including an AI identity management draft | IETF Datatracker, WIMSE documents page | 2026-09-27 00:47 | open <https://datatracker.ietf.org/wg/wimse/documents/> | Working-group drafts are not standards |
| A-04 | RFC 8693 is a Proposed Standard; OAuth 2.1 is a working-group draft | RFC Editor info page; Datatracker `draft-ietf-oauth-v2-1` (revision 16) | 2026-09-27 00:47 | open both pages | |
| A-05 | MCP authorization specification version 2026-07-28 states that authorization is optional | modelcontextprotocol.io, authorization page: "Authorization is OPTIONAL for MCP implementations" | 2026-09-27 00:47 | open the page | Applies to that specification version |
| A-06 | Open Policy Agent: CNCF Graduated (2021); 12,276 stars | cncf.io; GitHub API | 00:47; 00:40 | `rederive.py` A-stars | |
| A-07 | Kyverno: CNCF Graduated (2026-03-16); 8,184 stars | cncf.io; GitHub API | 00:47; 00:40 | `rederive.py` A-stars | |
| A-08 | Cedar: CNCF Sandbox (2025-10-08); 1,748 stars | cncf.io; GitHub API | 00:47; 00:40 | `rederive.py` A-stars | |
| A-09 | agentgateway: a Linux Foundation project, per its README; 5,052 stars | the project's README; GitHub API | 00:56; 00:40 | `rederive.py` A-stars | Foundation status is the project's own statement; the CNCF project URL returned 404 |
| A-stars | Every GitHub star count on the atlas (36 entries that name a repository) | GitHub API `repos/<owner>/<repo>` | 2026-09-27 00:40 to 00:41, except where a row says otherwise | `python3 tools/rederive.py` reads every entry with a `repo` in `data/atlas.toml` | Stars measure attention, not quality or use; at 01:34 four had moved by one or two |
| A-16 | OpenTelemetry: CNCF Graduated (2026-05-11); generative-AI and agent-span conventions marked "Development" | cncf.io; the conventions' own Markdown in `open-telemetry/semantic-conventions-genai` | 00:47; 00:51 | open both | "Development" is the conventions' own stability label |
| A-18 | in-toto: CNCF Graduated (2025-02-10); attestation specification v1.2 | cncf.io; the specification README ("Latest version: v1.2") | 00:47; 00:49 | open both | |
| A-19 | Sigstore: an OpenSSF project; Rekor v2 runs as a production instance with a 99.5% availability objective | openssf.org project list; the Rekor v2 README ("a productionized instance of Rekor v2 with a 99.5% availability SLO") | 00:52; 00:49 | open both | The OpenSSF page read does not show a maturity stage |
| A-20 | RFC 9943 and RFC 9942: Proposed Standards, June 2026 | IETF Datatracker, SCITT documents page | 00:47 to 00:52 | open the page | |
| A-21 | C2PA: a Joint Development Foundation project; specification 2.4 current | spec.c2pa.org specifications index | 00:49 | open the page | |
| A-22 | RFC 9162: Experimental (2021) | RFC Editor | 00:47 | open <https://www.rfc-editor.org/info/rfc9162> | |
| A-23 | RFC 8785: Informational | RFC Editor | 00:47 | open <https://www.rfc-editor.org/info/rfc8785> | |
| A-24 | Inspect: developed by the UK AI Security Institute and Meridian Labs | inspect.aisi.org.uk | 00:47 | open the page | |
| A-25 | METR: a research nonprofit that measures whether and when AI systems might pose catastrophic risks | metr.org/about: "a research nonprofit that scientifically measures whether and when AI systems might threaten catastrophic harm to society" | 00:47 | open the page | Paraphrased on the atlas; quoted here |
| A-26 | NIST CAISI runs an AI Agent Standards Initiative | nist.gov/caisi and the initiative page | 00:47; 00:54 | open both | |
| A-27 | MLCommons AILuminate covers 12 hazard categories | mlcommons.org/ailuminate: "assesses genAI across 12 hazard categories" | 00:47 | open the page | |
| A-28 | OWASP AI Testing Guide: version 1 published November 2025 | the project page: "Version 1 Published", 26 November 2025 | 00:47 | open the page | An OWASP Incubator project |
| A-29 | CEN-CENELEC lists the AI Act harmonised standards as under development | cencenelec.eu AI topic page: "Key Standards Under Development" | 00:47 | open the page | The JTC 21 dashboard returned HTTP 500 and supports nothing here |
| A-30 | EU AI Act: in force; consolidated version of 27 July 2026 | EUR-Lex: "In force ... Current consolidated version: 27/07/2026" | 00:47 | open the EUR-Lex page | |
| A-31 | NIST AI RMF 1.0: voluntary; under revision | nist.gov: "intended for voluntary use"; "being revised" | 00:47 | open the page | |
| A-32 | NIST AI 600-1 published July 2024 | nist.gov publication page (2024-07-26) | 00:47 | open the page | |
| A-33 | California SB 53: Chapter 138, Statutes of 2025 | leginfo.legislature.ca.gov bill status | 00:47 | open the page | |
| A-34 | AEF-1: minimum operating conditions for independent third-party evaluation, version 1 | aievaluatorforum.org: "Version 1, updated December 4, 2025" | 00:58 | open the page | |
| A-35 | OWASP Top 10 for Agentic Applications: 2026 edition, December 2025 | genai.owasp.org resource page, dated 9 December 2025 | 00:47 | open the page | |
| A-36 | Agentic AI Foundation: announced December 2025; working groups include identity and trust, and observability and traceability | Linux Foundation press release (2025-12-09); aaif.io | 00:47 | open both | |
| A-37 | Five repositories by the author | GitHub; crates.io | 00:44 | open each link on the atlas | |
| A-38 | vocabulary v0.3.0; vectors v0.13.0 with 817 vectors in 13 corpora; admission has no release; jcs-admit 0.1.0; dsse 0.1.0 | GitHub tags; PyPI; the 13 `MANIFEST.json` files at tag v0.13.0; crates.io | 00:44 to 00:46; vector total 2026-09-27 01:16 | `rederive.py` A-38a to A-38f | The vector count is the sum of manifest members at the tag, including 13 members of one corpus marked `proposed`; the repository's main branch is ahead of the tag |
| A-38q | Quotations "These rails evaluate an already-verified statement. They do not verify one." and "Implements the envelope and nothing else" | the agent-evidence-admission and dsse READMEs, main branch (commits 1ded5b8 and 83e0477) | 00:44 | read each README | |
| A-39 | Thirteen contributions and their states: nine pull requests open and unmerged (one of them as reviewer), one individual Internet-Draft, and three open issues, as listed on the atlas | GitHub API for each pull request and issue; IETF Datatracker for the draft | 00:41 to 00:42 | `rederive.py` A-39a to A-39l; Datatracker page for the draft | "Open" says nothing about the likelihood of merge |
| A-41 | The one-line description of each named project | each repository's own GitHub description, paraphrased; foundation membership from the project's site or README | 2026-09-27 01:31 | `gh api repos/<owner>/<repo> --jq .description` | Paraphrase; the repository's wording governs |
| A-42 | The mechanism table's "writer" column (self, peer, external) | the atlas's own classification, using the witness-scope terms of agent-evidence-vocabulary | 2026-09-27 | read `data/atlas.toml` | A reading of a typical deployment, stated as such on the page; a given deployment can differ |
| A-43 | Corpus member counts and splits (275; 232; 61; 52; 34; 34; 32; 27; 26; 15; 13; 8; 8) | each corpus's `MANIFEST.json` at tag v0.13.0 | 2026-09-27 01:16 | `rederive.py` A-38c for the total; `git show v0.13.0:<corpus>/MANIFEST.json` for each | |
| A-44 | OECD.AI catalogue listing; W3C mailing-list post of 12 September 2026 | the two pages, captured | 2026-09-27 01:23 | open both | A listing is not an endorsement |
| A-40 | None is merged or adopted as of the read | the same reads | 00:42 | the same | |

## Links

| id | claim | how it was checked | read (UTC) | limit |
|---|---|---|---|---|
| L-01 | Every internal link and anchor on the site resolves, and every link to the site's own published address names a page that was built | `python3 tools/check_links.py` | 2026-09-27 09:40 | Checks the built `docs/` directory |
| L-02 | Every external link answers 2xx, except links on hosts that refuse automated reads, each of which has its own row in this section | `python3 tools/check_links.py --external`; crates.io, doi.org and GitHub file links are checked through the same resource's API | 2026-09-27 09:40 | |
