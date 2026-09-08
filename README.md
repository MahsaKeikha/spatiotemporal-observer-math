# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.36.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one question:

> **If the subsystem we care about is allowed to move, can its boundary be inferred from the dynamics rather than declared in advance?**

The repository develops that question through exact Gaussian identities, moving-boundary optimization, identifiability results, deterministic robustness certificates, finite-sample concentration, and reproducible numerical studies.

> **Interpretation boundary.** The word "observer" is used here as an operational mathematical name for a persistent moving subsystem boundary. The results do not prove consciousness, subjective experience, or a unique metaphysical observer.

## Verified research state

| Research record | Current state |
| --- | ---: |
| Proved statements | **48 propositions** |
| Reproducible studies | **34 experiments, A-Z and AA-AH** |
| Committed scientific figures | **21 figures** |
| Claim-level tests | **156 / 156 passing** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software release | **0.36.0** |

### Start here

**New reader:** [Research overview](docs/research_overview.md)  
**Complete theorem and experiment map:** [Research index](docs/research_index.md)  
**Detailed proofs 1-43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Latest proofs 44-48:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md)  
**Numerical record:** [Experiments A-AC](docs/reproducible_results.md) · [Experiments AD-AH](docs/research_index.md#latest-experiments-ad-ah)  
**Assumptions and limits:** [Assumption ledger](docs/assumption_ledger.md)

---

# Latest result: matrix concentration with unknown AR(1) dependence

## Experiment AH: a uniform matrix certificate over the calibrated interval

[![Experiment AH: interval-uniform matrix concentration](docs/uniform_matrix_chernoff_ar1.svg)](docs/proposition_48_uniform_matrix_chernoff_ar1.md)

Proposition 47 removed the sphere-net bottleneck when the projected temporal spectrum was known. That left one important oracle assumption: the exact AR(1) coefficient, and therefore the exact projected spectrum, still had to be supplied.

**Proposition 48 removes that oracle requirement inside the current stationary nonnegative AR(1) model class.** It combines observable AR(1) calibration, the actual declared nuisance geometry, Weyl control of every projected temporal eigenvalue between grid points, and the direct matrix Chernoff argument from Proposition 47.

The continuum step is explicit. If `A(phi) = P R_phi P`, Proposition 46 gives a spectral Lipschitz bound for `A(phi)`. Weyl's inequality then bounds every ordered eigenvalue between neighboring AR(1) grid points. Because the exact Gaussian matrix-mgf factors are monotone in each nonnegative temporal eigenvalue, an inflated neighboring grid spectrum dominates the complete between-grid matrix mgf.

Experiment AH uses `N=500`, a four-dimensional covariance block, an affine nuisance design, 97.5% covariance confidence, 17 AR(1) grid points, and 1024 deterministic Chernoff parameters per tail.

| AR(1) interval | Proposition 46 sphere-net radius | Proposition 48 matrix radius | Known midpoint Proposition 47 | Reduction from P46 |
| --- | ---: | ---: | ---: | ---: |
| `[0.05, 0.15]` | `0.812` | **`0.378`** | `0.369` | 53.4% |
| `[0.35, 0.45]` | `1.086` | **`0.473`** | `0.442` | 56.5% |
| `[0.60, 0.70]` | `1.740` | **`0.705`** | `0.619` | 59.5% |
| `[0.70, 0.80]` | `2.409` | **`0.931`** | `0.770` | 61.3% |

The last row is the main practical transition. The previous interval certificate is above one at `2.409`. Proposition 48 stays below one at `0.931` without supplying the exact coefficient. This matters because several downstream relative-covariance perturbation arguments require a certified radius below one.

Two seeded finite-sample visibility checks were also run with a large unknown affine target mean. All 96 recorded target errors were below the Proposition 48 radius at true `phi=0.65`, and all 96 were below it at true `phi=0.75`. Those simulations show numerical scale. They are not the proof.

[Read Proposition 48](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [JSON results](docs/uniform_matrix_chernoff_ar1.json) · [reproduce Experiment AH](examples/uniform_matrix_chernoff_ar1.py) · [claim-level tests](tests/test_uniform_matrix_chernoff.py)

---

# The current proof frontier

The latest five propositions solve five different problems in the dependent Gaussian covariance layer.

## Proposition 44: remove an unknown time-varying mean

[![Experiment AD: nuisance-projected covariance calibration](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md)

For

\[
X=HB+R^{1/2}Z\Sigma^{1/2},
\]

with a fixed, predeclared temporal nuisance design `H`, Proposition 44 projects the nuisance subspace away with

\[
P_H=I-H(H^\mathsf TH)^{-1}H^\mathsf T.
\]

The estimator

\[
\widehat\Sigma_H=
\frac{X^\mathsf TP_HX}{\operatorname{tr}(P_HR)}
\]

is exactly unbiased for the spatial covariance. In Experiment AD, affine drift amplitude grows from 0 to 10 while the projected estimator remains near **0.14 median relative error**. Ordinary constant mean-centering reaches **121.76**.

[Proof](docs/proposition_44_nuisance_projection.md) · [data](docs/nuisance_projection_calibration.json) · [script](examples/nuisance_projection_calibration.py)

## Proposition 45: estimate the temporal dependence

[![Experiment AE: estimated AR(1) dependence with affine nuisance projection](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md)

Proposition 45 combines observable increment-energy calibration of a shared nonnegative AR(1) coefficient with nuisance projection and uncertainty in the projected covariance normalization. In Experiment AE, all **192 / 192** AR(1) intervals contained the true coefficient and all **192 / 192** calibrated covariance errors lay below the stated radius.

The calibrated estimator tracked the inaccessible oracle closely. The experiment also exposed the next problem: at strong correlation, the theorem radius could exceed one even though the estimator itself remained accurate.

[Proof](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [data](docs/estimated_ar1_nuisance_projection.json) · [script](examples/estimated_ar1_nuisance_projection.py)

## Proposition 46: use the actual nuisance geometry

[![Experiment AF: design-specific versus rank-only AR(1) envelopes](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

Proposition 45 used a rank-only worst case for the nuisance subspace. Proposition 46 instead certifies

\[
\operatorname{tr}(P_HR_\phi),\qquad
\|P_HR_\phi P_H\|_F,\qquad
\|P_HR_\phi P_H\|_2
\]

uniformly over an estimated AR(1) interval using the actual declared design `H`. A finite grid is made rigorous between grid points with analytic Lipschitz bounds.

Experiment AF exposes a false-vacuity regime. At nuisance rank `q=25`, the rank-only lower normalization is negative and cannot certify at all, while the design-specific theorem retains a positive lower normalization near **99.75**.

[Proof](docs/proposition_46_design_specific_ar1_envelope.md) · [data](docs/design_specific_ar1_envelope.json) · [script](examples/design_specific_ar1_envelope.py)

## Proposition 47: remove the operator-norm sphere net

[![Experiment AG: matrix concentration](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md)

Proposition 47 operates on a known projected temporal spectrum and replaces the `1/4`-net argument by a direct matrix tail bound. In Experiment AG, the tested covariance radii fall by roughly 52% to 60%, and several strong-correlation cases move back below one.

[Proof](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [data](docs/weighted_wishart_matrix_chernoff.json) · [script](examples/weighted_wishart_matrix_chernoff.py)

## Proposition 48: make the matrix bound observable over the AR(1) interval

[![Experiment AH: interval-uniform matrix concentration](docs/uniform_matrix_chernoff_ar1.svg)](docs/proposition_48_uniform_matrix_chernoff_ar1.md)

Proposition 48 controls the full projected eigenvalue profile between AR(1) grid points and composes that continuum matrix bound with the observable calibration interval and normalization uncertainty. This closes the known-spectrum gap left by Proposition 47 for the current AR(1) model class.

[Proof](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [data](docs/uniform_matrix_chernoff_ar1.json) · [script](examples/uniform_matrix_chernoff_ar1.py)

---

# The theorem ladder

| Proposition | Restriction or conservatism addressed | Result |
| ---: | --- | --- |
| 41 | i.i.d. temporal sampling | separably dependent Gaussian covariance screening |
| 42 | known constant mean | exact covariance normalization after mean removal |
| 43 | known AR(1) coefficient | observable same-record AR(1) calibration |
| 44 | constant target mean | arbitrary fixed-subspace time-varying nuisance mean |
| 45 | known temporal dependence in P44 | estimated AR(1) plus nuisance projection and normalization uncertainty |
| 46 | rank-only nuisance pessimism in P45 | design-specific continuum envelope over the calibrated interval |
| 47 | sphere-net operator-norm reduction | direct weighted-Wishart matrix concentration using the full temporal spectrum |
| 48 | known projected spectrum in P47 | interval-uniform matrix concentration with observable AR(1) calibration |

The full map of Propositions **1-48**, with plain-language descriptions and proof links, is in the [research index](docs/research_index.md).

---

# What is being optimized?

At each time `t`, a candidate subsystem is a coordinate subset `S_t`. A candidate history

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1})
\]

is called an **observer world-tube**.

For the implemented nonstationary linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\]

each candidate receives evidence from four ingredients:

1. **internal integration**: predictive interaction across its weakest internal cut;
2. **environmental insulation**: predictive information that must be imported from outside;
3. **persistence**: continuity of predictive structure into the next state;
4. **transport**: continuity of organization when physical membership changes.

A dynamic program returns the exact maximizing world-tube within the declared candidate family, plus the exact runner-up. Their action difference is the margin used by the deterministic robustness theorems.

## Controlled moving-boundary example

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

| Quantity | Value |
| --- | ---: |
| Planted boundaries recovered | 5 / 5 |
| Winning action | 1.254324 |
| Runner-up action | 1.127903 |
| Exact action margin | 0.126421 |
| Certified uniform score radius | 0.010535 |

| Selected moving path | Regularization and failure region |
| --- | --- |
| [![Candidate scores over time](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#regularization-result) |

The phase diagram includes a failure region deliberately. A scientific record is more useful when it shows where the method stops working than when it only displays successful parameter choices.

---

# Identifiability comes before optimization

A high objective value is not automatically evidence of an identifiable physical boundary. Proposition 14 constructs observationally identical models that assign incompatible boundary labels, producing a one-half maximin ceiling for any observational estimator in that setting.

That result sets the interpretation rule for the project:

> **The repository studies recovery under declared observables, symmetries, and model assumptions. It does not assume that every system possesses one representation-independent intrinsic boundary.**

See the [proof record](docs/proofs_and_conjectures.md) and the [assumption ledger](docs/assumption_ledger.md).

---

# What is established and what is still open

The repository now contains a substantial conditional mathematical pipeline from time-varying Gaussian dynamics to moving-boundary optimization and finite-sample certification. Depending on the theorem layer, it can account for localized covariance perturbations, structural nulls, adaptive screening, population drift, temporally dependent observations, unknown constant means, declared time-varying nuisance means, estimated AR(1) dependence, design-specific nuisance geometry, direct matrix concentration, and interval-uniform control of the full projected temporal spectrum.

It does not yet provide an unrestricted boundary-identification theorem. Important assumptions remain:

- Gaussian observation structure in the statistical concentration layer;
- separable temporal and spatial covariance in the newest dependent-sampling results;
- stationary nonnegative AR(1) temporal dependence for the calibrated interval layer;
- valid standardized calibration channels for estimating that AR(1) coefficient;
- a nuisance design selected before inspecting the same target record;
- no general non-Gaussian, nonseparable, adaptive-nuisance, or fully data-driven spatial-whitening theorem yet.

The immediate statistical frontier is no longer the single-parameter AR(1) composition. A natural next target is a broader stationary dependence class, for example a multi-parameter temporal model or a certified spectral-density envelope, while retaining finite-sample matrix concentration and explicit nuisance projection.

---

# Reproduce and audit

```bash
git clone https://github.com/MahsaKeikha/spatiotemporal-observer-math.git
cd spatiotemporal-observer-math
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Newest experiments:

```bash
python examples/nuisance_projection_calibration.py
python examples/estimated_ar1_nuisance_projection.py
python examples/design_specific_ar1_envelope.py
python examples/weighted_wishart_matrix_chernoff.py
python examples/uniform_matrix_chernoff_ar1.py
```

Every new numerical claim is expected to have a committed script, machine-readable result file, visible figure when useful, and claim-level test coverage. The repository-wide standard is documented in the [research index](docs/research_index.md#reproduction-and-audit-rule).

## Repository map

- [`docs/research_overview.md`](docs/research_overview.md): human-readable research narrative
- [`docs/research_index.md`](docs/research_index.md): canonical theorem and experiment navigation
- [`docs/proofs_and_conjectures.md`](docs/proofs_and_conjectures.md): detailed Propositions 1-43
- [`docs/proposition_44_nuisance_projection.md`](docs/proposition_44_nuisance_projection.md): Proposition 44
- [`docs/proposition_45_estimated_ar1_nuisance_projection.md`](docs/proposition_45_estimated_ar1_nuisance_projection.md): Proposition 45
- [`docs/proposition_46_design_specific_ar1_envelope.md`](docs/proposition_46_design_specific_ar1_envelope.md): Proposition 46
- [`docs/proposition_47_weighted_wishart_matrix_chernoff.md`](docs/proposition_47_weighted_wishart_matrix_chernoff.md): Proposition 47
- [`docs/proposition_48_uniform_matrix_chernoff_ar1.md`](docs/proposition_48_uniform_matrix_chernoff_ar1.md): Proposition 48
- [`docs/reproducible_results.md`](docs/reproducible_results.md): Experiments A-AC
- [`docs/assumption_ledger.md`](docs/assumption_ledger.md): assumptions and failure conditions
- [`src/observer_math/`](src/observer_math/): mathematical implementation
- [`tests/`](tests/): claim-level tests
- [`examples/`](examples/): reproducible studies

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). Current research-software release: **0.36.0**.

## License

MIT. See [`LICENSE`](LICENSE).
