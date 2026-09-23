# Experiment BG: empirical precision-ambiguity-workload Pareto frontier

BG applies P73 to the canonical Research I moving-module benchmark using the same declared covariance-radius sweep as BD and BE.

For each uncertainty radius, the experiment recomputes the P58 score uncertainty, P70/P69 retained graph, P71 exact retained world-tube count, and retained-edge workload. It then evaluates P73 Pareto dominance.

The downstream evidence coordinate is intentionally held constant at 1.0. This isolates the physical precision-ambiguity-workload geometry and prevents a controlled downstream e-value from being mistaken for a measured benchmark result.

A point is marked nondominated only if no other tested uncertainty level is simultaneously no worse in covariance radius, retained world-tube count, and retained-edge workload, with a strict improvement in at least one coordinate.

BG does not create a scalar score and does not rank incomparable operating points.

Generator: `../examples/empirical_precision_ambiguity_frontier.py`. Machine-readable record: `empirical_precision_ambiguity_frontier.json`.
