"""Check exact original/selected ZIP members against the public retention receipt."""

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('name', ['langgraph-durable-2026-10-02',
    'pydantic-failure-2026-10-02', 'model-operational-2026-10-02'])
def test_public_archive_preserves_selected_original_members(name: str) -> None:
    folder = ROOT / 'experiments' / name
    provenance = json.loads((folder / 'provenance.json').read_bytes())
    archive = folder / ('selected-capsule.zip' if name.startswith('model') else 'original-artifact.zip')
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == provenance['retainedArchiveSha256']
    selected = {item['member']: item for item in provenance['members'] if item['selected']}
    with zipfile.ZipFile(archive) as bundle:
        assert set(bundle.namelist()) == set(selected)
        for member, pin in selected.items():
            raw = bundle.read(member)
            assert len(raw) == pin['bytes']
            assert hashlib.sha256(raw).hexdigest() == pin['sha256']
        assert bundle.read(provenance['reportMember']) == (folder / 'report.json').read_bytes()
    assert provenance['roles']['independentEffectCustody'] == 'not-established'
