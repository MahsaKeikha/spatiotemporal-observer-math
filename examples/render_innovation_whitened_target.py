"""Render the deterministic Experiment AQ summary figure as SVG."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "innovation_whitened_target.json"
OUTPUT = ROOT / "docs" / "innovation_whitened_target.svg"


def _rect(x: float, y: float, width: float, height: float, css: str, rx: float = 8) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{rx}" class="{css}" />'
    )


def _text(x: float, y: float, value: str, css: str, anchor: str = "start") -> str:
    escaped = (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{css}">{escaped}</text>'


def build_svg(record: dict[str, object]) -> str:
    raw = record["raw_known_tau_oracle"]
    white = record["innovation_whitened"]
    visibility = record["seeded_visibility_check"]
    scalar = record["scalar_exact_reference"]

    raw_radius = float(raw["covariance_relative_error"])
    white_radius = float(white["covariance_relative_error"])
    reduction = 100.0 * float(white["relative_radius_reduction_fraction"])
    median = float(visibility["median_relative_error"])
    q95 = float(visibility["quantile_95_relative_error"])
    q975 = float(visibility["quantile_975_relative_error"])
    maximum = float(visibility["maximum_relative_error"])
    scalar_radius = float(scalar["two_sided_relative_radius"])

    width = 1200
    height = 820
    panel_w = 550
    panel_h = 285
    left = 35
    right = 615
    top = 150
    bottom = 465
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        ".bg{fill:#f8fafc}.panel{fill:#ffffff;stroke:#cbd5e1;stroke-width:1.5}",
        ".title{font:700 28px Arial,sans-serif;fill:#0f172a}.subtitle{font:15px Arial,sans-serif;fill:#475569}",
        ".ptitle{font:700 18px Arial,sans-serif;fill:#0f172a}.label{font:14px Arial,sans-serif;fill:#334155}",
        ".small{font:12px Arial,sans-serif;fill:#64748b}.value{font:700 17px Arial,sans-serif;fill:#0f172a}",
        ".old{fill:#94a3b8}.new{fill:#2563eb}.good{fill:#059669}.warn{fill:#dc2626}.guide{stroke:#94a3b8;stroke-width:1.5;stroke-dasharray:6 5}",
        ".axis{stroke:#cbd5e1;stroke-width:1}.matrix{fill:#dbeafe;stroke:#2563eb;stroke-width:.7}.matrix2{fill:#dcfce7;stroke:#059669;stroke-width:.7}",
        "</style>",
        _rect(0, 0, width, height, "bg", rx=0),
        _text(35, 48, "Experiment AQ - exact innovation-whitened target covariance", "title"),
        _text(35, 78, "Proposition 56 changes the target estimator: local physical-time innovations first, covariance concentration second.", "subtitle"),
        _text(35, 106, f"Known-tau raw oracle {raw_radius:.3f}  ->  innovation-whitened {white_radius:.3f}  ({reduction:.2f}% reduction)", "value"),
        _rect(left, top, panel_w, panel_h, "panel"),
        _rect(right, top, panel_w, panel_h, "panel"),
        _rect(left, bottom, panel_w, panel_h, "panel"),
        _rect(right, bottom, panel_w, panel_h, "panel"),
    ]

    # Panel A: certified radii.
    x0 = left + 45
    y0 = top + 70
    chart_w = 440
    max_scale = 2.4
    threshold_x = x0 + chart_w * (1.0 / max_scale)
    parts += [
        _text(left + 22, top + 32, "A. Target covariance radius", "ptitle"),
        f'<line x1="{x0}" y1="{y0+150}" x2="{x0+chart_w}" y2="{y0+150}" class="axis" />',
        f'<line x1="{threshold_x}" y1="{y0-5}" x2="{threshold_x}" y2="{y0+155}" class="guide" />',
        _text(threshold_x + 5, y0 + 8, "epsilon = 1", "small"),
        _text(x0, y0 + 45, "Raw known-tau oracle", "label"),
        _rect(x0, y0 + 55, chart_w * raw_radius / max_scale, 34, "old", rx=4),
        _text(x0 + chart_w * raw_radius / max_scale - 8, y0 + 79, f"{raw_radius:.3f}", "value", anchor="end"),
        _text(x0, y0 + 120, "Innovation-whitened", "label"),
        _rect(x0, y0 + 130, chart_w * white_radius / max_scale, 34, "new", rx=4),
        _text(x0 + chart_w * white_radius / max_scale - 8, y0 + 154, f"{white_radius:.3f}", "value", anchor="end"),
        _text(left + 22, top + 260, "The new theorem enters the perturbative epsilon < 1 regime on the same 120-sample target.", "small"),
    ]

    # Panel B: temporal concentration geometry.
    parts += [
        _text(right + 22, top + 32, "B. Concentration geometry", "ptitle"),
        _text(right + 28, top + 72, "Raw-time projected temporal spectrum", "label"),
        _text(right + 310, top + 72, "Innovation spectrum", "label"),
        _text(right + 28, top + 104, f"trace = {float(raw['projected_degrees_of_freedom_lower_bound']):.3f}", "value"),
        _text(right + 28, top + 134, f"max eigenvalue = {float(raw['projected_spectral_norm_bound']):.3f}", "value"),
        _text(right + 310, top + 104, "trace = 118", "value"),
        _text(right + 310, top + 134, "max eigenvalue = 1", "value"),
        _text(right + 28, top + 178, "strong leading temporal weight", "small"),
        _text(right + 310, top + 178, "118 equal unit weights", "small"),
    ]
    for idx, h in enumerate((92, 61, 45, 33, 26, 21, 17, 14)):
        parts.append(_rect(right + 42 + 22 * idx, top + 232 - h, 14, h, "old", rx=2))
    for idx in range(8):
        parts.append(_rect(right + 330 + 22 * idx, top + 185, 14, 47, "new", rx=2))
    parts += [
        _text(right + 22, top + 260, "Whitening uses the temporal law to change the estimator instead of paying a worst-case dependence penalty.", "small"),
    ]

    # Panel C: seeded error visibility check.
    gauge_x = left + 45
    gauge_y = bottom + 120
    gauge_w = 440
    gauge_scale = 0.48
    def gx(value: float) -> float:
        return gauge_x + gauge_w * value / gauge_scale

    parts += [
        _text(left + 22, bottom + 32, "C. Seeded scalar visibility check", "ptitle"),
        _text(left + 22, bottom + 62, f"512 / 512 recorded errors lie below the Proposition 56 radius", "label"),
        f'<line x1="{gauge_x}" y1="{gauge_y}" x2="{gauge_x+gauge_w}" y2="{gauge_y}" class="axis" />',
        _rect(gauge_x, gauge_y - 18, gx(median) - gauge_x, 16, "good", rx=3),
        f'<line x1="{gx(q95)}" y1="{gauge_y-32}" x2="{gx(q95)}" y2="{gauge_y+12}" class="axis" />',
        f'<line x1="{gx(q975)}" y1="{gauge_y-38}" x2="{gx(q975)}" y2="{gauge_y+18}" class="axis" />',
        f'<line x1="{gx(maximum)}" y1="{gauge_y-44}" x2="{gx(maximum)}" y2="{gauge_y+24}" class="warn" />',
        f'<line x1="{gx(white_radius)}" y1="{gauge_y-54}" x2="{gx(white_radius)}" y2="{gauge_y+30}" class="guide" />',
        _text(gauge_x, gauge_y + 44, f"median {median:.3f}", "small"),
        _text(gx(q95), gauge_y + 44, f"95% {q95:.3f}", "small", anchor="middle"),
        _text(gx(q975), gauge_y + 64, f"97.5% {q975:.3f}", "small", anchor="middle"),
        _text(gx(maximum), gauge_y - 52, f"max {maximum:.3f}", "small", anchor="middle"),
        _text(gx(white_radius), gauge_y - 66, f"theorem {white_radius:.3f}", "small", anchor="middle"),
        _text(left + 22, bottom + 244, f"Dimension-one exact chi-square reference: {scalar_radius:.3f}. The public theorem stays matrix-valued.", "small"),
    ]

    # Panel D: local operator sparsity.
    parts += [
        _text(right + 22, bottom + 32, "D. Local physical-time structure", "ptitle"),
        _text(right + 22, bottom + 64, "W_tau is lower bidiagonal", "label"),
        _text(right + 292, bottom + 64, "R_tau^-1 is tridiagonal", "label"),
    ]
    cell = 18
    mx1 = right + 70
    my = bottom + 92
    mx2 = right + 340
    n = 7
    for i in range(n):
        parts.append(_rect(mx1 + i * cell, my + i * cell, 12, 12, "matrix", rx=1))
        if i > 0:
            parts.append(_rect(mx1 + (i - 1) * cell, my + i * cell, 12, 12, "matrix", rx=1))
        parts.append(_rect(mx2 + i * cell, my + i * cell, 12, 12, "matrix2", rx=1))
        if i > 0:
            parts.append(_rect(mx2 + (i - 1) * cell, my + i * cell, 12, 12, "matrix2", rx=1))
            parts.append(_rect(mx2 + i * cell, my + (i - 1) * cell, 12, 12, "matrix2", rx=1))
    parts += [
        _text(right + 22, bottom + 234, f"239 nonzeros in W_tau; 358 in the 120 x 120 precision matrix", "small"),
        _text(right + 22, bottom + 257, f"whitening identity operator error {float(white['whitening_identity_operator_error']):.2e}", "small"),
        _text(right + 22, bottom + 278, "The predictable temporal step is removed locally before nuisance fitting and covariance estimation.", "small"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(build_svg(record), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
