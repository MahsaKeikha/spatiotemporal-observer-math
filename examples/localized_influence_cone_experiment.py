"""Demonstrate finite-speed covariance influence on a line graph."""

import numpy as np

from observer_math import (
    block_covariance_error_envelope_from_perturbations,
    block_joint_covariance_error_bound,
)


def main():
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

    print("Remote forcing block:", block_count - 1)
    print("Observed block:", 0)
    print("Graph distance:", block_count - 1)
    print("time  global state bound  local joint bound")
    for time in range(time_count):
        local = block_joint_covariance_error_bound(envelope, time, (0,))
        print(
            f"{time:>4d}  "
            f"{envelope.global_state_error_bounds[time]:>18.3e}  "
            f"{local:>17.3e}"
        )


if __name__ == "__main__":
    main()
