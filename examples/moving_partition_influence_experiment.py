"""Demonstrate a finite influence cone across changing block partitions."""

from itertools import pairwise

import numpy as np

from observer_math import (
    moving_block_covariance_error_envelope,
    moving_block_joint_covariance_error_bound,
)


def main() -> None:
    block_counts = (4, 3, 4, 2, 3)
    transitions = [
        np.zeros((future, present))
        for present, future in pairwise(block_counts)
    ]
    transitions[1][3, 2] = 0.2
    transitions[2][1, 3] = 0.2
    transitions[3][0, 1] = 0.2

    forcings = [np.zeros((count, count)) for count in block_counts[1:]]
    forcings[0][2, 2] = 0.01
    perturbations = [np.zeros_like(matrix) for matrix in transitions]
    envelope = moving_block_covariance_error_envelope(
        transitions,
        forcings,
        perturbations,
    )

    print(f"Block counts by layer: {envelope.block_counts}")
    print("time  global state bound  observed joint bound")
    for time in range(envelope.time_count):
        local = moving_block_joint_covariance_error_bound(
            envelope,
            time,
            (0,),
            (0,),
        )
        print(
            f"{time:>4d}  "
            f"{envelope.global_state_error_bounds[time + 1]:>18.3e}  "
            f"{local:>20.3e}"
        )


if __name__ == "__main__":
    main()
