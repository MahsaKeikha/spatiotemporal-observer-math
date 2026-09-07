import numpy as np

from observer_math import (
    minimum_sample_split_certification_size,
    sample_split_screened_recovery_bound,
)


def _bound(**overrides):
    arguments = {
        "screening_sample_count": 2_000,
        "certification_sample_count": 100_000,
        "retained_block_count": 25,
        "block_dimension": 20,
        "maximum_block_eigenvalue": 2.0,
        "maximum_admissible_covariance_error": 0.12,
        "screening_confidence": 0.975,
        "certification_confidence": 0.975,
        "independent_splits": True,
    }
    arguments.update(overrides)
    return sample_split_screened_recovery_bound(**arguments)


def test_sample_split_bound_reports_stagewise_and_combined_confidence():
    result = _bound()
    expected_deviation = (
        np.sqrt(20) + np.sqrt(2.0 * np.log(2.0 * 25 / 0.025))
    ) / np.sqrt(100_000 - 1)
    expected_error = 2.0 * (2.0 * expected_deviation + expected_deviation**2)

    assert np.isclose(result.overall_confidence, 0.975**2)
    assert np.isclose(result.covariance_spectral_error, expected_error)
    assert result.certification_radius_valid
    assert result.guarantees_population_path


def test_same_data_refuses_sample_split_guarantee():
    result = _bound(independent_splits=False)

    assert result.certification_radius_valid
    assert not result.independent_splits
    assert not result.guarantees_population_path


def test_screening_reduction_and_more_samples_tighten_certification_radius():
    screened = _bound(retained_block_count=25)
    unscreened = _bound(retained_block_count=10_000)
    larger_sample = _bound(certification_sample_count=200_000)

    assert screened.covariance_spectral_error < unscreened.covariance_spectral_error
    assert larger_sample.covariance_spectral_error < screened.covariance_spectral_error


def test_minimum_sample_split_size_is_first_certified_integer():
    minimum = minimum_sample_split_certification_size(
        screening_sample_count=2_000,
        retained_block_count=25,
        block_dimension=20,
        maximum_block_eigenvalue=2.0,
        maximum_admissible_covariance_error=0.12,
        maximum_sample_count=1_000_000,
    )

    assert minimum is not None
    assert _bound(certification_sample_count=minimum).guarantees_population_path
    assert not _bound(
        certification_sample_count=minimum - 1
    ).guarantees_population_path
