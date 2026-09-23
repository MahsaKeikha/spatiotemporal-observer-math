"""P73 reports precision, ambiguity, evidence, and workload as a vector."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchTradeoffPoint:
    precision_radius: float
    retained_path_count: int
    robust_e_value: float
    graph_workload: int


def dominates(a: ResearchTradeoffPoint, b: ResearchTradeoffPoint) -> bool:
    """Return whether a is no worse on every declared axis and better on one."""
    no_worse = (
        a.precision_radius <= b.precision_radius
        and a.retained_path_count <= b.retained_path_count
        and a.robust_e_value >= b.robust_e_value
        and a.graph_workload <= b.graph_workload
    )
    strictly_better = (
        a.precision_radius < b.precision_radius
        or a.retained_path_count < b.retained_path_count
        or a.robust_e_value > b.robust_e_value
        or a.graph_workload < b.graph_workload
    )
    return no_worse and strictly_better


def pareto_frontier(points: tuple[ResearchTradeoffPoint, ...]) -> tuple[ResearchTradeoffPoint, ...]:
    """Keep nondominated points without collapsing axes into an arbitrary score."""
    return tuple(
        p for i, p in enumerate(points)
        if not any(dominates(q, p) for j, q in enumerate(points) if i != j)
    )
