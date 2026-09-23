from observer_math.finite_sample_boundary import FiniteSampleBoundaryPoint
from observer_math.finite_sample_evidence import boundary_point_to_evidence


def test_p68_unavailable_boundary_certificate_does_not_invent_evidence():
    point = FiniteSampleBoundaryPoint(40, 1.2, False, None, (), False)
    out = boundary_point_to_evidence(point, {"W0": 30.0}, threshold=20.0)
    assert out.robust_e_value is None
    assert out.crosses_threshold is None


def test_p68_retained_competitor_can_block_finite_sample_conclusion():
    point = FiniteSampleBoundaryPoint(800, 0.2, True, 2, ("W0", "W1"), False)
    out = boundary_point_to_evidence(
        point, {"W0": 30.0, "W1": 2.0}, threshold=20.0
    )
    assert out.robust_e_value == 2.0
    assert out.crosses_threshold is False
