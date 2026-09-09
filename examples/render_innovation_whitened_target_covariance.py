"""Render Experiment AQ from its committed machine-readable record."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs" / "innovation_whitened_target_covariance.json"
OUTPUT = ROOT / "docs" / "innovation_whitened_target_covariance.svg"


def _text(x: float, y: float, value: str, size: int = 24, weight: int = 400) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#e6edf3">'
        f"{escape(value)}</text>"
    )


def _muted(x: float, y: float, value: str, size: int = 18) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" fill="#9da7b3">{escape(value)}</text>'
    )


def _panel(x: int, y: int, width: int, height: int, title: str) -> list[str]:
    return [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="18" '
        'fill="#111820" stroke="#30363d" stroke-width="2"/>',
        _text(x + 28, y + 42, title, 22, 650),
    ]


def _bar(
    x: int,
    y: int,
    label: str,
    value: float,
    maximum: float,
    width: int,
    note: str,
) -> list[str]:
    bar_width = max(2.0, width * value / maximum)
    return [
        _muted(x, y - 8, label, 16),
        f'<rect x="{x}" y="{y}" width="{width}" height="24" rx="7" fill="#202a35"/>',
        f'<rect x="{x}" y="{y}" width="{bar_width:.2f}" height="24" rx="7" fill="#58a6ff"/>',
        _text(x + width + 18, y + 20, f"{value:.3f}", 18, 650),
        _muted(x, y + 48, note, 14),
    ]


def render(record: dict[str, object]) -> str:
    comparison = record["certificate_comparison"]
    trials = record["visibility_trials"]
    model = record["model"]

    raw = float(comparison["raw_space_known_tau_oracle_relative_error"])
    matrix = float(comparison["innovation_whitened_matrix_relative_error"])
    scalar = float(comparison["innovation_whitened_exact_scalar_relative_error"])
    raw_degrees = float(comparison["raw_space_projected_degrees_lower_bound"])
    residual_degrees = int(comparison["innovation_whitened_residual_degrees"])

    pieces = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="940" viewBox="0 0 1400 940">',
        '<rect width="1400" height="940" fill="#0d1117"/>',
        _text(64, 70, "Experiment AQ | Innovation-whitened target covariance", 34, 750),
        _muted(
            64,
            105,
            "Exact temporal whitening exposes independent innovations before nuisance projection.",
            19,
        ),
    ]

    pieces += _panel(55, 145, 635, 330, "A. Same target, different covariance certificate")
    maximum = 2.35
    pieces += _bar(90, 205, "Raw-space known-tau theorem", raw, maximum, 410, "Existing P49 oracle geometry")
    pieces += _bar(90, 300, "Whitened matrix certificate", matrix, maximum, 410, "Ordinary Wishart after exact whitening")
    pieces += _bar(90, 395, "Whitened exact scalar", scalar, maximum, 410, "Exact chi-square law for p = 1")
    threshold_x = 90 + 410 / maximum
    pieces += [
        f'<line x1="{threshold_x:.2f}" y1="190" x2="{threshold_x:.2f}" y2="445" '
        'stroke="#f2cc60" stroke-width="3" stroke-dasharray="8 7"/>',
        _muted(threshold_x + 8, 458, "relative-error threshold = 1", 14),
    ]

    pieces += _panel(710, 145, 635, 330, "B. Temporal information exposed by whitening")
    degree_max = 120.0
    raw_width = 445 * raw_degrees / degree_max
    white_width = 445 * residual_degrees / degree_max
    pieces += [
        _muted(750, 215, "Raw projected normalization lower bound", 16),
        '<rect x="750" y="232" width="445" height="34" rx="8" fill="#202a35"/>',
        f'<rect x="750" y="232" width="{raw_width:.2f}" height="34" rx="8" fill="#8b949e"/>',
        _text(1215, 258, f"{raw_degrees:.2f}", 19, 650),
        _muted(750, 315, "Independent residual degrees after W then P_WH", 16),
        '<rect x="750" y="332" width="445" height="34" rx="8" fill="#202a35"/>',
        f'<rect x="750" y="332" width="{white_width:.2f}" height="34" rx="8" fill="#3fb950"/>',
        _text(1215, 358, str(residual_degrees), 19, 650),
        _muted(750, 415, "N = 120, nuisance rank q = 2, so N - q = 118", 16),
        _muted(750, 444, "Whitening changes coordinates. It does not create observations.", 16),
    ]

    pieces += _panel(55, 500, 635, 365, "C. 256 target visibility trials")
    median = float(trials["median_absolute_relative_error"])
    q95 = float(trials["q95_absolute_relative_error"])
    maximum_error = float(trials["maximum_absolute_relative_error"])
    coverage = float(trials["exact_interval_coverage_fraction"])
    invariance = float(trials["maximum_nuisance_invariance_error"])
    pieces += [
        _text(95, 570, f"Median absolute relative error   {median:.3f}", 20, 600),
        _text(95, 615, f"95th percentile                  {q95:.3f}", 20, 600),
        _text(95, 660, f"Maximum                           {maximum_error:.3f}", 20, 600),
        _text(95, 715, f"Exact interval coverage           {coverage * 100:.2f}%", 20, 600),
        _muted(95, 755, f"252 / 256 displayed trials inside the exact 97.5% interval", 16),
        _muted(95, 795, f"Maximum nuisance invariance error: {invariance:.2e}", 16),
        _muted(95, 830, "Trials illustrate scale. The theorem comes from the exact Wishart law.", 15),
    ]

    pieces += _panel(710, 500, 635, 365, "D. Physical inference pipeline")
    steps = [
        (750, 565, "temporally dependent target X"),
        (750, 625, "apply exact physical-time whitener W"),
        (750, 685, "transform nuisance design H to W H"),
        (750, 745, "project transformed nuisance modes"),
        (750, 805, f"{residual_degrees} iid Gaussian residual rows -> Wishart"),
    ]
    for index, (x, y, label) in enumerate(steps):
        pieces += [
            f'<rect x="{x}" y="{y - 32}" width="535" height="43" rx="10" '
            'fill="#16202a" stroke="#58a6ff" stroke-width="1.5"/>',
            _text(x + 18, y - 4, label, 17, 550),
        ]
        if index < len(steps) - 1:
            pieces += [
                f'<line x1="1018" y1="{y + 12}" x2="1018" y2="{y + 27}" '
                'stroke="#9da7b3" stroke-width="2"/>',
                f'<path d="M1012 {y + 22} L1018 {y + 29} L1024 {y + 22}" fill="none" '
                'stroke="#9da7b3" stroke-width="2"/>',
            ]

    pieces += [
        _muted(
            64,
            910,
            (
                "Scope: exact target temporal covariance is assumed known. "
                "Robust whitening under temporal uncertainty is a separate theorem."
            ),
            16,
        ),
        "</svg>",
    ]
    return "\n".join(pieces) + "\n"


def main() -> None:
    record = json.loads(DATA.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(record), encoding="utf-8")


if __name__ == "__main__":
    main()
