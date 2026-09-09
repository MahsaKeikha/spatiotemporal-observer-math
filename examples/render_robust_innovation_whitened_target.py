"""Render Experiment AR as a deterministic SVG figure."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "robust_innovation_whitened_target.json"
OUTPUT = ROOT / "docs" / "robust_innovation_whitened_target.svg"


def _bar(x: float, y: float, width: float, value: float, maximum: float, label: str) -> str:
    scaled = width * value / maximum
    return f"""
    <text x="{x:.1f}" y="{y - 8:.1f}" class="small">{label}</text>
    <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="18" rx="4" class="track"/>
    <rect x="{x:.1f}" y="{y:.1f}" width="{scaled:.1f}" height="18" rx="4" class="bar"/>
    <text x="{x + width + 12:.1f}" y="{y + 14:.1f}" class="value">{value:.5f}</text>
    """


def build_svg(record: dict[str, object]) -> str:
    cal = record["calibration_input"]
    model = record["target_model"]
    cover = record["certified_transformed_family_cover"]
    cert = record["uniform_target_certificate"]
    comp = record["comparison"]
    points = record["pointwise_diagnostics"]

    lower = float(cal["retained_lower_seconds"])
    upper = float(cal["retained_upper_seconds"])
    working = float(model["working_relaxation_time_seconds"])
    true_tau = float(model["true_relaxation_time_seconds_for_visibility"])
    eps = float(cert["covariance_relative_error"])

    x0, x1 = 90.0, 530.0
    tau_min, tau_max = 0.65, 0.88
    map_tau = lambda tau: x0 + (tau - tau_min) / (tau_max - tau_min) * (x1 - x0)

    bars = "".join(
        [
            _bar(690, 166, 330, float(comp["proposition_55_raw_time_calibrated_radius"]), 2.5, "P55 raw-time calibrated"),
            _bar(690, 226, 330, float(comp["proposition_56_exact_tau_innovation_radius"]), 2.5, "P56 exact-tau innovation"),
            _bar(690, 286, 330, float(comp["proposition_57_uncertain_tau_innovation_radius"]), 2.5, "P57 calibrated-tau robust"),
        ]
    )

    point_x = [690, 805, 920, 1035]
    diagnostics = ""
    max_radius = 0.65
    for x, row in zip(point_x, points):
        tau = float(row["true_relaxation_time_seconds"])
        radius = float(row["pointwise_relative_radius"])
        h = 122.0 * radius / max_radius
        diagnostics += f"""
        <rect x="{x:.1f}" y="{610 - h:.1f}" width="54" height="{h:.1f}" rx="5" class="bar2"/>
        <text x="{x + 27:.1f}" y="628" text-anchor="middle" class="tiny">{tau:.3f}s</text>
        <text x="{x + 27:.1f}" y="{595 - h:.1f}" text-anchor="middle" class="tiny">{radius:.3f}</text>
        """

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720">
  <style>
    .bg {{ fill: #ffffff; }}
    .panel {{ fill: #f8fafc; stroke: #d7dee8; stroke-width: 1.2; }}
    .title {{ font: 700 27px Arial, sans-serif; fill: #172033; }}
    .subtitle {{ font: 400 14px Arial, sans-serif; fill: #526075; }}
    .head {{ font: 700 17px Arial, sans-serif; fill: #172033; }}
    .body {{ font: 400 13px Arial, sans-serif; fill: #39475a; }}
    .small {{ font: 600 12px Arial, sans-serif; fill: #39475a; }}
    .tiny {{ font: 600 10px Arial, sans-serif; fill: #526075; }}
    .value {{ font: 700 12px Arial, sans-serif; fill: #172033; }}
    .axis {{ stroke: #738096; stroke-width: 2; }}
    .interval {{ stroke: #2563eb; stroke-width: 13; stroke-linecap: round; }}
    .working {{ stroke: #0f766e; stroke-width: 3; }}
    .truth {{ stroke: #b45309; stroke-width: 3; stroke-dasharray: 6 5; }}
    .track {{ fill: #e7ecf3; }}
    .bar {{ fill: #4f6f9f; }}
    .bar2 {{ fill: #7c8fae; }}
    .threshold {{ stroke: #a11d2e; stroke-width: 2; stroke-dasharray: 5 4; }}
    .emph {{ font: 700 23px Arial, sans-serif; fill: #0f766e; }}
    .eq {{ font: 600 15px Arial, sans-serif; fill: #172033; }}
  </style>
  <rect width="1200" height="720" class="bg"/>
  <text x="60" y="48" class="title">Experiment AR | Robust innovation whitening under calibrated physical-time uncertainty</text>
  <text x="60" y="74" class="subtitle">One working whitener, one finite-sample tau interval, one uniform target covariance certificate</text>

  <rect x="55" y="105" width="530" height="250" rx="12" class="panel"/>
  <text x="80" y="137" class="head">A. Calibration determines the admissible physical timescale</text>
  <line x1="{x0}" y1="224" x2="{x1}" y2="224" class="axis"/>
  <line x1="{map_tau(lower):.1f}" y1="224" x2="{map_tau(upper):.1f}" y2="224" class="interval"/>
  <line x1="{map_tau(working):.1f}" y1="188" x2="{map_tau(working):.1f}" y2="260" class="working"/>
  <line x1="{map_tau(true_tau):.1f}" y1="188" x2="{map_tau(true_tau):.1f}" y2="260" class="truth"/>
  <text x="{map_tau(lower):.1f}" y="278" text-anchor="middle" class="small">{lower:.6f}s</text>
  <text x="{map_tau(upper):.1f}" y="278" text-anchor="middle" class="small">{upper:.7f}s</text>
  <text x="{map_tau(working):.1f}" y="179" text-anchor="middle" class="small">working tau = {working:.8f}s</text>
  <text x="{map_tau(true_tau):.1f}" y="296" text-anchor="middle" class="small">true tau = {true_tau:.2f}s</text>
  <text x="80" y="329" class="body">Proposition 55 confidence: 0.975 | hull width: {float(cal['retained_width_seconds']):.7f}s</text>

  <rect x="615" y="105" width="530" height="250" rx="12" class="panel"/>
  <text x="640" y="137" class="head">B. The uncertain-tau target theorem stays below radius one</text>
  {bars}
  <line x1="690" y1="331" x2="1020" y2="331" class="threshold"/>
  <text x="1032" y="335" class="tiny">epsilon = 1 threshold</text>
  <text x="690" y="348" class="body">P57 reduction from P55 calibrated raw time: {100.0 * float(comp['reduction_from_raw_time_calibrated_fraction']):.1f}%</text>

  <rect x="55" y="380" width="530" height="280" rx="12" class="panel"/>
  <text x="80" y="412" class="head">C. Certified transformed temporal geometry</text>
  <text x="85" y="455" class="eq">C_tau = W0 R_tau W0^T</text>
  <text x="85" y="490" class="body">||W0||2 = {float(cover['whitening_operator_norm']):.5f}</text>
  <text x="85" y="518" class="body">transformed Lipschitz bound = {float(cover['transformed_operator_lipschitz_bound_per_second']):.3f} s^-1</text>
  <text x="85" y="546" class="body">eigenvalue cover radius = {float(cover['transformed_eigenvalue_covering_radius']):.6f}</text>
  <text x="85" y="574" class="body">projected normalization range = [{float(cert['projected_degrees_of_freedom_lower_bound']):.3f}, {float(cert['projected_degrees_of_freedom_upper_bound']):.3f}]</text>
  <text x="85" y="602" class="body">reference normalization = {float(cert['covariance_normalization']):.3f}</text>
  <text x="85" y="638" class="emph">uniform epsilon = {eps:.5f} &lt; 1</text>

  <rect x="615" y="380" width="530" height="280" rx="12" class="panel"/>
  <text x="640" y="412" class="head">D. Pointwise diagnostics show where the uniform bound is conservative</text>
  <line x1="670" y1="610" x2="1110" y2="610" class="axis"/>
  {diagnostics}
  <text x="640" y="652" class="body">Pointwise radii are diagnostics only. The theorem uses the complete continuum certificate.</text>

  <text x="60" y="699" class="subtitle">Combined calibration-target confidence lower bound: {float(model['combined_calibration_target_confidence']):.6f} | Conditional on the declared separable Gaussian one-timescale exponential model.</text>
</svg>
"""


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(build_svg(record), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
