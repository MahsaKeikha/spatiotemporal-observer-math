# Visual research guide

This page is the visual entry point to **Spatiotemporal Observer Mathematics**.

The project is built around one physical question:

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The primary conceptual starting point is Max Tegmark's observer-factorization question in ["Consciousness as a State of Matter"](https://doi.org/10.1016/j.chaos.2015.03.014), with technical preprint [arXiv:1401.1219](https://arxiv.org/abs/1401.1219). The present repository develops a separate operational program for moving subsystem boundaries, recovery, identifiability, finite-sample measurement certification, physical-time calibration, innovation inference, and covariance-to-world-tube recovery.

The word **observer** is operational here. It means a mathematically defined persistent moving subsystem. None of the results on this page prove consciousness or subjective experience. See the [Interpretation Protocol](interpretation_protocol.md).

---

# 1. The complete research arc in one picture

[![Physics to inference pipeline](physics_pipeline.svg)](physics_guide.md)

Read the diagram from physical measurement to inference:

| Stage | Physical question | Mathematical object | Where to read |
| --- | --- | --- | --- |
| Physical observables | What is actually measured? | \(X_t\), units, sensors, timestamps | [Physics Guide](physics_guide.md) |
| Effective dynamics | How do measured degrees of freedom evolve? | \(X_{t+1}=A_tX_t+\varepsilon_t\) | [Derivations](derivations.md) |
| Measurement cleanup | Which deterministic trends must not be mistaken for stochastic structure? | nuisance design \(H\), projection | [P44](proposition_44_nuisance_projection.md) |
| Temporal memory | How much independent information is in repeated measurements? | \(R_\theta\), \(K_\tau\) | [P41-P53 map](research_index.md) |
| Certified covariance | How uncertain is the measured fluctuation geometry? | relative operator radius \(\epsilon\) | [P47-P57 map](research_index.md) |
| Candidate boundary | Which coordinates belong to the candidate subsystem now? | \(S_t\subseteq\{1,\ldots,n\}\) | [Research Overview](research_overview.md) |
| Boundary evidence | Is the candidate integrated, insulated, persistent, and transportable? | information and canonical-correlation factors | [Physics Guide](physics_guide.md) |
| World-tube optimization | Which moving boundary path is globally best? | \(\mathcal W=(S_0,\ldots,S_{T-1})\) | [Proof record](proofs_and_conjectures.md) |
| Recovery and identifiability | Is the best path separated from competitors and statistically distinguishable? | action margin, recovery slack | [P58](proposition_58_observer_bridge.md) |
| Interpretation boundary | What is established, and what is not? | assumptions and bridge hypotheses | [Interpretation Protocol](interpretation_protocol.md) |

The central rule is simple: **the mathematics certifies an inference pipeline; it does not turn a statistical pattern into consciousness by definition.**

---

# 2. A five-minute visual route through the project

For a first reading, follow these six figures in order.

## Step 1. See the moving-boundary problem

[![World-tube baseline](worldtube_baseline.png)](reproducible_results.md)

A planted coherent module moves through measured coordinates as

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The physical organization can persist even though the coordinate labels representing it change.

## Step 2. See when the moving boundary is recoverable

[![World-tube phase diagram](worldtube_phase_diagram.png)](reproducible_results.md)

This figure exposes the recovery landscape rather than presenting one successful example. It shows that recovery depends on dynamical separation and noise, not on the optimizer alone.

## Step 3. Replace a sampling-dependent correlation by physical time

[![Physical relaxation sampling](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

For the declared exponential temporal model,

\[
K_\tau(t_i,t_j)=\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\qquad
\phi_{\Delta t}=e^{-\Delta t/\tau}.
\]

The discrete one-step correlation changes with acquisition rate. The physical relaxation time \(\tau\) does not.

## Step 4. Use the local physical dynamics before covariance concentration

[![Innovation-whitened target covariance](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

With exact \(\tau\), Proposition 53 gives a lower-bidiagonal whitener satisfying

\[
W_\tau R_\tau W_\tau^\mathsf T=I.
\]

Experiment AQ shows why representation matters: on the same scalar target benchmark, the known-\(\tau\) raw-time covariance radius falls from approximately `2.16725` to `0.43644` after innovation whitening.

## Step 5. Keep the innovation advantage when physical time is uncertain

[![Robust innovation whitening](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

Proposition 57 no longer assumes the target relaxation time is known exactly. It carries the finite-sample Proposition 55 interval through one fixed working whitener and obtains a uniform scalar target radius

\[
\epsilon_{57}=0.8677117535<1
\]

on the controlled benchmark.

## Step 6. Return to the original observer-scale question

[![Observer-scale covariance-to-world-tube audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

Experiment AS is the critical reality check. The scalar success of Propositions 56 and 57 does **not** automatically imply an end-to-end observer certificate. On the seven-coordinate moving-module benchmark, observer scoring needs blocks of dimension 10 with 175 simultaneous blocks. Even with exact \(\tau\), the current matrix theorem gives

\[
\epsilon_{\mathrm{observer}}=1.8573569119>1
\]

at 118 residual innovation degrees of freedom.

This negative result is part of the research. It identifies the next theorem frontier as **dimensional and structural**, not another physical-time calibration refinement.

---

# 3. The mathematics behind the visual story

Six objects organize most of the repository.

## 3.1 Adjacent-state covariance

\[
\operatorname{Cov}
\begin{pmatrix}
X_t\\X_{t+1}
\end{pmatrix}
=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^\mathsf T\\
A_t\Sigma_t & A_t\Sigma_tA_t^\mathsf T+Q_t
\end{pmatrix}.
\]

This is the fluctuation geometry from which the Gaussian information quantities are calculated.

## 3.2 Canonical transport

\[
C=\Sigma_X^{-1/2}\Sigma_{XY}\Sigma_Y^{-1/2}.
\]

The singular values quantify predictive transport between collective fluctuation directions after coordinate scale has been removed. The canonical-correlation lineage is [Hotelling 1936](bibliography.md#hotelling-1936).

## 3.3 Moving world-tube objective

For path \(p=(j_0,\ldots,j_{T-1})\),

\[
A(p)=
\sum_t\ell_t(j_t)
+\chi\sum_t\theta_t(j_t,j_{t+1})
-\lambda\sum_t d(j_t,j_{t+1}).
\]

The dynamic-programming lineage is [Bellman 1952](bibliography.md#bellman-1952). The quantity called an `action margin` is an optimization margin, not physical action in joule-seconds.

## 3.4 Relative covariance uncertainty

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

The value \(\epsilon=1\) is a mathematical perturbation threshold. It is not a physical phase transition.

## 3.5 Physical relaxation and irregular-grid innovations

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\qquad
X_{i+1}=\alpha_iX_i+\sqrt{1-\alpha_i^2}\,\varepsilon_i.
\]

The physical stochastic-process lineage is [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and [Doob 1942](bibliography.md#doob-1942).

## 3.6 Covariance-to-world-tube bridge

For a future candidate \(S\), Proposition 58 uses the observer block

\[
B_{t,S}=(X_t,X_{t+1}^{S}),
\qquad
d_{\mathrm{obs}}=n+s.
\]

One such block supports the local factors of \(S\) and every incoming transport edge to \(S\). The number of simultaneous covariance blocks is therefore

\[
B_{\mathrm{obs}}=TC,
\]

rather than the much larger raw candidate-edge count.

For Experiment AS,

\[
n=7,\quad s=3,\quad T=5,\quad C=35,
\]

so

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

The full derivation is in [Proposition 58](proposition_58_observer_bridge.md).

---

# 4. Recent theorem ladder: from physical time back to observer recovery

| Result | Scientific question | Main output | Visual | Full record |
| --- | --- | --- | --- | --- |
| P53 / AM | Is the temporal parameter a physical timescale or a sampling artifact? | sampling-consistent \(\tau\), exact irregular-grid Markov structure | [Figure](physical_relaxation_sampling.svg) | [Proof](proposition_53_physical_relaxation_time.md) |
| P53B / AN | Can \(\tau\) be calibrated directly from irregular finite data? | continuum e-value confidence set | [Figure](irregular_relaxation_evalue_calibration.svg) | [Proof](proposition_53b_irregular_tau_evalue.md) |
| P54 / AO | Can calibration resolution be separated from target-cover resolution? | two-scale certified cover | [Figure](two_scale_irregular_tau_cover.svg) | [Proof](proposition_54_two_scale_irregular_tau_cover.md) |
| P55 / AP | Can observed likelihood curvature tighten finite-sample \(\tau\) calibration? | calibrated hull \([0.686875,0.8515625]\) s; target radius `2.41488` | [Figure](quadratic_relaxation_calibration.svg) | [Proof](proposition_55_quadratic_relaxation_calibration.md) |
| P56 / AQ | Can exact local innovations remove most of the target temporal penalty? | scalar radius `0.43644` with exact \(\tau\) | [Figure](innovation_whitened_target.svg) | [Proof](proposition_56_innovation_whitened_target.md) |
| P57 / AR | Does the innovation advantage survive finite-sample \(\tau\) uncertainty? | uniform scalar radius `0.86771` | [Figure](robust_innovation_whitened_target.svg) | [Proof](proposition_57_robust_innovation_whitening.md) |
| P58 / AS | Can covariance uncertainty be carried back to the moving world-tube objective? | deterministic covariance-to-path bridge and observer-scale bottleneck audit | [Figure](observer_bridge_dimension_audit.svg) | [Proof](proposition_58_observer_bridge.md) |

## Reproducibility links for the current chain

| Result | Machine-readable data | Experiment | Tests | Renderer |
| --- | --- | --- | --- | --- |
| P55 / AP | [JSON](quadratic_relaxation_calibration.json) | [script](../examples/quadratic_relaxation_calibration.py) | [tests](../tests/test_relaxation_curvature.py) | [renderer](../examples/render_quadratic_relaxation_calibration.py) |
| P56 / AQ | [JSON](innovation_whitened_target.json) | [script](../examples/innovation_whitened_target.py) | [tests](../tests/test_innovation_whitening.py) | [renderer](../examples/render_innovation_whitened_target.py) |
| P57 / AR | [JSON](robust_innovation_whitened_target.json) | [script](../examples/robust_innovation_whitened_target.py) | [tests](../tests/test_robust_innovation_whitening.py) | [renderer](../examples/render_robust_innovation_whitened_target.py) |
| P58 / AS | [JSON](observer_bridge_dimension_audit.json) | [script](../examples/observer_bridge_dimension_audit.py) | [tests](../tests/test_observer_bridge.py) | [renderer](../examples/render_observer_bridge_dimension_audit.py) |

---

# 5. Complete scientific figure atlas

Every figure below is part of the public scientific record. Numerical figures illustrate implemented constructions and theorem scale; they do not replace proofs.

## Phase I. Moving-boundary recovery

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![World-tube baseline](worldtube_baseline.png)](reproducible_results.md) | Candidate scores and the recovered moving path | [Results](reproducible_results.md) |
| [![World-tube phase diagram](worldtube_phase_diagram.png)](reproducible_results.md) | Where planted-path recovery succeeds and fails | [Results](reproducible_results.md) |

## Phase II. Finite-sample and perturbation recovery

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Finite-sample benchmark](finite_sample_benchmark.png)](reproducible_results.md) | Recovery under finite covariance estimation | [Results](reproducible_results.md) |
| [![Symbolic recovery region](symbolic_recovery_region.png)](reproducible_results.md) | Analytic recovery region for structured moving systems | [Results](reproducible_results.md) |
| [![Perturbed recovery region](perturbed_recovery_region.png)](reproducible_results.md) | Robustness of the symbolic region to perturbation | [Results](reproducible_results.md) |

## Phase III. Screening and localization

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Gaussian screen calibration](gaussian_screen_calibration.png)](reproducible_results.md) | Safe finite-sample removal of noncompetitive candidates | [Results](reproducible_results.md) |
| [![Structural-null screen](structural_null_screen.png)](reproducible_results.md) | Sharper behavior when exact structural nulls are known | [Results](reproducible_results.md) |
| [![Trajectory-coupled screening](trajectory_coupled_screen_calibration.png)](reproducible_results.md) | Screening when path structure couples states across time | [Results](reproducible_results.md) |
| [![Relative covariance calibration](relative_covariance_calibration.png)](reproducible_results.md) | Population-normalized covariance control | [Results](reproducible_results.md) |

## Phase IV. Cross-fitting, drift, and changing populations

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Cross-fitted relative calibration](cross_fitted_relative_calibration.png)](reproducible_results.md) | Separation of selection and certification information | [Results](reproducible_results.md) |
| [![Drift-robust relative calibration](drift_robust_relative_calibration.png)](reproducible_results.md) | Effect of population drift on covariance certification | [Results](reproducible_results.md) |
| [![Calibrated drift comparison](calibrated_drift_comparison.png)](reproducible_results.md) | Oracle drift, statistically estimated drift, and refreshed reference | [Results](reproducible_results.md) |
| [![Multi-regime coupled calibration](multi_regime_coupled_calibration.png)](reproducible_results.md) | Behavior across several dynamical regimes | [Results](reproducible_results.md) |

## Phase V. Temporally dependent measurements

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Dependent Gaussian calibration](dependent_gaussian_calibration.png)](reproducible_results.md) | Loss of effective information under serial dependence | [Results](reproducible_results.md) |
| [![Dependent centered Gaussian calibration](dependent_centered_gaussian_calibration.png)](reproducible_results.md) | Unknown-mean correction under temporal dependence | [Results](reproducible_results.md) |
| [![Estimated AR1 calibration](estimated_ar1_calibration.png)](reproducible_results.md) | Learning temporal persistence rather than assuming it | [Results](reproducible_results.md) |

## Phase VI. Time-varying nuisance structure

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Nuisance projection](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md) | Removing declared deterministic temporal modes | [P44](proposition_44_nuisance_projection.md) |
| [![Estimated AR1 nuisance projection](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md) | Combining memory calibration with nuisance projection | [P45](proposition_45_estimated_ar1_nuisance_projection.md) |
| [![Design-specific AR1 envelope](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md) | Replacing rank-only pessimism by actual nuisance geometry | [P46](proposition_46_design_specific_ar1_envelope.md) |

## Phase VII. Direct matrix concentration

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Weighted Wishart matrix Chernoff](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md) | Direct matrix-Laplace control using the full temporal spectrum | [P47](proposition_47_weighted_wishart_matrix_chernoff.md) |
| [![Uniform matrix Chernoff AR1](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md) | Uniform matrix concentration over uncertain AR(1) persistence | [P48](proposition_48_uniform_matrix_chernoff_ar1.md) |
| [![Compact temporal family](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md) | Extending the matrix theorem to a covered temporal family | [P49](proposition_49_compact_temporal_family.md) |

## Phase VIII. Learning temporal physics from calibration data

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Calibrated temporal family](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md) | Learning a multi-parameter temporal family on calibration data | [P50](proposition_50_calibrated_temporal_family.md) |
| [![E-value temporal confidence set](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md) | Finite-sample likelihood-compatible temporal models | [P51](proposition_51_evalue_temporal_confidence_set.md) |
| [![Certified e-value outer cover](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md) | Deterministic enclosure of the continuum confidence set | [P52](proposition_52_certified_evalue_outer_cover.md) |

## Phase IX. Sampling consistency and physical-time calibration

| Figure | What to look for | Documentation |
| --- | --- | --- |
| [![Physical relaxation sampling](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md) | Different sampling rates map back to one physical relaxation time | [P53](proposition_53_physical_relaxation_time.md) |
| [![Physical relaxation Markov structure](physical_relaxation_markov.svg)](proposition_53_physical_relaxation_time.md) | Exact local transition, sparse precision, and whitening identities | [P53](proposition_53_physical_relaxation_time.md) |
| [![Irregular relaxation e-value calibration](irregular_relaxation_evalue_calibration.svg)](proposition_53b_irregular_tau_evalue.md) | Finite-sample calibration of \(\tau\) on irregular timestamps | [P53B](proposition_53b_irregular_tau_evalue.md) |
| [![Two-scale irregular tau cover](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md) | Separating calibration resolution from target-cover resolution | [P54](proposition_54_two_scale_irregular_tau_cover.md) |
| [![Quadratic relaxation calibration](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md) | How likelihood slope and curvature tighten the finite-sample hull | [P55](proposition_55_quadratic_relaxation_calibration.md) |

## Phase X. Exact innovation inference

[![Innovation-whitened target](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

The key comparison is raw-time concentration versus exact innovation concentration on the same target schedule.

## Phase XI. Robust innovation inference under calibrated physical time

[![Robust innovation-whitened target](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

The four panels show the finite-sample \(\tau\) interval, one working whitener, the radius comparison, transformed temporal geometry, and the conservatism of the uniform certificate.

## Phase XII. Covariance uncertainty back to world-tube recovery

[![Observer bridge dimension audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

The figure deliberately shows both progress and limitation: the covariance-to-path bridge is explicit, but the current observer-scale matrix and score perturbation chain is still conservative.

---

# 6. How to read a result correctly

The repository uses four different kinds of scientific statements. They should not be conflated.

| Type | Meaning |
| --- | --- |
| **Theorem / proposition** | A mathematical statement proved under explicitly declared assumptions |
| **Controlled numerical experiment** | A reproducible illustration of theorem scale or a controlled recovery construction |
| **Diagnostic** | A calculation designed to expose a bottleneck, failure regime, or conservatism gap |
| **Interpretive hypothesis** | A possible scientific connection requiring additional assumptions and independent tests |

Examples:

- P56's exact Wishart reduction is a theorem under the declared Gaussian model.
- AQ's seeded repeated trials are a visibility check, not the source of the probability guarantee.
- AS's `21,165,400,697` residual-degree calculation is a **conservatism diagnostic**, not a physical sample requirement.
- No covariance radius, integration factor, or world-tube score is claimed to be a measure of consciousness.

---

# 7. Reader routes

## For a physicist

Read in this order:

[Physics Guide](physics_guide.md) -> [Physics Pipeline](physics_pipeline.svg) -> [P53 physical relaxation](proposition_53_physical_relaxation_time.md) -> [P56 innovations](proposition_56_innovation_whitened_target.md) -> [P58 observer bridge](proposition_58_observer_bridge.md) -> [Assumption Ledger](assumption_ledger.md).

Focus on observables, units, sampling schedule, nuisance modes, temporal-model falsification, and what changes under a representation change.

## For a mathematician

Read:

[Derivations](derivations.md) -> [Proof record P1-P43](proofs_and_conjectures.md) -> [P47 matrix concentration](proposition_47_weighted_wishart_matrix_chernoff.md) -> [P49 compact families](proposition_49_compact_temporal_family.md) -> [P53 exact Markov factorization](proposition_53_physical_relaxation_time.md) -> [P58 path bridge](proposition_58_observer_bridge.md).

Focus on invariance, identifiability, perturbation inequalities, exact Gaussian reductions, finite covers, and path-margin propagation.

## For a statistician

Read:

[P41-P52 map](research_index.md) -> [P51 e-values](proposition_51_evalue_temporal_confidence_set.md) -> [P55 quadratic calibration](proposition_55_quadratic_relaxation_calibration.md) -> [P56 exact innovation covariance](proposition_56_innovation_whitened_target.md) -> [P57 robust whitening](proposition_57_robust_innovation_whitening.md) -> [P58](proposition_58_observer_bridge.md).

Focus on failure-budget accounting, calibration-target separation, simultaneous covariance events, matrix concentration, and conservatism diagnostics.

## For a reader coming from Tegmark's work

Read:

[Bibliography and Citation Map](bibliography.md) -> [Research Overview](research_overview.md) -> [World-tube baseline](reproducible_results.md) -> [P58](proposition_58_observer_bridge.md) -> [Interpretation Protocol](interpretation_protocol.md).

The conceptual relation is explicit: Tegmark's factorization question is the starting point; the moving-boundary world-tube program and its finite-sample machinery are independent mathematical developments in this repository.

---

# 8. Current frontier after Proposition 58

Experiment AS shows that the immediate bottleneck is no longer physical-time calibration alone.

On the controlled observer benchmark:

- scalar exact-\(\tau\) innovation radius: `0.436444`;
- observer-scale exact-\(\tau\) radius at 118 residual degrees: `1.857357`;
- first residual degree count at which the current observer-scale matrix theorem enters \(\epsilon<1\): `346`;
- largest current **uniform** relative covariance radius that certifies the population path through the present generic factor-perturbation chain: approximately `1.11e-4`.

The last number is intentionally recorded as a proof-conservatism diagnostic, not as a fundamental data requirement.

The next rigorous directions are therefore:

1. **factor-specific covariance blocks** instead of one maximum-dimensional block for every factor;
2. **screen-first simultaneity reduction** so only genuine near competitors consume the strongest simultaneous guarantee;
3. **candidate-local radii** rather than one global worst-case covariance radius;
4. **direct score-margin concentration** that avoids repeatedly converting covariance error through generic factor-by-factor worst cases;
5. richer temporal models only after the observer-scale structural bottleneck is understood.

This is the current mathematical frontier because it follows directly from the negative diagnostic in Experiment AS.

---

# 9. Audit trail and citation resources

Use these pages to audit the project rather than relying on the visual guide alone:

- [Research Overview](research_overview.md): the scientific story in prose;
- [Research Index](research_index.md): theorem-by-theorem and experiment-by-experiment navigation;
- [Physics Guide](physics_guide.md): physical meaning, units, nuisance terms, and model scope;
- [Assumption Ledger](assumption_ledger.md): assumptions, failure conditions, and what each result requires;
- [Bibliography and Citation Map](bibliography.md): external sources and their exact roles;
- [`references.bib`](../references.bib): machine-readable bibliography;
- [Interpretation Protocol](interpretation_protocol.md): rules for any future observer-to-consciousness interpretation;
- [`CITATION.cff`](../CITATION.cff): repository citation metadata.

A numerical figure is not a proof. A proof is not evidence that its assumptions hold in a real system. A mathematically recovered moving subsystem is not, by that fact alone, a conscious observer.
