# Visual research guide

This page is the visual entry point to **Spatiotemporal Observer Mathematics**.

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The primary conceptual starting point is Max Tegmark's observer-factorization question in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014). This repository develops a separate mathematical program for time-dependent subsystem boundaries, recovery, identifiability, finite-sample measurement certification, physical-time calibration, innovation inference, and covariance-to-world-tube recovery.

The word `observer` is operational. None of the figures on this page prove consciousness or subjective experience. See the [Interpretation Protocol](interpretation_protocol.md).

## How to use this page

Each figure is shown with three pieces of information:

- **What you are seeing:** the quantity displayed by the visual.
- **Why it matters:** the scientific question the figure answers.
- **Verify:** the theorem, experiment, or documentation page that supports the visual.

For equations and source provenance, use the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md). For physical meaning and units, use the [Physics Guide](physics_guide.md).

---

# 1. Complete physics-to-inference pipeline

[![Physics to inference pipeline](physics_pipeline.svg)](physics_guide.md)

**What you are seeing:** the full logic from physical observables to effective dynamics, temporal-memory modeling, covariance certification, moving-boundary scoring, path optimization, identifiability, and interpretation.

**Why it matters:** it keeps the theorem sequence tied to one physical inference problem instead of reading like unrelated statistical lemmas.

**Verify:** [Physics Guide](physics_guide.md) and [README](../README.md).

---

# 2. Phase I: moving-boundary recovery

## 2.1 Baseline world-tube recovery

[![World-tube baseline](worldtube_baseline.png)](reproducible_results.md)

**What you are seeing:** candidate scores and the globally recovered path for a planted moving module.

**Why it matters:** this is the simplest visible demonstration that identity can persist while coordinate membership changes.

Planted path:

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

**Verify:** [Reproducible Results](reproducible_results.md).

## 2.2 Recovery phase diagram

[![World-tube phase diagram](worldtube_phase_diagram.png)](reproducible_results.md)

**What you are seeing:** regions where the planted path remains recoverable as model and scoring parameters vary.

**Why it matters:** path recovery is not a yes-or-no property of the algorithm alone. It depends on dynamical separation and the chosen objective geometry.

**Verify:** [Reproducible Results](reproducible_results.md).

---

# 3. Phase II: finite-sample and perturbation recovery

## 3.1 Finite-sample benchmark

[![Finite-sample benchmark](finite_sample_benchmark.png)](reproducible_results.md)

**What you are seeing:** empirical finite-sample recovery behavior as covariance estimates replace population quantities.

**Why it matters:** the moving-boundary objective is only useful if its population structure survives estimation noise.

**Verify:** [Reproducible Results](reproducible_results.md).

## 3.2 Symbolic recovery region

[![Symbolic recovery region](symbolic_recovery_region.png)](reproducible_results.md)

**What you are seeing:** a deterministic region in perturbation space where the population path remains protected.

**Why it matters:** this separates an optimization margin from a finite-sample error budget.

**Verify:** [Reproducible Results](reproducible_results.md).

## 3.3 Perturbed recovery region

[![Perturbed recovery region](perturbed_recovery_region.png)](reproducible_results.md)

**What you are seeing:** how path stability degrades under controlled score and covariance perturbations.

**Why it matters:** it visualizes the margin logic used by the early recovery theorems.

**Verify:** [Reproducible Results](reproducible_results.md).

---

# 4. Phase III: screening and localization

## 4.1 Gaussian screen calibration

[![Gaussian screen calibration](gaussian_screen_calibration.png)](reproducible_results.md)

**What you are seeing:** calibration of a safe screening stage under the declared Gaussian model.

**Why it matters:** screening can reduce the candidate burden before the most expensive simultaneous certification step.

**Verify:** [Reproducible Results](reproducible_results.md).

## 4.2 Structural-null screen

[![Structural-null screen](structural_null_screen.png)](reproducible_results.md)

**What you are seeing:** screening behavior when structural null information is available independently of target noise.

**Why it matters:** exact structural zeros can sometimes sharpen inference without pretending noisy estimates are exact.

**Verify:** [Reproducible Results](reproducible_results.md).

## 4.3 Trajectory-coupled screening

[![Trajectory-coupled screening](trajectory_coupled_screen_calibration.png)](reproducible_results.md)

**What you are seeing:** a screen that respects path structure rather than treating time points as unrelated candidate lists.

**Why it matters:** the object of inference is a path, so candidate reduction should preserve path-level competitors.

**Verify:** [Reproducible Results](reproducible_results.md).

## 4.4 Relative covariance calibration

[![Relative covariance calibration](relative_covariance_calibration.png)](reproducible_results.md)

**What you are seeing:** covariance error after normalization by the population covariance geometry.

**Why it matters:** the relative operator norm

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\]

is the central perturbation quantity used by the later certification chain.

**Verify:** [Reproducible Results](reproducible_results.md).

---

# 5. Phase IV: cross-fitting, drift, and changing populations

## 5.1 Cross-fitted calibration

[![Cross-fitted relative calibration](cross_fitted_relative_calibration.png)](reproducible_results.md)

**What you are seeing:** separation of pilot geometry from target evaluation.

**Why it matters:** using the same noise both to choose a structure and to certify it can invalidate nominal guarantees.

**Verify:** [Reproducible Results](reproducible_results.md).

## 5.2 Drift-robust calibration

[![Drift-robust relative calibration](drift_robust_relative_calibration.png)](reproducible_results.md)

**What you are seeing:** covariance certification with controlled population drift.

**Why it matters:** calibration and target distributions need not be identical, but mismatch must enter the uncertainty budget explicitly.

**Verify:** [Reproducible Results](reproducible_results.md).

## 5.3 Calibrated drift comparison

[![Calibrated drift comparison](calibrated_drift_comparison.png)](reproducible_results.md)

**What you are seeing:** direct comparison of different drift-aware calibration strategies.

**Why it matters:** the figure makes the cost of robustness visible rather than hiding it inside a theorem constant.

**Verify:** [Reproducible Results](reproducible_results.md).

## 5.4 Multi-regime coupled calibration

[![Multi-regime coupled calibration](multi_regime_coupled_calibration.png)](reproducible_results.md)

**What you are seeing:** calibration across multiple related regimes.

**Why it matters:** a physically changing population may require more than one stationary calibration block.

**Verify:** [Reproducible Results](reproducible_results.md).

---

# 6. Phase V: temporally dependent measurements

## 6.1 Dependent Gaussian calibration

[![Dependent Gaussian calibration](dependent_gaussian_calibration.png)](reproducible_results.md)

**What you are seeing:** finite-sample covariance behavior when repeated measurements are temporally correlated.

**Why it matters:** treating correlated samples as independent exaggerates effective information.

**Verify:** [Reproducible Results](reproducible_results.md).

## 6.2 Unknown-mean dependent calibration

[![Dependent centered Gaussian calibration](dependent_centered_gaussian_calibration.png)](reproducible_results.md)

**What you are seeing:** the same dependence problem after an unknown constant mean is removed.

**Why it matters:** deterministic baseline uncertainty consumes degrees of freedom and changes the concentration geometry.

**Verify:** [Reproducible Results](reproducible_results.md).

## 6.3 Estimated AR(1) calibration

[![Estimated AR1 calibration](estimated_ar1_calibration.png)](reproducible_results.md)

**What you are seeing:** temporal persistence estimated from data rather than treated as known.

**Why it matters:** physical-time uncertainty must be propagated instead of silently replaced by a point estimate.

**Verify:** [Reproducible Results](reproducible_results.md).

---

# 7. Phase VI: deterministic nuisance structure

## 7.1 Proposition 44 / Experiment AD

[![Nuisance projection calibration](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

**What you are seeing:** covariance calibration after projection away from a predeclared nuisance subspace.

**Why it matters:** baseline and drift should not be mistaken for stochastic covariance.

**Verify:** [Proposition 44](proposition_44_nuisance_projection.md).

## 7.2 Proposition 45 / Experiment AE

[![Estimated AR1 nuisance projection](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

**What you are seeing:** nuisance removal and temporal-memory estimation combined.

**Why it matters:** real target records can contain both deterministic structure and correlated stochastic residuals.

**Verify:** [Proposition 45](proposition_45_estimated_ar1_nuisance_projection.md).

## 7.3 Proposition 46 / Experiment AF

[![Design-specific AR1 envelope](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

**What you are seeing:** a bound that uses the actual nuisance geometry rather than only its rank.

**Why it matters:** structure-specific geometry can be much less pessimistic than generic worst-case compression.

**Verify:** [Proposition 46](proposition_46_design_specific_ar1_envelope.md).

---

# 8. Phase VII: direct matrix concentration

## 8.1 Proposition 47 / Experiment AG

[![Weighted Wishart matrix Chernoff](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

**What you are seeing:** direct matrix concentration for weighted Gaussian covariance contributions.

**Why it matters:** the full projected temporal spectrum can be used instead of reducing everything to one effective sample-size scalar.

**Verify:** [Proposition 47](proposition_47_weighted_wishart_matrix_chernoff.md).

## 8.2 Proposition 48 / Experiment AH

[![Uniform matrix Chernoff AR1](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

**What you are seeing:** a uniform matrix certificate over an interval of AR(1) persistence values.

**Why it matters:** parameter uncertainty must remain inside the target guarantee.

**Verify:** [Proposition 48](proposition_48_uniform_matrix_chernoff_ar1.md).

## 8.3 Proposition 49 / Experiment AI

[![Compact temporal family](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

**What you are seeing:** finite covering of a compact temporal covariance family.

**Why it matters:** it is the general bridge from deterministic temporal-family covers to uniform target covariance concentration.

**Verify:** [Proposition 49](proposition_49_compact_temporal_family.md).

---

# 9. Phase VIII: learning temporal physics from calibration data

## 9.1 Proposition 50 / Experiment AJ

[![Calibrated temporal family](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

**What you are seeing:** an independently learned temporal covariance family propagated to the target theorem.

**Why it matters:** target covariance inference should account for uncertainty in the temporal law itself.

**Verify:** [Proposition 50](proposition_50_calibrated_temporal_family.md).

## 9.2 Proposition 51 / Experiment AK

[![E-value temporal confidence set](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

**What you are seeing:** a finite-sample continuum confidence set constructed from likelihood-ratio e-values.

**Why it matters:** continuum parameter uncertainty can be handled without a parameterwise union bound.

**Verify:** [Proposition 51](proposition_51_evalue_temporal_confidence_set.md).

## 9.3 Proposition 52 / Experiment AL

[![Certified e-value outer cover](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md)

**What you are seeing:** a deterministic finite outer cover of the continuum e-value confidence set.

**Why it matters:** the continuous calibration result becomes a finite object that can be safely propagated into the independent target theorem.

**Verify:** [Proposition 52](proposition_52_certified_evalue_outer_cover.md).

---

# 10. Phase IX: physical time and irregular sampling

## 10.1 Proposition 53 / Experiment AM: sampling consistency

[![Physical relaxation sampling](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

**What you are seeing:** how discrete correlation changes with sampling interval while the physical relaxation time \(\tau\) remains fixed.

**Why it matters:** a parameter measured in physical time should not change merely because the acquisition rate changes.

**Verify:** [Proposition 53](proposition_53_physical_relaxation_time.md).

## 10.2 Proposition 53: exact irregular-grid Markov structure

[![Physical relaxation Markov factorization](physical_relaxation_markov.svg)](proposition_53_physical_relaxation_time.md)

**What you are seeing:** local transition coefficients, lower-bidiagonal innovation whitening, and tridiagonal precision structure on irregular timestamps.

**Why it matters:** exponential temporal memory can be converted into local innovations using the actual physical time gaps.

**Verify:** [Proposition 53](proposition_53_physical_relaxation_time.md).

## 10.3 Proposition 53B / Experiment AN

[![Irregular relaxation e-value calibration](irregular_relaxation_evalue_calibration.svg)](proposition_53b_irregular_tau_evalue.md)

**What you are seeing:** finite-sample calibration of physical \(\tau\) directly on irregular timestamps.

**Why it matters:** the physical timescale is inferred from the same temporal representation used by the target model.

**Verify:** [Proposition 53B](proposition_53b_irregular_tau_evalue.md).

## 10.4 Proposition 54 / Experiment AO

[![Two-scale irregular tau cover](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)

**What you are seeing:** different resolutions for calibration certification and target propagation.

**Why it matters:** calibration resolution and target computational burden are different mathematical roles and need not be tied to one grid.

**Verify:** [Proposition 54](proposition_54_two_scale_irregular_tau_cover.md).

## 10.5 Proposition 55 / Experiment AP

[![Quadratic relaxation calibration](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)

**What you are seeing:** local slope and curvature information tightening the finite-sample physical-time cover.

**Why it matters:** the retained \(\tau\) hull becomes much narrower, but the raw-time target radius remains above one. This negative result motivates a change of estimator rather than another calibration-only refinement.

**Verify:** [Proposition 55](proposition_55_quadratic_relaxation_calibration.md).

---

# 11. Phase X: exact innovation target inference

## Proposition 56 / Experiment AQ

[![Innovation-whitened target covariance](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

**What you are seeing:** the known-\(\tau\) raw-time target radius compared with the exact innovation-whitened target radius, together with the local whitening geometry and seeded visibility diagnostics.

**Why it matters:** changing the representation before concentration reduces the scalar radius from about

\[
2.16725
\]

to

\[
\boxed{0.43647<1}.
\]

**Verify:** [Proposition 56](proposition_56_innovation_whitened_target.md), [AQ JSON](innovation_whitened_target.json), and [AQ experiment](../examples/innovation_whitened_target.py).

---

# 12. Phase XI: robust innovation inference under calibrated physical time

## Proposition 57 / Experiment AR

[![Robust innovation-whitened target covariance](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

**What you are seeing:** the calibrated physical-time interval, one working whitener, comparison of P55/P56/P57 radii, separate operator and projected-trace covers, and pointwise diagnostics.

**Why it matters:** the exact-target-\(\tau\) assumption is removed while the uniform target theorem remains below one.

Current tightened result:

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

The trace-specific normalization cover is

\[
\boxed{
\delta_d=0.01419745,
}
\]

and the reduction relative to the P55 calibrated raw-time target is about

\[
\boxed{70.2\%}.
\]

**Verify:** [Proposition 57](proposition_57_robust_innovation_whitening.md), [AR JSON](robust_innovation_whitened_target.json), [AR experiment](../examples/robust_innovation_whitened_target.py), and [AR renderer](../examples/render_robust_innovation_whitened_target.py).

---

# 13. Phase XII: covariance uncertainty back to world-tube recovery

## Proposition 58 / Experiment AS

[![Observer-scale covariance-to-world-tube audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

**What you are seeing:** the block dimension and simultaneous covariance burden that arise when scalar covariance theory is returned to the actual observer objective.

For the controlled benchmark,

\[
d_{\mathrm{obs}}=10,
\qquad
B_{\mathrm{obs}}=175.
\]

At 118 residual innovation degrees, the current exact-\(\tau\) observer-scale matrix theorem gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

**Why it matters:** a successful scalar covariance theorem does not automatically certify the full moving-boundary problem. The current bottleneck is dimensional and structural.

**Verify:** [Proposition 58](proposition_58_observer_bridge.md), [AS JSON](observer_bridge_dimension_audit.json), and [AS experiment](../examples/observer_bridge_dimension_audit.py).

---

# 14. How to read the visual record scientifically

The figures fall into four categories:

| Visual type | What it can establish |
| --- | --- |
| controlled population experiment | whether the declared model and algorithm behave as designed in a known synthetic setting |
| finite-sample diagnostic | the scale and conservatism of a theorem on a controlled benchmark |
| certified theorem visualization | a visible representation of a mathematical certificate already proved elsewhere |
| negative diagnostic | a rigorous or controlled indication of where the current theorem is still too conservative or structurally incomplete |

No figure should be used to claim more than its category supports.

The project deliberately preserves negative results, including radii above one and large conservatism gaps. Those results identify the next mathematical bottleneck and prevent the research record from becoming a sequence of only favorable plots.

---

# 15. Recommended next pages

After this visual guide:

1. read the [Physics Guide](physics_guide.md) for physical meaning and units;
2. read the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md) for equation provenance;
3. read the [Research Overview](research_overview.md) for the scientific narrative;
4. use the [Research Index](research_index.md) to enter the detailed theorem pages;
5. use the [Bibliography and Citation Map](bibliography.md) to audit external sources;
6. use the [Assumption Ledger](assumption_ledger.md) and [Interpretation Protocol](interpretation_protocol.md) before making physical or consciousness interpretations.
