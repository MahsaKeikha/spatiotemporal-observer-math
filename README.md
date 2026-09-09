# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.47.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one dynamical question:

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The project starts from a moving-boundary physical problem and develops the mathematics needed to make that inference accountable: recovery, identifiability, finite-sample covariance certification, temporal-memory calibration, sampling-consistent physical time, innovation inference, and finally a deterministic bridge from covariance uncertainty back to the complete moving world-tube objective.

## Start here

| Reader goal | Best entry point |
| --- | --- |
| Understand the whole project visually | **[Visual Research Guide](docs/visual_research_guide.md)** |
| Understand the physics and units | [Physics Guide](docs/physics_guide.md) |
| Read the scientific story in prose | [Research Overview](docs/research_overview.md) |
| Audit every proposition and experiment | [Research Index](docs/research_index.md) |
| Check assumptions and failure conditions | [Assumption Ledger](docs/assumption_ledger.md) |
| Trace external literature and citations | [Bibliography and Citation Map](docs/bibliography.md) |
| Understand the interpretation boundary | [Interpretation Protocol](docs/interpretation_protocol.md) |

---

# Latest result at a glance: Proposition 58 / Experiment AS

[![Experiment AS: observer-scale covariance-to-world-tube certification audit](docs/observer_bridge_dimension_audit.svg)](docs/proposition_58_observer_bridge.md)

The recent physical-time sequence solved an important scalar covariance problem. Proposition 56 showed that exact local innovation coordinates can reduce the scalar target covariance radius from approximately `2.16725` to `0.43644`. Proposition 57 retained a uniform scalar radius `0.86771 < 1` even when the physical relaxation time was known only through a finite-sample calibrated interval.

**Proposition 58 returns that measurement theory to the original observer problem.** It asks whether simultaneous relative covariance uncertainty on the blocks actually used by the observer score can be propagated through integration, insulation, persistence, transport, and the complete moving world-tube objective without spending another probability budget.

For a future candidate boundary \(S\), define the observer covariance block

\[
\boxed{
B_{t,S}=(X_t,X_{t+1}^{S})
}
\]

with dimension

\[
\boxed{d_{\mathrm{obs}}=n+s.}
\]

On the controlled seven-coordinate moving-module benchmark,

\[
n=7,\qquad s=3,\qquad T=5,\qquad C={7\choose3}=35,
\]

so the observer problem requires

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=TC=175.}
\]

The 4,900 candidate edges reuse these same target-indexed covariance blocks. They do not require 4,900 distinct covariance matrices.

The planted and recovered population path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

with population action margin

\[
0.1264216185.
\]

The crucial observer-scale diagnostic is negative and scientifically informative. Even when the true physical relaxation time is supplied exactly, the current matrix theorem at 118 residual innovation degrees gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

The same theorem first enters the relative perturbation regime at 346 residual innovation degrees, where

\[
\varepsilon=0.9991303523<1.
\]

But crossing one is not sufficient to certify the full world-tube. The current generic end-to-end factor-perturbation chain requires a much smaller uniform covariance radius, approximately

\[
1.11\times10^{-4}.
\]

The corresponding enormous residual-degree calculation is explicitly a **conservatism diagnostic, not a physical sample requirement**.

This identifies the next theorem frontier cleanly: factor-specific covariance blocks, screen-first simultaneity reduction, candidate-local radii, and direct score-margin concentration. The bottleneck is now dimensional and structural, not another refinement of physical-time calibration.

[Full Proposition 58](docs/proposition_58_observer_bridge.md) | [Experiment AS JSON](docs/observer_bridge_dimension_audit.json) | [Experiment AS script](examples/observer_bridge_dimension_audit.py) | [AS renderer](examples/render_observer_bridge_dimension_audit.py) | [Claim-level tests](tests/test_observer_bridge.py)

---

# 1. Research lineage and interpretation boundary

The **primary conceptual source and starting point** is Max Tegmark's paper [**"Consciousness as a State of Matter"**](https://doi.org/10.1016/j.chaos.2015.03.014), with technical preprint [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

Tegmark asks why observers perceive a particular factorization of the physical world and studies information, integration, independence, and dynamics as candidate organizing principles. This repository takes that factorization and observer-identification question in a separate operational direction: the relevant subsystem boundary may change with time and must be inferred from dynamical organization rather than fixed in advance.

The propositions and experiments here are not reproductions of Tegmark's derivations, and no endorsement by Tegmark is implied. The later mathematics also draws on information theory, canonical correlation, dynamic programming, Gaussian and random-matrix concentration, e-value statistics, and classical stochastic relaxation. See the [Bibliography and Citation Map](docs/bibliography.md) and [`references.bib`](references.bib).

The word **observer** is operational here. It means a mathematically defined persistent moving subsystem. The results do **not** prove consciousness or subjective experience. Any future observer-to-consciousness interpretation requires additional bridge assumptions under the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# 2. The complete physical problem in one picture

[![Physics to inference pipeline](docs/physics_pipeline.svg)](docs/physics_guide.md)

The figure is the shortest route through the project:

```text
physical observables
        |
effective dynamics
        |
nuisance and temporal memory
        |
certified covariance geometry
        |
candidate boundary S_t
        |
integration + insulation + persistence + transport
        |
world-tube optimization
        |
margin + identifiability + finite-sample recovery
        |
interpretation boundary
```

At time \(t\), write the measured state as

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}),
\]

with local effective dynamics

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

A candidate subsystem is

\[
S_t\subseteq\{1,\ldots,n\},
\]

and its changing history is

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

called an **observer world-tube** in this repository.

The operational score uses four ideas:

1. **Integration:** internal parts predict one another.
2. **Insulation:** outside variables add comparatively limited predictive information after conditioning on the candidate state.
3. **Persistence:** the organization carries predictive structure into its future.
4. **Transport:** the organization can move into new measured coordinates without losing dynamical continuity.

These are stochastic-dynamical properties, not definitions of consciousness.

---

# 3. Seven equations that organize the program

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

This is the fluctuation geometry from which the Gaussian information quantities are computed.

## 3.2 Canonical transport

\[
C=\Sigma_X^{-1/2}\Sigma_{XY}\Sigma_Y^{-1/2}.
\]

Whitening removes raw coordinate scale so singular values of \(C\) describe predictive transport between collective fluctuation directions.

## 3.3 Moving world-tube objective

For path \(p=(j_0,\ldots,j_{T-1})\),

\[
A(p)
=
\sum_t\ell_t(j_t)
+\chi\sum_t\theta_t(j_t,j_{t+1})
-\lambda\sum_t d(j_t,j_{t+1}).
\]

The first term rewards local candidate quality, the second rewards predictive continuity, and the third penalizes implausibly discontinuous boundary motion.

The quantity called an `action margin` is an optimization margin. It is not physical action in joule-seconds.

## 3.4 Relative covariance certification

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

When \(\epsilon<1\), inverse-covariance perturbation calculations remain in a controlled regime. The value one is a mathematical threshold, not a physical phase transition.

## 3.5 Sampling-consistent physical relaxation

\[
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\qquad
\phi_{\Delta t}=e^{-\Delta t/\tau}.
\]

The physical relaxation time \(\tau\) remains fixed while the discrete one-step correlation changes with acquisition interval.

## 3.6 Exact irregular-grid innovation structure

For

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

Proposition 53 gives

\[
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i,
\]

and an exact lower-bidiagonal temporal whitener

\[
W_\tau R_\tau W_\tau^\mathsf T=I,
\qquad
R_\tau^{-1}=W_\tau^\mathsf T W_\tau.
\]

## 3.7 Observer-scale covariance bridge

For future candidate \(S\), Proposition 58 uses

\[
B_{t,S}=(X_t,X_{t+1}^{S}),
\]

which contains the covariance submatrices needed for that candidate's local factors and all incoming transport edges. A simultaneous covariance certificate on these blocks can therefore be propagated deterministically to a world-tube path certificate without spending a new probability budget.

---

# 4. Current research record

| Research record | Current state |
| --- | ---: |
| Proved statements | **58 propositions** |
| Reproducible studies | **45 experiments, A-Z and AA-AS** |
| Scientific result figures | **33 figures** |
| Claim-level tests | **223 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.47.0** |

The physics pipeline is an explanatory diagram and is not included in the 33 scientific-result figure count.

---

# 5. Complete visual research history

The main page keeps the scientific visual record visible. Each figure links to the documentation that explains what it measures, what theorem or experiment it belongs to, what assumptions it uses, and what it does not establish.

For a curated explanation of every figure, use the **[Visual Research Guide](docs/visual_research_guide.md)**.

## Phase I. Moving-boundary recovery

| Candidate scores and recovered path | Recovery landscape |
| --- | --- |
| [![World-tube baseline](docs/worldtube_baseline.png)](docs/reproducible_results.md) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md) |

A planted module moves through the coordinate system as

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

## Phase II. Finite-sample and perturbation recovery

| Finite-sample benchmark | Symbolic recovery region |
| --- | --- |
| [![Finite-sample benchmark](docs/finite_sample_benchmark.png)](docs/reproducible_results.md) | [![Symbolic recovery region](docs/symbolic_recovery_region.png)](docs/reproducible_results.md) |

[![Perturbed recovery region](docs/perturbed_recovery_region.png)](docs/reproducible_results.md)

## Phase III. Screening and localization

| Gaussian screen calibration | Structural-null screen |
| --- | --- |
| [![Gaussian screen calibration](docs/gaussian_screen_calibration.png)](docs/reproducible_results.md) | [![Structural-null screen](docs/structural_null_screen.png)](docs/reproducible_results.md) |

| Trajectory-coupled screening | Relative covariance calibration |
| --- | --- |
| [![Trajectory-coupled screening](docs/trajectory_coupled_screen_calibration.png)](docs/reproducible_results.md) | [![Relative covariance calibration](docs/relative_covariance_calibration.png)](docs/reproducible_results.md) |

## Phase IV. Cross-fitting, drift, and changing populations

| Cross-fitted calibration | Drift-robust calibration |
| --- | --- |
| [![Cross-fitted relative calibration](docs/cross_fitted_relative_calibration.png)](docs/reproducible_results.md) | [![Drift-robust relative calibration](docs/drift_robust_relative_calibration.png)](docs/reproducible_results.md) |

| Calibrated drift comparison | Multi-regime coupled calibration |
| --- | --- |
| [![Calibrated drift comparison](docs/calibrated_drift_comparison.png)](docs/reproducible_results.md) | [![Multi-regime coupled calibration](docs/multi_regime_coupled_calibration.png)](docs/reproducible_results.md) |

## Phase V. Temporally dependent measurements

| Dependent Gaussian calibration | Unknown-mean dependent calibration |
| --- | --- |
| [![Dependent Gaussian calibration](docs/dependent_gaussian_calibration.png)](docs/reproducible_results.md) | [![Dependent centered Gaussian calibration](docs/dependent_centered_gaussian_calibration.png)](docs/reproducible_results.md) |

[![Estimated AR1 calibration](docs/estimated_ar1_calibration.png)](docs/reproducible_results.md)

## Phase VI. Time-varying nuisance structure

| Proposition 44, Experiment AD | Proposition 45, Experiment AE |
| --- | --- |
| [![Nuisance projection](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md) | [![Estimated AR1 nuisance projection](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md) |

[![Design-specific AR1 envelope](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

## Phase VII. Direct matrix concentration

| Proposition 47, Experiment AG | Proposition 48, Experiment AH |
| --- | --- |
| [![Weighted Wishart matrix Chernoff](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md) | [![Uniform matrix Chernoff AR1](docs/uniform_matrix_chernoff_ar1.svg)](docs/proposition_48_uniform_matrix_chernoff_ar1.md) |

[![Compact temporal family](docs/compact_temporal_family.svg)](docs/proposition_49_compact_temporal_family.md)

## Phase VIII. Learning temporal physics from calibration data

| Proposition 50, Experiment AJ | Proposition 51, Experiment AK |
| --- | --- |
| [![Calibrated temporal family](docs/calibrated_temporal_family.svg)](docs/proposition_50_calibrated_temporal_family.md) | [![E-value temporal confidence set](docs/evalue_temporal_confidence_set.svg)](docs/proposition_51_evalue_temporal_confidence_set.md) |

[![Certified e-value outer cover](docs/certified_evalue_outer_cover.svg)](docs/proposition_52_certified_evalue_outer_cover.md)

## Phase IX. Sampling consistency and physical-time calibration

| Sampling consistency | Irregular-grid Markov factorization |
| --- | --- |
| [![Experiment AM: physical relaxation time](docs/physical_relaxation_sampling.svg)](docs/proposition_53_physical_relaxation_time.md) | [![Proposition 53: irregular-grid Markov factorization](docs/physical_relaxation_markov.svg)](docs/proposition_53_physical_relaxation_time.md) |

[![Experiment AN: finite-sample irregular-time tau calibration](docs/irregular_relaxation_evalue_calibration.svg)](docs/proposition_53b_irregular_tau_evalue.md)

[![Experiment AO: two-scale certified relaxation cover](docs/two_scale_irregular_tau_cover.svg)](docs/proposition_54_two_scale_irregular_tau_cover.md)

[![Experiment AP: quadratic finite-sample relaxation calibration](docs/quadratic_relaxation_calibration.svg)](docs/proposition_55_quadratic_relaxation_calibration.md)

Experiment AP showed why calibration-only tightening was no longer enough: even exact knowledge of \(\tau\) left the old target concentration radius at `2.16725 > 1`.

## Phase X. Exact local innovation target inference

[![Experiment AQ: innovation-whitened target covariance](docs/innovation_whitened_target.svg)](docs/proposition_56_innovation_whitened_target.md)

**Proposition 56 / Experiment AQ:** applying the exact physical-time whitener before nuisance fitting and covariance concentration changes the scalar known-\(\tau\) radius from `2.16725` to approximately `0.43644` on the same 120-sample target.

## Phase XI. Robust innovation inference under calibrated physical time

[![Experiment AR: robust innovation-whitened target covariance](docs/robust_innovation_whitened_target.svg)](docs/proposition_57_robust_innovation_whitening.md)

**Proposition 57 / Experiment AR:** the complete finite-sample Proposition 55 interval is propagated through one fixed working whitener. The scalar target radius becomes

\[
\boxed{0.86771<1}
\]

at combined calibration-target confidence lower bound `0.950625`.

## Phase XII. Covariance uncertainty back to world-tube recovery

[![Experiment AS: observer-scale covariance-to-world-tube audit](docs/observer_bridge_dimension_audit.svg)](docs/proposition_58_observer_bridge.md)

**Proposition 58 / Experiment AS:** the deterministic bridge from simultaneous covariance uncertainty to the world-tube objective is explicit. The experiment then shows that scalar covariance success does not automatically imply observer-scale certification. The next bottleneck is dimensional and structural.

---

# 6. Theorem roadmap, Proposition 1 to Proposition 58

| Layer | Propositions | Main role |
| --- | ---: | --- |
| A | 1-14 | Foundations, transport, recovery, finite-sample stability, identifiability |
| B | 15-31 | Structural compression, moving partitions, overlap classes, localized recovery |
| C | 32-40 | Sample splitting, screening, adaptive calibration, population drift |
| D | 41-52 | Dependent measurements, nuisance projection, matrix concentration, temporal-family calibration |
| E | 53A-53B | Sampling-consistent physical relaxation and irregular-time finite-sample calibration |
| F | 54 | Two-scale physical-time uncertainty propagation |
| G | 55 | Local likelihood slope and curvature for sharper physical-time calibration |
| H | 56 | Exact innovation-whitened target covariance concentration |
| I | 57 | Uniform robust innovation whitening over calibrated physical-time uncertainty |
| J | 58 | Relative covariance uncertainty propagated to observer world-tube recovery |

Detailed proof navigation:

- [Propositions 1 to 43 proof record](docs/proofs_and_conjectures.md)
- [Proposition 44](docs/proposition_44_nuisance_projection.md)
- [Proposition 45](docs/proposition_45_estimated_ar1_nuisance_projection.md)
- [Proposition 46](docs/proposition_46_design_specific_ar1_envelope.md)
- [Proposition 47](docs/proposition_47_weighted_wishart_matrix_chernoff.md)
- [Proposition 48](docs/proposition_48_uniform_matrix_chernoff_ar1.md)
- [Proposition 49](docs/proposition_49_compact_temporal_family.md)
- [Proposition 50](docs/proposition_50_calibrated_temporal_family.md)
- [Proposition 51](docs/proposition_51_evalue_temporal_confidence_set.md)
- [Proposition 52](docs/proposition_52_certified_evalue_outer_cover.md)
- [Proposition 53A](docs/proposition_53_physical_relaxation_time.md)
- [Proposition 53B](docs/proposition_53b_irregular_tau_evalue.md)
- [Proposition 54](docs/proposition_54_two_scale_irregular_tau_cover.md)
- [Proposition 55](docs/proposition_55_quadratic_relaxation_calibration.md)
- [Proposition 56](docs/proposition_56_innovation_whitened_target.md)
- [Proposition 57](docs/proposition_57_robust_innovation_whitening.md)
- [Proposition 58](docs/proposition_58_observer_bridge.md)

---

# 7. Recent physical-time and observer-bridge sequence

| Result | Main question | Controlled result |
| --- | --- | ---: |
| P53B / AN | Can physical relaxation time be calibrated directly on irregular timestamps? | certified finite-sample continuum confidence set |
| P54 / AO | Can calibration and target cover resolutions be separated? | target radius `3.15549 -> 2.57207` |
| P55 / AP | Can likelihood curvature tighten the physical-time set? | calibrated hull width `0.1646875 s`; target radius `2.41488` |
| P56 / AQ | Can exact innovations change the target representation? | scalar `2.16725 -> 0.43644` |
| P57 / AR | Does the gain survive finite-sample \(\tau\) uncertainty? | scalar uniform radius `0.86771` |
| P58 / AS | Can covariance uncertainty return to the full observer objective? | deterministic bridge; observer-scale oracle radius `1.85736 > 1` at current N |

The sequence matters because each new theorem responds to a limitation exposed by the previous one. Negative diagnostics are retained rather than hidden.

---

# 8. What Proposition 58 adds mathematically

Suppose each declared observer block satisfies a simultaneous relative covariance event

\[
\left\|
\Sigma_{t,S}^{-1/2}
(\widehat\Sigma_{t,S}-\Sigma_{t,S})
\Sigma_{t,S}^{-1/2}
\right\|_2
\le\delta_{t,S}<1.
\]

Proposition 58 propagates these candidate-local radii through the operational observer factors.

Let

\[
L(\delta)=-\log(1-\delta).
\]

The generic integration-factor radius is

\[
e_I(\delta)=\min\{1,4L(\delta)\},
\]

and the environmental-independence radius is

\[
e_E(\delta)=
\min\left\{
1,
\frac{n+2s}{s}L(\delta)
\right\}.
\]

Persistence uses the existing relative-covariance canonical-correlation perturbation bound. The local observer score

\[
\ell=(g_Ig_Eg_P)^{1/3}
\]

and transport score

\[
\theta=(g_Eg_P)^{1/2}
\]

then inherit deterministic error radii through the repository's product-root perturbation theorem.

The complete world-tube action is bounded path by path. If the resulting recovery slack is positive, the population path is certified on the same simultaneous covariance event. **Proposition 58 spends no additional probability budget.**

Exact structural integration nulls can use a sharper null-specific refinement when those nulls are declared independently of covariance noise.

---

# 9. What covariance means physically

For a fluctuating multivariate system,

\[
\Sigma=\mathbb E[(X-\mu)(X-\mu)^\top]
\]

describes fluctuation geometry.

- diagonal entries are coordinate variances;
- off-diagonal entries describe co-fluctuation;
- eigenvectors describe collective fluctuation directions;
- eigenvalues describe variance along those directions.

These eigenvalues are **not automatically physical energies**. An energy interpretation requires a separate physical derivation connecting the measured coordinates and covariance to a Hamiltonian, temperature, power spectrum, or another physically defined energetic quantity.

See the [Physics Guide](docs/physics_guide.md) and [Figure Reading Guide](docs/figure_reading_guide.md).

---

# 10. What the repository establishes and does not establish

Under stated assumptions, the repository provides a conditional mathematical pipeline from measured stochastic dynamics to moving-boundary optimization, identifiability, finite-sample covariance certification, and deterministic propagation of covariance uncertainty to world-tube recovery.

It does not establish that every physical system has a unique observer boundary. It does not establish Gaussianity, separability, one exponential relaxation time, or a particular nuisance model in a real experiment without validation. It does not establish consciousness.

Relevant falsification diagnostics include:

- residual temporal correlation inconsistent with the declared or certified temporal family;
- multiple or drifting relaxation times;
- oscillatory or nonmonotone temporal dependence;
- heavy-tailed or non-Gaussian innovations;
- nonseparable space-time covariance;
- calibration-to-target mismatch;
- nuisance modes selected adaptively from the same target noise;
- candidate geometry that does not correspond to physically admissible subsystem boundaries.

A narrow mathematical certificate is meaningful only when the declared physical model survives those checks.

---

# 11. Reproducibility and audit standard

A result is considered complete only when the relevant pieces exist together:

- a physical question when a physical reading is intended;
- a declared measurement model;
- a precise mathematical statement;
- assumptions stated close to the claim;
- proof or derivation;
- implementation;
- claim-level tests;
- reproducible experiment when a numerical comparison is useful;
- machine-readable numerical results;
- visible figure when a figure improves understanding;
- explicit limitations and falsification conditions;
- front-page and index links so the result is discoverable.

For the newest chain:

| Result | Proof | Data | Experiment | Tests | Figure |
| --- | --- | --- | --- | --- | --- |
| P55 / AP | [proof](docs/proposition_55_quadratic_relaxation_calibration.md) | [JSON](docs/quadratic_relaxation_calibration.json) | [script](examples/quadratic_relaxation_calibration.py) | [tests](tests/test_relaxation_curvature.py) | [figure](docs/quadratic_relaxation_calibration.svg) |
| P56 / AQ | [proof](docs/proposition_56_innovation_whitened_target.md) | [JSON](docs/innovation_whitened_target.json) | [script](examples/innovation_whitened_target.py) | [tests](tests/test_innovation_whitening.py) | [figure](docs/innovation_whitened_target.svg) |
| P57 / AR | [proof](docs/proposition_57_robust_innovation_whitening.md) | [JSON](docs/robust_innovation_whitened_target.json) | [script](examples/robust_innovation_whitened_target.py) | [tests](tests/test_robust_innovation_whitening.py) | [figure](docs/robust_innovation_whitened_target.svg) |
| P58 / AS | [proof](docs/proposition_58_observer_bridge.md) | [JSON](docs/observer_bridge_dimension_audit.json) | [script](examples/observer_bridge_dimension_audit.py) | [tests](tests/test_observer_bridge.py) | [figure](docs/observer_bridge_dimension_audit.svg) |

The Markdown style guard rejects Unicode en dash and em dash characters.

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

---

# 12. Current frontier

Proposition 58 changes the next research question.

The project no longer needs another calibration-only theorem as its immediate step. The current observer-scale bottleneck is the combination of block dimension, simultaneous block count, and generic factor-by-factor perturbation.

The next rigorous directions are:

1. **Factor-specific covariance blocks:** certify only the covariance geometry required by each information factor instead of using one maximum-dimensional block everywhere.
2. **Screen-first simultaneity reduction:** use safe screening and near-competitor structure so distant candidates do not consume the strongest simultaneous guarantee.
3. **Candidate-local radii:** preserve heterogeneous uncertainty rather than replacing it by one global worst case.
4. **Direct score-margin concentration:** control the observer score or action difference more directly rather than repeatedly passing through generic intermediate bounds.
5. **Richer temporal physics after the structural bottleneck is understood:** move beyond one stationary exponential timescale without losing finite-sample accountability.

The broader physics frontiers remain sensor-coordinate geometry, spatial coarse graining, intervention-sensitive identifiability, and direct falsification on real measurement systems.

The guiding question remains the same:

> **When does the dynamics itself justify a moving subsystem boundary, and when does the available evidence remain insufficient to identify one?**

---

# 13. Relationship to Tegmark's observer-factorization question

This section makes the intellectual relationship to the project's primary conceptual source explicit. It is not a claim that the results below appear in Tegmark's paper, and it does not imply endorsement by Max Tegmark.

## 13.1 Primary source

The primary conceptual starting point is:

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270.**

- [DOI: 10.1016/j.chaos.2015.03.014](https://doi.org/10.1016/j.chaos.2015.03.014)
- [Technical preprint: arXiv:1401.1219](https://arxiv.org/abs/1401.1219)
- [Repository bibliography entry and role map](docs/bibliography.md#tegmark-2015)

Tegmark studies the problem of factorizing the physical world into subsystems and asks why an observer should correspond to one factorization rather than another. Information, integration, independence, and dynamics are among the organizing ideas considered in that program.

The present work begins from that observer-factorization question and asks a different mathematical question that is not developed as the central construction in Tegmark 2015:

> **What if the subsystem boundary itself is time dependent, and must be inferred as a persistent dynamical object rather than selected once as a static partition?**

That question leads to the moving boundary

\[
S_t\subseteq\{1,\ldots,n\}
\]

and the world-tube

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

The main object of inference is therefore not one partition alone, but a path through a candidate subsystem space.

## 13.2 What is inherited conceptually and what is developed here

| Scientific element | Tegmark 2015 lineage | This repository |
| --- | --- | --- |
| Observer-factorization problem | Primary conceptual source | Adopted as the starting question |
| Information and integration as organizing ideas | Central conceptual background | Used as operational score ingredients |
| Independence from the environment | Central conceptual background | Represented operationally through conditional predictive insulation |
| Dynamics as relevant to observer structure | Conceptual motivation | Made explicit through time-indexed subsystem recovery |
| Time-dependent subsystem boundary \(S_t\) | Not claimed here as a Tegmark result | Central mathematical object developed here |
| World-tube \(\mathcal W=(S_t)_t\) | Not attributed to Tegmark | Defined and optimized in this repository |
| Exact finite-horizon path recovery and runner-up margin | Not attributed to Tegmark | Developed here using dynamic programming and perturbation analysis |
| Recovery modulo symmetry and impossibility under observational equivalence | Not attributed to Tegmark | Formalized in Propositions 13 and 14 |
| Finite-sample covariance-to-path certification | Not attributed to Tegmark | Developed through the statistical theorem chain |
| Physical-time calibration and irregular-grid innovation inference | Not part of the Tegmark factorization derivation | Added here as measurement-certification machinery |
| Claim of consciousness | Tegmark discusses consciousness as a physical-state problem | **Not claimed by this repository** |

This distinction matters. The conceptual lineage is direct, while the mathematical development after the starting question is an independent research program.

## 13.3 The mathematical extension in one picture

```text
Tegmark observer-factorization question
                |
                v
Which subsystem decomposition is physically distinguished?
                |
                v
This repository adds explicit time dependence
                |
                v
S_0 -> S_1 -> ... -> S_{T-1}
                |
                v
integration + insulation + persistence + transport
                |
                v
world-tube optimization
                |
                v
identifiability + finite-sample recovery
                |
                v
physical measurement certification
```

The central extension is therefore not "a new measure of consciousness." It is a mathematical program for **dynamically inferred, time-dependent subsystem boundaries** with explicit recovery, uncertainty, and falsification conditions.

## 13.4 Why the later statistical machinery belongs to the same question

Once a moving subsystem score is defined from covariance-dependent information quantities, finite measurements create an unavoidable physical-statistical problem: the world-tube cannot be trusted unless the covariance geometry feeding the score is itself certified.

That is why the later propositions on temporally dependent measurements, nuisance removal, physical relaxation time, e-value calibration, matrix concentration, and innovation whitening are part of the same research program. They are not separate claims about consciousness. They answer the measurement question underneath the observer-boundary problem:

> **When the data are finite, correlated, irregularly sampled, and subject to nuisance structure, how much confidence can be placed in the dynamical boundary inferred from them?**

Proposition 58 makes that connection explicit by returning simultaneous covariance uncertainty to the integration, insulation, persistence, transport, and complete world-tube objective.

## 13.5 Related Tegmark work

A second relevant source is:

**Max Tegmark. "Improved Measures of Integrated Information." _PLoS Computational Biology_ 12(11) (2016): e1005123.**

- [DOI: 10.1371/journal.pcbi.1005123](https://doi.org/10.1371/journal.pcbi.1005123)
- [Preprint: arXiv:1601.02626](https://arxiv.org/abs/1601.02626)
- [Repository bibliography entry and role map](docs/bibliography.md#related-tegmark-work-tegmark-2016)

That work is relevant background for classifying integrated-information measures and factorization choices. It is not the primary source of the world-tube construction, transport term, recovery theorems, or the finite-sample measurement program developed here.

## 13.6 Interpretation boundary

The repository deliberately separates three statements:

1. **Mathematical statement:** a persistent moving subsystem can be defined, optimized, and under stated assumptions sometimes recovered or certified from dynamical data.
2. **Physical modeling statement:** a real application must validate its observables, dynamics, covariance model, temporal law, nuisance structure, and candidate geometry.
3. **Consciousness statement:** no theorem in this repository establishes that the recovered subsystem is conscious or that its score measures subjective experience.

Any future bridge from operational observer structure to consciousness requires assumptions beyond the mathematics proved here. Those assumptions are tracked in the [Interpretation Protocol](docs/interpretation_protocol.md).

## 13.7 Citation and attribution

For the conceptual origin of the observer-factorization question, cite Tegmark 2015. For integrated-information measure context, cite Tegmark 2016 where relevant. For mathematical or computational results introduced in this repository, cite the repository itself together with the external mathematical sources used by the particular theorem.

The complete proposition-to-literature map is maintained in the [Bibliography and Citation Map](docs/bibliography.md), with machine-readable entries in [`references.bib`](references.bib).

Repository citation metadata are maintained in [`CITATION.cff`](CITATION.cff). GitHub can render that file into standard citation formats.

The attribution rule throughout the project is:

> **Conceptual lineage is cited explicitly; original derivations are identified as repository results; related literature is cited for the methods it supplies; no citation is used to imply endorsement.**
