"""Render the publication SVG for Experiment AK from its committed JSON record."""

from __future__ import annotations

import json
from pathlib import Path


WIDTH = 1200
HEIGHT = 820


def _text(x, y, value, css="lab", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" class="{css}" '
        f'text-anchor="{anchor}">{value}</text>'
    )


def _line(x1, y1, x2, y2, css):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{css}"/>'


def _circle(x, y, radius, css):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" class="{css}"/>'


def _rect(x, y, width, height, css, rx=0):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{rx}" class="{css}"/>'
    )


def render(results):
    records = results["records"]
    final_record = records[-1]
    final_grid = final_record["proposition_51_grid_view"]
    final_rectangle = final_record["proposition_50_rectangle"]
    coverage = results["coverage_visibility_check"]

    phi_min, phi_max = results["declared_autocorrelation_interval"]
    eta_min, eta_max = results["declared_white_noise_fraction_interval"]

    plot_left = 90.0
    plot_right = 610.0
    plot_top = 220.0
    plot_bottom = 680.0

    def px(phi):
        return plot_left + (phi - phi_min) / (phi_max - phi_min) * (
            plot_right - plot_left
        )

    def py(eta):
        return plot_bottom - (eta - eta_min) / (eta_max - eta_min) * (
            plot_bottom - plot_top
        )

    style = """
.title{font:700 27px Arial,sans-serif;fill:#111827}
.sub{font:400 14px Arial,sans-serif;fill:#4b5563}
.h{font:700 17px Arial,sans-serif;fill:#111827}
.lab{font:400 12px Arial,sans-serif;fill:#374151}
.small{font:400 11px Arial,sans-serif;fill:#6b7280}
.metric{font:700 21px Arial,sans-serif;fill:#111827}
.panel{fill:#f8fafc;stroke:#d1d5db;stroke-width:1.2}
.grid{stroke:#e5e7eb;stroke-width:1}
.axis{stroke:#9ca3af;stroke-width:1.2}
.p50{fill:#fef3c7;fill-opacity:.45;stroke:#d97706;stroke-width:2.5}
.p51{fill:#2563eb;fill-opacity:.78}
.truth{fill:#dc2626;stroke:white;stroke-width:2}
.series{fill:none;stroke:#2563eb;stroke-width:3}
.series2{fill:none;stroke:#7c3aed;stroke-width:3}
.threshold{stroke:#dc2626;stroke-width:2;stroke-dasharray:6 5}
.card{fill:white;stroke:#d1d5db;stroke-width:1}
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Experiment AK: finite-sample e-value geometry for temporal calibration</title>',
        '<desc id="desc">A pointwise grid visualization of Proposition 51 is compared with the Proposition 50 rectangle. The exact confidence theorem is continuum valued and does not depend on this plotting grid.</desc>',
        '<rect width="1200" height="820" fill="white"/>',
        f"<style>{style}</style>",
        _text(60, 48, "Experiment AK | Full-likelihood e-value geometry", "title"),
        _text(
            60,
            75,
            "Proposition 51 uses the complete Gaussian residual likelihood instead of separate lag intervals",
            "sub",
        ),
        _rect(60, 95, 1080, 82, "panel", 10),
        _text(90, 120, "256-channel grid view", "small"),
        _text(90, 150, f'{100.0 * final_grid["accepted_fraction"]:.2f}% accepted', "metric"),
        _text(360, 120, "Grid-view bounding-box area", "small"),
        _text(
            360,
            150,
            f'{100.0 * final_grid["bounding_box_area_ratio_to_proposition_50"]:.1f}% of P50',
            "metric",
        ),
        _text(660, 120, "Repeated-sampling visibility check", "small"),
        _text(
            660,
            150,
            f'{coverage["success_count"]}/{coverage["trial_count"]} true parameters accepted',
            "metric",
        ),
        _text(990, 120, "Exact confidence level", "small"),
        _text(990, 150, f'{100.0 * results["confidence"]:.2f}%', "metric"),
        _rect(60, 195, 580, 525, "panel", 10),
        _text(85, 225, "A. Parameter geometry at 256 calibration channels", "h"),
    ]

    for phi in (0.4, 0.5, 0.6, 0.7, 0.8):
        x = px(phi)
        svg.append(_line(x, plot_top, x, plot_bottom, "grid"))
        svg.append(_text(x, 702, f"{phi:.2f}", "small", "middle"))
    for eta in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25):
        y = py(eta)
        svg.append(_line(plot_left, y, plot_right, y, "grid"))
        svg.append(_text(80, y + 4, f"{eta:.2f}", "small", "end"))

    rectangle_x = px(final_rectangle["autocorrelation_lower"])
    rectangle_y = py(final_rectangle["white_noise_fraction_upper"])
    rectangle_width = px(final_rectangle["autocorrelation_upper"]) - rectangle_x
    rectangle_height = py(final_rectangle["white_noise_fraction_lower"]) - rectangle_y
    svg.append(
        f'<rect x="{rectangle_x:.2f}" y="{rectangle_y:.2f}" width="{rectangle_width:.2f}" height="{rectangle_height:.2f}" class="p50"/>'
    )

    for phi, eta in final_grid["accepted_points"]:
        svg.append(_circle(f"{px(phi):.2f}", f"{py(eta):.2f}", 4.0, "p51"))

    svg.extend(
        [
            _circle(
                f'{px(results["true_autocorrelation"]):.2f}',
                f'{py(results["true_white_noise_fraction"]):.2f}',
                7.0,
                "truth",
            ),
            _text(350, 742, "AR(1) coefficient phi", "lab", "middle"),
            _text(94, 245, "eta", "lab"),
            _text(100, 700, "gold rectangle: Proposition 50", "small"),
            _text(310, 700, "blue points: Proposition 51 grid view", "small"),
            _text(520, 700, "red: controlled truth", "small"),
            _rect(665, 195, 475, 250, "panel", 10),
            _text(690, 225, "B. Pointwise accepted grid fraction", "h"),
        ]
    )

    chart_left = 710.0
    chart_right = 1100.0
    chart_top = 255.0
    chart_bottom = 400.0
    channels = [record["channel_count"] for record in records]
    fractions = [record["proposition_51_grid_view"]["accepted_fraction"] for record in records]
    max_fraction = 0.40

    def cx(index):
        return chart_left + index * (chart_right - chart_left) / (len(records) - 1)

    def fy(value):
        return chart_bottom - value / max_fraction * (chart_bottom - chart_top)

    for value in (0.0, 0.1, 0.2, 0.3, 0.4):
        y = fy(value)
        svg.append(_line(chart_left, y, chart_right, y, "grid"))
        svg.append(_text(700, y + 4, f"{100 * value:.0f}%", "small", "end"))
    points = " ".join(
        f"{cx(index):.1f},{fy(value):.1f}" for index, value in enumerate(fractions)
    )
    svg.append(f'<polyline points="{points}" class="series"/>')
    for index, (channel_count, value) in enumerate(zip(channels, fractions, strict=True)):
        svg.append(_circle(f"{cx(index):.1f}", f"{fy(value):.1f}", 5, "p51"))
        svg.append(_text(cx(index), 420, str(channel_count), "small", "middle"))
    svg.append(_text(905, 438, "independent calibration channels", "lab", "middle"))

    svg.extend(
        [
            _rect(665, 470, 475, 250, "panel", 10),
            _text(690, 500, "C. True-parameter log e-value", "h"),
        ]
    )
    log_values = [
        record["proposition_51_grid_view"]["true_parameter_log_evalue"]
        for record in records
    ]
    threshold = final_grid["log_evalue_threshold"]
    log_min = -6.5
    log_max = 5.0
    lower = 540.0
    upper = 675.0

    def ly(value):
        return upper - (value - log_min) / (log_max - log_min) * (upper - lower)

    svg.append(_line(chart_left, ly(threshold), chart_right, ly(threshold), "threshold"))
    svg.append(_text(1095, ly(threshold) - 7, "rejection threshold", "small", "end"))
    log_points = " ".join(
        f"{cx(index):.1f},{ly(value):.1f}" for index, value in enumerate(log_values)
    )
    svg.append(f'<polyline points="{log_points}" class="series2"/>')
    for index, (channel_count, value) in enumerate(zip(channels, log_values, strict=True)):
        svg.append(_circle(f"{cx(index):.1f}", f"{ly(value):.1f}", 5, "p51"))
        svg.append(_text(cx(index), 700, str(channel_count), "small", "middle"))
    svg.extend(
        [
            _text(905, 718, "independent calibration channels", "lab", "middle"),
            _text(
                60,
                770,
                "Important: blue points are a numerical view of the continuum set, not a certified outer grid cover.",
                "sub",
            ),
            _text(
                60,
                795,
                "Coverage comes from Proposition 51: E_theta[q(Z)/p_theta(Z)] = 1, followed by Markov's inequality.",
                "small",
            ),
            "</svg>",
        ]
    )
    return "\n".join(svg) + "\n"


def main():
    root = Path(__file__).resolve().parents[1]
    json_path = root / "docs" / "evalue_temporal_confidence_set.json"
    svg_path = root / "docs" / "evalue_temporal_confidence_set.svg"
    results = json.loads(json_path.read_text())
    svg_path.write_text(render(results))
    print(svg_path)


if __name__ == "__main__":
    main()
