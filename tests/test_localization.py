import numpy as np

from observer_math import (
    block_covariance_error_envelope_from_perturbations,
    block_joint_covariance_error_bound,
)


def _block_norm_comparison(matrix, groups):
    return np.array(
        [
            [
                np.linalg.norm(matrix[np.ix_(rows, columns)], ord=2)
                for columns in groups
            ]
            for rows in groups
        ]
    )


def test_block_covariance_envelope_covers_exact_matrix_recursion():
    rng = np.random.default_rng(141421)
    node_count = 6
    time_count = 4
    groups = ((0, 1), (2, 3, 4), (5,))
    base_transitions = []
    transition_errors = []
    noise_errors = []
    for _ in range(time_count):
        base_transitions.append(rng.normal(scale=0.04, size=(node_count, node_count)))
        transition_errors.append(
            rng.normal(scale=1e-3, size=(node_count, node_count))
        )
        noise = rng.normal(scale=2e-4, size=(node_count, node_count))
        noise_errors.append((noise + noise.T) / 2.0)

    base_comparisons = np.array(
        [_block_norm_comparison(matrix, groups) for matrix in base_transitions]
    )
    transition_comparisons = np.array(
        [_block_norm_comparison(matrix, groups) for matrix in transition_errors]
    )
    noise_comparisons = np.array(
        [_block_norm_comparison(matrix, groups) for matrix in noise_errors]
    )
    envelope = block_covariance_error_envelope_from_perturbations(
        base_comparisons,
        transition_comparisons,
        noise_comparisons,
    )

    exact_states = [np.zeros((node_count, node_count))]
    exact_crosses = []
    for base, error, noise in zip(
        base_transitions, transition_errors, noise_errors, strict=True
    ):
        transition = base + error
        forcing = base @ error.T + error @ base.T + error @ error.T + noise
        exact_crosses.append(transition @ exact_states[-1] + error)
        exact_states.append(
            transition @ exact_states[-1] @ transition.T + forcing
        )

    for time, state in enumerate(exact_states):
        assert np.linalg.norm(state, ord=2) <= (
            envelope.global_state_error_bounds[time] + 1e-14
        )
        for row_block, rows in enumerate(groups):
            for column_block, columns in enumerate(groups):
                assert np.linalg.norm(
                    state[np.ix_(rows, columns)], ord=2
                ) <= envelope.state_error_comparisons[time][
                    row_block, column_block
                ] + 1e-14
    present_blocks = (0, 2)
    future_blocks = (0,)
    present = groups[0] + groups[2]
    future = groups[0]
    for time in range(time_count):
        exact_joint_error = np.block(
            [
                [
                    exact_states[time][np.ix_(present, present)],
                    exact_crosses[time][np.ix_(future, present)].T,
                ],
                [
                    exact_crosses[time][np.ix_(future, present)],
                    exact_states[time + 1][np.ix_(future, future)],
                ],
            ]
        )
        assert np.linalg.norm(exact_joint_error, ord=2) <= (
            block_joint_covariance_error_bound(
                envelope, time, present_blocks, future_blocks
            )
            + 1e-14
        )


def test_block_covariance_envelope_has_finite_graph_influence_speed():
    block_count = 8
    time_count = 8
    base = np.zeros((time_count, block_count, block_count))
    for time in range(time_count):
        np.fill_diagonal(base[time], 0.2)
        for node in range(block_count - 1):
            base[time, node, node + 1] = 0.1
            base[time, node + 1, node] = 0.1
    transition_errors = np.zeros_like(base)
    noise_errors = np.zeros_like(base)
    noise_errors[0, -1, -1] = 0.01
    envelope = block_covariance_error_envelope_from_perturbations(
        base,
        transition_errors,
        noise_errors,
    )

    assert envelope.global_state_error_bounds[1] > 0.0
    assert all(
        block_joint_covariance_error_bound(envelope, time, (0,)) == 0.0
        for time in range(7)
    )
    assert block_joint_covariance_error_bound(envelope, 7, (0,)) > 0.0


def test_block_covariance_envelope_rejects_invalid_comparisons():
    base = np.zeros((2, 3, 3))
    transition_errors = np.zeros_like(base)
    noise_errors = np.zeros_like(base)
    transition_errors[0, 0, 0] = -1.0

    with np.testing.assert_raises_regex(ValueError, "finite and nonnegative"):
        block_covariance_error_envelope_from_perturbations(
            base,
            transition_errors,
            noise_errors,
        )
