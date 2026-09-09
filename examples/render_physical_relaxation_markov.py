"""Render the Proposition 53 irregular-grid Markov structure as deterministic SVG."""

from __future__ import annotations

import json
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "physical_relaxation_sampling.json"
OUTPUT = ROOT / "docs" / "physical_relaxation_markov.svg"

WIDTH = 1440
HEIGHT = 900


def _text(x: float, y: float, value: str, size: int = 18, weight: int = 400) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#162033">{value}</text>'
    )


def _rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "#d8e0ea") -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="16" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
    )


def _line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2.0) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"/>'
    )


def _circle(x: float, y: float, radius: float, fill: str) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}"/>'


def _map(value: float, low: float, high: float, start: float, end: float) -> float:
    return start + (value - low) * (end - start) / (high - low)


def render(record: dict[str, object]) -> str:
    true_tau = float(record["true_relaxation_time_seconds"])
    irregular = record["irregular_sampling"]
    markov = record["irregular_markov_factorization"]
    intervals = [float(value) for value in markov["step_intervals_seconds"]]
    correlations = [float(value) for value in markov["step_correlations"]]
    sample_count = len(irregular["sample_times_seconds"])

    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        ),
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        _text(60, 58, "Proposition 53: exact irregular-grid Markov factorization", 31, 700),
        _text(
            60,
            92,
            "The exponential physical-time kernel is dense in covariance form but local in precision form.",
            19,
        ),
        _rect(60, 116, 1320, 64, "#eaf2ff", "#b9d1f6"),
        _text(86, 156, f"Same physical relaxation time: tau = {true_tau:.3f} s", 23, 700),
        _text(760, 156, "alpha_i = exp(-Delta t_i / tau)", 20, 700),
    ]

    left_x = 60
    right_x = 745
    top_y = 205
    bottom_y = 525
    panel_w = 635
    panel_h = 285

    parts.extend(
        [
            _rect(left_x, top_y, panel_w, panel_h, "white"),
            _text(left_x + 24, top_y + 38, "A. Irregular gaps create local step correlations", 21, 700),
            _text(left_x + 24, top_y + 66, "Longer elapsed time gives a smaller alpha_i.", 16),
        ]
    )
    x0 = left_x + 70
    x1 = left_x + panel_w - 32
    y0 = top_y + 238
    y1 = top_y + 96
    parts.extend(
        [
            _line(x0, y0, x1, y0, "#9aa8ba", 1.5),
            _line(x0, y0, x0, y1, "#9aa8ba", 1.5),
            _text(x0 - 46, y1 + 6, "1.0", 13),
            _text(x0 - 46, y0 + 5, "0.5", 13),
            _text(x0 + 188, y0 + 30, "elapsed step dt (s)", 14),
        ]
    )
    points = []
    for interval, correlation in zip(intervals, correlations, strict=True):
        x = _map(interval, min(intervals), max(intervals), x0, x1)
        y = _map(correlation, 0.5, 1.0, y0, y1)
        points.append((x, y))
    points.sort()
    for first, second in pairwise(points):
        parts.append(_line(first[0], first[1], second[0], second[1], "#2563eb", 2.5))
    for x, y in points:
        parts.append(_circle(x, y, 5.5, "#2563eb"))

    parts.extend(
        [
            _rect(right_x, top_y, panel_w, panel_h, "white"),
            _text(right_x + 24, top_y + 38, "B. Exact precision matrix is tridiagonal", 21, 700),
            _text(right_x + 24, top_y + 66, "Only adjacent timestamps couple conditionally.", 16),
        ]
    )
    cell = 13.0
    grid_x = right_x + 92
    grid_y = top_y + 88
    for row in range(sample_count):
        for column in range(sample_count):
            active = abs(row - column) <= 1
            fill = "#2b6cb0" if active else "#edf2f7"
            parts.append(
                f'<rect x="{grid_x + cell * column:.1f}" y="{grid_y + cell * row:.1f}" '
                f'width="{cell - 1:.1f}" height="{cell - 1:.1f}" fill="{fill}"/>'
            )
    parts.extend(
        [
            _text(
                right_x + 300,
                top_y + 118,
                f'{int(markov["precision_nonzero_count"])} nonzero entries',
                17,
                700,
            ),
            _text(
                right_x + 300,
                top_y + 148,
                f'out of {int(markov["precision_total_entry_count"])} total entries',
                16,
            ),
            _text(right_x + 300, top_y + 187, "Dense covariance", 16, 700),
            _text(right_x + 300, top_y + 214, "Sparse conditional structure", 16, 700),
            _text(right_x + 300, top_y + 250, "No long-range precision edges appear.", 15),
        ]
    )

    parts.extend(
        [
            _rect(left_x, bottom_y, panel_w, panel_h, "white"),
            _text(left_x + 24, bottom_y + 38, "C. Innovation whitening is exact", 21, 700),
            _text(left_x + 24, bottom_y + 67, "W K_tau W^T = I and Q = W^T W", 17, 700),
        ]
    )
    metrics = [
        ("covariance products", float(markov["maximum_covariance_product_error"])),
        ("precision inverse", float(markov["precision_inverse_max_abs_error"])),
        ("whitening identity", float(markov["whitening_identity_max_abs_error"])),
        ("precision Gram", float(markov["precision_gram_max_abs_error"])),
    ]
    for index, (label, value) in enumerate(metrics):
        y = bottom_y + 108 + 40 * index
        parts.append(_text(left_x + 40, y, label, 16))
        parts.append(_text(left_x + 300, y, f"{value:.2e}", 17, 700))
        parts.append(_circle(left_x + 552, y - 6, 6, "#0f9d78"))
    parts.append(
        _text(
            left_x + 40,
            bottom_y + 265,
            "All identities hold at floating-point precision.",
            16,
            700,
        )
    )

    parts.extend(
        [
            _rect(right_x, bottom_y, panel_w, panel_h, "white"),
            _text(right_x + 24, bottom_y + 38, "D. Local innovations factor the determinant", 21, 700),
            _text(right_x + 24, bottom_y + 75, "det(K_tau) = product_i (1 - alpha_i^2)", 18, 700),
            _text(right_x + 24, bottom_y + 116, "log det from innovations", 16),
            _text(
                right_x + 322,
                bottom_y + 116,
                f'{float(markov["covariance_log_determinant_from_innovations"]):.12f}',
                16,
                700,
            ),
            _text(right_x + 24, bottom_y + 154, "dense log det", 16),
            _text(
                right_x + 322,
                bottom_y + 154,
                f'{float(markov["covariance_log_determinant_dense"]):.12f}',
                16,
                700,
            ),
            _text(right_x + 24, bottom_y + 192, "absolute difference", 16),
            _text(
                right_x + 322,
                bottom_y + 192,
                f'{float(markov["log_determinant_absolute_error"]):.2e}',
                16,
                700,
            ),
            _text(
                right_x + 24,
                bottom_y + 242,
                "Likelihood geometry can be evaluated from local steps.",
                15,
                700,
            ),
        ]
    )

    parts.extend(
        [
            _rect(60, 835, 1320, 42, "#eef7f3", "#b8ddcf"),
            _text(
                84,
                862,
                "Physical reading: irregular sampling changes local transition coefficients, not the underlying tau.",
                17,
                700,
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(record), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
