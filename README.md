# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.37.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one question:

> **If the subsystem we care about is allowed to move, can its boundary be inferred from the dynamics rather than declared in advance?**

The repository develops that question through exact Gaussian identities, moving-boundary optimization, identifiability results, deterministic robustness certificates, finite-sample concentration, and reproducible numerical studies.

> **Interpretation boundary.** The word "observer" is used here as an operational mathematical name for a persistent moving subsystem boundary. The results do not prove consciousness, subjective experience, or a unique metaphysical observer.

## Verified research state

| Research record | Current state |
| --- | ---: |
| Proved statements | **49 propositions** |
| Reproducible studies | **35 experiments, A-Z and AA-AI** |
| Committed scientific figures | **22 figures** |
| Claim-level tests | **161 / 161 passing before release integration** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software release | **0.37.0** |

### Start here

**New reader:** [Research overview](docs/research_overview.md)  
**Complete theorem and experiment map:** [Research index](docs/research_index.md)  
**Detailed proofs 1-43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Latest proofs 44-49:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [P49](docs/proposition_49_compact_temporal_family.md)  
**Numerical record:** [Experiments A-AC](docs/reproducible_results.md) · [latest experiments](docs/research_index.md)  
**Assumptions and limits:** [Assumption ledger](docs/assumption_ledger.md)

---

# Latest result: direct matrix concentration beyond a one-parameter temporal model

## Proposition 49 and Experiment AI

[![Experiment AI: compact temporal family concentration](docs/compact_temporal_family.svg)](docs/proposition_49_compact_temporal_family.md)

Proposition 48 made the direct matrix concentration theorem uniform over an unknown AR(1) coefficient. Proposition 49 changes the architecture of that argument.

**The concentration theorem no longer assumes AR(1), or even a parameterization.** It starts from a deterministic finite cover of any declared compact temporal covariance family. If every admissible projected temporal covariance is close to some cover point in operator norm and projected normalization, Weyl's inequality controls every ordered temporal eigenvalue. The exact Gaussian matrix-mgf factors from Proposition 47 are monotone in those nonnegative eigenvalues, so the finite cover produces one valid family-wide matrix Chernoff envelope.

The important probability point is explicit:

> **There is no stochastic union bound over temporal cover points.** The cover is deterministic geometry used to construct one worst-case mgf before the probability inequality is applied.

Experiment AI uses the two-parameter temporal family

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I,
\]

with

\[
\phi\in[0.45,0.72],
\qquad
\eta\in[0,0.05].
\]

Here `eta` is a white-noise fraction. The target record length is `N=400`, the covariance block dimension is four, the nuisance design is affine, and the covariance confidence is 97.5%.

| Product cover | Cover points | Proposition 49 radius | Sphere-net family radius | Reduction |
| --- | ---: | ---: | ---: | ---: |
| `5 x 3` | 15 | `1.104` | `3.002` | 63.2% |
| `9 x 5` | 45 | **`0.957`** | `2.572` | 62.8% |
| `17 x 9` | 153 | **`0.891`** | `2.358` | 62.2% |

The transition is scientifically useful. The temporal family, sample count, confidence, nuisance design, and spatial dimension are held fixed. Only the deterministic family cover is refined. The certified radius moves from above one to below one, while the corresponding sphere-net family certificate remains above two.

Two seeded target-record checks with a large unknown affine mean also remained inside the final `0.891` radius:

| True temporal parameters | Trials covered | Median error | Maximum error |
| --- | ---: | ---: | ---: |
| `(phi, eta) = (0.60, 0.02)` | 96 / 96 | 0.250 | 0.403 |
| `(phi, eta) = (0.70, 0.04)` | 96 / 96 | 0.272 | 0.660 |

These simulations make the scale visible. They are not the proof.

[Read Proposition 49](docs/proposition_49_compact_temporal_family.md) · [JSON results](docs/compact_temporal_family.json) · [reproduce Experiment AI](examples/compact_temporal_family.py) · [claim-level tests](tests/test_compact_temporal_family.py)

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

The progression is:

```text
known temporal covariance
        -> Proposition 47
unknown AR(1) coefficient in a calibrated interval
        -> Proposition 48
arbitrary compact temporal family with a deterministic cover
        -> Proposition 49
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

---

# What is established, and what is not

Under its stated assumptions, the repository contains a conditional mathematical pipeline from time-varying Gaussian dynamics to moving-boundary optimization and finite-sample recovery certification. The most developed covariance layer now handles temporally dependent Gaussian sampling, fixed-subspace time-varying nuisance means, estimated AR(1) dependence, design-specific temporal geometry, direct matrix concentration, and compact multi-parameter temporal families supplied through deterministic covers.

Important restrictions remain:

- Gaussianity in the current sharp statistical concentration layer;
- temporal-spatial separability;
- nuisance designs fixed before inspecting the target record;
- deterministic temporal-family covers justified independently of the target record;
- no general theorem yet for a data-calibrated multi-parameter or nonparametric temporal confidence set;
- no claim that every real system has one intrinsic observer boundary.

The next major statistical frontier is to construct a **data-calibrated confidence set for a broader temporal covariance family** and compose that random family with Proposition 49 while keeping confidence accounting explicit.

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
- [`docs/assumption_ledger.md`](docs/assumption_ledger.md): assumptions and failure conditions
- [`src/observer_math/`](src/observer_math/): mathematical implementation
- [`tests/`](tests/): claim-level tests
- [`examples/`](examples/): reproducible studies

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). Current research-software release: **0.37.0**.

## License

MIT. See [`LICENSE`](LICENSE).
