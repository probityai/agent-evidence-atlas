---
title: "Maintain the project catalog"
description: "Add a public project without changing existing project identities or Lab run records."
---

Edit `data/catalog.json`, then run the site build. It generates the task page, public JSON, llms.txt and sitemap.

## Add an entry

- Add a repository record with its public path and pinned README commit.
- Give the component a stable `id`, a task and a short summary. Link its repositories.
- Add a profile when a specific adapter or integration needs its own entry.
- Review the source and publication fields. Add its status source to `CLAIMS.md` and `data/catalog-sources.json`.

Components may share repositories or span several of them. Rename the display label without changing the ID. Retain an old ID when retiring a project.

Use public metadata in this file; planning notes belong in a private workspace. The schema owns field shape; `tools/discoverability/catalog.py` checks names, references, destinations and source pins. The build projects reviewed public fields.

## Check the update

```sh
python3 -m pip install -r requirements/discoverability-test.txt
python3 -m pytest -q tools/discoverability/test_catalog.py tests/test_discovery.py
python3 tools/build.py
python3 tools/build.py --check
python3 tools/check_links.py
python3 tools/check_lab.py
```

For a rename or retirement, validate with the previous catalog too:

```sh
python3 tools/discoverability/catalog.py validate data/catalog.json --previous tools/discoverability/catalog.seed.json
```

Keep project navigation in the catalog and measured runs in the Lab register.
