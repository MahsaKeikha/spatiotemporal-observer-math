# Figure reading guide

This page explains how to read the repository's scientific figures physically, mathematically, and statistically. It is a companion to the [Physics Guide](physics_guide.md) and the complete [Visual Research Guide](visual_research_guide.md).

A recurring source of confusion is that many plots show **uncertainty about a mathematical quantity**, not a directly measured physical observable. A covariance radius, confidence region, theorem bound, or recovery slack should not be read as an energy, force, consciousness level, or physical phase unless an additional derivation establishes that meaning.

---

# 1. Four kinds of figures

## Structural figures

These visualize the moving-boundary problem itself.

Examples:

- candidate scores over time;
- recovered world-tube paths;
- path-recovery phase diagrams.

Physical question:

> Where is the dynamically coherent subsystem, and can its boundary move while remaining identifiable?

## Calibration figures

These visualize which temporal-memory or physical-time models remain compatible with calibration data.

Examples:

- AR(1) intervals;
- two-parameter temporal regions;
- e-value confidence sets;
- physical relaxation-time intervals.

Physical question:

> What temporal law is compatible with the measured record, and how uncertain is that law?

## Certification figures

These compare finite-sample theorem radii with empirical error, older bounds, or exact-oracle diagnostics.

Physical question:

> Is the fluctuation covariance known accurately enough that downstream information and boundary scores can be trusted under the stated model?

The theorem radius is a guarantee under assumptions. It is not a physical state variable.

## Bottleneck figures

These are deliberately designed to show where the current theorem fails to be selective or becomes too conservative.

Examples include the known-tau oracle panel in Experiment AP and the observer-scale audit in Experiment AS.

A negative diagnostic is not a failed experiment. It identifies which part of the proof or measurement design must improve next.

---

# 2. Moving-boundary figures

## World-tube baseline

File: [`worldtube_baseline.png`](worldtube_baseline.png)

[![World-tube baseline](worldtube_baseline.png)](reproducible_results.md)

A controlled subsystem changes which coordinates represent it as time advances.

The planted path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

Physical reading: imagine a coherent structure moving across a sensor array. The physical pattern persists while the sensors representing it change.

What to look for:

- whether the recovered path follows the planted structure;
- how close the strongest competitors are;
- whether continuity regularization supports plausible motion rather than forcing it.

What it does not show: consciousness. It shows recovery of a planted dynamical boundary in a controlled model.

## World-tube phase diagram

File: [`worldtube_phase_diagram.png`](worldtube_phase_diagram.png)

[![World-tube phase diagram](worldtube_phase_diagram.png)](reproducible_results.md)

The figure shows regions where path recovery succeeds or fails as model and regularization parameters change.

Physical lesson: continuity can stabilize a moving physical structure, but excessive continuity pressure can overwhelm measured dynamical evidence.

---

# 3. Finite-sample, screening, and drift figures

The early and middle figures progressively ask whether the population moving-boundary result survives finite data, large candidate spaces, screening, reuse of pilot information, and changing populations.

Use the [Visual Research Guide](visual_research_guide.md#5-complete-scientific-figure-atlas) for the complete figure-by-figure atlas.

The central interpretation rule is:

> A smaller statistical radius means a tighter theorem under the declared model. It does not mean the physical system itself became more organized.

---

# 4. Proposition 44 / Experiment AD: nuisance projection

Figure: [`nuisance_projection_calibration.svg`](nuisance_projection_calibration.svg)

[![Nuisance projection](nuisance_projection_calibration.svg)](proposition_44_nuisance_projection.md)

Mathematical question: can a declared time-varying nuisance mean be removed without biasing covariance recovery?

Physical picture: a sensor record contains a large deterministic baseline or linear drift on top of stochastic fluctuations.

The figure shows that ordinary centering can leave severe drift contamination, while projection against the declared nuisance design keeps the stochastic covariance estimate stable.

What it does not mean: every slow trend is nuisance. If a removed mode is genuine system dynamics, projecting it away removes real physics.

---

# 5. Proposition 45 / Experiment AE: estimated temporal memory plus nuisance projection

Figure: [`estimated_ar1_nuisance_projection.svg`](estimated_ar1_nuisance_projection.svg)

[![Estimated AR1 nuisance projection](estimated_ar1_nuisance_projection.svg)](proposition_45_estimated_ar1_nuisance_projection.md)

Larger `phi` means longer modeled persistence and therefore more redundancy between neighboring observations.

A larger covariance theorem radius at strong correlation does not mean the physical system is less organized. It means a finite record contains less independent information for covariance estimation under that model.

---

# 6. Proposition 46 / Experiment AF: design-specific nuisance geometry

Figure: [`design_specific_ar1_envelope.svg`](design_specific_ar1_envelope.svg)

[![Design-specific AR1 envelope](design_specific_ar1_envelope.svg)](proposition_46_design_specific_ar1_envelope.md)

Two nuisance designs with the same rank can interact very differently with the temporal covariance modes of the measured process.

The figure shows why nuisance **geometry**, not only nuisance rank, matters for the information remaining after projection.

---

# 7. Proposition 47 / Experiment AG: direct matrix concentration

Figure: [`weighted_wishart_matrix_chernoff.svg`](weighted_wishart_matrix_chernoff.svg)

[![Weighted Wishart matrix Chernoff](weighted_wishart_matrix_chernoff.svg)](proposition_47_weighted_wishart_matrix_chernoff.md)

The plotted radius is a worst-case relative covariance uncertainty under the theorem.

Why the line at one matters:

\[
\epsilon<1
\]

places covariance estimation in the perturbative regime required by later inverse-covariance and information calculations.

It is not a physical critical point.

---

# 8. Proposition 48 / Experiment AH: uncertain AR(1)

Figure: [`uniform_matrix_chernoff_ar1.svg`](uniform_matrix_chernoff_ar1.svg)

[![Uniform matrix Chernoff AR1](uniform_matrix_chernoff_ar1.svg)](proposition_48_uniform_matrix_chernoff_ar1.md)

The theorem remains valid over a calibrated interval of temporal persistence rather than plugging in one guessed coefficient.

Physical lesson: a covariance claim should survive all temporal models the calibration experiment has not ruled out.

---

# 9. Proposition 49 / Experiment AI: compact temporal family

Figure: [`compact_temporal_family.svg`](compact_temporal_family.svg)

[![Compact temporal family](compact_temporal_family.svg)](proposition_49_compact_temporal_family.md)

A finite mathematical cover represents a continuum family of temporal covariance matrices.

When cover refinement lowers the radius, only the mathematical approximation of uncertainty has improved. The underlying physical process has not changed because the grid was refined.

---

# 10. Proposition 50 / Experiment AJ: learned temporal family

Figure: [`calibrated_temporal_family.svg`](calibrated_temporal_family.svg)

[![Calibrated temporal family](calibrated_temporal_family.svg)](proposition_50_calibrated_temporal_family.md)

More independent calibration information narrows uncertainty about temporal-memory parameters.

The target physical system is held fixed. A falling covariance radius reflects better parameter knowledge, not increasing physical stability.

---

# 11. Proposition 51 / Experiment AK: e-value temporal confidence set

Figure: [`evalue_temporal_confidence_set.svg`](evalue_temporal_confidence_set.svg)

[![E-value temporal confidence set](evalue_temporal_confidence_set.svg)](proposition_51_evalue_temporal_confidence_set.md)

Each point represents a temporal-memory model. The accepted region contains parameter values not rejected by the finite-sample e-value construction at the declared confidence level.

The region is not:

- a posterior probability density;
- an energy landscape;
- a consciousness landscape;
- a causal map.

The plotted grid visualizes a continuum e-value function. It is not the source of the probability guarantee.

---

# 12. Proposition 52 / Experiment AL: certified e-value outer cover

Figure: [`certified_evalue_outer_cover.svg`](certified_evalue_outer_cover.svg)

[![Certified e-value outer cover](certified_evalue_outer_cover.svg)](proposition_52_certified_evalue_outer_cover.md)

The certified outer cover is intentionally wider than a dense plotted accepted region because it must safely contain the complete between-grid continuum confidence set.

A retained cell is not declared true. It is simply not safe to exclude.

A displayed trial error is a numerical visibility check. The theorem radius comes from the proof.

---

# 13. Proposition 53 / Experiment AM: physical relaxation time

Figure: [`physical_relaxation_sampling.svg`](physical_relaxation_sampling.svg)

[![Physical relaxation sampling](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

The declared model is

\[
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\qquad
\phi_{\Delta t}=e^{-\Delta t/\tau}.
\]

### Panel A

The one-step correlation changes with sampling rate. This is expected because adjacent samples are separated by different physical times.

### Panel B

Every sampling rate maps back to the same controlled \(\tau=0.8\) s.

### Panel C

The analytic continuum-cover radius shrinks as the deterministic \(\tau\)-grid is refined. The dense numerical curve is a scale check, not the proof.

### Panel D

Irregular timestamps use actual elapsed physical time. No fictitious integer lag is inserted for missing samples.

What it does not establish: that every physical system has one exponential timescale.

---

# 14. Proposition 53: exact irregular-grid Markov structure

Figure: [`physical_relaxation_markov.svg`](physical_relaxation_markov.svg)

[![Physical relaxation Markov structure](physical_relaxation_markov.svg)](proposition_53_physical_relaxation_time.md)

This figure visualizes the exact local representation behind the dense exponential covariance:

\[
X_{i+1}
=
\alpha_iX_i+
\sqrt{1-\alpha_i^2}\,\varepsilon_i,
\qquad
\alpha_i=e^{-(t_{i+1}-t_i)/\tau}.
\]

The key visual facts are:

- local transition coefficients depend on actual elapsed gaps;
- the precision matrix is tridiagonal;
- the innovation whitener is lower bidiagonal;
- whitening and determinant identities hold at floating-point precision in the numerical verification.

The sparsity is conditional on the one-timescale exponential Gaussian model. It is not asserted for arbitrary temporal physics.

---

# 15. Proposition 53B / Experiment AN: finite-sample irregular-time tau calibration

Figure: [`irregular_relaxation_evalue_calibration.svg`](irregular_relaxation_evalue_calibration.svg)

[![Irregular relaxation e-value calibration](irregular_relaxation_evalue_calibration.svg)](proposition_53b_irregular_tau_evalue.md)

The figure separates two objects:

- a dense numerical view of which \(\tau\) values are compatible with the observed likelihood-ratio e-value;
- a certified deterministic outer enclosure of the complete continuum confidence set.

The outer enclosure can be wider without any coverage failure. The width difference is a tightness gap.

---

# 16. Proposition 54 / Experiment AO: two-scale tau cover

Figure: [`two_scale_irregular_tau_cover.svg`](two_scale_irregular_tau_cover.svg)

[![Two-scale irregular tau cover](two_scale_irregular_tau_cover.svg)](proposition_54_two_scale_irregular_tau_cover.md)

The figure separates fine calibration resolution from the target temporal-cover resolution.

A finer calibration grid improves deterministic enclosure of the physical-time confidence set. It does not create more physical data and does not spend another confidence budget.

---

# 17. Proposition 55 / Experiment AP: quadratic physical-time calibration

Figure: [`quadratic_relaxation_calibration.svg`](quadratic_relaxation_calibration.svg)

[![Quadratic relaxation calibration](quadratic_relaxation_calibration.svg)](proposition_55_quadratic_relaxation_calibration.md)

### Panel A

First-order and quadratic certified interval widths are compared at the same calibration-cell counts. The tighter quadratic curve means better deterministic use of the same finite-sample likelihood information.

### Panel B

The declared interval, first-order enclosure, quadratic enclosure, and controlled true \(\tau\) are shown in seconds.

### Panel C

Downstream target covariance radii are compared with the mathematical threshold one.

### Panel D

The most important panel is the negative oracle diagnostic: even exact knowledge of \(\tau\) leaves the old raw-time target theorem around `2.16725 > 1`.

That result redirects the next theorem from calibration to target representation.

---

# 18. Proposition 56 / Experiment AQ: exact innovation-whitened target

Figure: [`innovation_whitened_target.svg`](innovation_whitened_target.svg)

[![Innovation-whitened target](innovation_whitened_target.svg)](proposition_56_innovation_whitened_target.md)

Physical question:

> If the temporal law is known, should predictable temporal correlation be paid for again as worst-case dependence, or should the local dynamics be used before covariance estimation?

Proposition 56 uses

\[
W_\tau R_\tau W_\tau^\mathsf T=I
\]

to convert the target into innovation coordinates before nuisance fitting.

On the scalar benchmark, the radius changes from the old known-\(\tau\) raw-time value

\[
2.16725
\]

to approximately

\[
\boxed{0.43644<1}.
\]

The repeated seeded errors shown by the experiment are visibility checks. The finite-sample guarantee comes from the exact Wishart reduction and matrix concentration.

What it does not establish: exact \(\tau\) is not available in a general application. That limitation motivates P57.

---

# 19. Proposition 57 / Experiment AR: robust innovation whitening

Figure: [`robust_innovation_whitened_target.svg`](robust_innovation_whitened_target.svg)

[![Robust innovation-whitened target](robust_innovation_whitened_target.svg)](proposition_57_robust_innovation_whitening.md)

This figure answers whether the innovation advantage survives finite-sample physical-time uncertainty.

### Calibration interval

The Proposition 55 certified interval is

\[
[0.686875,0.8515625]\ \mathrm{s}.
\]

One working value

\[
\tau_0=0.76921875\ \mathrm{s}
\]

is used to define a fixed target whitener.

### Radius ladder

The key comparison is:

| Representation | Relative radius |
| --- | ---: |
| calibrated raw time, P55 | 2.41488 |
| exact-tau innovation, P56 | 0.43647 |
| calibrated-tau robust innovation, P57 | 0.86771 |

The difference between P56 and P57 is the explicit finite-sample price of uncertainty about physical relaxation time under the current robust envelope.

### Pointwise versus uniform radii

Pointwise diagnostic radii are smaller than the uniform theorem because the theorem must protect all still-admissible between-grid \(\tau\) values and normalization variation.

That gap measures theorem conservatism. It is not a discrepancy in probability coverage.

---

# 20. Proposition 58 / Experiment AS: observer-scale covariance-to-world-tube audit

Figure: [`observer_bridge_dimension_audit.svg`](observer_bridge_dimension_audit.svg)

[![Observer-scale covariance-to-world-tube audit](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

Experiment AS is a bottleneck figure. It returns to the original moving-boundary problem and asks whether the scalar covariance success is sufficient at the actual observer score scale.

## Panel A: return to the moving world-tube

The panel shows

```text
012 -> 123 -> 234 -> 345 -> 456
```

and records:

- population action margin `0.1264216185`;
- exact runner-up uniform score radius `0.0105351349`;
- 35 candidates across 5 times, giving 175 observer covariance blocks;
- observer block dimension \(n+s=10\).

The 4,900 raw candidate edges reuse these target-indexed blocks.

## Panel B: scalar success versus observer-scale certification

Scalar exact-tau innovation radius:

\[
0.436444.
\]

Observer-scale exact-tau radius at dimension 10 and 175 simultaneous blocks:

\[
\boxed{1.857357>1.}
\]

This isolates a dimensional and simultaneous-certification bottleneck. Exact \(\tau\) is already supplied, so calibration uncertainty is not causing the failure.

## Panel C: entry into the perturbative regime

At 345 residual innovation degrees the current matrix theorem gives

\[
1.000746432,
\]

while at 346 it gives

\[
\boxed{0.999130352<1.}
\]

With nuisance rank two, this corresponds to 348 target rows merely to make the current relative perturbation layer admissible.

Crossing one is not the same as certifying the path.

## Panel D: end-to-end conservatism diagnostic

The current generic covariance-to-factor-to-path chain certifies the controlled population path only at a uniform covariance radius around

\[
1.11\times10^{-4}.
\]

The very large residual-degree number displayed beside it is **not a physical sample requirement**. It is a diagnostic of conservatism in the present theorem composition.

The scientific message is the next theorem direction:

- factor-specific covariance blocks;
- screen-first simultaneity reduction;
- candidate-local radii;
- direct score-margin concentration;
- exact structural-null exploitation.

---

# 21. How to read any future figure

Before interpreting a chart, ask six questions.

1. **What is measured?** Is the axis a physical observable, model parameter, estimation error, theorem bound, optimization margin, or diagnostic?
2. **What are the units?** If the quantity is dimensionless, why?
3. **What changed physically?** Did the system change, or did only sample size, calibration information, sampling schedule, numerical resolution, or theorem representation change?
4. **What is proved?** Is the figure illustrating a theorem, or is the visual pattern itself only empirical?
5. **What is diagnostic?** Is a displayed failure or enormous number deliberately revealing proof conservatism rather than describing a physical requirement?
6. **What conclusion is forbidden?** What physical or consciousness interpretation would require an additional bridge?

This discipline is part of the repository's documentation standard.
