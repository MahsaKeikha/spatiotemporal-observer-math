"""P62 boundary-confidence-set robust evidence utilities."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class BoundaryEvidenceEnvelope:
    evidence_by_worldtube: Mapping[str, float]
    delta: float
    alpha: float

    def __post_init__(self) -> None:
        if not self.evidence_by_worldtube:
            raise ValueError("at least one admissible world-tube is required")
        if any(v < 0 for v in self.evidence_by_worldtube.values()):
            raise ValueError("e-values must be nonnegative")
        if not 0.0 <= self.delta < 1.0:
            raise ValueError("delta must lie in [0,1)")
        if not 0.0 < self.alpha < 1.0:
            raise ValueError("alpha must lie in (0,1)")

    @property
    def robust_evidence(self) -> float:
        return min(self.evidence_by_worldtube.values(), default=inf)

    @property
    def robust_reject(self) -> bool:
        return self.robust_evidence >= 1.0 / self.alpha

    @property
    def end_to_end_error_budget(self) -> float:
        return min(1.0, self.delta + self.alpha)

    @property
    def weakest_worldtubes(self) -> tuple[str, ...]:
        value = self.robust_evidence
        return tuple(k for k, v in self.evidence_by_worldtube.items() if v == value)
