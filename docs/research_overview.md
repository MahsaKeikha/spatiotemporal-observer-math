# Research overview

This page explains the project as a scientific story rather than as a file list. If the equations feel detached from their physical meaning, read the [Physics Guide](physics_guide.md) first. For the complete theorem and experiment map, use the [Research Index](research_index.md).

The 0.40.0 research record contains 52 propositions, 38 reproducible experiments, 25 scientific result figures, and 177 claim-level tests.

## The physical question

Most dynamical analyses begin by deciding which variables belong to a system and which belong to its environment.

This project asks whether, under controlled assumptions, part of that order can be reversed:

> **Can a subsystem boundary be inferred from dynamical organization when the relevant physical structure is allowed to move through the measured coordinates?**

At time `t`, let the measured state be

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

A candidate subsystem is a coordinate set

\[
S_t\subseteq\{1,\ldots,n\}.
\]

A changing candidate history is

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

called an **observer world-tube**.

The term is operational. It tracks a moving subset of measured degrees of freedom. It is not a claim about relativistic spacetime and it is not a definition of consciousness.

A useful physical picture is a coherent structure moving across a sensor field. The structure can persist while the sensors representing it change.

## The population model

The main exact theory uses a nonstationary linear Gaussian model

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

Physically, `A_t` is treated as an effective one-step coupling or propagation operator, and `Q_t` describes unresolved stochastic forcing inside the model.

This is an analytical model, not a claim that every physical system is fundamentally linear or Gaussian. A real application has to justify the measurement coordinates, sampling interval, preprocessing, nuisance structure, and model adequacy.

## What makes a candidate boundary interesting?

The implemented objective combines four operational ideas.

### Integration

Internal parts of the candidate should carry predictive information about one another.

Physical reading: the candidate contains coupled degrees of freedom participating in a common dynamical organization.

### Insulation

Once the candidate's own state is known, outside variables should add comparatively limited predictive information about its immediate evolution.

Physical reading: the candidate has some internal predictive closure without requiring physical isolation.

### Persistence

The present candidate should carry predictive structure into its future.

Physical reading: the organization is not a one-frame fluctuation.

### Transport

When the physical structure moves, predictive organization should transfer into the new coordinates representing it.

Physical reading: identity of the organization need not be tied forever to the same sensors.

A dynamic program finds the globally maximizing path in the declared candidate family. A second calculation identifies the best competitor. Their objective difference is used by the robustness theorems.

That objective difference is sometimes called an `action margin` in the code. It is not physical action in joule-seconds unless a separate derivation supplies that interpretation.

## Why covariance certification became a major part of the project

In the Gaussian model, the information quantities used in boundary scores are functions of covariance blocks.

If covariance is estimated badly, then integration, insulation, persistence, transport, and ultimately the recovered boundary can also be wrong.

This creates a second problem underneath the boundary problem:

> **How accurately do finite, temporally correlated, drifting measurements determine the covariance geometry used by the observer-like objective?**

That is the purpose of the recent temporal-calibration theorem ladder.

A typical relative covariance guarantee has the form

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

The quantity \(\epsilon\) is statistical uncertainty under the stated model. It is not an energy, force, degree of consciousness, or physical phase variable.

## Identifiability comes before interpretation

Optimization does not create identifiability.

Propositions 13 and 14 formalize recovery only up to declared symmetries and construct observationally equivalent models for which incompatible labels cannot both be recovered from the available observations with uniformly high probability.

This gives a standing rule:

> **Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

That rule matters for ordinary physical applications and becomes even more important for any future consciousness interpretation.

---

# How the proof program developed

## Foundations: Propositions 1 through 14

The first results establish covariance identities, information quantities, transport properties, path optimization, deterministic perturbation logic, finite-sample recovery, and identifiability limits.

## Structural compression: Propositions 15 through 31

These results reduce the cost of robust path certification by exploiting near-competitor graphs, overlap classes, block sparsity, covariance influence cones, interval classes, structural residuals, and screened environmental structure.

## Statistical screening and drift: Propositions 32 through 40

This layer introduces safe sample splitting, Gaussian screening, structural-null refinements, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

## Temporally dependent measurements: Propositions 41 through 52

This layer addresses the physical fact that repeated measurements are temporally correlated and can contain deterministic nuisance trends.

The sequence moves from a known temporal covariance model to a fully calibrated continuum family that can be propagated into an independent target covariance certificate.

---

# The recent temporal sequence

## Proposition 41: temporal dependence changes effective information

The covariance radius depends on temporal Frobenius and spectral geometry rather than treating record length as an independent sample count.

Physical question: how much independent information is really contained in a record with memory?

## Proposition 42: mean removal changes normalization

Under temporal dependence, removing an unknown constant mean changes the quadratic form and its exact normalization.

Physical question: how much fluctuation information remains after subtracting an unknown baseline?

## Proposition 43: estimate AR(1) persistence

Increment energy produces an observable confidence interval for a shared nonnegative AR(1) coefficient.

Physical question: can the persistence timescale be learned instead of assumed?

## Proposition 44: project away a declared time-varying nuisance

[![Experiment AD](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

A fixed temporal design is projected away exactly. Experiment AD shows why this matters: ordinary centering can fail badly under affine drift while declared nuisance projection remains stable.

## Proposition 45: combine temporal calibration and nuisance projection

[![Experiment AE](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

Temporal-memory uncertainty and deterministic nuisance removal enter one finite-sample covariance certificate.

## Proposition 46: use the actual nuisance geometry

[![Experiment AF](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

A rank-only worst case is replaced by a continuum certificate using the actual declared nuisance design.

## Proposition 47: direct matrix concentration

[![Experiment AG](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

The earlier directional sphere-net reduction is replaced by direct Gaussian matrix concentration using the full projected temporal eigenvalue profile.

## Proposition 48: make the matrix bound uniform over unknown AR(1)

[![Experiment AH](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

The projected temporal spectrum is controlled across the complete calibrated AR(1) interval.

## Proposition 49: separate temporal-family geometry from probability

[![Experiment AI](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

A deterministic finite cover controls a complete compact temporal covariance family without treating cover points as separate stochastic tests.

## Proposition 50: learn a two-parameter temporal family from independent calibration data

[![Experiment AJ](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

For

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I,
\]

lag-1 and lag-2 increment energies produce a conservative finite-sample parameter rectangle.

## Proposition 51: use the complete residual likelihood

[![Experiment AK](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

A fixed mean-removal contrast and a proper mixture density produce the pointwise e-value

\[
e_\theta(Z)=\frac{q(Z)}{p_\theta(Z)}.
\]

At the true parameter,

\[
\mathbb E_\theta e_\theta(Z)=1,
\]

so the continuum set

\[
\mathcal C_\alpha(Z)
=
\{\theta:e_\theta(Z)<1/\alpha\}
\]

has finite-sample coverage at least \(1-\alpha\).

The plotted grid in Experiment AK is only a visualization of that continuum function.

## Proposition 52: certify the continuum set for target use

[![Experiment AL](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md)

Proposition 52 partitions the declared parameter box into fixed cells. A cell is discarded only if a uniform likelihood perturbation bound proves that every point inside the cell is outside the exact Proposition 51 confidence set.

Therefore, if \(\mathcal O_\alpha(Z)\) denotes the union of retained cells,

\[
\boxed{
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z)
}.
\]

This turns the irregular continuum confidence set into a finite certified family that can be used by Proposition 49.

For Experiment AL, 5,325 of 7,381 cells are retained and 2,056 are certified excluded. The independent target composition gives a relative covariance radius

\[
0.8998157009696983<1
\]

with combined confidence lower bound

\[
0.975^2=0.950625.
\]

The physical meaning is straightforward: every temporal-memory model still compatible with calibration is carried into the target covariance uncertainty rather than replacing the calibration uncertainty by one fitted parameter.

---

# What the project now establishes

Under the stated assumptions, the repository provides a conditional mathematical pipeline from nonstationary Gaussian measurements to moving-boundary optimization and finite-sample recovery certification.

The current statistical layer can handle:

- temporally dependent Gaussian sampling;
- unknown constant and fixed-subspace nuisance means;
- estimated temporal persistence;
- actual nuisance-design geometry;
- direct matrix concentration using the full projected temporal spectrum;
- compact multi-parameter temporal covariance families;
- independently calibrated two-parameter temporal uncertainty;
- a finite-sample continuum confidence set from the full residual likelihood;
- a certified finite outer cover of that continuum set;
- independent-target covariance certification over the complete retained temporal family.

## What remains open

The current theory still depends on explicit model assumptions, including Gaussian calibration, a correct declared temporal family, channel independence in the calibration model, target separability, fixed nuisance structure, and a declared candidate family.

The next statistical frontier should move beyond the current AR(1) plus white-noise family toward richer temporal kernels or spectral-density families, while preserving finite-sample calibration and transparent physical interpretation.

The next physical frontier should ask which conclusions survive changes of sampling interval, sensor coordinates, coarse graining, and physically admissible reparameterization.

The structural frontier remains intervention-sensitive and representation-invariant observer quantities, together with impossibility theorems for distinctions that passive measurements cannot identify.

Any consciousness interpretation remains a separate bridge problem under the [Interpretation Protocol](interpretation_protocol.md). It is not a hidden consequence of observer notation.

## Why negative results matter

The project keeps impossibility results, failed parameter regimes, conservative bounds, and model diagnostics visible. A theorem describing what cannot be identified can be more useful than a broad positive claim because it tells us which additional observables, interventions, or assumptions are mathematically necessary.