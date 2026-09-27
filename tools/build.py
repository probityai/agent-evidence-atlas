#!/usr/bin/env python3
"""Build the site from Markdown into docs/, with pandoc, and fail on any warning.

    python3 tools/build.py            build into docs/
    python3 tools/build.py --check    build into a scratch directory and fail if docs/ differs

Sources: every src/*.md becomes docs/<name>.html, and CLAIMS.md at the repository
root becomes docs/claims.html. The site's navigation lists only the pages that were
built, so a page whose source is not in the repository is never linked; the version
ledger shows such an artifact as held. Every page carries a canonical link under
BASE_URL, the site's published home. A line of the form

    <!-- include: relative/path -->

is replaced by that file's contents before pandoc runs. Files a page links to for
download (the verifier demonstration's sources) are copied under docs/ so every
link resolves on the published site and in a local preview alike.

Requires pandoc 3.x. The build is deterministic: no timestamps, no commit ids.
"""

from __future__ import annotations

import filecmp
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
TEMPLATE = ROOT / "tools" / "template.html"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
BASE_URL = "https://probityai.github.io/agent-evidence-atlas/"
SITE_NAME = "Independent evidence for AI agent actions"

# Navigation order and labels. A page appears only when it is built.
NAV = [
    ("atlas", "Atlas"),
    ("essay", "Essay"),
    ("demo", "Verifier"),
    ("experiments", "Experiments"),
    ("series", "Series"),
    ("claims", "Claims"),
    ("versions", "Versions"),
]

# Published copies of files the pages link to: (source, destination under docs/, the
# page whose links need it, or None for every page). A copy is made exactly when its
# page is built, and a missing source for a built page fails the build.
COPIES = [
    ("assets/site.css", "assets/site.css", None),
    ("demo/verifier/Cargo.toml", "demo/verifier/Cargo.toml", "demo"),
    ("demo/verifier/Cargo.lock", "demo/verifier/Cargo.lock", "demo"),
    ("demo/verifier/src/main.rs", "demo/verifier/src/main.rs", "demo"),
    ("demo/verifier/run-demo.sh", "demo/verifier/run-demo.sh", "demo"),
    ("demo/verifier/inputs/vcc938c6038536dcb.json", "demo/verifier/inputs/vcc938c6038536dcb.json", "demo"),
    ("demo/TRANSCRIPT.txt", "demo/TRANSCRIPT.txt", "demo"),
    ("demo/NEGATIVE-CONTROL.txt", "demo/NEGATIVE-CONTROL.txt", "demo"),
]

INCLUDE = re.compile(r"^<!-- include: (\S+) -->$", re.MULTILINE)
FRONT_TOC = re.compile(r"^toc:\s*true\s*$", re.MULTILINE)


def expand(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return (ROOT / m.group(1)).read_text(encoding="utf-8").rstrip("\n")
    return INCLUDE.sub(repl, text)


def nav_html(built: set[str]) -> tuple[str, str]:
    """The home link and the navigation links for the set of page stems being built."""
    home = (f'<a class="home" href="index.html">{SITE_NAME}</a>' if "index" in built
            else f'<span class="home">{SITE_NAME}</span>')
    links = "\n".join(f'      <a href="{stem}.html">{label}</a>' for stem, label in NAV if stem in built)
    return home, links


def render(source: Path, dest: Path, built: set[str]) -> None:
    text = expand(source.read_text(encoding="utf-8"))
    home, links = nav_html(built)
    canonical = BASE_URL if dest.stem == "index" else f"{BASE_URL}{dest.stem}.html"
    args = [
        "pandoc",
        "--from=markdown+smart",
        "--to=html5",
        "--standalone",
        f"--template={TEMPLATE}",
        "--fail-if-warnings",
        "--variable=root:",
        f"--variable=build:{VERSION}",
        f"--variable=sitename:{SITE_NAME}",
        f"--variable=canonical:{canonical}",
        f"--variable=homelink:{home}",
        f"--variable=navlinks:{links}",
        "--wrap=none",
        f"--output={dest}",
    ]
    if FRONT_TOC.search(text.split("\n---", 1)[0] if text.startswith("---") else ""):
        args += ["--toc", "--toc-depth=2"]
    proc = subprocess.run(args, input=text, text=True, capture_output=True, check=False)
    if proc.returncode != 0 or proc.stderr.strip():
        sys.stderr.write(f"pandoc failed or warned on {source.relative_to(ROOT)}:\n{proc.stderr}")
        raise SystemExit(1)


def versions_markdown(built: set[str]) -> str:
    """The version ledger page, with each source file's SHA-256 computed now.

    An artifact whose page is not built from this repository is listed as held,
    with no link, so the ledger never points at a page that does not exist."""
    data = tomllib.loads((ROOT / "data" / "versions.toml").read_text(encoding="utf-8"))
    rows = ["| artifact | version | date | status | source SHA-256 (first 16) | note |", "|---|---|---|---|---|---|"]
    for a in data["artifact"]:
        source = ROOT / a["source"]
        page_stem = Path(a["page"]).stem
        if page_stem in built and source.exists():
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
            rows.append(f"| [{a['name']}]({a['page']}) | {a['version']} | {a['date']} | "
                        f"[{a['status']}]{{.label .{a['status']}}} | `{digest}` `{a['source']}` | {a['note']} |")
        else:
            rows.append(f"| {a['name']} | {a['version']} | {a['date']} | [held]{{.label .draft}} | "
                        f"page not built in this repository yet | Held until it passes its release criteria |")
    return "\n".join([
        "---",
        'title: "Version ledger"',
        'subtitle: "Every artifact on this site, its version, its status, and a digest of the source it was built from"',
        f'status: "Site version {VERSION}. Rebuilt on every change; the digests let a reader check that a page matches the version recorded here."',
        "---",
        "",
        "A digest here is the SHA-256 of the artifact's source file in the site's repository, "
        "truncated to 16 hexadecimal characters for display. A change to the source changes the digest, "
        "and a change that alters what a page claims also gets a new version and a note.",
        "",
        *rows,
        "",
    ])


def build(out: Path) -> None:
    pages = sorted(SRC.glob("*.md"))
    if (SRC / "atlas.md").exists():
        gen = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_atlas.py"), "--check"],
                             capture_output=True, text=True, check=False)
        if gen.returncode != 0:
            sys.stderr.write(gen.stdout + gen.stderr)
            raise SystemExit(1)
    built = {p.stem for p in pages} | {"claims", "versions"}
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for page in pages:
        render(page, out / f"{page.stem}.html", built)
    render(ROOT / "CLAIMS.md", out / "claims.html", built)
    with tempfile.TemporaryDirectory() as tmp:
        ledger = Path(tmp) / "versions.md"
        ledger.write_text(versions_markdown(built), encoding="utf-8")
        render(ledger, out / "versions.html", built)
    for src, dst, page in COPIES:
        if page is not None and page not in built:
            continue
        target = out / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / src, target)
    (out / ".nojekyll").write_text("", encoding="utf-8")


def same_tree(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    if mismatch or errors:
        return False
    return all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    if "--check" in sys.argv[1:]:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "docs"
            build(fresh)
            if not OUT.exists() or not same_tree(fresh, OUT):
                print("docs/ is out of date with its sources: run python3 tools/build.py")
                return 1
        print("docs/ matches its sources")
        return 0
    build(OUT)
    print(f"built {len(list(OUT.glob('*.html')))} pages into docs/ (version {VERSION})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
