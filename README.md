# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.34.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research project by **Mahsa Keikha, PhD** on whether a changing subsystem boundary can be identified from dynamical integration, environmental insulation, persistence, and transport across time.

> **Interpretation boundary:** “observer” here is an operational mathematical term for a persistent, moving subsystem boundary. This repository does **not** claim to prove consciousness, subjective experience, or a unique metaphysical observer.

## Current verified research state

| Research record | Verified state |
| --- | ---: |
| Proved statements | **46 propositions** |
| Reproducible numerical studies | **32 experiments, A–Z and AA–AF** |
| Committed scientific figures | **19 figures** |
| Claim-level tests | **145 / 145 passing** |
| Continuous integration | **Python 3.10, 3.11, 3.12** |
| Current release | **0.34.0** |

**Best entry points:** [research overview](docs/research_overview.md) · [proof record](docs/proofs_and_conjectures.md) · [reproducible results](docs/reproducible_results.md) · [experimental protocol](docs/experimental_protocol.md) · [latest Proposition 46 proof](docs/proposition_46_design_specific_ar1_envelope.md)

---

# Latest results — visible first

The newest work attacks practical weaknesses of finite-sample covariance certification for real time series: unknown time-varying means, unknown temporal dependence, and overly pessimistic treatment of nuisance geometry. Propositions 44–46 address those restrictions under an explicit Gaussian separable AR(1) model.

## Experiment AF — the actual nuisance geometry can rescue a certificate

[![Experiment AF: design-specific versus rank-only AR(1) envelopes](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

**Proposition 46** replaces Proposition 45's rank-only worst case with a continuum certificate that uses the actual predeclared nuisance design `H`. It evaluates projected temporal geometry on a finite AR(1) grid and then proves coverage between the grid points using analytic Lipschitz bounds. The grid is therefore a computational device, not an unsupported discretization assumption.

Experiment AF fixes `N=300`, the calibrated interval `phi in [0.75, 0.85]`, and a predeclared low-frequency cosine nuisance basis. As the nuisance rank grows:

- at `q=2`, the covariance radius improves from `4.865` to `4.561`;
- at `q=8`, it improves from `7.764` to `5.021`;
- at `q=16`, it improves from `18.966` to `5.348`;
- at `q=24`, the rank-only normalization collapses to `4`, producing a radius near `629.1`, while the design-specific proof retains normalization above `103.6` and radius about `5.833`;
- at `q=25`, the rank-only lower normalization becomes negative (`-8.33`) and Proposition 45 cannot certify at all, while Proposition 46 retains a positive lower normalization about `99.75` and a finite radius about `5.904`.

The scientific point is structural: **the covariance did not become unidentified merely because the rank-only proof became vacuous.** The proof had discarded the geometry of the nuisance subspace.

[Proof and continuum derivation](docs/proposition_46_design_specific_ar1_envelope.md) · [machine-readable results](docs/design_specific_ar1_envelope.json) · [reproducible script](examples/design_specific_ar1_envelope.py) · [claim-level tests](tests/test_design_interval.py)

## Experiment AE — estimated temporal dependence + time-varying nuisance projection

[![Experiment AE: estimated AR(1) dependence with affine nuisance projection](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md)

**Proposition 45** combines an observable AR(1) confidence interval with a predeclared nuisance projection. The target mean may be an arbitrary unknown element of a fixed temporal subspace such as intercept + linear drift.

In Experiment AE, 20 standardized calibration channels estimate the common nonnegative AR(1) coefficient and a separate four-dimensional target record contains a large unknown affine mean drift. Across **192 seeded trials**:

- all **192 / 192** AR(1) confidence intervals contained the true coefficient;
- all **192 / 192** calibrated projected covariance errors were below the theorem radius;
- median calibrated errors were `0.108`, `0.139`, and `0.170` for true correlations `0.10`, `0.40`, and `0.65`;
- the inaccessible oracle errors were almost identical: `0.109`, `0.140`, and `0.169`;
- ordinary constant mean-centering failed under the affine drift, with median relative covariance error above `61` in every tested regime.

Experiment AE also exposed the next concentration problem: at correlation `0.65`, the median Proposition 45 radius is about `1.217`. Proposition 46 fixes nuisance-geometry pessimism, but the remaining sphere-net covariance constant is still conservative.

[Proof and derivation](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [machine-readable results](docs/estimated_ar1_nuisance_projection.json) · [reproducible script](examples/estimated_ar1_nuisance_projection.py) · [claim-level tests](tests/test_estimated_nuisance.py)

## Experiment AD — arbitrary declared time-varying mean with known dependence

[![Experiment AD: nuisance-projected covariance calibration](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md)

**Proposition 44** replaces ordinary mean-centering by projection away from any fixed, predeclared temporal nuisance design `H`. For

\[
X = HB + R^{1/2}Z\Sigma^{1/2},
\]

with

\[
P_H=I-H(H^\mathsf TH)^{-1}H^\mathsf T,
\]

the estimator

\[
\widehat\Sigma_H=
\frac{X^\mathsf TP_HX}{\operatorname{tr}(P_HR)}
\]

is exactly unbiased for the spatial covariance. The finite-sample population-relative error is controlled by the projected temporal norms

\[
\|P_HRP_H\|_F,
\qquad
\|P_HRP_H\|_2.
\]

Experiment AD uses affine drift amplitudes from `0` to `10`. The projected estimator remains near **0.14 median relative error**, while ordinary constant centering reaches **121.76** median error at the largest drift. All **480 / 480** projected covariance events are covered by the stated radius, and adding an arbitrary further mean inside the declared nuisance subspace changes the estimator only at floating-point precision (`~1e-15`).

[Proof and derivation](docs/proposition_44_nuisance_projection.md) · [machine-readable results](docs/nuisance_projection_calibration.json) · [reproducible script](examples/nuisance_projection_calibration.py) · [claim-level tests](tests/test_nuisance_projection.py)

---

# The current theorem ladder

The most recent propositions form a deliberate sequence rather than isolated numerical claims.

| Proposition | What assumption or pessimism is removed | Result |
| --- | --- | --- |
| **41** | i.i.d. temporal sampling | finite-sample covariance screening for separably dependent Gaussian observations |
| **42** | known constant mean | exact mean-centered normalization under dependent Gaussian sampling |
| **43** | known AR(1) coefficient | same-record finite-sample estimation of a shared nonnegative AR(1) coefficient |
| **44** | constant target mean | arbitrary unknown target mean inside a fixed temporal nuisance subspace |
| **45** | known temporal dependence in Proposition 44 | estimated AR(1) dependence + nuisance projection + normalization uncertainty |
| **46** | rank-only nuisance geometry in Proposition 45 | design-specific continuum envelope over the calibrated AR(1) interval |

The rank-one case of Proposition 45 is regression-tested against Proposition 43. Proposition 46 is separately tested against dense continuum checks: the certified interval envelope contains exact projected temporal quantities at 101 intermediate AR(1) values, not just at the grid nodes.

## Earlier dependence-calibration results

[![Same-record temporal calibration and centered covariance recovery](docs/estimated_ar1_calibration.png)](docs/reproducible_results.md#experiment-ac-same-record-ar1-estimation-and-centered-covariance-calibration)

**Experiment AC / Proposition 43.** Increment energy estimates a shared nonnegative AR(1) coefficient and propagates its interval through centered covariance recovery. The temporal estimate and covariance calculation may reuse the same record; confidence is composed by a union bound rather than an independence assumption. All 896 recorded joint events are covered.

[Complete Experiment AC](docs/reproducible_results.md#experiment-ac-same-record-ar1-estimation-and-centered-covariance-calibration) · [machine-readable results](docs/estimated_ar1_calibration.json)

[![Mean-centered covariance under dependent Gaussian sampling](docs/dependent_centered_gaussian_calibration.png)](docs/reproducible_results.md#experiment-ab-mean-centered-dependent-gaussian-calibration)

**Experiment AB / Proposition 42.** Mean-centering under separable temporal dependence requires the exact normalization `tr(P R)`, not automatically `N-1`. All 896 recorded centered covariance events are covered.

[Complete Experiment AB](docs/reproducible_results.md#experiment-ab-mean-centered-dependent-gaussian-calibration) · [machine-readable results](docs/dependent_centered_gaussian_calibration.json)

[![Relative covariance concentration under dependent Gaussian samples](docs/dependent_gaussian_calibration.png)](docs/reproducible_results.md#experiment-aa-dependent-gaussian-covariance-calibration)

**Experiment AA / Proposition 41.** Stationary temporal dependence reduces effective sample size in a quantitatively explicit way. The dependence-aware radius covers all 896 recorded events; an i.i.d. radius fails badly at high correlation.

[Complete Experiment AA](docs/reproducible_results.md#experiment-aa-dependent-gaussian-covariance-calibration) · [machine-readable results](docs/dependent_gaussian_calibration.json)

---

# Central mathematical question

Most analyses begin by declaring which variables form the system and which form its environment. This project asks a prior question:

> **Can the boundary itself be inferred when the boundary is allowed to move?**

At time `t`, a candidate subsystem is a subset `S_t` of the available variables. Its history is the path

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

called an **observer world-tube**.

For a time-varying linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\]

the repository constructs candidate scores from four ingredients:

1. **internal integration** across the weakest bipartition of the candidate;
2. **environmental insulation**, penalizing predictive information imported from outside;
3. **persistence**, measured through canonical predictive structure into the next state;
4. **transport**, rewarding predictive continuity when the physical membership of the candidate changes.

A dynamic program finds the globally maximizing path, while a second exact calculation finds the runner-up and the **action margin**. That margin becomes a deterministic robustness quantity: if all score perturbations stay below a derived threshold, the selected world-tube cannot change.

## A controlled moving-boundary example

The planted three-variable module moves by one variable at each step:

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The optimizer recovers all five planted boundaries in this construction.

| Quantity | Value |
| --- | ---: |
| Recovered boundaries | 5 / 5 |
| Winning action | 1.254324 |
| Runner-up action | 1.127903 |
| Action margin | 0.126421 |
| Certified uniform score radius | 0.010535 |

| Moving-boundary scores | Regularization / failure region |
| --- | --- |
| [![Candidate scores over time with selected path](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![Recovery over transport and continuity weights](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) |

The phase diagram deliberately includes failure. If changing physical membership is penalized too strongly, the optimizer leaves the moving process. That negative region is part of the scientific record.

---

# Finite-sample recovery and screening

The repository does not stop at population calculations. A long sequence of results builds finite-sample covariance radii, score perturbation bounds, candidate-local certificates, structural-null improvements, safe competitor screening, covariance-normalized screening, drift calibration, and temporal-dependence corrections.

| Finite-sample recovery | Gaussian screening calibration |
| --- | --- |
| [![Finite-sample recovery and internal baselines](docs/finite_sample_benchmark.png)](docs/reproducible_results.md#experiment-c-finite-sample-recovery) | [![Gaussian coverage and retained graph fractions](docs/gaussian_screen_calibration.png)](docs/reproducible_results.md#experiment-s-gaussian-screening-calibration) |

| Covariance-normalized screening | Reusable-pilot adaptive screening |
| --- | --- |
| [![Absolute and covariance-normalized screening comparison](docs/relative_covariance_calibration.png)](docs/reproducible_results.md#experiment-w-covariance-normalized-screening) | [![Reusable pilot geometry and adaptive Gaussian screening](docs/cross_fitted_relative_calibration.png)](docs/reproducible_results.md#experiment-x-reusable-pilot-adaptive-screening) |

| Drift-aware screening | Empirical drift calibration |
| --- | --- |
| [![Pilot-normalized screening under declared covariance drift](docs/drift_robust_relative_calibration.png)](docs/reproducible_results.md#experiment-y-screening-under-declared-population-drift) | [![Estimated drift and refreshed-reference comparison](docs/calibrated_drift_comparison.png)](docs/reproducible_results.md#experiment-z-estimating-drift-versus-refreshing-the-reference) |

The worst-case end-to-end theorem is intentionally conservative. Earlier global bounds required astronomically large sample sizes compared with empirical recovery at hundreds of trajectories. The later localized and screened results reduce that gap substantially, but do not erase it. The repository keeps those discrepancies visible because they identify where the mathematics still needs to improve.

---

# Identifiability comes before optimization

A high score does not make a boundary identifiable. The repository includes explicit impossibility results showing that observationally identical models can assign incompatible subsystem boundaries. Recovery is therefore meaningful only up to scientifically admissible symmetries and only under assumptions that distinguish the candidate boundaries in the observed law.

This matters for the interpretation of every numerical success in the repository: a recovered world-tube is evidence about the stated model class and observables, not a universal proof of an intrinsic boundary independent of representation.

---

# What is solved here, and what is not

The project has now established a substantial **conditional mathematical pipeline**: population observer-like scores, exact path optimization, deterministic margin certificates, finite-sample Gaussian covariance control, candidate screening, temporal dependence correction, unknown constant-mean correction, time-varying nuisance projection, observable AR(1) calibration, and a design-specific continuum treatment of nuisance geometry.

It has **not** solved the unrestricted boundary-identification problem. The current frontier is explicit:

- the latest covariance layer still assumes stationary Gaussian AR(1) temporal dependence;
- calibration channels require known marginal standardization and the assumptions of Proposition 43;
- the nuisance design must be fixed before inspecting the same target record;
- the covariance model remains temporally/spatially separable;
- the current covariance concentration step still uses a conservative sphere-net reduction;
- non-Gaussian, nonseparable, adaptive-design, and fully data-driven spatial-whitening guarantees remain open;
- mathematical observer-like organization is not equivalent to consciousness.

Proposition 46 resolves the rank-only nuisance-geometry gap that was previously listed here. The next proof target is the **matrix concentration layer itself**: exploit the full eigenvalue profile of the projected temporal covariance instead of reducing the Gaussian quadratic-form event through a `1/4` sphere net. A sharper weighted-Wishart matrix bound is the most direct route to reducing the valid radius below one in strongly correlated regimes.

---

# Reproduce the repository

```bash
git clone https://github.com/MahsaKeikha/spatiotemporal-observer-math.git
cd spatiotemporal-observer-math
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Run the three newest experiments directly:

```bash
python examples/nuisance_projection_calibration.py
python examples/estimated_ar1_nuisance_projection.py
python examples/design_specific_ar1_envelope.py
```

Each experiment keeps the numerical output in machine-readable JSON alongside a committed figure and a claim-level test file.

## Repository map

- [`src/observer_math/`](src/observer_math/) — mathematical implementation
- [`tests/`](tests/) — tests tied to scientific claims
- [`examples/`](examples/) — reproducible numerical studies
- [`docs/proofs_and_conjectures.md`](docs/proofs_and_conjectures.md) — central proof record through Proposition 43
- [`docs/proposition_44_nuisance_projection.md`](docs/proposition_44_nuisance_projection.md) — time-varying nuisance projection theorem
- [`docs/proposition_45_estimated_ar1_nuisance_projection.md`](docs/proposition_45_estimated_ar1_nuisance_projection.md) — estimated-dependence extension
- [`docs/proposition_46_design_specific_ar1_envelope.md`](docs/proposition_46_design_specific_ar1_envelope.md) — design-specific continuum theorem
- [`docs/reproducible_results.md`](docs/reproducible_results.md) — Experiments A–AC
- [`docs/nuisance_projection_calibration.json`](docs/nuisance_projection_calibration.json) — Experiment AD data
- [`docs/estimated_ar1_nuisance_projection.json`](docs/estimated_ar1_nuisance_projection.json) — Experiment AE data
- [`docs/design_specific_ar1_envelope.json`](docs/design_specific_ar1_envelope.json) — Experiment AF data
- [`docs/research_overview.md`](docs/research_overview.md) — broader research narrative
- [`docs/experimental_protocol.md`](docs/experimental_protocol.md) — reproducibility and claim-testing protocol

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). The current research-software release is **0.34.0**.

## License

MIT. See [`LICENSE`](LICENSE).
