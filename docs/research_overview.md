# Research overview

This page explains the project as one scientific story rather than as a file list. If the equations feel detached from their physical meaning, start with the [Physics Guide](physics_guide.md). For the complete theorem and experiment map, use the [Research Index](research_index.md).

The current 0.46.0 record contains **57 propositions, 44 reproducible experiments, 32 scientific result figures, and 219 claim-level tests** across Python 3.10, 3.11, and 3.12.

## Conceptual starting point

The primary conceptual starting point is Max Tegmark's paper ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014), with technical preprint [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

Tegmark asks why observers perceive a particular factorization of the physical world and studies information, integration, independence, and dynamics as candidate organizing principles. This repository develops that factorization and observer-identification question in a separate operational direction: a subsystem boundary may change with time and must be inferred from dynamical organization rather than fixed in advance.

The repository does not reproduce Tegmark's derivations and does not imply his endorsement. The word **observer** is operational here. It denotes a mathematically defined persistent moving subsystem. The results do not establish consciousness or subjective experience. Any future connection requires additional bridge assumptions under the [Interpretation Protocol](interpretation_protocol.md).

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

A useful physical picture is a coherent structure moving across a sensor field. The structure can persist while the sensor coordinates representing it change.

## Population model and operational score

The main exact theory begins from a nonstationary linear Gaussian model

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

Here \(A_t\) is treated as an effective one-step coupling or propagation operator and \(Q_t\) as unresolved stochastic forcing inside the declared model.

This is an analytical model, not a claim that every physical system is fundamentally linear or Gaussian. A real application must justify measurement coordinates, physical units, sampling schedule, preprocessing, nuisance structure, and model adequacy.

The implemented objective combines four operational ideas:

1. **Integration.** Internal parts of a candidate carry predictive information about one another.
2. **Insulation.** After conditioning on the candidate state, exterior variables add comparatively limited predictive information about its immediate evolution.
3. **Persistence.** The present candidate carries predictive structure into its future.
4. **Transport.** When the physical organization moves, predictive structure can transfer into different measured coordinates.

A dynamic program finds the globally maximizing path in the declared candidate family. A second calculation identifies the best competitor. Their objective difference drives robustness and recovery certificates.

The quantity called an `action margin` in the implementation is an optimization margin. It is not physical action in joule-seconds.

---

# Why covariance certification became central

In the Gaussian model, the information factors entering integration, insulation, persistence, and transport are functions of covariance blocks.

If covariance is estimated badly, the score can be wrong and the recovered world-tube can be wrong. This creates a second problem underneath the boundary problem:

> **How accurately do finite, temporally correlated, drifting measurements determine the covariance geometry used by the moving-boundary objective?**

A typical relative covariance guarantee is

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

The quantity \(\epsilon\) is statistical uncertainty under the stated model. It is not an energy, force, degree of consciousness, or physical phase variable. The threshold \(\epsilon<1\) matters mathematically because inverse-covariance perturbation calculations remain in a controlled regime.

## Identifiability comes before interpretation

Optimization does not create identifiability.

Propositions 13 and 14 formalize recovery only up to declared symmetries and construct observationally equivalent models for which incompatible labels cannot both be recovered from the available observations with uniformly high probability.

The standing rule is:

> **Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

That rule applies to ordinary physical applications and becomes even more important for any later consciousness interpretation.

---

# How the proof program developed

## Propositions 1 through 14: foundations and first recovery theory

These results establish covariance identities, information quantities, transport properties, path optimization, deterministic perturbation logic, finite-sample recovery, and identifiability limits.

## Propositions 15 through 31: structural compression

These results reduce robust path-certification cost by exploiting near-competitor graphs, overlap classes, block sparsity, covariance influence cones, interval classes, structural residuals, and screened environmental structure.

## Propositions 32 through 40: screening and population drift

This layer introduces safe sample splitting, Gaussian screening, structural-null refinements, covariance-normalized concentration, reusable pilot geometry, and statistically calibrated population drift.

## Propositions 41 through 52: temporally dependent measurements

This layer addresses the fact that repeated measurements have temporal memory and can contain deterministic nuisance trends.

The sequence moves from known temporal covariance to learned temporal uncertainty and finally to an independently calibrated continuum family that can be propagated into a target covariance theorem.

## Proposition 53: physical time and exact irregular-grid local structure

The discrete AR(1) coefficient depends on acquisition interval, so Proposition 53 parameterizes the exponential temporal model by a physical relaxation time \(\tau\):

\[
K_\tau(t,s)
=
\exp\left(-\frac{|t-s|}{\tau}\right).
\]

Under uniform sampling interval \(\Delta t\),

\[
\phi_{\Delta t}
=
\exp\left(-\frac{\Delta t}{\tau}\right).
\]

The one-step correlation changes when the sampling interval changes; the declared physical relaxation time does not.

For irregular adjacent gaps,

\[
\alpha_i
=
\exp\left(-\frac{t_{i+1}-t_i}{\tau}\right),
\]

and the model has the exact transition law

\[
X_{i+1}
=
\alpha_iX_i
+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
\]

The same theorem gives an exact lower-bidiagonal innovation whitener and tridiagonal precision matrix:

\[
W_\tau R_\tau W_\tau^\mathsf T=I,
\qquad
R_\tau^{-1}=W_\tau^\mathsf T W_\tau.
\]

This exact local structure becomes decisive in Propositions 56 and 57.

---

# The recent physical-time sequence

## Proposition 53B / Experiment AN: infer physical relaxation time directly

Proposition 53B uses the exact irregular-grid Gaussian innovation likelihood to construct a finite-sample continuum e-value confidence set for \(\tau\).

Experiment AN demonstrates direct physical-time inference on irregular timestamps, time-unit covariance, a certified finite outer cover, and independent target composition.

The remaining target covariance radius is `3.15549 > 1`, making the tightness problem visible rather than hiding it.

## Proposition 54 / Experiment AO: separate calibration and target resolution

Proposition 54 separates the fine resolution used to certify the calibration continuum from the smaller cover propagated into the independent target theorem.

The Experiment AN target radius improves from `3.15549` to `2.57207`, but remains above one.

## Proposition 55 / Experiment AP: use local likelihood curvature

[![Experiment AP](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)

Proposition 55 uses the exact observed-data log-evalue slope plus a rigorous cell-local second-derivative bound to tighten the finite-sample physical-time outer cover without spending an additional probability budget.

At 160 calibration cells, the retained hull becomes

\[
\boxed{
[0.686875,0.8515625]\ \mathrm{s}
}
\]

with width `0.1646875 s`, about 73% narrower than the corresponding first-order enclosure.

The target covariance radius improves to

\[
2.4148799294.
\]

But an intentionally unrealistic known-\(\tau\) oracle still gives

\[
2.1672468952>1.
\]

That negative diagnostic is important: calibration uncertainty is no longer the dominant bottleneck on this benchmark. Improving calibration alone cannot cross the perturbative threshold.

## Proposition 56 / Experiment AQ: change the target representation

[![Experiment AQ](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

Proposition 56 uses the exact Proposition 53 innovation coordinates before nuisance fitting and target covariance concentration.

For

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma),
\]

with exact \(\tau\), define

\[
Z=W_\tau Y,
\qquad
G=W_\tau H,
\]

and residualize with

\[
P_G=I-G(G^\mathsf TG)^{-1}G^\mathsf T.
\]

Then

\[
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}Z^\mathsf TP_GZ
\]

satisfies

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

For the controlled target, \(N=120\), \(q=2\), so the target contains exactly 118 residual Gaussian innovation degrees of freedom.

The radius changes from the old known-\(\tau\) raw-time oracle

\[
2.1672468952
\]

to

\[
\boxed{0.4364443814<1}.
\]

The approximately 79.86% reduction comes from changing the statistical representation before concentration, not from another calibration refinement.

The remaining limitation is exact knowledge of target \(\tau\).

## Proposition 57 / Experiment AR: retain the innovation advantage under calibrated tau uncertainty

[![Experiment AR](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

Proposition 57 removes the exact-target-\(\tau\) assumption on the same controlled benchmark.

Starting from the independently calibrated Proposition 55 interval

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s},
\]

choose one working relaxation time

\[
\tau_0=0.76921875\ \mathrm{s}
\]

and let \(W_0\) be its exact Proposition 53 whitener.

For every admissible true \(\tau\), the target covariance in working innovation coordinates is

\[
C_\tau=W_0R_\tau W_0^\mathsf T.
\]

The Proposition 53 operator-Lipschitz envelope gives

\[
\|C_\tau-C_{\tau'}\|_2
\le
\|W_0\|_2^2L_R|\tau-\tau'|.
\]

A deterministic finite cover of this transformed family, together with Weyl control and a conservative projected-normalization envelope, feeds directly into Proposition 49 matrix concentration.

The resulting uniform target covariance radius is

\[
\boxed{
\varepsilon_{57}=0.8677117535<1.
}
\]

Calibration and target confidence are each `0.975`, giving combined confidence lower bound

\[
\boxed{0.950625}.
\]

The comparison on the same target schedule is:

| Target representation | Physical-time information | Relative covariance radius |
| --- | --- | ---: |
| Proposition 55 raw-time target | finite-sample calibrated interval | 2.41488 |
| Proposition 55 raw-time oracle | exact true tau | 2.16725 |
| Proposition 56 innovation target | exact true tau | 0.43647 |
| **Proposition 57 robust innovation target** | **finite-sample calibrated interval** | **0.86771** |

Thus the price of physical-time uncertainty is explicit rather than ignored. The radius grows relative to the exact-\(\tau\) theorem, but remains below one and is about 64.1% smaller than the calibrated raw-time theorem.

---

# What the project now establishes

Under its stated assumptions, the repository provides a conditional mathematical pipeline from measured stochastic dynamics to moving-boundary optimization and finite-sample recovery certification.

The current statistical and physical-accountability layers include:

- temporally dependent Gaussian sampling;
- unknown constant and fixed-subspace nuisance means;
- estimated temporal persistence;
- design-specific nuisance geometry;
- direct matrix concentration using the full projected temporal spectrum;
- compact multi-parameter temporal covariance families;
- finite-sample continuum e-value calibration;
- certified outer covers propagated to independent target records;
- sampling-consistent physical relaxation time;
- exact irregular-grid Markov factorization and innovation whitening;
- exact known-\(\tau\) innovation-whitened target covariance concentration;
- uniform robust innovation-whitened covariance concentration over a finite-sample calibrated \(\tau\)-interval.

These are mathematical statements conditional on declared models. They do not by themselves validate those models for a real physical system.

## Why negative results remain part of the record

The project deliberately keeps impossibility results, failed parameter regimes, conservative bounds, and model diagnostics visible.

Experiment AP's known-\(\tau\) radius `2.16725 > 1` was not a failure to hide. It identified the wrong target representation and directly motivated Proposition 56.

Proposition 57 also records its remaining conservatism: pointwise diagnostic radii on Experiment AR are roughly `0.404` to `0.580`, while the uniform theorem reports `0.86771`. The gap identifies where a sharper transformed-family normalization theorem could improve the certificate without changing the estimator.

---

# Current frontiers

The immediate conceptual frontier returns to the original moving-boundary problem:

> **Can the certified post-whitening covariance uncertainty be propagated through integration, insulation, persistence, transport, and world-tube path recovery without discarding its structure in an unnecessarily large generic bound?**

A parallel statistical frontier is to tighten Proposition 57's conservative projected-normalization envelope using the actual transformed nuisance geometry.

The physical-model frontier is to move beyond one stationary exponential relaxation time toward richer kernels or spectral-density families while preserving finite-sample calibration, explicit physical units, and falsifiability.

The representation frontier remains sensor-coordinate geometry, spatial coarse graining, and intervention-sensitive identifiability.

Any future consciousness interpretation remains a separate bridge problem under the [Interpretation Protocol](interpretation_protocol.md). It is not a hidden consequence of observer notation or covariance certification.

For the complete audit trail, see the [Research Index](research_index.md), [Assumption Ledger](assumption_ledger.md), [Bibliography and Citation Map](bibliography.md), and [0.46.0 Research Record](release_0_46.md).