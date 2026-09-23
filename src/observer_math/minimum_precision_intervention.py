"""P79: minimum certified precision intervention under a monotone declared sweep."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class DecisionEvaluator(Protocol):
    def __call__(self, block_id: str, radius: float) -> tuple[int, float]: ...


@dataclass(frozen=True)
class PrecisionIntervention:
    block_id: str
    baseline_radius: float
    required_radius: float | None
    radius_reduction: float | None
    ambiguity_count: int | None
    robust_evidence: float | None
    target_evidence: float
    achieved: bool


def minimum_radius_on_declared_grid(
    block_id: str,
    baseline_radius: float,
    candidate_radii: tuple[float, ...],
    target_evidence: float,
    evaluator: DecisionEvaluator,
) -> PrecisionIntervention:
    """Find the least tightening on a declared grid that reaches the evidence target."""
    if baseline_radius < 0 or target_evidence <= 0:
        raise ValueError("baseline radius must be nonnegative and target evidence positive")
    radii = sorted({float(r) for r in candidate_radii if 0 <= r <= baseline_radius}, reverse=True)
    if baseline_radius not in radii:
        radii.insert(0, float(baseline_radius))
    previous_evidence = None
    for radius in radii:
        ambiguity, evidence = evaluator(block_id, radius)
        if ambiguity < 1 or evidence <= 0:
            raise ValueError("evaluator returned invalid certified output")
        if previous_evidence is not None and evidence + 1e-12 < previous_evidence:
            raise ValueError("declared sweep is not monotone in robust evidence")
        previous_evidence = evidence
        if evidence >= target_evidence:
            return PrecisionIntervention(
                block_id, baseline_radius, radius, baseline_radius - radius,
                ambiguity, evidence, target_evidence, True,
            )
    return PrecisionIntervention(
        block_id, baseline_radius, None, None, None, None, target_evidence, False
    )
