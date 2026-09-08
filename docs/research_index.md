# Research index

This page is the navigation layer for the entire repository. It is written for a reader who did not participate in the development and should not have to guess how the pieces fit together.

The project contains three different kinds of evidence, and they are kept separate on purpose:

1. **proved statements** — mathematical results under explicit assumptions;
2. **reproducible experiments** — numerical studies that illustrate scale, tightness, failure modes, or implementation behavior;
3. **software checks** — tests that connect code paths to specific mathematical claims.

A numerical experiment is not presented as a proof. A theorem is not presented as evidence that its assumptions hold in nature. And an optimized world-tube is not presented as proof of consciousness.

## Where to start

| Reader goal | Best page |
| --- | --- |
| Understand the scientific question without reading all proofs | [Research overview](research_overview.md) |
| See the newest results and figures first | [Repository front page](../README.md) |
| Audit Propositions 1–43 in detail | [Proved results and open problems](proofs_and_conjectures.md) |
| Audit Proposition 44 | [Time-varying nuisance projection](proposition_44_nuisance_projection.md) |
| Audit Proposition 45 | [Estimated AR(1) + nuisance projection](proposition_45_estimated_ar1_nuisance_projection.md) |
| Audit Proposition 46 | [Design-specific AR(1) interval geometry](proposition_46_design_specific_ar1_envelope.md) |
| Audit Proposition 47 | [Weighted-Wishart matrix concentration](proposition_47_weighted_wishart_matrix_chernoff.md) |
| Reproduce Experiments A–AC | [Reproducible results](reproducible_results.md) |
| Reproduce the newest studies AD–AG | Follow the direct links in [Latest experiments](#latest-experiments-adag) |
| Inspect assumptions and interpretation limits | [Assumption ledger](assumption_ledger.md) |

---

# The theorem chain

The propositions are cumulative. Later results are not a disconnected list of increasingly complicated bounds; each one removes a specific restriction or source of conservatism from the previous pipeline.

## Foundations: defining and identifying the moving subsystem

| No. | Proposition | Plain-language role |
| ---: | --- | --- |
| 1 | Nonstationary adjacent covariance | Computes exact adjacent-state covariance for time-varying linear Gaussian dynamics. |
| 2 | Representation invariance of canonical transport | Shows canonical transport does not depend on invertible reparameterization inside the declared blocks. |
| 3 | Bounded transport score | Proves the implemented transport factors remain in the unit interval. |
| 4 | Finite-horizon path robustness certificate | Converts an action margin into a deterministic score-error radius that preserves the winning path. |
| 5 | Componentwise planted-path recovery | Gives a stronger but easier-to-check sufficient condition based on local and incident-edge advantages. |
| 6 | Finite-sample recovery from uniform score bounds | Connects a simultaneous score event to a path-recovery probability. |
| 7 | Covariance perturbation bound for Gaussian CMI | Controls conditional mutual information from spectral covariance error. |
| 8 | Canonical-persistence perturbation bound | Controls canonical correlations and persistence from covariance error. |
| 9 | End-to-end Gaussian sample-complexity guarantee | Produces the first complete covariance-to-world-tube finite-sample theorem. |
| 10 | Positive-factor stability of geometric scores | Replaces worst-case root behavior by local Lipschitz behavior away from zero score factors. |
| 11 | Localized finite-sample path certificate | Uses candidate-specific covariance blocks instead of one global error radius. |
| 12 | Parameter-level linear-Gaussian certificate | Propagates transition/noise perturbations directly to path recovery. |
| 13 | Objective identifiability modulo symmetry | Formalizes recovery only up to symmetries that leave the objective unchanged. |
| 14 | Two-model impossibility bound | Shows that observationally identical models with incompatible labels impose a one-half maximin ceiling. |

Detailed proofs: [Propositions 1–14](proofs_and_conjectures.md).

## Structural compression and localized recovery

| No. | Proposition | Plain-language role |
| ---: | --- | --- |
| 15 | Sufficient near-competitor graph | Safely removes states and edges that cannot challenge the winner. |
| 16 | Symbolic recovery for covariance-preserving moving cliques | Gives a closed-form moving-boundary base case. |
| 17 | Covariance propagation around the moving-clique family | Converts transition/noise perturbations to finite-horizon covariance radii. |
| 18 | Quadratic CMI bound at zero conditional cross-covariance | Exploits the fact that CMI grows quadratically near an exact structural null. |
| 19 | Robust recovery with external coupling and anisotropic noise | Extends symbolic recovery to a declared perturbation neighborhood. |
| 20 | Support-resolved finite-horizon recovery | Restricts covariance errors to score-relevant coordinates. |
| 21 | A priori row-local recovery | Uses row-local transition and forcing budgets without propagating the realized covariance. |
| 22 | Overlap-class recovery without candidate enumeration | Compresses candidate calculations to overlap classes. |
| 23 | Structural budgets from block sparsity | Converts entry magnitudes and block degrees to operator-norm budgets. |
| 24 | Block-local covariance influence cones | Proves finite-speed support propagation on a fixed block graph. |
| 25 | Moving-partition covariance influence cones | Extends influence cones to blocks that split, merge, or move. |
| 26 | Moving-partition path-recovery certificate | Propagates moving-partition covariance radii through the complete path objective. |
| 27 | Class-compressed robust path recovery | Replaces candidate lists by exact factor-symmetry classes. |
| 28 | Interval-certified class recovery | Allows bounded within-class heterogeneity instead of exact equality. |
| 29 | Covariance-residual derivation of class intervals | Derives factor intervals from representative covariances and spectral residuals. |
| 30 | Block-structural residual class recovery | Generates those residuals from moving block envelopes. |
| 31 | Screened-environment structural recovery | Allows source-specific present compression while explicitly charging omitted information. |

Detailed proofs: [Propositions 15–31](proofs_and_conjectures.md).

## Statistical screening, drift, and temporal dependence

| No. | Proposition | Plain-language role |
| ---: | --- | --- |
| 32 | Independent sample-split confidence composition | Separates data-dependent screening from final certification. |
| 33 | Gaussian first-split screening safety | Gives the first complete Gaussian concentration-to-screen guarantee. |
| 34 | Positive-factor refinement of Gaussian screening | Tightens state/edge radii when empirical factors are safely bounded away from zero. |
| 35 | Structural-null screening at the score boundary | Uses exact predeclared integration nulls to obtain a quadratic boundary bound. |
| 36 | Trajectory-coupled Gaussian screening safety | Allows all times to come from the same independent trajectories. |
| 37 | Covariance-normalized Gaussian screening | Removes the global covariance-condition-number penalty in population-whitened coordinates. |
| 38 | Pilot-normalized adaptive screening | Uses an observed pilot covariance to create candidate-specific later-cohort radii. |
| 39 | Drift-robust pilot-normalized screening | Transports the adaptive certificate under a declared population drift envelope. |
| 40 | Statistically calibrated population drift | Estimates a candidate-specific drift envelope from old and current calibration cohorts. |
| 41 | Separably dependent Gaussian covariance screening | Replaces i.i.d. sample count by dependence-aware temporal effective sample sizes. |
| 42 | Mean-centered separably dependent Gaussian screening | Corrects the covariance normalization after removing an unknown constant mean. |
| 43 | Same-record AR(1) calibration and covariance screening | Estimates a shared nonnegative AR(1) coefficient and propagates its uncertainty without requiring cross-event independence. |

Detailed proofs: [Propositions 32–43](proofs_and_conjectures.md).

## Current frontier: time-varying nuisance means and sharper dependent covariance concentration

| No. | Proposition | What changed | Direct proof |
| ---: | --- | --- | --- |
| 44 | Time-varying nuisance projection | Replaces constant mean-centering by projection away from any fixed declared temporal nuisance subspace. | [Proof](proposition_44_nuisance_projection.md) |
| 45 | Estimated AR(1) + nuisance projection | Combines observable AR(1) calibration with time-varying nuisance removal and normalization uncertainty. | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) |
| 46 | Design-specific AR(1) continuum envelope | Replaces rank-only nuisance pessimism by a rigorous interval certificate that uses the actual declared design geometry. | [Proof](proposition_46_design_specific_ar1_envelope.md) |
| 47 | Weighted-Wishart matrix concentration | Replaces the `1/4` sphere net and `9^m` factor by an exact matrix exponential moment and matrix-Laplace tail bound. | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) |

The newest chain is therefore

```text
unknown time-varying mean
        ↓
Proposition 44: exact nuisance projection
        ↓
unknown AR(1) coefficient
        ↓
Proposition 45: observable temporal calibration
        ↓
rank-only nuisance pessimism
        ↓
Proposition 46: actual design geometry over the whole interval
        ↓
sphere-net concentration bottleneck
        ↓
Proposition 47: direct matrix concentration using the full temporal spectrum
```

---

# Experiment index

Experiments are organized by what they are trying to reveal, not by how impressive their numerical values look. Failure regions and conservative gaps are part of the record.

## A–J: basic behavior, identifiability, and structural recovery

| ID | Experiment | Main purpose |
| --- | --- | --- |
| A | Fixed modular structure | Verifies that directed integration rejects a correlated-but-dynamically-uncoupled control. |
| B | Changing-boundary world-tube | Recovers a planted moving subsystem and exposes the continuity-weight failure region. |
| C | Finite-sample recovery | Measures empirical recovery versus sample size and compares internal baselines. |
| D | Exchangeable non-identifiability | Demonstrates a constructed symmetry-driven impossibility case. |
| E | Symbolic moving-clique recovery | Checks the closed-form moving-clique theorem against exact optimization. |
| F | Robust symbolic recovery | Adds external coupling and anisotropic noise and compares several deterministic certificates. |
| G | Block-sparse structural recovery | Demonstrates class-level certification for an implicitly enormous candidate family. |
| H | Localized influence cone | Visualizes finite-speed covariance-error propagation on a fixed block graph. |
| I | Moving-partition influence cone | Extends the influence-cone picture to changing block partitions. |
| J | Moving-partition recovery certificate | Checks the complete moving-partition covariance-to-path pipeline. |

## K–R: class compression and safe screening

| ID | Experiment | Main purpose |
| --- | --- | --- |
| K | Class-compressed robust recovery | Verifies exact factor-symmetry compression. |
| L | Heterogeneous interval-class recovery | Replaces exact class equality by certified factor intervals. |
| M | Covariance-residual-derived class intervals | Derives class intervals from covariance residuals. |
| N | Block-structured residual class recovery | Generates residual intervals from block structure. |
| O | Screened-environment structural recovery | Demonstrates explicit charging for omitted environmental information. |
| P | Independent sample-split confidence accounting | Checks two-stage confidence composition. |
| Q | Gaussian-safe first-split screening | Builds the first complete statistically safe screen. |
| R | Positive-factor screening refinement | Shows how positive factor floors sharpen safe screening radii. |

## S–Z: calibration, relative geometry, and population drift

| ID | Experiment | Main purpose |
| --- | --- | --- |
| S | Gaussian screening calibration | Empirically checks coverage and retained graph fractions. |
| T | Structural-null boundary screening | Tests exact-null boundary refinements and corrects an overly broad structural mask. |
| U | Trajectory-coupled Gaussian calibration | Checks screening when all times share the same trajectories. |
| V | Multi-regime trajectory-coupled calibration | Repeats the coupled analysis across several regimes. |
| W | Covariance-normalized screening | Compares absolute and population-relative covariance concentration. |
| X | Reusable-pilot adaptive screening | Uses a pilot covariance to adapt later screening geometry. |
| Y | Screening under declared population drift | Stress-tests pilot-normalized screening under a declared drift envelope. |
| Z | Estimating drift versus refreshing the reference | Compares calibrated drift estimation with collecting a refreshed reference. |

## AA–AC: dependent Gaussian sampling

| ID | Experiment | Main purpose |
| --- | --- | --- |
| AA | Dependent Gaussian covariance calibration | Quantifies how temporal correlation reduces effective sample size. |
| AB | Mean-centered dependent Gaussian calibration | Verifies the exact normalization required after removing an unknown constant mean. |
| AC | Same-record AR(1) estimation and centered covariance calibration | Estimates temporal dependence and checks joint interval/covariance coverage. |

Full numerical records and commands: [Experiments A–AC](reproducible_results.md).

## Latest experiments AD–AG

| ID | Result | What a reader should notice | Proof / data / code |
| --- | --- | --- | --- |
| AD | Time-varying nuisance projection | As affine drift grows, ordinary centering fails catastrophically while declared nuisance projection remains stable. | [Proof](proposition_44_nuisance_projection.md) · [JSON](nuisance_projection_calibration.json) · [script](../examples/nuisance_projection_calibration.py) |
| AE | Estimated AR(1) + affine nuisance mean | Observable calibration tracks the inaccessible oracle estimator, but the old concentration radius becomes loose at strong correlation. | [Proof](proposition_45_estimated_ar1_nuisance_projection.md) · [JSON](estimated_ar1_nuisance_projection.json) · [script](../examples/estimated_ar1_nuisance_projection.py) |
| AF | Design-specific interval geometry | A rank-only certificate can become vacuous even when the actual declared nuisance geometry still leaves substantial covariance information. | [Proof](proposition_46_design_specific_ar1_envelope.md) · [JSON](design_specific_ar1_envelope.json) · [script](../examples/design_specific_ar1_envelope.py) |
| AG | Weighted-Wishart matrix concentration | Direct matrix concentration cuts the valid covariance radius by roughly 52–65% in the tested regimes and restores several strongly correlated cases to radius below one. | [Proof](proposition_47_weighted_wishart_matrix_chernoff.md) · [JSON](weighted_wishart_matrix_chernoff.json) · [script](../examples/weighted_wishart_matrix_chernoff.py) |

### The four newest figures

[![Experiment AD](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

[![Experiment AE](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

[![Experiment AF](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

[![Experiment AG](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

---

# What the repository currently establishes

Under the stated Gaussian/modeling assumptions, the repository now contains a conditional pipeline from time-varying dynamics to moving-boundary optimization and finite-sample recovery certification. The most developed statistical layer can account for temporal dependence, unknown constant or declared time-varying nuisance means, estimated nonnegative AR(1) dependence, actual nuisance-design geometry, and direct matrix concentration when the projected temporal spectrum is known.

It does **not** establish that every real system has an identifiable observer boundary. It does **not** establish consciousness. It does **not** eliminate assumptions about Gaussianity, separability, stationarity, calibration-channel validity, or predeclared nuisance structure.

## Immediate next proof target

Proposition 47 is sharper but currently assumes the projected temporal eigenvalue profile is known. Proposition 46 handles an estimated AR(1) interval but through norm envelopes. The next composition is therefore clear:

> **Uniform matrix-Chernoff concentration over the calibrated AR(1) interval, using the actual declared nuisance design.**

That would combine Propositions 45, 46, and 47 into one fully observable covariance certificate for the current model class.

---

# Reproduction and audit rule

A result should be considered complete in this repository only when the following pieces exist together:

- a precise mathematical statement;
- assumptions stated close to the claim;
- a proof or derivation;
- a code implementation;
- tests tied to the mathematical claim;
- a reproducible experiment when a numerical scale comparison is useful;
- machine-readable results for committed numerical claims;
- a visible figure when a figure improves understanding;
- a front-page or index link so the result is discoverable.

This is the standard used for the current development going forward.
