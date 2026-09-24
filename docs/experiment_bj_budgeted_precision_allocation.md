# Experiment BJ: canonical budgeted multi-block precision allocation

BJ extends the canonical BI single-block audit to joint precision allocation. It asks whether selecting several uncertainty blocks by their individual BI ranking remains effective after the complete certificate pipeline is rerun jointly, or whether interaction changes the best allocation.

The experiment uses the 12 candidate-time blocks with the largest BI path-count reductions at covariance radius 0.0001. Each intervention has one unit of nominal design cost. For budgets one, two, and three, BJ compares:

1. the exact P80 optimum over the screened 12-block library;
2. greedy selection with marginal effects recomputed after every choice;
3. static selection from the original BI single-block ranking.

Every allocation is evaluated by rerunning the same covariance-to-world-tube certificate and certified ambiguity graph used by BI. The experiment also reports the interaction gain

\[
G(S)-\sum_{i\in S}G(\{i\}),
\]

where \(G(S)\) is the reduction in retained complete paths produced by the joint allocation. A nonzero value demonstrates that single-block gains are not simply additive over that allocation.

## Numerical result

The exact restricted budget-one solution reproduces BI's strongest block, `t1:c34`, and removes 1,484,350 retained paths.

At budget two, the exact restricted solution selects `t1:c31` and `t1:c34`. It removes 2,636,725 paths and 87 edges. Recomputed greedy selection finds the same pair. Static BI ranking instead selects `t1:c34` and `t2:c14`, removing 2,633,400 paths and 85 edges. The exact restricted joint rerun therefore improves on static ranking by 3,325 paths and two edges.

At budget three, exact restricted, recomputed greedy, and static ranking converge on the same three blocks: `t1:c31`, `t1:c34`, and `t2:c14`. The joint allocation removes 3,742,900 paths and 123 edges, reducing the baseline ambiguity by 7.173 percent. Unique recovery is still not achieved.

The selected exact allocations have interaction gains of 0, -4,620, and -90,370 paths at budgets one, two, and three. The negative values show diminishing joint returns relative to adding the corresponding single-block BI gains. This directly justifies joint pipeline reruns: single-block sensitivities are useful for screening but are not additive allocation coefficients.

## Scope

The exact label applies only to the screened 12-block library, unit nominal costs, and budgets one to three. BJ is not a global search over all 175 canonical candidate-time blocks. Unit cost is a controlled design convention, not a measurement of money, power, acquisition time, calibration burden, or hardware feasibility.

Run:

```bash
python examples/canonical_budgeted_precision_allocation.py
```

Machine-readable output and deterministic figure:

- `docs/canonical_budgeted_precision_allocation.json`
- `docs/canonical_budgeted_precision_allocation.svg`
