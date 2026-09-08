import numpy as np
from scipy.stats import wishart

from examples.trajectory_coupled_screen_calibration import (
    coupled_problem,
    extract_adjacent_covariances,
    run_coupled_trial,
    theoretical_variance_error_correlation,
)


def test_complete_trajectory_covariance_reproduces_population_adjacent_blocks():
    problem, trajectory, null_mask = coupled_problem()
    extracted = extract_adjacent_covariances(
        trajectory, problem["node_count"], len(problem["joints"])
    )

    assert trajectory.shape == (42, 42)
    assert np.all(np.linalg.eigvalsh(trajectory) > 0.0)
    assert all(
        np.allclose(actual, expected)
        for actual, expected in zip(extracted, problem["joints"], strict=True)
    )
    assert np.count_nonzero(null_mask) == 28


def test_coupled_trial_is_reproducible_and_covers_both_screens():
    first = run_coupled_trial((80_000, 19471))
    second = run_coupled_trial((80_000, 19471))

    assert first == second
    assert first["covariance_covered"]
    assert first["factor_covered"]
    assert first["score_covered"]
    assert first["null_score_covered"]
    assert first["population_path_retained"]
    assert first["null_population_path_retained"]


def test_gaussian_sample_variance_error_correlation_formula():
    covariance = np.array([[1.4, 0.55], [0.55, 0.9]])
    expected = theoretical_variance_error_correlation(covariance, 1, 1)
    draws = wishart.rvs(
        df=199,
        scale=covariance / 199,
        size=4_000,
        random_state=np.random.default_rng(2718),
    )
    variance_errors = np.column_stack(
        (draws[:, 0, 0] - covariance[0, 0], draws[:, 1, 1] - covariance[1, 1])
    )
    empirical = np.corrcoef(variance_errors, rowvar=False)

    assert np.allclose(np.diag(expected), 1.0)
    assert np.isclose(empirical[0, 1], expected[0, 1], atol=0.035)
