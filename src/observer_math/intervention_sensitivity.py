"""P78: intervention sensitivity over certified uncertainty blocks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class InterventionOutcome:
    block_id: str
    baseline_radius: float
    intervened_radius: float
    baseline_ambiguity: int
    intervened_ambiguity: int
    baseline_robust_evidence: float
    intervened_robust_evidence: float

    @property
    def ambiguity_reduction(self) -> int:
        return self.baseline_ambiguity - self.intervened_ambiguity

    @property
    def evidence_gain(self) -> float:
        return self.intervened_robust_evidence - self.baseline_robust_evidence


def evaluate_single_block_intervention(
    block_id: str,
    baseline_radius: float,
    intervened_radius: float,
    evaluator: Callable[[str, float], tuple[int, float]],
) -> InterventionOutcome:
    """Rerun the declared certification/evidence evaluator before and after tightening one block."""
    if baseline_radius < 0 or intervened_radius < 0:
        raise ValueError("uncertainty radii must be nonnegative")
    if intervened_radius > baseline_radius:
        raise ValueError("intervention must not increase the declared uncertainty radius")
    n0, e0 = evaluator(block_id, baseline_radius)
    n1, e1 = evaluator(block_id, intervened_radius)
    if n0 < 1 or n1 < 1:
        raise ValueError("retained ambiguity count must contain at least one complete path")
    if e0 <= 0 or e1 <= 0:
        raise ValueError("robust evidence must be positive")
    return InterventionOutcome(block_id, baseline_radius, intervened_radius, n0, n1, e0, e1)
