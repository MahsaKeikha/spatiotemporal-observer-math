import numpy as np

from examples.moving_world_tube_active_measurement import (
    N,
    TRUE_PATH,
    competitor_support,
    mean_for_support,
    choose_channel,
)


def test_planted_path_moves_one_coordinate_per_epoch():
    for a, b in zip(TRUE_PATH[:-1], TRUE_PATH[1:]):
        assert len(set(a).symmetric_difference(b)) == 2


def test_competitor_has_same_size_and_is_distinct():
    for support in TRUE_PATH:
        comp = competitor_support(support)
        assert len(comp) == len(support)
        assert comp != support


def test_predictive_sensor_lies_on_hypothesis_disagreement():
    rng = np.random.default_rng(1)
    for support in TRUE_PATH:
        comp = competitor_support(support)
        mu_p, mu_r = mean_for_support(support), mean_for_support(comp)
        j = choose_channel("predictive", mu_p, mu_r, rng)
        assert not np.isclose(mu_p[j], mu_r[j])


def test_fixed_sensor_becomes_uninformative_for_later_motion():
    rng = np.random.default_rng(1)
    support = TRUE_PATH[2]
    comp = competitor_support(support)
    mu_p, mu_r = mean_for_support(support), mean_for_support(comp)
    j = choose_channel("fixed", mu_p, mu_r, rng)
    assert j == 0
    assert np.isclose(mu_p[j], mu_r[j])
