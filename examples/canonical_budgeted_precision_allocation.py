"""Experiment BJ: budgeted multi-block precision allocation on canonical BI data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if __package__ in (None, ""):
    sys.path.insert(0, str(ROOT))

from examples.canonical_design_sensitivity import evaluate, population_problem
from observer_math.budgeted_precision_allocation import exact_budgeted_allocation

BI_RECORD = ROOT / "docs" / "canonical_design_sensitivity.json"
OUTPUT = ROOT / "docs" / "canonical_budgeted_precision_allocation.json"
FIGURE = ROOT / "docs" / "canonical_budgeted_precision_allocation.svg"
TARGET_RADIUS = 0.0001
POOL_SIZE = 12
MAX_BUDGET = 3


def block_id(time, candidate_index):
    return f"t{time}:c{candidate_index}"


def render(stages):
    width, height = 1200, 720
    left, right, top, bottom = 120, 60, 120, 110
    plot_width = width - left - right
    plot_height = height - top - bottom
    policies = (
        ("exact_restricted", "Exact restricted", "#0f766e"),
        ("greedy_recomputed", "Greedy recomputed", "#2563eb"),
        ("static_single_rank", "Static BI rank", "#d97706"),
    )
    maximum = max(stage[key]["path_reduction"] for stage in stages for key, _, _ in policies)
    maximum = maximum or 1
    elements = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" '
            'viewBox="0 0 1200 720" role="img" aria-labelledby="title description">'
        ),
        '<title id="title">Canonical budgeted precision allocation</title>',
        (
            '<desc id="description">Certified ambiguity reduction for exact restricted, '
            "greedy recomputed, and static single-block ranking policies at budgets one to three.</desc>"
        ),
        '<rect width="1200" height="720" rx="24" fill="#f8fafc"/>',
        (
            '<text x="60" y="52" font-family="system-ui,sans-serif" font-size="28" '
            'font-weight="700" fill="#0f172a">Budgeted canonical precision allocation</text>'
        ),
        (
            '<text x="60" y="82" font-family="system-ui,sans-serif" font-size="15" '
            'fill="#475569">Joint reruns expose interaction effects that single-block ranking cannot certify</text>'
        ),
    ]
    for tick in range(6):
        value = maximum * tick / 5
        y = top + plot_height * (1 - value / maximum)
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
    group_width = plot_width / len(stages)
    bar_width = 68
    for group_index, stage in enumerate(stages):
        center = left + group_width * (group_index + 0.5)
        for policy_index, (key, _label, color) in enumerate(policies):
            value = stage[key]["path_reduction"]
            bar_height = plot_height * value / maximum
            x = center + (policy_index - 1) * (bar_width + 14) - bar_width / 2
            y = top + plot_height - bar_height
            elements.append(
                f'<rect x="{x:.3f}" y="{y:.3f}" width="{bar_width}" height="{bar_height:.3f}" '
                f'rx="5" fill="{color}"/>'
            )
        elements.append(
            f'<text x="{center:.3f}" y="{height - bottom + 34}" text-anchor="middle" '
            'font-family="system-ui,sans-serif" font-size="15" font-weight="600" '
            f'fill="#334155">Budget {stage["budget"]}</text>'
        )
    for index, (_key, label, color) in enumerate(policies):
        x = 690 + index * 160
        elements.extend(
            [
                f'<rect x="{x}" y="48" width="13" height="13" rx="2" fill="{color}"/>',
                (
                    f'<text x="{x + 20}" y="59" font-family="system-ui,sans-serif" '
                    f'font-size="12" fill="#334155">{label}</text>'
                ),
            ]
        )
    elements.extend(
        [
            (
                f'<line x1="{left}" y1="{height - bottom}" x2="{width - right}" '
                f'y2="{height - bottom}" stroke="#334155" stroke-width="1.5"/>'
            ),
            (
                '<text x="30" y="360" text-anchor="middle" transform="rotate(-90 30 360)" '
                'font-family="system-ui,sans-serif" font-size="15" fill="#334155">'
                "Reduction in retained complete paths</text>"
            ),
            "</svg>",
        ]
    )
    FIGURE.write_text("\n".join(elements) + "\n", encoding="utf-8")


def main():
    bi = json.loads(BI_RECORD.read_text(encoding="utf-8"))
    baseline = bi["baseline"]
    single_rows = [row for row in bi["rows"] if row["radius"] == TARGET_RADIUS]
    single_rows.sort(
        key=lambda row: (
            -(baseline["retained_paths"] - row["retained_paths"]),
            -(baseline["retained_edges"] - row["retained_edges"]),
            row["time"],
            row["candidate_index"],
        )
    )
    pool_rows = single_rows[:POOL_SIZE]
    pool = {block_id(row["time"], row["candidate_index"]): row for row in pool_rows}
    costs = {identifier: 1.0 for identifier in pool}

    _planted, candidates, local_factors, transport_factors = population_problem()
    cache = {}

    def joint_outcome(selected):
        key = frozenset(selected)
        if key not in cache:
            delta_map = {
                (pool[identifier]["time"], pool[identifier]["candidate_index"]): TARGET_RADIUS
                for identifier in key
            }
            cache[key] = evaluate(local_factors, transport_factors, candidates, delta_map)
        return cache[key]

    def evaluator(selected):
        outcome = joint_outcome(selected)
        return outcome["retained_paths"], float(outcome["retained_edges"])

    stages = []
    for budget in range(1, MAX_BUDGET + 1):
        exact = exact_budgeted_allocation(
            costs,
            float(budget),
            evaluator,
            max_cardinality=budget,
        )
        static_ids = tuple(list(pool)[:budget])
        static_outcome = joint_outcome(static_ids)

        greedy_ids = []
        for _step in range(budget):
            remaining = [identifier for identifier in pool if identifier not in greedy_ids]
            selected = min(
                remaining,
                key=lambda identifier: (
                    joint_outcome((*greedy_ids, identifier))["retained_paths"],
                    joint_outcome((*greedy_ids, identifier))["retained_edges"],
                    identifier,
                ),
            )
            greedy_ids.append(selected)
        greedy_outcome = joint_outcome(greedy_ids)
        exact_outcome = joint_outcome(exact.intervention_ids)
        individual_gain_sum = sum(
            baseline["retained_paths"] - pool[identifier]["retained_paths"]
            for identifier in exact.intervention_ids
        )

        def policy_record(identifiers, outcome):
            return {
                "intervention_ids": list(identifiers),
                "retained_paths": outcome["retained_paths"],
                "retained_edges": outcome["retained_edges"],
                "path_reduction": baseline["retained_paths"] - outcome["retained_paths"],
                "edge_reduction": baseline["retained_edges"] - outcome["retained_edges"],
                "unique_recovery": outcome["unique_recovery"],
            }

        exact_record = policy_record(exact.intervention_ids, exact_outcome)
        exact_record["feasible_subsets_evaluated"] = exact.feasible_subsets_evaluated
        exact_record["sum_of_single_block_path_reductions"] = individual_gain_sum
        exact_record["interaction_gain"] = exact_record["path_reduction"] - individual_gain_sum
        stages.append(
            {
                "budget": budget,
                "exact_restricted": exact_record,
                "greedy_recomputed": policy_record(greedy_ids, greedy_outcome),
                "static_single_rank": policy_record(static_ids, static_outcome),
            }
        )

    record = {
        "experiment": "BJ",
        "title": "Canonical budgeted multi-block precision allocation",
        "baseline_radius": bi["baseline_radius"],
        "target_radius": TARGET_RADIUS,
        "baseline": baseline,
        "screened_library_size": POOL_SIZE,
        "screening_rule": "top BI single-block path reduction, then edge reduction",
        "pool": [
            {
                "intervention_id": identifier,
                "time": row["time"],
                "candidate_index": row["candidate_index"],
                "candidate": row["candidate"],
                "single_block_path_reduction": baseline["retained_paths"] - row["retained_paths"],
                "single_block_edge_reduction": baseline["retained_edges"] - row["retained_edges"],
            }
            for identifier, row in pool.items()
        ],
        "stages": stages,
        "joint_allocations_evaluated": len(cache),
        "scientific_boundary": (
            "BJ is exact only over the screened 12-block library with unit nominal costs and "
            "budgets one to three. It is not a global optimum over all 175 blocks and unit cost "
            "is not a hardware, acquisition-time, power, or monetary cost claim."
        ),
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    render(stages)
    print(json.dumps(record, indent=2))
    return record


if __name__ == "__main__":
    main()
