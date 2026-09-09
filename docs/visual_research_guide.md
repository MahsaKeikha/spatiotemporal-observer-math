# Visual research guide

This page is the visual atlas for **Spatiotemporal Observer Mathematics**.

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The primary conceptual starting point is Max Tegmark's observer-factorization question in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014). The present research develops a time-dependent mathematical program for subsystem boundaries, recovery, identifiability, finite-sample measurement certification, physical-time calibration, innovation inference, and covariance-to-world-tube recovery.

For equations and source provenance, use the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md). For physical meaning and units, use the [Physics Guide](physics_guide.md). For the theorem sequence, use the [Research Index](research_index.md).

---

# 1. The complete physics-to-inference pipeline

[![Physics to inference pipeline](physics_pipeline.svg)](physics_guide.md)

**What this figure shows.** The full conceptual flow from measured physical observables to effective dynamics, covariance geometry, candidate moving boundaries, world-tube optimization, finite-sample certification, and interpretation.

**Why it matters.** It is the shortest visual summary of how the physics and mathematics fit together.

**Verify.** [Physics Guide](physics_guide.md) | [Research Overview](research_overview.md) | [Equation provenance](physics_mathematics_citation_map.md)

---

# 2. Phase I: moving-boundary recovery

## 2.1 Baseline moving world-tube

[![World-tube baseline](worldtube_baseline.png)](reproducible_results.md)

**What this figure shows.** Candidate scores across time together with the recovered moving subsystem path.

**Physical question.** Can a coherent subsystem be tracked when the coordinates representing it change through time?

**Mathematical object.** The optimized world-tube

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

**Verify.** [Reproducible results](reproducible_results.md)

## 2.2 Recovery phase diagram

[![World-tube phase diagram](worldtube_phase_diagram.png)](reproducible_results.md)

**What this figure shows.** The region of parameter space in which the planted moving path remains optimal.

**Why it matters.** It visualizes where dynamical support is sufficient for path recovery and where competing paths become indistinguishable or superior.

**Verify.** [Reproducible results](reproducible_results.md)

---

# 3. Phase II: finite-sample and perturbation recovery

## 3.1 Finite-sample benchmark

[![Finite-sample benchmark](finite_sample_benchmark.png)](reproducible_results.md)

**What this figure shows.** Recovery behavior under finite covariance estimation rather than exact population covariances.

**Why it matters.** It introduces the gap between population identifiability and finite-data certification.

**Verify.** [Reproducible results](reproducible_results.md)

## 3.2 Symbolic recovery region

[![Symbolic recovery region](symbolic_recovery_region.png)](reproducible_results.md)

**What this figure shows.** A theorem-derived region in model parameters where the planted moving path is guaranteed to dominate structured alternatives.

**Why it matters.** It connects closed-form model structure to path recovery without relying only on numerical optimization.

**Verify.** [Reproducible results](reproducible_results.md) | [Proof record](proofs_and_conjectures.md)

## 3.3 Perturbed recovery region

[![Perturbed recovery region](perturbed_recovery_region.png)](reproducible_results.md)

**What this figure shows.** How admissible recovery changes under perturbations of transitions, forcing, and covariance geometry.

**Why it matters.** It visualizes the difference between exact planted structure and robust recovery under model deviations.

**Verify.** [Reproducible results](reproducible_results.md) | [Proof record](proofs_and_conjectures.md)

---

# 4. Phase III: screening and localization

## 4.1 Gaussian screen calibration

[![Gaussian screen calibration](gaussian_screen_calibration.png)](reproducible_results.md)

**What this figure shows.** Finite-sample screening of candidate states under Gaussian covariance uncertainty.

**Why it matters.** It demonstrates how safe screening can reduce the candidate family while retaining paths that could still win within the uncertainty budget.

**Verify.** [Reproducible results](reproducible_results.md)

## 4.2 Structural-null screen

[![Structural-null screen](structural_null_screen.png)](reproducible_results.md)

**What this figure shows.** The effect of exact structural integration nulls on candidate score uncertainty and retained graph size.

**Why it matters.** Exact null structure can improve local perturbation rates when the null is physically and mathematically justified.

**Verify.** [Reproducible results](reproducible_results.md) | [Assumption Ledger](assumption_ledger.md)

## 4.3 Trajectory-coupled screening

[![Trajectory-coupled screening](trajectory_coupled_screen_calibration.png)](reproducible_results.md)

**What this figure shows.** Screening when time-indexed covariance estimates arise from the same ensemble of complete trajectories.

**Why it matters.** It separates within-trajectory dependence from independence across trajectories.

**Verify.** [Reproducible results](reproducible_results.md)

## 4.4 Relative covariance calibration

[![Relative covariance calibration](relative_covariance_calibration.png)](reproducible_results.md)

**What this figure shows.** Calibration using population-whitened relative covariance error rather than absolute spectral error.

**Mathematical object.** The central event is

\[
\left\|
\Sigma^{-1/2}(\widehat\Sigma-\Sigma)\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

**Verify.** [Reproducible results](reproducible_results.md)

---

# 5. Phase IV: cross-fitting, drift, and changing populations

## 5.1 Cross-fitted relative calibration

[![Cross-fitted relative calibration](cross_fitted_relative_calibration.png)](reproducible_results.md)

**What this figure shows.** Separation of pilot geometry from the data used for certification.

**Why it matters.** It makes the statistical role of independent sample splitting explicit.

**Verify.** [Reproducible results](reproducible_results.md)

## 5.2 Drift-robust relative calibration

[![Drift-robust relative calibration](drift_robust_relative_calibration.png)](reproducible_results.md)

**What this figure shows.** Candidate uncertainty after both finite-sample covariance error and declared population drift are included.

**Why it matters.** A calibration population and target population need not have identical covariance geometry.

**Verify.** [Reproducible results](reproducible_results.md)

## 5.3 Calibrated drift comparison

[![Calibrated drift comparison](calibrated_drift_comparison.png)](reproducible_results.md)

**What this figure shows.** Comparison among exact-oracle drift, statistically estimated drift, and refreshed reference geometry.

**Why it matters.** It makes the cost of estimating population change visible rather than hiding it inside one radius.

**Verify.** [Reproducible results](reproducible_results.md)

## 5.4 Multi-regime coupled calibration

[![Multi-regime coupled calibration](multi_regime_coupled_calibration.png)](reproducible_results.md)

**What this figure shows.** Recovery and screening behavior across multiple memory, coupling, and covariance-conditioning regimes.

**Why it matters.** It exposes where stronger population margins can coexist with harder finite-sample covariance certification.

**Verify.** [Reproducible results](reproducible_results.md)

---

# 6. Phase V: temporally dependent measurements

## 6.1 Dependent Gaussian calibration

[![Dependent Gaussian calibration](dependent_gaussian_calibration.png)](reproducible_results.md)

**What this figure shows.** Relative covariance calibration when repeated measurements have temporal correlation.

**Why it matters.** Treating correlated observations as independent can substantially understate uncertainty.

**Verify.** [Reproducible results](reproducible_results.md)

## 6.2 Unknown-mean dependent calibration

[![Dependent centered Gaussian calibration](dependent_centered_gaussian_calibration.png)](reproducible_results.md)

**What this figure shows.** Covariance inference after accounting for an unknown constant mean under temporal dependence.

**Why it matters.** Mean removal changes the temporal normalization and therefore the effective information available for covariance estimation.

**Verify.** [Reproducible results](reproducible_results.md)

## 6.3 Estimated AR(1) calibration

[![Estimated AR1 calibration](estimated_ar1_calibration.png)](reproducible_results.md)

**What this figure shows.** Finite-sample estimation of a shared AR(1) temporal-correlation parameter and propagation of that uncertainty into covariance certification.

**Why it matters.** Temporal persistence is learned from data rather than supplied as an oracle parameter.

**Verify.** [Reproducible results](reproducible_results.md) | [Proof record](proofs_and_conjectures.md)

---

# 7. Phase VI: time-varying nuisance structure

## 7.1 Proposition 44 / Experiment AD

[![Nuisance projection](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

**What this figure shows.** Covariance estimation after projecting out a fixed, predeclared temporal nuisance subspace.

**Mathematical object.** For nuisance design \(H\),

\[
P_H=I-H(H^{\mathsf T}H)^{-1}H^{\mathsf T}.
\]

**Verify.** [Proposition 44](proposition_44_nuisance_projection.md)

## 7.2 Proposition 45 / Experiment AE

[![Estimated AR1 nuisance projection](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

**What this figure shows.** Joint uncertainty from estimated temporal correlation and nuisance projection.

**Why it matters.** It combines two measurement complications in one finite-sample certificate.

**Verify.** [Proposition 45](proposition_45_estimated_ar1_nuisance_projection.md)

## 7.3 Proposition 46 / Experiment AF

[![Design-specific AR1 envelope](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

**What this figure shows.** Design-specific temporal envelopes compared with rank-only bounds.

**Why it matters.** The actual nuisance geometry can be much less pessimistic than a bound depending only on nuisance rank.

**Verify.** [Proposition 46](proposition_46_design_specific_ar1_envelope.md)

---

# 8. Phase VII: direct matrix concentration

## 8.1 Proposition 47 / Experiment AG

[![Weighted Wishart matrix Chernoff](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

**What this figure shows.** Direct matrix concentration for weighted Gaussian Wishart covariance using the projected temporal eigenvalue spectrum.

**Why it matters.** It replaces a sphere-net reduction with a direct matrix-Laplace treatment.

**Verify.** [Proposition 47](proposition_47_weighted_wishart_matrix_chernoff.md) | [Tropp lineage](bibliography.md#tropp-2012)

## 8.2 Proposition 48 / Experiment AH

[![Uniform matrix Chernoff AR1](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

**What this figure shows.** Matrix concentration made uniform over an observed AR(1) confidence interval.

**Why it matters.** The direct matrix theorem remains usable when temporal persistence is uncertain.

**Verify.** [Proposition 48](proposition_48_uniform_matrix_chernoff_ar1.md)

## 8.3 Proposition 49 / Experiment AI

[![Compact temporal family](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

**What this figure shows.** A compact temporal covariance family covered by finitely many certified spectra plus a deterministic interpolation radius.

**Why it matters.** It abstracts the concentration theorem beyond a single AR(1) parameterization.

**Verify.** [Proposition 49](proposition_49_compact_temporal_family.md)

---

# 9. Phase VIII: learning temporal physics from calibration data

## 9.1 Proposition 50 / Experiment AJ

[![Calibrated temporal family](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

**What this figure shows.** A data-calibrated two-parameter temporal family combining persistence and white-noise fraction.

**Why it matters.** The target theorem is conditioned on a family learned from calibration rather than a manually declared parameter point.

**Verify.** [Proposition 50](proposition_50_calibrated_temporal_family.md)

## 9.2 Proposition 51 / Experiment AK

[![E-value temporal confidence set](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

**What this figure shows.** A continuum confidence set obtained by inverting finite-sample likelihood-ratio e-values.

**Why it matters.** It replaces asymptotic parameter estimation with an explicit finite-sample confidence construction.

**Verify.** [Proposition 51](proposition_51_evalue_temporal_confidence_set.md) | [E-value lineage](bibliography.md#vovk-and-wang-2021)

## 9.3 Proposition 52 / Experiment AL

[![Certified e-value outer cover](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md)

**What this figure shows.** A deterministic outer cover of the continuum e-value confidence set and its propagation into an independent target covariance theorem.

**Why it matters.** It creates the bridge from calibration uncertainty to target measurement uncertainty.

**Verify.** [Proposition 52](proposition_52_certified_evalue_outer_cover.md)

---

# 10. Phase IX: sampling consistency and physical-time calibration

## 10.1 Experiment AM: physical relaxation under changing sampling rate

[![Physical relaxation sampling](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

**What this figure shows.** One physical relaxation time \(\tau\) represented at different acquisition intervals.

**Mathematical object.** The sampling-consistent covariance is

\[
K_\tau(t_i,t_j)=e^{-|t_i-t_j|/\tau}.
\]

**Verify.** [Proposition 53A](proposition_53_physical_relaxation_time.md)

## 10.2 Proposition 53A: irregular-grid Markov factorization

[![Irregular-grid Markov factorization](physical_relaxation_markov.svg)](proposition_53_physical_relaxation_time.md)

**What this figure shows.** The exact local innovation structure on irregular timestamps.

For

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

\[
X_{i+1}=\alpha_iX_i+\sqrt{1-\alpha_i^2}\,\varepsilon_i.
\]

**Verify.** [Proposition 53A](proposition_53_physical_relaxation_time.md)

## 10.3 Experiment AN: irregular-time relaxation calibration

[![Irregular-time tau calibration](irregular_relaxation_evalue_calibration.svg)](proposition_53b_irregular_tau_evalue.md)

**What this figure shows.** Finite-sample calibration of the physical relaxation time directly on irregular observation times.

**Why it matters.** The physical parameter is estimated in seconds rather than as a sampling-dependent one-step correlation coefficient.

**Verify.** [Proposition 53B](proposition_53b_irregular_tau_evalue.md)

## 10.4 Experiment AO: two-scale relaxation cover

[![Two-scale relaxation cover](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)

**What this figure shows.** Separate resolution for calibration-set geometry and target temporal-family covering.

**Why it matters.** A fine calibration grid need not force an equally expensive target matrix cover.

**Verify.** [Proposition 54](proposition_54_two_scale_irregular_tau_cover.md)

## 10.5 Experiment AP: quadratic relaxation calibration

[![Quadratic relaxation calibration](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)

**What this figure shows.** First-order and curvature-aware outer covers, target-radius progression, and the exact-\(\tau\) raw-time diagnostic.

**Recorded result.** The calibrated hull contracts to width `0.1646875 s`; the raw-time target radius is `2.41488`, while the exact-\(\tau\) raw-time diagnostic remains `2.16725 > 1`.

**Verify.** [Proposition 55](proposition_55_quadratic_relaxation_calibration.md) | [AP JSON](quadratic_relaxation_calibration.json)

---

# 11. Phase X: exact local innovation target inference

## 11.1 Proposition 56 / Experiment AQ

[![Innovation-whitened target covariance](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

**What this figure shows.** Target covariance concentration after transforming the physical-time process into exact local innovation coordinates.

With exact \(\tau\), after nuisance removal,

\[
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
\]

**Recorded result.** The scalar exact-\(\tau\) target radius contracts from approximately `2.16725` to `0.43647`.

**Verify.** [Proposition 56](proposition_56_innovation_whitened_target.md) | [AQ JSON](innovation_whitened_target.json)

---

# 12. Phase XI: robust innovation inference under calibrated physical time

## 12.1 Proposition 57 / Experiment AR

[![Robust innovation-whitened target covariance](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

**What this figure shows.** The Proposition 55 finite-sample relaxation-time interval propagated through one working innovation whitener.

The transformed family is

\[
C_\tau=W_0R_\tau W_0^{\mathsf T}.
\]

The 0.47.1 tightening keeps the operator/eigenvalue cover unchanged and uses a direct trace-specific certificate for the projected normalization.

**Current recorded result.**

\[
\boxed{
\varepsilon_{57}=0.7195879984<1
}
\]

at combined calibration-target confidence lower bound `0.950625`.

**Verify.** [Proposition 57](proposition_57_robust_innovation_whitening.md) | [AR JSON](robust_innovation_whitened_target.json) | [0.47.1 correction record](release_0_47_1.md)

---

# 13. Phase XII: covariance uncertainty back to world-tube recovery

## 13.1 Proposition 58 / Experiment AS

[![Observer-scale covariance-to-world-tube audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

**What this figure shows.** The dimensional bridge from scalar covariance success back to the full observer-scale moving-boundary problem.

For future candidate \(S\),

\[
B_{t,S}=(X_t,X_{t+1}^{S}),
\]

with

\[
d_{\mathrm{obs}}=n+s.
\]

On the controlled benchmark,

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
\boxed{
d_{\mathrm{obs}}=10,
\qquad
B_{\mathrm{obs}}=175.
}
\]

At 118 residual innovation degrees, the exact-\(\tau\) observer-scale radius is

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

**Why it matters.** The current bottleneck is no longer scalar physical-time calibration. It is observer-scale dimension and structural propagation of covariance uncertainty through the full score.

**Verify.** [Proposition 58](proposition_58_observer_bridge.md) | [AS JSON](observer_bridge_dimension_audit.json) | [Research Index](research_index.md)

---

# 14. Figure inventory

The 33 scientific result figures are distributed as follows:

| Phase | Figures | Count |
| --- | --- | ---: |
| I | baseline recovery, recovery phase diagram | 2 |
| II | finite-sample benchmark, symbolic recovery, perturbed recovery | 3 |
| III | Gaussian screen, structural null, trajectory coupling, relative covariance | 4 |
| IV | cross-fitting, drift robustness, drift comparison, multi-regime calibration | 4 |
| V | dependent Gaussian, centered dependent Gaussian, estimated AR(1) | 3 |
| VI | nuisance projection, estimated AR(1) nuisance projection, design-specific envelope | 3 |
| VII | weighted Wishart, uniform matrix Chernoff, compact temporal family | 3 |
| VIII | calibrated temporal family, e-value confidence set, certified outer cover | 3 |
| IX | physical relaxation sampling, Markov factorization, AN, AO, AP | 5 |
| X | AQ | 1 |
| XI | AR | 1 |
| XII | AS | 1 |
| **Total** |  | **33** |

The explanatory `physics_pipeline.svg` is intentionally excluded from the scientific-result count.

---

# 15. Reading the atlas as one argument

The visual sequence can be summarized as:

```text
moving path can be recovered
        |
finite data make recovery uncertain
        |
screening localizes the candidate family
        |
temporal dependence reduces effective information
        |
nuisance structure must be projected out
        |
direct matrix concentration improves covariance control
        |
temporal physics is calibrated from data
        |
physical time replaces sampling-index time
        |
innovation coordinates recover local information
        |
finite-sample tau uncertainty survives whitening
        |
observer-scale dimension becomes the new bottleneck
```

That progression is the visual structure of the current research program.
