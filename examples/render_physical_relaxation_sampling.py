"""Render the committed Experiment AM record as a deterministic SVG."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "physical_relaxation_sampling.json"
OUTPUT = ROOT / "docs" / "physical_relaxation_sampling.svg"

WIDTH = 1440
HEIGHT = 940


def _text(x: float, y: float, value: str, size: int = 20, weight: int = 400) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#162033">{value}</text>'
    )


def _rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "#d8e0ea") -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="18" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    )


def _line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2.0) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"/>'
    )


def _circle(x: float, y: float, radius: float, fill: str, stroke: str = "white") -> str:
    return (
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2"/>'
    )


def _polyline(points: list[tuple[float, float]], stroke: str, width: float = 3.0) -> str:
    value = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polyline points="{value}" fill="none" stroke="{stroke}" '
        f'stroke-width="{width:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _map(value: float, low: float, high: float, start: float, end: float) -> float:
    return start + (value - low) * (end - start) / (high - low)


def render(record: dict[str, object]) -> str:
    uniform = record["uniform_sampling"]
    cover = record["relaxation_time_cover"]
    irregular = record["irregular_sampling"]
    true_tau = float(record["true_relaxation_time_seconds"])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        _text(60, 66, "Experiment AM: one physical relaxation time across sampling schemes", 32, 700),
        _text(
            60,
            102,
            "Proposition 53 makes tau the physical parameter and treats phi as sampling dependent.",
            19,
            400,
        ),
        _rect(60, 126, 1320, 66, "#eaf2ff", "#b9d1f6"),
        _text(88, 168, f"Physical invariant: tau = {true_tau:.3f} s", 25, 700),
        _text(
            510,
            168,
            "Different sample clocks change phi, not the underlying relaxation time.",
            19,
            400,
        ),
    ]

    panel_w = 635
    panel_h = 300
    left_x = 60
    right_x = 745
    top_y = 220
    bottom_y = 545

    parts.extend(
        [
            _rect(left_x, top_y, panel_w, panel_h, "white"),
            _text(
                left_x + 24,
                top_y + 38,
                "A. Sampling rate changes the discrete correlation",
                22,
                700,
            ),
            _text(left_x + 24, top_y + 68, "phi = exp(-dt/tau)", 17, 400),
        ]
    )

    plot_x0 = left_x + 72
    plot_x1 = left_x + panel_w - 34
    plot_y0 = top_y + 248
    plot_y1 = top_y + 92
    parts.extend(
        [
            _line(plot_x0, plot_y0, plot_x1, plot_y0, "#9aa8ba", 1.5),
            _line(plot_x0, plot_y0, plot_x0, plot_y1, "#9aa8ba", 1.5),
            _text(plot_x0 - 50, plot_y1 + 8, "1.0", 14),
            _text(plot_x0 - 50, plot_y0 + 5, "0.5", 14),
            _text(plot_x0 + 190, plot_y0 + 35, "sampling rate (Hz)", 15),
        ]
    )
    rate_points = []
    for row in reversed(uniform):
        rate = float(row["sample_rate_hz"])
        phi = float(row["phi"])
        x = _map(rate, 2.5, 40.0, plot_x0, plot_x1)
        y = _map(phi, 0.5, 1.0, plot_y0, plot_y1)
        rate_points.append((x, y))
        parts.append(_circle(x, y, 7, "#2563eb"))
        parts.append(_text(x - 18, plot_y0 + 20, f"{rate:g}", 13))
    parts.append(_polyline(rate_points, "#2563eb", 3.0))

    parts.extend(
        [
            _rect(right_x, top_y, panel_w, panel_h, "white"),
            _text(
                right_x + 24,
                top_y + 38,
                "B. Every sampling rate recovers the same tau",
                22,
                700,
            ),
            _text(right_x + 24, top_y + 68, "tau = -dt / log(phi)", 17, 400),
            _text(right_x + 32, top_y + 105, "rate", 15, 700),
            _text(right_x + 176, top_y + 105, "phi", 15, 700),
            _text(right_x + 350, top_y + 105, "recovered tau", 15, 700),
        ]
    )
    for index, row in enumerate(uniform):
        y = top_y + 139 + 31 * index
        parts.append(
            _text(right_x + 32, y, f'{float(row["sample_rate_hz"]):5.1f} Hz', 15)
        )
        parts.append(_text(right_x + 176, y, f'{float(row["phi"]):.6f}', 15))
        parts.append(
            _text(
                right_x + 350,
                y,
                f'{float(row["recovered_tau_seconds"]):.6f} s',
                15,
                700,
            )
        )
        parts.append(_circle(right_x + 554, y - 5, 6, "#0f9d78"))
    parts.append(_text(right_x + 350, top_y + 284, "same physical timescale", 16, 700))

    parts.extend(
        [
            _rect(left_x, bottom_y, panel_w, panel_h, "white"),
            _text(
                left_x + 24,
                bottom_y + 38,
                "C. Certified continuum cover in physical time",
                22,
                700,
            ),
            _text(left_x + 24, bottom_y + 68, "Declared interval: tau in [0.55, 1.05] s", 17),
        ]
    )
    cplot_x0 = left_x + 76
    cplot_x1 = left_x + panel_w - 32
    cplot_y0 = bottom_y + 250
    cplot_y1 = bottom_y + 98
    parts.extend(
        [
            _line(cplot_x0, cplot_y0, cplot_x1, cplot_y0, "#9aa8ba", 1.5),
            _line(cplot_x0, cplot_y0, cplot_x0, cplot_y1, "#9aa8ba", 1.5),
            _text(cplot_x0 - 55, cplot_y1 + 8, "0.45", 13),
            _text(cplot_x0 - 55, cplot_y0 + 5, "0.00", 13),
            _text(cplot_x0 + 180, cplot_y0 + 34, "tau grid points", 15),
        ]
    )
    certified_points = []
    observed_points = []
    grid_rows = cover["grid_results"]
    for row in grid_rows:
        grid_size = int(row["grid_size"])
        x = _map(grid_size, 5, 65, cplot_x0, cplot_x1)
        certified = float(row["certified_operator_radius"])
        observed = float(row["dense_max_observed_operator_error"])
        yc = _map(certified, 0.0, 0.45, cplot_y0, cplot_y1)
        yo = _map(observed, 0.0, 0.45, cplot_y0, cplot_y1)
        certified_points.append((x, yc))
        observed_points.append((x, yo))
        parts.append(_text(x - 8, cplot_y0 + 20, str(grid_size), 13))
    parts.append(_polyline(certified_points, "#e06b35", 3.0))
    parts.append(_polyline(observed_points, "#2563eb", 3.0))
    for x, y in certified_points:
        parts.append(_circle(x, y, 6, "#e06b35"))
    for x, y in observed_points:
        parts.append(_circle(x, y, 6, "#2563eb"))
    parts.extend(
        [
            _line(left_x + 370, bottom_y + 88, left_x + 400, bottom_y + 88, "#e06b35", 3),
            _text(left_x + 408, bottom_y + 94, "certified radius", 14),
            _line(
                left_x + 370,
                bottom_y + 112,
                left_x + 400,
                bottom_y + 112,
                "#2563eb",
                3,
            ),
            _text(left_x + 408, bottom_y + 118, "dense numerical check", 14),
        ]
    )

    parts.extend(
        [
            _rect(right_x, bottom_y, panel_w, panel_h, "white"),
            _text(
                right_x + 24,
                bottom_y + 38,
                "D. Irregular timestamps use elapsed physical time",
                22,
                700,
            ),
            _text(right_x + 24, bottom_y + 68, "K(t,s) = exp(-|t-s|/tau)", 17),
        ]
    )
    timeline_x0 = right_x + 42
    timeline_x1 = right_x + panel_w - 38
    timeline_y = bottom_y + 148
    parts.append(_line(timeline_x0, timeline_y, timeline_x1, timeline_y, "#74849a", 2.0))
    irregular_times = irregular["sample_times_seconds"]
    for value in irregular_times:
        x = _map(float(value), 0.0, 2.75, timeline_x0, timeline_x1)
        parts.append(_circle(x, timeline_y, 6, "#6f42c1"))
    parts.extend(
        [
            _text(
                right_x + 28,
                bottom_y + 197,
                "No integer lag is invented. Each covariance entry uses the actual time separation.",
                15,
            ),
            _text(
                right_x + 28,
                bottom_y + 228,
                f'Minimum covariance eigenvalue: {float(irregular["minimum_covariance_eigenvalue"]):.4f}',
                15,
                700,
            ),
            _text(
                right_x + 28,
                bottom_y + 255,
                f'Time-unit invariance error: {float(irregular["time_unit_invariance_max_abs_error"]):.2e}',
                15,
                700,
            ),
            _text(
                right_x + 28,
                bottom_y + 283,
                "Seconds or milliseconds describe the same covariance geometry.",
                15,
            ),
        ]
    )

    parts.extend(
        [
            _rect(60, 866, 1320, 48, "#eef7f3", "#b8ddcf"),
            _text(
                84,
                897,
                "Physical reading: tau belongs to the declared relaxation model; phi belongs to the sampling schedule.",
                18,
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
