import numpy as np
import pytest

from observer_math.minimum_precision_intervention import minimum_radius_on_declared_grid


def test_p79_finds_least_tightening_that_changes_decision():
    def evaluator(_block, radius):
        if radius > 0.2:
            return 20, 4.0
        if radius > 0.1:
            return 5, 12.0
        return 2, 25.0

    out = minimum_radius_on_declared_grid("B3", 0.4, (0.3, 0.2, 0.1, 0.05), 20.0, evaluator)
    assert out.achieved
    assert np.isclose(out.required_radius, 0.1)
    assert np.isclose(out.radius_reduction, 0.3)
    assert out.ambiguity_count == 2
    assert np.isclose(out.robust_evidence, 25.0)


def test_p79_rejects_nonmonotone_declared_sweep():
    values = {0.4: 5.0, 0.2: 4.0}
    with pytest.raises(ValueError, match="not monotone"):
        minimum_radius_on_declared_grid("B", 0.4, (0.2,), 20.0, lambda _b, r: (2, values[r]))
