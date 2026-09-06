"""Compare fixed-subsystem scores on modular and correlation-only systems."""

from observer_math import (
    block_system,
    correlated_but_uncoupled_system,
    observer_metrics,
    rank_subsystems,
)


def print_metrics(label, metrics):
    print(f"\n{label}")
    print(f"  subset: {metrics.subset}")
    print(f"  static integration:   {metrics.static_integration_bits_per_node:.6f} bits/node")
    print(f"  directed integration: {metrics.directed_integration_bits_per_node:.6f} bits/node")
    print(f"  environmental leakage:{metrics.environmental_leakage_bits_per_node:.6f} bits/node")
    print(f"  predictive persistence: {metrics.persistence:.6f}")
    print(f"  observer score:          {metrics.observer_score:.6f}")


def main():
    transition, noise = block_system(external_coupling=0.005)
    print("Top candidate subsystems in a two-module process")
    for candidate in rank_subsystems(transition, noise, min_size=3, max_size=3)[:5]:
        print(candidate.rank, candidate.metrics.subset, f"{candidate.metrics.observer_score:.6f}")

    correlated_transition, correlated_noise = correlated_but_uncoupled_system()
    correlation_only = observer_metrics(
        correlated_transition, correlated_noise, tuple(range(4))
    )
    print_metrics("Correlation-only control", correlation_only)


if __name__ == "__main__":
    main()
