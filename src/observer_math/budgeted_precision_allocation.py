"""P80: exact budgeted allocation on a declared finite intervention library."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from itertools import combinations
from math import isfinite
from typing import Protocol


class AllocationEvaluator(Protocol):
    def __call__(self, intervention_ids: frozenset[str]) -> tuple[int, float]: ...


@dataclass(frozen=True)
class BudgetedAllocation:
    intervention_ids: tuple[str, ...]
    total_cost: float
    ambiguity_count: int
    secondary_score: float
    budget: float
    feasible_subsets_evaluated: int


def exact_budgeted_allocation(
    intervention_costs: Mapping[str, float],
    budget: float,
    evaluator: AllocationEvaluator,
    *,
    max_cardinality: int | None = None,
) -> BudgetedAllocation:
    """Return the best feasible subset in a declared finite intervention library.

    The primary objective is minimum certified ambiguity. The declared secondary
    score, total cost, cardinality, and lexicographic intervention IDs provide a
    deterministic tie break in that order.
    """
    if not intervention_costs:
        raise ValueError("intervention_costs must be nonempty")
    if not isfinite(budget) or budget < 0:
        raise ValueError("budget must be finite and nonnegative")
    normalized = {str(key): float(value) for key, value in intervention_costs.items()}
    if len(normalized) != len(intervention_costs):
        raise ValueError("intervention IDs must remain unique when converted to strings")
    if any(not isfinite(cost) or cost <= 0 for cost in normalized.values()):
        raise ValueError("intervention costs must be finite and positive")
    if max_cardinality is None:
        max_cardinality = len(normalized)
    if not isinstance(max_cardinality, int) or isinstance(max_cardinality, bool):
        raise TypeError("max_cardinality must be an integer")
    if max_cardinality < 0:
        raise ValueError("max_cardinality must be nonnegative")

    identifiers = tuple(sorted(normalized))
    candidates: list[tuple[tuple[int, float, float, int, tuple[str, ...]], BudgetedAllocation]] = []
    evaluated = 0
    for size in range(min(max_cardinality, len(identifiers)) + 1):
        for subset in combinations(identifiers, size):
            cost = sum(normalized[key] for key in subset)
            if cost > budget + 1e-12:
                continue
            ambiguity, secondary = evaluator(frozenset(subset))
            if ambiguity < 1 or not isfinite(secondary):
                raise ValueError("evaluator returned an invalid certified outcome")
            evaluated += 1
            outcome = BudgetedAllocation(
                intervention_ids=subset,
                total_cost=cost,
                ambiguity_count=ambiguity,
                secondary_score=float(secondary),
                budget=budget,
                feasible_subsets_evaluated=0,
            )
            rank = (ambiguity, float(secondary), cost, len(subset), subset)
            candidates.append((rank, outcome))
    if not candidates:
        raise ValueError("no feasible allocation exists")
    best = min(candidates, key=lambda item: item[0])[1]
    return BudgetedAllocation(
        intervention_ids=best.intervention_ids,
        total_cost=best.total_cost,
        ambiguity_count=best.ambiguity_count,
        secondary_score=best.secondary_score,
        budget=best.budget,
        feasible_subsets_evaluated=evaluated,
    )
