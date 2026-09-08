# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.39.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around a precise question:

> **If a subsystem is allowed to move through a larger dynamical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The repository develops that question through exact Gaussian identities, information-theoretic scores, moving-boundary optimization, identifiability limits, deterministic robustness, finite-sample statistics, temporal-dependence calibration, and reproducible experiments.

> **Interpretation boundary.** The word "observer" is operational. It refers to a mathematically defined persistent moving subsystem structure. The results do not prove consciousness, subjective experience, or a unique metaphysical observer. Any future observer-to-consciousness bridge must be introduced as an additional hypothesis and evaluated under the [interpretation protocol](docs/interpretation_protocol.md).

## Current research record

| Research record | Current state |
| --- | ---: |
| Proved statements | **51 propositions** |
| Reproducible studies | **37 experiments, A-Z and AA-AK** |
| Committed scientific figures | **24 figures** |
| Claim-level tests | **171 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.39.0** |

### Start here

**Research story:** [Research overview](docs/research_overview.md)  
**Theorem and experiment map:** [Research index](docs/research_index.md)  
**Propositions 1-43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Propositions 44-51:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [P49](docs/proposition_49_compact_temporal_family.md) · [P50](docs/proposition_50_calibrated_temporal_family.md) · [P51](docs/proposition_51_evalue_temporal_confidence_set.md)  
**Assumptions and failure conditions:** [Assumption ledger](docs/assumption_ledger.md)  
**Consciousness interpretation rules:** [Interpretation protocol](docs/interpretation_protocol.md)

---

# Latest result: a continuum confidence set from the full residual likelihood

## Proposition 51 and Experiment AK

[![Experiment AK: full-likelihood e-value geometry](docs/evalue_temporal_confidence_set.svg)](docs/proposition_51_evalue_temporal_confidence_set.md)

Proposition 50 learns a two-parameter temporal covariance family from lag-1 and lag-2 increment statistics. That construction is finite sample and rigorous, but it treats the two lag summaries through rectangular interval arithmetic.

Proposition 51 uses the complete Gaussian residual likelihood instead.

The calibration family is

\[
R_{\phi,\eta}
=
(1-\eta)R_\phi+\eta I,
\]

where \(R_\phi\) is stationary AR(1) covariance and \(\eta\) is a white-noise fraction.

Each calibration channel may have its own unknown constant mean. A fixed orthonormal Helmert contrast removes that mean exactly. If \(p_\theta\) denotes the resulting residual Gaussian density under parameter \(\theta=(\phi,\eta)\), choose a proper mixture density \(q\) before seeing the calibration data and define

\[
e_\theta(Z)
=
\frac{q(Z)}{p_\theta(Z)}.
\]

When \(\theta\) is the true temporal parameter,

\[
\mathbb E_\theta e_\theta(Z)=1.
\]

Therefore, by Markov's inequality,

\[
\mathcal C_\alpha(Z)
=
\left\{
\theta:
 e_\theta(Z)<1/\alpha
\right\}
\]

contains the true parameter with probability at least \(1-\alpha\).

This probability statement is **continuum valued**. It does not require a union bound over a parameter grid, and the true parameter does not need to be one of the mixture support points.

### What Experiment AK shows

Experiment AK evaluates the exact pointwise e-value function on a fixed visualization grid so its geometry can be inspected. At 256 independent calibration channels:

- Proposition 50's rectangular propagation spans approximately `phi = 0.510 to 0.701` and `eta = 0 to 0.216`;
- the Proposition 51 visualization accepts grid points spanning approximately `phi = 0.55 to 0.65` and `eta = 0 to 0.12`;
- only about **6.76 percent** of the displayed parameter grid is accepted;
- a separate 256-trial visibility study accepted the controlled true parameter in **256 / 256** trials.

The simulation is not the coverage proof. The theorem is the density-ratio identity plus Markov's inequality.

The displayed grid is also **not** a certified outer cover of the full continuum confidence set. Points between displayed grid locations remain governed by the continuum theorem. Constructing a certified outer cover, and then composing it with Proposition 49 for an independent target covariance record, is the next theorem rather than an assumption hidden inside this result.

[Full proof](docs/proposition_51_evalue_temporal_confidence_set.md) · [machine-readable Experiment AK](docs/evalue_temporal_confidence_set.json) · [experiment script](examples/evalue_temporal_confidence_set.py) · [SVG renderer](examples/render_evalue_temporal_confidence_set.py) · [claim-level tests](tests/test_evalue_temporal_family.py)

---

# The recent theorem ladder

The newest results form one continuous proof program.

| Proposition | Question answered |
| ---: | --- |
| **41** | How does temporal dependence alter Gaussian covariance concentration? |
| **42** | What changes when an unknown constant mean must be removed? |
| **43** | Can a shared nonnegative AR(1) coefficient be estimated from the record? |
| **44** | Can the target mean vary inside a fixed declared temporal subspace? |
| **45** | Can temporal calibration and nuisance projection be combined? |
| **46** | Can the actual nuisance geometry replace a rank-only worst case? |
| **47** | Can direct matrix concentration replace the sphere-net operator bound? |
| **48** | Can the direct matrix bound remain valid for an unknown AR(1) coefficient? |
| **49** | Can the concentration theorem cover an arbitrary compact temporal family? |
| **50** | Can a two-parameter temporal family be learned from independent data? |
| **51** | Can the complete residual likelihood produce a joint continuum confidence set without parameterwise multiple-testing inflation? |

The statistical direction now points naturally toward a certified adaptive outer cover of the Proposition 51 confidence set. The structural direction runs in parallel toward intervention-sensitive and representation-invariant observer quantities.

---

# Earlier visual results

## Proposition 50: data-calibrated two-parameter temporal family

[![Experiment AJ: observable temporal-family calibration](docs/calibrated_temporal_family.svg)](docs/proposition_50_calibrated_temporal_family.md)

Experiment AJ keeps the target covariance problem fixed while increasing only the amount of independent temporal calibration information. The full declared-family radius is about `1.142`. The calibrated radius falls to about `0.871` at 64 calibration channels and continues to about `0.772` at 256 channels.

[Proof](docs/proposition_50_calibrated_temporal_family.md) · [data](docs/calibrated_temporal_family.json)

## Proposition 49: compact temporal-family concentration

[![Experiment AI: compact temporal covariance family](docs/compact_temporal_family.svg)](docs/proposition_49_compact_temporal_family.md)

Proposition 49 separates temporal-family geometry from matrix probability. A finite deterministic cover controls a complete compact family without paying a stochastic union penalty for the cover points.

[Proof](docs/proposition_49_compact_temporal_family.md) · [data](docs/compact_temporal_family.json)

## Proposition 47: weighted Gaussian matrix concentration

[![Experiment AG: weighted-Wishart matrix concentration](docs/weighted_wishart_matrix_chernoff.svg)](docs/proposition_47_weighted_wishart_matrix_chernoff.md)

Proposition 47 replaces the earlier sphere-net reduction with direct matrix concentration using the full temporal eigenvalue profile. In the displayed high-correlation regimes, this changes a previously unusable radius above one into a rigorous radius below one.

[Proof](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [data](docs/weighted_wishart_matrix_chernoff.json)

## Moving-boundary recovery

| Candidate scores | Recovery landscape |
| --- | --- |
| [![Candidate scores over time](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) |

A controlled planted module moves through the coordinates as

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

The optimizer recovers the planted path in the stated construction. The phase diagram also retains the failure region where continuity regularization is made too strong.

---

# Central mathematical object

At time \(t\), let a candidate subsystem be a coordinate set \(S_t\). A changing candidate history is

\[
\mathcal W
=
(S_0,S_1,\ldots,S_{T-1}),
\]

called an **observer world-tube**.

For a nonstationary linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\]

the repository constructs candidate scores from four ingredients:

1. **internal integration**, evaluated across the weakest internal bipartition;
2. **environmental insulation**, penalizing predictive information imported from outside the candidate;
3. **persistence**, measured through canonical predictive structure into the next state;
4. **transport**, rewarding predictive continuity when physical membership changes.

A dynamic program computes the globally maximizing path in the declared candidate family. A second exact calculation identifies the best competing path. Their difference gives an action margin that can be propagated through deterministic and finite-sample perturbation bounds.

---

# Identifiability before interpretation

Optimization is not the same as identifiability.

The repository contains explicit symmetry and two-model impossibility results. If two admissible models produce the same declared observational law while assigning incompatible labels outside the allowed symmetry class, no estimator based only on those observations can uniformly identify both labels.

This leads to a standing rule for the project:

> **Every recovery statement is relative to declared observables, model assumptions, candidate families, and admissible symmetries.**

That rule is especially important for any future consciousness interpretation. The current observer mathematics is a structural inference framework. A consciousness hypothesis would require additional bridge assumptions, causal or interventional content, independent empirical anchors, and falsifiable predictions. Those requirements are documented separately in the [interpretation protocol](docs/interpretation_protocol.md).

---

# What the repository currently establishes

Under its stated model assumptions, the repository now contains a conditional mathematical pipeline for:

- defining observer-like subsystem scores;
- optimizing moving subsystem paths;
- quantifying exact action margins;
- proving recovery stability under deterministic perturbations;
- deriving finite-sample Gaussian covariance guarantees;
- screening competitor paths safely under declared conditions;
- handling temporally dependent Gaussian observations;
- removing unknown constant and fixed-subspace nuisance means;
- estimating temporal dependence;
- exploiting actual nuisance geometry;
- using direct matrix concentration with the full temporal spectrum;
- certifying compact temporal covariance families;
- learning a two-parameter temporal family from independent calibration data;
- constructing a finite-sample joint continuum confidence set from the full residual likelihood.

## What is not established

The repository does not establish that every physical system has a unique observer boundary. It does not establish consciousness. It does not remove the need to justify Gaussianity, separability, nuisance structure, temporal-family assumptions, candidate construction, or any empirical bridge to phenomenal experience.

Proposition 51 does not yet turn its irregular continuum confidence set into a certified finite cover for Proposition 49. That missing step is explicit and is the immediate statistical frontier.

---

# Reproduce

```bash
git clone https://github.com/MahsaKeikha/spatiotemporal-observer-math.git
cd spatiotemporal-observer-math
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Run the newest experiments:

```bash
python examples/evalue_temporal_confidence_set.py
python examples/render_evalue_temporal_confidence_set.py
python examples/calibrated_temporal_family.py
python examples/compact_temporal_family.py
```

Each recent numerical claim is paired with machine-readable JSON, a reproducible script, a visible figure when useful, and claim-level tests.

## Repository map

- [`src/observer_math/`](src/observer_math/) contains the mathematical implementation.
- [`tests/`](tests/) contains tests tied to scientific claims.
- [`examples/`](examples/) contains reproducible numerical studies and figure renderers.
- [`docs/research_overview.md`](docs/research_overview.md) explains the research as a narrative.
- [`docs/research_index.md`](docs/research_index.md) maps propositions, experiments, figures, data, and code.
- [`docs/assumption_ledger.md`](docs/assumption_ledger.md) records assumptions and failure conditions.
- [`docs/interpretation_protocol.md`](docs/interpretation_protocol.md) states the requirements for any future consciousness interpretation.
- [`CITATION.cff`](CITATION.cff) contains citation metadata.

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). The current research-software version is **0.39.0**.

## License

MIT. See [`LICENSE`](LICENSE).
