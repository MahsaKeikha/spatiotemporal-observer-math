import pytest

from observer_math.robust_boundary_evidence import evidence_path, robust_e_value


def test_p66_unresolved_competitor_controls_robust_evidence():
    e = {"W0": 30.0, "W1": 2.0}
    assert robust_e_value(e, ("W0", "W1")) == 2.0
    assert robust_e_value(e, ("W0",)) == 30.0


def test_p66_selected_path_cannot_override_retained_competitor():
    points = evidence_path(
        {"ambiguous": ("W0", "W1"), "resolved": ("W0",)},
        {"W0": 30.0, "W1": 2.0},
        selected_path="W0",
        threshold=20.0,
    )
    assert points[0].selected_e_value == 30.0
    assert points[0].crosses_threshold is False
    assert points[1].crosses_threshold is True


def test_p66_missing_evidence_is_rejected():
    with pytest.raises(KeyError):
        robust_e_value({"W0": 3.0}, ("W0", "W1"))
