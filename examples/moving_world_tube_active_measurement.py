"""Moving world-tube active-measurement benchmark.

A planted three-coordinate module translates across seven coordinates. At each
epoch the true structural hypothesis and its strongest one-step-shifted
competitor induce different Gaussian predictive means. Every policy receives
the same one-channel measurement budget.

This benchmark tests whether a sensing policy can follow a changing
disagreement support rather than exploiting one permanently informative sensor.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

SEED = 20260921
N = 7
MODULE_SIZE = 3
EPOCHS = 5
STEPS_PER_EPOCH = 24
TRIALS = 300
ALPHA = 0.01
PREDICTIVE_VAR = 0.18
NOISE_VAR = np.array([0.04, 0.05, 0.07, 0.04, 0.08, 0.05, 0.06])
TOTAL_VAR = PREDICTIVE_VAR + NOISE_VAR
ACTIVE_LEVEL = 0.70
BACKGROUND_LEVEL = 0.05

TRUE_PATH = [
    (0, 1, 2),
    (1, 2, 3),
    (2, 3, 4),
    (3, 4, 5),
    (4, 5, 6),
]


def mean_for_support(support: tuple[int, ...]) -> np.ndarray:
    mu = np.full(N, BACKGROUND_LEVEL)
    mu[list(support)] = ACTIVE_LEVEL
    return mu


def competitor_support(true_support: tuple[int, ...]) -> tuple[int, ...]:
    """Return a nearby same-size support that differs at the moving edge."""
    lo, hi = min(true_support), max(true_support)
    if hi + 1 < N:
        return tuple(range(lo + 1, hi + 2))
    return tuple(range(lo - 1, hi))


def kl_channel(mu_p: np.ndarray, mu_r: np.ndarray, j: int) -> float:
    return 0.5 * (mu_p[j] - mu_r[j]) ** 2 / TOTAL_VAR[j]


def llr(y: float, mu_p: float, mu_r: float, var: float) -> float:
    return ((y - mu_r) ** 2 - (y - mu_p) ** 2) / (2.0 * var)


def choose_channel(policy: str, mu_p: np.ndarray, mu_r: np.ndarray, rng: np.random.Generator) -> int:
    if policy == "predictive":
        return int(np.argmax([kl_channel(mu_p, mu_r, j) for j in range(N)]))
    if policy == "disagreement":
        return int(np.argmax(np.abs(mu_p - mu_r)))
    if policy == "random":
        return int(rng.integers(0, N))
    if policy == "fixed":
        return 0
    raise ValueError(policy)


def run_trial(policy: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    threshold = float(np.log(1.0 / ALPHA))
    epoch_rows = []
    total_counts = np.zeros(N, dtype=int)

    for epoch, support in enumerate(TRUE_PATH):
        comp = competitor_support(support)
        mu_p, mu_r = mean_for_support(support), mean_for_support(comp)
        evidence = 0.0
        crossing = None
        counts = np.zeros(N, dtype=int)

        for step in range(1, STEPS_PER_EPOCH + 1):
            j = choose_channel(policy, mu_p, mu_r, rng)
            counts[j] += 1
            total_counts[j] += 1
            y = rng.normal(mu_p[j], np.sqrt(TOTAL_VAR[j]))
            evidence += llr(y, mu_p[j], mu_r[j], TOTAL_VAR[j])
            if crossing is None and evidence >= threshold:
                crossing = step

        epoch_rows.append(
            {
                "epoch": epoch,
                "true_support": list(support),
                "competitor_support": list(comp),
                "certified": crossing is not None,
                "crossing_step": crossing,
                "final_evidence": float(evidence),
                "channel_counts": counts.tolist(),
            }
        )

    return {
        "all_epochs_certified": all(r["certified"] for r in epoch_rows),
        "certified_epochs": sum(r["certified"] for r in epoch_rows),
        "epoch_rows": epoch_rows,
        "channel_counts": total_counts.tolist(),
    }


def summarize(policy: str) -> dict:
    rows = [run_trial(policy, SEED + i) for i in range(TRIALS)]
    crossings = [
        e["crossing_step"]
        for r in rows
        for e in r["epoch_rows"]
        if e["crossing_step"] is not None
    ]
    return {
        "policy": policy,
        "trials": TRIALS,
        "all_epochs_certified_rate": float(np.mean([r["all_epochs_certified"] for r in rows])),
        "mean_certified_epochs": float(np.mean([r["certified_epochs"] for r in rows])),
        "mean_crossing_step_given_certified": float(np.mean(crossings)) if crossings else None,
        "aggregate_channel_counts": np.sum(
            np.array([r["channel_counts"] for r in rows]), axis=0
        ).tolist(),
    }


def main() -> None:
    results = {
        "seed_root": SEED,
        "true_path": [list(s) for s in TRUE_PATH],
        "equal_budget": "one channel per measurement step",
        "alpha": ALPHA,
        "steps_per_epoch": STEPS_PER_EPOCH,
        "policies": [summarize(p) for p in ("predictive", "disagreement", "random", "fixed")],
        "scope": (
            "Synthetic moving-support mechanism benchmark. The predictive laws "
            "are deliberately simple and do not constitute a biological model."
        ),
    }
    out = Path(__file__).resolve().parents[1] / "docs" / "moving_world_tube_active_measurement.json"
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
