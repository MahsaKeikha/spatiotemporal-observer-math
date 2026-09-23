"""P66 composes retained boundary alternatives with robust downstream e-evidence."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class RobustEvidencePoint:
    stage: str
    retained_paths: tuple[str, ...]
    robust_e_value: float
    selected_e_value: float
    crosses_threshold: bool


def robust_e_value(e_values: Mapping[str, float], retained_paths: Sequence[str]) -> float:
    """Return the union-null-valid worst-case e-value over retained paths."""
    paths = tuple(retained_paths)
    if not paths:
        raise ValueError("at least one retained path is required")
    missing = [p for p in paths if p not in e_values]
    if missing:
        raise KeyError(f"missing downstream e-values for: {missing}")
    values = [float(e_values[p]) for p in paths]
    if any(v < 0 for v in values):
        raise ValueError("e-values must be nonnegative")
    return min(values)


def evidence_path(
    stages: Mapping[str, Sequence[str]],
    e_values: Mapping[str, float],
    *,
    selected_path: str,
    threshold: float,
) -> tuple[RobustEvidencePoint, ...]:
    """Audit how boundary-set contraction changes robust evidence."""
    if selected_path not in e_values:
        raise KeyError("selected_path must have a downstream e-value")
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    selected = float(e_values[selected_path])
    return tuple(
        RobustEvidencePoint(
            stage=name,
            retained_paths=tuple(paths),
            robust_e_value=(robust := robust_e_value(e_values, paths)),
            selected_e_value=selected,
            crosses_threshold=robust >= threshold,
        )
        for name, paths in stages.items()
    )
