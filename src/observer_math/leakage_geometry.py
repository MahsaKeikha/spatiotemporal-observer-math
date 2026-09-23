"""Engineering geometry for environmental-leakage measurement.

Proposition 60 formalizes what can and cannot reduce the full leakage block.
The module separates exact measurement geometry from model-dependent screening.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LeakageMeasurementGeometry:
    node_count: int
    subset_size: int
    environment_size: int
    exact_block_dimension: int
    screened_environment_size: int | None
    screened_block_dimension: int | None
    exact_reduction_justified: bool


def leakage_measurement_geometry(
    node_count: int,
    subset_size: int,
    *,
    screened_environment_size: int | None = None,
    conditional_screening_certified: bool = False,
) -> LeakageMeasurementGeometry:
    """Describe exact and screened covariance dimensions for leakage.

    The exact leakage I(X_future^S; X_present^environment | X_present^S)
    uses future S, present S, and the complete present environment, hence n+s
    variables. A reduced environment is recorded as exact only when an external
    conditional-screening certificate justifies deleting the omitted variables.
    This function does not infer such a certificate from the data.
    """
    if node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    environment_size = node_count - subset_size
    if screened_environment_size is not None:
        if not 0 <= screened_environment_size <= environment_size:
            raise ValueError("screened_environment_size must lie in [0, n-s]")
        screened_dimension = 2 * subset_size + screened_environment_size
    else:
        screened_dimension = None
    return LeakageMeasurementGeometry(
        node_count=node_count,
        subset_size=subset_size,
        environment_size=environment_size,
        exact_block_dimension=node_count + subset_size,
        screened_environment_size=screened_environment_size,
        screened_block_dimension=screened_dimension,
        exact_reduction_justified=bool(
            screened_environment_size is not None and conditional_screening_certified
        ),
    )
