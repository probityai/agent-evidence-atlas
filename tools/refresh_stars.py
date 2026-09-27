#!/usr/bin/env python3
"""Re-read every atlas star count and write the new values, with their read time.

    python3 tools/refresh_stars.py            read, then rewrite data/atlas.toml and CLAIMS.md
    python3 tools/refresh_stars.py --dry-run  read and print, change nothing

`tools/rederive.py` only compares. This tool is the other half: it takes a fresh
read of every entry in data/atlas.toml that names a `repo`, rewrites each `stars`
value in place, records the read time as `meta.stars_read`, and rewrites every
claim-ledger row that quotes one of those counts. It changes nothing unless every
read succeeded, so a partial refresh can never leave some counts new and others
old under one read time. Run `python3 tools/gen_atlas.py` afterwards to regenerate
the page.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "atlas.toml"
CLAIMS = ROOT / "CLAIMS.md"
UA = "agent-evidence-atlas-claim-check (https://github.com/probityai/agent-evidence-atlas)"

ENTRY = re.compile(r'^repo = "([^"]+)"\n((?:(?!\[\[)[^\n]*\n)*?)stars = ([0-9]+)$', re.MULTILINE)


def stars(repo: str) -> int:
    headers = {"User-Agent": UA, "Accept": "application/json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return int(json.load(r)["stargazers_count"])


def main() -> int:
    dry = "--dry-run" in sys.argv[1:]
    text = DATA.read_text(encoding="utf-8")
    found = [(m.group(1), int(m.group(3))) for m in ENTRY.finditer(text)]
    declared = len(re.findall(r'^repo = "', text, flags=re.MULTILINE))
    if not found or len(found) != declared:
        print(f"matched {len(found)} repo/stars pairs but the file declares {declared} repos; nothing written")
        return 2
    new: dict[str, int] = {}
    for repo, old in found:
        try:
            new[repo] = stars(repo)
        except Exception as e:  # noqa: BLE001 - one failed read stops the whole refresh
            print(f"UNREAD {repo}: {type(e).__name__}: {e}; nothing written")
            return 2
        print(f"{repo:48} {old:>7} -> {new[repo]:>7}")
    read_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if dry:
        print(f"dry run: {len(new)} counts read at {read_at}; nothing written")
        return 0

    def repl(m: re.Match[str]) -> str:
        return f'repo = "{m.group(1)}"\n{m.group(2)}stars = {new[m.group(1)]}'

    text = ENTRY.sub(repl, text)
    text, n = re.subn(r'^stars_read = "[^"]*"$', f'stars_read = "{read_at}"', text, flags=re.MULTILINE)
    if n != 1:
        print("data/atlas.toml has no single meta.stars_read line; nothing written")
        return 2
    claims = CLAIMS.read_text(encoding="utf-8")
    changed_rows = 0
    for repo, old in found:
        before = f"{old:,} stars"
        after = f"{new[repo]:,} stars"
        if before != after and before in claims:
            changed_rows += claims.count(before)
            claims = claims.replace(before, after)
    DATA.write_text(text, encoding="utf-8")
    CLAIMS.write_text(claims, encoding="utf-8")
    print(f"wrote {len(new)} counts read at {read_at}; {changed_rows} claim-ledger quotation(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
