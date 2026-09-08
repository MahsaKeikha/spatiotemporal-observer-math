# Research overview

This page explains the project as a research story rather than as a list of files. For the complete numbered map of theorems and experiments, use the [research index](research_index.md).

The current verified record is 48 propositions, 34 reproducible experiments, 21 committed figures, and 156 passing claim-level tests across Python 3.10, 3.11, and 3.12.

## The question

Most dynamical analyses begin by deciding which variables belong to the system and which belong to its environment. This project asks whether that order can sometimes be reversed.

At time `t`, let a candidate subsystem be a coordinate set `S_t`. A changing candidate history is

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

which the repository calls an **observer world-tube**.

The central question is:

> **When can a moving subsystem path be distinguished from alternatives using internal predictive organization, environmental insulation, and continuity through time?**

The word "observer" is operational. It is not a claim about consciousness or subjective experience.

## The exact population model

The main exact theory uses a nonstationary linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

This setting makes adjacent covariances, Gaussian conditional mutual information, and canonical correlations analytically tractable. It allows the repository to separate three questions that are often mixed together:

1. what score should a candidate boundary receive?
2. which moving path maximizes the declared objective?
3. how much estimation or model error can occur before the winner changes?

## What the score measures

The implemented path objective combines four ideas:

- **integration**: predictive interaction across the candidate's weakest internal cut;
- **insulation**: how little predictive information must be imported from outside;
- **persistence**: survival of predictive structure into the next state;
- **transport**: continuity of organization even when physical membership changes.

A dynamic program computes the exact maximizing path in the declared candidate family. A second exact calculation finds the runner-up. Their difference is the action margin used by the robustness theorems.

## A controlled moving-boundary example

The planted path

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

is recovered at all five times in the controlled example.

| Quantity | Value |
| --- | ---: |
| Boundaries recovered | 5 / 5 |
| Winning action | 1.254324 |
| Runner-up action | 1.127903 |
| Action margin | 0.126421 |
| Certified uniform score radius | 0.010535 |

| Selected path | Failure region |
| --- | --- |
| [![Candidate scores over time](worldtube_baseline.png)](reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](worldtube_phase_diagram.png)](reproducible_results.md#regularization-result) |

The failure region is part of the scientific record. If material continuity is weighted too heavily, the optimizer leaves the planted moving process.

## Identifiability comes first

Optimization alone cannot establish an identifiable physical boundary. Propositions 13-14 formalize recovery only up to admissible symmetries and construct an observational equivalence case where incompatible labels cannot both be recovered with probability above one half in the stated maximin sense.

This sets the interpretation rule for the project:

> **Recovery is always relative to declared observables, model assumptions, and admissible symmetries.**

## How the proof program developed

The theorem sequence has five broad stages.

### Population mathematics

Propositions 1-8 establish covariance identities, information quantities, transport properties, path robustness logic, and covariance perturbation bounds.

### Finite-sample recovery

Proposition 9 gives the first complete Gaussian sample-complexity theorem. Later results localize covariance blocks, exploit positive factor floors, derive candidate-specific budgets, and propagate them through the path optimization problem.

### Structural compression

Propositions 15-31 use near-competitor graphs, overlap classes, block sparsity, influence cones, moving partitions, factor intervals, and screened environment structure. The goal is to make the certificate respect the same structural sparsity that makes the model interpretable.

### Statistically safe screening and drift

Propositions 32-40 add sample splitting, Gaussian screening guarantees, structural-null refinements, trajectory coupling, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

### Temporally dependent observations

Propositions 41-48 address the fact that time-series observations are not i.i.d. This is the current frontier.

## The recent sequence

### Proposition 41: temporal dependence changes effective sample size

[![Experiment AA](dependent_gaussian_calibration.png)](reproducible_results.md#experiment-aa-dependent-gaussian-covariance-calibration)

The covariance radius now depends on temporal Frobenius and spectral norms rather than treating record length as an i.i.d. sample count.

### Proposition 42: mean removal changes normalization

[![Experiment AB](dependent_centered_gaussian_calibration.png)](reproducible_results.md#experiment-ab-mean-centered-dependent-gaussian-calibration)

Under temporal dependence, removing an unknown constant mean changes the quadratic form and its exact normalization.

### Proposition 43: estimate the AR(1) coefficient

[![Experiment AC](estimated_ar1_calibration.png)](reproducible_results.md#experiment-ac-same-record-ar1-estimation-and-centered-covariance-calibration)

Increment energy produces an observable confidence interval for a shared nonnegative AR(1) coefficient, and that uncertainty is propagated into the covariance certificate.

### Proposition 44: allow a time-varying nuisance mean

[![Experiment AD](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

A fixed declared temporal design `H` is projected away exactly. Experiment AD shows why this matters: the projected estimator stays near 0.14 median relative error while ordinary mean-centering reaches 121.76 under large affine drift.

### Proposition 45: combine temporal calibration with nuisance projection

[![Experiment AE](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

Observable AR(1) calibration and time-varying nuisance removal are combined in one finite-sample covariance bound. The estimator tracks the oracle closely, but the radius becomes conservative at stronger correlation.

### Proposition 46: use the actual nuisance geometry

[![Experiment AF](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

The rank-only normalization bound is replaced by a continuum certificate that uses the actual design. Experiment AF shows a regime where rank-only control becomes vacuous while the design-specific theorem remains finite.

### Proposition 47: use direct matrix concentration

[![Experiment AG](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

The sphere-net operator-norm reduction is replaced by an exact Gaussian matrix exponential moment and a matrix-Laplace bound. At `N=850`, the tested radius falls from 1.077 to 0.459 at `phi=0.65`, and from 1.630 to 0.653 at `phi=0.80`.

### Proposition 48: make the matrix result uniform over estimated dependence

[![Experiment AH](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

Proposition 48 removes the known-spectrum requirement from Proposition 47 inside the current stationary nonnegative AR(1) model class. Proposition 46 controls the spectral movement of `P R_phi P` between AR(1) grid points. Weyl's inequality turns that matrix movement into a bound on every ordered projected temporal eigenvalue. The exact Proposition 47 matrix-mgf factors are monotone in those nonnegative eigenvalues, so an inflated neighboring grid spectrum gives a valid continuum matrix bound.

Experiment AH fixes `N=500` and compares the older sphere-net interval certificate with the new interval-uniform matrix certificate. For the strong-dependence interval `[0.70, 0.80]`, the radius falls from 2.409 to 0.931. The exact coefficient is not supplied to Proposition 48.

The experiment also contains two seeded target-record checks with a large unknown affine mean. All recorded errors remain below the stated Proposition 48 radii. Those simulations illustrate scale and implementation behavior. The proof is the continuum eigenvalue and matrix-mgf argument.

## What the project has established

Under the stated assumptions, the repository now provides a conditional mathematical pipeline from nonstationary Gaussian dynamics to moving-boundary optimization and finite-sample recovery certification. Its most developed statistical layer handles temporal dependence, unknown constant or declared time-varying nuisance means, estimated nonnegative AR(1) dependence, design-specific nuisance geometry, direct matrix concentration, and interval-uniform control of the full projected temporal eigenvalue profile.

Within that model class, the covariance certificate no longer requires the exact projected temporal spectrum to be supplied as an oracle input.

## What remains open

The current results still assume important structure. The newest statistical theorems rely on Gaussianity, temporal and spatial separability, stationary nonnegative AR(1) dependence for the calibrated interval layer, valid standardized calibration channels, and a nuisance design fixed before inspecting the target record.

The next statistical question is broader than Proposition 48:

> **Can the interval-uniform matrix concentration strategy be extended beyond a single AR(1) coefficient to a richer stationary dependence class without losing finite-sample auditability?**

Natural directions are a multi-parameter temporal family, a certified spectral-density envelope, or a nonparametric dependence class with a valid operator-norm matrix concentration theorem. A separate frontier is careful sample splitting for adaptive nuisance structure or data-driven whitening.
