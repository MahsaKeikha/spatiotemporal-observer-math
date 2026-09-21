import numpy as np

from examples.adaptive_measurement_benchmark import (
    TOTAL_VAR,
    TRUE_MEAN,
    COMPETITOR_MEANS,
    channel_kl,
    choose_predictive_channel,
    llr_gaussian_equal_variance,
)


def test_channel_kl_nonnegative_and_zero_for_equal_means():
    assert channel_kl(1.0, 1.0, 0.5) == 0.0
    assert channel_kl(1.0, 0.0, 0.5) > 0.0


def test_llr_expectation_matches_kl_by_direct_formula():
    mu_p, mu_r, var = 0.8, 0.0, 0.25
    expected = channel_kl(mu_p, mu_r, var)
    # E[(Y-r)^2-(Y-p)^2]/(2v) under Y~N(p,v)
    direct = ((var + (mu_p - mu_r) ** 2) - var) / (2 * var)
    assert np.isclose(expected, direct)


def test_predictive_policy_targets_hardest_competitor_best_channel():
    threshold = 10.0
    evidence = np.zeros(len(COMPETITOR_MEANS))
    j = choose_predictive_channel(evidence, threshold)
    r = 0
    kls = [
        channel_kl(TRUE_MEAN[k], COMPETITOR_MEANS[r, k], TOTAL_VAR[k])
        for k in range(len(TRUE_MEAN))
    ]
    assert j == int(np.argmax(kls))
