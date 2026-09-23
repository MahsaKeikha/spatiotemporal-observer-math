# Experiment BH: targeted precision design versus naive policies

BH is a controlled policy experiment for P78 and P79. It asks whether a decision-aware precision intervention can identify a binding uncertainty block that a naive largest-uncertainty rule misses.

Three uncertainty blocks have declared precision menus. B1 begins with the largest radius, but B0 is constructed as the decision-binding block. The full declared evaluator is rerun for every design point.

The targeted P79 policy searches each block's achievable grid and selects the feasible intervention with the smallest absolute radius reduction. It is compared with:

1. largest-uncertainty-first selection;
2. a uniform policy that reduces every block radius to 25 percent of baseline.

The experiment is deliberately controlled. Its purpose is to test the design-policy logic and negative control, not to claim a real sensor cost advantage. A hardware study must replace normalized radius reduction with measured acquisition cost, power, latency, calibration burden, or monetary cost.

Run:

python examples/design_policy_comparison.py

Machine-readable output:

docs/design_policy_comparison.json
