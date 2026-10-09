#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements/public-layout.txt

# Match the site's existing pinned Pandoc job, without changing shared packages.
mkdir -p .venv/toolchain
curl -fsSL https://github.com/jgm/pandoc/releases/download/3.3/pandoc-3.3-1-amd64.deb -o .venv/pandoc.deb
printf '%s  %s\n' 7a6625d5aeb6b8666375807a3e16cc00659c48fb88299707651f60d88c31a360 .venv/pandoc.deb | sha256sum -c -
dpkg-deb -x .venv/pandoc.deb .venv/toolchain
export PATH="$PWD/.venv/toolchain/usr/bin:$PATH"
pandoc --version
.venv/bin/python scripts/qualify_approved_sql_site.py
