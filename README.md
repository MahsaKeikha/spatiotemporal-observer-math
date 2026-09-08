# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.38.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one question:

> **If the subsystem we care about is allowed to move, can its boundary be inferred from the dynamics rather than declared in advance?**

The repository develops that question through exact Gaussian identities, moving-boundary optimization, identifiability results, deterministic robustness certificates, finite-sample concentration, and reproducible numerical studies.

> **Interpretation boundary.** The word "observer" is used here as an operational mathematical name for a persistent moving subsystem boundary. The results do not prove consciousness, subjective experience, or a unique metaphysical observer. Any future observer-to-consciousness bridge must be stated and tested separately; see the [interpretation protocol](docs/interpretation_protocol.md).

## Verified research state

| Research record | Current state |
| --- | ---: |
| Proved statements | **50 propositions** |
| Reproducible studies | **36 experiments, A-Z and AA-AJ** |
| Committed scientific figures | **23 figures** |
| Claim-level tests | **166 / 166 passing before final release integration** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software release | **0.38.0** |

### Start here

**New reader:** [Research overview](docs/research_overview.md)  
**Complete theorem and experiment map:** [Research index](docs/research_index.md)  
**Detailed proofs 1-43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Latest proofs 44-50:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [P49](docs/proposition_49_compact_temporal_family.md) · [P50](docs/proposition_50_calibrated_temporal_family.md)  
**Numerical record:** [Experiments A-AC](docs/reproducible_results.md) · [latest experiments](docs/research_index.md)  
**Assumptions and limits:** [Assumption ledger](docs/assumption_ledger.md)  
**Observer-to-consciousness bridge rules:** [Interpretation protocol](docs/interpretation_protocol.md)

---

# Latest result: learning a two-parameter temporal family from data

## Proposition 50 and Experiment AJ

[![Experiment AJ: observable temporal-family calibration](docs/calibrated_temporal_family.svg)](docs/proposition_50_calibrated_temporal_family.md)

Proposition 49 can certify covariance uniformly over a compact temporal covariance family once a deterministic cover of that family is supplied. Proposition 50 adds an observable statistical layer in front of it.

The calibration family is

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I,
\]

where \(R_\phi\) is stationary AR(1) covariance and \(\eta\) is a white-noise fraction. Independent standardized Gaussian calibration channels may each have an arbitrary constant mean.

The lag correlations satisfy

\[
r_1=(1-\eta)\phi,
\qquad
r_2=(1-\eta)\phi^2,
\]

so, when positive,

\[
\phi=\frac{r_2}{r_1},
\qquad
\eta=1-\frac{r_1^2}{r_2}.
\]

Proposition 50 estimates simultaneous finite-sample intervals for \(r_1\) and \(r_2\) from lagged increment energies, maps them into a conservative confidence rectangle for \((\phi,\eta)\), then conditions on the independent calibration record and applies Proposition 49 to a separate target record.

The main sharpening is structural: the theorem analyzes the **increment covariance spectrum itself** rather than multiplying the raw temporal spectral norm by a generic difference-operator bound. For lag 1, the AR(1) increment spectral peak is

\[
4\frac{1-\phi}{1+\phi},
\]

and for lag 2 it is

\[
4(1-\phi^2).
\]

Thus the low-frequency persistence that makes the raw AR(1) level spectrum large is strongly suppressed by the statistic used to estimate it.

Experiment AJ fixes the target problem and changes only the number of independent calibration channels:

| Calibration channels | Calibrated `phi` interval | Proposition 50 radius | Full-family Proposition 49 radius |
| ---: | --- | ---: | ---: |
| 16 | `[0.487, 0.750]` | `1.117` | `1.142` |
| 32 | `[0.504, 0.737]` | `1.054` | `1.142` |
| 64 | `[0.517, 0.679]` | **`0.871`** | `1.142` |
| 128 | `[0.545, 0.659]` | **`0.814`** | `1.142` |
| 256 | `[0.559, 0.640]` | **`0.772`** | `1.142` |

The target sample count, spatial dimension, nuisance design, confidence split, cover resolution, and controlled temporal parameters remain fixed. Learning the temporal uncertainty alone moves the rigorous covariance radius from above one to below one at 64 calibration channels.

At 64 channels, the lag-1 increment-specific correlation radius is about `0.021`, compared with about `0.091` from a generic raw-spectrum product bound. For lag 2, the corresponding comparison is about `0.035` versus `0.108`.

Two independent 96-trial target-record visibility checks recorded maximum relative covariance errors `0.438` and `0.409`, below theorem radii `0.871` and `0.772`. These simulations make scale visible. They are not the proof.

[Read Proposition 50](docs/proposition_50_calibrated_temporal_family.md) · [JSON results](docs/calibrated_temporal_family.json) · [reproduce Experiment AJ](examples/calibrated_temporal_family.py) · [render figure](examples/render_calibrated_temporal_family.py) · [claim-level tests](tests/test_calibrated_temporal_family.py) · [release record](docs/release_0_38.md)

---

# The current dependent-Gaussian theorem ladder

The newest statistical sequence removes one restriction at a time.

| Proposition | Restriction addressed | Result |
| ---: | --- | --- |
| 41 | i.i.d. temporal sampling | separably dependent Gaussian covariance screening |
| 42 | known constant mean | exact normalization after same-record mean removal |
| 43 | known AR(1) coefficient | observable same-record AR(1) calibration |
| 44 | constant target mean | projection away from any fixed declared nuisance subspace |
| 45 | known temporal dependence in P44 | estimated AR(1), nuisance projection, and normalization uncertainty |
| 46 | rank-only nuisance pessimism | design-specific continuum geometry over the calibrated interval |
| 47 | sphere-net operator-norm reduction | direct weighted-Wishart matrix concentration using the full temporal spectrum |
| 48 | known projected spectrum in P47 | interval-uniform direct matrix concentration with observable AR(1) calibration |
| 49 | one-dimensional AR(1) family | direct matrix concentration over any compact temporal family with a certified finite cover |
| 50 | deterministic multi-parameter family in P49 | observable two-parameter confidence family learned from independent calibration data |

The progression is:

```text
known temporal covariance
        -> Proposition 47
unknown AR(1) coefficient in a calibrated interval
        -> Proposition 48
arbitrary compact temporal family with a deterministic cover
        -> Proposition 49
random two-parameter confidence family learned from independent data
        -> Proposition 50
```

---

# Recent visual proof frontier

## Proposition 44: unknown time-varying nuisance mean

[![Experiment AD](docs/nuisance_projection_calibration.svg)](docs/proposition_44_nuisance_projection.md)

A fixed temporal nuisance design is projected away exactly. Experiment AD shows ordinary mean-centering failing under large affine drift while the declared nuisance projection remains stable.

## Proposition 45: estimated temporal dependence

[![Experiment AE](docs/estimated_ar1_nuisance_projection.svg)](docs/proposition_45_estimated_ar1_nuisance_projection.md)

Observable increment-energy calibration supplies an AR(1) interval and propagates its uncertainty through nuisance-projected covariance estimation.

## Proposition 46: actual nuisance geometry

[![Experiment AF](docs/design_specific_ar1_envelope.svg)](docs/proposition_46_design_specific_ar1_envelope.md)

The actual declared nuisance design replaces a rank-only worst case. A regime that is vacuous under rank-only control remains certifiable with design-specific geometry.

## Proposition 47: direct matrix concentration

[![Experiment AG](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md)

The operator-norm sphere net is removed. Direct matrix concentration cuts the displayed covariance radii by roughly 52% to 60%.

## Proposition 48: unknown AR(1) coefficient without losing the matrix bound

[![Experiment AH](docs/uniform_matrix_chernoff_ar1.svg)](docs/proposition_48_uniform_matrix_chernoff_ar1.md)

The full projected eigenvalue profile is controlled between AR(1) grid points. In the strongest displayed interval, the previous interval certificate is `2.409` while Proposition 48 is `0.931`.

## Proposition 49: compact temporal families

[![Experiment AI](docs/compact_temporal_family.svg)](docs/proposition_49_compact_temporal_family.md)

The temporal geometry layer is modularized. Any family with a valid deterministic spectral and normalization cover can reuse the direct Gaussian matrix-concentration layer.

## Proposition 50: data-calibrated compact family

[![Experiment AJ](docs/calibrated_temporal_family.svg)](docs/proposition_50_calibrated_temporal_family.md)

Independent calibration data now learns a finite-sample two-parameter temporal confidence rectangle before the compact-family covariance theorem is applied to an independent target record.

---

# What is being optimized?

At each time `t`, a candidate subsystem is a coordinate set `S_t`. A changing candidate history

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1})
\]

is called an **observer world-tube**.

For the implemented nonstationary linear Gaussian dynamics

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\]

each candidate receives evidence from four ingredients:

1. **integration:** predictive interaction across the weakest internal cut;
2. **insulation:** how little predictive information must be imported from outside;
3. **persistence:** survival of predictive structure into the next state;
4. **transport:** continuity of organization when physical membership changes.

A dynamic program returns the exact maximizing path in the declared candidate family and the exact runner-up. Their action difference is the margin used by the robustness theorems.

A controlled moving-boundary example recovers

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

at all five times, with winning action `1.254324`, runner-up `1.127903`, and exact action margin `0.126421`.

| Selected moving path | Regularization and failure region |
| --- | --- |
| [![Candidate scores over time](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#regularization-result) |

The failure region is intentionally part of the record.

---

# Identifiability comes before optimization

A high objective value is not automatically evidence of an identifiable physical boundary. Proposition 14 constructs observationally identical models that assign incompatible boundary labels, producing a one-half maximin ceiling for any observational estimator in that setting.

> **Recovery is always relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

None of the implemented scores is a measurement or proof of phenomenal consciousness.

The project now maintains a separate [interpretation protocol](docs/interpretation_protocol.md) for any future attempt to connect observer structure to consciousness hypotheses. Such a bridge would require additional assumptions and tests, including representation invariance, causal discriminability, temporal identity, counterfactual robustness, empirical anchoring, and falsifiability.

---

# What is established, and what is not

Under its stated assumptions, the repository contains a conditional mathematical pipeline from time-varying Gaussian dynamics to moving-boundary optimization and finite-sample recovery certification. The most developed covariance layer now handles temporally dependent Gaussian sampling, fixed-subspace time-varying nuisance means, estimated AR(1) dependence, design-specific temporal geometry, direct matrix concentration, compact multi-parameter temporal families, and an independently data-calibrated two-parameter temporal confidence family.

Important restrictions remain:

- Gaussianity in the current sharp statistical concentration layer;
- temporal-spatial separability;
- nuisance designs fixed before inspecting the target record;
- exact standardized independent calibration channels in Proposition 50;
- independence between Proposition 50 calibration data and the target covariance record;
- a stationary AR(1) plus white-noise family for the current two-parameter calibration theorem;
- the conservative rectangular propagation from lag correlations to parameter space;
- no general finite-sample theorem yet for nonparametric temporal spectral uncertainty;
- no claim that every real system has one intrinsic observer boundary;
- no theorem connecting the observer objective by itself to phenomenal consciousness.

The next statistical frontier is a **sharper joint confidence region for the temporal parameters**, followed by finite-sample spectral-density confidence sets that can reuse Proposition 49.

In parallel, the structural frontier is to develop **intervention-sensitive and representation-invariant observer quantities** before treating any consciousness bridge as a formal hypothesis.

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
python examples/compact_temporal_family.py
python examples/calibrated_temporal_family.py
python examples/render_calibrated_temporal_family.py
```

Every numerical claim is expected to have a committed script, a machine-readable result file, a visible figure when useful, and claim-level test coverage.

## Repository map

- [`docs/research_overview.md`](docs/research_overview.md): research narrative
- [`docs/research_index.md`](docs/research_index.md): theorem and experiment navigation
- [`docs/proofs_and_conjectures.md`](docs/proofs_and_conjectures.md): detailed Propositions 1-43
- [`docs/proposition_44_nuisance_projection.md`](docs/proposition_44_nuisance_projection.md): Proposition 44
- [`docs/proposition_45_estimated_ar1_nuisance_projection.md`](docs/proposition_45_estimated_ar1_nuisance_projection.md): Proposition 45
- [`docs/proposition_46_design_specific_ar1_envelope.md`](docs/proposition_46_design_specific_ar1_envelope.md): Proposition 46
- [`docs/proposition_47_weighted_wishart_matrix_chernoff.md`](docs/proposition_47_weighted_wishart_matrix_chernoff.md): Proposition 47
- [`docs/proposition_48_uniform_matrix_chernoff_ar1.md`](docs/proposition_48_uniform_matrix_chernoff_ar1.md): Proposition 48
- [`docs/proposition_49_compact_temporal_family.md`](docs/proposition_49_compact_temporal_family.md): Proposition 49
- [`docs/proposition_50_calibrated_temporal_family.md`](docs/proposition_50_calibrated_temporal_family.md): Proposition 50
- [`docs/interpretation_protocol.md`](docs/interpretation_protocol.md): rules for any future observer-to-consciousness bridge hypothesis
- [`docs/assumption_ledger.md`](docs/assumption_ledger.md): assumptions and failure conditions
- [`docs/release_0_38.md`](docs/release_0_38.md): release 0.38.0 record
- [`src/observer_math/`](src/observer_math/): mathematical implementation
- [`tests/`](tests/): claim-level tests
- [`examples/`](examples/): reproducible studies

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). Current research-software release: **0.38.0**.

## License

MIT. See [`LICENSE`](LICENSE).
