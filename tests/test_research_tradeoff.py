from observer_math.research_tradeoff import (
    ResearchTradeoffPoint,
    dominates,
    pareto_frontier,
)


def test_p73_dominance_requires_no_tradeoff():
    a = ResearchTradeoffPoint(0.1, 2, 10.0, 50)
    b = ResearchTradeoffPoint(0.2, 3, 8.0, 60)
    assert dominates(a, b)


def test_p73_conflicting_axes_are_not_forced_into_ranking():
    precision_better = ResearchTradeoffPoint(0.1, 3, 8.0, 60)
    evidence_better = ResearchTradeoffPoint(0.2, 2, 20.0, 40)
    assert not dominates(precision_better, evidence_better)
    assert not dominates(evidence_better, precision_better)
    assert set(pareto_frontier((precision_better, evidence_better))) == {
        precision_better, evidence_better
    }
