"""P72 joins certified ambiguity counts to robust evidence without probabilistic reinterpretation."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .robust_boundary_evidence import robust_e_value


@dataclass(frozen=True)
class AmbiguityEvidencePoint:
    stage: str
    retained_path_count: int
    robust_e_value: float
    crosses_threshold: bool


def ambiguity_evidence_point(
    stage: str,
    retained_paths: Sequence[str],
    e_values: Mapping[str, float],
    *,
    threshold: float,
) -> AmbiguityEvidencePoint:
    """Report ambiguity cardinality beside, but not inside, the robust e-value."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    paths = tuple(retained_paths)
    if not paths:
        raise ValueError("retained_paths must be nonempty")
    value = robust_e_value(e_values, paths)
    return AmbiguityEvidencePoint(stage, len(paths), value, value >= threshold)
