import json
import sys
from pathlib import Path

from run import CASES, run_case


ADAPTER = '''
import json
import os
import sys
import urllib.request

cases = json.load(open(sys.argv[1], encoding="utf-8"))
case = next(c for c in cases if c["id"] == sys.argv[2])
body = json.dumps({"operationKey": case["operationKey"]}).encode("ascii")
def effect():
    request = urllib.request.Request(os.environ["PROBITY_EFFECT_URL"], body, method="POST")
    urllib.request.urlopen(request, timeout=2).read()

effect()
if case["mode"] == "no-dedup" or os.environ.get("EXTRA_EFFECT"):
    effect()
print(json.dumps({
    "requestIds": [2, 2 if os.environ.get("REUSED_ID") else 3],
    "firstResponseLost": True,
    "retrySource": "application",
    "protocolVersion": case["protocolVersion"],
    "effects": 999,
}))
'''


def adapter(tmp_path: Path) -> list[str]:
    script = tmp_path / "adapter.py"
    script.write_text(ADAPTER, encoding="utf-8")
    return [sys.executable, str(script)]


def test_both_modes_count_effects_at_the_sink(tmp_path):
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    results = [run_case(case, adapter(tmp_path), 5) for case in cases]
    assert [(r["effects"], r["errors"]) for r in results] == [(2, []), (1, [])]


def test_keyed_retry_that_mutates_again_fails(tmp_path, monkeypatch):
    monkeypatch.setenv("EXTRA_EFFECT", "1")
    case = json.loads(CASES.read_text(encoding="utf-8"))[1]
    result = run_case(case, adapter(tmp_path), 5)
    assert result["effects"] == 2
    assert result["errors"] == ["effect sink recorded 2, expected 1"]


def test_reused_json_rpc_id_fails_even_with_the_right_effect_count(tmp_path, monkeypatch):
    monkeypatch.setenv("REUSED_ID", "1")
    case = json.loads(CASES.read_text(encoding="utf-8"))[0]
    result = run_case(case, adapter(tmp_path), 5)
    assert result["effects"] == 2
    assert result["errors"] == ["retry must use a fresh JSON-RPC request ID"]


def test_missing_adapter_is_reported(tmp_path):
    case = json.loads(CASES.read_text(encoding="utf-8"))[0]
    result = run_case(case, [sys.executable, str(tmp_path / "missing.py")], 5)
    assert result["effects"] == 0
    assert "adapter did not print a JSON report" in result["errors"]
    assert any(error.startswith("adapter exited 2:") for error in result["errors"])
