import pytest

from observer_math.precision_workload import precision_workload_curve, scale_action_intervals


def test_precision_improvement_can_reduce_certified_workload():
    actions = {"W0": 10.0, "W1": 9.7, "W2": 8.8}
    radii = {"W0": 0.4, "W1": 0.5, "W2": 0.6}
    points = precision_workload_curve(actions, radii, (1.0, 0.5, 0.1))
    assert points[0].retained_count >= points[-1].retained_count
    assert "W0" in points[-1].retained_paths


def test_zero_radius_scale_reduces_to_nominal_action_comparison():
    actions = {"A": 2.0, "B": 1.0}
    radii = {"A": 5.0, "B": 5.0}
    intervals = scale_action_intervals(actions, radii, 0.0)
    assert intervals["A"].lower == intervals["A"].upper == 2.0
    assert intervals["B"].lower == intervals["B"].upper == 1.0


def test_negative_precision_scale_rejected():
    with pytest.raises(ValueError):
        scale_action_intervals({"A": 1.0}, {"A": 0.1}, -0.1)
