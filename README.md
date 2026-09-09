# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.46.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one dynamical question:

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The project begins with moving subsystem boundaries and develops recovery, identifiability, finite-sample certification, temporal-memory calibration, sampling-consistent physical time, exact innovation inference, and now robust innovation-whitened covariance certification under finitely calibrated physical-time uncertainty.

## Latest result at a glance

[![Experiment AR: robust innovation whitening under calibrated physical-time uncertainty](docs/robust_innovation_whitened_target.svg)](docs/proposition_57_robust_innovation_whitening.md)

**Proposition 57 / Experiment AR** removes the exact-target-relaxation-time assumption from Proposition 56 without returning to the much looser raw-time covariance theorem.

Proposition 55 constrains the physical relaxation time to

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s}
\]

at calibration confidence `0.975`. Proposition 57 chooses one working relaxation time from that independent calibration result,

\[
\tau_0=0.76921875\ \mathrm{s},
\]

applies its exact Proposition 53 innovation whitener to the target record and nuisance design, and certifies the entire family

\[
C_\tau=W_0R_\tau W_0^\mathsf T
\]

for every still-admissible true \(\tau\).

On the same 120-sample target used in Experiments AP and AQ:

\[
N=120,\qquad q=2,\qquad N-q=118.
\]

The Proposition 55 calibrated raw-time radius was

\[
\varepsilon_{55}=2.4148799294>1.
\]

The exact-\(\tau\) Proposition 56 innovation radius is approximately

\[
\varepsilon_{56}=0.43647,
\]

and the new **uniform uncertain-\(\tau\)** radius is

\[
\boxed{
\varepsilon_{57}=0.8677117535<1
}.
\]

That is a **64.1% reduction** relative to the Proposition 55 calibrated raw-time theorem while removing the assumption that the true target relaxation time is known exactly. With calibration and target covariance confidence both `0.975`, the combined lower bound is `0.950625`.

[Full Proposition 57 proof](docs/proposition_57_robust_innovation_whitening.md) | [Experiment AR JSON](docs/robust_innovation_whitened_target.json) | [Experiment AR script](examples/robust_innovation_whitened_target.py) | [AR renderer](examples/render_robust_innovation_whitened_target.py) | [Claim-level tests](tests/test_robust_innovation_whitening.py) | [Release 0.46.0](docs/release_0_46.md)

---

# 1. Research lineage and interpretation boundary

The **primary conceptual source and starting point for this research program** is Max Tegmark's paper [**"Consciousness as a State of Matter"**](https://doi.org/10.1016/j.chaos.2015.03.014), with technical preprint [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

Tegmark asks why observers perceive a particular factorization of the physical world and studies information, integration, independence, and dynamics as candidate organizing principles. This repository develops that factorization and observer-identification question in a separate operational direction: time-dependent subsystem boundaries, moving world-tubes, recovery, identifiability, finite-sample certification, temporal-memory uncertainty, physical-time representation, and local innovation inference.

The propositions and experiments here are not reproductions of Tegmark's derivations, and no endorsement by Tegmark is implied. The later mathematics also uses information theory, canonical correlation, dynamic programming, Gaussian and random-matrix concentration, e-value statistics, and classical stochastic relaxation. See the [Bibliography and Citation Map](docs/bibliography.md) and [`references.bib`](references.bib).

The word **observer** is operational here. It means a mathematically defined persistent moving subsystem. The results do **not** prove consciousness or subjective experience. Any future observer-to-consciousness interpretation requires additional bridge assumptions under the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# 2. The complete physical problem in one picture

[![Physics to inference pipeline](docs/physics_pipeline.svg)](docs/physics_guide.md)

Let the measured state be

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}),
\]

with local effective dynamics

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

A candidate subsystem boundary is

\[
S_t\subseteq\{1,\ldots,n\},
\]

and its moving history is

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

# 3. Six equations that organize the program

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

\[
A(p)
=
\sum_t\ell_t(j_t)
+\chi\sum_t\theta_t(j_t,j_{t+1})
-\lambda\sum_t d(j_t,j_{t+1}).
\]

The terms reward local subsystem quality and predictive continuity while penalizing implausibly discontinuous jumps.

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

The physical timescale \(\tau\) stays fixed while the discrete one-step correlation changes with the sampling interval.

## 3.6 Exact and robust irregular-grid innovation whitening

For

\[
\alpha_i=e^{-(t_{i+1}-t_i)/\tau},
\]

Proposition 53 gives

\[
X_{i+1}=\alpha_iX_i+\sqrt{1-\alpha_i^2}\,\varepsilon_i,
\]

with an exact lower-bidiagonal whitener

\[
W_\tau R_\tau W_\tau^\mathsf T=I,
\qquad
R_\tau^{-1}=W_\tau^\mathsf T W_\tau.
\]

Proposition 56 uses this identity directly when \(\tau\) is known. Proposition 57 fixes one calibration-derived working whitener \(W_0\) and certifies the compact family

\[
C_\tau=W_0R_\tau W_0^\mathsf T
\]

over the complete finite-sample calibrated \(\tau\)-interval.

---

# 4. Current verified research record

| Research record | 0.46.0 state |
| --- | ---: |
| Proved statements | **57 propositions** |
| Reproducible studies | **44 experiments, A-Z and AA-AR** |
| Scientific result figures | **32 figures** |
| Claim-level tests | **219 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.46.0** |

The physics pipeline is an explanatory diagram and is not included in the 32 scientific-result figure count.

---

# 5. Complete visual research history

The main page intentionally keeps the scientific visual record visible. Each figure is linked to the documentation that explains what it measures, what assumptions it uses, and what it does not establish.

## Phase I. Moving-boundary recovery

| Candidate scores and recovered path | Recovery landscape |
| --- | --- |
| [![World-tube baseline](docs/worldtube_baseline.png)](docs/reproducible_results.md) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md) |

A planted module moves through measured coordinates as

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

Experiment AP showed why another calibration-only refinement was not enough: even exact knowledge of \(\tau\) left the old target concentration radius at `2.16725 > 1`.

## Phase X. Exact local innovation target inference

### Physical question

If the temporal law is known, can the exact local dynamics be used before covariance concentration so that predictable temporal dependence no longer consumes most of the target information budget?

[![Experiment AQ: innovation-whitened target covariance](docs/innovation_whitened_target.svg)](docs/proposition_56_innovation_whitened_target.md)

**Proposition 56 / Experiment AQ:** applying the exact physical-time whitener to both measurements and the nuisance design turns the target problem into an ordinary Gaussian regression in innovation coordinates. After rank-2 nuisance removal, the 120-sample target has exactly 118 residual Gaussian innovation degrees of freedom. Proposition 47 then applies with 118 unit weights.

**Result:** `2.16725 -> 0.43644`, a `79.86%` radius reduction, crossing `epsilon < 1` on the same benchmark.

**Limitation exposed by AQ:** Proposition 56 assumes exact target \(\tau\). A wrong timescale leaves residual temporal dependence.

## Phase XI. Robust innovation inference under calibrated physical time

### Physical question

How much of the innovation-whitening information gain survives when the true target relaxation time is not known exactly, but only lies in the finite-sample Proposition 55 calibrated interval?

[![Experiment AR: robust innovation-whitened target covariance](docs/robust_innovation_whitened_target.svg)](docs/proposition_57_robust_innovation_whitening.md)

**Proposition 57 / Experiment AR:** use one working whitener selected from the independent calibration result, transform both measurements and nuisance design, and certify the complete transformed temporal covariance family induced by every admissible true \(\tau\).

The theorem combines a deterministic transformed-family operator cover with Proposition 49 matrix concentration. On the same target schedule,

\[
\boxed{
\varepsilon_{57}=0.86771<1
}.
\]

The exact-\(\tau\) advantage is partially lost, as it should be, but the result remains inside the perturbative regime. Relative to the calibrated raw-time Proposition 55 theorem, the robust innovation radius is smaller by approximately `64.1%`.

**What this does not establish:** the exponential one-timescale model still requires physical validation. The midpoint working timescale and current trace envelope are valid choices, not claims of optimality.

---

# 6. Theorem roadmap, Proposition 1 to Proposition 57

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

For detailed proofs:

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

---

# 7. From exact to robust innovation whitening

Let the target record be

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma).
\]

## 7.1 Exact physical time, Proposition 56

If \(\tau\) is known, Proposition 53 gives

\[
W_\tau R_\tau W_\tau^\mathsf T=I.
\]

Define

\[
Z=W_\tau Y,
\qquad
G=W_\tau H,
\]

and

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

## 7.2 Calibrated physical time, Proposition 57

If instead

\[
\tau\in[\tau_-,\tau_+],
\]

choose a calibration-derived working value \(\tau_0\) and its whitener \(W_0\). The transformed temporal family is

\[
C_\tau=W_0R_\tau W_0^\mathsf T.
\]

From the Proposition 53 covariance Lipschitz bound,

\[
\|C_\tau-C_{\tau'}\|_2
\le
\|W_0\|_2^2L_R|\tau-\tau'|.
\]

This gives a certified finite operator cover of the complete transformed family. Proposition 49 then supplies one uniform covariance theorem using a deterministic reference normalization.

For Experiment AR, the comparison is

| Representation | Relative radius |
| --- | ---: |
| calibrated raw time, P55 | 2.41488 |
| exact-tau innovation, P56 | 0.43647 |
| calibrated-tau robust innovation, P57 | 0.86771 |

The difference between `0.43647` and `0.86771` is the explicit finite-sample price of not knowing the physical relaxation time exactly under the current robust envelope.

---

# 8. What covariance means physically

For a fluctuating multivariate system,

\[
\Sigma=\mathbb E[(X-\mu)(X-\mu)^\top]
\]

describes fluctuation geometry.

- diagonal entries are coordinate variances;
- off-diagonal entries describe co-fluctuation;
- eigenvectors describe collective fluctuation directions;
- eigenvalues describe variance along those directions.

These eigenvalues are **not automatically physical energies**. An energy interpretation requires a separate derivation connecting the coordinates and covariance to a Hamiltonian, temperature, power spectrum, or another physically defined energetic quantity.

See the [Physics Guide](docs/physics_guide.md) and [Figure Reading Guide](docs/figure_reading_guide.md).

---

# 9. What the repository establishes and does not establish

Under stated assumptions, the repository provides a conditional mathematical pipeline for moving-boundary optimization, path recovery, identifiability, covariance certification, large-candidate screening, drift handling, temporal-memory uncertainty, nuisance projection, physical-time calibration, irregular-grid Markov factorization, exact known-\(\tau\) innovation inference, and robust innovation-whitened covariance certification over a finite-sample calibrated \(\tau\)-interval.

It does not establish that every physical system has a unique observer boundary. It does not establish Gaussianity, separability, one exponential relaxation time, or a particular nuisance model in a real experiment without validation. It does not establish consciousness.

For Propositions 56 and 57, relevant falsification diagnostics include:

- residual temporal correlation inconsistent with the exact or certified transformed family;
- evidence for multiple or drifting relaxation times;
- oscillatory or nonmonotone temporal dependence;
- heavy-tailed or non-Gaussian innovations;
- nonseparable space-time covariance;
- target/calibration mismatch;
- adaptively selected nuisance modes from the same target noise.

---

# 10. How to read the repository

| If you want to understand... | Start here |
| --- | --- |
| Primary conceptual source and literature lineage | [Bibliography and Citation Map](docs/bibliography.md) |
| Physical meaning of the equations | [Physics Guide](docs/physics_guide.md) |
| Meaning and limitations of figures | [Figure Reading Guide](docs/figure_reading_guide.md) |
| Complete research story | [Research Overview](docs/research_overview.md) |
| Proposition and experiment map | [Research Index](docs/research_index.md) |
| Propositions 1 to 43 | [Proof record](docs/proofs_and_conjectures.md) |
| Proposition 56 | [Exact innovation-whitened target proof](docs/proposition_56_innovation_whitened_target.md) |
| Proposition 57 | [Robust innovation-whitening proof](docs/proposition_57_robust_innovation_whitening.md) |
| Experiment AR data | [Machine-readable AR record](docs/robust_innovation_whitened_target.json) |
| Assumptions and failure conditions | [Assumption Ledger](docs/assumption_ledger.md) |
| Public temporal and sampling API | [Temporal Calibration API](docs/api_temporal_calibration.md) |
| Release 0.46.0 | [0.46.0 Research Record](docs/release_0_46.md) |
| Rules for any future consciousness interpretation | [Interpretation Protocol](docs/interpretation_protocol.md) |

---

# 11. Reproducibility standard

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
- explicit statements of limitations and falsification conditions;
- front-page or index links so the result is discoverable.

The Markdown style guard rejects Unicode en dash and em dash characters.

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

---

# 12. Current frontier

Proposition 55 established a finite-sample physical-time interval. Proposition 56 showed that exact innovation coordinates radically improve target covariance concentration. Proposition 57 now carries the complete Proposition 55 calibrated hull through one fixed working innovation whitener and retains

\[
\varepsilon_{57}=0.86771<1
\]

at combined calibration-target confidence lower bound `0.950625` on the controlled benchmark.

The immediate conceptual frontier therefore returns to the original observer-identification problem:

> **Can this certified post-whitening covariance uncertainty be propagated through integration, insulation, persistence, transport, and world-tube path recovery without discarding its structure in an unnecessarily large generic bound?**

A parallel technical frontier is to tighten Proposition 57 itself. Its current projected-normalization uncertainty uses the conservative bound

\[
(N-q)\delta_\lambda.
\]

A design-specific transformed-family trace theorem may reduce the gap between the pointwise diagnostic radii, approximately `0.404` to `0.580`, and the uniform radius `0.86771`.

The broader physics frontiers remain model falsification beyond one exponential timescale, sensor-coordinate invariance, spatial coarse graining, and intervention-sensitive identifiability.

The guiding question remains:

> **Which inferred structures belong to the underlying dynamical organization, and which are artifacts of measurement representation or insufficient information?**

---

# 13. Citation

The primary conceptual source is:

**Tegmark, M. (2015).** [*Consciousness as a State of Matter*](https://doi.org/10.1016/j.chaos.2015.03.014). *Chaos, Solitons & Fractals*, **76**, 238-270. Technical preprint: [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

The complete literature record is maintained in the [Bibliography and Citation Map](docs/bibliography.md), with machine-readable entries in [`references.bib`](references.bib).

For citation of this repository and research software, see [CITATION.cff](CITATION.cff).

License: [MIT](LICENSE).