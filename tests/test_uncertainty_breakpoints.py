import numpy as np

from observer_math.uncertainty_breakpoints import (
    pairwise_affine_breakpoints,
    positive_affine_crossing,
)


def test_p74_positive_affine_crossing():
    assert positive_affine_crossing(1.0, 2.0, 2.0, 1.0) == 1.0
    assert positive_affine_crossing(1.0, 1.0, 2.0, 1.0) is None


def test_p74_pairwise_breakpoints_are_sorted_unique_and_positive():
    roots = pairwise_affine_breakpoints(
        np.array([0.0, 1.0, 2.0]),
        np.array([2.0, 1.0, 0.0]),
    )
    assert roots == (1.0,)
