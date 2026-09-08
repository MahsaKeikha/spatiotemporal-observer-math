# Research overview

This page explains the project as a research story rather than as a file list. For the complete theorem and experiment map, use the [research index](research_index.md).

The current 0.39.0 research record contains 51 propositions, 37 reproducible experiments, 24 committed scientific figures, and 171 claim-level tests.

## The question

Most dynamical analyses begin by deciding which variables belong to the system and which belong to its environment. This project asks whether that order can sometimes be reversed.

At time `t`, let a candidate subsystem be a coordinate set `S_t`. A changing candidate history is

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

which the repository calls an **observer world-tube**.

The central question is:

> **When can a moving subsystem path be distinguished from alternatives using internal predictive organization, environmental insulation, persistence, and continuity through time?**

The word "observer" is operational. It is not a claim about consciousness or subjective experience.

## The population model

The main exact theory uses a nonstationary linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

This setting makes adjacent covariances, Gaussian conditional mutual information, and canonical correlations analytically tractable. It lets the research separate three questions:

1. what score should a candidate boundary receive?
2. which moving path maximizes the declared objective?
3. how much estimation or model error can occur before the winner changes?

The implemented path objective combines integration, insulation, persistence, and transport. A dynamic program computes the exact maximizing path in the declared candidate family. A second exact calculation finds the best competitor. Their difference is the action margin used by the robustness theorems.

## Identifiability comes first

Optimization does not create identifiability.

Propositions 13 and 14 formalize recovery only up to admissible symmetries and construct an observational equivalence case where incompatible labels cannot both be recovered from the stated observations with uniformly high success probability.

This sets a standing interpretation rule:

> **Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

That rule applies to every result in the repository and becomes even more important for any future consciousness interpretation.

## How the proof program developed

### Population mathematics

Propositions 1 through 8 establish covariance identities, information quantities, transport properties, path robustness logic, and covariance perturbation bounds.

### Finite-sample recovery

Proposition 9 gives the first complete Gaussian sample-complexity theorem. Later results localize covariance blocks, exploit positive factor floors, derive candidate-specific budgets, and propagate those budgets through path optimization.

### Structural compression

Propositions 15 through 31 use near-competitor graphs, overlap classes, block sparsity, covariance influence cones, moving partitions, factor intervals, and screened environmental structure.

### Statistically safe screening and drift

Propositions 32 through 40 add sample splitting, Gaussian screening guarantees, structural-null refinements, trajectory coupling, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

### Temporally dependent observations

Propositions 41 through 51 address temporal dependence, nuisance means, temporal-parameter uncertainty, direct matrix concentration, compact covariance families, and finite-sample temporal calibration.

---

# The recent sequence

## Proposition 41: temporal dependence changes effective sample size

The covariance radius begins to depend on temporal Frobenius and spectral norms rather than treating record length as an independent sample count.

## Proposition 42: removing the mean changes normalization

Under temporal dependence, removing an unknown constant mean changes the quadratic form and its exact normalization.

## Proposition 43: estimate a shared AR(1) coefficient

Increment energy produces an observable confidence interval for a shared nonnegative AR(1) coefficient, and that uncertainty is propagated into covariance calibration.

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

## Proposition 48: make the matrix bound uniform over unknown AR(1)

[![Experiment AH](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

The complete projected temporal eigenvalue profile is controlled between AR(1) grid points, allowing the matrix bound to survive coefficient uncertainty.

## Proposition 49: separate temporal-family geometry from probability

[![Experiment AI](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

Proposition 49 replaces the one-dimensional AR(1) continuum by a compact temporal covariance family represented by a certified deterministic finite cover. The cover controls projected eigenvalues and covariance normalization. The cover points do not consume a probability union bound because they are deterministic geometry used before the matrix probability argument is applied.

## Proposition 50: learn a two-parameter temporal family from data

[![Experiment AJ](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

For

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I,
\]

lag-1 and lag-2 increment energies yield finite-sample intervals for the lag correlations. Those intervals are mapped into a conservative parameter rectangle and then composed with Proposition 49 for an independent target record.

The theorem exploits the increment covariance spectrum itself, which is much better conditioned than a generic bound based on the raw persistent process.

## Proposition 51: build a joint continuum confidence set from the full likelihood

[![Experiment AK](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

Proposition 51 removes the rectangular lag-summary step. A fixed Helmert contrast first removes arbitrary constant means from the calibration channels. Let \(p_\theta\) be the exact residual Gaussian density and let \(q\) be a proper mixture density fixed before the data are observed. The pointwise e-value is

\[
e_\theta(Z)=\frac{q(Z)}{p_\theta(Z)}.
\]

If \(\theta\) is the true parameter,

\[
\mathbb E_\theta e_\theta(Z)=1.
\]

Therefore

\[
\mathcal C_\alpha(Z)
=
\{\theta:e_\theta(Z)<1/\alpha\}
\]

contains the true parameter with probability at least \(1-\alpha\).

The true parameter does not need to be one of the mixture support points. The probability statement is continuum valued and finite sample. There is no union bound over parameter values.

Experiment AK evaluates the exact pointwise function on a visualization grid. At 256 calibration channels, the displayed accepted points occupy about 6.76 percent of the declared grid and span a visibly tighter joint region than the Proposition 50 rectangle in the controlled example.

The plotted grid is not a certified outer cover of the continuum confidence set. The theorem applies between grid points as well. Turning the irregular confidence set into a certified adaptive outer cover is the next statistical theorem.

---

# What the project has established

Under the stated assumptions, the repository now provides a conditional mathematical pipeline from nonstationary Gaussian dynamics to moving-boundary optimization and finite-sample recovery certification.

Its most developed statistical layer can handle:

- temporally dependent Gaussian sampling;
- unknown constant or fixed-subspace nuisance means;
- estimated nonnegative AR(1) dependence;
- actual nuisance-design geometry;
- direct matrix concentration using the full temporal spectrum;
- compact multi-parameter temporal covariance families;
- independently calibrated two-parameter temporal uncertainty;
- a finite-sample joint continuum confidence set based on the complete residual likelihood.

## What remains open

The newest results still rely on explicit model assumptions, including Gaussian calibration, temporal-family correctness, and declared nuisance structure.

Proposition 51 solves the continuum confidence-set problem for the stated two-parameter family. It does not yet produce a certified finite outer cover that can be passed into Proposition 49 without losing coverage.

The immediate statistical target is therefore:

> **Construct a certified adaptive outer cover of the Proposition 51 e-value confidence set, then compose that random cover with Proposition 49 for an independent target record.**

A parallel statistical direction is to extend the same e-value principle beyond the AR(1) plus white-noise family toward richer covariance and spectral-density models.

The structural frontier runs in parallel:

> **Develop intervention-sensitive and representation-invariant observer quantities, together with impossibility theorems that state exactly what passive observations cannot identify.**

Any later consciousness interpretation must remain a separate bridge hypothesis under the [interpretation protocol](interpretation_protocol.md). It is not a hidden consequence of the observer notation.

## Why negative results matter

The project treats impossibility results, failed parameter regimes, conservative bounds, and counterexamples as part of the research record. A theorem that says what cannot be identified can be more informative than a broad positive claim because it tells us which additional observables or assumptions are mathematically necessary.
