# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.39.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around a precise dynamical question:

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The repository develops that question through moving-boundary optimization, Gaussian information geometry, identifiability limits, deterministic robustness, finite-sample statistics, temporal-dependence calibration, and reproducible experiments.

> **Interpretation boundary.** The word "observer" is operational. It refers to a mathematically defined persistent moving subsystem structure. The results do not prove consciousness, subjective experience, or a unique metaphysical observer. Any future observer-to-consciousness bridge must be introduced as an additional hypothesis and evaluated under the [interpretation protocol](docs/interpretation_protocol.md).

---

# Physics first: what problem are we actually solving?

Before reading the newest probability bounds, it helps to see the physical inference problem they support.

![Physics to inference pipeline](docs/physics_pipeline.svg)

Imagine a large dynamical system measured through many coordinates. Depending on the application, a coordinate might be a voltage, displacement, pressure sensor, neural signal, concentration, position, or another physical observable.

At time \(t\), the full measured state is

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

A candidate subsystem is a subset of those measured degrees of freedom,

\[
S_t\subseteq\{1,\ldots,n\}.
\]

The key point is that the same physical organization may move. A coherent structure crossing a sensor field, for example, may be represented by one set of channels now and a neighboring set later. The repository therefore follows a changing path

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}),
\]

called an **observer world-tube**.

The phrase `world-tube` is an analogy for the history of an extended structure through time. It is not a claim that this is a relativistic spacetime construction.

The population dynamics are modeled locally as

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

Physically:

- \(X_t\) is what was measured;
- \(A_t\) is an effective coupling or propagation operator over one sampling interval;
- \(Q_t\) describes unresolved stochastic forcing inside the model;
- \(S_t\) is a proposed boundary in the measured coordinate system.

The candidate boundary is evaluated using four operational properties:

1. **Integration:** internal parts predict one another.
2. **Insulation:** outside variables add comparatively limited predictive information once the candidate state is known.
3. **Persistence:** the organization carries predictive structure into its future.
4. **Transport:** the organization can move into new coordinates without losing dynamical continuity.

These are structural properties of a stochastic dynamical system. They are not definitions of consciousness.

The recent Propositions 41 through 52 mainly solve a different but necessary problem: **can we trust the covariance and information quantities used to score a boundary when the record has temporal memory, drift, nuisance trends, and finite length?**

That is why so much of the recent mathematics concerns temporal covariance, matrix concentration, calibration, and confidence sets. Those results are measurement-certification machinery underneath the moving-boundary problem.

For the full physical interpretation of every major equation, including units, relaxation time, covariance modes, nuisance projection, the meaning of \(\epsilon<1\), and a proposition-by-proposition physics translation, read the **[Physics Guide](docs/physics_guide.md)** before the detailed proofs.

---

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

**Physics story and equation dictionary:** [Physics Guide](docs/physics_guide.md)  
**Research story:** [Research overview](docs/research_overview.md)  
**Theorem and experiment map:** [Research index](docs/research_index.md)  
**Propositions 1-43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Propositions 44-51:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [P49](docs/proposition_49_compact_temporal_family.md) · [P50](docs/proposition_50_calibrated_temporal_family.md) · [P51](docs/proposition_51_evalue_temporal_confidence_set.md)  
**Assumptions and failure conditions:** [Assumption ledger](docs/assumption_ledger.md)  
**Consciousness interpretation rules:** [Interpretation protocol](docs/interpretation_protocol.md)

---

# What covariance means physically

For a fluctuating multivariate system,

\[
\Sigma=\mathbb E[(X-\mu)(X-\mu)^\top]
\]

records the geometry of fluctuations.

The diagonal entries are coordinate variances. The off-diagonal entries record co-fluctuation. The eigenvectors describe collective fluctuation directions and the eigenvalues describe variance along those directions.

These covariance eigenvalues are **not automatically physical energies**. An energy interpretation requires an additional physical model connecting the measured coordinates to a Hamiltonian, temperature, power spectrum, or another energetic quantity.

Covariance is central here because Gaussian conditional mutual information and canonical predictive quantities can be computed from covariance blocks. If covariance is badly estimated, the candidate-boundary scores can also be wrong.

That is why the repository spends effort proving bounds such as

\[
\left\|
\Sigma^{-1/2}(\widehat\Sigma-\Sigma)\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

When \(\epsilon<1\), the empirical fluctuation geometry remains in a perturbative regime where positive variance directions, inverse covariance quantities, and downstream Gaussian information calculations can be controlled.

The number `1` is not a physical phase transition. It is a mathematical threshold that makes several perturbation arguments available.

---

# Why temporal physics matters

A physical system has memory, so repeated time samples are usually correlated. Treating them as independent would overstate the amount of information in a finite record.

The simplest recent temporal model is

\[
R_\phi(i,j)=\phi^{|i-j|}.
\]

Here \(\phi\) controls persistence. If samples are separated by \(\Delta t\), an AR(1) relaxation-time interpretation is

\[
\tau=-\frac{\Delta t}{\log\phi},
\]

when the AR(1) approximation is physically suitable.

The newer two-parameter family is

\[
R_{\phi,\eta}
=(1-\eta)R_\phi+\eta I.
\]

In this effective model, \(\phi\) controls the persistence timescale of the correlated part and \(\eta\) controls a temporally uncorrelated variance fraction.

Real physical systems may require multiple timescales, oscillatory kernels, colored noise, nonstationarity, or continuous spectral densities. The current family is a controlled mathematical starting point, not a universal physical law.

---

# Latest completed result: a continuum confidence set from the full residual likelihood

## Proposition 51 and Experiment AK

[![Experiment AK: full-likelihood e-value geometry](docs/evalue_temporal_confidence_set.svg)](docs/proposition_51_evalue_temporal_confidence_set.md)

Proposition 50 learns a two-parameter temporal covariance family from lag-1 and lag-2 increment statistics. Proposition 51 uses the complete Gaussian residual likelihood instead.

Each calibration channel may have its own unknown constant mean. A fixed orthonormal Helmert contrast removes that mean exactly. If \(p_\theta\) denotes the residual Gaussian density under \(\theta=(\phi,\eta)\), choose a proper mixture density \(q\) before observing the calibration record and define

\[
e_\theta(Z)=\frac{q(Z)}{p_\theta(Z)}.
\]

At the true temporal parameter,

\[
\mathbb E_\theta e_\theta(Z)=1.
\]

Therefore

\[
\mathcal C_\alpha(Z)
=
\left\{\theta:e_\theta(Z)<1/\alpha\right\}
\]

contains the true parameter with probability at least \(1-\alpha\).

Physical reading: the calibration record defines a finite-sample set of temporal-memory models that remain compatible with the observed residual dynamics under the declared model family.

The e-value is not a posterior probability that a parameter is true. It is a finite-sample testing construction.

### What Experiment AK shows

At 256 independent calibration channels:

- Proposition 50's rectangular propagation spans approximately `phi = 0.510 to 0.701` and `eta = 0 to 0.216`;
- the Proposition 51 visualization accepts grid points spanning approximately `phi = 0.55 to 0.65` and `eta = 0 to 0.12`;
- about **6.76 percent** of the displayed parameter grid is accepted;
- a separate 256-trial visibility study accepted the controlled true parameter in **256 / 256** trials.

The simulation is not the coverage proof. The theorem is the density-ratio identity plus Markov's inequality.

The displayed grid is not a certified outer cover of the continuum confidence set. Proposition 52, currently under development, addresses that missing step before the set is propagated to an independent target covariance problem.

[Full proof](docs/proposition_51_evalue_temporal_confidence_set.md) · [machine-readable Experiment AK](docs/evalue_temporal_confidence_set.json) · [experiment script](examples/evalue_temporal_confidence_set.py) · [SVG renderer](examples/render_evalue_temporal_confidence_set.py) · [claim-level tests](tests/test_evalue_temporal_family.py)

---

# The recent theorem ladder, with physical meaning

| Proposition | Mathematical question | Physical question |
| ---: | --- | --- |
| **41** | How does temporal dependence alter covariance concentration? | How much independent information is really in a record with memory? |
| **42** | What changes when an unknown constant mean is removed? | How does subtracting an unknown baseline change usable fluctuation information? |
| **43** | Can a shared nonnegative AR(1) coefficient be estimated? | Can the persistence timescale be learned instead of assumed? |
| **44** | Can the target mean vary inside a declared temporal subspace? | Can drift and known acquisition trends be removed without corrupting fluctuation covariance? |
| **45** | Can temporal calibration and nuisance projection be combined? | Can memory uncertainty and deterministic drift be handled at once? |
| **46** | Can actual nuisance geometry replace a rank-only worst case? | Can the real shape of removed drift modes improve the physical information budget? |
| **47** | Can direct matrix concentration replace a sphere-net bound? | Can complete fluctuation modes be certified without a loose directional approximation? |
| **48** | Can the matrix bound survive unknown AR(1)? | Does the covariance guarantee survive uncertainty in relaxation time? |
| **49** | Can a compact temporal family be covered? | Can a physically admissible family of memory kernels be propagated safely? |
| **50** | Can a two-parameter family be learned from calibration data? | Can persistence and fast uncorrelated variance be estimated from an independent experiment? |
| **51** | Can full likelihood produce a continuum confidence set? | Which temporal models remain compatible with the entire calibration record? |
| **52, in progress** | Can the continuum set be safely outer-covered and composed with Proposition 49? | Can calibrated temporal uncertainty be carried all the way into a target covariance certificate without pretending a plotting grid is exact? |

---

# Moving-boundary recovery: the physical target of the statistical machinery

| Candidate scores | Recovery landscape |
| --- | --- |
| [![Candidate scores over time](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) |

A controlled planted module moves through the coordinates as

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

A useful physical analogy is a coherent structure moving across a sensor array. The same organization persists, but the sensors representing it change as the structure moves.

The optimizer recovers the planted path in the stated construction. The phase diagram also retains the failure region where continuity regularization is too strong.

That failure region matters physically. If the model rewards continuity too strongly, it can prefer a smooth path even when the measured dynamics support a different boundary.

---

# The central mathematical object

At each time, the repository scores a candidate subsystem using:

1. **internal integration**, evaluated across the weakest internal bipartition;
2. **environmental insulation**, penalizing predictive information imported from outside the candidate;
3. **persistence**, measured through canonical predictive structure into the next state;
4. **transport**, rewarding predictive continuity when physical membership changes.

A dynamic program computes the globally maximizing path in the declared candidate family. A second exact calculation identifies the best competing path. Their difference gives an optimization margin that can be propagated through deterministic and finite-sample perturbation bounds.

The repository sometimes calls this an `action margin`. It is an objective difference, **not physical action in joule-seconds** unless a future derivation explicitly connects the objective to a physical action functional.

---

# Identifiability before interpretation

Optimization is not the same as identifiability.

The repository contains symmetry and two-model impossibility results. If two admissible models produce the same declared observational law while assigning incompatible labels outside the allowed symmetry class, no estimator based only on those observations can uniformly identify both labels.

This gives a standing rule:

> **Every recovery statement is relative to declared observables, physical modeling assumptions, candidate families, and admissible symmetries.**

A physically serious application must therefore document the observables, units, sampling interval, sensor processing, coupling model, nuisance modes, temporal assumptions, candidate geometry, and model-failure tests.

See the [Physics Guide](docs/physics_guide.md) for the complete accountability checklist.

---

# What the repository currently establishes

Under its stated assumptions, the repository contains a conditional mathematical pipeline for:

- defining observer-like subsystem scores;
- optimizing moving subsystem paths;
- quantifying exact optimization margins;
- proving path stability under deterministic perturbations;
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

The repository does not establish that every physical system has a unique observer boundary. It does not establish that the current Gaussian or AR(1) models hold in any particular experiment without validation. It does not establish consciousness.

A physical application must still justify:

- what each coordinate measures and in what units;
- why the sampling interval resolves the relevant dynamics;
- why the chosen effective dynamics are adequate;
- why the nuisance projection does not remove genuine physics;
- why the temporal family is adequate;
- how candidate boundaries map to physical geometry;
- what interventions or held-out tests could falsify the interpretation.

Any consciousness hypothesis requires a further bridge with independent empirical content. Those obligations are documented in the [interpretation protocol](docs/interpretation_protocol.md).

---

# Reproduce

```bash
git clone https://github.com/MahsaKeikha/spatiotemporal-observer-math.git
cd spatiotemporal-observer-math
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Run the newest completed experiments:

```bash
python examples/evalue_temporal_confidence_set.py
python examples/render_evalue_temporal_confidence_set.py
python examples/calibrated_temporal_family.py
python examples/compact_temporal_family.py
```

Each recent numerical claim is paired with machine-readable JSON, a reproducible script, a visible figure when useful, and claim-level tests.

## Repository map

- [`docs/physics_guide.md`](docs/physics_guide.md) explains what the mathematical objects mean physically and how to validate them.
- [`docs/physics_pipeline.svg`](docs/physics_pipeline.svg) shows the physical inference pipeline visually.
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
