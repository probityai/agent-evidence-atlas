"""Check exact original/selected ZIP members against the public retention receipt."""

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('name', ['langgraph-durable-2026-10-02',
    'pydantic-failure-2026-10-02', 'model-operational-2026-10-02',
    'authority-recovery-2026-10-02', 'target-process-recovery-2026-10-02',
    'model-paired-cpu-2026-10-02', 'openai-agents-ticket-2026-10-02'])
def test_public_archive_preserves_selected_original_members(name: str) -> None:
    folder = ROOT / 'experiments' / name
    provenance = json.loads((folder / 'provenance.json').read_bytes())
    archive = folder / ('selected-capsule.zip' if name == 'model-operational-2026-10-02' else 'original-artifact.zip')
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


def model_provenance() -> dict:
    """Read the public original compact/full preparation mapping."""
    path = ROOT / 'experiments' / 'model-paired-cpu-2026-10-02' / 'provenance.json'
    return json.loads(path.read_bytes())


def check_full_mapping(provenance: dict) -> None:
    """Refuse invented compact identity, mismapped native bytes or hidden omissions."""
    compact = {item['member']: item for item in provenance['members']}
    full = provenance['fullPreparationMembers']
    summary = provenance['fullPreparationArchive']
    assert len({item['member'] for item in full}) == len(full) == summary['memberCount'] == 276
    selected = [item for item in full if item['retainedInCompact']]
    omitted = [item for item in full if not item['retainedInCompact']]
    assert len(selected) == len(compact) == summary['publiclyRetainedNativeMembers'] == 246
    assert len(omitted) == summary['omittedPreparationMembers'] == 30
    assert {item['compactMember'] for item in selected} == set(compact)
    for item in selected:
        assert item['member'] == 'run/' + item['compactMember']
        actual = compact[item['compactMember']]
        assert (item['sha256'], item['bytes']) == (actual['sha256'], actual['bytes'])
    assert all(item['compactMember'] is None for item in omitted)
    assert {'smol135-q4.gguf', 'smol360-q4.gguf'} <= {item['member'] for item in omitted}
    history = provenance['preparationHistory']
    assert history['cumulativeResponseBodyBytesAcrossTwoPreparations'] == (
        history['initialNoInferenceFailureResponseBodyBytes'] +
        history['correctedSuccessfulResponseBodyBytes'])
    assert history['cumulativeResponseBodyBytesAcrossTwoPreparations'] > 512 * 1024 * 1024


def test_full_preparation_mapping_preserves_native_bytes_and_omissions() -> None:
    check_full_mapping(model_provenance())


@pytest.mark.parametrize('field,value', [
    ('memberCount', 275), ('publiclyRetainedNativeMembers', 245),
    ('omittedPreparationMembers', 0)])
def test_changed_preparation_counts_refuse(field: str, value: int) -> None:
    provenance = model_provenance()
    provenance['fullPreparationArchive'][field] = value
    with pytest.raises(AssertionError):
        check_full_mapping(provenance)


def test_full_preparation_rebound_native_member_refuses() -> None:
    provenance = model_provenance()
    item = next(m for m in provenance['fullPreparationMembers'] if m['retainedInCompact'])
    item['sha256'] = '0' * 64
    with pytest.raises(AssertionError):
        check_full_mapping(provenance)


def test_full_preparation_hidden_omission_refuses() -> None:
    provenance = model_provenance()
    item = next(m for m in provenance['fullPreparationMembers'] if not m['retainedInCompact'])
    item['retainedInCompact'] = True
    item['compactMember'] = 'report.json'
    with pytest.raises(AssertionError):
        check_full_mapping(provenance)


def test_cumulative_transfer_cannot_be_reported_as_one_preparation() -> None:
    provenance = model_provenance()
    history = provenance['preparationHistory']
    history['cumulativeResponseBodyBytesAcrossTwoPreparations'] = history['correctedSuccessfulResponseBodyBytes']
    with pytest.raises(AssertionError):
        check_full_mapping(provenance)
