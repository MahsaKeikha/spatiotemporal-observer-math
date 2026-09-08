# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.40.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one dynamical question:

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The repository develops that question from first principles. It begins with a moving-boundary dynamical model, defines operational observer-like structure, proves recovery and identifiability statements, develops finite-sample guarantees, and then builds a measurement-certification layer for drift, temporal memory, uncertain covariance, and calibration.

## Conceptual lineage

One important starting point for this research program is Max Tegmark's paper [**"Consciousness as a State of Matter"**](https://doi.org/10.1016/j.chaos.2015.03.014), which asks why observers perceive a particular factorization of the physical world and studies information, integration, independence, and dynamics as candidate organizing principles. The technical preprint is available as [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

This repository does not reproduce Tegmark's results and does not imply his endorsement of the present framework. It takes the factorization and observer-identification problem as a motivating question, then develops a separate operational program around time-dependent subsystem boundaries, moving world-tubes, recovery, identifiability, finite-sample certification, and temporal-memory uncertainty.

The word **observer** is operational here. It refers to a mathematically defined persistent moving subsystem. The results do not prove consciousness or subjective experience. Any future connection to consciousness requires additional bridge assumptions under the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# 1. The complete physical problem in one picture

[![Physics to inference pipeline](docs/physics_pipeline.svg)](docs/physics_guide.md)

Imagine a physical process measured through many coordinates. Depending on the application, a coordinate could represent a voltage, displacement, pressure, neural signal, concentration, position, or another measured degree of freedom.

At time $t$, write the measured state as

$$
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
$$

The local effective dynamics are modeled as

$$
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
$$

The physical reading is:

- $X_t$: measured observables at time $t$;
- $A_t$: effective coupling or propagation over one sampling interval;
- $Q_t$: covariance of unresolved stochastic forcing inside the model;
- $S_t$: a proposed subsystem boundary in the measured coordinate system.

A candidate subsystem is

$$
S_t\subseteq\{1,\ldots,n\}.
$$

The boundary is allowed to move. Its history is

$$
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
$$

which this repository calls an **observer world-tube**.

The term `world-tube` is an analogy for the history of an extended structure through time. It is not a claim that this construction is a relativistic spacetime world tube.

The physical problem is therefore not just to find correlated variables. It is to determine whether a coherent dynamical organization can be followed through changing measured coordinates while remaining distinguishable from competing boundaries and robust to measurement uncertainty.

The operational properties used in the score are:

1. **Integration:** internal parts predict one another.
2. **Insulation:** outside variables add comparatively limited predictive information once the candidate state is known.
3. **Persistence:** the organization carries predictive structure into its future.
4. **Transport:** the organization can move into new coordinates without losing dynamical continuity.

These are properties of a stochastic dynamical model. They are not definitions of consciousness.

For the physical meaning of every major variable, covariance, timescale, nuisance term, and theorem radius, see the **[Physics Guide](docs/physics_guide.md)**.

---

# 2. Core equations and what they mean physically

The repository contains many propositions, but a reader can follow most of the program by keeping five mathematical objects in view.

## 2.1 Adjacent-state covariance

Proposition 1 gives the joint covariance of two neighboring states:

$$
\operatorname{Cov}
\begin{pmatrix}
X_t\\X_{t+1}
\end{pmatrix}
=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^\mathsf T\\
A_t\Sigma_t & A_t\Sigma_tA_t^\mathsf T+Q_t
\end{pmatrix}.
$$

**Physical meaning:** this matrix records the fluctuation geometry at the present time, at the next time, and across the transition between them. It is the statistical object from which the Gaussian information quantities are computed.

## 2.2 Transport between changing boundaries

For present and future candidate coordinates, canonical transport is based on the singular values of

$$
C=\Sigma_X^{-1/2}\Sigma_{XY}\Sigma_Y^{-1/2}.
$$

**Physical meaning:** whitening removes coordinate scale, so the singular values quantify predictive transport between collective fluctuation directions rather than raw amplitude alone.

## 2.3 World-tube objective

For a candidate path $p=(j_0,\ldots,j_{T-1})$, the optimization layer uses an objective of the form

$$
A(p)
=
\sum_{t=0}^{T-1}\ell_t(j_t)
+\chi\sum_{t=0}^{T-2}\theta_t(j_t,j_{t+1})
-\lambda\sum_{t=0}^{T-2}d(j_t,j_{t+1}).
$$

**Physical meaning:** the first term rewards locally coherent subsystem structure, the second rewards predictive continuity across a changing boundary, and the third prevents implausibly discontinuous jumps through the candidate space.

The quantity called an `action margin` in the code is an optimization margin. It is not physical action in joule-seconds.

## 2.4 Covariance certification

Many later propositions reduce measurement uncertainty to

$$
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le \epsilon.
$$

**Physical meaning:** $\epsilon$ measures how uncertain the estimated fluctuation geometry is relative to the true fluctuation geometry under the declared model. It is not an energy, a force, or a consciousness measure.

When $\epsilon<1$, inverse covariance quantities and later Gaussian information calculations remain in a controlled perturbative regime. The value one is a mathematical threshold, not a physical phase transition.

## 2.5 Temporal memory

The simplest recent memory model is

$$
R_\phi(i,j)=\phi^{|i-j|}.
$$

For sampling interval $\Delta t$, an AR(1) approximation can be related to an effective relaxation time by

$$
\tau=-\frac{\Delta t}{\log\phi}.
$$

The two-parameter family used later is

$$
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I.
$$

**Physical meaning:** $\phi$ controls persistence of the correlated component and $\eta$ represents a temporally uncorrelated variance fraction inside this effective model. Real systems may require richer kernels, multiple relaxation times, oscillations, colored noise, or nonstationarity.

---

# 3. Current verified research record

| Research record | Current verified state |
| --- | ---: |
| Proved statements | **52 propositions** |
| Reproducible studies | **38 experiments, A-Z and AA-AL** |
| Scientific result figures | **25 figures** |
| Claim-level tests | **177 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.40.0** |

The physics pipeline is an explanatory diagram and is not included in the 25 scientific-result figure count.

---

# 4. Visual research history

This section keeps the complete scientific visual record visible from the main page. Each group of figures corresponds to one stage of the mathematical program. The figures illustrate implemented constructions and numerical scale. They do not replace the proofs.

## Phase I. Moving-boundary recovery

### Physical question

Can the same dynamical organization be followed when the measured coordinates representing it change with time?

| Candidate scores and recovered path | Recovery landscape |
| --- | --- |
| [![World-tube baseline](docs/worldtube_baseline.png)](docs/reproducible_results.md) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md) |

A planted module moves through the coordinate system as

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

**How to read these figures:** the first shows the changing candidate scores and recovered path. The second shows where recovery succeeds or fails as the objective weights change.

**Physics interpretation:** think of a coherent structure crossing a sensor array. The physical organization can persist even though the sensor labels covering it change.

**What the figures do not establish:** they do not prove that every physical system contains a unique observer-like subsystem. They validate the controlled construction and expose its failure region.

---

## Phase II. Finite-sample and perturbation recovery

### Physical question

If the underlying dynamical structure is real but the measured covariance is noisy or the model is slightly perturbed, when does the recovered moving boundary remain unchanged?

| Finite-sample benchmark | Symbolic recovery region |
| --- | --- |
| [![Finite-sample benchmark](docs/finite_sample_benchmark.png)](docs/reproducible_results.md) | [![Symbolic recovery region](docs/symbolic_recovery_region.png)](docs/reproducible_results.md) |

[![Perturbed recovery region](docs/perturbed_recovery_region.png)](docs/reproducible_results.md)

**How to read these figures:** the plots compare recovery against sample size, model separation, or perturbation strength. The visible failure regions are part of the result.

**Physics interpretation:** the observer-like boundary should not change merely because the experiment is repeated with finite noise, unless the statistical uncertainty is large enough to erase the separation between the best path and its competitors.

---

## Phase III. Screening and localization

### Physical question

When the candidate space is large, can obviously noncompetitive structures be removed without invalidating the confidence statement?

| Gaussian screen calibration | Structural-null screen |
| --- | --- |
| [![Gaussian screen calibration](docs/gaussian_screen_calibration.png)](docs/reproducible_results.md) | [![Structural-null screen](docs/structural_null_screen.png)](docs/reproducible_results.md) |

| Trajectory-coupled screening | Relative covariance calibration |
| --- | --- |
| [![Trajectory-coupled screening](docs/trajectory_coupled_screen_calibration.png)](docs/reproducible_results.md) | [![Relative covariance calibration](docs/relative_covariance_calibration.png)](docs/reproducible_results.md) |

**How to read these figures:** screening is successful only when discarded candidates are guaranteed not to become the maximizing path under the stated uncertainty event.

**Physics interpretation:** these are computational and statistical safeguards. They do not create physical structure. They prevent the search over possible boundaries from becoming either computationally intractable or statistically circular.

---

## Phase IV. Cross-fitting, drift, and changing populations

### Physical question

What happens when calibration, screening, or the population itself changes across the experiment?

| Cross-fitted calibration | Drift-robust calibration |
| --- | --- |
| [![Cross-fitted relative calibration](docs/cross_fitted_relative_calibration.png)](docs/reproducible_results.md) | [![Drift-robust relative calibration](docs/drift_robust_relative_calibration.png)](docs/reproducible_results.md) |

| Calibrated drift comparison | Multi-regime coupled calibration |
| --- | --- |
| [![Calibrated drift comparison](docs/calibrated_drift_comparison.png)](docs/reproducible_results.md) | [![Multi-regime coupled calibration](docs/multi_regime_coupled_calibration.png)](docs/reproducible_results.md) |

**How to read these figures:** they show how confidence changes when nuisance structure or the sampling population is allowed to vary instead of being treated as fixed.

**Physics interpretation:** deterministic drift, changing regimes, and calibration reuse can imitate or obscure covariance structure. These experiments quantify the cost of protecting against those effects.

---

## Phase V. Temporally dependent measurements

### Physical question

A physical record has memory. How much independent information is really present when neighboring samples are correlated?

| Dependent Gaussian calibration | Unknown-mean dependent calibration |
| --- | --- |
| [![Dependent Gaussian calibration](docs/dependent_gaussian_calibration.png)](docs/reproducible_results.md) | [![Dependent centered Gaussian calibration](docs/dependent_centered_gaussian_calibration.png)](docs/reproducible_results.md) |

[![Estimated AR1 calibration](docs/estimated_ar1_calibration.png)](docs/reproducible_results.md)

**How to read these figures:** the relevant comparison is not simply error versus sample count. It is error versus the effective information remaining after temporal correlation is taken into account.

**Physics interpretation:** repeatedly observing the same slowly relaxing fluctuation does not create as much independent information as observing independent realizations. Propositions 41 to 43 formalize this measurement issue.

---

## Phase VI. Time-varying nuisance structure

### Physical question

Can deterministic baseline drift or a known temporal trend be removed without being mistaken for stochastic fluctuation covariance?

| Proposition 44, Experiment AD | Proposition 45, Experiment AE |
| --- | --- |
| [![Nuisance projection](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md) | [![Estimated AR1 nuisance projection](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md) |

[![Design-specific AR1 envelope](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

**How to read these figures:** compare covariance error after the declared nuisance subspace is projected out against the error obtained when the same drift is treated as fluctuation.

**Physics interpretation:** a slow baseline, affine drift, or known instrument trend is not automatically part of the system's stochastic fluctuation geometry. The projection layer separates those declared deterministic modes from covariance estimation.

---

## Phase VII. Direct matrix concentration

### Physical question

Can the entire collective fluctuation geometry be certified more tightly than by checking many separate directions?

| Proposition 47, Experiment AG | Proposition 48, Experiment AH |
| --- | --- |
| [![Weighted Wishart matrix Chernoff](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md) | [![Uniform matrix Chernoff AR1](docs/uniform_matrix_chernoff_ar1.svg)](docs/proposition_48_uniform_matrix_chernoff_ar1.md) |

[![Compact temporal family](docs/compact_temporal_family.svg)](docs/proposition_49_compact_temporal_family.md)

**How to read these figures:** the plotted radius is a bound on relative covariance error under the declared Gaussian temporal model. A smaller radius means a tighter statistical certificate for the whole covariance matrix.

**Physics interpretation:** the theorem is certifying the geometry of measured fluctuations, not claiming those eigenmodes are physical energy modes unless a separate physical derivation says so.

---

## Phase VIII. Learning temporal physics from calibration data

### Physical question

If temporal memory is not known in advance, can an independent calibration experiment determine which memory models remain compatible with the data?

| Proposition 50, Experiment AJ | Proposition 51, Experiment AK |
| --- | --- |
| [![Calibrated temporal family](docs/calibrated_temporal_family.svg)](docs/proposition_50_calibrated_temporal_family.md) | [![E-value temporal confidence set](docs/evalue_temporal_confidence_set.svg)](docs/proposition_51_evalue_temporal_confidence_set.md) |

[![Certified e-value outer cover](docs/certified_evalue_outer_cover.svg)](docs/proposition_52_certified_evalue_outer_cover.md)

**How to read these figures:** Proposition 50 begins with simpler lag-based calibration. Proposition 51 uses the full residual likelihood to define a continuum confidence set. Proposition 52 converts that continuum set into a certified outer cover that can be passed to an independent target covariance theorem.

**Physics interpretation:** the result does not identify one exact temporal law. It propagates uncertainty over all temporal models that the calibration record has not ruled out.

---

# 5. Complete theorem roadmap, Proposition 1 to Proposition 52

The project did not begin at Proposition 41. The temporal calibration results are the latest layer of a longer program.

## Layer A. Foundations and first recovery theory, Propositions 1 to 14

| Proposition | Role in the program | Physical reading |
| ---: | --- | --- |
| 1 | Adjacent-state covariance for time-varying linear Gaussian dynamics | Relates present fluctuations, next-state fluctuations, and one-step coupling |
| 2 | Representation invariance of canonical transport inside declared blocks | Transport should not depend on an invertible change of coordinates inside the same physical block |
| 3 | Bounded transport score | Keeps the operational transport score in a controlled dimensionless range |
| 4 | Finite-horizon path robustness | Converts path separation into tolerance against score error |
| 5 | Componentwise planted-path recovery | Gives a simple sufficient condition for exact moving-path recovery |
| 6 | Finite-sample recovery from uniform score bounds | Connects statistical score accuracy to path recovery probability |
| 7 | Gaussian conditional-information perturbation | Controls information quantities when covariance is uncertain |
| 8 | Canonical-persistence perturbation | Controls predictive persistence when covariance is uncertain |
| 9 | End-to-end Gaussian sample complexity | Connects sample size to correct path recovery under the Gaussian model |
| 10 | Positive-factor geometric-score stability | Recovers sharper local behavior when score factors stay away from zero |
| 11 | Localized finite-sample path certificate | Uses only covariance blocks relevant to each candidate |
| 12 | Parameter-level linear-Gaussian certificate | Connects $A_t$, $Q_t$, covariance, and recovery in one computable chain |
| 13 | Objective identifiability modulo symmetry | Separates true ambiguity from arbitrary coordinate relabeling |
| 14 | Two-model impossibility bound | Shows when observations cannot distinguish incompatible labels |

Detailed proofs: [Propositions 1 to 43 proof record](docs/proofs_and_conjectures.md).

## Layer B. Structural compression and moving-partition theory, Propositions 15 to 31

This layer develops exact competitor structure, symbolic moving-clique recovery, perturbation propagation, structural-null control, overlap classes, influence cones, class compression, interval-certified classes, residual bounds, and screened environmental recovery.

The role of this layer is to replace brute-force enumeration with mathematically certified structure while keeping the moving-boundary problem explicit.

| Proposition range | Main question |
| --- | --- |
| 15 to 20 | Which competitors can actually threaten the optimum, and how robust is a structured moving clique? |
| 21 to 25 | Which covariance blocks and overlap classes can influence a candidate score? |
| 26 to 31 | How can moving partitions, class compression, interval certificates, and environmental screening be combined without losing correctness? |

Detailed proofs: [Propositions 15 to 31](docs/proofs_and_conjectures.md).

## Layer C. Statistical screening and drift, Propositions 32 to 40

| Proposition | Main role |
| ---: | --- |
| 32 | Independent sample-split confidence composition |
| 33 | Gaussian first-split screening safety |
| 34 | Positive-factor refinement of Gaussian screening |
| 35 | Structural-null screening at score boundaries |
| 36 | Trajectory-coupled Gaussian screening |
| 37 | Covariance-normalized Gaussian screening |
| 38 | Pilot-normalized adaptive screening |
| 39 | Drift-robust pilot-normalized screening |
| 40 | Statistically calibrated population drift |

**Physical role:** this layer protects the boundary inference procedure against data reuse, large candidate spaces, and changing population structure before the temporal-memory problem is introduced.

Detailed proofs: [Propositions 32 to 40](docs/proofs_and_conjectures.md).

## Layer D. Dependent measurements and temporal calibration, Propositions 41 to 52

| Proposition | Mathematical question | Physical question |
| ---: | --- | --- |
| 41 | How does temporal dependence alter covariance concentration? | How much independent information is really in a record with memory? |
| 42 | What changes when an unknown constant mean is removed? | How does baseline removal change usable fluctuation information? |
| 43 | Can a shared nonnegative AR(1) coefficient be estimated? | Can persistence be learned instead of assumed? |
| 44 | Can the target mean vary inside a declared temporal subspace? | Can known drift shapes be removed without corrupting fluctuation covariance? |
| 45 | Can temporal calibration and nuisance projection be combined? | Can memory uncertainty and deterministic drift be handled together? |
| 46 | Can actual nuisance geometry replace a rank-only worst case? | Does the real shape of removed drift modes change the information budget? |
| 47 | Can direct matrix concentration replace a sphere-net reduction? | Can the complete fluctuation geometry be certified directly? |
| 48 | Can the matrix bound survive unknown AR(1)? | Does the covariance guarantee survive uncertainty in persistence? |
| 49 | Can a compact temporal family be covered? | Can a full admissible family of memory kernels be propagated safely? |
| 50 | Can a two-parameter temporal family be learned from calibration data? | Can persistence and fast uncorrelated variance be estimated from an independent experiment? |
| 51 | Can full likelihood produce a continuum confidence set? | Which temporal models remain compatible with the complete calibration record? |
| 52 | Can that continuum set be certified for target use? | Can every still-compatible temporal model be carried into an independent target covariance guarantee? |

Direct proof pages: [P44](docs/proposition_44_nuisance_projection.md), [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md), [P46](docs/proposition_46_design_specific_ar1_envelope.md), [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md), [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md), [P49](docs/proposition_49_compact_temporal_family.md), [P50](docs/proposition_50_calibrated_temporal_family.md), [P51](docs/proposition_51_evalue_temporal_confidence_set.md), [P52](docs/proposition_52_certified_evalue_outer_cover.md).

---

# 6. Latest completed result, Proposition 52 and Experiment AL

[![Experiment AL: certified e-value outer cover](docs/certified_evalue_outer_cover.svg)](docs/proposition_52_certified_evalue_outer_cover.md)

## Physical problem

Suppose a calibration experiment tells us which temporal-memory models are still compatible with a physical process. A second independent target record shares those temporal parameters but has its own stochastic fluctuations and declared nuisance drift.

Choosing the single best-fit memory model would understate uncertainty. The target covariance certificate should remain valid for every temporal model the calibration data have not ruled out.

Proposition 51 defines the exact continuum set

$$
\mathcal C_\alpha(Z)
=
\left\{
(\phi,\eta):
\log e_{\phi,\eta}(Z)<\log(1/\alpha)
\right\}.
$$

Proposition 52 constructs a certified retained region $\mathcal O_\alpha(Z)$ and proves

$$
\boxed{
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z)
}.
$$

The retained region can then be propagated to an independent target covariance certificate.

Two different geometric errors are kept separate:

$$
\delta_{\mathrm{eig}}
$$

controls nuisance-compressed temporal eigenvalues, while

$$
\delta_{\mathrm{norm}}
$$

controls projected trace normalization. They answer different mathematical questions and are not interchangeable.

## Experiment AL record

The controlled record uses

$$
\phi_*=0.50,
\qquad
\eta_*=0.01,
$$

with 48 calibration time samples across 256 independent channels. The declared family is

$$
\phi\in[0.30,0.70],
\qquad
\eta\in[0,0.05].
$$

The fixed `121 x 61` grid contains 7,381 cells. In the committed deterministic record:

- 5,325 cells are retained;
- 2,056 cells are certified excluded;
- the target eigenvalue-cover radius is `0.03170414963221639`;
- the target normalization-cover radius is `0.07038592646700755`;
- calibration confidence is `0.975`;
- target covariance confidence is `0.975`;
- the combined confidence lower bound is `0.950625`;
- the final relative target covariance radius is

$$
\boxed{0.8998157009696983<1}.
$$

A separate 128-trial visibility study has median relative error about `0.116`, 95th percentile about `0.304`, and maximum about `0.544`. All 128 displayed errors lie below the theorem radius.

The trials are diagnostics. The guarantee comes from the Proposition 51 e-value result, deterministic cell containment, and conditional Proposition 49 matrix concentration for the independent target record.

[Full proof](docs/proposition_52_certified_evalue_outer_cover.md) | [Machine-readable results](docs/certified_evalue_outer_cover.json) | [Experiment script](examples/certified_evalue_outer_cover.py) | [Figure renderer](examples/render_certified_evalue_outer_cover.py) | [Claim-level tests](tests/test_evalue_outer_cover.py)

---

# 7. What covariance means physically

For a fluctuating multivariate system,

$$
\Sigma
=
\mathbb E[(X-\mu)(X-\mu)^\top]
$$

describes the geometry of fluctuations.

- diagonal entries are coordinate variances;
- off-diagonal entries describe co-fluctuation;
- eigenvectors describe collective fluctuation directions;
- eigenvalues describe variance along those directions.

These eigenvalues are **not automatically physical energies**. An energy interpretation requires a separate derivation connecting the coordinates and covariance to a Hamiltonian, temperature, power spectrum, or another physically defined energetic quantity.

This distinction is enforced throughout the [Physics Guide](docs/physics_guide.md) and [Figure Reading Guide](docs/figure_reading_guide.md).

---

# 8. Identifiability before interpretation

Optimization is not identifiability.

If two admissible models produce the same declared observational law while assigning incompatible labels outside the allowed symmetry class, no estimator using only those observations can uniformly recover both labels.

The standing rule is:

> **Every recovery statement is relative to declared observables, modeling assumptions, candidate families, and admissible symmetries.**

A physically serious application should document observables, units, sampling interval, preprocessing, effective coupling model, nuisance modes, temporal assumptions, candidate geometry, and explicit model-failure tests.

---

# 9. What this repository establishes

Under its stated assumptions, the repository provides a conditional mathematical pipeline for:

- defining observer-like subsystem scores;
- optimizing moving subsystem paths;
- quantifying exact optimization margins;
- proving path stability under deterministic perturbations;
- deriving finite-sample Gaussian covariance guarantees;
- establishing identifiability conditions and impossibility results;
- screening large candidate spaces with explicit confidence accounting;
- handling temporally dependent observations;
- removing declared nuisance means and drifts;
- learning uncertain temporal-memory models from independent calibration data;
- constructing a finite-sample continuum confidence set for a two-parameter temporal family;
- turning that continuum set into a certified finite outer cover;
- propagating retained temporal uncertainty into an independent target covariance certificate.

## What is not established

The repository does not establish that every physical system has a unique observer boundary. It does not establish that Gaussianity, separability, or the current temporal family holds in a particular experiment without validation. It does not establish consciousness.

Any future observer-to-consciousness interpretation must enter as an additional bridge hypothesis and must satisfy the falsifiability, invariance, identifiability, causal, and competing-explanation requirements in the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# 10. How to read the repository

| If you want to understand... | Start here |
| --- | --- |
| The physical meaning of the equations | [Physics Guide](docs/physics_guide.md) |
| What every major figure means | [Figure Reading Guide](docs/figure_reading_guide.md) |
| The complete research story | [Research Overview](docs/research_overview.md) |
| The proposition and experiment map | [Research Index](docs/research_index.md) |
| Propositions 1 to 43 in full detail | [Proof record](docs/proofs_and_conjectures.md) |
| Propositions 44 to 52 | [Research Index](docs/research_index.md) |
| Assumptions and failure conditions | [Assumption Ledger](docs/assumption_ledger.md) |
| Reproduction commands and numerical records | [Reproducible Results](docs/reproducible_results.md) |
| Public temporal-calibration API | [Temporal Calibration API](docs/api_temporal_calibration.md) |
| Rules for any future consciousness interpretation | [Interpretation Protocol](docs/interpretation_protocol.md) |

---

# 11. Reproducibility standard

A result is considered complete here only when the relevant pieces exist together:

- physical problem statement when a physical reading is intended;
- declared measurement model;
- precise mathematical statement;
- assumptions stated close to the claim;
- proof or derivation;
- implementation;
- claim-level tests;
- reproducible experiment when a numerical comparison is useful;
- machine-readable results for committed numerical claims;
- visible figure when a figure improves understanding;
- explicit statement of what the result does not establish;
- front-page or index link so the result is discoverable.

The documentation style check also rejects Unicode en dash and em dash characters in Markdown files.

## Reproduce the repository tests

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Individual experiment commands are listed in [Reproducible Results](docs/reproducible_results.md) and on the proposition-specific proof pages.

---

# 12. Current frontier

The current completed chain ends at Proposition 52. The immediate physics-facing frontier is not simply another statistical inequality. It is to ask which observer-like conclusions survive changes in the way a physical experiment is represented:

- sampling interval;
- irregular sampling times;
- physical units;
- sensor basis;
- spatial resolution;
- coarse graining;
- richer temporal kernels;
- intervention rather than passive observation.

The next physics question can be stated simply:

> **Which inferred structures belong to the underlying dynamical organization, and which are artifacts of how the experiment was sampled, labeled, or represented?**

That question is deliberately kept separate from any claim about consciousness.

---

# 13. Citation and conceptual source

For the conceptual source that motivates the factorization and observer-identification question:

**Tegmark, M. (2015).** [*Consciousness as a State of Matter*](https://doi.org/10.1016/j.chaos.2015.03.014). *Chaos, Solitons & Fractals*, **76**, 238-270. Technical preprint: [arXiv:1401.1219](https://arxiv.org/abs/1401.1219).

For citation of this repository and research software, see [CITATION.cff](CITATION.cff).

License: [MIT](LICENSE).
