"""Experiment BI: canonical benchmark precision-design sensitivity.

Uses the same population problem and certificate pipeline as Experiment BD.
The intervention variable is the simultaneous covariance-radius scale assigned
to one candidate-time block at a time. No sensor-cost or hardware claim is made.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from examples.full_benchmark_scalable_certification import population_problem
from observer_math.ambiguity_count import count_retained_paths
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
from observer_math.score_interval_graph import compress_score_interval_graph

OUTPUT = ROOT / "docs" / "canonical_design_sensitivity.json"
FIGURE = ROOT / "docs" / "canonical_design_sensitivity.svg"


def continuity_matrix(candidates):
    out = np.zeros((len(candidates), len(candidates)))
    for i, a in enumerate(candidates):
        for j, b in enumerate(candidates):
            out[i, j] = 1.0 - len(set(a) & set(b)) / len(set(a) | set(b))
    return out


def evaluate(local_factors, transport_factors, candidates, delta_map):
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    errors = np.full(local_scores.shape, 0.0005)
    for (t, j), radius in delta_map.items():
        errors[t, j] = radius
    bridge = relative_covariance_worldtube_recovery_bound(
        local_factors,
        transport_factors,
        candidates,
        7,
        3,
        covariance_relative_errors=errors,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    graph = compress_score_interval_graph(
        local_scores,
        bridge.local_score_errors,
        transport_scores,
        bridge.transport_score_errors,
        continuity_matrix(candidates),
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    return {
        "retained_paths": int(
            count_retained_paths(graph.retained_nodes, graph.retained_edges).total_paths
        ),
        "retained_nodes": int(np.sum(graph.retained_nodes)),
        "retained_edges": int(np.sum(graph.retained_edges)),
        "unique_recovery": bool(bridge.guarantees_population_path),
    }


def render(rows, baseline_paths):
    reductions = [baseline_paths - row["retained_paths"] for row in rows]
    width, height = 1200, 720
    left, right, top, bottom = 110, 50, 105, 105
    plot_width = width - left - right
    plot_height = height - top - bottom
    maximum = max(reductions) or 1

    def x_position(index):
        return left + plot_width * index / max(1, len(rows) - 1)

    def y_position(value):
        return top + plot_height * (1.0 - value / maximum)

    elements = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" '
            'viewBox="0 0 1200 720" role="img" aria-labelledby="title description">'
        ),
        '<title id="title">Canonical benchmark localized precision interventions</title>',
        (
            '<desc id="description">Reduction in retained complete paths for 350 single-block '
            "covariance-radius interventions.</desc>"
        ),
        '<rect width="1200" height="720" rx="24" fill="#f8fafc"/>',
        (
            '<text x="60" y="50" font-family="system-ui,sans-serif" font-size="28" '
            'font-weight="700" fill="#0f172a">Canonical precision sensitivity</text>'
        ),
        (
            '<text x="60" y="78" font-family="system-ui,sans-serif" font-size="15" '
            'fill="#475569">Single-block interventions on the canonical moving-module benchmark</text>'
        ),
    ]
    for tick in range(6):
        value = maximum * tick / 5
        y = y_position(value)
        elements.extend(
            [
                (
                    f'<line x1="{left}" y1="{y:.3f}" x2="{width - right}" y2="{y:.3f}" '
                    'stroke="#cbd5e1" stroke-width="1"/>'
                ),
                (
                    f'<text x="{left - 14}" y="{y + 5:.3f}" text-anchor="end" '
                    'font-family="system-ui,sans-serif" font-size="13" fill="#475569">'
                    f"{round(value):,}</text>"
                ),
            ]
        )
    for index, (row, reduction) in enumerate(zip(rows, reductions, strict=True)):
        color = "#0f766e" if row["radius"] == 0.0001 else "#2563eb"
        elements.append(
            f'<circle cx="{x_position(index):.3f}" cy="{y_position(reduction):.3f}" '
            f'r="3.2" fill="{color}" fill-opacity="0.78"/>'
        )
    elements.extend(
        [
            (
                f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" '
                'stroke="#334155" stroke-width="1.5"/>'
            ),
            (
                f'<line x1="{left}" y1="{height - bottom}" x2="{width - right}" '
                f'y2="{height - bottom}" stroke="#334155" stroke-width="1.5"/>'
            ),
            (
                f'<text x="{left + plot_width / 2:.3f}" y="{height - 48}" text-anchor="middle" '
                'font-family="system-ui,sans-serif" font-size="15" fill="#334155">'
                "Single-block intervention index</text>"
            ),
            (
                f'<text x="28" y="{top + plot_height / 2:.3f}" text-anchor="middle" '
                'transform="rotate(-90 28 360)" font-family="system-ui,sans-serif" '
                'font-size="15" fill="#334155">Reduction in retained complete paths</text>'
            ),
            '<circle cx="780" cy="52" r="5" fill="#2563eb"/>',
            (
                '<text x="794" y="57" font-family="system-ui,sans-serif" font-size="13" '
                'fill="#334155">radius 0.0002</text>'
            ),
            '<circle cx="940" cy="52" r="5" fill="#0f766e"/>',
            (
                '<text x="954" y="57" font-family="system-ui,sans-serif" font-size="13" '
                'fill="#334155">radius 0.0001</text>'
            ),
            "</svg>",
        ]
    )
    FIGURE.write_text("\n".join(elements) + "\n", encoding="utf-8")


def main():
    planted, candidates, local_factors, transport_factors = population_problem()
    baseline = evaluate(local_factors, transport_factors, candidates, {})
    candidate_radii = (0.0002, 0.0001)
    rows = []
    for t in range(len(planted)):
        for j, candidate in enumerate(candidates):
            for radius in candidate_radii:
                out = evaluate(local_factors, transport_factors, candidates, {(t, j): radius})
                rows.append(
                    {
                        "time": t,
                        "candidate_index": j,
                        "candidate": list(candidate),
                        "radius": radius,
                        **out,
                    }
                )
    best = min(rows, key=lambda r: (r["retained_paths"], r["retained_edges"], r["radius"]))
    record = {
        "experiment": "BI",
        "title": "Canonical moving-module single-block precision sensitivity",
        "baseline_radius": 0.0005,
        "baseline": baseline,
        "candidate_radii": list(candidate_radii),
        "interventions_evaluated": len(rows),
        "best_by_ambiguity_then_edges": best,
        "rows": rows,
        "scientific_boundary": (
            "BI is an in-silico certificate-design audit on the canonical population benchmark. "
            "A candidate-time covariance radius is a mathematical uncertainty block, not a physical "
            "sensor cost. The experiment tests whether localized precision can change the certified "
            "ambiguity graph before any hardware interpretation is made."
        ),
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    render(rows, baseline["retained_paths"])
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
