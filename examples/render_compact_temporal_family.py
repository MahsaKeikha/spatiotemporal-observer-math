"""Render the committed publication SVG for Experiment AI from its JSON record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _render(results):
    records = results["cover_refinement"]
    checks = results["finite_sample_checks"]

    def y(value, top=154.0, bottom=350.0, maximum=3.2):
        return bottom - (bottom - top) * value / maximum

    def y_error(value):
        return 680.0 - 196.0 * value

    x_values = (132, 322, 512)
    sphere = [record["sphere_net_family_radius"] for record in records]
    matrix = [record["matrix_family_radius"] for record in records]
    cover_radius = [
        record["projected_eigenvalue_covering_radius"] for record in records
    ]
    reduction = [100.0 * record["relative_radius_reduction"] for record in records]

    sphere_points = " ".join(
        f"{x},{y(value):.1f}" for x, value in zip(x_values, sphere, strict=True)
    )
    matrix_points = " ".join(
        f"{x},{y(value):.1f}" for x, value in zip(x_values, matrix, strict=True)
    )

    cover_x = (684, 822, 960)

    def y_cover(value):
        return 350.0 - 196.0 * value

    def y_reduction(value):
        return 350.0 - 196.0 * (value - 60.0) / 5.0

    cover_points = " ".join(
        f"{x},{y_cover(value):.1f}"
        for x, value in zip(cover_x, cover_radius, strict=True)
    )
    reduction_points = " ".join(
        f"{x},{y_reduction(value):.1f}"
        for x, value in zip(cover_x, reduction, strict=True)
    )

    check_x = (190, 454)
    q95_points = " ".join(
        f"{x},{y_error(check['q95_relative_error']):.1f}"
        for x, check in zip(check_x, checks, strict=True)
    )
    maximum_points = " ".join(
        f"{x},{y_error(check['max_relative_error']):.1f}"
        for x, check in zip(check_x, checks, strict=True)
    )
    theorem_points = " ".join(
        f"{x},{y_error(check['uniform_family_radius']):.1f}"
        for x, check in zip(check_x, checks, strict=True)
    )

    left, right, top, bottom = 688.0, 1084.0, 493.0, 661.0
    phi_lower, phi_upper = results["autocorrelation_interval"]
    eta_lower, eta_upper = results["white_noise_fraction_interval"]

    def parameter_x(phi):
        return left + (right - left) * (phi - phi_lower) / (phi_upper - phi_lower)

    def parameter_y(eta):
        return bottom - (bottom - top) * (eta - eta_lower) / (eta_upper - eta_lower)

    cover_lines = []
    for phi in results["final_cover"]["autocorrelation_grid"]:
        x = parameter_x(phi)
        cover_lines.append(
            f'<line x1="{x:.1f}" y1="493" x2="{x:.1f}" y2="661" class="cover"/>'
        )
    for eta in results["final_cover"]["white_noise_fraction_grid"]:
        yy = parameter_y(eta)
        cover_lines.append(
            f'<line x1="688" y1="{yy:.1f}" x2="1084" y2="{yy:.1f}" class="cover"/>'
        )

    stars = []
    for check in checks:
        x = parameter_x(check["true_autocorrelation"])
        yy = parameter_y(check["true_white_noise_fraction"])
        stars.append(
            f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="8" class="star"/>'
            f'<text x="{x:.1f}" y="{yy + 4:.1f}" text-anchor="middle" '
            'class="startext">*</text>'
        )

    total_trials = sum(check["trial_count"] for check in checks)
    theorem_radius = checks[0]["uniform_family_radius"]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="820" viewBox="0 0 1200 820" role="img" aria-labelledby="title desc">
<title id="title">Experiment AI: compact temporal-family matrix concentration</title>
<desc id="desc">Proposition 49 matrix concentration over a two-parameter temporal covariance family. Refining a deterministic cover moves the matrix certificate below relative error one without a stochastic union penalty over cover points.</desc>
<rect width="1200" height="820" fill="white"/>
<style>
.title{{font:700 25px system-ui,-apple-system,Segoe UI,sans-serif;fill:#111827}}
.sub{{font:14px system-ui,-apple-system,Segoe UI,sans-serif;fill:#4b5563}}
.pt{{font:700 18px system-ui,-apple-system,Segoe UI,sans-serif;fill:#111827}}
.lab{{font:14px system-ui,-apple-system,Segoe UI,sans-serif;fill:#374151}}
.tick{{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:#4b5563}}
.small{{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:#374151}}
.tiny{{font:11px system-ui,-apple-system,Segoe UI,sans-serif;fill:#6b7280}}
.axis{{stroke:#374151;stroke-width:1.4}}
.cover{{stroke:#dbeafe;stroke-width:1}}
.blue{{stroke:#2563eb;fill:none;stroke-width:3}}
.orange{{stroke:#ea580c;fill:none;stroke-width:3}}
.teal{{stroke:#0f766e;fill:none;stroke-width:3}}
.gray{{stroke:#6b7280;fill:none;stroke-width:2;stroke-dasharray:8 6}}
.b{{fill:#2563eb}} .o{{fill:#ea580c}} .t{{fill:#0f766e}}
.card{{fill:#f9fafb;stroke:#e5e7eb;stroke-width:1.2}}
.good{{fill:#ecfdf5;stroke:#a7f3d0}}
.metric{{font:700 22px system-ui,-apple-system,Segoe UI,sans-serif;fill:#065f46}}
.metriclabel{{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:#065f46}}
.star{{fill:#0f766e}} .startext{{font:700 12px system-ui;fill:white}}
</style>
<text x="600" y="40" text-anchor="middle" class="title">Experiment AI: matrix concentration over a compact two-parameter temporal family</text>
<text x="600" y="66" text-anchor="middle" class="sub">N = {results['sample_count']}, dimension {results['dimension']}, affine nuisance design, {100.0 * results['confidence']:.1f}% covariance confidence</text>

<rect x="42" y="94" width="544" height="306" rx="10" class="card"/>
<text x="314" y="124" text-anchor="middle" class="pt">Deterministic cover refinement crosses the radius-one boundary</text>
<line x1="92" y1="350" x2="552" y2="350" class="axis"/><line x1="92" y1="154" x2="92" y2="350" class="axis"/>
<line x1="92" y1="{y(1.0):.1f}" x2="552" y2="{y(1.0):.1f}" class="gray"/><text x="544" y="{y(1.0) - 8.0:.1f}" text-anchor="end" class="small">relative error = 1</text>
<polyline points="{sphere_points}" class="orange"/><polyline points="{matrix_points}" class="blue"/>
{''.join(f'<circle cx="{x}" cy="{y(value):.1f}" r="5" class="o"/>' for x, value in zip(x_values, sphere, strict=True))}
{''.join(f'<circle cx="{x}" cy="{y(value):.1f}" r="5" class="b"/>' for x, value in zip(x_values, matrix, strict=True))}
{''.join(f'<text x="{x}" y="371" text-anchor="middle" class="tick">{records[index]["cover_point_count"]}</text>' for index, x in enumerate(x_values))}
<text x="322" y="391" text-anchor="middle" class="lab">temporal cover points</text>
<line x1="116" y1="144" x2="144" y2="144" class="orange"/><text x="152" y="149" class="small">sphere-net family</text>
<line x1="330" y1="144" x2="358" y2="144" class="blue"/><text x="366" y="149" class="small">Proposition 49</text>
{''.join(f'<text x="{x}" y="{y(matrix[index]) + 18.0:.1f}" text-anchor="middle" class="tiny">{matrix[index]:.3f}</text>' for index, x in enumerate(x_values))}

<rect x="614" y="94" width="544" height="306" rx="10" class="card"/>
<text x="886" y="124" text-anchor="middle" class="pt">Better geometry costs no stochastic cover multiplicity</text>
<line x1="664" y1="350" x2="1124" y2="350" class="axis"/><line x1="664" y1="154" x2="664" y2="350" class="axis"/>
<polyline points="{cover_points}" class="blue"/><polyline points="{reduction_points}" class="teal"/>
{''.join(f'<circle cx="{x}" cy="{y_cover(value):.1f}" r="5" class="b"/>' for x, value in zip(cover_x, cover_radius, strict=True))}
{''.join(f'<circle cx="{x}" cy="{y_reduction(value):.1f}" r="5" class="t"/>' for x, value in zip(cover_x, reduction, strict=True))}
{''.join(f'<text x="{x}" y="371" text-anchor="middle" class="tick">{records[index]["cover_point_count"]}</text>' for index, x in enumerate(cover_x))}
<text x="894" y="391" text-anchor="middle" class="lab">cover points: 15 -&gt; 45 -&gt; 153</text>
<text x="654" y="158" text-anchor="end" class="tick">1.0</text><text x="654" y="354" text-anchor="end" class="tick">0</text>
<text x="1114" y="176" text-anchor="end" class="small">operator radius: {cover_radius[0]:.3f} -&gt; {cover_radius[-1]:.3f}</text>
<text x="1114" y="198" text-anchor="end" class="small">reduction vs sphere-net: {reduction[-1]:.1f}%</text>
<rect x="696" y="224" width="380" height="84" rx="8" class="good"/>
<text x="886" y="258" text-anchor="middle" class="metric">no union bound over cover points</text>
<text x="886" y="283" text-anchor="middle" class="metriclabel">the finite cover is deterministic geometry inside one matrix-mgf envelope</text>

<rect x="42" y="424" width="544" height="306" rx="10" class="card"/>
<text x="314" y="454" text-anchor="middle" class="pt">Seeded target-record visibility check</text>
<line x1="92" y1="680" x2="552" y2="680" class="axis"/><line x1="92" y1="484" x2="92" y2="680" class="axis"/>
<polyline points="{q95_points}" class="teal"/><polyline points="{maximum_points}" class="orange"/><polyline points="{theorem_points}" class="blue"/>
{''.join(f'<circle cx="{x}" cy="{y_error(check["q95_relative_error"]):.1f}" r="5" class="t"/><circle cx="{x}" cy="{y_error(check["max_relative_error"]):.1f}" r="5" class="o"/><circle cx="{x}" cy="{y_error(check["uniform_family_radius"]):.1f}" r="5" class="b"/>' for x, check in zip(check_x, checks, strict=True))}
<text x="190" y="704" text-anchor="middle" class="tick">phi=.60, eta=.02</text><text x="454" y="704" text-anchor="middle" class="tick">phi=.70, eta=.04</text>
<text x="314" y="722" text-anchor="middle" class="small">{total_trials} of {total_trials} recorded target errors covered by radius {theorem_radius:.3f}</text>
<line x1="118" y1="474" x2="146" y2="474" class="teal"/><text x="154" y="479" class="small">95th percentile</text>
<line x1="270" y1="474" x2="298" y2="474" class="orange"/><text x="306" y="479" class="small">maximum</text>
<line x1="424" y1="474" x2="452" y2="474" class="blue"/><text x="460" y="479" class="small">P49 radius</text>

<rect x="614" y="424" width="544" height="306" rx="10" class="card"/>
<text x="886" y="454" text-anchor="middle" class="pt">Final 17 x 9 cover spans the full parameter rectangle</text>
<rect x="688" y="493" width="396" height="168" fill="#fff" stroke="#9ca3af"/>
{''.join(cover_lines)}
{''.join(stars)}
<text x="886" y="684" text-anchor="middle" class="lab">AR(1) coefficient phi: {phi_lower:.2f} to {phi_upper:.2f}</text>
<text x="665" y="577" transform="rotate(-90 665 577)" text-anchor="middle" class="lab">white-noise fraction eta: {eta_lower:.2f} to {eta_upper:.2f}</text>
<text x="886" y="712" text-anchor="middle" class="small">{records[-1]['cover_point_count']} deterministic cover points; stars mark seeded target checks</text>

<text x="600" y="786" text-anchor="middle" class="small">Source: docs/compact_temporal_family.json | Render: python examples/render_compact_temporal_family.py</text>
</svg>
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/compact_temporal_family.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/compact_temporal_family.svg"),
    )
    args = parser.parse_args()
    results = json.loads(args.input.read_text())
    args.output.write_text(_render(results))


if __name__ == "__main__":
    main()
