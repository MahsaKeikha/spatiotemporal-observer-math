# Research overview

This page explains **Spatiotemporal Observer Mathematics** as one scientific story rather than as a file list.

For a visual first reading, start with the [Visual Research Guide](visual_research_guide.md). For physical meaning, units, and model accountability, use the [Physics Guide](physics_guide.md). For proposition-by-proposition navigation, use the [Research Index](research_index.md).

The current 0.47.0 record contains **58 propositions, 45 reproducible experiments, 33 scientific result figures, and 223 claim-level tests** across Python 3.10, 3.11, and 3.12.

---

# 1. Conceptual starting point

The primary conceptual starting point is Max Tegmark's paper ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014), with technical preprint [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

Tegmark asks why observers perceive a particular factorization of the physical world and studies information, integration, independence, and dynamics as candidate organizing principles. This repository develops that factorization and observer-identification question in a separate operational direction: the relevant subsystem boundary may change with time and must be inferred from dynamical organization rather than fixed in advance.

The repository does not reproduce Tegmark's derivations and does not imply his endorsement. The word **observer** is operational here. It denotes a mathematically defined persistent moving subsystem. The results do not establish consciousness or subjective experience. Any future connection requires additional bridge assumptions under the [Interpretation Protocol](interpretation_protocol.md).

---

# 2. The physical question

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

[![Physics to inference pipeline](physics_pipeline.svg)](physics_guide.md)

---

# 3. Population dynamics and operational observer score

The main exact theory begins from a nonstationary linear Gaussian model

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

Here \(A_t\) is an effective one-step coupling or propagation operator and \(Q_t\) is unresolved stochastic forcing inside the declared model.

This is an analytical model, not a claim that every physical system is fundamentally linear or Gaussian. A real application must justify its measurement coordinates, units, sampling schedule, preprocessing, nuisance structure, and model adequacy.

The implemented objective combines four operational ideas:

1. **Integration.** Internal parts of a candidate carry predictive information about one another.
2. **Insulation.** After conditioning on the candidate state, exterior variables add comparatively limited predictive information about its immediate evolution.
3. **Persistence.** The present candidate carries predictive structure into its future.
4. **Transport.** When the physical organization moves, predictive structure can transfer into different measured coordinates.

For path \(p=(j_0,\ldots,j_{T-1})\), the world-tube objective has the form

\[
A(p)
=
\sum_t\ell_t(j_t)
+\chi\sum_t\theta_t(j_t,j_{t+1})
-\lambda\sum_t d(j_t,j_{t+1}).
\]

A dynamic program finds the globally maximizing path in the declared candidate family. A second calculation identifies the best competitor. Their objective difference drives robustness and recovery certificates.

The implementation term `action margin` refers to this optimization margin. It is not physical action in joule-seconds.

[![World-tube baseline](worldtube_baseline.png)](reproducible_results.md)

---

# 4. Why covariance certification became central

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

# 5. How the proof program developed

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

The discrete AR(1) coefficient depends on acquisition interval, so Proposition 53 parameterizes the declared exponential temporal model by a physical relaxation time \(\tau\):

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

This local structure becomes decisive in Propositions 56 and 57.

---

# 6. The recent physical-time sequence

## Proposition 53B / Experiment AN: infer physical relaxation time directly

Proposition 53B uses the exact irregular-grid Gaussian innovation likelihood to construct a finite-sample continuum e-value confidence set for \(\tau\).

[![Experiment AN](irregular_relaxation_evalue_calibration.svg)](proposition_53b_irregular_tau_evalue.md)

The remaining target covariance radius is `3.15549 > 1`, making the tightness problem visible rather than hiding it.

## Proposition 54 / Experiment AO: separate calibration and target resolution

Proposition 54 separates the fine resolution used to certify the calibration continuum from the smaller cover propagated into the independent target theorem.

[![Experiment AO](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)

The target radius improves from `3.15549` to `2.57207`, but remains above one.

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

That negative diagnostic is important: calibration uncertainty is no longer the dominant bottleneck on this benchmark.

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

and residualize in the transformed coordinates. The covariance estimator satisfies

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

For the controlled target, \(N=120\), \(q=2\), giving 118 residual Gaussian innovation degrees of freedom.

The scalar radius changes from

\[
2.1672468952
\]

to

\[
\boxed{0.4364443814<1}.
\]

The improvement comes from changing the statistical representation before concentration, not from another calibration refinement.

## Proposition 57 / Experiment AR: retain the innovation advantage under calibrated tau uncertainty

[![Experiment AR](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

Proposition 57 removes the exact-target-\(\tau\) assumption on the same controlled scalar benchmark.

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

A deterministic finite cover of this transformed family feeds into Proposition 49 matrix concentration. The resulting uniform scalar target covariance radius is

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

The price of physical-time uncertainty is explicit rather than ignored.

---

# 7. Proposition 58 / Experiment AS: return to the observer problem

[![Experiment AS](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

Proposition 58 closes the deterministic bridge from simultaneous relative covariance uncertainty back to the original moving-boundary objective.

For future candidate \(S\), define

\[
B_{t,S}=(X_t,X_{t+1}^{S}).
\]

This block has dimension

\[
d_{\mathrm{obs}}=n+s
\]

and contains the covariance submatrices required for the candidate's local factors and every incoming transport edge.

For Experiment AS,

\[
n=7,
\qquad
s=3,
\qquad
T=5,
\qquad
C=35,
\]

so

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

The planted and recovered path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

with population action margin `0.1264216185`.

## The observer-scale diagnostic

At the scalar level, exact-tau innovation concentration gives

\[
0.4364443814.
\]

At observer block dimension 10, block count 175, and the same 118 residual innovation degrees, the current exact-tau unit-weight matrix theorem gives

\[
\boxed{
1.8573569119>1.
}
\]

The first residual degree count at which the current matrix theorem enters the relative perturbation regime is 346:

\[
\varepsilon_{345}=1.0007464318,
\qquad
\varepsilon_{346}=0.9991303523.
\]

But \(\epsilon<1\) only makes the relative perturbation layer admissible. It does not automatically certify the full moving path.

The present generic factor-by-factor world-tube bridge certifies the controlled population path only for a much smaller uniform covariance radius, approximately `1.11e-4`. The corresponding enormous unit-weight residual-degree calculation is deliberately recorded as a **conservatism diagnostic, not a physical sample requirement**.

This result changes the frontier. The dominant limitation is now observer-scale dimension and structural worst-case propagation, not another physical-time calibration step.

---

# 8. What the project now establishes

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
- uniform robust innovation-whitened covariance concentration over a finite-sample calibrated \(\tau\)-interval;
- deterministic propagation of simultaneous relative covariance uncertainty into integration, insulation, persistence, transport, and the full world-tube action.

These are mathematical statements conditional on declared models. They do not by themselves validate those models for a real physical system.

## Why negative results remain part of the record

The project deliberately keeps impossibility results, failed parameter regimes, conservative bounds, and model diagnostics visible.

Experiment AP's known-\(\tau\) radius `2.16725 > 1` identified the wrong target representation and motivated Proposition 56.

Experiment AS's observer-scale radius `1.85736 > 1` shows that scalar covariance success is not the same as end-to-end observer certification and redirects the program toward localized structural control.

A negative diagnostic is useful when it prevents theorem complexity from being spent on the wrong bottleneck.

---

# 9. Current frontiers

The immediate mathematical frontier is now localized observer-scale certification:

> **Can the covariance geometry actually needed by near-competitive observer factors be certified directly enough that the world-tube action margin, rather than a chain of global worst-case intermediate bounds, becomes the main object of concentration?**

The concrete directions are:

1. factor-specific covariance blocks;
2. screen-first simultaneity reduction;
3. candidate-local covariance radii;
4. direct score-margin or action-difference concentration;
5. richer temporal physics only after the observer-scale structural bottleneck is understood.

The physical-model frontier is to move beyond one stationary exponential relaxation time toward richer kernels or spectral-density families while preserving finite-sample calibration, explicit physical units, and falsifiability.

The representation frontier remains sensor-coordinate geometry, spatial coarse graining, and intervention-sensitive identifiability.

Any future consciousness interpretation remains a separate bridge problem under the [Interpretation Protocol](interpretation_protocol.md). It is not a hidden consequence of observer notation or covariance certification.

---

# 10. Audit trail

For the complete visual record, use the [Visual Research Guide](visual_research_guide.md).

For theorem and experiment navigation, use the [Research Index](research_index.md).

For assumptions and failure conditions, use the [Assumption Ledger](assumption_ledger.md).

For external scientific sources and their exact roles, use the [Bibliography and Citation Map](bibliography.md).

For the current release, use the [0.47.0 Research Record](release_0_47.md).

A numerical experiment is not a proof. A theorem is not evidence that its assumptions hold in a real system. A mathematically recovered moving subsystem is not, by that fact alone, a conscious observer.
