# Research index

This page is the navigation layer for the repository. It separates proved mathematics, reproducible numerical evidence, software verification, assumptions, and interpretation so each layer can be audited independently.

A numerical experiment is not presented as a proof. A theorem is not presented as evidence that its assumptions hold in nature. An optimized world-tube is not presented as proof of consciousness.

## Current research record

| Record | Current state |
| --- | ---: |
| Propositions | **51** |
| Reproducible experiments | **37, A-Z and AA-AK** |
| Committed scientific figures | **24** |
| Claim-level tests | **171** |
| Research-software version | **0.39.0** |

## Where to start

| Reader goal | Best page |
| --- | --- |
| Understand the scientific question without reading all proofs | [Research overview](research_overview.md) |
| See the newest results and figures first | [Repository front page](../README.md) |
| Audit Propositions 1-43 | [Proved results and open problems](proofs_and_conjectures.md) |
| Audit Proposition 44 | [Time-varying nuisance projection](proposition_44_nuisance_projection.md) |
| Audit Proposition 45 | [Estimated AR(1) plus nuisance projection](proposition_45_estimated_ar1_nuisance_projection.md) |
| Audit Proposition 46 | [Design-specific AR(1) interval geometry](proposition_46_design_specific_ar1_envelope.md) |
| Audit Proposition 47 | [Weighted Gaussian matrix concentration](proposition_47_weighted_wishart_matrix_chernoff.md) |
| Audit Proposition 48 | [Uniform matrix concentration over calibrated AR(1)](proposition_48_uniform_matrix_chernoff_ar1.md) |
| Audit Proposition 49 | [Compact temporal-family matrix concentration](proposition_49_compact_temporal_family.md) |
| Audit Proposition 50 | [Data-calibrated two-parameter temporal family](proposition_50_calibrated_temporal_family.md) |
| Audit Proposition 51 | [Finite-sample e-value confidence set](proposition_51_evalue_temporal_confidence_set.md) |
| Reproduce Experiments A-AC | [Reproducible results](reproducible_results.md) |
| Inspect assumptions and failure conditions | [Assumption ledger](assumption_ledger.md) |
| Inspect requirements for any future consciousness interpretation | [Interpretation protocol](interpretation_protocol.md) |

---

# The theorem chain

## Foundations: Propositions 1-14

| No. | Plain-language role |
| ---: | --- |
| 1 | Computes adjacent-state covariance for time-varying linear Gaussian dynamics. |
| 2 | Shows canonical transport is invariant to invertible reparameterization inside declared blocks. |
| 3 | Proves the implemented transport factors remain in the unit interval. |
| 4 | Converts an action margin into a deterministic score-error radius that preserves the winner. |
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

## Dependent Gaussian sampling and temporal calibration: Propositions 41-51

| No. | What changed | Direct source |
| ---: | --- | --- |
| 41 | Replaces independent temporal sampling by separably dependent Gaussian sampling. | [Proof record](proofs_and_conjectures.md) |
| 42 | Corrects normalization after removing an unknown constant mean. | [Proof record](proofs_and_conjectures.md) |
| 43 | Estimates a shared nonnegative AR(1) coefficient and propagates its uncertainty. | [Proof record](proofs_and_conjectures.md) |
| 44 | Replaces constant mean removal by projection away from any fixed declared nuisance subspace. | [Proof](proposition_44_nuisance_projection.md) |
| 45 | Combines observable AR(1) calibration with nuisance projection and normalization uncertainty. | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) |
| 46 | Uses the actual nuisance design over the full calibrated AR(1) interval instead of only its rank. | [Proof](proposition_46_design_specific_ar1_envelope.md) |
| 47 | Replaces the sphere-net operator-norm reduction with direct matrix concentration using the full temporal spectrum. | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) |
| 48 | Makes Proposition 47 uniform over a calibrated AR(1) interval by controlling projected temporal eigenvalues between grid points. | [Proof](proposition_48_uniform_matrix_chernoff_ar1.md) |
| 49 | Replaces the one-dimensional AR(1) continuum by any compact temporal covariance family with a certified finite cover. | [Proof](proposition_49_compact_temporal_family.md) |
| 50 | Learns a random two-parameter temporal confidence rectangle from independent calibration data and composes it with Proposition 49. | [Proof](proposition_50_calibrated_temporal_family.md) |
| 51 | Uses the complete residual Gaussian likelihood to construct a finite-sample continuum e-value confidence set directly in two-parameter space. | [Proof](proposition_51_evalue_temporal_confidence_set.md) |

The latest progression is:

```text
Can the mean vary with time?
        -> Proposition 44
Can temporal dependence be estimated?
        -> Proposition 45
Can we use the actual nuisance geometry?
        -> Proposition 46
Can we remove the sphere-net concentration bottleneck?
        -> Proposition 47
Can the matrix bound survive an unknown AR(1) coefficient?
        -> Proposition 48
Can the concentration theorem stop depending on AR(1) geometry?
        -> Proposition 49
Can a multi-parameter temporal family be learned from data?
        -> Proposition 50
Can the full likelihood learn joint parameter geometry without rectangular lag propagation?
        -> Proposition 51
```

---

# Experiment index

Experiments are organized by the mathematical question they expose. Failure regions and conservative gaps remain part of the record.

## Experiments A-J

Basic objective behavior, changing-boundary world-tubes, finite-sample recovery, identifiability counterexamples, symbolic moving-clique recovery, robust perturbation regions, block-sparse recovery, and covariance influence cones.

## Experiments K-R

Class compression, interval classes, covariance-residual classes, block-structural residuals, screened environmental recovery, sample-split confidence accounting, and safe Gaussian screening.

## Experiments S-Z

Gaussian screening calibration, structural-null refinements, trajectory-coupled sampling, covariance-normalized screening, reusable pilot geometry, population drift, and empirical drift calibration.

## Experiments AA-AC

| ID | Main purpose |
| --- | --- |
| AA | Quantifies how temporal correlation reduces effective sample size. |
| AB | Verifies exact normalization after removing an unknown constant mean. |
| AC | Estimates temporal dependence and checks joint interval and covariance coverage. |

Full commands and numerical records: [Experiments A-AC](reproducible_results.md).

## Latest experiments AD-AK

| ID | Result | What to notice | Proof, data, code |
| --- | --- | --- | --- |
| AD | Time-varying nuisance projection | Ordinary centering fails under affine drift while declared nuisance projection remains stable. | [Proof](proposition_44_nuisance_projection.md) · [JSON](nuisance_projection_calibration.json) · [script](../examples/nuisance_projection_calibration.py) |
| AE | Estimated AR(1) plus affine nuisance mean | Observable calibration tracks the oracle, while the earlier concentration radius becomes loose at stronger correlation. | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) · [JSON](estimated_ar1_nuisance_projection.json) · [script](../examples/estimated_ar1_nuisance_projection.py) |
| AF | Design-specific interval geometry | A rank-only certificate can become vacuous even when the actual nuisance geometry retains substantial covariance information. | [Proof](proposition_46_design_specific_ar1_envelope.md) · [JSON](design_specific_ar1_envelope.json) · [script](../examples/design_specific_ar1_envelope.py) |
| AG | Weighted Gaussian matrix concentration | Direct matrix concentration materially reduces the displayed covariance radii. | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) · [JSON](weighted_wishart_matrix_chernoff.json) · [script](../examples/weighted_wishart_matrix_chernoff.py) |
| AH | Interval-uniform matrix concentration | Unknown AR(1) correlation no longer forces the displayed strong-correlation certificate above one. | [Proof](proposition_48_uniform_matrix_chernoff_ar1.md) · [JSON](uniform_matrix_chernoff_ar1.json) · [script](../examples/uniform_matrix_chernoff_ar1.py) |
| AI | Compact temporal-family concentration | A two-parameter temporal family crosses below radius one under deterministic cover refinement while the earlier sphere-net family bound remains much larger. | [Proof](proposition_49_compact_temporal_family.md) · [JSON](compact_temporal_family.json) · [script](../examples/compact_temporal_family.py) |
| AJ | Observable two-parameter temporal calibration | Increasing only independent calibration information contracts the temporal family and moves the target covariance certificate below one at 64 channels. | [Proof](proposition_50_calibrated_temporal_family.md) · [JSON](calibrated_temporal_family.json) · [script](../examples/calibrated_temporal_family.py) |
| AK | Full-likelihood e-value temporal calibration | The complete residual likelihood produces a joint continuum confidence set. The displayed grid geometry contracts strongly with additional calibration channels and tightens the white-noise direction in the controlled example. | [Proof](proposition_51_evalue_temporal_confidence_set.md) · [JSON](evalue_temporal_confidence_set.json) · [script](../examples/evalue_temporal_confidence_set.py) |

### Eight newest figures

[![Experiment AD](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

[![Experiment AE](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

[![Experiment AF](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

[![Experiment AG](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

[![Experiment AH](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

[![Experiment AI](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

[![Experiment AJ](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

[![Experiment AK](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

---

# Current frontier

Proposition 51 proves coverage for the continuum e-value confidence set itself. The numerical grid in Experiment AK is a visualization, not a certified outer cover.

The immediate statistical target is:

> **Construct a certified adaptive outer cover of the Proposition 51 confidence set and compose that random cover with Proposition 49 for an independent target record.**

That theorem should guarantee that every parameter in the exact continuum confidence set is represented by the retained finite temporal cover. It should then carry the calibration confidence and target covariance confidence through one explicit end-to-end statement.

A parallel direction is to extend the same e-value principle beyond the AR(1) plus white-noise family toward richer covariance and spectral-density models.

The structural frontier is separate:

> **Develop intervention-sensitive and representation-invariant observer quantities, together with impossibility theorems for distinctions that passive observations cannot identify.**

Any later consciousness interpretation must enter only as a separate bridge hypothesis under the [interpretation protocol](interpretation_protocol.md).

---

# Reproduction and audit rule

A result is considered complete in this repository when the relevant pieces exist together:

- a precise mathematical statement;
- assumptions stated close to the claim;
- a proof or derivation;
- a code implementation;
- tests tied to the mathematical claim;
- a reproducible experiment when a numerical scale comparison is useful;
- machine-readable results for committed numerical claims;
- a visible figure when a figure improves understanding;
- a front-page or index link so the result is discoverable.

The repository also enforces a prose-style check that rejects Unicode en dash and em dash characters in Markdown documentation. Ordinary punctuation is used instead.
