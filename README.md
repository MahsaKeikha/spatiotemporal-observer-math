# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.35.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** on a deceptively simple question:

> **If the subsystem we care about is allowed to move, can its boundary be inferred from the dynamics rather than declared in advance?**

The repository develops that question through exact Gaussian identities, moving-boundary optimization, identifiability results, deterministic robustness certificates, finite-sample concentration, and reproducible numerical experiments.

> **Interpretation boundary.** “Observer” is used here as an operational mathematical name for a persistent, moving subsystem boundary. The results do **not** prove consciousness, subjective experience, or a unique metaphysical observer.

## Verified research state

| Research record | Current state |
| --- | ---: |
| Proved statements | **47 propositions** |
| Reproducible studies | **33 experiments, A–Z and AA–AG** |
| Committed scientific figures | **20 figures** |
| Claim-level tests | **150 / 150 passing** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software release | **0.35.0** |

### Start here

**New reader:** [Research overview](docs/research_overview.md)  
**Complete theorem + experiment map:** [Research index](docs/research_index.md)  
**Detailed proofs 1–43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Latest proofs 44–47:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md)  
**Numerical record:** [Experiments A–AC](docs/reproducible_results.md) · [AD–AG index](docs/research_index.md#latest-experiments-adag)  
**Assumptions and limits:** [Assumption ledger](docs/assumption_ledger.md)

---

# The newest result: the strong-correlation barrier was partly a proof artifact

## Experiment AG — direct matrix concentration replaces the sphere net

[![Experiment AG: matrix Chernoff versus sphere-net covariance bounds](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md)

The dependent-Gaussian covariance theory developed in Propositions 41–46 used a standard but conservative route: control every quadratic form on a finite `1/4`-net of the unit sphere, then convert that directional event into an operator-norm event. That introduces the familiar `9^m` factor and an additional constant.

**Proposition 47 removes that step.** For the weighted Gaussian Wishart form produced by temporal dependence and nuisance projection, the matrix exponential moment of every rank-one summand can be evaluated exactly. A matrix-Laplace/Chernoff argument then works directly in operator norm and uses the **full temporal eigenvalue spectrum**, not only its Frobenius and spectral norms.

For a four-dimensional covariance block with an affine nuisance mean and `N=850`:

| AR(1) coefficient | Previous sphere-net radius | Proposition 47 | Reduction |
| ---: | ---: | ---: | ---: |
| `0.10` | `0.579` | **`0.278`** | 52.0% |
| `0.40` | `0.731` | **`0.331`** | 54.7% |
| `0.65` | `1.077` | **`0.459`** | 57.3% |
| `0.80` | `1.630` | **`0.653`** | 59.9% |

The important change is not merely a smaller number. Several downstream relative-covariance perturbation arguments require a radius below one. The previous theorem left the `phi=0.65` and `phi=0.80` cases outside that usable regime; Proposition 47 brings both back below one.

At the shorter record length `N=300`, `phi=0.65`, the same transition happens: **`2.165 → 0.832`**.

A 96-trial seeded numerical check also stayed inside the Proposition 47 radius in that short, strongly correlated setting. That experiment is a scale check, not the proof; the proof is the exact matrix exponential moment plus the matrix-Laplace tail inequality.

[Read Proposition 47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [JSON results](docs/weighted_wishart_matrix_chernoff.json) · [reproduce Experiment AG](examples/weighted_wishart_matrix_chernoff.py) · [claim-level tests](tests/test_matrix_chernoff.py)

---

# The current proof frontier, visually

The latest four propositions solve four different problems. Keeping those roles separate makes the progression easier to audit.

## 44 — remove an unknown time-varying mean

[![Experiment AD: nuisance-projected covariance calibration](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md)

For

\[
X=HB+R^{1/2}Z\Sigma^{1/2},
\]

with a fixed, predeclared temporal nuisance design `H`, Proposition 44 replaces ordinary mean-centering by projection with

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

## 45 — estimate the temporal dependence instead of supplying it

[![Experiment AE: estimated AR(1) dependence with affine nuisance projection](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md)

Proposition 45 combines observable increment-energy calibration of a shared nonnegative AR(1) coefficient with nuisance projection and uncertainty in the projected covariance normalization. In Experiment AE, all **192 / 192** AR(1) intervals contained the true coefficient and all **192 / 192** calibrated covariance errors lay below the stated radius.

The calibrated estimator tracked the inaccessible oracle closely. The experiment also revealed the next problem honestly: at strong correlation the theorem radius could exceed one even though the estimator itself remained accurate.

[Proof](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [data](docs/estimated_ar1_nuisance_projection.json) · [script](examples/estimated_ar1_nuisance_projection.py)

## 46 — use the actual nuisance geometry, not only its rank

[![Experiment AF: design-specific versus rank-only AR(1) envelopes](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

Proposition 45 used a rank-only worst case for the nuisance subspace. Proposition 46 instead certifies

\[
\operatorname{tr}(P_HR_\phi),\qquad
\|P_HR_\phi P_H\|_F,\qquad
\|P_HR_\phi P_H\|_2
\]

uniformly over an estimated AR(1) interval using the **actual declared design `H`**. A finite grid is made rigorous between grid points with analytic Lipschitz bounds; the proof does not assume the worst case occurs at a grid node.

Experiment AF exposes a false-vacuity regime: at nuisance rank `q=25`, the rank-only lower normalization is negative and cannot certify at all, while the design-specific theorem retains a positive lower normalization near **99.75**.

[Proof](docs/proposition_46_design_specific_ar1_envelope.md) · [data](docs/design_specific_ar1_envelope.json) · [script](examples/design_specific_ar1_envelope.py)

## 47 — remove the sphere-net concentration bottleneck

[![Experiment AG: matrix concentration](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md)

Proposition 47 operates on the known projected temporal spectrum and replaces the `1/4`-net argument by a direct matrix tail bound. This is why the strong-correlation radius falls so sharply in Experiment AG.

The remaining composition is now mathematically precise: **make the Proposition 47 matrix bound uniform over the calibrated AR(1) interval from Propositions 45–46.** That is the Proposition 48 target.

---

# The theorem ladder

| Proposition | Restriction or conservatism addressed | Result |
| ---: | --- | --- |
| 41 | i.i.d. temporal sampling | separably dependent Gaussian covariance screening |
| 42 | known constant mean | exact covariance normalization after mean removal |
| 43 | known AR(1) coefficient | observable same-record AR(1) calibration |
| 44 | constant target mean | arbitrary fixed-subspace time-varying nuisance mean |
| 45 | known temporal dependence in P44 | estimated AR(1) + nuisance projection + normalization uncertainty |
| 46 | rank-only nuisance pessimism in P45 | design-specific continuum envelope over the calibrated interval |
| 47 | sphere-net operator-norm reduction | direct weighted-Wishart matrix concentration using the full temporal spectrum |

The full map of Propositions **1–47**, with plain-language descriptions and proof links, is in the [research index](docs/research_index.md).

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

1. **internal integration** — does the candidate have predictive interaction across its weakest internal cut?
2. **environmental insulation** — how much predictive information must be imported from outside?
3. **persistence** — does its predictive structure survive into the next state?
4. **transport** — can that organization continue even if the physical membership changes?

A dynamic program returns the exact maximizing world-tube within the declared candidate family, plus the exact runner-up. Their action difference is the **margin** used by the deterministic robustness theorems.

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

| Selected moving path | Regularization / failure region |
| --- | --- |
| [![Candidate scores over time](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#regularization-result) |

The phase diagram includes a failure region deliberately. A scientific record is more useful when it shows where the method stops working than when it only displays successful parameter choices.

---

# Identifiability comes before optimization

A high objective value is not automatically evidence of an identifiable physical boundary. Proposition 14 constructs observationally identical models that assign incompatible boundary labels, producing a one-half maximin ceiling for any observational estimator in that setting.

That impossibility result is central to the interpretation of the project:

> **The repository studies recovery under declared observables, symmetries, and model assumptions. It does not assume that every system possesses one representation-independent intrinsic boundary.**

See [identifiability results](docs/proofs_and_conjectures.md#proposition-13-objective-identifiability-modulo-symmetry) and the [assumption ledger](docs/assumption_ledger.md).

---

# What is established — and what is still open

The repository now contains a substantial **conditional mathematical pipeline** from time-varying Gaussian dynamics to moving-boundary optimization and finite-sample certification. Depending on the theorem layer being used, it can account for localized covariance perturbations, structural nulls, adaptive screening, population drift, temporally dependent observations, unknown constant means, declared time-varying nuisance means, estimated AR(1) dependence, design-specific nuisance geometry, and direct matrix concentration.

It does **not** yet provide an unrestricted boundary-identification theorem. Important current assumptions remain:

- Gaussian observation structure in the statistical concentration layer;
- separable temporal/spatial covariance in the newest dependent-sampling results;
- stationary nonnegative AR(1) temporal dependence for Propositions 43–46;
- valid standardized calibration channels for estimating that AR(1) coefficient;
- a nuisance design selected before inspecting the same target record;
- a known projected temporal spectrum in Proposition 47;
- no general non-Gaussian, nonseparable, adaptive-nuisance, or fully data-driven spatial-whitening theorem yet.

**Immediate next proof target — Proposition 48:** combine the calibrated AR(1) interval and design-specific geometry of Propositions 45–46 with Proposition 47's direct matrix concentration. The desired result is one observable certificate with unknown time-varying nuisance mean, estimated temporal dependence, actual nuisance geometry, and a matrix radius that remains usable in stronger-correlation regimes.

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
```

Every new numerical claim is expected to have a committed script, machine-readable result file, visible figure when useful, and claim-level test coverage. The repository-wide standard is documented in the [research index](docs/research_index.md#reproduction-and-audit-rule).

## Repository map

- [`docs/research_overview.md`](docs/research_overview.md) — human-readable narrative of the research
- [`docs/research_index.md`](docs/research_index.md) — canonical theorem/experiment navigation
- [`docs/proofs_and_conjectures.md`](docs/proofs_and_conjectures.md) — detailed Propositions 1–43
- [`docs/proposition_44_nuisance_projection.md`](docs/proposition_44_nuisance_projection.md) — Proposition 44
- [`docs/proposition_45_estimated_ar1_nuisance_projection.md`](docs/proposition_45_estimated_ar1_nuisance_projection.md) — Proposition 45
- [`docs/proposition_46_design_specific_ar1_envelope.md`](docs/proposition_46_design_specific_ar1_envelope.md) — Proposition 46
- [`docs/proposition_47_weighted_wishart_matrix_chernoff.md`](docs/proposition_47_weighted_wishart_matrix_chernoff.md) — Proposition 47
- [`docs/reproducible_results.md`](docs/reproducible_results.md) — detailed Experiments A–AC
- [`docs/assumption_ledger.md`](docs/assumption_ledger.md) — assumptions and failure conditions
- [`src/observer_math/`](src/observer_math/) — mathematical implementation
- [`tests/`](tests/) — claim-level tests
- [`examples/`](examples/) — reproducible studies

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). Current research-software release: **0.35.0**.

## License

MIT. See [`LICENSE`](LICENSE).
