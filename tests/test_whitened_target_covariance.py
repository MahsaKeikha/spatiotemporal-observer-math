import numpy as np

from observer_math.matrix_chernoff import gaussian_weighted_wishart_matrix_bound
from observer_math.physical_relaxation import exponential_relaxation_markov_factorization
from observer_math.whitened_target_covariance import (
    exponential_relaxation_whitened_projected_covariance,
    gaussian_whitened_projected_covariance_bound,
    gaussian_whitened_scalar_chi_square_bound,
    separable_gaussian_whitened_projected_covariance,
    whitened_nuisance_projector,
)


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _target_design(times: np.ndarray) -> np.ndarray:
    centered = times - np.mean(times)
    return np.column_stack((np.ones(times.size), centered))


def _simulate_relaxation(
    times: np.ndarray,
    tau: float,
    spatial_covariance: np.ndarray,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    sample_count = times.size
    dimension = spatial_covariance.shape[0]
    spatial_factor = np.linalg.cholesky(spatial_covariance)
    innovations = rng.standard_normal((sample_count, dimension)) @ spatial_factor.T
    values = np.empty_like(innovations)
    values[0] = innovations[0]
    for index, gap in enumerate(np.diff(times)):
        alpha = np.exp(-gap / tau)
        values[index + 1] = (
            alpha * values[index]
            + np.sqrt(1.0 - alpha * alpha) * innovations[index + 1]
        )
    return values


def test_whitened_projector_is_orthogonal_and_annihilates_transformed_design() -> None:
    times = _target_times()
    design = _target_design(times)
    whitening = exponential_relaxation_markov_factorization(times, 0.78).whitening_matrix

    projector = whitened_nuisance_projector(whitening, design)
    transformed_design = whitening @ design

    assert np.allclose(projector, projector.T, atol=1e-12)
    assert np.allclose(projector @ projector, projector, atol=1e-12)
    assert np.allclose(projector @ transformed_design, 0.0, atol=1e-11)
    assert np.isclose(np.trace(projector), times.size - design.shape[1], atol=1e-11)


def test_whitened_covariance_is_exactly_invariant_to_declared_nuisance_mean() -> None:
    times = _target_times()
    design = _target_design(times)
    tau = 0.78
    whitening = exponential_relaxation_markov_factorization(times, tau).whitening_matrix
    covariance = np.array([[1.0, 0.35], [0.35, 0.8]])
    stochastic = _simulate_relaxation(times, tau, covariance, seed=20261121)
    coefficients = np.array([[8.0, -5.0], [3.5, 6.0]])
    shifted = stochastic + design @ coefficients

    base = separable_gaussian_whitened_projected_covariance(
        stochastic,
        whitening,
        design,
    )
    nuisance_shifted = separable_gaussian_whitened_projected_covariance(
        shifted,
        whitening,
        design,
    )

    assert np.allclose(base, nuisance_shifted, atol=2e-12)


def test_whitened_matrix_bound_is_exactly_the_unit_weight_wishart_bound() -> None:
    times = _target_times()
    design = _target_design(times)
    degrees = times.size - design.shape[1]

    whitened = gaussian_whitened_projected_covariance_bound(
        design,
        block_dimension=2,
        block_count=3,
        confidence=0.975,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )
    reference = gaussian_weighted_wishart_matrix_bound(
        block_dimension=2,
        block_count=3,
        temporal_eigenvalues=np.ones(degrees),
        confidence=0.975,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )

    assert whitened.residual_degrees_of_freedom == 118
    assert whitened.covariance_bound == reference


def test_ap_oracle_benchmark_crosses_below_one_after_exact_whitening() -> None:
    times = _target_times()
    design = _target_design(times)

    bound = gaussian_whitened_projected_covariance_bound(
        design,
        block_dimension=1,
        block_count=1,
        confidence=0.975,
        upper_theta_grid_size=2048,
        lower_theta_grid_size=2048,
    )

    assert bound.residual_degrees_of_freedom == 118
    assert 0.40 < bound.covariance_bound.relative_covariance_error < 0.47
    assert bound.covariance_bound.relative_covariance_error < 1.0


def test_exact_scalar_chi_square_bound_is_tighter_than_matrix_laplace_on_ap_benchmark() -> None:
    times = _target_times()
    design = _target_design(times)

    exact = gaussian_whitened_scalar_chi_square_bound(
        design,
        block_count=1,
        confidence=0.975,
    )
    matrix = gaussian_whitened_projected_covariance_bound(
        design,
        block_dimension=1,
        block_count=1,
        confidence=0.975,
        upper_theta_grid_size=2048,
        lower_theta_grid_size=2048,
    )

    assert exact.residual_degrees_of_freedom == 118
    assert np.isclose(exact.lower_variance_ratio, 0.7311633508199835)
    assert np.isclose(exact.upper_variance_ratio, 1.3142366148262574)
    assert np.isclose(exact.relative_covariance_error, 0.3142366148262574)
    assert exact.relative_covariance_error < matrix.covariance_bound.relative_covariance_error


def test_exponential_relaxation_convenience_estimator_matches_generic_whitener() -> None:
    times = _target_times()
    design = _target_design(times)
    tau = 0.78
    covariance = np.array([[1.0, -0.2], [-0.2, 0.65]])
    samples = _simulate_relaxation(times, tau, covariance, seed=20261122)
    whitening = exponential_relaxation_markov_factorization(times, tau).whitening_matrix

    generic = separable_gaussian_whitened_projected_covariance(
        samples,
        whitening,
        design,
    )
    physical_time = exponential_relaxation_whitened_projected_covariance(
        samples,
        times,
        tau,
        design,
    )

    assert np.allclose(generic, physical_time, atol=1e-12)
