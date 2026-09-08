# Research index

This page is the navigation layer for the repository. It separates physical interpretation, proved mathematics, reproducible numerical evidence, software verification, assumptions, and any later consciousness interpretation so each layer can be audited independently.

A numerical experiment is not presented as a proof. A theorem is not presented as evidence that its assumptions hold in nature. An optimized world-tube is not presented as proof of consciousness.

## Current research record

| Record | Current state |
| --- | ---: |
| Propositions | **53** |
| Reproducible experiments | **39, A-Z and AA-AM** |
| Scientific result figures | **26** |
| Claim-level tests | **183** |
| Research-software version | **0.41.0** |

The physics pipeline is an explanatory diagram and is not included in the scientific-result figure count.

## Where to start

| Reader goal | Best page |
| --- | --- |
| Understand the physical problem first | [Physics Guide](physics_guide.md) |
| Learn how to read the figures and theorem radii | [Figure Reading Guide](figure_reading_guide.md) |
| Follow the research as one coherent story | [Research Overview](research_overview.md) |
| See the complete visual history | [Repository front page](../README.md) |
| Audit Propositions 1-43 | [Proof record](proofs_and_conjectures.md) |
| Audit Propositions 44-52 | Proposition-specific proof pages listed below |
| Audit Proposition 53 | [Sampling-consistent physical relaxation time](proposition_53_physical_relaxation_time.md) |
| Inspect assumptions and failure conditions | [Assumption Ledger](assumption_ledger.md) |
| Inspect the temporal-calibration software interface | [Temporal Calibration API](api_temporal_calibration.md) |
| Inspect requirements for any future consciousness interpretation | [Interpretation Protocol](interpretation_protocol.md) |

---

# The theorem program

## Layer A. Foundations and first recovery theory, Propositions 1-14

These results establish adjacent-state covariance, representation invariance inside declared blocks, transport bounds, world-tube optimization robustness, finite-sample recovery, covariance perturbation control, and identifiability limits.

Detailed statements and proofs: [Propositions 1-14](proofs_and_conjectures.md).

## Layer B. Structural compression and moving-partition theory, Propositions 15-31

This layer develops near-competitor structure, symbolic moving-clique recovery, overlap classes, covariance influence cones, interval-certified structural classes, residual bounds, and screened environmental recovery.

Its purpose is to replace brute-force competitor enumeration with certified structure while keeping the moving-boundary problem explicit.

Detailed statements and proofs: [Propositions 15-31](proofs_and_conjectures.md).

## Layer C. Statistical screening and drift, Propositions 32-40

This layer introduces safe sample splitting, Gaussian screening, structural-null refinements, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

Detailed statements and proofs: [Propositions 32-40](proofs_and_conjectures.md).

## Layer D. Dependent measurements and temporal calibration, Propositions 41-52

| Proposition | Mathematical role | Physical role | Direct source |
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

## Layer E. Sampling-consistent physical time, Proposition 53

Proposition 53 changes the temporal parameterization from a sample-index coefficient to a physical time constant for the exponential relaxation model.

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

The theorem proves exact coarse-sampling consistency, time-unit invariance, validity on irregular timestamps, and a deterministic operator cover over a declared \(\tau\)-interval that composes with Proposition 49.

Direct source: [Proposition 53 proof](proposition_53_physical_relaxation_time.md).

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
| AM | 53 | Sampling-consistent physical relaxation time | Different acquisition rates produce different \(\phi\) values but the same physical \(\tau\) | [Proof](proposition_53_physical_relaxation_time.md) · [JSON](physical_relaxation_sampling.json) · [script](../examples/physical_relaxation_sampling.py) |

### Latest figure

[![Experiment AM](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

For \(\tau=0.8\) s, the controlled record uses sampling rates from 2.5 Hz through 40 Hz. The corresponding one-step correlations differ substantially, but each maps back to the same relaxation time. The figure also shows irregular timestamps and the deterministic continuum cover over \(\tau\in[0.55,1.05]\) s.

The figure is a visibility aid. The exact sampling identities and continuum bound are the theorem.

---

# Current frontier

Proposition 53 closes one representation issue: under the declared exponential model, temporal memory can be parameterized by a physical relaxation time rather than an arbitrary sample-to-sample coefficient.

The next physics questions are therefore more structural:

- which observer scores survive invertible changes of sensor coordinates;
- which transformations preserve the physical meaning of a candidate boundary;
- how spatial resolution and coarse graining change the candidate family;
- how richer temporal kernels alter the physical timescale picture;
- which distinctions require interventions rather than passive observations.

The next statistical frontier is to preserve finite-sample calibration while moving beyond one-timescale exponential or AR(1)-based temporal families.

Any future consciousness interpretation remains a separate bridge problem under the [Interpretation Protocol](interpretation_protocol.md).

---

# Reproduction and audit rule

A result is considered complete in this repository when the relevant pieces exist together: physical question, declared measurement model, mathematical statement, assumptions, proof, implementation, claim-level tests, reproducible numerical record when useful, visible figure when useful, explicit failure conditions, and discoverable links.

The documentation style check rejects Unicode en dash and em dash characters in Markdown files.
