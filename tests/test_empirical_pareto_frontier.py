from observer_math.research_tradeoff import ResearchTradeoffPoint, pareto_frontier


def test_bg_duplicate_evidence_coordinate_does_not_create_false_preference():
    coarse = ResearchTradeoffPoint(0.02, 100, 1.0, 50)
    fine_but_costly = ResearchTradeoffPoint(0.01, 80, 1.0, 60)
    frontier = pareto_frontier((coarse, fine_but_costly))
    assert coarse in frontier
    assert fine_but_costly in frontier
