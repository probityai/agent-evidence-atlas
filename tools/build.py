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
    ("lab", "Open Evidence Lab"),
    ("pilot", "Pilot status"),
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
    ("experiments/installed-boundary-policy-2026-10-02/report.json", "experiments/installed-boundary-policy-2026-10-02/report.json", "lab"),
    ("experiments/installed-boundary-policy-2026-10-02/provenance.json", "experiments/installed-boundary-policy-2026-10-02/provenance.json", "lab"),
    ("experiments/installed-boundary-policy-2026-10-02/selected-capsule.zip", "experiments/installed-boundary-policy-2026-10-02/selected-capsule.zip", "lab"),
    ("experiments/installed-boundary-policy-2026-10-02/source-contract.json", "experiments/installed-boundary-policy-2026-10-02/source-contract.json", "lab"),
    ("experiments/model-boundary-cpu-2026-10-02/original-artifact.zip", "experiments/model-boundary-cpu-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/model-boundary-cpu-2026-10-02/provenance.json", "experiments/model-boundary-cpu-2026-10-02/provenance.json", "lab"),
    ("experiments/model-boundary-cpu-2026-10-02/report.json", "experiments/model-boundary-cpu-2026-10-02/report.json", "lab"),
    ("experiments/model-boundary-cpu-2026-10-02/finite-findings.json", "experiments/model-boundary-cpu-2026-10-02/finite-findings.json", "lab"),
    ("experiments/google-adk-ticket-2026-10-02/original-artifact.zip", "experiments/google-adk-ticket-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/google-adk-ticket-2026-10-02/provenance.json", "experiments/google-adk-ticket-2026-10-02/provenance.json", "lab"),
    ("experiments/google-adk-ticket-2026-10-02/report.json", "experiments/google-adk-ticket-2026-10-02/report.json", "lab"),
    ("experiments/installed-format-policy-2026-10-02/original-artifact.zip", "experiments/installed-format-policy-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/installed-format-policy-2026-10-02/provenance.json", "experiments/installed-format-policy-2026-10-02/provenance.json", "lab"),
    ("experiments/installed-format-policy-2026-10-02/report.json", "experiments/installed-format-policy-2026-10-02/report.json", "lab"),
    ("experiments/model-format-cpu-2026-10-02/original-artifact.zip", "experiments/model-format-cpu-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/model-format-cpu-2026-10-02/provenance.json", "experiments/model-format-cpu-2026-10-02/provenance.json", "lab"),
    ("experiments/model-format-cpu-2026-10-02/report.json", "experiments/model-format-cpu-2026-10-02/report.json", "lab"),
    ("experiments/execsurface-state-2026-10-02/original-artifact.zip", "experiments/execsurface-state-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/execsurface-state-2026-10-02/provenance.json", "experiments/execsurface-state-2026-10-02/provenance.json", "lab"),
    ("experiments/execsurface-state-2026-10-02/report.json", "experiments/execsurface-state-2026-10-02/report.json", "lab"),
    ("experiments/authority-recovery-2026-10-02/original-artifact.zip", "experiments/authority-recovery-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/authority-recovery-2026-10-02/provenance.json", "experiments/authority-recovery-2026-10-02/provenance.json", "lab"),
    ("experiments/authority-recovery-2026-10-02/report.json", "experiments/authority-recovery-2026-10-02/report.json", "lab"),
    ("experiments/target-process-recovery-2026-10-02/original-artifact.zip", "experiments/target-process-recovery-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/target-process-recovery-2026-10-02/provenance.json", "experiments/target-process-recovery-2026-10-02/provenance.json", "lab"),
    ("experiments/target-process-recovery-2026-10-02/report.json", "experiments/target-process-recovery-2026-10-02/report.json", "lab"),
    ("experiments/model-paired-cpu-2026-10-02/original-artifact.zip", "experiments/model-paired-cpu-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/model-paired-cpu-2026-10-02/provenance.json", "experiments/model-paired-cpu-2026-10-02/provenance.json", "lab"),
    ("experiments/model-paired-cpu-2026-10-02/report.json", "experiments/model-paired-cpu-2026-10-02/report.json", "lab"),
    ("experiments/openai-agents-ticket-2026-10-02/original-artifact.zip", "experiments/openai-agents-ticket-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/openai-agents-ticket-2026-10-02/provenance.json", "experiments/openai-agents-ticket-2026-10-02/provenance.json", "lab"),
    ("experiments/openai-agents-ticket-2026-10-02/report.json", "experiments/openai-agents-ticket-2026-10-02/report.json", "lab"),
    ("experiments/langgraph-durable-2026-10-02/original-artifact.zip", "experiments/langgraph-durable-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/langgraph-durable-2026-10-02/provenance.json", "experiments/langgraph-durable-2026-10-02/provenance.json", "lab"),
    ("experiments/langgraph-durable-2026-10-02/report.json", "experiments/langgraph-durable-2026-10-02/report.json", "lab"),
    ("experiments/pydantic-failure-2026-10-02/original-artifact.zip", "experiments/pydantic-failure-2026-10-02/original-artifact.zip", "lab"),
    ("experiments/pydantic-failure-2026-10-02/provenance.json", "experiments/pydantic-failure-2026-10-02/provenance.json", "lab"),
    ("experiments/pydantic-failure-2026-10-02/report.json", "experiments/pydantic-failure-2026-10-02/report.json", "lab"),
    ("experiments/model-operational-2026-10-02/provenance.json", "experiments/model-operational-2026-10-02/provenance.json", "lab"),
    ("experiments/model-operational-2026-10-02/report.json", "experiments/model-operational-2026-10-02/report.json", "lab"),
    ("experiments/model-operational-2026-10-02/selected-capsule.zip", "experiments/model-operational-2026-10-02/selected-capsule.zip", "lab"),
    ('experiments/jep-core07-2026-10-02/original-artifact.zip', 'experiments/jep-core07-2026-10-02/original-artifact.zip', 'lab'),
    ('experiments/jep-core07-2026-10-02/provenance.json', 'experiments/jep-core07-2026-10-02/provenance.json', 'lab'),
    ('experiments/jep-core07-2026-10-02/report.json', 'experiments/jep-core07-2026-10-02/report.json', 'lab'),
    ('experiments/remora-e7-2026-10-02/external-run-record-v1.json', 'experiments/remora-e7-2026-10-02/external-run-record-v1.json', 'lab'),
    ('experiments/remora-e7-2026-10-02/original-artifact.zip', 'experiments/remora-e7-2026-10-02/original-artifact.zip', 'lab'),
    ('experiments/remora-e7-2026-10-02/provenance.json', 'experiments/remora-e7-2026-10-02/provenance.json', 'lab'),
    ('experiments/remora-e7-2026-10-02/report.json', 'experiments/remora-e7-2026-10-02/report.json', 'lab'),

    ("data/readouts/rederive-2026-10-01.txt", "readouts/rederive-2026-10-01.txt", "claims"),
    ("data/lab-register.json", "lab/register.json", "lab"),
    ("assets/site.css", "assets/site.css", None),
    ("experiments/observer-vantage/run.py", "experiments/observer-vantage/run.py", "experiments"),
    ("experiments/observer-vantage/recorded.json", "experiments/observer-vantage/recorded.json", "experiments"),
    ("experiments/trace-transcript/run.py", "experiments/trace-transcript/run.py", "experiments"),
    ("experiments/trace-transcript/recorded.json", "experiments/trace-transcript/recorded.json", "experiments"),
    ("experiments/observer-admission/run.py", "experiments/observer-admission/run.py", "experiments"),
    ("experiments/observer-admission/source-pins.json", "experiments/observer-admission/source-pins.json", "experiments"),
    ("experiments/observer-admission/recorded.json", "experiments/observer-admission/recorded.json", "experiments"),
    ("experiments/observer-admission/provenance.json", "experiments/observer-admission/provenance.json", "experiments"),
    ("experiments/observer-admission/retained/demo-report.json", "experiments/observer-admission/retained/demo-report.json", "experiments"),
    ("experiments/observer-admission/retained/consumer/policy.json", "experiments/observer-admission/retained/consumer/policy.json", "experiments"),
    ("experiments/observer-admission/retained/consumer/decision.json", "experiments/observer-admission/retained/consumer/decision.json", "experiments"),
    ("experiments/observer-admission/retained/consumer/state.json", "experiments/observer-admission/retained/consumer/state.json", "experiments"),
    ("experiments/observer-admission/retained/producer/packet.json", "experiments/observer-admission/retained/producer/packet.json", "experiments"),
    ("experiments/observer-admission/retained/producer/history.jsonl", "experiments/observer-admission/retained/producer/history.jsonl", "experiments"),
    ("experiments/observer-admission/retained/producer/ledger.jsonl", "experiments/observer-admission/retained/producer/ledger.jsonl", "experiments"),
    ("experiments/observer-admission/retained/producer/workspace/result.txt", "experiments/observer-admission/retained/producer/workspace/result.txt", "experiments"),
    ("demo/verifier/Cargo.toml", "demo/verifier/Cargo.toml", "demo"),
    ("demo/verifier/Cargo.lock", "demo/verifier/Cargo.lock", "demo"),
    ("demo/verifier/src/main.rs", "demo/verifier/src/main.rs", "demo"),
    ("demo/verifier/run-demo.sh", "demo/verifier/run-demo.sh", "demo"),
    ("demo/verifier/inputs/vcc938c6038536dcb.json", "demo/verifier/inputs/vcc938c6038536dcb.json", "demo"),
    ("demo/TRANSCRIPT.txt", "demo/TRANSCRIPT.txt", "demo"),
    ("demo/NEGATIVE-CONTROL.txt", "demo/NEGATIVE-CONTROL.txt", "demo"),
]

INCLUDE = re.compile(r"^<!-- include: (\S+) -->$", re.MULTILINE)
TR = re.compile(r"<tr([^>]*)>(.*?)</tr>", re.DOTALL)
CELL = re.compile(r"<t[hd][^>]*>(.*?)</t[hd]>", re.DOTALL)
TABLE = re.compile(r"<table.*?</table>", re.DOTALL)
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

# Marks each stamped row stale once the reader's clock passes read date plus cadence. The
# page is built without a clock, so the comparison happens where the reader is.
STALE_SCRIPT = """<script>
(function () {
  var now = Date.now(), stale = 0;
  document.querySelectorAll("tr[data-read][data-cadence-days]").forEach(function (row) {
    var due = Date.parse(row.dataset.read + "T00:00:00Z") + Number(row.dataset.cadenceDays) * 864e5;
    if (now > due) {
      stale += 1;
      row.classList.add("stale");
      var mark = document.createElement("span");
      mark.className = "label stale";
      mark.textContent = "stale";
      row.cells[0].appendChild(document.createTextNode(" "));
      row.cells[0].appendChild(mark);
    }
  });
  var note = document.getElementById("stale-count");
  if (note) {
    note.textContent = stale === 0 ? "Today no row is past its cadence."
      : "Today " + stale + (stale === 1 ? " row is past its cadence" : " rows are past their cadence") + " and marked stale.";
  }
})();
</script>
"""
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
    # Pandoc 3.1 emits table-row parity classes that 3.3 omits. Keep the
    # published HTML byte-stable across those writers; site CSS does not use
    # these classes, and claim-ledger cadence stamping uses plain <tr> rows.
    html = dest.read_text(encoding="utf-8")
    dest.write_text(re.sub(r'<tr class="(?:header|odd|even)">', "<tr>", html), encoding="utf-8")


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
        f'status: "Draft. Site version {VERSION}. Rebuilt on every change; the digests let a reader check that a page matches the version recorded here."',
        "---",
        "",
        "A digest here is the SHA-256 of the artifact's source file in the site's repository, "
        "truncated to 16 hexadecimal characters for display. A change to the source changes the digest, "
        "and a change that alters what a page claims also gets a new version and a note.",
        "",
        *rows,
        "",
    ])


def plain(cell: str) -> str:
    return re.sub(r"<[^>]+>", "", cell).strip()


def stamp_cadence(html: str) -> str:
    """Stamp every claim row that has a read time with its read date and cadence.

    A row gets data-read (its earliest date) and, when its cadence expires, data-cadence-days;
    its read cell gains the cadence in words. A read-dated row with no cadence entry, or a read
    cell with no date, fails the build rather than going unmarked."""
    cadence = tomllib.loads((ROOT / "data" / "claim_cadence.toml").read_text(encoding="utf-8"))["cadence"]
    missing: list[str] = []

    def one_table(tm: re.Match[str]) -> str:
        table = tm.group(0)
        rows = TR.findall(table)
        if not rows:
            return table
        header = [plain(c) for c in CELL.findall(rows[0][1])]
        if "id" not in header or "read (UTC)" not in header:
            return table
        i_id, i_read = header.index("id"), header.index("read (UTC)")

        def one_row(rm: re.Match[str]) -> str:
            attrs, body = rm.group(1), rm.group(2)
            cells = CELL.findall(body)
            if len(cells) <= max(i_id, i_read) or "<th" in body:
                return rm.group(0)
            cid, read = plain(cells[i_id]), plain(cells[i_read])
            dates = sorted(DATE.findall(read))
            if not dates or cid not in cadence:
                missing.append(f"{cid} (read {read!r}, cadence {cadence.get(cid)!r})")
                return rm.group(0)
            c = cadence[cid]
            extra = f' data-read="{dates[0]}"'
            words = "does not expire"
            if c != "none":
                extra += f' data-cadence-days="{int(c)}"'
                words = f"{int(c)}-day cadence"
            parts = re.split(r"(<t[hd][^>]*>.*?</t[hd]>)", body, flags=re.DOTALL)
            cell_parts = [k for k, s in enumerate(parts) if s.startswith("<td")]
            k = cell_parts[i_read]
            parts[k] = parts[k].replace("</td>", f' <span class="cadence">({words})</span></td>')
            return f"<tr{attrs}{extra}>" + "".join(parts) + "</tr>"

        return TR.sub(one_row, table)

    html = TABLE.sub(one_table, html)
    if missing:
        sys.stderr.write("claim rows with a read time but no usable date or cadence:\n  " + "\n  ".join(missing) + "\n")
        raise SystemExit(1)
    return html.replace("</body>", STALE_SCRIPT + "</body>")


def build(out: Path) -> None:
    pages = sorted(SRC.glob("*.md"))
    if (SRC / "lab.md").exists():
        registry = subprocess.run([sys.executable, str(ROOT / "tools" / "check_lab.py")],
                                  capture_output=True, text=True, check=False)
        if registry.returncode != 0:
            sys.stderr.write(registry.stdout + registry.stderr)
            raise SystemExit(1)
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
    claims = out / "claims.html"
    claims.write_text(stamp_cadence(claims.read_text(encoding="utf-8")), encoding="utf-8")
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
