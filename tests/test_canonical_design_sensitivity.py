from examples.canonical_design_sensitivity import evaluate
from examples.full_benchmark_scalable_certification import population_problem


def test_bi_local_precision_audit_is_well_formed():
    _planted, candidates, local_factors, transport_factors = population_problem()
    baseline = evaluate(local_factors, transport_factors, candidates, {})
    tightened = evaluate(local_factors, transport_factors, candidates, {(0, 0): 0.0002})
    assert baseline["retained_paths"] >= 1
    assert tightened["retained_paths"] >= 1
    assert baseline["retained_nodes"] >= 1
    assert tightened["retained_nodes"] >= 1
