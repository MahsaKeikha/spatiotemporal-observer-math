import numpy as np

from examples.gaussian_screen_calibration import population_problem
from examples.multi_regime_coupled_calibration import (
    parameterized_moving_module_systems,
    regime_grid,
    regime_problem,
    run_regime,
)


def test_baseline_parameterized_system_reproduces_original_problem():
    planted, systems = parameterized_moving_module_systems(
        base_memory=0.32,
        active_memory=0.46,
        internal_coupling=0.18,
        noise_condition=1.0,
    )
    rebuilt, _, _, _, declared = regime_problem(0.32, 0.46, 0.18, 1.0)
    original = population_problem()

    assert planted == tuple(original["candidates"][:5])
    assert declared == (0, 1, 2, 3, 4)
    assert all(
        np.allclose(left, right)
        for left, right in zip(rebuilt["joints"], original["joints"], strict=True)
    )
    assert all(np.allclose(noise, 0.18 * np.eye(7)) for _, noise in systems)


def test_declared_regime_grid_has_three_independent_axes():
    grid = regime_grid()

    assert len(grid) == 18
    assert len({record[0] for record in grid}) == 3
    assert len({record[3] for record in grid}) == 3
    assert len({record[4] for record in grid}) == 2


def test_small_regime_run_is_reproducible_and_well_formed():
    task = ("baseline", 0.32, 0.46, 0.18, 1.0, 80_000, [11, 12, 13])
    first = run_regime(task)
    second = run_regime(task)

    assert first == second
    assert first["trial_count"] == 3
    assert first["population_action_margin"] > 0.0
    assert first["structural_null_state_count"] == 28
    assert 0.0 <= first["null_score_covered_rate"] <= 1.0
    assert 0.0 <= first["mean_null_retained_edge_fraction"] <= 1.0
