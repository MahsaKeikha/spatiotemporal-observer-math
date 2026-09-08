# Spatiotemporal Observer Mathematics

[![tests](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml/badge.svg)](https://github.com/MahsaKeikha/spatiotemporal-observer-math/actions/workflows/test.yml)
[![version](https://img.shields.io/badge/version-0.40.0-2563eb)](CITATION.cff)
[![license](https://img.shields.io/badge/license-MIT-059669)](LICENSE)

An open mathematical research program by **Mahsa Keikha, PhD** built around one dynamical question:

> **If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?**

The repository studies that question through moving-boundary optimization, Gaussian information geometry, identifiability, finite-sample statistics, temporal-memory calibration, and reproducible experiments.

> **Interpretation boundary.** The word "observer" is operational. It refers to a mathematically defined persistent moving subsystem structure. The results do not prove consciousness, subjective experience, or a unique metaphysical observer. Any future observer-to-consciousness bridge must be introduced as an additional hypothesis and evaluated under the [interpretation protocol](docs/interpretation_protocol.md).

---

# Physics first: what problem are we solving?

![Physics to inference pipeline](docs/physics_pipeline.svg)

Imagine a physical process measured through many coordinates. Depending on the application, a coordinate might be a voltage, displacement, pressure, neural signal, concentration, position, or another measured degree of freedom.

At time \(t\), write the full measured state as

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

A candidate subsystem is a subset

\[
S_t\subseteq\{1,\ldots,n\}.
\]

The same physical organization may move through the measured coordinates. A coherent structure crossing a sensor field, for example, can be represented by one set of sensors now and a neighboring set later. The changing history

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1})
\]

is called an **observer world-tube**.

The term `world-tube` is an analogy for the history of an extended structure through time. It is not a claim that the construction is a relativistic spacetime world tube.

The main population model is

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

A physical reading is:

- \(X_t\): measured observables;
- \(A_t\): an effective coupling or propagation operator over one sampling interval;
- \(Q_t\): covariance of unresolved stochastic forcing inside the model;
- \(S_t\): a proposed subsystem boundary in the measured coordinate system.

Candidate boundaries are evaluated using four operational properties:

1. **Integration:** internal parts predict one another.
2. **Insulation:** outside variables add comparatively limited predictive information once the candidate state is known.
3. **Persistence:** the organization carries predictive structure into its future.
4. **Transport:** the organization can move into new coordinates without losing dynamical continuity.

These are structural properties of a stochastic dynamical system. They are not definitions of consciousness.

The recent Propositions 41 through 52 form a measurement-certification layer underneath this boundary problem. Their job is to answer a necessary question:

> **Can the covariance and information quantities used to score a boundary be trusted when the measured record has temporal memory, drift, nuisance structure, and finite length?**

For a complete physical dictionary, units guidance, relaxation-time interpretation, covariance meaning, failure diagnostics, and proposition-by-proposition translation, start with the **[Physics Guide](docs/physics_guide.md)** and the **[Figure Reading Guide](docs/figure_reading_guide.md)**.

---

## Current research record

| Research record | Current state |
| --- | ---: |
| Proved statements | **52 propositions** |
| Reproducible studies | **38 experiments, A-Z and AA-AL** |
| Scientific result figures | **25 figures** |
| Claim-level tests | **177 tests** |
| CI matrix | **Python 3.10, 3.11, 3.12** |
| Research-software version | **0.40.0** |

The separate physics pipeline is an explanatory diagram and is not included in the scientific-result figure count.

### Start here

**Physics story and equation dictionary:** [Physics Guide](docs/physics_guide.md)  
**How to read the figures:** [Figure Reading Guide](docs/figure_reading_guide.md)  
**Research story:** [Research Overview](docs/research_overview.md)  
**Theorem and experiment map:** [Research Index](docs/research_index.md)  
**Propositions 1-43:** [Proved results and open problems](docs/proofs_and_conjectures.md)  
**Propositions 44-52:** [P44](docs/proposition_44_nuisance_projection.md) · [P45](docs/proposition_45_estimated_ar1_nuisance_projection.md) · [P46](docs/proposition_46_design_specific_ar1_envelope.md) · [P47](docs/proposition_47_weighted_wishart_matrix_chernoff.md) · [P48](docs/proposition_48_uniform_matrix_chernoff_ar1.md) · [P49](docs/proposition_49_compact_temporal_family.md) · [P50](docs/proposition_50_calibrated_temporal_family.md) · [P51](docs/proposition_51_evalue_temporal_confidence_set.md) · [P52](docs/proposition_52_certified_evalue_outer_cover.md)  
**Assumptions and failure conditions:** [Assumption Ledger](docs/assumption_ledger.md)  
**Consciousness interpretation rules:** [Interpretation Protocol](docs/interpretation_protocol.md)

---

# Latest result: carry temporal-memory uncertainty into an independent target covariance

## Proposition 52 and Experiment AL

[![Experiment AL: certified e-value outer cover](docs/certified_evalue_outer_cover.svg)](docs/proposition_52_certified_evalue_outer_cover.md)

### The physical problem

Suppose a separate calibration experiment tells us which temporal-memory models are still compatible with a measured physical process. A second, independent target experiment shares the same temporal parameters but contains its own stochastic fluctuations and a declared nuisance drift.

It is not enough to choose the single best-fitting temporal parameter and proceed as though it were exact. The covariance certificate used downstream should remain valid for **every temporal model the calibration data have not ruled out**.

Proposition 51 provides an exact continuum confidence set

\[
\mathcal C_\alpha(Z)
=
\left\{
(\phi,\eta):
\log e_{\phi,\eta}(Z)<\log(1/\alpha)
\right\}.
\]

A plotting grid is useful for seeing that set, but a plotting grid is not automatically a certified representation between grid points.

Proposition 52 closes that gap.

### The mathematical step

A fixed parameter grid partitions the declared temporal family into cells. A cell is removed only if a deterministic likelihood perturbation bound proves that **every parameter inside it** is outside the exact Proposition 51 confidence set.

If \(\mathcal O_\alpha(Z)\) denotes the union of retained cells, Proposition 52 proves

\[
\boxed{
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z)
}.
\]

The retained cover can then be passed to Proposition 49 for an independent target record.

Two different target geometry radii are carried deliberately:

\[
\delta_{\mathrm{eig}}
\]

controls the nuisance-compressed temporal eigenvalues used by matrix concentration, while

\[
\delta_{\mathrm{norm}}
\]

controls the projected trace normalization using the raw temporal operator radius and the equal-trace property of the temporal family.

These quantities answer different mathematical questions and are not interchangeable.

### Experiment AL

The controlled experiment uses

\[
\phi_*=0.50,
\qquad
\eta_*=0.01,
\]

with 48 calibration time samples across 256 independent channels. The declared parameter box is

\[
\phi\in[0.30,0.70],
\qquad
\eta\in[0,0.05].
\]

The fixed `121 x 61` outer grid contains **7,381 cells**.

For the committed deterministic record:

- **5,325 cells** are retained;
- **2,056 cells** are certified excluded;
- the target eigenvalue-cover radius is `0.03170414963221639`;
- the target normalization-cover radius is `0.07038592646700755`;
- calibration confidence is `0.975`;
- target covariance confidence is `0.975`;
- the combined confidence lower bound is `0.950625`;
- the final relative target covariance radius is

\[
\boxed{0.8998157009696983<1}.
\]

A separate 128-trial target visibility study has median relative error about `0.116`, 95th percentile about `0.304`, and maximum about `0.544`. All 128 displayed errors lie below the theorem radius.

Those trials are diagnostics, not the proof. The guarantee comes from the Proposition 51 e-value result, deterministic cell containment, and conditional Proposition 49 matrix concentration for the independent target record.

The threshold one is a mathematical perturbation threshold. It is not a physical phase transition.

[Full proof](docs/proposition_52_certified_evalue_outer_cover.md) · [machine-readable Experiment AL](docs/certified_evalue_outer_cover.json) · [experiment script](examples/certified_evalue_outer_cover.py) · [SVG renderer](examples/render_certified_evalue_outer_cover.py) · [claim-level tests](tests/test_evalue_outer_cover.py)

---

# What covariance means physically

For a fluctuating multivariate system,

\[
\Sigma
=
\mathbb E[(X-\mu)(X-\mu)^\top]
\]

describes the geometry of fluctuations.

Diagonal entries are coordinate variances. Off-diagonal entries describe co-fluctuation. Eigenvectors describe collective fluctuation directions and eigenvalues describe variance along those directions.

These eigenvalues are **not automatically physical energies**. An energy interpretation requires a separate physical derivation connecting the coordinates and covariance to a Hamiltonian, temperature, power spectrum, or another energetic quantity.

The recent covariance theorems control quantities such as

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

When \(\epsilon<1\), the estimate remains in a perturbative regime where positive variance directions, inverse covariance quantities, and later Gaussian information calculations can be controlled.

---

# Why temporal physics matters

Repeated physical measurements are usually correlated in time. Treating them as independent would overstate how much information a finite record contains.

The simplest recent temporal model is

\[
R_\phi(i,j)=\phi^{|i-j|}.
\]

If samples are separated by \(\Delta t\), the AR(1) parameter can be related to an effective relaxation time through

\[
\tau=-\frac{\Delta t}{\log\phi},
\]

when the AR(1) approximation is physically appropriate.

The recent two-parameter family is

\[
R_{\phi,\eta}
=(1-\eta)R_\phi+\eta I.
\]

Here \(\phi\) controls persistence of the correlated component and \(\eta\) is a temporally uncorrelated variance fraction inside this effective model.

Real physical systems may require multiple relaxation times, oscillatory kernels, colored noise, nonstationarity, or continuous spectral densities. The current family is a controlled mathematical model, not a universal law.

---

# The recent theorem ladder, with physical meaning

| Proposition | Mathematical question | Physical question |
| ---: | --- | --- |
| **41** | How does temporal dependence alter covariance concentration? | How much independent information is really in a record with memory? |
| **42** | What changes when an unknown constant mean is removed? | How does subtracting an unknown baseline change usable fluctuation information? |
| **43** | Can a shared nonnegative AR(1) coefficient be estimated? | Can a persistence timescale be learned instead of assumed? |
| **44** | Can the target mean vary inside a declared temporal subspace? | Can known drift shapes be removed without corrupting fluctuation covariance? |
| **45** | Can temporal calibration and nuisance projection be combined? | Can memory uncertainty and deterministic drift be handled together? |
| **46** | Can actual nuisance geometry replace a rank-only worst case? | Can the real shape of removed drift modes improve the information budget? |
| **47** | Can direct matrix concentration replace a sphere-net bound? | Can complete fluctuation modes be certified without a loose directional approximation? |
| **48** | Can the matrix bound survive unknown AR(1)? | Does the covariance guarantee survive uncertainty in relaxation time? |
| **49** | Can a compact temporal family be covered? | Can a physically admissible family of memory kernels be propagated safely? |
| **50** | Can a two-parameter family be learned from calibration data? | Can persistence and fast uncorrelated variance be estimated from an independent experiment? |
| **51** | Can full likelihood produce a continuum confidence set? | Which temporal models remain compatible with the complete calibration record? |
| **52** | Can that continuum set be certified for target use? | Can all still-compatible temporal memory be carried into an independent target covariance guarantee? |

---

# Moving-boundary recovery: the physical target of the statistical machinery

| Candidate scores | Recovery landscape |
| --- | --- |
| [![Candidate scores over time](docs/worldtube_baseline.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) | [![World-tube phase diagram](docs/worldtube_phase_diagram.png)](docs/reproducible_results.md#experiment-b-changing-boundary-world-tube) |

A controlled planted module moves through the coordinates as

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

A useful physical analogy is a coherent structure moving across a sensor array. The same organization persists while the sensors representing it change.

The optimizer recovers the planted path in the stated construction. The phase diagram also retains the failure region where continuity regularization is too strong. That failure region is part of the result: a prior preference for smooth motion can overwhelm measured evidence if it is weighted too heavily.

---

# The central observer-like objective

At each time, a candidate subsystem is evaluated through:

1. **internal integration**, evaluated across the weakest internal bipartition;
2. **environmental insulation**, penalizing predictive information imported from outside the candidate;
3. **persistence**, measuring predictive structure into the next state;
4. **transport**, rewarding predictive continuity when physical membership changes.

A dynamic program computes the maximizing world-tube in the declared candidate family. A second calculation identifies the best competing path. Their difference gives an optimization margin that can be propagated through deterministic and finite-sample perturbation bounds.

The repository sometimes calls this an `action margin`. It is an objective difference, **not physical action in joule-seconds** unless a future derivation explicitly connects the objective to a physical action functional.

---

# Identifiability before interpretation

Optimization is not identifiability.

If two admissible models produce the same declared observational law while assigning incompatible labels outside the allowed symmetry class, no estimator using only those observations can uniformly recover both labels.

The standing rule is therefore:

> **Every recovery statement is relative to declared observables, physical modeling assumptions, candidate families, and admissible symmetries.**

A physically serious application should document the observables, units, sampling interval, preprocessing, effective coupling model, nuisance modes, temporal assumptions, candidate geometry, and model-failure tests.

---

# What the repository establishes

Under its stated assumptions, the repository provides a conditional mathematical pipeline for:

- defining observer-like subsystem scores;
- optimizing moving subsystem paths;
- quantifying exact optimization margins;
- proving path stability under deterministic perturbations;
- deriving finite-sample Gaussian covariance guarantees;
- handling temporally dependent observations;
- removing declared nuisance means and drifts;
- learning uncertain temporal-memory models from calibration data;
- constructing a finite-sample continuum confidence set for a two-parameter temporal family;
- turning that continuum set into a certified finite outer cover;
- propagating the retained temporal uncertainty into an independent target covariance certificate.

## What is not established

The repository does not establish that every physical system has a unique observer boundary. It does not establish that Gaussianity, separability, or the current AR(1) plus white-noise family holds in a particular experiment without validation. It does not establish consciousness.

A physical application must still justify what is measured, the units and sampling interval, the adequacy of the effective dynamics, the nuisance interpretation, the temporal model, the physical candidate geometry, and the tests that could falsify those assumptions.

Any consciousness hypothesis requires an additional bridge with independent empirical content. Those obligations are documented in the [Interpretation Protocol](docs/interpretation_protocol.md).

---

# Reproduce

```bash
git clone https://github.com/MahsaKeikha/spatiotemporal-observer-math.git
cd spatiotemporal-observer-math
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Run Proposition 52 and regenerate its figure:

```bash
python examples/certified_evalue_outer_cover.py
python examples/render_certified_evalue_outer_cover.py
```

Run the preceding calibration result:

```bash
python examples/evalue_temporal_confidence_set.py
python examples/render_evalue_temporal_confidence_set.py
```

Each recent numerical claim is paired with machine-readable JSON, reproducible code, a visible figure when useful, and claim-level tests.

## Repository map

- [`docs/physics_guide.md`](docs/physics_guide.md) explains the physical meaning of the mathematical objects.
- [`docs/figure_reading_guide.md`](docs/figure_reading_guide.md) explains how to interpret structural, calibration, and certification plots.
- [`docs/physics_pipeline.svg`](docs/physics_pipeline.svg) shows the physical inference pipeline.
- [`src/observer_math/`](src/observer_math/) contains the mathematical implementation.
- [`tests/`](tests/) contains tests tied to scientific claims.
- [`examples/`](examples/) contains reproducible numerical studies and figure renderers.
- [`docs/research_overview.md`](docs/research_overview.md) explains the research as a narrative.
- [`docs/research_index.md`](docs/research_index.md) maps propositions, experiments, figures, data, and code.
- [`docs/assumption_ledger.md`](docs/assumption_ledger.md) records assumptions and failure conditions.
- [`docs/interpretation_protocol.md`](docs/interpretation_protocol.md) states requirements for any future consciousness interpretation.
- [`CITATION.cff`](CITATION.cff) contains citation metadata.

## Citation

Citation metadata is maintained in [`CITATION.cff`](CITATION.cff). The current research-software version is **0.40.0**.

## License

MIT. See [`LICENSE`](LICENSE).