# Research index

This page is the audit-oriented navigation layer for **Spatiotemporal Observer Mathematics**. It connects the physical question, mathematical statements, reproducible experiments, figures, assumptions, literature, and software verification in one place.

## Current research record

| Record | Current state |
| --- | ---: |
| Propositions | **58** |
| Reproducible experiments | **45, A-Z and AA-AS** |
| Scientific result figures | **33** |
| Claim-level tests | **223** |
| Research-software version | **0.47.1** |
| CI matrix | **Python 3.10, 3.11, 3.12** |

The explanatory physics pipeline is not included in the scientific-result figure count.

## Primary navigation

| Reader goal | Best page |
| --- | --- |
| Understand the project from the physics outward | **[Physics Guide](physics_guide.md)** |
| See equations and source provenance together | **[Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md)** |
| Follow the research as one scientific argument | **[Research Overview](research_overview.md)** |
| Browse every scientific figure | **[Visual Research Guide](visual_research_guide.md)** |
| Trace external literature | [Bibliography and Citation Map](bibliography.md) |
| Inspect assumptions and failure conditions | [Assumption Ledger](assumption_ledger.md) |
| Review interpretation boundaries | [Interpretation Protocol](interpretation_protocol.md) |
| Inspect the current patch record | [Release 0.47.1](release_0_47_1.md) |
| Return to the repository landing page | [README](../README.md) |

---

# 1. Conceptual and citation architecture

The primary conceptual starting point is Max Tegmark's 2015 paper *Consciousness as a State of Matter*, which frames the observer-factorization question that motivates this program.

The repository distinguishes three kinds of source relationship:

1. **Conceptual lineage:** the source motivates the scientific question or interpretation of a mathematical object.
2. **Mathematical foundation:** the source supplies an identity, theorem, inequality, distributional result, or algorithmic principle used directly in a derivation.
3. **Repository development:** the definition, proposition, proof, or computational construction is developed in this research program.

The full source-role map is maintained in the [Bibliography and Citation Map](bibliography.md), with machine-readable entries in [`references.bib`](../references.bib).

---

# 2. The theorem program

## Layer A. Foundations, transport, recovery, and identifiability: P1-P14

| Range | Main role | Proof record |
| --- | --- | --- |
| P1-P3 | adjacent-state covariance, observer factors, transport geometry | [Proofs](proofs_and_conjectures.md) |
| P4-P6 | world-tube optimization, runner-up margin, perturbation stability | [Proofs](proofs_and_conjectures.md) |
| P7-P12 | covariance perturbation, finite-sample recovery, sample complexity | [Proofs](proofs_and_conjectures.md) |
| P13-P14 | symmetry-aware identifiability and observational impossibility | [Proofs](proofs_and_conjectures.md) |

## Layer B. Structural compression and moving partitions: P15-P31

| Range | Main role | Proof record |
| --- | --- | --- |
| P15-P20 | near-competitor structure and symbolic moving-clique recovery | [Proofs](proofs_and_conjectures.md) |
| P21-P25 | covariance influence cones, overlap classes, localized perturbation | [Proofs](proofs_and_conjectures.md) |
| P26-P31 | class compression, interval certificates, residual bounds, environmental screening | [Proofs](proofs_and_conjectures.md) |

## Layer C. Statistical screening and drift: P32-P40

| Proposition | Main role | Proof record |
| ---: | --- | --- |
| 32 | independent sample-split confidence composition | [Proofs](proofs_and_conjectures.md) |
| 33 | Gaussian first-split screening | [Proofs](proofs_and_conjectures.md) |
| 34 | positive-factor screening refinement | [Proofs](proofs_and_conjectures.md) |
| 35 | structural-null score refinement | [Proofs](proofs_and_conjectures.md) |
| 36 | trajectory-coupled screening | [Proofs](proofs_and_conjectures.md) |
| 37 | covariance-normalized Gaussian screening | [Proofs](proofs_and_conjectures.md) |
| 38 | pilot-normalized adaptive screening | [Proofs](proofs_and_conjectures.md) |
| 39 | drift-robust screening | [Proofs](proofs_and_conjectures.md) |
| 40 | calibrated population drift | [Proofs](proofs_and_conjectures.md) |

## Layer D. Dependent measurements and temporal calibration: P41-P52

| Proposition | Mathematical role | Physical role | Proof |
| ---: | --- | --- | --- |
| 41 | dependent Gaussian covariance concentration | accounts for temporal memory | [Proofs](proofs_and_conjectures.md) |
| 42 | unknown constant-mean extension | removes baseline uncertainty | [Proofs](proofs_and_conjectures.md) |
| 43 | finite-sample AR(1) calibration | estimates discrete persistence | [Proofs](proofs_and_conjectures.md) |
| 44 | fixed nuisance-subspace projection | removes declared temporal modes | [P44](proposition_44_nuisance_projection.md) |
| 45 | estimated AR(1) with nuisance projection | combines temporal calibration and nuisance removal | [P45](proposition_45_estimated_ar1_nuisance_projection.md) |
| 46 | design-specific continuum envelope | uses the actual nuisance geometry | [P46](proposition_46_design_specific_ar1_envelope.md) |
| 47 | weighted-Wishart matrix concentration | uses the full temporal spectrum | [P47](proposition_47_weighted_wishart_matrix_chernoff.md) |
| 48 | uniform AR(1) matrix concentration | retains validity under correlation uncertainty | [P48](proposition_48_uniform_matrix_chernoff_ar1.md) |
| 49 | compact temporal-family concentration | covers a general declared temporal family | [P49](proposition_49_compact_temporal_family.md) |
| 50 | calibrated two-parameter temporal family | learns persistence and white-noise fraction | [P50](proposition_50_calibrated_temporal_family.md) |
| 51 | continuum e-value confidence set | finite-sample temporal-model inference | [P51](proposition_51_evalue_temporal_confidence_set.md) |
| 52 | certified outer cover and target composition | transfers temporal uncertainty into target inference | [P52](proposition_52_certified_evalue_outer_cover.md) |

## Layer E. Physical relaxation time: P53A-P53B

| Proposition | Main role | Proof |
| ---: | --- | --- |
| 53A | sampling-consistent exponential covariance and exact irregular-grid Markov factorization | [P53A](proposition_53_physical_relaxation_time.md) |
| 53B | finite-sample continuum e-value inference for physical relaxation time \(\tau\) | [P53B](proposition_53b_irregular_tau_evalue.md) |

## Layer F. Two-scale relaxation cover: P54

Proposition 54 separates calibration-cell resolution from target temporal-cover resolution.

[Proof](proposition_54_two_scale_irregular_tau_cover.md) | [Figure](two_scale_irregular_tau_cover.svg)

## Layer G. Local likelihood curvature: P55

Proposition 55 uses exact local log-evalue slope and a certified curvature bound to sharpen the physical-time confidence hull.

[Proof](proposition_55_quadratic_relaxation_calibration.md) | [Experiment AP](quadratic_relaxation_calibration.json) | [Figure](quadratic_relaxation_calibration.svg)

## Layer H. Exact innovation-whitened target inference: P56

For exact \(\tau\), the physical-time whitener transforms the target model into innovation coordinates. After a rank-\(q\) nuisance projection,

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q).
}
\]

Experiment AQ reduces the scalar known-\(\tau\) target radius from approximately `2.16725` to `0.43647`.

[Proof](proposition_56_innovation_whitened_target.md) | [Data](innovation_whitened_target.json) | [Figure](innovation_whitened_target.svg)

## Layer I. Robust innovation whitening under calibrated physical time: P57

Starting from the independently calibrated interval

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s},
\]

Proposition 57 uses one working whitener \(W_0\) and certifies the transformed temporal family

\[
C_\tau=W_0R_\tau W_0^{\mathsf T}.
\]

The 0.47.1 tightening uses a trace-specific deterministic derivative bound for the projected normalization while retaining the original operator/eigenvalue cover. Experiment AR gives

\[
\boxed{
\varepsilon_{57}=0.7195879984<1
}
\]

at combined calibration-target confidence lower bound `0.950625`.

[Proof](proposition_57_robust_innovation_whitening.md) | [Data](robust_innovation_whitened_target.json) | [Figure](robust_innovation_whitened_target.svg) | [0.47.1 correction record](release_0_47_1.md)

## Layer J. Covariance uncertainty to world-tube recovery: P58

For future candidate \(S\), define

\[
B_{t,S}=(X_t,X_{t+1}^{S}).
\]

The observer block has dimension

\[
d_{\mathrm{obs}}=n+s
\]

and contains the covariance geometry used by the local observer factors and incoming transport terms. Proposition 58 propagates simultaneous candidate-local relative covariance radii through the complete world-tube objective without introducing an additional probability event.

[Proof](proposition_58_observer_bridge.md) | [Experiment AS](observer_bridge_dimension_audit.json) | [Figure](observer_bridge_dimension_audit.svg)

---

# 3. Recent experiment sequence

| Experiment | Proposition | Scientific question | Main recorded result | Visual |
| --- | ---: | --- | --- | --- |
| AM | 53A | Does one physical timescale survive changes of sampling rate? | one \(\tau\) maps to sampling-dependent one-step correlations | [Figure](physical_relaxation_sampling.svg) |
| AN | 53B | Can \(\tau\) be calibrated from irregular finite data? | continuum confidence set; target radius `3.15549` | [Figure](irregular_relaxation_evalue_calibration.svg) |
| AO | 54 | Can calibration and target resolutions be separated? | `3.15549 -> 2.57207` | [Figure](two_scale_irregular_tau_cover.svg) |
| AP | 55 | Can likelihood curvature tighten calibration? | hull width `0.1646875 s`; target radius `2.41488` | [Figure](quadratic_relaxation_calibration.svg) |
| AQ | 56 | Can exact innovations remove the raw-time temporal penalty? | `2.16725 -> 0.43647` | [Figure](innovation_whitened_target.svg) |
| AR | 57 | Does the innovation advantage survive finite-sample \(\tau\) uncertainty? | corrected robust radius `0.71959 < 1` | [Figure](robust_innovation_whitened_target.svg) |
| AS | 58 | Does scalar covariance success imply observer-scale certification? | observer-scale exact-\(\tau\) radius `1.85736 > 1` at current N | [Figure](observer_bridge_dimension_audit.svg) |

For the complete 33-figure record, use the [Visual Research Guide](visual_research_guide.md).

---

# 4. Current observer-scale diagnostic

On the controlled moving-module benchmark,

\[
n=7,
\qquad
s=3,
\qquad
T=5,
\qquad
C={7\choose3}=35.
\]

Therefore

\[
\boxed{
d_{\mathrm{obs}}=10,
\qquad
B_{\mathrm{obs}}=175.
}
\]

The planted and recovered population path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

with population action margin `0.1264216185`.

At 118 residual innovation degrees and exact \(\tau\), the current matrix theorem gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

The current theorem first enters \(\varepsilon<1\) at 346 residual innovation degrees. This diagnostic identifies the present structural frontier: factor-specific covariance geometry, reduced simultaneity, candidate-local uncertainty, and more direct score-margin concentration.

---

# 5. Proof, experiment, and software verification

| Record type | Meaning |
| --- | --- |
| **Proposition** | mathematical statement proved under declared assumptions |
| **Experiment** | reproducible numerical study under specified parameters |
| **Figure** | visual representation of a theorem, diagnostic, or numerical study |
| **Claim-level test** | software check that implementation and committed artifacts agree with stated invariants |
| **Physical interpretation** | model-dependent reading that requires the declared observation assumptions |

Software tests verify code and artifact consistency. Physical validity is assessed through the model assumptions and falsification diagnostics in the [Physics Guide](physics_guide.md) and [Assumption Ledger](assumption_ledger.md).

---

# 6. Reproducibility map for the current frontier

| Result | Proof | Data | Experiment | Tests | Figure |
| --- | --- | --- | --- | --- | --- |
| P55 / AP | [proof](proposition_55_quadratic_relaxation_calibration.md) | [JSON](quadratic_relaxation_calibration.json) | [script](../examples/quadratic_relaxation_calibration.py) | [tests](../tests/test_relaxation_curvature.py) | [figure](quadratic_relaxation_calibration.svg) |
| P56 / AQ | [proof](proposition_56_innovation_whitened_target.md) | [JSON](innovation_whitened_target.json) | [script](../examples/innovation_whitened_target.py) | [tests](../tests/test_innovation_whitening.py) | [figure](innovation_whitened_target.svg) |
| P57 / AR | [proof](proposition_57_robust_innovation_whitening.md) | [JSON](robust_innovation_whitened_target.json) | [script](../examples/robust_innovation_whitened_target.py) | [tests](../tests/test_robust_innovation_whitening.py) | [figure](robust_innovation_whitened_target.svg) |
| P58 / AS | [proof](proposition_58_observer_bridge.md) | [JSON](observer_bridge_dimension_audit.json) | [script](../examples/observer_bridge_dimension_audit.py) | [tests](../tests/test_observer_bridge.py) | [figure](observer_bridge_dimension_audit.svg) |

---

# 7. Current research frontier

The immediate mathematical frontier is no longer temporal calibration alone. Proposition 58 shows that the dominant difficulty is observer-scale dimension and structural propagation of covariance uncertainty.

The next directions are:

1. factor-specific covariance blocks;
2. safe screen-first reduction of the simultaneous family;
3. candidate-local uncertainty radii;
4. direct score-margin or action-margin concentration;
5. richer physical temporal models once the observer-scale structural bottleneck is better understood.

The guiding question remains:

> **When does the dynamics itself justify a moving subsystem boundary, and when does the available evidence remain insufficient to identify one?**
