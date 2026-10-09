# Approved SQL example

This reader compares an approval, an application record, a database audit projection, and a later state observation.
It is for people who want to test whether those records agree before connecting a native export.

Use the locked development tools. The reader itself has no external dependencies.

```sh
uv sync --frozen --group dev
.venv/bin/python -m sql_illustration.check fixtures/matching-commit-later-change.json
```

The output includes `"result": "recorded_commit_matches"` and `"later_state": "supplied_state_differs"`.
That is the useful distinction: a later change does not erase an earlier matching execution record.

Version 0.1.0. The 16 fixtures are author-created examples. This source does not invoke Tadpole or a database.
The reader compares supplied records. It does not authenticate them or prove that an audit export is complete.

| Read next | Content |
|---|---|
| [Input contract](docs/INPUT-CONTRACT.md) | Fields, exact comparisons, outputs, and native input needed |
| [Source map](SOURCE-MAP.md) | Cho's case, pinned Tadpole source, and the actual native boundaries |
| [Design decisions](docs/architecture/DESIGN_DECISIONS.md) | Why SQL bytes, outcome, and later state stay separate |
| [Join the case](https://github.com/probityai/agent-evidence-atlas/issues/49) | Bring a native pair, another reader, or a check to keep |

Cho HyunJong (`hangum`) supplied the case in [the Lab thread](https://github.com/probityai/agent-evidence-atlas/issues/49#issuecomment-6072475161).
We own this illustration's fields and code. The producer owns its export semantics.
