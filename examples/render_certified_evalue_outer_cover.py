"""Render Experiment AL from its committed machine-readable result."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "docs" / "certified_evalue_outer_cover.json"
OUTPUT_PATH = REPO_ROOT / "docs" / "certified_evalue_outer_cover.svg"

WIDTH = 1200
HEIGHT = 760


def text(x: float, y: float, value: str, size: int = 18, weight: int = 400) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#172033">'
        f"{escape(value)}</text>"
    )


def rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    stroke: str = "none",
    radius: float = 12,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}"/>'
    )


def line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{width}"/>'
    )


def range_x(value: float) -> float:
    return 78 + (value - 0.30) / 0.40 * 470


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">',
        rect(0, 0, WIDTH, HEIGHT, "#f7f9fc", radius=0),
        text(54, 55, "Experiment AL | From temporal calibration to target covariance", 27, 700),
        text(
            54,
            84,
            "Proposition 52 certifies a continuum temporal uncertainty set before target use.",
            16,
        ),
    ]

    parts.extend(
        [
            rect(40, 115, 535, 265, "#ffffff", "#d9e0ea"),
            text(64, 150, "1. What temporal memory remains compatible?", 19, 700),
            text(64, 178, "Horizontal axis: AR(1) persistence parameter phi", 14),
            line(78, 325, 548, 325, "#9aa6b6", 2),
        ]
    )
    for value in (0.30, 0.40, 0.50, 0.60, 0.70):
        x = range_x(value)
        parts.append(line(x, 318, x, 332, "#9aa6b6", 1))
        parts.append(text(x - 15, 353, f"{value:.2f}", 12))

    ranges = [
        (
            "Declared family",
            data["declared_autocorrelation_lower_bound"],
            data["declared_autocorrelation_upper_bound"],
            215,
            "#c9d4e5",
        ),
        (
            "P52 certified outer cover",
            data["outer_cover_autocorrelation_lower_bound"],
            data["outer_cover_autocorrelation_upper_bound"],
            255,
            "#6b8cc4",
        ),
        (
            "P51 plotted accepted span",
            data["pointwise_accepted_autocorrelation_lower_bound"],
            data["pointwise_accepted_autocorrelation_upper_bound"],
            295,
            "#2f5f9d",
        ),
    ]
    for label, lower, upper, y, fill in ranges:
        parts.append(text(64, y + 5, label, 13, 600))
        x1 = range_x(lower)
        x2 = range_x(upper)
        parts.append(rect(x1, y - 12, max(4, x2 - x1), 17, fill, radius=8))

    parts.append(
        text(
            64,
            374,
            "The P51 grid is a visualization. The P52 retained cells certify the continuum.",
            12,
        )
    )

    parts.extend(
        [
            rect(600, 115, 560, 265, "#ffffff", "#d9e0ea"),
            text(624, 150, "2. Which parameter cells can be ruled out?", 19, 700),
        ]
    )
    total = data["outer_cover_total_cells"]
    retained = data["outer_cover_retained_cells"]
    excluded = data["outer_cover_excluded_cells"]
    retained_width = 470 * retained / total
    excluded_width = 470 * excluded / total
    parts.extend(
        [
            text(624, 190, f"Fixed cells in declared box: {total:,}", 15),
            rect(624, 220, retained_width, 34, "#6b8cc4", radius=6),
            rect(624 + retained_width, 220, excluded_width, 34, "#d5dbe5", radius=6),
            text(624, 280, f"Retained: {retained:,}  ({retained / total:.1%})", 14, 600),
            text(885, 280, f"Certified excluded: {excluded:,}", 14, 600),
            text(
                624,
                315,
                f"P51 displayed accepted grid points: {data['pointwise_accepted_grid_points']:,}",
                13,
            ),
            text(
                624,
                346,
                "A cell is discarded only when every point in it is proved outside P51.",
                12,
            ),
        ]
    )

    parts.extend(
        [
            rect(40, 405, 535, 300, "#ffffff", "#d9e0ea"),
            text(64, 440, "3. Is the independent target covariance usable?", 19, 700),
            text(64, 466, "Relative operator error scale", 14),
        ]
    )
    bar_left = 92
    bar_width = 430

    def error_x(value: float) -> float:
        return bar_left + min(max(value, 0.0), 1.0) * bar_width

    parts.append(line(bar_left, 620, bar_left + bar_width, 620, "#9aa6b6", 2))
    for value in (0.0, 0.25, 0.50, 0.75, 1.0):
        x = error_x(value)
        parts.append(line(x, 614, x, 627, "#9aa6b6", 1))
        parts.append(text(x - 10, 648, f"{value:.2f}", 12))

    errors = [
        ("Median observed", data["empirical_median_relative_error"], 505, "#c3d3ea"),
        ("95th percentile", data["empirical_q95_relative_error"], 538, "#91add4"),
        ("Maximum observed", data["empirical_max_relative_error"], 571, "#5c83b7"),
        ("Theorem radius", data["covariance_relative_error"], 604, "#244f87"),
    ]
    for label, value, y, fill in errors:
        parts.append(text(64, y + 4, label, 12, 600))
        parts.append(rect(bar_left, y - 11, error_x(value) - bar_left, 15, fill, radius=5))
        parts.append(text(error_x(value) + 7, y + 3, f"{value:.3f}", 11, 600))

    parts.append(
        text(
            64,
            682,
            "The value 1 is a perturbation threshold, not a physical phase transition.",
            12,
        )
    )

    parts.extend(
        [
            rect(600, 405, 560, 300, "#ffffff", "#d9e0ea"),
            text(624, 440, "4. Physical inference chain", 19, 700),
            text(624, 469, "Calibration record", 14, 700),
            text(624, 490, "48 time samples x 256 independent channels", 12),
            text(624, 525, "Certified temporal family", 14, 700),
            text(624, 546, "All P51-compatible parameters are inside retained P52 cells", 12),
            text(624, 581, "Independent target record", 14, 700),
            text(624, 602, "120 samples, affine nuisance drift projected away", 12),
            text(624, 637, "Target covariance certificate", 14, 700),
            text(
                624,
                658,
                f"Combined confidence >= {100 * data['combined_confidence_lower_bound']:.3f}%",
                12,
            ),
            text(
                624,
                681,
                f"Relative covariance radius = {data['covariance_relative_error']:.6f} < 1",
                12,
                700,
            ),
        ]
    )

    parts.append(
        text(
            54,
            737,
            "The theorem certifies measurement uncertainty under the stated model. "
            "It does not identify consciousness.",
            13,
            600,
        )
    )
    parts.append("</svg>")
    OUTPUT_PATH.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
