from observer_math import (
    block_system,
    correlated_but_uncoupled_system,
    observer_metrics,
    rank_subsystems,
)


def test_metrics_are_bounded():
    transition, noise = block_system()
    result = observer_metrics(transition, noise, (0, 1, 2))
    assert 0.0 <= result.integration_strength <= 1.0
    assert 0.0 <= result.independence <= 1.0
    assert 0.0 <= result.persistence <= 1.0
    assert 0.0 <= result.observer_score <= 1.0


def test_static_correlation_is_not_mistaken_for_directed_integration():
    transition, noise = correlated_but_uncoupled_system()
    result = observer_metrics(transition, noise, (0, 1, 2, 3))
    assert result.static_integration_bits_per_node > 0.01
    assert result.directed_integration_bits_per_node < 1e-8
    assert result.observer_score < 1e-3


def test_true_module_ranks_above_mixed_subsets():
    transition, noise = block_system(external_coupling=0.005)
    candidates = rank_subsystems(transition, noise, min_size=3, max_size=3)
    top_subsets = {candidate.metrics.subset for candidate in candidates[:2]}
    assert top_subsets == {(0, 1, 2), (3, 4, 5)}
