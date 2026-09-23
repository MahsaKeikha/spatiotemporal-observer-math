from observer_math.finite_sample_boundary import FiniteSampleBoundaryPoint
from observer_math.finite_sample_evidence import boundary_point_to_evidence


def test_bb_boundary_contraction_can_change_robust_decision_only_when_blocker_removed():
    evidence = {"W000": 30.0, "W001": 2.0}
    ambiguous = FiniteSampleBoundaryPoint(
        800, 0.2, True, 2, ("W000", "W001"), False
    )
    resolved = FiniteSampleBoundaryPoint(
        3200, 0.08, True, 1, ("W000",), True
    )
    a = boundary_point_to_evidence(ambiguous, evidence, threshold=20.0)
    b = boundary_point_to_evidence(resolved, evidence, threshold=20.0)
    assert a.crosses_threshold is False
    assert b.crosses_threshold is True
    assert b.robust_e_value > a.robust_e_value
