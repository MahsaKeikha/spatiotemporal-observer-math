# Reproducible results

This page records numerical outputs generated from committed code. It is an
experiment log, not evidence for phenomenal consciousness or a claim of a
complete observer theory.

## Experiment A: fixed modular structure

Command:

```bash
python examples/baseline_experiment.py
```

For two planted three-node modules, the two highest-ranked candidates are the
two planted modules. Both receive observer score `0.237050`.

In the correlated-but-dynamically-uncoupled control:

| Quantity | Value |
| --- | ---: |
| Static integration | 0.102050 bits/node |
| Directed integration | 0.000000 bits/node |
| Predictive persistence | 0.422500 |
| Observer score | 0.000000 |

The control demonstrates a narrow but important property: static correlation
alone does not create a positive score under the implemented directed criterion.

## Experiment B: changing-boundary world-tube

Command:

```bash
python examples/worldtube_experiment.py
```

The planted and recovered paths are identical:

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

![Local candidate scores with the selected path outlined](worldtube_baseline.png)

The heat map contains local scores. The cyan outline comes from the complete
world-tube action, which also includes transport and continuity terms.

| Quantity | Value |
| --- | ---: |
| Boundaries recovered | 5 / 5 |
| Winning action | 1.254324 |
| Runner-up action | 1.127902 |
| Exact action margin | 0.126422 |
| Certified uniform score radius | 0.010535 |
| Componentwise sufficient condition | Not satisfied |
| Minimum componentwise margin | -0.046147 |

The radius means that if every local score and every raw transport score changes
by less than `0.010535` in absolute value, the inferred path is guaranteed not
to change under the assumptions of Proposition 4. This is a deterministic
score-space guarantee, not yet a sampling-error confidence interval.

The negative componentwise margin does not contradict recovery. Proposition 5
is deliberately sufficient but not necessary: it requires the planted path to
win every edge separately, whereas the global action can recover a path through
tradeoffs accumulated across several times.

## Regularization result

The generated phase diagram scans transport and material-continuity weights.
It exposes both the recovery region and a failure region where an excessive
preference for retaining the same physical members overwhelms the moving
organization.

![Regularization phase diagram](worldtube_phase_diagram.png)

## Reproduce validation

```bash
python -m pip install -e ".[dev,viz]"
python -m pytest
python -m ruff check .
python examples/baseline_experiment.py
python examples/worldtube_experiment.py
```

The automated suite currently contains 29 tests. Continuous integration runs
the tests and lint checks on Python 3.10, 3.11, and 3.12.

## Experiment C: finite-sample recovery

Command used for the committed result:

```bash
python examples/finite_sample_benchmark.py --trials 32 --jobs 6
```

Each trial draws a fresh ensemble of independent trajectories through the same
nonstationary system. Adjacent covariances are estimated from paired samples
with scale-relative ridge `1e-5`. Neither the analytical covariance nor the true
transition matrix is supplied to the distributional world-tube method.

![Finite-sample benchmark](finite_sample_benchmark.png)

For the distributional world-tube:

| Trajectories | Mean boundary accuracy | Standard error | Exact path recovery | Wilson 95% interval |
| ---: | ---: | ---: | ---: | ---: |
| 20 | 0.094 | 0.022 | 0.000 | [0.000, 0.107] |
| 40 | 0.313 | 0.038 | 0.000 | [0.000, 0.107] |
| 80 | 0.706 | 0.048 | 0.313 | [0.180, 0.486] |
| 160 | 0.944 | 0.018 | 0.750 | [0.579, 0.867] |
| 320 | 0.988 | 0.009 | 0.938 | [0.799, 0.983] |
| 640 | 1.000 | 0.000 | 1.000 | [0.893, 1.000] |

The curve is consistent with convergence toward the population solution on
this model. Thirty-two trials per point are enough to expose the transition but
not enough for a precise tail estimate.

### Internal baseline comparison

At 160 trajectories:

| Procedure | Mean boundary accuracy | Exact path recovery |
| --- | ---: | ---: |
| Distributional world-tube | 0.944 | 0.750 |
| Independent local choices | 0.994 | 0.969 |
| Local score plus continuity | 0.975 | 0.875 |
| Coefficient-based transport | 0.894 | 0.594 |
| Best fixed boundary | 0.194 | 0.000 |

This benchmark does not show an advantage for the full transport objective.
Independent local choices and local score plus continuity perform better at
intermediate sample sizes. The fixed-boundary baseline cannot follow the moving
module and reaches its maximum possible accuracy of one boundary out of five.

The comparison identifies a design requirement for the next benchmark: local
evidence must be ambiguous while cross-time organizational transport remains
informative. Otherwise the transport term adds estimation variance to a problem
that local scoring already solves.

The raw aggregated values, Wilson intervals, trial count, ridge, sample sizes,
and root seed are stored in [`finite_sample_results.json`](finite_sample_results.json).

## End-to-end theoretical guarantee

The five population adjacent covariances have the eigenvalue envelope

\[
m=0.085512,
\qquad
M=1.125000,
\qquad
M/m\approx13.156.
\]

Using the exact population action margin `0.126422`, confidence `0.95`, and the
worst-case bound of Proposition 9, 640 samples do not certify path recovery. The
smallest certified ensemble size returned by the bound is approximately

\[
N_{\mathrm{sufficient}}=1.263\times10^{19}.
\]

This is a mathematically sufficient number, not an estimate of the practical
sample requirement. The simulation recovered 30 of 32 complete paths at 320
samples and 32 of 32 at 640. The gap of roughly seventeen orders of magnitude
comes from several deliberately worst-case steps:

1. spectral control of the complete 14-dimensional covariance
2. a union bound over all five time-indexed covariances
3. dependence on the global minimum eigenvalue
4. uniform control of every candidate, partition, and edge
5. cube-root Hölder continuity when a score factor can approach zero

The localized certificate of Propositions 10 through 12 uses the
\((n+s)\)-dimensional covariance block associated with each target candidate,
positive factor floors where they are available, and an exact dynamic program
for the strongest error-inflated competing path. Its sufficient count is

\[
N_{\mathrm{localized}}=3.132\times10^{12}.
\]

This is approximately four million times smaller than the global result. It is
still roughly ten orders of magnitude above the empirical recovery scale, so it
should not be interpreted as a practical sample-size estimate.

The rate calculation in Proposition 9 makes the main penalty explicit. In the
absence of positive score-factor floors, the local-score error decays at the
worst-case rate \(N^{-1/6}\), producing sixth-power dependence on the inverse
path margin. Positive floors would make the product roots locally Lipschitz and
can reduce that margin dependence from \(q^{-6}\) to \(q^{-2}\). This is the
specific mathematical lever for the next refinement.

## Experiment D: exchangeable non-identifiability

Command:

```bash
python examples/identifiability_counterexample.py
```

The process has \(A=0.5I\) and \(Q=0.2I\), so every node permutation preserves
its complete trajectory law. Distinct constant two-node paths have equal
action, and the exact labeled-path margin is zero. If two interpretations of
this same law designate paths in disjoint symmetry orbits, Proposition 14 caps
the maximin success probability of every observational estimator at `0.500`.
This is a constructed impossibility example, not a claim about biological data.

## Required next controls

- concentration over a provably sufficient near-competitor set
- random, shuffled, and adversarial moving-boundary nulls
- recovery curves over signal-to-noise ratio and coupling separation
- comparisons with fixed-boundary and dynamic-community baselines
- replication on independently designed generative systems
