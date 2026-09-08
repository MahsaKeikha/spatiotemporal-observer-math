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
| Runner-up action | 1.127903 |
| Exact action margin | 0.126421 |
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

The automated suite currently contains 83 tests. Continuous integration runs
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

Using the exact population action margin `0.126421`, confidence `0.95`, and the
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

At the localized threshold, the forward-backward near-competitor screen retains
`5 / 175` time-indexed candidate states and `4 / 4900` candidate edges. These are
exactly the states and edges of the certified path. The screen does not improve
the stated threshold by itself; it identifies the deterministic subgraph on
which a subsequent, separately justified concentration refinement can focus.

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

## Experiment E: symbolic moving-clique recovery

Command:

```bash
python examples/symbolic_recovery_experiment.py
```

The model uses \(\Sigma_0=I\), self-memory \(\alpha=0.2\), internal coupling
\(\beta=0.3\), two-node moving cliques, and
\(Q_t=I-A_tA_t^\mathsf T\). Transport and continuity weights are `0.02` and
`0.01`. The closed-form and exact calculations give:

| Quantity | Value |
| --- | ---: |
| Planted local score | 0.184140 |
| Symbolic action-margin lower bound | 0.130806 |
| Exact action margin | 0.175335 |
| Boundaries recovered | 3 / 3 |

The exact margin exceeds the symbolic lower bound, as required. This theorem is
specific to zero external off-diagonal coupling and covariance-preserving noise.
It establishes a parameter-level base case rather than a general modular-system
result.

![Symbolic recovery margin over self-memory and internal coupling](symbolic_recovery_region.png)

The black contour is the zero lower-bound boundary. Points above it satisfy the
sufficient condition for the fixed weights and one-node consecutive overlap;
points below it are uncertified, not proven failures. Gray marks parameters that
violate the covariance-preserving stability condition. The gold star is the
committed numerical example.

## Experiment F: robust symbolic recovery

Command:

```bash
python examples/perturbed_symbolic_recovery_experiment.py
```

This experiment perturbs every transition by a matrix of operator norm
\(\gamma=10^{-5}\) whose support crosses the planted boundary. It also perturbs
every process covariance by an anisotropic diagonal matrix of operator norm
\(\nu=10^{-6}\). Covariances are propagated from \(\Sigma_0=I\); unit covariance
is not imposed after the initial time.

| Quantity | Value |
| --- | ---: |
| Maximum transition perturbation norm | `1.000e-05` |
| Maximum noise perturbation norm | `1.000e-06` |
| Largest incorrect integration factor | `6.489e-12` |
| Largest incorrect local score | `0.000063` |
| Global incorrect-score upper bound | `0.007891` |
| Support-resolved incorrect-score upper bound | `0.001002` |
| A priori support-aware incorrect-score upper bound | `0.001096` |
| Overlap-class incorrect-score upper bound | `0.002357` |
| Global action-margin lower bound | `0.121550` |
| Support-resolved action-margin lower bound | `0.129801` |
| A priori support-aware action-margin lower bound | `0.129669` |
| Overlap-class action-margin lower bound | `0.127900` |
| Exact action margin | `0.175280` |
| Boundaries recovered | 3 / 3 |

Incorrect candidates have positive integration in the numerical model, as
allowed by Proposition 19. Proposition 20 restricts the covariance error to
each score's coordinates and uses time-specific edge penalties. Its upper
bound remains larger than the observed score, but reduces the gap without
changing the model or fitting a constant to the result.

Proposition 21 does not propagate the actual covariance. Its row-local forcing
recursion produces a margin only `0.000131` below the realized
support-resolved result. Eight additional dense perturbation sequences verify
that its state and candidate-joint radii contain the directly propagated
errors and that its score bounds cover every enumerated candidate.

Proposition 22 receives five arrays of norm budgets rather than the
perturbation matrices. In this example the complete family of ten candidates
compresses to the three overlap values \(q=0,1,2\). Its `0.127900` lower
margin is more conservative than the matrix-level a priori margin because each
class uses worst-case local budgets and the worst feasible preceding overlap.
The tests verify both that the integer occupancy rule is exact and that each
class bound contains every candidate-level Proposition 21 bound, including
across the eight dense perturbation sequences.

![Robust recovery margin over transition and noise perturbation radii](perturbed_recovery_region.png)

The black contour is the zero lower-bound boundary. The warm region is
certified by the sufficient action inequality; the cool region is uncertified.
The plot does not classify the cool region as a failure region. The gold star
marks the direct numerical check.

## Experiment G: block-sparse structural recovery

Command:

```bash
python examples/block_sparse_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Population size | `1,000` |
| Implicit five-node candidates | `8,250,291,250,200` |
| Overlap classes evaluated | `6` |
| Global transition perturbation bound | `4.000e-08` |
| Maximum incorrect-score upper bound | `0.000148` |
| Action-margin lower bound | `0.045031` |
| Sufficient condition | satisfied |

The input consists only of two-by-two tables of entry magnitudes and integer
row and column degrees. The transition envelope uses entry magnitude
`1e-8` and degree two in every block; the noise envelope uses `1e-9` and
degree two. No \(1000\times1000\) perturbation matrix is created. The example
is a deterministic theorem evaluation, not an empirical scalability benchmark
or evidence that a particular physical system satisfies these envelopes.

## Experiment H: localized influence cone

Command:

```bash
python examples/localized_influence_cone_experiment.py
```

| Time | Global state-error bound | Block-zero joint-error bound |
| ---: | ---: | ---: |
| 0 | `0.000e+00` | `0.000e+00` |
| 1 | `1.000e-02` | `0.000e+00` |
| 2 | `5.000e-04` | `0.000e+00` |
| 3 | `4.200e-05` | `0.000e+00` |
| 4 | `4.290e-06` | `0.000e+00` |
| 5 | `4.862e-07` | `0.000e+00` |
| 6 | `5.879e-08` | `0.000e+00` |
| 7 | `7.429e-09` | `1.000e-16` |

The transition comparison graph is a line with self coefficient `0.2` and
nearest-neighbor coefficient `0.1`. A covariance forcing of `0.01` is applied
only to block seven at time zero. Block zero is seven graph edges away. Its
local joint bound is therefore exactly zero until the time-seven calculation,
even though the global bound is positive from time one. The final small value
is the propagated bound, not a numerical zero threshold.

## Experiment I: moving-partition influence cone

Command:

```bash
python examples/moving_partition_influence_experiment.py
```

The block counts change as `4 -> 3 -> 4 -> 2 -> 3`. A forcing of `0.01` is
placed in block two of the first future layer. The only route to observed block
zero passes through block three, then block one, then block zero in consecutive
layers.

| Time | Global next-state bound | Observed joint bound |
| ---: | ---: | ---: |
| 0 | `1.000e-02` | `0.000e+00` |
| 1 | `4.000e-04` | `0.000e+00` |
| 2 | `1.600e-05` | `0.000e+00` |
| 3 | `6.400e-07` | `6.400e-07` |

The calculation uses four rectangular transition comparisons and never forms
a common refinement. The final equality is specific to this single-path
construction; Proposition 25 provides an upper bound in general.

## Experiment J: moving-partition recovery certificate

Command:

```bash
python examples/moving_partition_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Partition block counts | `2 -> 3 -> 4 -> 2` |
| Population path | `(0, 1, 0)` |
| Adversarial competitor | `(1, 1, 0)` |
| Population action margin | `0.935000` |
| Maximum covariance radius | `1.000e-10` |
| Maximum local-score error | `3.438e-09` |
| Maximum transport-score error | `2.236e-09` |
| Recovery slack | `0.935000` |
| Sufficient condition | satisfied |

Candidate zero splits into two future blocks at the first layer, both
candidates split into singleton blocks at the second layer, and each candidate
merges back to one block at the final layer. The example verifies the complete
calculation from rectangular covariance comparisons through score errors and
the adversarial path dynamic program. The deliberately separated factors make
this an implementation check of Proposition 26, not a boundary-tightness
experiment.

## Experiment K: class-compressed robust recovery

Command:

```bash
python examples/class_compressed_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Candidates per time | `8,250,291,250,200` |
| Overlap classes per time | `6` |
| Implicit paths | `38,224,903,791,340,352,895,816,928,931,546,866,094,388,102,127,330,000,320,000,000,000` |
| Adversarial class path | `(5, 5, 5, 5, 4)` |
| Planted action lower bound | `4.554664` |
| Competitor action upper bound | `4.023003` |
| Recovery slack | `0.531662` |
| Sufficient condition | satisfied |

The six classes are indexed by planted overlap \(q=0,\ldots,5\). Their exact
multiplicities are
\(\binom{5}{q}\binom{995}{5-q}\), which sum to the complete five-node
candidate count. The optimizer operates only on the class arrays and a binary
mismatch flag. Zero continuity lower bounds are used for competitor edges, so
the result does not rely on a favorable unproved geometric penalty. The
population factors are deliberately class-constant; this experiment tests the
scope of Proposition 27 rather than claiming that arbitrary systems possess
the required symmetry.

## Experiment L: heterogeneous interval-class recovery

Command:

```bash
python examples/heterogeneous_class_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Candidates per time | `8,250,291,250,200` |
| Maximum local factor interval width | `0.026` |
| Maximum transport factor interval width | `0.020` |
| Adversarial class path | `(5, 5, 5, 5, 4)` |
| Planted action lower bound | `4.513864` |
| Competitor action upper bound | `4.064802` |
| Recovery slack | `0.449062` |
| Sufficient condition | satisfied |

This calculation uses the same six overlap classes as Experiment K but assigns
nonzero factor intervals to every class and class pair. The local interval
width also varies with overlap. Separate covariance radii enlarge those boxes
before the local and transport geometric means are bounded. The positive slack
therefore holds uniformly over the declared within-class heterogeneity rather
than relying on exact equality of member factors. The example does not derive
the intervals from a generative matrix model; that remains a separate modeling
obligation.

## Experiment M: covariance-residual-derived class intervals

Command:

```bash
python examples/residual_derived_class_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Candidates per time | `8,250,291,250,200` |
| Maximum local covariance residual | `7.000e-06` |
| Maximum transport covariance residual | `4.000e-06` |
| Maximum derived local factor width | `0.002828` |
| Maximum derived transport factor width | `0.001616` |
| Adversarial class path | `(5, 5, 5, 5, 4)` |
| Planted action lower bound | `4.553926` |
| Competitor action upper bound | `4.023811` |
| Recovery slack | `0.530115` |
| Sufficient condition | satisfied |

Unlike Experiment L, this calculation does not specify factor widths. It
starts with representative factors and covariance residual radii. Proposition
29 converts the residuals to population factor intervals, adjusts the member
spectral envelopes, and then applies a separate observation covariance error.
The numerical result tests this complete composition. It remains conditional
on the stated covariance residuals covering every represented class member.

## Experiment N: block-structured residual class recovery

Command:

```bash
python examples/structured_residual_class_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Candidates per time | `8,250,291,250,200` |
| Maximum derived local covariance residual | `2.772e-07` |
| Maximum derived transport covariance residual | `2.772e-07` |
| Adversarial class path | `(0, 1, 1, 1, 1)` |
| Planted action lower bound | `4.554591` |
| Competitor action upper bound | `3.753083` |
| Recovery slack | `0.801508` |
| Sufficient condition | satisfied |

The calculation begins with two-by-two transition, forcing, and cross-error
comparison matrices. It propagates their blockwise covariance influence,
compresses the resulting joint comparisons onto two declared classes, derives
factor intervals, and evaluates the robust path dynamic program. No covariance
residual or factor interval is supplied directly. The two classes are a
singleton planted class and its complement, so the bound is deliberately
coarse but covers the complete fixed-size candidate count.

## Experiment O: screened-environment structural recovery

Command:

```bash
python examples/screened_environment_recovery_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Candidates per time | `8,250,291,250,200` |
| Full-environment residual radius | `6.250e-05` |
| Maximum screened local residual radius | `2.500e-08` |
| Omitted leakage bound | `0.002 bits/node` |
| Adversarial class path | `(0, 1, 1, 1, 1)` |
| Planted action lower bound | `4.552532` |
| Competitor action upper bound | `3.753008` |
| Recovery slack | `0.799524` |
| Sufficient condition | satisfied |

The third block carries a comparatively large but dynamically disconnected
forcing residual. The screened selections exclude that block from the local
covariance comparison, but the calculation does not declare it irrelevant for
free: every local and transport insulation lower bound is reduced using an
omitted conditional-leakage budget of `0.002 bits/node`. This is a controlled
test of Proposition 31, not an empirical procedure for learning the screen.

## Experiment P: independent sample-split confidence accounting

Command:

```bash
python examples/sample_split_screening_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Screening sample count | `2,000` |
| Retained covariance blocks | `25` |
| Unscreened covariance blocks | `10,000` |
| Minimum screened certification sample | `80,182` |
| Minimum unscreened certification sample | `107,350` |
| Covariance radius at threshold | `0.119999` |
| Maximum admissible radius | `0.120000` |
| Screening confidence | `0.975000` |
| Certification confidence | `0.975000` |
| Combined confidence | `0.950625` |
| Independent-split guarantee | satisfied |
| Same-data guarantee | refused |

The first-stage confidence and deterministic admissible radius are inputs, not
outputs learned by this experiment. The calculation demonstrates the valid
conditional union bound on an independent second split and the exact integer
sample threshold. It also records the more modest unscreened threshold, making
clear that reducing the block count improves a logarithmic concentration term
rather than changing the rate itself.

## Experiment Q: Gaussian-safe first-split screening

Command:

```bash
python examples/gaussian_safe_screen_experiment.py
```

| Quantity | Value |
| --- | ---: |
| Screening sample count | `1,000,000,000,000` |
| Screening confidence | `0.975000` |
| Maximum screening covariance radius | `0.000026` |
| Maximum screening local-score radius | `0.087184` |
| Maximum screening transport-score radius | `0.023409` |
| Complete states | `60` |
| Retained states | `5` |
| Complete edges | `576` |
| Retained edges | `4` |
| Screen center path | `(0, 1, 2, 3, 4)` |
| All perturbation blocks valid | yes |
| Safe-screen guarantee | satisfied |

The example closes the previously external first-stage premise: its confidence
and score budgets are derived from the screening sample count, fixed spectral
envelopes, and Proposition 33. The extremely large sample count is intentional
and should not be hidden. It shows how slowly the zero-safe cube-root local
score bound contracts, even in a strongly separated synthetic score table.
The experiment establishes logical completeness of the two-stage argument, not
practical sample efficiency. Obtaining comparable safety with materially fewer
observations is the next statistical target.

## Required next controls

- empirical coverage and sharpness of the Gaussian-safe near-competitor set
- random, shuffled, and adversarial moving-boundary nulls
- recovery curves over signal-to-noise ratio and coupling separation
- comparisons with fixed-boundary and dynamic-community baselines
- replication on independently designed generative systems
