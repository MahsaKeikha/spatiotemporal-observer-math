# Experiment BG: empirical precision-ambiguity-workload Pareto frontier

BG applies P73 to the canonical Research I moving-module benchmark using the same declared covariance-radius sweep as BD and BE.

For each uncertainty radius, the experiment recomputes the P58 score uncertainty, P70/P69 retained graph, P71 exact retained world-tube count, and retained-edge workload. It then evaluates P73 Pareto dominance.

The downstream evidence coordinate is intentionally held constant at 1.0. This isolates the physical precision-ambiguity-workload geometry and prevents a controlled downstream e-value from being mistaken for a measured benchmark result.

A point is marked nondominated only if no other tested uncertainty level is simultaneously no worse in covariance radius, retained world-tube count, and retained-edge workload, with a strict improvement in at least one coordinate.

BG does not create a scalar score and does not rank incomparable operating points.

Generator: `../examples/empirical_precision_ambiguity_frontier.py`. Machine-readable record: `empirical_precision_ambiguity_frontier.json`.

## Reproduced result

The canonical CI run shows a pronounced transition rather than a smooth reduction. For covariance radii from 0.05 through 0.001, all 52,521,875 complete world-tubes remain and all 4,900 layered transitions remain. At 0.0005 the count decreases only slightly to 52,178,875 with 4,892 retained edges. At 0.0002 it collapses to 720 paths and 126 edges. At 0.0001 only 2 complete paths and 5 edges remain.

P58's stronger unique-recovery certificate is still false at every tested point, including 0.0001. Thus graph-level ambiguity compression can become extremely sharp before the sufficient unique-recovery condition is met. This is an observed property of this controlled population benchmark and declared uncertainty sweep, not a general sample-complexity law.
