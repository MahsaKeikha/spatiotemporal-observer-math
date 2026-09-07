"""Account for independent screening and certification samples."""

from observer_math import (
    minimum_sample_split_certification_size,
    sample_split_screened_recovery_bound,
)


def main() -> None:
    screening_sample_count = 2_000
    retained_block_count = 25
    unscreened_block_count = 10_000
    block_dimension = 20
    maximum_eigenvalue = 2.0
    admissible_error = 0.12
    screened_minimum = minimum_sample_split_certification_size(
        screening_sample_count,
        retained_block_count,
        block_dimension,
        maximum_eigenvalue,
        admissible_error,
        screening_confidence=0.975,
        certification_confidence=0.975,
        maximum_sample_count=10_000_000,
    )
    unscreened_minimum = minimum_sample_split_certification_size(
        screening_sample_count,
        unscreened_block_count,
        block_dimension,
        maximum_eigenvalue,
        admissible_error,
        screening_confidence=0.975,
        certification_confidence=0.975,
        maximum_sample_count=10_000_000,
    )
    if screened_minimum is None or unscreened_minimum is None:
        raise RuntimeError("the configured search range must contain both thresholds")
    result = sample_split_screened_recovery_bound(
        screening_sample_count,
        screened_minimum,
        retained_block_count,
        block_dimension,
        maximum_eigenvalue,
        admissible_error,
        screening_confidence=0.975,
        certification_confidence=0.975,
        independent_splits=True,
    )
    reused = sample_split_screened_recovery_bound(
        screening_sample_count,
        screened_minimum,
        retained_block_count,
        block_dimension,
        maximum_eigenvalue,
        admissible_error,
        screening_confidence=0.975,
        certification_confidence=0.975,
        independent_splits=False,
    )

    print(f"Screening sample count: {screening_sample_count:,}")
    print(f"Retained covariance blocks: {retained_block_count:,}")
    print(f"Unscreened covariance blocks: {unscreened_block_count:,}")
    print(f"Minimum screened certification sample: {screened_minimum:,}")
    print(f"Minimum unscreened certification sample: {unscreened_minimum:,}")
    print(f"Covariance radius at threshold: {result.covariance_spectral_error:.6f}")
    print(f"Maximum admissible radius: {admissible_error:.6f}")
    print(f"Screening confidence: {result.screening_confidence:.6f}")
    print(f"Certification confidence: {result.certification_confidence:.6f}")
    print(f"Combined confidence: {result.overall_confidence:.6f}")
    print(f"Independent-split guarantee: {result.guarantees_population_path}")
    print(f"Same-data guarantee: {reused.guarantees_population_path}")


if __name__ == "__main__":
    main()
