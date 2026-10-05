#!/usr/bin/env python3
"""Check retained native qualification populations from their original bytes."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

SELECTED = (
    "aps-jcs-2026-10-04",
    "google-adk-responses-2026-10-04",
    "go-jcs-2026-10-04",
    "ag2-push-authority-2026-10-04",
    "remora-boundary-2026-10-04",
)


def check_selected_native_qualifications(register: dict[str, Any], root: Path) -> None:
    """Re-derive selected native reports after general artifact authentication.

    Parameters
    ----------
    register : dict of str to Any
        Complete register already checked for artifact hashes and claim bindings.
    root : Path
        Repository root containing the selected, tracked data-only validators.

    Raises
    ------
    ValueError
        If a selected validator is missing or refuses its retained native bytes.
    """
    identities = {record["id"] for record in register["records"]}
    for identity in SELECTED:
        if identity not in identities:
            continue
        path = root / "experiments" / identity / "validate_capsule.py"
        spec = importlib.util.spec_from_file_location("qualification_" + identity.replace("-", "_"), path)
        if spec is None or spec.loader is None:
            raise ValueError("native qualification validator is missing")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.validate()
