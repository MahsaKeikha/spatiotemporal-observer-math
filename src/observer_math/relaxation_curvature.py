"""Second-order certificates for irregular-time relaxation calibration.

Proposition 55 tightens the deterministic outer cover of the Proposition 53B
continuum e-value confidence set. At each calibration cell center it uses the
exact observed-data derivative of log e_tau and a rigorous cell-local bound on
the second derivative. Taylor's theorem then gives a quadratic lower enclosure
for log e_tau throughout the cell.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .irregular_relaxation_evalue import (
    GaussianIrregularRelaxationEValueModel,
    gaussian_irregular_relaxation_log_evalue,
)


@dataclass(frozen=True)
class GaussianIrregularRelaxationQuadraticOuterCover:
    """Certified cell cover using exact center slopes and quadratic remainders."""

    cell_edges: np.ndarray
    cell_centers: np.ndarray
    cell_radius: float
    log_evalues_at_centers: np.ndarray
    log_evalue_derivatives_at_centers: np.ndarray
    cell_second_derivative_bounds: np.ndarray
    retained_mask: np.ndarray
    retained_cell_count: int
    excluded_cell_count: int
    total_cell_count: int
    retained_relaxation_time_lower_bound: float
    retained_relaxation_time_upper_bound: float


def _validated_subinterval(
    model: GaussianIrregularRelaxationEValueModel,
    lower: float,
    upper: float,
) -> tuple[float, float]:
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    lo = float(lower)
    hi = float(upper)
    if not (
        model.declared_relaxation_time_lower_bound
        <= lo
        <= hi
        <= model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("requested interval lies outside the declared relaxation model")
    return lo, hi


def _validated_cell_count(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError("cell_count must be an integer")
    if value < 2:
        raise ValueError("cell_count must be at least two")
    return int(value)


def _alpha_derivative(distance: float, relaxation_time: float) -> float:
    tau = float(relaxation_time)
    return float(distance * np.exp(-distance / tau) / tau**2)


def _alpha_derivative_supremum(distance: float, lower: float, upper: float) -> float:
    candidate = float(np.clip(0.5 * distance, lower, upper))
    return _alpha_derivative(distance, candidate)


def _alpha_second_derivative_supremum(distance: float, lower: float, upper: float) -> float:
    if distance == 0.0:
        return 0.0
    x_lower = distance / upper
    x_upper = distance / lower
    candidates = [x_lower, x_upper]
    for critical in (3.0 - np.sqrt(3.0), 3.0 + np.sqrt(3.0)):
        if x_lower <= critical <= x_upper:
            candidates.append(float(critical))
    values = [
        np.exp(-x) * x**3 * abs(x - 2.0) / distance**2
        for x in candidates
    ]
    return float(max(values))


def _transition_alpha_bounds(distance: float, lower: float, upper: float) -> tuple[float, float]:
    alpha_lower = float(np.exp(-distance / lower))
    alpha_upper = float(np.exp(-distance / upper))
    return alpha_lower, alpha_upper


def _log_likelihood_alpha_derivative(
    channel_count: int,
    sum_xx: float,
    sum_xy: float,
    sum_yy: float,
    alpha: float,
) -> float:
    variance = 1.0 - alpha * alpha
    residual = sum_yy - 2.0 * alpha * sum_xy + alpha * alpha * sum_xx
    numerator = sum_xy + alpha * (channel_count - sum_xx)
    return float(numerator / variance - alpha * residual / variance**2)


def gaussian_irregular_relaxation_log_evalue_derivative(
    model: GaussianIrregularRelaxationEValueModel,
    relaxation_time: float,
) -> float:
    """Return the exact observed-data derivative d log e_tau / d tau."""
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    tau = float(relaxation_time)
    if not (
        model.declared_relaxation_time_lower_bound
        <= tau
        <= model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("relaxation_time lies outside the declared model")

    derivative = 0.0
    for index, distance in enumerate(np.diff(model.sample_times)):
        alpha = float(np.exp(-distance / tau))
        likelihood_alpha_derivative = _log_likelihood_alpha_derivative(
            model.channel_count,
            float(model.transition_sum_xx[index]),
            float(model.transition_sum_xy[index]),
            float(model.transition_sum_yy[index]),
            alpha,
        )
        derivative -= likelihood_alpha_derivative * _alpha_derivative(float(distance), tau)
    return float(derivative)


def _log_likelihood_alpha_derivative_bound(
    channel_count: int,
    sum_xx: float,
    sum_xy: float,
    sum_yy: float,
    alpha_upper: float,
) -> float:
    variance_min = 1.0 - alpha_upper * alpha_upper
    residual_upper = (
        sum_yy
        + 2.0 * alpha_upper * abs(sum_xy)
        + alpha_upper * alpha_upper * sum_xx
    )
    numerator_upper = abs(sum_xy) + alpha_upper * abs(channel_count - sum_xx)
    return float(
        numerator_upper / variance_min
        + alpha_upper * residual_upper / variance_min**2
    )


def _log_likelihood_alpha_second_derivative_bound(
    channel_count: int,
    sum_xx: float,
    sum_xy: float,
    sum_yy: float,
    alpha_upper: float,
) -> float:
    variance_min = 1.0 - alpha_upper * alpha_upper
    c_minus_x = float(channel_count - sum_xx)
    numerator_upper = abs(sum_xy) + alpha_upper * abs(c_minus_x)
    residual_upper = (
        sum_yy
        + 2.0 * alpha_upper * abs(sum_xy)
        + alpha_upper * alpha_upper * sum_xx
    )
    residual_derivative_upper = 2.0 * abs(sum_xy) + 2.0 * alpha_upper * sum_xx

    return float(
        abs(c_minus_x) / variance_min
        + 2.0 * alpha_upper * numerator_upper / variance_min**2
        + (residual_upper + alpha_upper * residual_derivative_upper) / variance_min**2
        + 4.0 * alpha_upper**2 * residual_upper / variance_min**3
    )


def gaussian_irregular_relaxation_log_evalue_second_derivative_bound(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    lower_relaxation_time: float,
    upper_relaxation_time: float,
) -> float:
    """Bound |d^2 log e_tau / d tau^2| on one declared subinterval.

    Since the mixture numerator density is constant as a function of candidate
    tau after the calibration record is observed, log e_tau differs from the
    negative log likelihood only by a constant. The bound therefore follows by
    the chain rule through each local transition coefficient alpha_i(tau).
    """
    lower, upper = _validated_subinterval(
        model,
        lower_relaxation_time,
        upper_relaxation_time,
    )

    total = 0.0
    for index, distance_value in enumerate(np.diff(model.sample_times)):
        distance = float(distance_value)
        _, alpha_upper = _transition_alpha_bounds(distance, lower, upper)
        sum_xx = float(model.transition_sum_xx[index])
        sum_xy = float(model.transition_sum_xy[index])
        sum_yy = float(model.transition_sum_yy[index])

        first_alpha_bound = _log_likelihood_alpha_derivative_bound(
            model.channel_count,
            sum_xx,
            sum_xy,
            sum_yy,
            alpha_upper,
        )
        second_alpha_bound = _log_likelihood_alpha_second_derivative_bound(
            model.channel_count,
            sum_xx,
            sum_xy,
            sum_yy,
            alpha_upper,
        )
        alpha_first = _alpha_derivative_supremum(distance, lower, upper)
        alpha_second = _alpha_second_derivative_supremum(distance, lower, upper)
        total += second_alpha_bound * alpha_first**2 + first_alpha_bound * alpha_second
    return float(total)


def gaussian_irregular_relaxation_quadratic_outer_cover(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    cell_count: int = 160,
) -> GaussianIrregularRelaxationQuadraticOuterCover:
    """Certify an outer cover with a cell-local second-order Taylor enclosure."""
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    if model.declared_relaxation_time_lower_bound == model.declared_relaxation_time_upper_bound:
        raise ValueError("quadratic cells require a nondegenerate relaxation-time interval")
    count = _validated_cell_count(cell_count)
    edges = np.linspace(
        model.declared_relaxation_time_lower_bound,
        model.declared_relaxation_time_upper_bound,
        count + 1,
    )
    centers = 0.5 * (edges[:-1] + edges[1:])
    radius = float(0.5 * (edges[1] - edges[0]))

    log_evalues = np.asarray(
        [gaussian_irregular_relaxation_log_evalue(model, float(tau)) for tau in centers],
        dtype=float,
    )
    derivatives = np.asarray(
        [gaussian_irregular_relaxation_log_evalue_derivative(model, float(tau)) for tau in centers],
        dtype=float,
    )
    second_bounds = np.asarray(
        [
            gaussian_irregular_relaxation_log_evalue_second_derivative_bound(
                model,
                lower_relaxation_time=float(edges[index]),
                upper_relaxation_time=float(edges[index + 1]),
            )
            for index in range(count)
        ],
        dtype=float,
    )

    lower_enclosure = (
        log_evalues - np.abs(derivatives) * radius - 0.5 * second_bounds * radius**2
    )
    retained = lower_enclosure < model.log_evalue_threshold
    retained_count = int(np.sum(retained))
    if retained_count:
        indices = np.flatnonzero(retained)
        retained_lower = float(edges[indices[0]])
        retained_upper = float(edges[indices[-1] + 1])
    else:
        retained_lower = np.nan
        retained_upper = np.nan

    return GaussianIrregularRelaxationQuadraticOuterCover(
        cell_edges=edges,
        cell_centers=centers,
        cell_radius=radius,
        log_evalues_at_centers=log_evalues,
        log_evalue_derivatives_at_centers=derivatives,
        cell_second_derivative_bounds=second_bounds,
        retained_mask=retained,
        retained_cell_count=retained_count,
        excluded_cell_count=int(count - retained_count),
        total_cell_count=count,
        retained_relaxation_time_lower_bound=retained_lower,
        retained_relaxation_time_upper_bound=retained_upper,
    )
