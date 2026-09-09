# Research overview

This page explains the project as one scientific story rather than as a file list. If the equations feel detached from their physical meaning, start with the [Physics Guide](physics_guide.md). For the complete theorem and experiment map, use the [Research Index](research_index.md).

The 0.44.0 research record targets 55 propositions, 42 reproducible experiments, 30 scientific result figures, and 206 claim-level tests. These counts become verified after the exact release candidate is merged and the resulting `main` workflow succeeds.

## Conceptual starting point

One important conceptual source is Max Tegmark's paper ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014), which asks why observers perceive a particular factorization of the physical world and studies information, integration, independence, and dynamics as candidate organizing principles. The technical preprint is [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

This repository is a separate research program. It does not reproduce Tegmark's results and does not imply his endorsement. It develops an operational moving-boundary formulation, recovery and identifiability theory, finite-sample certification, temporal calibration, and physical representation tests.

## The physical question

Most dynamical analyses begin by deciding which variables belong to a system and which belong to its environment.

This project asks whether, under controlled assumptions, part of that order can be reversed:

> **Can a subsystem boundary be inferred from dynamical organization when the relevant physical structure is allowed to move through the measured coordinates?**

At time \(t\), let the measured state be

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

A candidate subsystem is

\[
S_t\subseteq\{1,\ldots,n\},
\]

and a changing candidate history is

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

Physically, \(A_t\) is treated as an effective one-step coupling or propagation operator, while \(Q_t\) describes unresolved stochastic forcing inside the model.

This is an analytical model, not a claim that every physical system is fundamentally linear or Gaussian. A real application has to justify the measurement coordinates, physical units, sampling schedule, preprocessing, nuisance structure, and model adequacy.

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

The quantity called an `action margin` in the code is an optimization margin. It is not physical action in joule-seconds.

## Why covariance certification became a major part of the project

In the Gaussian model, the information quantities used in boundary scores are functions of covariance blocks.

If covariance is estimated badly, then integration, insulation, persistence, transport, and ultimately the recovered boundary can also be wrong.

This creates a second problem underneath the boundary problem:

> **How accurately do finite, temporally correlated, drifting measurements determine the covariance geometry used by the observer-like objective?**

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

The standing rule is:

> **Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

That rule matters for ordinary physical applications and becomes even more important for any later consciousness interpretation.

---

# How the proof program developed

## Foundations, Propositions 1 through 14

The first results establish covariance identities, information quantities, transport properties, path optimization, deterministic perturbation logic, finite-sample recovery, and identifiability limits.

## Structural compression, Propositions 15 through 31

These results reduce the cost of robust path certification by exploiting near-competitor graphs, overlap classes, block sparsity, covariance influence cones, interval classes, structural residuals, and screened environmental structure.

## Statistical screening and drift, Propositions 32 through 40

This layer introduces safe sample splitting, Gaussian screening, structural-null refinements, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

## Temporally dependent measurements, Propositions 41 through 52

This layer addresses the physical fact that repeated measurements are temporally correlated and can contain deterministic nuisance trends.

The sequence moves from a known temporal covariance model to a calibrated continuum family that can be propagated into an independent target covariance certificate.

## Sampling-consistent physical time, Proposition 53

This layer asks whether the temporal parameter survives a change in how the same physical process is sampled.

Instead of treating the discrete AR(1) coefficient \(\phi\) as fundamental, Proposition 53 uses a physical relaxation time \(\tau\) for the exponential model:

\[
K_\tau(t,s)
=
\exp\left(-\frac{|t-s|}{\tau}\right).
\]

For uniform sampling interval \(\Delta t\),

\[
\phi_{\Delta t}
=
\exp\left(-\frac{\Delta t}{\tau}\right).
\]

The discrete correlation changes when the acquisition interval changes. The declared physical relaxation time does not.

---

# The recent temporal and sampling sequence

## Proposition 41: temporal dependence changes effective information

The covariance radius depends on temporal Frobenius and spectral geometry rather than treating record length as an independent sample count.

Physical question: how much independent information is really contained in a record with memory?

## Proposition 42: mean removal changes normalization

Under temporal dependence, removing an unknown constant mean changes the quadratic form and its exact normalization.

Physical question: how much fluctuation information remains after subtracting an unknown baseline?

## Proposition 43: estimate discrete AR(1) persistence

Increment energy produces an observable confidence interval for a shared nonnegative AR(1) coefficient.

Physical question: can persistence be learned instead of assumed?

## Propositions 44 through 46: nuisance structure and actual temporal geometry

These propositions remove fixed time-varying nuisance subspaces, combine that projection with estimated temporal dependence, and replace a rank-only worst case with the actual declared nuisance geometry.

[![Experiment AD](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

[![Experiment AF](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

## Propositions 47 through 49: direct matrix concentration over temporal families

The earlier directional reduction is replaced by direct Gaussian matrix concentration using the full projected temporal spectrum, then extended from one known temporal covariance to compact temporal families.

[![Experiment AG](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

[![Experiment AI](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

## Propositions 50 through 52: learn temporal uncertainty and carry it into a target record

Proposition 50 builds a conservative two-parameter calibration region. Proposition 51 uses the complete residual likelihood to form a finite-sample continuum e-value confidence set. Proposition 52 certifies a finite outer cover of that continuum set and propagates it into an independent target covariance theorem.

[![Experiment AK](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

[![Experiment AL](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md)

For Experiment AL the final target relative covariance radius is

\[
0.8998157009696983<1
\]

with combined confidence lower bound

\[
0.975^2=0.950625.
\]

The physical meaning is that every temporal-memory model still compatible with calibration is carried into the target covariance uncertainty rather than replacing calibration uncertainty by one fitted parameter.

## Proposition 53: make the timescale physical

[![Experiment AM](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

Experiment AM uses one controlled relaxation time,

\[
\tau=0.8\ \mathrm{s},
\]

and samples the same exponential model at 40 Hz, 20 Hz, 10 Hz, 5 Hz, and 2.5 Hz.

The one-step correlations range from about `0.9692` to `0.6065`, yet every value maps back to the same \(0.8\) s relaxation time.

The exact coarse-sampling identity is

\[
\phi_{k\Delta t}=\phi_{\Delta t}^k.
\]

The theorem also supports irregular timestamps and proves an operator-Lipschitz continuum bound over a declared \(\tau\)-interval. This lets a physical relaxation-time family enter Proposition 49 directly.

The important hierarchy is now explicit:

\[
\boxed{
\text{physical timescale }\tau
\longrightarrow
\text{sampling schedule}
\longrightarrow
\text{discrete covariance representation}
}
\]

rather than treating a sample-index coefficient as if it were automatically an intrinsic physical constant.

## Propositions 54 and 55: separate calibration resolution, then use local curvature

[![Experiment AO](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)

[![Experiment AP](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)

Proposition 54 separates the fine grid needed to certify the continuum calibration set from the smaller target covariance cover. Proposition 55 then uses the exact observed-data e-value slope and a rigorous local curvature bound to tighten the calibration enclosure itself.

At 160 calibration cells, the certified physical-time width falls from `0.6109375 s` to `0.1646875 s`. The target covariance radius improves to `2.4148799294`.

The known-tau oracle radius is still `2.1672468952 > 1`. This identifies the next bottleneck: target covariance concentration rather than calibration uncertainty.

---

# What the project now establishes

Under its stated assumptions, the repository provides a conditional mathematical pipeline from nonstationary Gaussian measurements to moving-boundary optimization and finite-sample recovery certification.

The current statistical and physical-accountability layers can handle:

- temporally dependent Gaussian sampling;
- unknown constant and fixed-subspace nuisance means;
- estimated temporal persistence;
- actual nuisance-design geometry;
- direct matrix concentration using the full projected temporal spectrum;
- compact multi-parameter temporal covariance families;
- independently calibrated temporal uncertainty;
- a finite-sample continuum confidence set from the full residual likelihood;
- a certified finite outer cover of that continuum set;
- independent-target covariance certification over the complete retained temporal family;
- a physical relaxation-time representation for the exponential kernel;
- uniform, coarse, and irregular sampling schedules;
- invariance under a change of time units;
- a certified continuum cover over a declared physical \(\tau\)-interval.

## What remains open

The current theory still depends on explicit model assumptions, including Gaussian calibration where invoked, a correct declared temporal family, target separability, fixed nuisance structure, and a declared candidate family.

The next temporal frontier is to move beyond one exponential relaxation time toward richer kernels or spectral-density families while preserving finite-sample calibration and transparent physical units.

The next representation frontier is sensor-coordinate geometry: determine which observer-like conclusions survive invertible sensor transformations, which transformations preserve the meaning of a boundary, and how coarse graining or spatial resolution changes the candidate family.

The structural frontier remains intervention-sensitive observer quantities and impossibility theorems for distinctions that passive measurements cannot identify.

Any consciousness interpretation remains a separate bridge problem under the [Interpretation Protocol](interpretation_protocol.md). It is not a hidden consequence of observer notation.

## Why negative results matter

The project keeps impossibility results, failed parameter regimes, conservative bounds, and model diagnostics visible. A theorem describing what cannot be identified can be more useful than a broad positive claim because it tells us which additional observables, interventions, or assumptions are mathematically necessary.

## Proposition 55 oracle bottleneck

Experiment AP includes a known-tau diagnostic that removes temporal calibration uncertainty completely. The current target concentration theorem still gives relative radius `2.1672468952 > 1`. This is a negative but actionable result: further calibration refinement alone cannot solve this target benchmark. The next theorem should attack the target concentration layer or derive explicit information requirements for entering the `epsilon < 1` regime.
