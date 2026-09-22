"""Deterministic benchmark for competitor-directed adaptive measurement.

The benchmark isolates the measurement-selection mechanism. A true Gaussian
predictive hypothesis is compared with finite alternatives. Policies receive
the same one-channel budget at every step.

Run:
    python examples/adaptive_measurement_benchmark.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT_SEED = 20260921
N_TRIALS = 400
HORIZON = 80
ALPHA = 0.01
N_CHANNELS = 6

TRUE_MEAN = np.array([0.80, 0.15, 0.05, 0.00, 0.00, 0.00])
COMPETITOR_MEANS = np.array(
    [
        [0.00, 0.15, 0.05, 0.00, 0.00, 0.00],
        [0.80, 0.15, 0.05, 0.55, 0.00, 0.00],
        [0.80, -0.35, 0.05, 0.00, 0.00, 0.00],
    ]
)
PREDICTIVE_VAR = np.array([0.20, 0.10, 0.10, 0.15, 0.10, 0.10])
NOISE_VAR = np.array([0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
TOTAL_VAR = PREDICTIVE_VAR + NOISE_VAR


def channel_kl(mu_p: float, mu_r: float, var: float) -> float:
    return 0.5 * (mu_p - mu_r) ** 2 / var


def llr_gaussian_equal_variance(y: float, mu_p: float, mu_r: float, var: float) -> float:
    return ((y - mu_r) ** 2 - (y - mu_p) ** 2) / (2.0 * var)


def choose_hardest_competitor(evidence: np.ndarray, threshold: float) -> int:
    deficits = np.maximum(threshold - evidence, 0.0)
    return int(np.argmax(deficits))


def choose_predictive_channel(evidence: np.ndarray, threshold: float) -> int:
    r = choose_hardest_competitor(evidence, threshold)
    kls = np.array(
        [channel_kl(TRUE_MEAN[j], COMPETITOR_MEANS[r, j], TOTAL_VAR[j]) for j in range(N_CHANNELS)]
    )
    return int(np.argmax(kls))


def choose_disagreement_channel(evidence: np.ndarray, threshold: float) -> int:
    r = choose_hardest_competitor(evidence, threshold)
    diffs = np.abs(TRUE_MEAN - COMPETITOR_MEANS[r])
    return int(np.argmax(diffs))


def run_policy(policy: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    evidence = np.zeros(len(COMPETITOR_MEANS))
    threshold = np.log(len(COMPETITOR_MEANS) / ALPHA)
    crossing = None
    channel_counts = np.zeros(N_CHANNELS, dtype=int)

    for k in range(1, HORIZON + 1):
        if policy == "predictive":
            j = choose_predictive_channel(evidence, threshold)
        elif policy == "disagreement":
            j = choose_disagreement_channel(evidence, threshold)
        elif policy == "random":
            j = int(rng.integers(0, N_CHANNELS))
        elif policy == "fixed":
            j = 0
        else:
            raise ValueError(policy)

        channel_counts[j] += 1
        y = rng.normal(TRUE_MEAN[j], np.sqrt(TOTAL_VAR[j]))
        for i, mu_r in enumerate(COMPETITOR_MEANS):
            evidence[i] += llr_gaussian_equal_variance(
                y, TRUE_MEAN[j], mu_r[j], TOTAL_VAR[j]
            )

        if crossing is None and np.all(evidence >= threshold):
            crossing = k

    return {
        "certified": crossing is not None,
        "crossing_step": crossing,
        "final_min_evidence": float(np.min(evidence)),
        "channel_counts": channel_counts.tolist(),
    }


def run_equivalence_control(policy: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    evidence = 0.0
    max_abs_evidence = 0.0
    for _ in range(HORIZON):
        if policy == "random":
            j = int(rng.integers(0, N_CHANNELS))
        else:
            j = 0
        y = rng.normal(TRUE_MEAN[j], np.sqrt(TOTAL_VAR[j]))
        evidence += llr_gaussian_equal_variance(
            y, TRUE_MEAN[j], EQUIVALENT_COMPETITOR_MEAN[j], TOTAL_VAR[j]
        )
        max_abs_evidence = max(max_abs_evidence, abs(evidence))
    return {
        "final_evidence": float(evidence),
        "max_abs_evidence": float(max_abs_evidence),
        "correctly_unresolved": bool(max_abs_evidence == 0.0),
    }


def summarize_equivalence() -> dict:
    rows = [run_equivalence_control("random", ROOT_SEED + 10000 + i) for i in range(N_TRIALS)]
    return {
        "description": "Distinct structural label, identical observable predictive law.",
        "trials": N_TRIALS,
        "correctly_unresolved_rate": float(np.mean([r["correctly_unresolved"] for r in rows])),
        "max_abs_evidence_over_trials": float(max(r["max_abs_evidence"] for r in rows)),
    }


def summarize(policy: str) -> dict:
    rows = [run_policy(policy, ROOT_SEED + i) for i in range(N_TRIALS)]
    crossing = [r["crossing_step"] for r in rows if r["crossing_step"] is not None]
    counts = np.sum(np.array([r["channel_counts"] for r in rows]), axis=0)
    return {
        "policy": policy,
        "trials": N_TRIALS,
        "horizon": HORIZON,
        "certification_rate": float(np.mean([r["certified"] for r in rows])),
        "mean_crossing_step_given_certified": float(np.mean(crossing)) if crossing else None,
        "median_crossing_step_given_certified": float(np.median(crossing)) if crossing else None,
        "mean_final_min_evidence": float(np.mean([r["final_min_evidence"] for r in rows])),
        "aggregate_channel_counts": counts.tolist(),
    }


def main() -> None:
    results = {
        "seed_root": ROOT_SEED,
        "alpha": ALPHA,
        "threshold": float(np.log(len(COMPETITOR_MEANS) / ALPHA)),
        "one_channel_budget_per_step": True,
        "true_mean": TRUE_MEAN.tolist(),
        "competitor_means": COMPETITOR_MEANS.tolist(),
        "total_variance": TOTAL_VAR.tolist(),
        "policies": [summarize(p) for p in ("predictive", "disagreement", "random", "fixed")],
        "observational_equivalence_control": summarize_equivalence(),
        "interpretation": (
            "Synthetic mechanism benchmark only. Certification means all declared "
            "pairwise evidence thresholds were crossed under the specified Gaussian model."
        ),
    }
    out = Path(__file__).resolve().parents[1] / "docs" / "adaptive_measurement_benchmark.json"
    out.write_text(json.dumps(results, indent=2) + "
", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
