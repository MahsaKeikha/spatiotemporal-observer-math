# Research index

This page is the navigation layer for the repository. It separates physical interpretation, proved mathematics, reproducible numerical evidence, software verification, assumptions, and consciousness interpretation so each layer can be audited independently.

A numerical experiment is not presented as a proof. A theorem is not presented as evidence that its assumptions hold in nature. An optimized world-tube is not presented as proof of consciousness.

## Current research record

| Record | Current state |
| --- | ---: |
| Propositions | **52** |
| Reproducible experiments | **38, A-Z and AA-AL** |
| Scientific result figures | **25** |
| Claim-level tests | **177** |
| Research-software version | **0.40.0** |

The physics pipeline is an explanatory diagram and is not included in the scientific-result figure count.

## Where to start

| Reader goal | Best page |
| --- | --- |
| Understand what the equations mean physically | [Physics Guide](physics_guide.md) |
| Learn how to interpret the figures and theorem radii | [Figure Reading Guide](figure_reading_guide.md) |
| Understand the research story without reading every proof | [Research Overview](research_overview.md) |
| See the newest result first | [Repository front page](../README.md) |
| Audit Propositions 1-43 | [Proved results and open problems](proofs_and_conjectures.md) |
| Audit Proposition 44 | [Time-varying nuisance projection](proposition_44_nuisance_projection.md) |
| Audit Proposition 45 | [Estimated AR(1) plus nuisance projection](proposition_45_estimated_ar1_nuisance_projection.md) |
| Audit Proposition 46 | [Design-specific AR(1) interval geometry](proposition_46_design_specific_ar1_envelope.md) |
| Audit Proposition 47 | [Weighted Gaussian matrix concentration](proposition_47_weighted_wishart_matrix_chernoff.md) |
| Audit Proposition 48 | [Uniform matrix concentration over calibrated AR(1)](proposition_48_uniform_matrix_chernoff_ar1.md) |
| Audit Proposition 49 | [Compact temporal-family matrix concentration](proposition_49_compact_temporal_family.md) |
| Audit Proposition 50 | [Data-calibrated two-parameter temporal family](proposition_50_calibrated_temporal_family.md) |
| Audit Proposition 51 | [Finite-sample e-value confidence set](proposition_51_evalue_temporal_confidence_set.md) |
| Audit Proposition 52 | [Certified e-value outer cover](proposition_52_certified_evalue_outer_cover.md) |
| Inspect assumptions and failure conditions | [Assumption Ledger](assumption_ledger.md) |
| Inspect requirements for any future consciousness interpretation | [Interpretation Protocol](interpretation_protocol.md) |

---

# The theorem chain

## Foundations: Propositions 1-14

| No. | Plain-language role |
| ---: | --- |
| 1 | Computes adjacent-state covariance for time-varying linear Gaussian dynamics. |
| 2 | Shows canonical transport is invariant to invertible reparameterization inside declared blocks. |
| 3 | Proves the implemented transport factors remain in the unit interval. |
| 4 | Converts an optimization margin into a deterministic score-error radius that preserves the winner. |
| 5 | Gives a componentwise planted-path recovery condition. |
| 6 | Connects a simultaneous score event to path-recovery probability. |
| 7 | Controls Gaussian conditional mutual information from covariance error. |
| 8 | Controls canonical persistence from covariance error. |
| 9 | Gives the first end-to-end Gaussian sample-complexity guarantee. |
| 10 | Improves product-score stability when factors stay away from zero. |
| 11 | Localizes finite-sample path certification to candidate-specific covariance blocks. |
| 12 | Propagates transition and noise perturbations directly to recovery. |
| 13 | Formalizes identifiability modulo objective-preserving symmetry. |
| 14 | Gives a two-model impossibility bound for observationally identical incompatible labels. |

Detailed statements and proofs: [Propositions 1-14](proofs_and_conjectures.md).

## Structural compression: Propositions 15-31

| Range | Main contribution |
| --- | --- |
| 15-20 | Near-competitor graphs, symbolic moving-clique recovery, perturbation propagation, structural-null CMI control, and support-resolved recovery. |
| 21-25 | Row-local budgets, overlap classes, block sparsity, and covariance influence cones for fixed and moving partitions. |
| 26-31 | Moving-partition path recovery, class compression, interval-certified classes, covariance-residual intervals, block-structural residuals, and screened environmental recovery. |

Detailed statements and proofs: [Propositions 15-31](proofs_and_conjectures.md).

## Statistical screening and drift: Propositions 32-40

| No. | Plain-language role |
| ---: | --- |
| 32 | Independent sample-split confidence composition. |
| 33 | Gaussian first-split screening safety. |
| 34 | Positive-factor refinement of Gaussian screening. |
| 35 | Structural-null screening at score boundaries. |
| 36 | Trajectory-coupled Gaussian screening. |
| 37 | Covariance-normalized Gaussian screening. |
| 38 | Pilot-normalized adaptive screening. |
| 39 | Drift-robust pilot-normalized screening. |
| 40 | Statistically calibrated population drift. |

Detailed statements and proofs: [Propositions 32-40](proofs_and_conjectures.md).

## Dependent measurements and temporal calibration: Propositions 41-52

| No. | Mathematical role | Physical role | Direct source |
| ---: | --- | --- | --- |
| 41 | Dependent Gaussian covariance concentration | Corrects the information budget when samples have memory | [Proof record](proofs_and_conjectures.md) |
| 42 | Mean-centered temporal normalization | Accounts for removing an unknown baseline | [Proof record](proofs_and_conjectures.md) |
| 43 | Observable AR(1) calibration | Learns persistence instead of assuming it | [Proof record](proofs_and_conjectures.md) |
| 44 | Fixed nuisance-subspace projection | Removes declared drift shapes before covariance estimation | [Proof](proposition_44_nuisance_projection.md) |
| 45 | Estimated dependence plus nuisance projection | Handles memory uncertainty and drift together | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) |
| 46 | Design-specific temporal geometry | Uses the actual removed drift geometry rather than only its rank | [Proof](proposition_46_design_specific_ar1_envelope.md) |
| 47 | Direct matrix concentration | Uses the complete projected temporal fluctuation spectrum | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) |
| 48 | Uniform matrix concentration over AR(1) uncertainty | Keeps the covariance guarantee valid across uncertain relaxation time | [Proof](proposition_48_uniform_matrix_chernoff_ar1.md) |
| 49 | Compact temporal-family cover | Propagates a complete family of admissible memory kernels | [Proof](proposition_49_compact_temporal_family.md) |
| 50 | Two-parameter temporal calibration | Learns persistence and fast uncorrelated variance from independent calibration | [Proof](proposition_50_calibrated_temporal_family.md) |
| 51 | Continuum e-value confidence set | Uses the full calibration residual likelihood to retain compatible temporal models | [Proof](proposition_51_evalue_temporal_confidence_set.md) |
| 52 | Certified finite outer cover plus target composition | Carries every still-compatible temporal model into an independent target covariance certificate | [Proof](proposition_52_certified_evalue_outer_cover.md) |

The newest sequence can be read as one physical measurement problem:

```text
Physical record has memory and drift
        -> P41-P46: calibrate effective information and nuisance geometry
Need a tight covariance guarantee
        -> P47-P49: direct matrix concentration over temporal families
Temporal family is not known
        -> P50-P51: learn a finite-sample parameter confidence set
A continuum confidence set must be used by a finite target theorem
        -> P52: certify an outer cover and propagate it to an independent target record
```

---

# Experiment index

Experiments are organized by the mathematical question they expose. Failure regions and conservative gaps remain part of the record.

## Experiments A-AC

These cover the original boundary objective, changing-boundary world-tubes, finite-sample recovery, identifiability counterexamples, structural compression, Gaussian screening, drift calibration, dependent sampling, and the first observable AR(1) calibration results.

Full commands and numerical records: [Reproducible results](reproducible_results.md).

## Recent experiments AD-AL

| ID | Proposition | What it tests | Physical reading | Proof, data, code |
| --- | ---: | --- | --- | --- |
| AD | 44 | Time-varying nuisance projection | Large deterministic drift should not masquerade as fluctuation covariance | [Proof](proposition_44_nuisance_projection.md) · [JSON](nuisance_projection_calibration.json) · [script](../examples/nuisance_projection_calibration.py) |
| AE | 45 | Estimated AR(1) plus affine nuisance mean | Memory uncertainty and drift can be propagated together | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) · [JSON](estimated_ar1_nuisance_projection.json) · [script](../examples/estimated_ar1_nuisance_projection.py) |
| AF | 46 | Design-specific interval geometry | The physical shape of removed drift modes matters, not only their count | [Proof](proposition_46_design_specific_ar1_envelope.md) · [JSON](design_specific_ar1_envelope.json) · [script](../examples/design_specific_ar1_envelope.py) |
| AG | 47 | Weighted Gaussian matrix concentration | Complete temporal fluctuation modes can tighten covariance certification | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) · [JSON](weighted_wishart_matrix_chernoff.json) · [script](../examples/weighted_wishart_matrix_chernoff.py) |
| AH | 48 | Interval-uniform matrix concentration | Uncertain relaxation time can be carried through the matrix bound | [Proof](proposition_48_uniform_matrix_chernoff_ar1.md) · [JSON](uniform_matrix_chernoff_ar1.json) · [script](../examples/uniform_matrix_chernoff_ar1.py) |
| AI | 49 | Compact temporal-family concentration | A full family of memory kernels can be represented by certified geometry | [Proof](proposition_49_compact_temporal_family.md) · [JSON](compact_temporal_family.json) · [script](../examples/compact_temporal_family.py) |
| AJ | 50 | Observable two-parameter calibration | More independent calibration narrows uncertainty without changing the target physics | [Proof](proposition_50_calibrated_temporal_family.md) · [JSON](calibrated_temporal_family.json) · [script](../examples/calibrated_temporal_family.py) |
| AK | 51 | Full-likelihood e-value calibration | The full residual record defines a joint continuum set of compatible temporal models | [Proof](proposition_51_evalue_temporal_confidence_set.md) · [JSON](evalue_temporal_confidence_set.json) · [script](../examples/evalue_temporal_confidence_set.py) |
| AL | 52 | Certified e-value outer cover and target composition | Every calibration-compatible temporal model is carried into an independent target covariance certificate | [Proof](proposition_52_certified_evalue_outer_cover.md) · [JSON](certified_evalue_outer_cover.json) · [script](../examples/certified_evalue_outer_cover.py) |

### Latest figure

[![Experiment AL](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md)

The figure is explained panel by panel in the [Figure Reading Guide](figure_reading_guide.md).

---

# Current frontier

Proposition 52 closes the immediate gap between the Proposition 51 continuum confidence set and Proposition 49's finite target-family interface.

The next statistical frontier is to extend finite-sample temporal calibration beyond the current AR(1) plus white-noise family toward richer kernels or spectral-density models.

The next physics frontier is to make sampling and representation more explicit:

> **Which observer-like conclusions are stable when sampling interval, sensor units, sensor basis, spatial resolution, or physically admissible coarse graining changes?**

The structural frontier remains intervention-sensitive and representation-invariant observer quantities, together with impossibility theorems for distinctions that passive observations cannot identify.

Any future consciousness interpretation must enter only as a separate bridge hypothesis under the [Interpretation Protocol](interpretation_protocol.md).

---

# Reproduction and audit rule

A result is considered complete in this repository when the relevant pieces exist together:

- a physical problem statement when a physical reading is intended;
- a declared measurement model;
- a precise mathematical statement;
- assumptions stated close to the claim;
- a proof or derivation;
- a code implementation;
- tests tied to the mathematical claim;
- a reproducible experiment when a numerical scale comparison is useful;
- machine-readable results for committed numerical claims;
- a visible figure when a figure improves understanding;
- a clear statement of what the result does not establish;
- a front-page or index link so the result is discoverable.

The repository also enforces a prose-style check that rejects Unicode en dash and em dash characters in Markdown documentation.