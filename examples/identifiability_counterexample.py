"""Show non-identifiability in a fully exchangeable Gaussian process."""

from itertools import combinations

import numpy as np

from observer_math import (
    certify_worldtube,
    observer_metrics_from_covariances,
    transport_metrics,
    two_point_identifiability_bound,
)
from observer_math.gaussian import stationary_covariance, two_time_covariance


def main():
    node_count = 4
    transition = np.eye(node_count) * 0.5
    noise = np.eye(node_count) * 0.2
    present = stationary_covariance(transition, noise)
    joint = two_time_covariance(transition, noise)
    candidates = tuple(combinations(range(node_count), 2))
    local = np.array(
        [
            [
                observer_metrics_from_covariances(present, joint, candidate).observer_score
                for candidate in candidates
            ]
            for _ in range(2)
        ]
    )
    transport = np.empty((1, len(candidates), len(candidates)))
    for previous, source in enumerate(candidates):
        for current, target in enumerate(candidates):
            transport[0, previous, current] = transport_metrics(
                present, transition, noise, source, target
            ).transport_score

    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    impossibility = two_point_identifiability_bound(0.0)
    print("Selected representative:", certificate.result.path)
    print("Runner-up representative:", certificate.runner_up_path)
    print("Labeled-path action margin:", f"{certificate.action_margin:.6f}")
    print(
        "Two-model maximin ceiling under identical laws:",
        f"{impossibility.maximin_success_probability:.3f}",
    )


if __name__ == "__main__":
    main()
