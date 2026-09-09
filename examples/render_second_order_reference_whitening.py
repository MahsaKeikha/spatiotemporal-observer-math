"""Render Experiment AO from its committed machine-readable record."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "second_order_reference_whitening.json"
OUTPUT = ROOT / "docs" / "second_order_reference_whitening.svg"

WIDTH = 1440
HEIGHT = 960


def _text(
    x: float,
    y: float,
    value: str,
    size: int = 18,
    weight: int = 400,
    fill: str = "#162033",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(value)}</text>'
    )


def _rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    stroke: str = "#d8e0ea",
    radius: int = 18,
) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    )


def _line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    width: float = 2.0,
    dash: str | None = None,
) -> str:
    dashed = "" if dash is None else f' stroke-dasharray="{dash}"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"{dashed}/>'
    )


def _circle(x: float, y: float, radius: float, fill: str) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}"/>'


def _polyline(points: list[tuple[float, float]], stroke: str, width: float = 3.0) -> str:
    encoded = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polyline points="{encoded}" fill="none" stroke="{stroke}" '
        f'stroke-width="{width:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _map(value: float, low: float, high: float, start: float, end: float) -> float:
    return start + (value - low) * (end - start) / (high - low)


def render(record: dict[str, object]) -> str:
    model = record["model"]
    diagnostic = record["diagnostic_continuum"]
    first = record["first_order_certificate"]
    second = record["second_order_certificate"]
    raw = record["raw_target_certificate"]
    whitened = record["reference_whitened_target_certificate"]
    dense = record["dense_target_visibility_check"]

    true_tau = float(model["true_relaxation_time_seconds"])
    tau_low, tau_high = [float(value) for value in model["declared_interval_seconds"]]
    first_low = float(first["retained_lower_seconds"])
    first_high = float(first["retained_upper_seconds"])
    second_low = float(second["retained_lower_seconds"])
    second_high = float(second["retained_upper_seconds"])
    diagnostic_low = float(diagnostic["accepted_lower_seconds"])
    diagnostic_high = float(diagnostic["accepted_upper_seconds"])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        _text(60, 62, "Experiment AO: second-order tau certification and reference whitening", 31, 700),
        _text(
            60,
            98,
            "Same calibration and target geometry as Experiment AN; only the certified method changes.",
            18,
            400,
            "#526277",
        ),
        _rect(60, 122, 1320, 66, "#e9f7f1", "#a6d9c5"),
        _text(88, 164, f"true tau = {true_tau:.2f} s", 23, 700, "#0f766e"),
        _text(
            330,
            164,
            f"combined confidence = {100.0 * float(model['combined_confidence']):.4f}%",
            19,
            700,
        ),
        _text(
            870,
            164,
            f"final covariance radius = {float(whitened['covariance_relative_error']):.4f} < 1",
            19,
            700,
            "#0f766e",
        ),
    ]

    panel_w = 635
    panel_h = 315
    left_x = 60
    right_x = 745
    top_y = 220
    bottom_y = 560

    parts.extend(
        [
            _rect(left_x, top_y, panel_w, panel_h, "white"),
            _text(left_x + 24, top_y + 38, "A. Certified physical-time geometry", 21, 700),
            _text(
                left_x + 24,
                top_y + 66,
                "Curvature replaces the first-derivative cell penalty.",
                15,
                400,
                "#526277",
            ),
        ]
    )
    x0 = left_x + 130
    x1 = left_x + panel_w - 35
    axis_y = top_y + 265
    parts.append(_line(x0, axis_y, x1, axis_y, "#8da0b6", 2))
    for value in (0.4, 0.6, 0.8, 1.0, 1.2):
        x = _map(value, tau_low, tau_high, x0, x1)
        parts.append(_line(x, axis_y - 6, x, axis_y + 6, "#8da0b6", 1.4))
        parts.append(_text(x - 13, axis_y + 27, f"{value:.1f}", 13))

    rows = [
        ("first order", first_low, first_high, top_y + 112, "#f6c8bf", "#d36c56"),
        ("second order", second_low, second_high, top_y + 158, "#cfe0ff", "#5b8fdc"),
        ("diagnostic", diagnostic_low, diagnostic_high, top_y + 204, "#bfe9dc", "#3f9e80"),
    ]
    for label, lower, upper, y, fill, stroke in rows:
        parts.append(_text(left_x + 24, y + 6, label, 14, 700))
        start = _map(lower, tau_low, tau_high, x0, x1)
        end = _map(upper, tau_low, tau_high, x0, x1)
        parts.append(_rect(start, y - 12, end - start, 22, fill, stroke, 6))
    true_x = _map(true_tau, tau_low, tau_high, x0, x1)
    parts.append(_line(true_x, top_y + 92, true_x, axis_y - 12, "#7c3aed", 2.4, "5 5"))
    parts.append(_text(true_x + 7, top_y + 100, "true tau", 13, 700, "#7c3aed"))
    parts.append(
        _text(
            left_x + 24,
            top_y + 304,
            f"width reduction: {float(second['width_reduction_factor_vs_first_order']):.2f}x",
            15,
            700,
            "#1d4ed8",
        )
    )

    parts.extend(
        [
            _rect(right_x, top_y, panel_w, panel_h, "white"),
            _text(right_x + 24, top_y + 38, "B. Continuum e-value remains the statistical object", 21, 700),
            _text(
                right_x + 24,
                top_y + 66,
                "The grid is a visibility check, not the confidence theorem.",
                15,
                400,
                "#526277",
            ),
        ]
    )
    px0 = right_x + 58
    px1 = right_x + panel_w - 34
    py0 = top_y + 260
    py1 = top_y + 96
    tau_grid = [float(value) for value in diagnostic["tau_grid_seconds"]]
    log_values = [float(value) for value in diagnostic["log_evalues"]]
    threshold = float(diagnostic["log_evalue_threshold"])
    ymin = min(min(log_values), threshold) - 0.5
    ymax = max(min(max(log_values), threshold + 9.0), threshold + 1.0)
    parts.extend(
        [
            _line(px0, py0, px1, py0, "#8da0b6", 1.5),
            _line(px0, py0, px0, py1, "#8da0b6", 1.5),
        ]
    )
    curve = []
    for tau, log_value in zip(tau_grid, log_values, strict=True):
        clipped = min(max(log_value, ymin), ymax)
        curve.append(
            (
                _map(tau, tau_low, tau_high, px0, px1),
                _map(clipped, ymin, ymax, py0, py1),
            )
        )
    parts.append(_polyline(curve, "#2563eb", 2.6))
    threshold_y = _map(threshold, ymin, ymax, py0, py1)
    parts.append(_line(px0, threshold_y, px1, threshold_y, "#b54733", 1.8, "6 5"))
    parts.append(_text(px0 + 8, threshold_y - 8, "e-value threshold", 13, 700, "#b54733"))
    parts.append(
        _text(
            right_x + 24,
            top_y + 302,
            f"retained cells: {int(first['retained_cell_count'])} -> {int(second['retained_cell_count'])}",
            15,
            700,
        )
    )

    parts.extend(
        [
            _rect(left_x, bottom_y, panel_w, panel_h, "white"),
            _text(left_x + 24, bottom_y + 38, "C. The downstream covariance bottleneck closes", 21, 700),
            _text(
                left_x + 24,
                bottom_y + 66,
                "Reference whitening changes the temporal geometry before Proposition 49.",
                15,
                400,
                "#526277",
            ),
        ]
    )
    chart_x0 = left_x + 105
    chart_x1 = left_x + panel_w - 50
    chart_y0 = bottom_y + 260
    chart_y1 = bottom_y + 100
    parts.extend(
        [
            _line(chart_x0, chart_y0, chart_x1, chart_y0, "#8da0b6", 1.5),
            _line(chart_x0, chart_y0, chart_x0, chart_y1, "#8da0b6", 1.5),
        ]
    )
    max_error = 3.4
    one_y = _map(1.0, 0.0, max_error, chart_y0, chart_y1)
    parts.append(_line(chart_x0, one_y, chart_x1, one_y, "#b54733", 2.0, "6 5"))
    parts.append(_text(chart_x0 + 8, one_y - 8, "epsilon = 1 threshold", 13, 700, "#b54733"))
    values = [
        ("Prop 53B raw", float(raw["covariance_relative_error"]), "#d36c56"),
        ("Prop 54 whitened", float(whitened["covariance_relative_error"]), "#0f9d78"),
    ]
    for index, (label, value, fill) in enumerate(values):
        x = chart_x0 + 95 + index * 220
        y = _map(value, 0.0, max_error, chart_y0, chart_y1)
        parts.append(_rect(x - 38, y, 76, chart_y0 - y, fill, fill, 5))
        parts.append(_text(x - 31, y - 10, f"{value:.3f}", 16, 700, fill))
        parts.append(_text(x - 66, chart_y0 + 28, label, 13, 700))

    parts.extend(
        [
            _rect(right_x, bottom_y, panel_w, panel_h, "white"),
            _text(right_x + 24, bottom_y + 38, "D. Why the new certificate is tighter", 21, 700),
            _text(
                right_x + 24,
                bottom_y + 78,
                f"reference tau: {float(whitened['reference_relaxation_time_seconds']):.6f} s",
                16,
                700,
            ),
            _text(
                right_x + 24,
                bottom_y + 112,
                f"temporal cover radius: {float(whitened['temporal_covering_radius']):.6f}",
                16,
                700,
                "#0f766e",
            ),
            _text(
                right_x + 24,
                bottom_y + 146,
                f"normalization cover radius: {float(whitened['normalization_covering_radius']):.6f}",
                16,
                700,
            ),
            _text(
                right_x + 24,
                bottom_y + 180,
                f"projected spectral bound: {float(whitened['projected_spectral_norm_bound']):.6f}",
                16,
                700,
            ),
            _text(
                right_x + 24,
                bottom_y + 214,
                f"reference whitening identity error: {float(whitened['reference_whitening_identity_max_abs_error']):.2e}",
                15,
            ),
            _text(
                right_x + 24,
                bottom_y + 248,
                f"dense operator check / certificate: {float(dense['operator_error_to_certificate_ratio']):.3f}",
                15,
            ),
            _text(
                right_x + 24,
                bottom_y + 282,
                f"dense normalization check / certificate: {float(dense['normalization_error_to_certificate_ratio']):.6f}",
                15,
            ),
        ]
    )

    parts.extend(
        [
            _text(
                60,
                925,
                "Proposition 54 closes the controlled epsilon < 1 bottleneck. It does not validate the one-timescale Gaussian model for a real system.",
                16,
                600,
                "#39485a",
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(record), encoding="utf-8")


if __name__ == "__main__":
    main()
