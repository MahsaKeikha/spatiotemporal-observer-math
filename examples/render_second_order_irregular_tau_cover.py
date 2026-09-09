"""Render Experiment AO from its committed machine-readable record."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "second_order_irregular_tau_cover.json"
OUTPUT = ROOT / "docs" / "second_order_irregular_tau_cover.svg"

WIDTH = 1440
HEIGHT = 900


def _text(x: float, y: float, value: str, size: int = 18, weight: int = 400, fill: str = "#162033") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{value}</text>'
    )


def _rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "#d8e0ea", radius: int = 16) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    )


def _line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2.0) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"/>'
    )


def _map(value: float, low: float, high: float, start: float, end: float) -> float:
    return start + (value - low) * (end - start) / (high - low)


def render(record: dict[str, object]) -> str:
    model = record["model"]
    diagnostic = record["diagnostic_continuum"]
    first = record["first_order_certificate"]
    second = record["second_order_certificate"]
    oracle = record["oracle_known_tau"]

    tau_low, tau_high = [float(v) for v in model["declared_interval_seconds"]]
    true_tau = float(model["true_relaxation_time_seconds"])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        _text(60, 62, "Experiment AO: second-order certification reveals the real bottleneck", 30, 700),
        _text(60, 98, "The tau cover becomes nearly diagnostic, but raw target dependence still prevents an error radius below one.", 18, 400, "#526277"),
        _rect(60, 122, 1320, 66, "#eaf2ff", "#b9d1f6"),
        _text(88, 164, f"true tau = {true_tau:.2f} s", 23, 700, "#1d4ed8"),
        _text(330, 164, f"combined confidence = {100.0 * float(model['combined_confidence']):.4f}%", 19, 700, "#0f766e"),
        _text(800, 164, "same calibration and target geometry as Experiment AN", 18, 500),
    ]

    left_x = 60
    right_x = 745
    top_y = 220
    bottom_y = 545
    panel_w = 635
    panel_h = 285

    parts.extend([
        _rect(left_x, top_y, panel_w, panel_h, "white"),
        _text(left_x + 24, top_y + 38, "A. Certified physical-time interval", 21, 700),
        _text(left_x + 24, top_y + 65, "Second-order Taylor control removes most of the geometric slack.", 15, 400, "#526277"),
    ])
    x0 = left_x + 80
    x1 = left_x + panel_w - 35
    axis_y = top_y + 232
    parts.append(_line(x0, axis_y, x1, axis_y, "#8da0b6", 1.8))
    for value in (0.4, 0.6, 0.8, 1.0, 1.2):
        x = _map(value, tau_low, tau_high, x0, x1)
        parts.append(_line(x, axis_y - 6, x, axis_y + 6, "#8da0b6", 1.2))
        parts.append(_text(x - 15, axis_y + 28, f"{value:.1f}", 13))

    rows = [
        ("first-order", float(first["retained_lower_seconds"]), float(first["retained_upper_seconds"]), top_y + 106, "#cfe0ff", "#77a5ee"),
        ("second-order", float(second["retained_lower_seconds"]), float(second["retained_upper_seconds"]), top_y + 151, "#bfe9dc", "#49a98a"),
        ("diagnostic", float(diagnostic["accepted_lower_seconds"]), float(diagnostic["accepted_upper_seconds"]), top_y + 196, "#eadcff", "#9d76d9"),
    ]
    for label, low, high, y, fill, stroke in rows:
        parts.append(_text(left_x + 24, y + 6, label, 14, 700))
        sx = _map(low, tau_low, tau_high, x0, x1)
        ex = _map(high, tau_low, tau_high, x0, x1)
        parts.append(_rect(sx, y - 12, ex - sx, 22, fill, stroke, 5))
    true_x = _map(true_tau, tau_low, tau_high, x0, x1)
    parts.append(_line(true_x, top_y + 88, true_x, axis_y - 10, "#7c3aed", 2.0))

    parts.extend([
        _rect(right_x, top_y, panel_w, panel_h, "white"),
        _text(right_x + 24, top_y + 38, "B. Cell certificate contraction", 21, 700),
        _text(right_x + 24, top_y + 72, f"First-order retained cells: {int(first['retained_cell_count'])} / {int(model['cell_count'])}", 17),
        _text(right_x + 24, top_y + 106, f"Second-order retained cells: {int(second['retained_cell_count'])} / {int(model['cell_count'])}", 17, 700, "#0f766e"),
        _text(right_x + 24, top_y + 150, f"Certified width reduction: {100.0 * float(second['cover_width_reduction_fraction']):.1f}%", 22, 700, "#0f766e"),
        _text(right_x + 24, top_y + 190, f"First-order width: {float(first['retained_width_seconds']):.6f} s", 15),
        _text(right_x + 24, top_y + 220, f"Second-order width: {float(second['retained_width_seconds']):.6f} s", 15, 700),
        _text(right_x + 24, top_y + 250, f"Diagnostic width: {float(diagnostic['accepted_width_seconds']):.6f} s", 15),
    ])

    parts.extend([
        _rect(left_x, bottom_y, panel_w, panel_h, "white"),
        _text(left_x + 24, bottom_y + 38, "C. Target covariance radius", 21, 700),
        _text(left_x + 24, bottom_y + 65, "The cover improvement helps, but does not cross the perturbative threshold.", 15, 400, "#526277"),
    ])
    bar_x0 = left_x + 170
    bar_x1 = left_x + panel_w - 45
    scale_max = 3.4
    entries = [
        ("first-order", float(first["target_covariance_relative_error"]), bottom_y + 111, "#7aa2e3"),
        ("second-order", float(second["target_covariance_relative_error"]), bottom_y + 166, "#0f9d78"),
        ("oracle tau", float(oracle["target_covariance_relative_error"]), bottom_y + 221, "#7c3aed"),
    ]
    threshold_x = _map(1.0, 0.0, scale_max, bar_x0, bar_x1)
    parts.append(_line(threshold_x, bottom_y + 86, threshold_x, bottom_y + 245, "#c94d3f", 2.0))
    parts.append(_text(threshold_x - 24, bottom_y + 270, "radius = 1", 13, 700, "#b54733"))
    for label, value, y, fill in entries:
        parts.append(_text(left_x + 24, y + 6, label, 14, 700))
        ex = _map(value, 0.0, scale_max, bar_x0, bar_x1)
        parts.append(_rect(bar_x0, y - 12, ex - bar_x0, 24, fill, fill, 5))
        parts.append(_text(ex + 10, y + 6, f"{value:.3f}", 14, 700))

    parts.extend([
        _rect(right_x, bottom_y, panel_w, panel_h, "white"),
        _text(right_x + 24, bottom_y + 38, "D. What Proposition 54 changes", 21, 700),
        _text(right_x + 24, bottom_y + 78, "Cover uncertainty is no longer the main limitation.", 18, 700, "#0f766e"),
        _text(right_x + 24, bottom_y + 112, "Even exact knowledge of tau leaves the raw target radius above one.", 16),
        _text(right_x + 24, bottom_y + 151, "Next theorem:", 16, 700),
        _text(right_x + 24, bottom_y + 184, "propagate calibrated tau uncertainty through the exact irregular-time", 16),
        _text(right_x + 24, bottom_y + 211, "innovation whitener, then concentrate the near-iid target innovations.", 16),
        _rect(right_x + 24, bottom_y + 235, panel_w - 48, 34, "#fff3cd", "#e6b84c", 8),
        _text(right_x + 40, bottom_y + 258, "The bottleneck has moved from calibration geometry to temporal dependence.", 15, 700, "#8a5b00"),
    ])

    parts.extend([
        _text(60, 870, "Proposition 54 preserves the 97.5% finite-sample calibration guarantee. The new cover is deterministic conditional on the observed calibration record.", 15, 600, "#39485a"),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(record), encoding="utf-8")


if __name__ == "__main__":
    main()
