#!/usr/bin/env python3
"""Check retained artifact hashes and measured claim bindings in the lab register."""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger("atlas.lab_register")
RESULTS = {"pass", "fail", "unknown", "not-exercised", "out-of-scope"}


def require(condition: bool, message: str) -> None:
    """Raise a bounded validation error when a register condition fails."""
    if not condition:
        raise ValueError(message)


def artifact_path(root: Path, reference: str) -> Path:
    """Resolve a published register reference inside its repository.

    Parameters
    ----------
    root : Path
        Repository root containing original retained files.
    reference : str
        Relative path from the published ``lab/register.json`` directory.

    Returns
    -------
    Path
        Resolved source path inside ``root``.

    Raises
    ------
    ValueError
        If a reference is absolute or escapes the repository. This checker
        reads retained local bytes and never retrieves candidate URLs.
    """
    require(isinstance(reference, str) and not Path(reference).is_absolute(),
            "artifact reference must be a relative local path")
    path = (root / "lab" / reference).resolve()
    require(path.is_relative_to(root.resolve()), "artifact reference escapes the repository")
    return path


def pointer_value(document: Any, pointer: str) -> Any:
    """Read an RFC 6901 JSON pointer without guessing missing claim fields.

    Parameters
    ----------
    document : Any
        Parsed retained report, authenticated by :func:`check_artifacts`.
    pointer : str
        Nonempty JSON pointer to a measured field, including ``~0`` and ``~1``
        escaping where needed. Array indices must use their canonical form.

    Returns
    -------
    Any
        Exact value recorded at that pointer.

    Raises
    ------
    ValueError
        If the pointer syntax is invalid or the field/index does not exist.
    """
    require(isinstance(pointer, str) and pointer.startswith("/"), "claim pointer is invalid")
    value = document
    for encoded in pointer[1:].split("/"):
        require(re.search(r"~(?![01])", encoded) is None, "claim pointer is invalid")
        token = encoded.replace("~1", "/").replace("~0", "~")
        value = _pointer_step(value, token)
    return value


def _pointer_step(value: Any, token: str) -> Any:
    """Resolve one object member or array index with an exact missing-field error."""
    if isinstance(value, dict):
        require(token in value, "claim pointer does not name a retained field")
        return value[token]
    if isinstance(value, list):
        require(re.fullmatch(r"0|[1-9][0-9]*", token) is not None, "claim pointer array index is invalid")
        require(int(token) < len(value), "claim pointer does not name a retained field")
        return value[int(token)]
    raise ValueError("claim pointer does not name a retained field")


def check_artifacts(record: dict[str, Any], root: Path) -> set[str]:
    """Authenticate every artifact before using its report values.

    Parameters
    ----------
    record : dict of str to Any
        Register entry with a nonempty ``artifacts`` list of path/digest pairs.
    root : Path
        Repository root used by :func:`artifact_path`.

    Returns
    -------
    set of str
        Unique validated artifact references.

    Raises
    ------
    ValueError
        For malformed, repeated, missing, escaped or altered artifacts.
    """
    artifacts = record.get("artifacts")
    require(isinstance(artifacts, list) and bool(artifacts), "record has no retained artifacts")
    require(all(isinstance(artifact, dict) for artifact in artifacts), "artifact entry is invalid")
    references: set[str] = set()
    for artifact in artifacts:
        reference, expected = artifact.get("path"), artifact.get("sha256")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
                "artifact SHA-256 is invalid")
        path = artifact_path(root, reference)
        require(reference not in references, "record repeats an artifact reference")
        require(path.is_file(), "retained artifact is missing")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                "retained artifact differs from its SHA-256")
        references.add(reference)
    return references


def check_claim(claim: dict[str, Any], report: Any) -> None:
    """Require measured verdicts to bind to the exact retained report value.

    Parameters
    ----------
    claim : dict of str to Any
        Unique named claim. ``pass`` or ``fail`` requires ``recordedField`` and
        ``expectedValue``; other outcomes must not pretend to be measured.
    report : Any
        Hash-checked report read by :func:`validate_register`.

    Raises
    ------
    ValueError
        If the result is invalid, the measured binding is absent/wrong, or an
        unmeasured outcome carries a measured field. Equality is recursively
        type-strict, so ``True`` cannot substitute for integer ``1``, including
        inside an object or array. Integer and floating point types differ.

    Notes
    -----
    A correct binding verifies what the report says, not the interpretation of
    the claim or independent operation. Those remain explicit review duties.
    """
    result = claim.get("result")
    require(isinstance(result, str) and result in RESULTS, "claim result is invalid")
    if result not in {"pass", "fail"}:
        require("recordedField" not in claim and "expectedValue" not in claim,
                "unmeasured claim carries a measured binding")
        return
    require("recordedField" in claim and "expectedValue" in claim,
            "measured claim has no retained-field binding")
    actual = pointer_value(report, claim["recordedField"])
    expected = claim["expectedValue"]
    require(_same_json_value(actual, expected),
            "measured claim differs from the retained report")


def _same_json_value(actual: Any, expected: Any) -> bool:
    """Compare JSON values without Python's nested Boolean/numeric coercion.

    Parameters
    ----------
    actual, expected : Any
        Parsed JSON values, potentially containing objects and arrays.

    Returns
    -------
    bool
        Whether every corresponding value has the same Python JSON type and
        value. Object member order does not matter; array order does.
    """
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, dict):
        return actual.keys() == expected.keys() and all(
            _same_json_value(value, expected[key]) for key, value in actual.items()
        )
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(
            _same_json_value(value, counterpart) for value, counterpart in zip(actual, expected)
        )
    return actual == expected


def _check_record(record: dict[str, Any], root: Path) -> None:
    """Check report inclusion and uniquely named claim bindings for one record."""
    references = check_artifacts(record, root)
    require(record.get("report") in references, "record report is not a retained artifact")
    report = json.loads(artifact_path(root, record["report"]).read_text(encoding="utf-8"))
    claims = record.get("claimResults")
    require(isinstance(claims, list) and bool(claims), "record has no claim results")
    require(all(isinstance(claim, dict) for claim in claims), "claim entry is invalid")
    names = [claim.get("claim") for claim in claims]
    require(all(isinstance(name, str) and bool(name) for name in names), "claim name is invalid")
    require(len(names) == len(set(names)), "record repeats a claim")
    for claim in claims:
        check_claim(claim, report)


def validate_register(register: dict[str, Any], root: Path) -> None:
    """Verify local register evidence while preserving the limits of review.

    Parameters
    ----------
    register : dict of str to Any
        Parsed protocol-0.1 registry with unique records.
    root : Path
        Repository root containing all referenced source artifacts.

    Raises
    ------
    ValueError
        If structure, file integrity or claim binding fails. Refusals log a
        bounded reason, never candidate report contents or credentials.

    Notes
    -----
    This is an integrity and measured-field gate. It cannot certify an
    externally operated witness or turn a fixture into host-project adoption.
    """
    try:
        require(isinstance(register, dict), "register structure is invalid")
        require(register.get("protocolVersion") == "0.1", "register protocol version is unsupported")
        records = register.get("records")
        require(isinstance(records, list) and bool(records), "register has no records")
        require(all(isinstance(record, dict) for record in records), "record entry is invalid")
        ids = [record.get("id") for record in records]
        require(all(isinstance(identity, str) and bool(identity) for identity in ids), "record id is invalid")
        require(len(ids) == len(set(ids)), "register repeats a record id")
        for record in records:
            _check_record(record, root)
    except ValueError as exc:
        LOGGER.error("lab register refused: %s", exc)
        raise


def main() -> None:
    """Validate the checked-in register without network reads or extra dependencies."""
    register = json.loads((ROOT / "data" / "lab-register.json").read_text(encoding="utf-8"))
    validate_register(register, ROOT)
    print(f"lab register: {len(register['records'])} record(s), artifact hashes and measured bindings pass")


if __name__ == "__main__":
    main()
