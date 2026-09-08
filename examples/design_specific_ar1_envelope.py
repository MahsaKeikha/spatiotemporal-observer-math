"""Experiment AF: design-specific versus rank-only AR(1) interval envelopes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.design_interval import (
    gaussian_estimated_ar1_design_projected_covariance_bound,
)
from observer_math.estimated_nuisance import (
    gaussian_estimated_ar1_projected_covariance_bound,
)
from observer_math.recovery import GaussianAR1AutocorrelationInterval


def cosine_design(sample_count: int, rank: int) -> np.ndarray:
    index = np.arange(sample_count, dtype=float)
    columns = [np.ones(sample_count)]
    for frequency in range(1, rank):
        columns.append(np.cos(np.pi * frequency * (index + 0.5) / sample_count))
    return np.column_stack(columns)


def fixed_interval(lower: float, upper: float) -> GaussianAR1AutocorrelationInterval:
    return GaussianAR1AutocorrelationInterval(
        sample_count=1,
        channel_count=1,
        confidence=0.975,
        declared_upper_bound=upper,
        estimate=0.5 * (lower + upper),
        error_radius=0.5 * (upper - lower),
        lower_bound=lower,
        upper_bound=upper,
        interval_intersects_declared_model=True,
    )


def run(sample_count: int = 300, grid_size: int = 17):
    lower = 0.75
    upper = 0.85
    interval = fixed_interval(lower, upper)
    ranks = (2, 8, 16, 24, 25)
    records = []

    for rank in ranks:
        design = cosine_design(sample_count, rank)
        design_bound = gaussian_estimated_ar1_design_projected_covariance_bound(
            4,
            1,
            design,
            interval,
            covariance_confidence=0.975,
            grid_size=grid_size,
        )
        envelope = design_bound.design_envelope
        try:
            rank_only = gaussian_estimated_ar1_projected_covariance_bound(
                4,
                1,
                sample_count,
                rank,
                interval,
                covariance_confidence=0.975,
            )
            rank_only_radius = rank_only.covariance_relative_error
            rank_only_oracle_radius = rank_only.oracle_normalized_covariance_error
        except ValueError:
            rank_only_radius = None
            rank_only_oracle_radius = None

        records.append(
            {
                "nuisance_rank": rank,
                "design_degrees_lower": envelope.projected_degrees_of_freedom_lower_bound,
                "design_degrees_upper": envelope.projected_degrees_of_freedom_upper_bound,
                "rank_only_degrees_lower": envelope.rank_only_degrees_of_freedom_lower_bound,
                "design_projected_frobenius_bound": envelope.projected_frobenius_norm_bound,
                "global_frobenius_bound": envelope.global_frobenius_norm_bound,
                "design_projected_spectral_bound": envelope.projected_spectral_norm_bound,
                "global_spectral_bound": envelope.global_spectral_norm_bound,
                "design_oracle_radius": design_bound.oracle_normalized_covariance_error,
                "design_covariance_radius": design_bound.covariance_relative_error,
                "rank_only_oracle_radius": rank_only_oracle_radius,
                "rank_only_covariance_radius": rank_only_radius,
            }
        )

    return {
        "experiment": "AF",
        "sample_count": sample_count,
        "autocorrelation_interval": [lower, upper],
        "nuisance_basis": "predeclared low-frequency cosine basis",
        "block_dimension": 4,
        "block_count": 1,
        "covariance_confidence": 0.975,
        "grid_size": grid_size,
        "continuum_method": "uniform grid plus analytic Frobenius/spectral Lipschitz remainder",
        "records": records,
    }


def plot(results, output_path: Path):
    records = results["records"]
    rank = np.array([row["nuisance_rank"] for row in records])
    design_d = np.array([row["design_degrees_lower"] for row in records])
    rank_d = np.array([row["rank_only_degrees_lower"] for row in records])
    design_f = np.array([row["design_projected_frobenius_bound"] for row in records])
    global_f = np.array([row["global_frobenius_bound"] for row in records])
    design_s = np.array([row["design_projected_spectral_bound"] for row in records])
    global_s = np.array([row["global_spectral_bound"] for row in records])
    design_radius = np.array([row["design_covariance_radius"] for row in records])
    rank_radius = np.array(
        [
            np.nan if row["rank_only_covariance_radius"] is None else row["rank_only_covariance_radius"]
            for row in records
        ]
    )

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))

    ax = axes[0, 0]
    ax.plot(rank, design_d, marker="o", label="design-specific lower normalization")
    ax.plot(rank, rank_d, marker="o", label="rank-only lower normalization")
    ax.axhline(0.0, linestyle="--")
    ax.set_xlabel("nuisance rank q")
    ax.set_ylabel("certified lower normalization")
    ax.set_title("Actual nuisance geometry prevents false vacuity")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(rank, design_f, marker="o", label="projected Frobenius bound")
    ax.plot(rank, global_f, linestyle="--", label="global Frobenius bound")
    ax.set_xlabel("nuisance rank q")
    ax.set_ylabel("Frobenius norm bound")
    ax.set_title("Projected variance scale shrinks with declared geometry")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 0]
    ax.plot(rank, design_s, marker="o", label="projected spectral bound")
    ax.plot(rank, global_s, linestyle="--", label="global spectral bound")
    ax.set_xlabel("nuisance rank q")
    ax.set_ylabel("spectral norm bound")
    ax.set_title("Projected operator scale is also geometry-aware")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 1]
    ax.plot(rank, design_radius, marker="o", label="Proposition 46")
    ax.plot(rank, rank_radius, marker="o", label="Proposition 45")
    ax.set_yscale("log")
    ax.set_xlabel("nuisance rank q")
    ax.set_ylabel("relative covariance radius")
    ax.set_title("Rank-only radius diverges before the covariance does")
    ax.grid(True, alpha=0.25)
    ax.legend()

    fig.suptitle(
        "Experiment AF — design-specific AR(1) interval geometry",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-count", type=int, default=300)
    parser.add_argument("--grid-size", type=int, default=17)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(sample_count=args.sample_count, grid_size=args.grid_size)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "design_specific_ar1_envelope.json"
    figure_path = args.output_dir / "design_specific_ar1_envelope.svg"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
