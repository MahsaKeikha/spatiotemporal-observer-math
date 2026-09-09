# Research index

This page is the audit-oriented navigation layer for **Spatiotemporal Observer Mathematics**. It keeps physical interpretation, proved mathematics, reproducible numerical evidence, software verification, assumptions, literature sources, and any future consciousness interpretation separate.

A numerical experiment is not a proof. A theorem is not evidence that its assumptions hold in nature. An optimized world-tube is not proof of consciousness. A citation is not an endorsement by the cited author.

## Current research record

| Record | Current state |
| --- | ---: |
| Propositions | **58** |
| Reproducible experiments | **45, A-Z and AA-AS** |
| Scientific result figures | **33** |
| Claim-level tests | **223** |
| Research-software version | **0.47.0** |
| CI matrix | **Python 3.10, 3.11, 3.12** |

The physics pipeline is an explanatory diagram and is not included in the scientific-result figure count.

## Where to start

| Reader goal | Best page |
| --- | --- |
| See the complete figure record with explanations | **[Visual Research Guide](visual_research_guide.md)** |
| See the repository landing page | [README](../README.md) |
| Trace conceptual and mathematical literature | [Bibliography and Citation Map](bibliography.md) |
| Understand physical meaning, units, and model scope | [Physics Guide](physics_guide.md) |
| Learn how to interpret theorem figures | [Figure Reading Guide](figure_reading_guide.md) |
| Follow the program as one coherent story | [Research Overview](research_overview.md) |
| Audit Propositions 1-43 | [Proof record](proofs_and_conjectures.md) |
| Audit Proposition 53A | [Physical relaxation and irregular-grid Markov structure](proposition_53_physical_relaxation_time.md) |
| Audit Proposition 53B | [Irregular-time finite-sample tau calibration](proposition_53b_irregular_tau_evalue.md) |
| Audit Proposition 54 | [Two-scale tau cover](proposition_54_two_scale_irregular_tau_cover.md) |
| Audit Proposition 55 | [Quadratic relaxation calibration](proposition_55_quadratic_relaxation_calibration.md) |
| Audit Proposition 56 | [Exact innovation-whitened target covariance](proposition_56_innovation_whitened_target.md) |
| Audit Proposition 57 | [Robust innovation whitening under calibrated tau](proposition_57_robust_innovation_whitening.md) |
| Audit Proposition 58 | [Covariance uncertainty to world-tube recovery](proposition_58_observer_bridge.md) |
| Inspect Experiment AS | [Machine-readable AS record](observer_bridge_dimension_audit.json) |
| Inspect the current release | [0.47.0 Research Record](release_0_47.md) |
| Inspect assumptions and failure conditions | [Assumption Ledger](assumption_ledger.md) |
| Inspect temporal-calibration APIs | [Temporal Calibration API](api_temporal_calibration.md) |
| Inspect rules for future consciousness interpretation | [Interpretation Protocol](interpretation_protocol.md) |

---

# 1. Citation architecture

The project keeps three citation roles distinct.

1. **Primary conceptual source.** Max Tegmark's 2015 paper *Consciousness as a State of Matter* is the primary conceptual source and starting point for the research question.
2. **Direct mathematical or statistical source.** A theorem, inequality, distributional fact, or method that materially enters a proof or algorithm is cited as a direct source.
3. **Background lineage.** A paper can be important context without being the source of a proposition in this repository.

The complete attribution record is maintained in the [Bibliography and Citation Map](bibliography.md), with machine-readable references in [`references.bib`](../references.bib).

---

# 2. The theorem program

## Layer A. Foundations and first recovery theory, Propositions 1-14

This layer establishes adjacent-state covariance, representation invariance inside declared blocks, transport, moving-path robustness, finite-sample recovery, covariance perturbation control, and identifiability limits.

| Range | Main question | Proof record |
| --- | --- | --- |
| P1-P3 | Which covariance and transport objects define the population problem? | [Proofs](proofs_and_conjectures.md) |
| P4-P6 | When does objective separation imply robust path recovery? | [Proofs](proofs_and_conjectures.md) |
| P7-P12 | How does covariance uncertainty propagate to information factors and finite-sample recovery? | [Proofs](proofs_and_conjectures.md) |
| P13-P14 | Which boundary labels are identifiable, and when is recovery impossible? | [Proofs](proofs_and_conjectures.md) |

## Layer B. Structural compression and moving-partition theory, Propositions 15-31

This layer develops near-competitor structure, symbolic moving-clique recovery, overlap classes, covariance influence cones, interval-certified structural classes, residual bounds, and screened environmental recovery.

| Range | Main role | Proof record |
| --- | --- | --- |
| P15-P20 | Exact competitor structure and symbolic recovery for structured moving systems | [Proofs](proofs_and_conjectures.md) |
| P21-P25 | Covariance influence cones, overlap classes, and localized perturbation | [Proofs](proofs_and_conjectures.md) |
| P26-P31 | Class compression, interval certificates, residuals, and environmental screening | [Proofs](proofs_and_conjectures.md) |

## Layer C. Statistical screening and drift, Propositions 32-40

This layer adds safe sample splitting, Gaussian screening, structural-null refinements, covariance-normalized concentration, reusable pilot geometry, and population-drift calibration.

| Proposition | Main role | Proof record |
| ---: | --- | --- |
| 32 | Independent sample-split confidence composition | [Proofs](proofs_and_conjectures.md) |
| 33 | Gaussian first-split screening safety | [Proofs](proofs_and_conjectures.md) |
| 34 | Positive-factor refinement of Gaussian screening | [Proofs](proofs_and_conjectures.md) |
| 35 | Structural-null screening at score boundaries | [Proofs](proofs_and_conjectures.md) |
| 36 | Trajectory-coupled Gaussian screening | [Proofs](proofs_and_conjectures.md) |
| 37 | Covariance-normalized Gaussian screening | [Proofs](proofs_and_conjectures.md) |
| 38 | Pilot-normalized adaptive screening | [Proofs](proofs_and_conjectures.md) |
| 39 | Drift-robust pilot-normalized screening | [Proofs](proofs_and_conjectures.md) |
| 40 | Statistically calibrated population drift | [Proofs](proofs_and_conjectures.md) |

## Layer D. Dependent measurements and temporal calibration, Propositions 41-52

| Proposition | Mathematical role | Physical role | Direct proof |
| ---: | --- | --- | --- |
| 41 | Dependent Gaussian covariance concentration | Corrects the information budget when samples have memory | [Proof record](proofs_and_conjectures.md) |
| 42 | Unknown constant-mean extension | Removes baseline uncertainty under temporal dependence | [Proof record](proofs_and_conjectures.md) |
| 43 | Finite-sample AR(1) calibration | Learns discrete persistence instead of assuming it | [Proof record](proofs_and_conjectures.md) |
| 44 | Fixed nuisance-subspace projection | Removes declared deterministic temporal modes | [P44](proposition_44_nuisance_projection.md) |
| 45 | Estimated AR(1) plus nuisance projection | Combines temporal calibration and drift removal | [P45](proposition_45_estimated_ar1_nuisance_projection.md) |
| 46 | Design-specific continuum envelope | Uses actual nuisance geometry instead of rank-only pessimism | [P46](proposition_46_design_specific_ar1_envelope.md) |
| 47 | Direct weighted-Wishart matrix concentration | Certifies covariance with the full temporal spectrum | [P47](proposition_47_weighted_wishart_matrix_chernoff.md) |
| 48 | Uniform matrix bound over AR(1) uncertainty | Keeps direct matrix concentration valid when persistence is uncertain | [P48](proposition_48_uniform_matrix_chernoff_ar1.md) |
| 49 | Compact temporal-family matrix concentration | Abstracts the theorem to a covered temporal covariance family | [P49](proposition_49_compact_temporal_family.md) |
| 50 | Calibrated two-parameter temporal family | Learns persistence and white-noise fraction from calibration data | [P50](proposition_50_calibrated_temporal_family.md) |
| 51 | Continuum e-value confidence set | Inverts a finite-sample likelihood-ratio e-value over temporal models | [P51](proposition_51_evalue_temporal_confidence_set.md) |
| 52 | Certified outer cover and target composition | Carries every still-compatible temporal model into an independent target theorem | [P52](proposition_52_certified_evalue_outer_cover.md) |

## Layer E. Physical time and irregular-grid inference, Proposition 53

| Proposition | Mathematical role | Physical role | Proof |
| ---: | --- | --- | --- |
| 53A | Sampling-consistent exponential covariance and exact irregular-grid Markov factorization | Separates physical relaxation time from sampling-dependent correlation | [P53A](proposition_53_physical_relaxation_time.md) |
| 53B | Finite-sample continuum e-value inference for \(\tau\) | Calibrates physical relaxation time directly on irregular timestamps | [P53B](proposition_53b_irregular_tau_evalue.md) |

## Layer F. Two-scale physical-time uncertainty propagation, Proposition 54

Proposition 54 separates calibration-cell resolution from the target temporal-cover resolution so a fine finite-sample physical-time certificate does not force a prohibitively large target cover.

[Proof](proposition_54_two_scale_irregular_tau_cover.md) | [Figure](two_scale_irregular_tau_cover.svg)

## Layer G. Local likelihood curvature, Proposition 55

Proposition 55 uses exact observed-data log-evalue slope plus a rigorous cell-local curvature bound to tighten the deterministic outer enclosure of the same finite-sample continuum confidence set without spending another probability budget.

[Proof](proposition_55_quadratic_relaxation_calibration.md) | [Experiment AP](quadratic_relaxation_calibration.json) | [Figure](quadratic_relaxation_calibration.svg)

## Layer H. Exact innovation-whitened target inference, Proposition 56

For

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma),
\]

with exact \(\tau\), Proposition 53 supplies a whitener \(W_\tau\). Applying it to both target data and nuisance design yields an ordinary Gaussian regression in innovation coordinates. After rank-\(q\) nuisance removal,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

On Experiment AQ, the scalar known-\(\tau\) target radius is approximately

\[
\boxed{0.43644<1},
\]

compared with the previous raw-time known-\(\tau\) oracle `2.16725`.

[Proof](proposition_56_innovation_whitened_target.md) | [Data](innovation_whitened_target.json) | [Figure](innovation_whitened_target.svg)

## Layer I. Robust innovation whitening under calibrated physical time, Proposition 57

Proposition 57 removes the exact-target-\(\tau\) assumption on the controlled scalar benchmark.

Starting from the independent Proposition 55 interval

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s},
\]

choose one working whitener \(W_0\) and define

\[
C_\tau=W_0R_\tau W_0^\mathsf T.
\]

A deterministic cover of this transformed family feeds into Proposition 49. Experiment AR gives

\[
\boxed{
\varepsilon_{57}=0.8677117535<1
}
\]

at target confidence `0.975`; together with the independent calibration confidence `0.975`, the combined lower bound is `0.950625`.

[Proof](proposition_57_robust_innovation_whitening.md) | [Data](robust_innovation_whitened_target.json) | [Figure](robust_innovation_whitened_target.svg)

## Layer J. Relative covariance uncertainty to world-tube recovery, Proposition 58

Proposition 58 reconnects covariance certification to the original moving-boundary problem.

For future candidate \(S\), the observer block

\[
B_{t,S}=(X_t,X_{t+1}^{S})
\]

has dimension

\[
d_{\mathrm{obs}}=n+s
\]

and supports the local observer factors plus every incoming transport edge to that target candidate. The simultaneous covariance count is therefore

\[
B_{\mathrm{obs}}=TC.
\]

Given candidate-local relative covariance radii \(\delta_{t,S}<1\), the theorem propagates them through integration, environmental independence, canonical persistence, local observer scores, transport scores, and the complete world-tube action. A positive returned recovery slack certifies the population path on the same simultaneous covariance event. No additional probability budget is spent by this deterministic bridge.

[Proof](proposition_58_observer_bridge.md) | [Experiment AS data](observer_bridge_dimension_audit.json) | [Figure](observer_bridge_dimension_audit.svg)

---

# 3. Recent experiment ladder

The recent experiments form one causal sequence. Each experiment exposes the next limitation rather than simply adding another benchmark.

| Experiment | Proposition | Question | Main recorded result | Visual |
| --- | ---: | --- | --- | --- |
| AM | 53A | Does one physical timescale survive changes of sampling rate? | one \(\tau\) maps to sampling-dependent one-step correlations | [Figure](physical_relaxation_sampling.svg) |
| AN | 53B | Can \(\tau\) be calibrated from irregular finite data? | finite-sample continuum confidence set; target radius `3.15549` | [Figure](irregular_relaxation_evalue_calibration.svg) |
| AO | 54 | Can calibration and target cover resolution be separated? | target radius `3.15549 -> 2.57207` | [Figure](two_scale_irregular_tau_cover.svg) |
| AP | 55 | Can likelihood curvature tighten calibration? | 160-cell hull width `0.1646875 s`; target radius `2.41488`; raw oracle `2.16725 > 1` | [Figure](quadratic_relaxation_calibration.svg) |
| AQ | 56 | Can exact innovations remove the raw-time temporal penalty? | scalar raw oracle `2.16725 -> 0.43644` | [Figure](innovation_whitened_target.svg) |
| AR | 57 | Does the innovation advantage survive finite-sample \(\tau\) uncertainty? | scalar robust radius `0.86771 < 1` | [Figure](robust_innovation_whitened_target.svg) |
| AS | 58 | Does scalar covariance success imply observer-scale world-tube certification? | observer-scale exact-tau radius `1.85736 > 1`; current structural bottleneck exposed | [Figure](observer_bridge_dimension_audit.svg) |

For the complete 33-figure atlas, use the [Visual Research Guide](visual_research_guide.md).

---

# 4. Proposition 58 observer-scale audit

Experiment AS uses the original controlled moving-module problem:

\[
n=7,
\quad
s=3,
\quad
T=5,
\quad
C=35.
\]

Thus

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

The planted and recovered population path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

with population action margin `0.1264216185`.

At 118 residual innovation degrees and exact \(\tau\), the current unit-weight matrix theorem gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

It first enters \(\varepsilon<1\) at 346 residual degrees:

\[
\varepsilon_{345}=1.0007464318,
\qquad
\varepsilon_{346}=0.9991303523.
\]

The present generic factor-perturbation chain requires a much smaller uniform covariance radius, approximately `1.11e-4`, to certify this population path. The corresponding huge residual-degree calculation is recorded explicitly as a **proof-conservatism diagnostic, not a physical sample requirement**.

This is the current reason to pursue factor-specific blocks, screen-first reduction, candidate-local radii, and direct action-margin concentration.

---

# 5. Proof versus experiment versus diagnostic

| Record type | What it means |
| --- | --- |
| Proposition | Proved mathematical statement under declared assumptions |
| Controlled experiment | Reproducible numerical construction or theorem-scale illustration |
| Diagnostic | Calculation designed to reveal a bottleneck, failure regime, or conservatism gap |
| Interpretation hypothesis | Scientific connection requiring additional bridge assumptions and empirical tests |

Examples:

- the exact Proposition 56 Wishart reduction is a theorem;
- AQ's repeated seeded trials are visibility checks;
- AS's `21,165,400,697` residual-degree value is a conservatism diagnostic;
- no observer score or covariance radius is claimed to be a measure of consciousness.

---

# 6. Reproducibility map for P55-P58

| Result | Proof | JSON | Experiment | Tests | Figure |
| --- | --- | --- | --- | --- | --- |
| P55 / AP | [proof](proposition_55_quadratic_relaxation_calibration.md) | [data](quadratic_relaxation_calibration.json) | [script](../examples/quadratic_relaxation_calibration.py) | [tests](../tests/test_relaxation_curvature.py) | [figure](quadratic_relaxation_calibration.svg) |
| P56 / AQ | [proof](proposition_56_innovation_whitened_target.md) | [data](innovation_whitened_target.json) | [script](../examples/innovation_whitened_target.py) | [tests](../tests/test_innovation_whitening.py) | [figure](innovation_whitened_target.svg) |
| P57 / AR | [proof](proposition_57_robust_innovation_whitening.md) | [data](robust_innovation_whitened_target.json) | [script](../examples/robust_innovation_whitened_target.py) | [tests](../tests/test_robust_innovation_whitening.py) | [figure](robust_innovation_whitened_target.svg) |
| P58 / AS | [proof](proposition_58_observer_bridge.md) | [data](observer_bridge_dimension_audit.json) | [script](../examples/observer_bridge_dimension_audit.py) | [tests](../tests/test_observer_bridge.py) | [figure](observer_bridge_dimension_audit.svg) |

---

# 7. Assumption and interpretation audit

The mathematics is conditional on explicitly declared measurement models and candidate geometry. The exact assumptions differ by proposition.

Use the [Assumption Ledger](assumption_ledger.md) for the proposition-specific audit.

Typical assumptions in the recent physical-time chain include:

- strictly increasing timestamps;
- a declared stationary one-timescale exponential relaxation family;
- Gaussian innovations;
- separable space-time covariance for the target covariance theorems;
- calibration information independent of the target record when confidence products are used;
- fixed predeclared nuisance design;
- candidate blocks declared before simultaneous concentration is evaluated.

Relevant falsification checks include residual temporal correlation, evidence for several timescales, oscillatory dependence, heavy tails, nonseparable covariance, calibration-target mismatch, and sensitivity to nuisance or candidate design.

The word **observer** does not by itself cross the interpretation boundary. See the [Interpretation Protocol](interpretation_protocol.md).

---

# 8. Current frontier

Proposition 58 changes the immediate theorem priority.

The next rigorous question is:

> **Can the covariance geometry actually needed by near-competitive observer factors be certified directly enough that the world-tube action margin, rather than a chain of global worst-case intermediate bounds, becomes the main object of concentration?**

The concrete directions are:

1. factor-specific covariance blocks;
2. screen-first simultaneity reduction;
3. candidate-local covariance radii;
4. direct score-margin or action-difference concentration;
5. richer temporal models after the observer-scale structural bottleneck is understood.

This frontier follows from the actual negative diagnostic in Experiment AS. It is not chosen merely to extend the proposition count.

---

# 9. Release and citation audit

Current release: [0.47.0 Research Record](release_0_47.md).

Citation metadata: [`CITATION.cff`](../CITATION.cff).

Machine-readable bibliography: [`references.bib`](../references.bib).

External-source roles: [Bibliography and Citation Map](bibliography.md).

A numerical experiment is not a proof. A theorem is not evidence that its assumptions hold in nature. A recovered moving subsystem is not, by that fact alone, a conscious observer.
