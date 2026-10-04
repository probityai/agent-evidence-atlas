# Maintain the project catalog

Edit `data/catalog.json`, then run the site build. It generates the task page, public JSON, llms.txt and sitemap.

<a id="add-an-entry"></a>

## Add an entry

- Add a repository record with its public path and pinned README commit.
- Give the component a stable `id`, a task and a short summary. Link its repositories.
- Add a profile when a specific adapter or integration needs its own entry.
- Review the source and publication fields. Add its status source to `CLAIMS.md` and `data/catalog-sources.json`.

Components may share repositories or span several of them. Rename the display label without changing the ID. Retain an old ID when retiring a project.

Use public metadata in this file; planning notes belong in a private workspace. The schema owns field shape; `tools/discoverability/catalog.py` checks names, references, destinations and source pins. The build projects reviewed public fields.

<a id="check-the-update"></a>

## Check the update

``` sh
python3 -m pip install -r requirements/discoverability-test.txt
python3 -m pytest -q tools/discoverability/test_catalog.py tests/test_discovery.py
python3 tools/build.py
python3 tools/build.py --check
python3 tools/check_links.py
python3 tools/check_lab.py
```

For a rename or retirement, validate with the previous catalog too:

``` sh
python3 tools/discoverability/catalog.py validate data/catalog.json --previous tools/discoverability/catalog.seed.json
```

<a id="import-a-reviewed-catalog"></a>

## Import a reviewed catalog

Keep the current catalog as the baseline. Import the reviewed public fields with stable IDs and publication gates, then validate against that baseline. Review its pinned README sources and retain their earlier rows in `data/catalog-sources.json`.

Run the native build and compare `docs/catalog.json` with the reviewed public projection. They should contain the same repositories, components and profiles. Update the C rows in `CLAIMS.md` and the catalog revision in `data/versions.toml` with the source capture.

Leave planning fields out of the import. Generate the pages and indexes from the catalog; the source history retains the earlier pins.

For a source refresh, give each component quickstart the same reviewed README pin as its owning repository. Append source history; keep earlier reviews. Current navigation does not update historical Lab claims or experiment objects.

Keep project navigation in the catalog and measured runs in the Lab register.

[HTML view](catalog.html) | [Agent guide](llms.txt)
