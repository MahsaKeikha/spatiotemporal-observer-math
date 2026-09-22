import numpy as np
from examples.matched_budget_certification_benchmark import (
    BUDGET, PRESSURE, choose_channel, run_trial, structural_radius,
)

def test_structural_radius_contracts_with_measurements():
    zero = np.zeros(PRESSURE.size)
    one = np.ones(PRESSURE.size)
    assert structural_radius(one) < structural_radius(zero)

def test_all_policies_respect_same_budget_when_uncertified_or_finished():
    for policy in ("fixed", "random", "kl", "certificate", "joint"):
        result = run_trial(policy, 17)
        assert result["certified_at"] is None or 1 <= result["certified_at"] <= BUDGET

def test_equivalent_laws_never_cross_positive_evidence_gate():
    for policy in ("fixed", "random", "kl", "certificate", "joint"):
        result = run_trial(policy, 19, equivalent=True)
        assert not result["certified"]
        assert result["final_llr"] == 0.0

def test_certificate_policy_targets_largest_current_radius_reduction():
    counts = np.zeros(PRESSURE.size)
    selected = choose_channel("certificate", counts, np.random.default_rng(1))
    gains = PRESSURE / (1.0 + np.zeros_like(PRESSURE)) - PRESSURE / (
        1.0 + np.array([0.12, 0.10, 0.04, 0.03, 0.08, 0.02])
    )
    assert selected == int(np.argmax(gains))
