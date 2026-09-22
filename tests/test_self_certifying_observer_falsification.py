from examples.self_certifying_observer_falsification import run_trial

def test_exact_equivalence_never_certifies():
    for seed in range(10):
        assert not run_trial("exact_equivalence",seed)["certified"]

def test_missing_candidate_coverage_blocks_singleton_certificate():
    for seed in range(10):
        result=run_trial("candidate_misspecification",seed)
        assert not result["coverage"]
        assert not result["certified"]

def test_certification_requires_positive_evidence_and_structural_margin():
    result=run_trial("nominal",42)
    if result["certified"]:
        assert result["final_llr"]>0
        assert result["final_radius"]<.62
