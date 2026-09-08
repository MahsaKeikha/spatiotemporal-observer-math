"""Render the publication SVG for Experiment AJ from its committed JSON record."""

from __future__ import annotations

import json
from pathlib import Path


def render(results):
    records = results["calibration_refinement"]
    checks = results["finite_sample_checks"]

    def radius_y(value):
        return 350.0 - (value - 0.7) / 0.5 * 230.0

    def phi_y(value):
        return 350.0 - (value - 0.45) / 0.31 * 230.0

    def error_y(value):
        return 730.0 - value / 0.12 * 200.0

    def check_y(value):
        return 730.0 - value / 0.95 * 200.0

    record_64 = next(record for record in records if record["channel_count"] == 64)
    record_256 = next(record for record in records if record["channel_count"] == 256)
    x_radius = [110 + 105 * index for index in range(len(records))]
    x_phi = [690 + 95 * index for index in range(len(records))]

    radius_points = " ".join(
        f"{x},{radius_y(record['matrix_radius']):.1f}"
        for x, record in zip(x_radius, records, strict=True)
    )
    lower_points = " ".join(
        f"{x},{phi_y(record['autocorrelation_lower']):.1f}"
        for x, record in zip(x_phi, records, strict=True)
    )
    upper_points = " ".join(
        f"{x},{phi_y(record['autocorrelation_upper']):.1f}"
        for x, record in zip(x_phi, records, strict=True)
    )

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" '
        'viewBox="0 0 1200 900" role="img" aria-labelledby="title desc">',
        '<title id="title">Experiment AJ: data-calibrated two-parameter temporal family</title>',
        '<desc id="desc">Proposition 50 uses lag-1 and lag-2 increment energies from '
        'independent calibration channels to learn a confidence rectangle for temporal '
        'dependence, then composes it with Proposition 49. The displayed covariance radius '
        'drops below one at 64 calibration channels.</desc>',
        '<rect width="1200" height="900" fill="#ffffff"/>',
        '<style>.title{font:700 28px Arial,sans-serif;fill:#111827}.sub{font:400 15px '
        'Arial,sans-serif;fill:#4b5563}.panel{fill:#f8fafc;stroke:#d1d5db;stroke-width:1.2}'
        '.h{font:700 17px Arial,sans-serif;fill:#111827}.lab{font:400 12px Arial,sans-serif;'
        'fill:#4b5563}.num{font:700 20px Arial,sans-serif;fill:#111827}.small{font:400 '
        '11px Arial,sans-serif;fill:#6b7280}.grid{stroke:#e5e7eb;stroke-width:1}.axis{stroke:'
        '#9ca3af;stroke-width:1.2}.main{fill:none;stroke:#2563eb;stroke-width:4}.bound{fill:'
        'none;stroke:#7c3aed;stroke-width:3}.low{fill:none;stroke:#059669;stroke-width:3}.truth'
        '{stroke:#dc2626;stroke-width:2;stroke-dasharray:7 5}.full{stroke:#6b7280;stroke-width:'
        '2;stroke-dasharray:8 5}.threshold{stroke:#d97706;stroke-width:2;stroke-dasharray:3 5}'
        '</style>',
        '<text x="60" y="55" class="title">Experiment AJ | Observable calibration of temporal '
        'uncertainty</text>',
        '<text x="60" y="83" class="sub">Lag-specific Gaussian concentration + nonlinear '
        'parameter map + compact-family matrix Chernoff bound</text>',
        '<rect x="60" y="100" width="1080" height="70" rx="10" fill="#eef2ff" '
        'stroke="#c7d2fe"/>',
        f'<text x="85" y="128" class="lab">Full declared family radius</text><text x="85" '
        f'y="155" class="num">{results["full_prior_matrix_radius"]:.3f}</text>',
        f'<text x="360" y="128" class="lab">64-channel calibrated radius</text><text x="360" '
        f'y="155" class="num">{record_64["matrix_radius"]:.3f}</text>',
        f'<text x="650" y="128" class="lab">256-channel calibrated radius</text><text x="650" '
        f'y="155" class="num">{record_256["matrix_radius"]:.3f}</text>',
        f'<text x="940" y="128" class="lab">Combined confidence lower bound</text><text '
        f'x="940" y="155" class="num">{100.0 * results["combined_confidence_lower_bound"]:.2f}%</text>',
        '<rect x="60" y="190" width="520" height="300" rx="12" class="panel"/><text '
        'x="85" y="222" class="h">A. Covariance certificate becomes usable</text>',
    ]

    for value in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2):
        y = radius_y(value)
        lines.append(
            f'<line x1="90" y1="{y:.1f}" x2="555" y2="{y:.1f}" class="grid"/>'
            f'<text x="65" y="{y + 4:.1f}" class="small">{value:.1f}</text>'
        )
    lines.extend(
        [
            f'<line x1="90" y1="{radius_y(results["full_prior_matrix_radius"]):.1f}" '
            'x2="555" y2="146.7" class="full"/>',
            f'<line x1="90" y1="{radius_y(1.0):.1f}" x2="555" y2="{radius_y(1.0):.1f}" '
            'class="threshold"/>',
            f'<polyline points="{radius_points}" class="main"/>',
        ]
    )
    for x, record in zip(x_radius, records, strict=True):
        lines.append(
            f'<circle cx="{x}" cy="{radius_y(record["matrix_radius"]):.1f}" r="5" '
            'fill="#2563eb"/>'
            f'<text x="{x - 10}" y="378" class="small">{record["channel_count"]}</text>'
        )
    lines.extend(
        [
            '<text x="200" y="402" class="lab">independent calibration channels</text>',
            '<text x="105" y="462" class="small">gray: full prior family     orange: '
            'relative-error threshold 1</text>',
            '<rect x="600" y="190" width="540" height="300" rx="12" class="panel"/>'
            '<text x="625" y="222" class="h">B. The AR(1) interval contracts</text>',
        ]
    )
    for value in (0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75):
        y = phi_y(value)
        lines.append(
            f'<line x1="635" y1="{y:.1f}" x2="1110" y2="{y:.1f}" class="grid"/>'
            f'<text x="605" y="{y + 4:.1f}" class="small">{value:.2f}</text>'
        )
    lines.extend(
        [
            f'<polyline points="{lower_points}" class="low"/><polyline points="{upper_points}" '
            'class="bound"/>',
            f'<line x1="635" y1="{phi_y(results["true_autocorrelation"]):.1f}" x2="1110" '
            f'y2="{phi_y(results["true_autocorrelation"]):.1f}" class="truth"/>',
        ]
    )
    for x, record in zip(x_phi, records, strict=True):
        lines.append(
            f'<circle cx="{x}" cy="{phi_y(record["autocorrelation_lower"]):.1f}" r="4" '
            'fill="#059669"/>'
            f'<circle cx="{x}" cy="{phi_y(record["autocorrelation_upper"]):.1f}" r="4" '
            'fill="#7c3aed"/>'
            f'<text x="{x - 10}" y="378" class="small">{record["channel_count"]}</text>'
        )
    lines.extend(
        [
            '<text x="755" y="402" class="lab">independent calibration channels</text>'
            '<text x="645" y="462" class="small">green: lower bound     purple: upper bound     '
            'red: controlled-study truth</text>',
            '<rect x="60" y="515" width="520" height="300" rx="12" class="panel"/>'
            '<text x="85" y="547" class="h">C. Increment-specific bounds remove the dependence '
            'penalty</text>',
        ]
    )
    for value in (0.0, 0.03, 0.06, 0.09, 0.12):
        y = error_y(value)
        lines.append(
            f'<line x1="90" y1="{y:.1f}" x2="555" y2="{y:.1f}" class="grid"/>'
            f'<text x="65" y="{y + 4:.1f}" class="small">{value:.2f}</text>'
        )
    bars = (
        (125, "lag 1 specific", record_64["lag_one_error_radius"], "#2563eb"),
        (235, "lag 1 generic", record_64["lag_one_generic_error_radius"], "#9ca3af"),
        (365, "lag 2 specific", record_64["lag_two_error_radius"], "#2563eb"),
        (475, "lag 2 generic", record_64["lag_two_generic_error_radius"], "#9ca3af"),
    )
    for x, label, value, fill in bars:
        y = error_y(value)
        lines.append(
            f'<rect x="{x - 30}" y="{y:.1f}" width="60" height="{730.0 - y:.1f}" rx="5" '
            f'fill="{fill}"/><text x="{x - 42}" y="755" class="small">{label}</text>'
            f'<text x="{x - 20}" y="{y - 8:.1f}" class="small">{value:.3f}</text>'
        )
    lines.extend(
        [
            '<text x="88" y="795" class="small">64-channel comparison. Generic uses ||D||^2 '
            '||R||; specific uses the increment spectrum itself.</text>',
            '<rect x="600" y="515" width="540" height="300" rx="12" class="panel"/>'
            '<text x="625" y="547" class="h">D. Independent target-record visibility checks</text>',
        ]
    )
    for value in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        y = check_y(value)
        lines.append(
            f'<line x1="640" y1="{y:.1f}" x2="1110" y2="{y:.1f}" class="grid"/>'
            f'<text x="610" y="{y + 4:.1f}" class="small">{value:.1f}</text>'
        )
    for x, record in zip((760, 970), checks, strict=True):
        maximum_y = check_y(record["max_relative_error"])
        theorem_y = check_y(record["theorem_radius"])
        lines.append(
            f'<rect x="{x - 55}" y="{maximum_y:.1f}" width="45" '
            f'height="{730.0 - maximum_y:.1f}" rx="4" fill="#059669"/>'
            f'<rect x="{x + 10}" y="{theorem_y:.1f}" width="45" '
            f'height="{730.0 - theorem_y:.1f}" rx="4" fill="#7c3aed"/>'
        )
        lines.append(
            f'<text x="{x - 44}" y="{maximum_y - 8:.1f}" class="small">'
            f'{record["max_relative_error"]:.3f}</text>'
            f'<text x="{x + 16}" y="{theorem_y - 8:.1f}" class="small">'
            f'{record["theorem_radius"]:.3f}</text>'
            f'<text x="{x - 40}" y="755" class="lab">'
            f'{record["calibration_channel_count"]} channels</text>'
        )
    lines.extend(
        [
            '<text x="665" y="790" class="small">green: maximum observed error     purple: '
            'theorem radius     all 192 trials covered</text>',
            '<text x="60" y="858" class="sub">Proof and simulation are separate: the probability '
            'guarantee comes from Proposition 50; the seeded trials only show numerical scale.</text>',
            '<text x="60" y="882" class="small">Reproduce data: python examples/'
            'calibrated_temporal_family.py   |   Render publication SVG: python examples/'
            'render_calibrated_temporal_family.py</text>',
            '</svg>',
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    root = Path(__file__).resolve().parents[1]
    json_path = root / "docs" / "calibrated_temporal_family.json"
    svg_path = root / "docs" / "calibrated_temporal_family.svg"
    results = json.loads(json_path.read_text())
    svg_path.write_text(render(results))
    print(svg_path)


if __name__ == "__main__":
    main()
