"""Render Experiment AS as a deterministic SVG figure."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs" / "observer_bridge_dimension_audit.json"
OUTPUT = ROOT / "docs" / "observer_bridge_dimension_audit.svg"


def _bar(
    x: float,
    y: float,
    width: float,
    value: float,
    maximum: float,
    label: str,
) -> str:
    scaled = min(width, width * value / maximum)
    return f"""
    <text x="{x:.1f}" y="{y - 8:.1f}" class="small">{label}</text>
    <rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="18" rx="4" class="track"/>
    <rect x="{x:.1f}" y="{y:.1f}" width="{scaled:.1f}" height="18" rx="4" class="bar"/>
    <text x="{x + width + 12:.1f}" y="{y + 14:.1f}" class="value">{value:.6f}</text>
    """


def build_svg(record: dict[str, object]) -> str:
    population = record["population_worldtube"]
    geometry = record["covariance_geometry"]
    oracle = record["exact_tau_innovation_oracle"]
    entry = record["dimension_entry_threshold"]
    bridge = record["current_end_to_end_bridge"]

    scalar = float(oracle["scalar_block_radius"])
    observer = float(oracle["observer_scale_radius"])
    action_margin = float(population["population_action_margin"])
    uniform_score = float(population["uniform_score_radius"])
    path_delta = float(bridge["maximum_uniform_relative_radius_certifying_population_path"])

    bars = "".join(
        (
            _bar(680, 170, 330, scalar, 2.0, "scalar exact-tau innovation"),
            _bar(680, 238, 330, observer, 2.0, "observer-scale exact-tau innovation"),
        )
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">
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
    .emph {{ font: 700 21px Arial, sans-serif; fill: #0f766e; }}
    .warn {{ font: 700 20px Arial, sans-serif; fill: #9a3412; }}
    .track {{ fill: #e7ecf3; }}
    .bar {{ fill: #4f6f9f; }}
    .threshold {{ stroke: #a11d2e; stroke-width: 2; stroke-dasharray: 5 4; }}
    .path {{ font: 700 14px Arial, sans-serif; fill: #172033; }}
    .arrow {{ stroke: #64748b; stroke-width: 2; marker-end: url(#arrow); }}
    .box {{ fill: #eef4fb; stroke: #94a3b8; stroke-width: 1; }}
  </style>
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#64748b"/>
    </marker>
  </defs>
  <rect width="1200" height="760" class="bg"/>
  <text x="60" y="48" class="title">Experiment AS | Observer-scale covariance-to-world-tube certification audit</text>
  <text x="60" y="74" class="subtitle">The scalar covariance bottleneck is closed; the observer-scale dimensional and structural bottleneck is now explicit.</text>

  <rect x="55" y="105" width="540" height="275" rx="12" class="panel"/>
  <text x="80" y="138" class="head">A. Return to the original moving-boundary problem</text>
  <rect x="82" y="178" width="82" height="42" rx="7" class="box"/>
  <rect x="184" y="178" width="82" height="42" rx="7" class="box"/>
  <rect x="286" y="178" width="82" height="42" rx="7" class="box"/>
  <rect x="388" y="178" width="82" height="42" rx="7" class="box"/>
  <rect x="490" y="178" width="82" height="42" rx="7" class="box"/>
  <text x="123" y="204" text-anchor="middle" class="path">012</text>
  <text x="225" y="204" text-anchor="middle" class="path">123</text>
  <text x="327" y="204" text-anchor="middle" class="path">234</text>
  <text x="429" y="204" text-anchor="middle" class="path">345</text>
  <text x="531" y="204" text-anchor="middle" class="path">456</text>
  <line x1="164" y1="199" x2="181" y2="199" class="arrow"/>
  <line x1="266" y1="199" x2="283" y2="199" class="arrow"/>
  <line x1="368" y1="199" x2="385" y2="199" class="arrow"/>
  <line x1="470" y1="199" x2="487" y2="199" class="arrow"/>
  <text x="82" y="258" class="body">Population action margin: {action_margin:.10f}</text>
  <text x="82" y="286" class="body">Exact runner-up uniform score radius: {uniform_score:.10f}</text>
  <text x="82" y="314" class="body">35 candidates x 5 times = {int(geometry['simultaneous_covariance_block_count'])} covariance blocks</text>
  <text x="82" y="342" class="body">Each observer block has dimension n + s = {int(geometry['maximum_required_block_dimension'])}</text>
  <text x="82" y="366" class="tiny">4,900 candidate edges reuse these same target-indexed covariance blocks.</text>

  <rect x="620" y="105" width="525" height="275" rx="12" class="panel"/>
  <text x="645" y="138" class="head">B. Scalar success does not imply observer-scale certification</text>
  {bars}
  <line x1="680" y1="311" x2="1010" y2="311" class="threshold"/>
  <text x="1022" y="315" class="tiny">relative radius = 1</text>
  <text x="680" y="346" class="warn">observer-scale epsilon = {observer:.4f} &gt; 1</text>
  <text x="680" y="367" class="tiny">Exact tau is supplied here: calibration uncertainty is not causing this failure.</text>

  <rect x="55" y="405" width="540" height="285" rx="12" class="panel"/>
  <text x="80" y="438" class="head">C. Where the current matrix theorem first enters delta &lt; 1</text>
  <text x="82" y="482" class="body">118 residual innovation degrees:</text>
  <text x="360" y="482" class="warn">epsilon = {observer:.6f}</text>
  <text x="82" y="522" class="body">345 residual innovation degrees:</text>
  <text x="360" y="522" class="value">epsilon = {float(entry['radius_one_step_below_threshold']):.9f}</text>
  <text x="82" y="562" class="body">346 residual innovation degrees:</text>
  <text x="360" y="562" class="emph">epsilon = {float(entry['radius_at_threshold']):.9f}</text>
  <text x="82" y="606" class="body">With nuisance rank 2, the entry point is N = {int(entry['corresponding_sample_count_at_nuisance_rank_two'])} target rows.</text>
  <text x="82" y="646" class="tiny">Crossing one only makes the relative perturbation layer admissible. It does not yet certify the path.</text>

  <rect x="620" y="405" width="525" height="285" rx="12" class="panel"/>
  <text x="645" y="438" class="head">D. The bridge identifies the next theorem frontier</text>
  <text x="650" y="485" class="body">Largest current uniform delta certifying the population path:</text>
  <text x="650" y="522" class="emph">delta = {path_delta:.3e}</text>
  <text x="650" y="565" class="body">Current unit-weight matrix bound at that delta:</text>
  <text x="650" y="602" class="warn">r = {int(bridge['current_matrix_chernoff_residual_degrees_at_that_radius']):,}</text>
  <text x="650" y="640" class="body">This is a conservatism diagnostic, not a physical sample requirement.</text>
  <text x="650" y="666" class="tiny">Next: factor-specific blocks, screen-first simultaneity reduction, candidate-local radii, direct score-margin concentration.</text>

  <text x="60" y="730" class="subtitle">Proposition 58 spends no new probability budget: a positive path slack inherits the confidence of the simultaneous covariance event.</text>
</svg>
"""


def main() -> None:
    record = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.write_text(build_svg(record), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
