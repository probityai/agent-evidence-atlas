# Use Probity from an automated job

Use the [worked report example](evidence-test-meaning.md) to interpret test results separately from evidence conclusions. Its [retained accounting procedure](experiments/w3c-report-replay-2026-10-06/README.md) checks original files through the maintained Lab consumer.

<a id="find-a-project"></a>

## Find a project

Read [llms.txt](llms.txt) for the navigation index or [catalog.json](catalog.json) for structured records. Components name the tools; repository records hold their pinned README sources. Integration profiles belong to a component.

Use the stable `id` for lookups. Follow `docs_url` for the quickstart and `source.commit` to reproduce the captured source.

<a id="check-discovery"></a>

## Check discovery

Use the [fixed discovery prompts and receipt checker](discovery-evaluation.md) to retain a reader or agent session and review its answers against pinned public sources. Keep actual discovery attempts separate from author-operated packet checks.

<a id="run-a-local-replay"></a>

## Run a local replay

To produce a new local APS/PriorSeal capture, use the [replay tools guide](replay-tools.md). Declare the caller and keep the source hashes, actual process logs and result together. The guide links one complete pinned procedure, including the copied-file route.

<a id="read-a-retained-run"></a>

## Read a retained run

From a pinned Atlas checkout:

``` sh
python3 tools/check_lab.py --list
python3 tools/check_lab.py --record E6-observer-admission --json
```

The checker validates artifact hashes and measured fields before returning a record. The JSON includes results, operator roles and review state.

<a id="share-a-result"></a>

## Share a result

Keep the source pins, command, raw output and retained artifact together. Submit them through the [run form](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-run.yml), or use the [correction form](https://github.com/probityai/agent-evidence-atlas/issues/new?template=evidence-correction.yml) when a recorded claim needs fixing.

[HTML view](automation.html) | [Agent guide](llms.txt)
