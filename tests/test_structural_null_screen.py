import numpy as np
from scipy.stats import wishart

from examples.gaussian_screen_calibration import empirical_factors, population_problem
from observer_math import (
    gaussian_factor_aware_near_competitor_screen,
    gaussian_null_cmi_covariance_error_bound,
    gaussian_structural_null_near_competitor_screen,
)
from observer_math.gaussian import gaussian_conditional_mutual_information


def test_quadratic_null_cmi_bound_contains_random_covariance_perturbations():
    base = np.array(
        [
            [1.49, -0.28, 0.7],
            [-0.28, 1.16, -0.4],
            [0.7, -0.4, 1.0],
        ]
    )
    eigenvalues = np.linalg.eigvalsh(base)
    radius = 1e-3
    bound = gaussian_null_cmi_covariance_error_bound(
        1,
        minimum_eigenvalue=float(eigenvalues[0]),
        maximum_eigenvalue=float(eigenvalues[-1]),
        covariance_spectral_error=radius,
    )
    rng = np.random.default_rng(8119)

    for _ in range(200):
        direction = rng.normal(size=(3, 3))
        direction = (direction + direction.T) / 2.0
        perturbation = direction * radius / np.linalg.norm(direction, ord=2)
        actual = base + rng.uniform(0.0, 1.0) * perturbation
        conditional_information = gaussian_conditional_mutual_information(
            actual, (0,), (1,), (2,)
        )
        assert conditional_information <= bound


def test_null_cmi_bound_is_quadratic_near_zero():
    larger = gaussian_null_cmi_covariance_error_bound(
        1,
        minimum_eigenvalue=0.5,
        maximum_eigenvalue=2.0,
        covariance_spectral_error=1e-5,
    )
    smaller = gaussian_null_cmi_covariance_error_bound(
        1,
        minimum_eigenvalue=0.5,
        maximum_eigenvalue=2.0,
        covariance_spectral_error=5e-6,
    )

    assert 3.9 < larger / smaller < 4.1


def test_structural_null_screen_reduces_graph_and_retains_population_path():
    problem = population_problem()
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    sample_count = 80_000_000_000
    rng = np.random.default_rng(20260909)
    empirical_joints = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=rng,
        )
        for joint in problem["joints"]
    )
    local_factors, transport_factors = empirical_factors(
        empirical_joints, problem
    )
    null_mask = np.ones((time_count, candidate_count), dtype=bool)
    for time in range(time_count):
        null_mask[time, time] = False
    arguments = {
        "candidates": problem["candidates"],
        "screening_sample_count": sample_count,
        "node_count": problem["node_count"],
        "subset_size": 3,
        "minimum_block_eigenvalues": problem["minimum"],
        "maximum_block_eigenvalues": problem["maximum"],
        "certification_local_score_errors": np.zeros(
            (time_count, candidate_count)
        ),
        "certification_transport_score_errors": np.zeros(
            (time_count - 1, candidate_count, candidate_count)
        ),
        "confidence": 0.975,
        "transport_weight": 0.25,
        "continuity_weight": 0.08,
    }
    generic = gaussian_factor_aware_near_competitor_screen(
        local_factors, transport_factors, **arguments
    )
    null_aware = gaussian_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        structural_integration_null_mask=null_mask,
        **arguments,
    )

    assert generic.screen.viable_state_count == 40
    assert generic.screen.viable_edge_count == 231
    assert null_aware.screen.viable_state_count == 6
    assert null_aware.screen.viable_edge_count == 5
    path = problem["population_path"]
    assert all(
        path[time] in null_aware.screen.viable_states[time]
        for time in range(time_count)
    )
    assert all(
        (path[time], path[time + 1]) in null_aware.screen.viable_edges[time]
        for time in range(time_count - 1)
    )


def test_false_structural_null_can_understate_score_error():
    local_factors = np.array([[[0.0, 1.0, 1.0]]])
    transport_factors = np.empty((0, 1, 1, 2))
    result = gaussian_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        ((0, 1),),
        1_000_000,
        3,
        2,
        structural_integration_null_mask=np.ones((1, 1), dtype=bool),
        minimum_block_eigenvalues=np.ones((1, 1)),
        maximum_block_eigenvalues=np.ones((1, 1)),
        certification_local_score_errors=np.zeros((1, 1)),
        certification_transport_score_errors=np.empty((0, 1, 1)),
    )
    admissible_positive_factor = min(
        0.5 * result.screening_local_factor_errors[0, 0, 0], 1.0
    )
    hypothetical_population_score = admissible_positive_factor ** (1.0 / 3.0)

    assert result.screening_local_score_errors[0, 0] == 0.0
    assert hypothetical_population_score > result.screening_local_score_errors[0, 0]
