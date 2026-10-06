"""Render task navigation and machine indexes for the existing site build.

The reviewed catalog supplies project names, tasks and source pins. This module
adds site destinations; it does not read or modify the Lab register.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any, cast
from xml.sax.saxutils import escape

from discoverability import catalog

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://probityai.github.io/agent-evidence-atlas/"
PAGE_NAME = re.compile(r"[a-z][a-z0-9-]*\Z")
SITE_LINKS = (
    ("start", "Choose a project", "Tools grouped by the task you need."),
    ("automation", "Automation", "Read the catalog and pinned run records."),
    ("lab", "Open Evidence Lab", "Retained runs, submissions and corrections."),
    ("runs", "Find a retained run", "Search recorded claims, declared roles, limits and original evidence."),
    ("atlas", "Assurance atlas", "Projects, mechanisms and evidence boundaries."),
    ("experiments", "Experiments", "Pinned procedures and recorded results."),
    ("replay-an-evidence-decision", "Replay an evidence decision", "A retained admission and its state-preserving refusals."),
    ("replay-tools", "Run the APS and PriorSeal replay", "Declare the caller and retain pinned sources, process logs and results."),
    ("claims", "Claim ledger", "Sources and re-derive commands."),
    ("repository", "Repository guide", "Sources, checks and the site build."),
)


def load_public(root: Path = ROOT) -> dict[str, Any]:
    """Load and project reviewed catalog records for a site build.

    Parameters
    ----------
    root : pathlib.Path
        Repository containing ``data/catalog.json``.

    Returns
    -------
    dict[str, Any]
        Validated public fields from :func:`catalog.public_projection`.
        Editing notes, extensions and unreviewed records are absent.

    Raises
    ------
    catalog.CatalogError
        If catalog shape, references, public text or source pins are invalid.
    OSError
        If the catalog cannot be read.
    """
    data = catalog.load_catalog(root / "data/catalog.json")
    baseline = catalog.load_catalog(root / "tools/discoverability/catalog.seed.json")
    public = catalog.public_projection(catalog.validate_catalog(data, baseline))
    sources = json.loads(
        (root / "data/catalog-sources.json").read_text(encoding="ascii")
    )
    check_source_bindings(public, sources)
    return public


def check_source_bindings(
    public: dict[str, Any], sources: list[dict[str, str]]
) -> None:
    """Bind public repository pins to their reviewed README capture records.

    Parameters
    ----------
    public : dict[str, Any]
        Validated catalog projection.
    sources : list of dict of str to str
        Reviewed source URLs, commits and Git blob digests. These are source
        identities, not measurements of tool performance.

    Raises
    ------
    catalog.CatalogError
        If source URLs repeat or a published repository lacks its matching pin.
    """
    index = {row["url"]: row for row in sources}
    if len(index) != len(sources):
        catalog.fail("Catalog source URL is repeated")
    for repository in public["repositories"]:
        source = index.get(repository["source"]["url"])
        if source is None or source["commit"] != repository["source"]["commit"]:
            catalog.fail(f"Catalog source pin is unreviewed: {repository['id']}")


def project_entries(public: dict[str, Any]) -> list[dict[str, Any]]:
    """Return components and integration profiles in stable identity order."""
    return sorted([*public["components"], *public["profiles"]], key=lambda r: r["id"])


def project_url(record: dict[str, Any], public: dict[str, Any]) -> str:
    """Choose a reviewed guide, falling back to the owning repository."""
    repositories = {row["id"]: row for row in public["repositories"]}
    return cast(
        str, record.get("docs_url", repositories[record["repositories"][0]]["url"])
    )


def start_markdown(public: dict[str, Any]) -> str:
    """Build a task table and short project entries from projected fields.

    Parameters
    ----------
    public : dict[str, Any]
        Output of :func:`load_public` or ``catalog.public_projection``.

    Returns
    -------
    str
        Markdown for ``start.html``. Stable IDs own fragment anchors, so a
        display-name change leaves existing project links usable.
    """
    rows = [
        "---",
        'title: "Choose a project"',
        'subtitle: "Start with the task you need."',
        'description: "Find Probity tools for evidence terms, conformance tests, observation, verification and workload admission."',
        "---",
        "",
        "Vectors tests how a verifier behaves. Verify checks a supplied claim against evidence bytes.",
        "",
        "Use the catalog ID when selecting a tool or profile in a structured record. Repository names and display labels can differ from that ID.",
        "",
        "| Task | Project |",
        "| --- | --- |",
    ]
    entries = project_entries(public)
    for record in entries:
        rows.append(
            f"| {record['task']} | [{record['display_name']}](#{record['id']}) |"
        )
    for record in entries:
        rows.extend(
            [
                "",
                f"## {record['display_name']} {{#{record['id']}}}",
                "",
                (
                    f"Profile ID: `{record['id']}`. Component ID: `{record['component']}`."
                    if "component" in record
                    else f"Component ID: `{record['id']}`."
                ),
                "",
                record["summary"],
                "",
                f"{record['status'].capitalize()}. [Quickstart and source]({project_url(record, public)})",
            ]
        )
    rows.extend(
        [
            "",
            "## Run and share a check",
            "",
            "The [Open Evidence Lab](lab.html) holds replayable runs and accepts new results and corrections. For scripted lookups, use the [automation guide](automation.html).",
            "",
        ]
    )
    return "\n".join(rows)


def llms_index(public: dict[str, Any], pages: set[str]) -> str:
    """Render an index whose site links name pages in the current build.

    Parameters
    ----------
    public : dict[str, Any]
        Validated, projected catalog records.
    pages : set[str]
        Page stems that the build will publish.

    Returns
    -------
    str
        ASCII Markdown index. Each project destination retains its reviewed
        source pin; page links use the site's canonical base URL.
    """
    rows = [
        "# Probity AI",
        "",
        "> Tools and run records for checking claims about agent actions.",
        "",
        "## Guides",
        "",
    ]
    for stem, label, summary in SITE_LINKS:
        if stem in pages:
            rows.append(f"- [{label}]({BASE_URL}{stem}.md): {summary}")
    rows.extend(["", "## Projects", ""])
    for record in project_entries(public):
        identity = (
            f"Profile ID: `{record['id']}`. Component ID: `{record['component']}`."
            if "component" in record
            else f"Component ID: `{record['id']}`."
        )
        rows.append(
            f"- [{record['display_name']}]({project_url(record, public)}): {identity} {record['summary']}"
        )
    rows.extend(
        [
            "",
            "## Data",
            "",
            f"- [Project catalog]({BASE_URL}catalog.json): Stable project IDs, tasks and pinned README sources.",
        ]
    )
    if "lab" in pages:
        rows.append(
            f"- [Lab register]({BASE_URL}lab/register.json): Retained artifacts, results and review state."
        )
    return "\n".join(rows) + "\n"


def sitemap(pages: Iterable[str]) -> str:
    """Render canonical page URLs without a fabricated modification time.

    Parameters
    ----------
    pages : iterable of str
        Built page stems. Order and repetition do not change the output.

    Returns
    -------
    str
        Sitemap XML with the home page's canonical directory URL.

    Raises
    ------
    ValueError
        If a page stem could change a URL or XML element.
    """
    stems = sorted(set(pages))
    if any(PAGE_NAME.fullmatch(stem) is None for stem in stems):
        catalog.fail("Sitemap page must be a plain page stem")
    rows = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for stem in stems:
        url = BASE_URL if stem == "index" else f"{BASE_URL}{stem}.html"
        rows.append(f"  <url><loc>{escape(url)}</loc></url>")
    rows.append("</urlset>")
    return "\n".join(rows) + "\n"


def site_assets(public: dict[str, Any], pages: set[str]) -> dict[str, str]:
    """Return the machine-readable files emitted by the existing site build."""
    return {
        "catalog.json": json.dumps(public, indent=2, sort_keys=True, ensure_ascii=True)
        + "\n",
        "llms.txt": llms_index(public, pages),
        "sitemap.xml": sitemap(pages),
    }
