"""Render Experiment AK from its committed machine-readable result."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


def render(results, output_path):
    records = results["records"]
    final_record = records[-1]
    grid_view = final_record["proposition_51_grid_view"]
    rectangle = final_record["proposition_50_rectangle"]
    points = np.asarray(grid_view["accepted_points"], dtype=float)
    channels = np.asarray([record["channel_count"] for record in records])
    fractions = np.asarray(
        [record["proposition_51_grid_view"]["accepted_fraction"] for record in records]
    )
    true_log_evalues = np.asarray(
        [
            record["proposition_51_grid_view"]["true_parameter_log_evalue"]
            for record in records
        ]
    )

    fig = plt.figure(figsize=(12, 8))
    grid = fig.add_gridspec(2, 2, width_ratios=(1.25, 1.0))
    geometry = fig.add_subplot(grid[:, 0])
    fraction_axis = fig.add_subplot(grid[0, 1])
    evalue_axis = fig.add_subplot(grid[1, 1])

    geometry.add_patch(
        Rectangle(
            (
                rectangle["autocorrelation_lower"],
                rectangle["white_noise_fraction_lower"],
            ),
            rectangle["autocorrelation_upper"] - rectangle["autocorrelation_lower"],
            rectangle["white_noise_fraction_upper"]
            - rectangle["white_noise_fraction_lower"],
            alpha=0.25,
            label="Proposition 50 rectangle",
        )
    )
    geometry.scatter(
        points[:, 0],
        points[:, 1],
        s=24,
        label="Proposition 51 pointwise grid view",
    )
    geometry.scatter(
        [results["true_autocorrelation"]],
        [results["true_white_noise_fraction"]],
        s=90,
        marker="*",
        label="controlled truth",
    )
    geometry.set_xlim(results["declared_autocorrelation_interval"])
    geometry.set_ylim(results["declared_white_noise_fraction_interval"])
    geometry.set_xlabel("AR(1) coefficient phi")
    geometry.set_ylabel("white-noise fraction eta")
    geometry.set_title("256-channel parameter geometry")
    geometry.grid(alpha=0.25)
    geometry.legend(loc="upper left")

    fraction_axis.plot(channels, 100.0 * fractions, marker="o")
    fraction_axis.set_xlabel("independent calibration channels")
    fraction_axis.set_ylabel("accepted grid points (%)")
    fraction_axis.set_title("Pointwise grid view contracts")
    fraction_axis.grid(alpha=0.25)

    threshold = grid_view["log_evalue_threshold"]
    evalue_axis.plot(channels, true_log_evalues, marker="o", label="true parameter")
    evalue_axis.axhline(threshold, linestyle="--", label="rejection threshold")
    evalue_axis.set_xlabel("independent calibration channels")
    evalue_axis.set_ylabel("log e-value")
    evalue_axis.set_title("True parameter remains below threshold")
    evalue_axis.grid(alpha=0.25)
    evalue_axis.legend()

    fig.suptitle(
        "Experiment AK | Full-likelihood e-value geometry\n"
        "Grid points visualize the continuum theorem; they are not its probability proof",
        fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(output_path, format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    root = Path(__file__).resolve().parents[1]
    json_path = root / "docs" / "evalue_temporal_confidence_set.json"
    svg_path = root / "docs" / "evalue_temporal_confidence_set.svg"
    results = json.loads(json_path.read_text())
    render(results, svg_path)
    print(svg_path)


if __name__ == "__main__":
    main()
