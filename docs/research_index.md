# Research index

This page is the navigation layer for the repository. It separates physical interpretation, proved mathematics, reproducible numerical evidence, software verification, assumptions, literature sources, and any later consciousness interpretation so each layer can be audited independently.

A numerical experiment is not presented as a proof. A theorem is not presented as evidence that its assumptions hold in nature. An optimized world-tube is not presented as proof of consciousness. A citation is not presented as an endorsement by the cited author.

## Current research record

| Record | Current state |
| --- | ---: |
| Propositions | **53** |
| Reproducible experiments | **39, A-Z and AA-AM** |
| Scientific result figures | **27** |
| Claim-level tests | **188** |
| Research-software version | **0.41.1** |

The physics pipeline is an explanatory diagram and is not included in the scientific-result figure count.

## Where to start

| Reader goal | Best page |
| --- | --- |
| Trace the primary conceptual source and mathematical literature | [Bibliography and Citation Map](bibliography.md) |
| Use machine-readable references | [`references.bib`](../references.bib) |
| Understand the physical problem first | [Physics Guide](physics_guide.md) |
| Learn how to read the figures and theorem radii | [Figure Reading Guide](figure_reading_guide.md) |
| Follow the research as one coherent story | [Research Overview](research_overview.md) |
| See the complete visual history | [Repository front page](../README.md) |
| Audit Propositions 1-43 | [Proof record](proofs_and_conjectures.md) |
| Audit Propositions 44-52 | Proposition-specific proof pages listed below |
| Audit Proposition 53 | [Sampling-consistent physical relaxation time and irregular-grid Markov structure](proposition_53_physical_relaxation_time.md) |
| Inspect the current patch release | [0.41.1 Research Record](release_0_41_1.md) |
| Inspect assumptions and failure conditions | [Assumption Ledger](assumption_ledger.md) |
| Inspect the temporal-calibration software interface | [Temporal Calibration API](api_temporal_calibration.md) |
| Inspect requirements for any future consciousness interpretation | [Interpretation Protocol](interpretation_protocol.md) |

## Citation architecture

The project uses three citation roles and keeps them distinct.

1. **Primary conceptual source.** Max Tegmark's 2015 paper *Consciousness as a State of Matter* is the primary conceptual source and starting point for the research question developed in this repository.
2. **Direct mathematical or statistical source.** A theorem, inequality, distributional fact, or method that materially enters a proof or algorithm is cited as a direct source.
3. **Background lineage.** A paper can be scientifically important context without being the source of a proposition in this repository.

The complete attribution record, including proposition-to-literature mapping and DOI links, is maintained in the [Bibliography and Citation Map](bibliography.md). BibTeX entries are maintained in [`references.bib`](../references.bib).

This distinction matters because the repository develops new statements and proofs while building on established mathematics. Citing a paper does not imply that the cited author derived the repository's later propositions or endorses the project.

---

# The theorem program

## Layer A. Foundations and first recovery theory, Propositions 1-14

These results establish adjacent-state covariance, representation invariance inside declared blocks, transport bounds, world-tube optimization robustness, finite-sample recovery, covariance perturbation control, and identifiability limits.

Important literature foundations include Shannon and Cover and Thomas for information theory, Hotelling for canonical correlation, Bellman for dynamic programming, Wishart for Gaussian sample covariance, Bhatia for matrix analysis, and Davidson and Szarek for the Gaussian singular-value concentration step used in the finite-sample proof layer.

Detailed statements and proofs: [Propositions 1-14](proofs_and_conjectures.md). Literature roles: [Bibliography](bibliography.md).

## Layer B. Structural compression and moving-partition theory, Propositions 15-31

This layer develops near-competitor structure, symbolic moving-clique recovery, overlap classes, covariance influence cones, interval-certified structural classes, residual bounds, and screened environmental recovery.

Its purpose is to replace brute-force competitor enumeration with certified structure while keeping the moving-boundary problem explicit.

Detailed statements and proofs: [Propositions 15-31](proofs_and_conjectures.md).

## Layer C. Statistical screening and drift, Propositions 32-40

This layer introduces safe sample splitting, Gaussian screening, structural-null refinements, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

Detailed statements and proofs: [Propositions 32-40](proofs_and_conjectures.md).

## Layer D. Dependent measurements and temporal calibration, Propositions 41-52

| Proposition | Mathematical role | Physical role | Direct proof |
| ---: | --- | --- | --- |
| 41 | Dependent Gaussian covariance concentration | Corrects the information budget when samples have memory | [Proof record](proofs_and_conjectures.md) |
| 42 | Mean-centered temporal normalization | Accounts for removing an unknown baseline | [Proof record](proofs_and_conjectures.md) |
| 43 | Observable AR(1) calibration | Learns discrete persistence instead of assuming it | [Proof record](proofs_and_conjectures.md) |
| 44 | Fixed nuisance-subspace projection | Removes declared drift shapes before covariance estimation | [Proof](proposition_44_nuisance_projection.md) |
| 45 | Estimated dependence plus nuisance projection | Handles memory uncertainty and drift together | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) |
| 46 | Design-specific temporal geometry | Uses the actual removed drift geometry rather than only its rank | [Proof](proposition_46_design_specific_ar1_envelope.md) |
| 47 | Direct matrix concentration | Uses the complete projected temporal fluctuation spectrum | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) |
| 48 | Uniform matrix concentration over AR(1) uncertainty | Keeps the covariance guarantee valid across uncertain discrete persistence | [Proof](proposition_48_uniform_matrix_chernoff_ar1.md) |
| 49 | Compact temporal-family cover | Propagates a complete family of admissible memory kernels | [Proof](proposition_49_compact_temporal_family.md) |
| 50 | Two-parameter temporal calibration | Learns persistence and fast uncorrelated variance from independent calibration | [Proof](proposition_50_calibrated_temporal_family.md) |
| 51 | Continuum e-value confidence set | Uses the full calibration residual likelihood to retain compatible temporal models | [Proof](proposition_51_evalue_temporal_confidence_set.md) |
| 52 | Certified outer cover plus target composition | Carries every still-compatible temporal model into an independent target covariance certificate | [Proof](proposition_52_certified_evalue_outer_cover.md) |

The physical measurement story is:

```text
record has memory and drift
        -> P41-P46: effective information and nuisance geometry
need a tight covariance guarantee
        -> P47-P49: direct matrix concentration over temporal families
temporal family is uncertain
        -> P50-P51: finite-sample calibration of compatible models
continuum uncertainty must enter an independent target theorem
        -> P52: certified outer cover and target composition
```

Direct literature foundations for this layer include Laurent and Massart and Hsu, Kakade, and Zhang for quadratic-form concentration, Tropp for the matrix-Laplace concentration method, and Vovk and Wang and Shafer for the e-value literature. See the [proposition-to-literature map](bibliography.md#7-proposition-to-literature-map).

## Layer E. Sampling-consistent physical time and exact irregular-grid structure, Proposition 53

Proposition 53 changes the temporal parameterization from a sample-index coefficient to a physical time constant for the exponential relaxation model and then derives its exact local Gaussian representation on arbitrary increasing timestamps.

For physical sample times \(t_i\),

\[
R_\tau(i,j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

Under uniform sampling with interval \(\Delta t\),

\[
\phi_{\Delta t}
=
\exp\left(-\frac{\Delta t}{\tau}\right),
\qquad
\tau
=
-\frac{\Delta t}{\log\phi_{\Delta t}}.
\]

For irregular adjacent gaps, define

\[
\alpha_i
=
\exp\left(-\frac{t_{i+1}-t_i}{\tau}\right).
\]

The exact local transition law is

\[
X_{i+1}
=
\alpha_iX_i
+
\sqrt{1-\alpha_i^2}\,\varepsilon_i.
\]

The theorem proves exact coarse-sampling consistency, time-unit invariance, validity on irregular timestamps, a deterministic operator cover over a declared \(\tau\)-interval that composes with Proposition 49, exact innovation whitening, a tridiagonal temporal precision matrix, local determinant factorization, and exact missing-sample transition composition.

The physical stochastic-process lineage is the classical Ornstein-Uhlenbeck exponential-relaxation model of Uhlenbeck and Ornstein. Doob 1942 is recorded as historical Gaussian Markov-process context. The irregular-grid formulas themselves are derived directly in Proposition 53.

Direct source: [Proposition 53 proof](proposition_53_physical_relaxation_time.md). Release audit: [0.41.1 Research Record](release_0_41_1.md). Literature context: [Bibliography](bibliography.md#6-physical-relaxation-and-continuous-time-stochastic-dynamics).

---

# Experiment index

## Experiments A-AC

These cover the original boundary objective, changing-boundary world-tubes, finite-sample recovery, identifiability counterexamples, structural compression, Gaussian screening, drift calibration, dependent sampling, and the first observable AR(1) calibration results.

Full commands and numerical records: [Reproducible Results](reproducible_results.md).

## Recent experiments AD-AM

| ID | Proposition | Main question | Physical reading | Proof, data, code |
| --- | ---: | --- | --- | --- |
| AD | 44 | Time-varying nuisance projection | Large deterministic drift should not masquerade as fluctuation covariance | [Proof](proposition_44_nuisance_projection.md) |
| AE | 45 | Estimated AR(1) plus affine nuisance mean | Memory uncertainty and drift can be propagated together | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) |
| AF | 46 | Design-specific interval geometry | The physical shape of removed drift modes matters, not only their count | [Proof](proposition_46_design_specific_ar1_envelope.md) |
| AG | 47 | Weighted Gaussian matrix concentration | Complete temporal fluctuation modes can tighten covariance certification | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) |
| AH | 48 | Interval-uniform matrix concentration | Uncertain discrete persistence can be carried through the matrix bound | [Proof](proposition_48_uniform_matrix_chernoff_ar1.md) |
| AI | 49 | Compact temporal-family concentration | A full family of memory kernels can be represented by certified geometry | [Proof](proposition_49_compact_temporal_family.md) |
| AJ | 50 | Observable two-parameter calibration | More independent calibration narrows temporal uncertainty without changing the target record | [Proof](proposition_50_calibrated_temporal_family.md) |
| AK | 51 | Full-likelihood e-value calibration | The full residual record defines a continuum set of compatible temporal models | [Proof](proposition_51_evalue_temporal_confidence_set.md) |
| AL | 52 | Certified outer cover and target composition | Every calibration-compatible temporal model is carried into an independent target covariance certificate | [Proof](proposition_52_certified_evalue_outer_cover.md) |
| AM | 53 | Sampling-consistent physical relaxation and irregular-grid factorization | Sampling changes local coefficients while the same \(\tau\) generates exact local innovations and sparse temporal precision | [Proof](proposition_53_physical_relaxation_time.md) · [JSON](physical_relaxation_sampling.json) · [script](../examples/physical_relaxation_sampling.py) |

### Proposition 53 figures

| Sampling consistency | Exact irregular-grid Markov factorization |
| --- | --- |
| [![Experiment AM](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md) | [![Markov factorization](physical_relaxation_markov.svg)](proposition_53_physical_relaxation_time.md) |

For \(\tau=0.8\) s, the controlled record uses sampling rates from 2.5 Hz through 40 Hz. The corresponding one-step correlations differ substantially, but each maps back to the same relaxation time.

On the 13-point irregular record, the exact precision matrix has only 37 nonzero entries out of 169. The covariance-product, inverse, whitening, precision-Gram, and determinant identities all agree numerically to approximately \(10^{-15}\) or better.

The figures are visibility aids. The exact sampling, Markov, whitening, precision, determinant, and semigroup identities are the theorem.

---

# Current frontier

Proposition 53 now closes two representation issues under the declared one-timescale exponential Gaussian model: temporal memory is parameterized by a physical relaxation time rather than an arbitrary sample-to-sample coefficient, and that same physical-time model has an exact local transition representation under irregular or missing observations.

The next question inside this temporal line is whether \(\tau\) can be calibrated directly on irregular timestamps with a finite-sample confidence construction that exploits the exact innovation likelihood.

The broader next physics questions remain:

- which observer scores survive invertible changes of sensor coordinates;
- which transformations preserve the physical meaning of a candidate boundary;
- how spatial resolution and coarse graining change the candidate family;
- how richer temporal kernels alter the physical timescale picture;
- which distinctions require interventions rather than passive observations.

The next statistical frontier is to preserve finite-sample calibration while moving beyond one-timescale exponential or AR(1)-based temporal families.

Any future consciousness interpretation remains a separate bridge problem under the [Interpretation Protocol](interpretation_protocol.md).

---

# Reproduction and audit rule

A result is considered complete in this repository when the relevant pieces exist together: physical question, declared measurement model, mathematical statement, assumptions, proof, implementation, claim-level tests, reproducible numerical record when useful, visible figure when useful, explicit failure conditions, discoverable links, and attribution to any external theorem, method, or physical model materially used.

The documentation style check rejects Unicode en dash and em dash characters in Markdown files.
