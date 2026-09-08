# Research overview

This page explains the project as a research story rather than as a list of files. For the complete numbered map of theorems and experiments, use the [research index](research_index.md).

The current release record is 49 propositions, 35 reproducible experiments, 22 committed figures, and 161 claim-level tests, with the release candidate checked across Python 3.10, 3.11, and 3.12 before merge.

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

## The population model

The main exact theory uses a nonstationary linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

This setting makes adjacent covariances, Gaussian conditional mutual information, and canonical correlations analytically tractable. It allows the repository to separate three questions:

1. what score should a candidate boundary receive?
2. which moving path maximizes the declared objective?
3. how much estimation or model error can occur before the winner changes?

The implemented path objective combines integration, insulation, persistence, and transport. A dynamic program computes the exact maximizing path in the declared candidate family. A second exact calculation finds the runner-up. Their difference is the action margin used by the robustness theorems.

## Identifiability comes first

Optimization alone cannot establish an identifiable physical boundary. Propositions 13-14 formalize recovery only up to admissible symmetries and construct an observational equivalence case where incompatible labels cannot both be recovered with probability above one half in the stated maximin sense.

This sets the interpretation rule for the project:

> **Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

## How the proof program developed

### Population mathematics

Propositions 1-8 establish covariance identities, information quantities, transport properties, path robustness logic, and covariance perturbation bounds.

### Finite-sample recovery

Proposition 9 gives the first complete Gaussian sample-complexity theorem. Later results localize covariance blocks, exploit positive factor floors, derive candidate-specific budgets, and propagate them through path optimization.

### Structural compression

Propositions 15-31 use near-competitor graphs, overlap classes, block sparsity, influence cones, moving partitions, factor intervals, and screened environment structure.

### Statistically safe screening and drift

Propositions 32-40 add sample splitting, Gaussian screening guarantees, structural-null refinements, trajectory coupling, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

### Temporally dependent observations

Propositions 41-49 address the fact that time-series observations are not i.i.d. This is the current proof frontier.

---

# The recent sequence

## Proposition 41: temporal dependence changes effective sample size

The covariance radius begins to depend on temporal Frobenius and spectral norms rather than treating record length as an i.i.d. sample count.

## Proposition 42: mean removal changes normalization

Under temporal dependence, removing an unknown constant mean changes the quadratic form and its exact normalization.

## Proposition 43: estimate the AR(1) coefficient

Increment energy produces an observable confidence interval for a shared nonnegative AR(1) coefficient, and that uncertainty is propagated into the covariance certificate.

## Proposition 44: allow a time-varying nuisance mean

[![Experiment AD](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

A fixed declared temporal design `H` is projected away exactly. Experiment AD shows why this matters: the projected estimator remains stable while ordinary mean-centering fails under large affine drift.

## Proposition 45: combine temporal calibration with nuisance projection

[![Experiment AE](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

Observable AR(1) calibration and time-varying nuisance removal are combined in one finite-sample covariance bound.

## Proposition 46: use the actual nuisance geometry

[![Experiment AF](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

A rank-only normalization bound is replaced by a continuum certificate that uses the actual declared nuisance design.

## Proposition 47: use direct matrix concentration

[![Experiment AG](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

The sphere-net operator-norm reduction is replaced by an exact Gaussian matrix exponential moment and a matrix-Laplace bound.

## Proposition 48: make the direct matrix bound uniform over unknown AR(1)

[![Experiment AH](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

The complete projected eigenvalue profile is controlled between AR(1) grid points. The matrix bound therefore survives uncertainty in the coefficient itself.

## Proposition 49: separate temporal-family geometry from matrix probability

[![Experiment AI](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

Proposition 49 replaces the one-dimensional AR(1) continuum by an arbitrary compact temporal covariance family with a certified finite cover. The theorem requires two deterministic cover controls:

\[
\|U^\mathsf T(R-R_j)U\|_2\le\delta_\lambda
\]

and

\[
|\operatorname{tr}(P(R-R_j))|\le\delta_d.
\]

Weyl's inequality then controls every ordered projected eigenvalue, and the monotone exact Gaussian matrix-mgf factors produce one family-wide matrix Chernoff envelope.

The cover points do not consume a probability union bound. They are deterministic geometry used to build the mgf envelope before probability enters.

Experiment AI uses the two-parameter family

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I
\]

with `phi in [0.45, 0.72]` and `eta in [0, 0.05]`. At `N=400`, refining the deterministic product cover gives:

| Cover | Proposition 49 | Sphere-net family |
| --- | ---: | ---: |
| `5 x 3` | 1.104 | 3.002 |
| `9 x 5` | **0.957** | 2.572 |
| `17 x 9` | **0.891** | 2.358 |

The same temporal family crosses below the critical relative-error threshold one without changing sample count or confidence. Two seeded target regimes also produced 192 of 192 covariance errors below the final theorem radius. The simulations show scale; the proof is the deterministic cover plus the matrix-mgf argument.

---

# What the project has established

Under the stated assumptions, the repository now provides a conditional mathematical pipeline from nonstationary Gaussian dynamics to moving-boundary optimization and finite-sample recovery certification. Its most developed covariance layer can handle temporally dependent sampling, unknown fixed-subspace nuisance means, estimated AR(1) dependence, design-specific geometry, direct matrix concentration, and compact multi-parameter temporal covariance families supplied through deterministic covers.

## What remains open

The newest theorems still rely on Gaussian temporal-spatial separability, valid nuisance structure, and temporal-family information justified independently of the target covariance record.

Proposition 49 solves the concentration problem once a deterministic family cover is supplied. It does not yet solve how that broader family should be calibrated from data.

The immediate next statistical target is therefore:

> **Construct an observable finite-sample confidence set for a multi-parameter or nonparametric temporal covariance family, then compose its calibration failure probability with Proposition 49.**

That would extend the observable calibration logic of Proposition 43 from one AR(1) coefficient to a genuinely broader dependence class.
