---
title: "Use Probity from an automated job"
description: "Look up public projects and read pinned Open Evidence Lab records from a script."
---

## Find a project

Read [llms.txt](llms.txt) for the navigation index or [catalog.json](catalog.json) for structured records. Components name the tools; repository records hold their pinned README sources. Integration profiles belong to a component.

Use the stable `id` for lookups. Follow `docs_url` for the quickstart and `source.commit` to reproduce the captured source.

## Check discovery

Use the [fixed discovery prompts and receipt checker](discovery-evaluation.md)
to retain a reader or agent session and review its answers against pinned public
sources. Keep actual discovery attempts separate from author-operated packet checks.

## Read a retained run

From a pinned Atlas checkout:

```sh
python3 tools/check_lab.py --list
python3 tools/check_lab.py --record E6-observer-admission --json
```

The checker validates artifact hashes and measured fields before returning a record. The JSON includes results, operator roles and review state.

## Share a result

Keep the source pins, command, raw output and retained artifact together. Submit them through the [run form](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-run.yml), or use the [correction form](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-correction.yml) when a recorded claim needs fixing.
