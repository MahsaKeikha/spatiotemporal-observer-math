# Research overview

This page explains the project as a research story rather than as a list of files. For the complete numbered map of theorems and experiments, use the [research index](research_index.md).

The current release candidate contains 50 propositions, 36 reproducible experiments, 23 committed scientific figures, and 166 claim-level tests. The exact release head has passed the repository test and lint workflow on Python 3.10, 3.11, and 3.12.

## The question

Most dynamical analyses begin by deciding which variables belong to the system and which belong to its environment. This project asks whether that order can sometimes be reversed.

At time `t`, let a candidate subsystem be a coordinate set `S_t`. A changing candidate history is

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

which the repository calls an **observer world-tube**.

The central question is:

> **When can a moving subsystem path be distinguished from alternatives using internal predictive organization, environmental insulation, and continuity through time?**

The word "observer" is operational. It is not a claim about consciousness or subjective experience. The repository now also includes an [observer-to-consciousness interpretation protocol](observer_consciousness_interpretation_protocol.md) that states what additional bridge assumptions would have to be justified before the observer mathematics could support a consciousness interpretation.

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

Negative results are part of the mathematical program. A proof that a boundary cannot be identified from a declared observation model is as important as a positive recovery theorem, because it states where additional information or assumptions are necessary.

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

Propositions 41-50 address the fact that time-series observations are not i.i.d. The sequence now progresses from known temporal covariance to observable two-parameter temporal-family calibration.

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

Proposition 49 replaces the one-dimensional AR(1) continuum by an arbitrary compact temporal covariance family with a certified finite cover. If every admissible compressed temporal covariance is close to one cover point in operator norm and projected normalization, Weyl's inequality controls every ordered projected eigenvalue. The exact Gaussian matrix-mgf factors then produce one family-wide matrix Chernoff envelope.

The cover points do not consume a probability union bound. They are deterministic geometry used before the probability inequality is applied.

Experiment AI uses

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I
\]

with `phi in [0.45, 0.72]` and `eta in [0, 0.05]`. At `N=400`, the displayed Proposition 49 radius moves from `1.104` on a `5 x 3` cover to `0.891` on a `17 x 9` cover, while the corresponding sphere-net family radius remains `2.358`.

## Proposition 50: calibrate the two-parameter temporal family from data

[![Experiment AJ](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

Proposition 50 makes the two-parameter family observable under a stated calibration model. Independent standardized Gaussian calibration channels supply lag-1 and lag-2 increment energies. Their population lag correlations are

\[
r_1=(1-\eta)\phi,
\qquad
r_2=(1-\eta)\phi^2.
\]

Whenever the relevant denominators stay away from zero, these relations imply

\[
\phi=\frac{r_2}{r_1},
\qquad
1-\eta=\frac{r_1^2}{r_2}.
\]

The theorem does not treat those identities as plug-in estimates without error control. It first constructs simultaneous finite-sample intervals for the two lag correlations, propagates them through the nonlinear parameter map into a valid `(phi, eta)` rectangle, then conditions on that calibration event and invokes Proposition 49. Calibration and covariance failure probabilities are combined explicitly.

The concentration step is sharpened by analyzing the filtered increment process rather than applying a generic temporal spectral norm to the raw process. For lag 1, the persistent AR(1) level-spectrum penalty cancels and the relevant spectral peak is controlled by

\[
4\frac{1-\phi}{1+\phi}.
\]

For lag 2, the corresponding bound is

\[
4(1-\phi^2).
\]

This is useful because stronger persistence can make the raw process more strongly correlated while the differenced statistic used for calibration becomes better conditioned.

Experiment AJ holds the target sample count, nuisance design, spatial dimension, and covariance confidence fixed. Carrying the entire declared temporal family gives a matrix radius near `1.142`. Independent calibration contracts the final family certificate to approximately `1.055` with 32 channels, `0.871` with 64, `0.814` with 128, and `0.772` with 256.

The experiment also exposes the remaining limitation: at these calibration sizes, the white-noise-fraction interval remains substantially prior-limited. Most of the useful contraction comes from learning `phi`. The next statistical refinement should therefore attack the joint parameter geometry directly rather than treating the two lag-correlation intervals as an axis-aligned rectangle.

---

# What the project has established

Under the stated assumptions, the repository provides a conditional mathematical pipeline from nonstationary Gaussian dynamics to moving-boundary optimization and finite-sample recovery certification. Its most developed covariance layer can now account for temporally dependent sampling, unknown fixed-subspace nuisance means, estimated temporal dependence, design-specific geometry, direct matrix concentration, compact multi-parameter temporal covariance families, and an observable finite-sample calibration of one explicit two-parameter family.

That is a statement about the mathematics inside the declared model class. It is not evidence that those assumptions hold for every physical system, and it is not a proof of consciousness.

## A disciplined path toward consciousness-related mathematics

The project can still ask a deeper question without weakening its scientific standard. The [interpretation protocol](observer_consciousness_interpretation_protocol.md) treats a consciousness interpretation as a separate bridge problem. It lists conditions that would need independent justification, including representation invariance, observational identifiability, causal or interventional discriminability, temporal identity, counterfactual robustness, external empirical anchoring, falsifiability, and comparison against alternative explanations.

This separation is intentional. The observer mathematics should become stronger on its own terms. Any later claim about consciousness would have to survive additional axioms and tests rather than being built into the name of the mathematical object.

## What remains open

The sharpest current statistical results still rely on Gaussian temporal-spatial separability, valid nuisance structure, and a correctly specified calibration family. Proposition 50 uses independent standardized calibration channels and a two-parameter AR(1)-plus-white-noise family. It is not a nonparametric dependence estimator.

The immediate statistical target is:

> **Replace the rectangular two-lag parameter propagation by a genuinely joint confidence region, then extend the calibration layer toward broader temporal covariance families while retaining explicit finite-sample confidence accounting.**

The broader foundational target is different:

> **Determine which observer-like structures remain identifiable, invariant, causally discriminable, and robust when the Gaussian coordinate model is progressively weakened.**

Those two directions, statistical generalization and foundational invariance, are complementary. The first makes the certificates more observable. The second tests whether the mathematical object survives changes of representation and modeling assumptions.
