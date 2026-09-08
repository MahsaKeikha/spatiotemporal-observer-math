"""Render the publication SVG for Experiment AJ from its committed JSON record."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

WIDTH = 1200
HEIGHT = 900


def _text(x, y, value, css="lab", anchor=None):
    anchor_attr = "" if anchor is None else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}" class="{css}"{anchor_attr}>{escape(str(value))}</text>'


def _line(x1, y1, x2, y2, css):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{css}"/>'


def _circle(x, y, radius, fill):
    return f'<circle cx="{x}" cy="{y:.1f}" r="{radius}" fill="{fill}"/>'


def _rect(x, y, width, height, css=None, fill=None, rx=0):
    attrs = [f'x="{x}"', f'y="{y:.1f}"', f'width="{width}"', f'height="{height:.1f}"']
    if css is not None:
        attrs.append(f'class="{css}"')
    if fill is not None:
        attrs.append(f'fill="{fill}"')
    if rx:
        attrs.append(f'rx="{rx}"')
    return f"<rect {' '.join(attrs)}/>"


def _polyline(points, css):
    encoded = " ".join(f"{x},{y:.1f}" for x, y in points)
    return f'<polyline points="{encoded}" class="{css}"/>'


def render(results):
    records = results["calibration_refinement"]
    checks = results["finite_sample_checks"]
    record_64 = next(record for record in records if record["channel_count"] == 64)
    record_256 = next(record for record in records if record["channel_count"] == 256)

    radius_y = lambda value: 382.0 - (value - 0.70) / 0.50 * 220.0
    phi_y = lambda value: 382.0 - (value - 0.45) / 0.30 * 220.0
    error_y = lambda value: 752.0 - value / 0.12 * 190.0
    check_y = lambda value: 752.0 - value / 1.00 * 190.0

    style = (
        ".title{font:700 28px Arial,sans-serif;fill:#111827}"
        ".sub{font:400 15px Arial,sans-serif;fill:#4b5563}"
        ".panel{fill:#f8fafc;stroke:#d1d5db;stroke-width:1.2}"
        ".h{font:700 17px Arial,sans-serif;fill:#111827}"
        ".lab{font:400 12px Arial,sans-serif;fill:#4b5563}"
        ".num{font:700 20px Arial,sans-serif;fill:#111827}"
        ".small{font:400 11px Arial,sans-serif;fill:#6b7280}"
        ".grid{stroke:#e5e7eb;stroke-width:1}"
        ".main{fill:none;stroke:#2563eb;stroke-width:4}"
        ".upper{fill:none;stroke:#7c3aed;stroke-width:3}"
        ".lower{fill:none;stroke:#059669;stroke-width:3}"
        ".truth{stroke:#dc2626;stroke-width:2;stroke-dasharray:7 5}"
        ".prior{stroke:#6b7280;stroke-width:2;stroke-dasharray:8 5}"
        ".threshold{stroke:#d97706;stroke-width:2;stroke-dasharray:3 5}"
    )

    svg_open = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">'
    )
    description = (
        '<desc id="desc">Proposition 50 calibrates temporal uncertainty from independent '
        'Gaussian channels and composes the result with Proposition 49.</desc>'
    )
    svg = [
        svg_open,
        '<title id="title">Experiment AJ: data-calibrated two-parameter temporal family</title>',
        description,
        '<rect width="1200" height="900" fill="white"/>',
        f"<style>{style}</style>",
        _text(60, 55, "Experiment AJ | Observable calibration of temporal uncertainty", "title"),
        _text(
            60,
            83,
            "Lag-specific concentration, parameter calibration, and compact-family covariance control",
            "sub",
        ),
        _rect(60, 100, 1080, 70, fill="#eef2ff", rx=10),
        _text(85, 128, "Full declared family radius"),
        _text(85, 155, f'{results["full_prior_matrix_radius"]:.3f}', "num"),
        _text(350, 128, "64-channel calibrated radius"),
        _text(350, 155, f'{record_64["matrix_radius"]:.3f}', "num"),
        _text(635, 128, "256-channel calibrated radius"),
        _text(635, 155, f'{record_256["matrix_radius"]:.3f}', "num"),
        _text(925, 128, "Combined confidence lower bound"),
        _text(925, 155, f'{100 * results["combined_confidence_lower_bound"]:.2f}%', "num"),
        _rect(60, 190, 520, 300, css="panel", rx=12),
        _text(85, 222, "A. Learning temporal uncertainty changes theorem usability", "h"),
        _rect(600, 190, 540, 300, css="panel", rx=12),
        _text(625, 222, "B. The calibrated AR(1) interval contracts", "h"),
        _rect(60, 515, 520, 300, css="panel", rx=12),
        _text(85, 547, "C. Increment geometry removes most of the dependence penalty", "h"),
        _rect(600, 515, 540, 300, css="panel", rx=12),
        _text(625, 547, "D. Independent target-record visibility checks", "h"),
    ]

    for value in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2):
        y = radius_y(value)
        svg.extend([_line(90, y, 555, y, "grid"), _text(82, y + 4, f"{value:.1f}", "small", "end")])
    svg.extend(
        [
            _line(
                90,
                radius_y(results["full_prior_matrix_radius"]),
                555,
                radius_y(results["full_prior_matrix_radius"]),
                "prior",
            ),
            _line(90, radius_y(1.0), 555, radius_y(1.0), "threshold"),
        ]
    )
    x_a = [110 + 105 * index for index in range(len(records))]
    points_a = [
        (x, radius_y(record["matrix_radius"]))
        for x, record in zip(x_a, records, strict=True)
    ]
    svg.append(_polyline(points_a, "main"))
    for x, y, record in zip(x_a, [point[1] for point in points_a], records, strict=True):
        svg.extend(
            [
                _circle(x, y, 5, "#2563eb"),
                _text(x, 410, record["channel_count"], "small", "middle"),
            ]
        )
    svg.extend(
        [
            _text(322, 436, "independent calibration channels", "lab", "middle"),
            _text(105, 468, "gray: full family   orange: relative-error threshold 1", "small"),
        ]
    )

    for value in (0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75):
        y = phi_y(value)
        svg.extend([_line(635, y, 1110, y, "grid"), _text(627, y + 4, f"{value:.2f}", "small", "end")])
    x_b = [675 + 100 * index for index in range(len(records))]
    low_points = [
        (x, phi_y(record["autocorrelation_lower"]))
        for x, record in zip(x_b, records, strict=True)
    ]
    upper_points = [
        (x, phi_y(record["autocorrelation_upper"]))
        for x, record in zip(x_b, records, strict=True)
    ]
    svg.extend(
        [
            _polyline(low_points, "lower"),
            _polyline(upper_points, "upper"),
            _line(
                635,
                phi_y(results["true_autocorrelation"]),
                1110,
                phi_y(results["true_autocorrelation"]),
                "truth",
            ),
        ]
    )
    for x, low, upper, record in zip(x_b, low_points, upper_points, records, strict=True):
        svg.extend(
            [
                _circle(x, low[1], 4, "#059669"),
                _circle(x, upper[1], 4, "#7c3aed"),
                _text(x, 410, record["channel_count"], "small", "middle"),
            ]
        )
    svg.extend(
        [
            _text(872, 436, "independent calibration channels", "lab", "middle"),
            _text(645, 468, "green: lower   purple: upper   red: controlled-study truth", "small"),
        ]
    )

    for value in (0.0, 0.03, 0.06, 0.09, 0.12):
        y = error_y(value)
        svg.extend([_line(90, y, 555, y, "grid"), _text(82, y + 4, f"{value:.2f}", "small", "end")])
    bars = [
        (135, "lag 1 specific", record_64["lag_one_error_radius"], "#2563eb"),
        (245, "lag 1 generic", record_64["lag_one_generic_error_radius"], "#9ca3af"),
        (365, "lag 2 specific", record_64["lag_two_error_radius"], "#2563eb"),
        (475, "lag 2 generic", record_64["lag_two_generic_error_radius"], "#9ca3af"),
    ]
    for x, label, value, fill in bars:
        y = error_y(value)
        svg.extend(
            [
                _rect(x - 28, y, 56, 752 - y, fill=fill, rx=5),
                _text(x, y - 8, f"{value:.3f}", "small", "middle"),
                _text(x, 778, label, "small", "middle"),
            ]
        )
    svg.append(
        _text(
            90,
            800,
            "64-channel comparison. Specific bounds use the increment spectrum directly.",
            "small",
        )
    )

    for value in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        y = check_y(value)
        svg.extend([_line(640, y, 1110, y, "grid"), _text(632, y + 4, f"{value:.1f}", "small", "end")])
    for x, check in zip((770, 980), checks, strict=True):
        maximum_y = check_y(check["max_relative_error"])
        theorem_y = check_y(check["theorem_radius"])
        svg.extend(
            [
                _rect(x - 55, maximum_y, 45, 752 - maximum_y, fill="#059669", rx=4),
                _rect(x + 10, theorem_y, 45, 752 - theorem_y, fill="#7c3aed", rx=4),
                _text(
                    x - 33,
                    maximum_y - 8,
                    f'{check["max_relative_error"]:.3f}',
                    "small",
                    "middle",
                ),
                _text(
                    x + 32,
                    theorem_y - 8,
                    f'{check["theorem_radius"]:.3f}',
                    "small",
                    "middle",
                ),
                _text(
                    x,
                    778,
                    f'{check["calibration_channel_count"]} channels',
                    "lab",
                    "middle",
                ),
            ]
        )
    svg.extend(
        [
            _text(665, 800, "green: maximum observed error   purple: theorem radius", "small"),
            _text(
                60,
                858,
                "Proof and simulation remain separate. The probability guarantee is analytical; seeded trials show scale.",
                "sub",
            ),
            _text(
                60,
                882,
                "Reproduce data: python examples/calibrated_temporal_family.py | Render: python examples/render_calibrated_temporal_family.py",
                "small",
            ),
            "</svg>",
        ]
    )
    return "\n".join(svg) + "\n"


def main():
    root = Path(__file__).resolve().parents[1]
    results = json.loads((root / "docs" / "calibrated_temporal_family.json").read_text())
    output = root / "docs" / "calibrated_temporal_family.svg"
    output.write_text(render(results))
    print(output)


if __name__ == "__main__":
    main()
