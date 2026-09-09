"""Render Experiment AP from the committed machine-readable record."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "quadratic_relaxation_calibration.json"
OUTPUT = ROOT / "docs" / "quadratic_relaxation_calibration.svg"


def render(record: dict[str, object]) -> str:
    width, height = 1200, 860
    bg = "#0d1117"
    panel = "#161b22"
    border = "#30363d"
    fg = "#e6edf3"
    muted = "#8b949e"
    blue = "#58a6ff"
    orange = "#f0883e"
    green = "#3fb950"
    red = "#f85149"
    purple = "#bc8cff"

    rows = record["outer_cover_comparison"]
    model = record["model"]
    final = record["quadratic_target_final"]
    references = record["reference_radii"]
    oracle = record["oracle_known_tau_target"]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{bg}"/>',
        f'<text x="60" y="55" fill="{fg}" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="700">Proposition 55 | Experiment AP</text>',
        f'<text x="60" y="84" fill="{muted}" font-family="Arial, Helvetica, sans-serif" font-size="16">Quadratic finite-sample relaxation calibration and the target-concentration bottleneck</text>',
    ]

    for x, y, w, h in ((50, 115, 535, 300), (615, 115, 535, 300), (50, 445, 535, 350), (615, 445, 535, 350)):
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{panel}" stroke="{border}" stroke-width="1.5"/>'
        )

    out.extend(
        [
            f'<text x="75" y="150" fill="{fg}" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="700">A. Certified interval width</text>',
            f'<text x="75" y="174" fill="{muted}" font-family="Arial, Helvetica, sans-serif" font-size="13">Same finite-sample confidence, tighter deterministic enclosure</text>',
        ]
    )
    x0, y0, wplot, hplot = 105, 205, 430, 155
    out.extend(
        [
            f'<line x1="{x0}" y1="{y0 + hplot}" x2="{x0 + wplot}" y2="{y0 + hplot}" stroke="{border}"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + hplot}" stroke="{border}"/>',
        ]
    )
    xs = []
    for index, row in enumerate(rows):
        x = x0 + index * (wplot / (len(rows) - 1))
        xs.append(x)
        out.append(
            f'<text x="{x}" y="{y0 + hplot + 22}" text-anchor="middle" fill="{muted}" font-family="Arial" font-size="12">{row["cell_count"]}</text>'
        )

    def y_width(value: float) -> float:
        return y0 + hplot - (value / 0.9) * hplot

    for tick in (0.0, 0.3, 0.6, 0.9):
        y = y_width(tick)
        out.extend(
            [
                f'<line x1="{x0 - 5}" y1="{y}" x2="{x0}" y2="{y}" stroke="{border}"/>',
                f'<text x="{x0 - 10}" y="{y + 4}" text-anchor="end" fill="{muted}" font-family="Arial" font-size="11">{tick:.1f}</text>',
            ]
        )
    first_points = " ".join(
        f'{x:.1f},{y_width(row["first_order_width_seconds"]):.1f}' for x, row in zip(xs, rows)
    )
    quadratic_points = " ".join(
        f'{x:.1f},{y_width(row["quadratic_width_seconds"]):.1f}' for x, row in zip(xs, rows)
    )
    out.extend(
        [
            f'<polyline points="{first_points}" fill="none" stroke="{blue}" stroke-width="3"/>',
            f'<polyline points="{quadratic_points}" fill="none" stroke="{orange}" stroke-width="3"/>',
        ]
    )
    for x, row in zip(xs, rows):
        out.extend(
            [
                f'<circle cx="{x}" cy="{y_width(row["first_order_width_seconds"])}" r="4" fill="{blue}"/>',
                f'<circle cx="{x}" cy="{y_width(row["quadratic_width_seconds"])}" r="4" fill="{orange}"/>',
            ]
        )
    out.extend(
        [
            f'<text x="325" y="397" text-anchor="middle" fill="{muted}" font-family="Arial" font-size="12">calibration cells</text>',
            f'<rect x="355" y="188" width="12" height="3" fill="{blue}"/><text x="373" y="193" fill="{muted}" font-family="Arial" font-size="11">first-order</text>',
            f'<rect x="447" y="188" width="12" height="3" fill="{orange}"/><text x="465" y="193" fill="{muted}" font-family="Arial" font-size="11">quadratic</text>',
        ]
    )

    out.extend(
        [
            f'<text x="640" y="150" fill="{fg}" font-family="Arial" font-size="20" font-weight="700">B. Physical-time interval at 160 cells</text>',
            f'<text x="640" y="174" fill="{muted}" font-family="Arial" font-size="13">Seconds, with the controlled true value shown as a marker</text>',
        ]
    )
    low_decl, high_decl = 0.4, 1.25
    barx0, barx1 = 680, 1105

    def x_tau(value: float) -> float:
        return barx0 + (value - low_decl) / (high_decl - low_decl) * (barx1 - barx0)

    intervals = (
        ("declared", 0.4, 1.25, muted),
        ("first-order", 0.495625, 1.1065625, blue),
        ("quadratic", final["retained_lower_seconds"], final["retained_upper_seconds"], orange),
    )
    for (label, lower, upper, color), y in zip(intervals, (225, 285, 345)):
        out.extend(
            [
                f'<text x="640" y="{y + 5}" fill="{fg}" font-family="Arial" font-size="13">{label}</text>',
                f'<line x1="{x_tau(lower)}" y1="{y}" x2="{x_tau(upper)}" y2="{y}" stroke="{color}" stroke-width="12" stroke-linecap="round"/>',
                f'<text x="{x_tau(lower)}" y="{y + 25}" text-anchor="middle" fill="{muted}" font-family="Arial" font-size="10">{lower:.3f}</text>',
                f'<text x="{x_tau(upper)}" y="{y + 25}" text-anchor="middle" fill="{muted}" font-family="Arial" font-size="10">{upper:.3f}</text>',
            ]
        )
    true_tau = model["true_relaxation_time_seconds"]
    true_x = x_tau(true_tau)
    out.extend(
        [
            f'<line x1="{true_x}" y1="195" x2="{true_x}" y2="370" stroke="{green}" stroke-width="2" stroke-dasharray="5 5"/>',
            f'<text x="{true_x + 6}" y="205" fill="{green}" font-family="Arial" font-size="12">true τ = {true_tau:.2f} s</text>',
            f'<text x="900" y="397" text-anchor="middle" fill="{orange}" font-family="Arial" font-size="13" font-weight="700">73.0% width contraction at equal cell count</text>',
        ]
    )

    out.extend(
        [
            f'<text x="75" y="480" fill="{fg}" font-family="Arial" font-size="20" font-weight="700">C. Downstream target covariance radius</text>',
            f'<text x="75" y="504" fill="{muted}" font-family="Arial" font-size="13">Smaller is tighter. The horizontal line at 1 is a mathematical usability threshold.</text>',
        ]
    )
    values = (
        ("P53B", references["proposition_53b"], blue),
        ("P54", references["proposition_54"], purple),
        ("P55", final["target_covariance_relative_error"], orange),
        ("known-τ oracle", oracle["target_covariance_relative_error"], green),
    )
    base_y = 745
    threshold_y = base_y - (1.0 / 3.4) * 190.0
    out.extend(
        [
            f'<line x1="90" y1="{threshold_y:.1f}" x2="550" y2="{threshold_y:.1f}" stroke="{red}" stroke-width="1.5" stroke-dasharray="7 5"/>',
            f'<text x="548" y="{threshold_y - 6:.1f}" text-anchor="end" fill="{red}" font-family="Arial" font-size="11">ε = 1</text>',
        ]
    )
    for index, (label, value, color) in enumerate(values):
        x = 110 + index * 100
        bar_height = (value / 3.4) * 190.0
        y = base_y - bar_height
        out.extend(
            [
                f'<rect x="{x}" y="{y:.1f}" width="70" height="{bar_height:.1f}" rx="5" fill="{color}" opacity="0.88"/>',
                f'<text x="{x + 35}" y="{y - 8:.1f}" text-anchor="middle" fill="{fg}" font-family="Arial" font-size="12" font-weight="700">{value:.3f}</text>',
                f'<text x="{x + 35}" y="{base_y + 22}" text-anchor="middle" fill="{muted}" font-family="Arial" font-size="11">{html.escape(label)}</text>',
            ]
        )

    out.extend(
        [
            f'<text x="640" y="480" fill="{fg}" font-family="Arial" font-size="20" font-weight="700">D. What Experiment AP changes</text>',
            f'<text x="650" y="525" fill="{green}" font-family="Arial" font-size="16" font-weight="700">Calibration geometry is now much tighter.</text>',
            f'<text x="650" y="554" fill="{fg}" font-family="Arial" font-size="14">Quadratic cell certificates use exact local slope plus a rigorous</text>',
            f'<text x="650" y="576" fill="{fg}" font-family="Arial" font-size="14">second-order remainder. They do not spend extra probability budget.</text>',
            f'<text x="650" y="620" fill="{orange}" font-family="Arial" font-size="16" font-weight="700">But calibration is no longer the dominant bottleneck.</text>',
            f'<text x="650" y="649" fill="{fg}" font-family="Arial" font-size="14">Even if τ were known exactly, the current target theorem gives</text>',
            f'<text x="650" y="676" fill="{fg}" font-family="Arial" font-size="24" font-weight="700">εoracle = 2.167 &gt; 1</text>',
            f'<text x="650" y="716" fill="{muted}" font-family="Arial" font-size="13">Next proof target: sharpen target covariance concentration or increase</text>',
            f'<text x="650" y="738" fill="{muted}" font-family="Arial" font-size="13">effective target information. More calibration alone cannot close this benchmark.</text>',
            f'<text x="650" y="775" fill="{muted}" font-family="Arial" font-size="11">These are theorem radii under the declared Gaussian exponential-relaxation model.</text>',
        ]
    )
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(record), encoding="utf-8")


if __name__ == "__main__":
    main()
