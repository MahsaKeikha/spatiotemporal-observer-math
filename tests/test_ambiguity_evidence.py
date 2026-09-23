from observer_math.ambiguity_evidence import ambiguity_evidence_point


def test_p72_ambiguity_count_does_not_reweight_robust_evidence():
    e = {"W0": 30.0, "W1": 2.0, "W2": 8.0}
    broad = ambiguity_evidence_point(
        "broad", ("W0", "W1", "W2"), e, threshold=20.0
    )
    compressed = ambiguity_evidence_point(
        "compressed", ("W0", "W1"), e, threshold=20.0
    )
    assert broad.retained_path_count == 3
    assert compressed.retained_path_count == 2
    assert broad.robust_e_value == 2.0
    assert compressed.robust_e_value == 2.0
    assert broad.crosses_threshold is False
    assert compressed.crosses_threshold is False


def test_p72_removing_binding_competitor_can_change_robust_evidence():
    e = {"W0": 30.0, "W1": 2.0}
    resolved = ambiguity_evidence_point("resolved", ("W0",), e, threshold=20.0)
    assert resolved.retained_path_count == 1
    assert resolved.robust_e_value == 30.0
    assert resolved.crosses_threshold is True
