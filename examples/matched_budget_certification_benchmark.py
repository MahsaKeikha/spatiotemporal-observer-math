"""Matched-budget benchmark for certification-aware measurement.

This benchmark isolates the decision logic of the adaptive extension. Every
policy receives exactly the same number of scalar measurements. The synthetic
environment exposes both structural uncertainty radii and action-conditioned
Gaussian predictive laws, allowing separate and joint acquisition policies to
be compared without changing measurement budget.

This is a methodological benchmark, not a biological model.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from observer_math.active_measurement import gaussian_equal_variance_kl

SEED = 20260921
TRIALS = 400
BUDGET = 48
ALPHA = 0.01
THRESHOLD = float(np.log(1.0 / ALPHA))
CHANNELS = 6
TRUE_MARGIN = 0.62

# Initial contributions to E(p)+E(r). Each measurement of channel j contracts
# the uncertainty components it observes by the declared deterministic law.
PRESSURE = np.array([0.31, 0.27, 0.09, 0.06, 0.18, 0.05])
CONTRACTION = np.array([0.12, 0.10, 0.04, 0.03, 0.08, 0.02])

MU_P = np.array([0.70, 0.10, 0.55, 0.05, 0.35, 0.20])
MU_R = np.array([0.05, 0.10, 0.15, 0.05, 0.30, 0.20])
VAR = np.array([0.24, 0.18, 0.20, 0.18, 0.22, 0.20])

POLICIES = ("fixed", "random", "kl", "certificate", "joint")


def structural_radius(counts: np.ndarray) -> float:
    """Deterministic residual pairwise radius after channel allocations."""
    return float(np.sum(PRESSURE / (1.0 + CONTRACTION * counts)))


def channel_structural_gain(counts: np.ndarray) -> np.ndarray:
    before = PRESSURE / (1.0 + CONTRACTION * counts)
    after = PRESSURE / (1.0 + CONTRACTION * (counts + 1.0))
    return before - after


def choose_channel(policy: str, counts: np.ndarray, rng: np.random.Generator) -> int:
    kl = gaussian_equal_variance_kl(MU_P, MU_R, VAR)
    structural = channel_structural_gain(counts)
    if policy == "fixed":
        return 0
    if policy == "random":
        return int(rng.integers(CHANNELS))
    if policy == "kl":
        return int(np.argmax(kl))
    if policy == "certificate":
        return int(np.argmax(structural))
    if policy == "joint":
        # Normalize both objectives so neither units nor scale decides the
        # comparison. The minimum of the normalized utilities rewards actions
        # that simultaneously reduce structural and evidence deficits.
        s = structural / max(float(np.max(structural)), np.finfo(float).eps)
        k = kl / max(float(np.max(kl)), np.finfo(float).eps)
        return int(np.argmax(np.minimum(s, k)))
    raise ValueError(f"unknown policy: {policy}")


def run_trial(policy: str, seed: int, *, equivalent: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    counts = np.zeros(CHANNELS)
    llr = 0.0
    certified_at = None
    false_certification = False
    mu_r = MU_P if equivalent else MU_R
    for step in range(1, BUDGET + 1):
        if equivalent:
            # Preserve the same structural allocation policy but remove every
            # predictive distinction. No evidence-based singleton certificate
            # is then permitted.
            kl = gaussian_equal_variance_kl(MU_P, mu_r, VAR)
            if policy in ("kl", "joint") and np.allclose(kl, 0.0):
                channel = int(rng.integers(CHANNELS))
            else:
                channel = choose_channel(policy, counts, rng)
        else:
            channel = choose_channel(policy, counts, rng)
        y = rng.normal(MU_P[channel], np.sqrt(VAR[channel]))
        llr += (
            -0.5 * (y - MU_P[channel]) ** 2 / VAR[channel]
            + 0.5 * (y - mu_r[channel]) ** 2 / VAR[channel]
        )
        counts[channel] += 1
        structural_ok = TRUE_MARGIN > structural_radius(counts)
        evidence_ok = llr >= THRESHOLD
        if structural_ok and evidence_ok and certified_at is None:
            certified_at = step
    if equivalent and certified_at is not None:
        false_certification = True
    return {
        "certified": certified_at is not None,
        "certified_at": certified_at,
        "false_certification": false_certification,
        "final_structural_radius": structural_radius(counts),
        "final_llr": float(llr),
    }


def summarize(policy: str, *, equivalent: bool = False) -> dict:
    rows = [run_trial(policy, SEED + i, equivalent=equivalent) for i in range(TRIALS)]
    times = [r["certified_at"] for r in rows if r["certified_at"] is not None]
    return {
        "policy": policy,
        "equal_budget": BUDGET,
        "trials": TRIALS,
        "equivalent_control": equivalent,
        "certification_rate": float(np.mean([r["certified"] for r in rows])),
        "false_certification_rate": float(np.mean([r["false_certification"] for r in rows])),
        "median_time_to_certificate": None if not times else float(np.median(times)),
        "mean_final_structural_radius": float(np.mean([r["final_structural_radius"] for r in rows])),
        "mean_final_llr": float(np.mean([r["final_llr"] for r in rows])),
    }


def main():
    result = {
        "scope": "synthetic matched-budget certification benchmark; not a biological model",
        "policies": [summarize(p) for p in POLICIES],
        "observational_equivalence": [summarize(p, equivalent=True) for p in POLICIES],
    }
    out = Path("docs/matched_budget_certification_benchmark.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
