# Figure reading guide

This page explains what the main repository figures mean physically and statistically. It is a companion to the [Physics Guide](physics_guide.md).

A recurring source of confusion is that several plots show **uncertainty about a mathematical quantity**, not a directly measured physical observable. A covariance radius, confidence region, or theorem bound should not be read as an energy, force, consciousness level, or physical phase unless an additional derivation establishes that meaning.

## Three kinds of figures in the repository

### 1. Structural figures

These visualize the moving-boundary problem itself.

Examples:

- candidate scores over time;
- recovered world-tube paths;
- path-recovery phase diagrams.

Physical question: **where is the dynamically coherent subsystem, and can its boundary move while remaining identifiable?**

### 2. Calibration figures

These visualize what temporal-memory models remain compatible with a calibration record.

Examples:

- AR(1) confidence intervals;
- two-parameter `phi, eta` regions;
- e-value confidence-set geometry.

Physical question: **how strongly does the measured process remember its past, and how uncertain are we about that temporal-memory model?**

### 3. Certification figures

These compare finite-sample theorem radii with empirical estimation error or with older, looser bounds.

Physical question: **is the fluctuation covariance known accurately enough that downstream boundary scores can be trusted under the stated assumptions?**

The theorem radius is a guarantee under a model. It is not itself a physical state variable.

---

# Moving-boundary figures

## Candidate scores over time

File: `worldtube_baseline.png`

What it shows:

A controlled subsystem changes which coordinates represent it as time advances. Candidate scores indicate which coordinate set is preferred at each time.

Physical reading:

Imagine a coherent structure moving across a sensor array. The physical pattern persists, while the sensors representing it change.

What to look for:

- Does the highest-scoring candidate follow the planted moving structure?
- Are alternative candidates close in score?
- Does the preferred boundary jump in a physically implausible way?

What it does not show:

It does not show consciousness. It shows recovery of a planted dynamical boundary in a controlled model.

## World-tube phase diagram

File: `worldtube_phase_diagram.png`

What it shows:

Regions where path recovery succeeds or fails as model or regularization parameters change.

Physical reading:

Continuity is useful because a physical structure normally does not teleport arbitrarily across coordinates. But too much continuity pressure can force the estimator to prefer a smooth path even when the dynamics support another boundary.

The failure region is therefore physically informative. It shows that prior assumptions about motion can overwhelm measured evidence.

---

# Proposition 44, Experiment AD

Figure: `nuisance_projection_calibration.svg`

Mathematical question:

Can a declared time-varying nuisance mean be removed without biasing covariance recovery?

Physical picture:

A sensor record contains a large deterministic baseline or linear drift on top of stochastic fluctuations.

What the figure means:

Ordinary centering leaves strong drift contamination as the nuisance amplitude grows. Projection onto the orthogonal complement of the declared nuisance design keeps the stochastic covariance estimate stable.

Physical lesson:

A deterministic trend can look like strong covariance even when the underlying fluctuation physics has not changed.

What it does not mean:

The theorem does not say every slow trend is nuisance. If a removed trend is genuine system dynamics, projecting it away would remove real physics.

---

# Proposition 45, Experiment AE

Figure: `estimated_ar1_nuisance_projection.svg`

Mathematical question:

Can uncertain temporal memory and time-varying nuisance drift be handled together?

Physical picture:

The target system has both deterministic drift and temporally correlated fluctuations.

What the correlation parameter means:

Larger `phi` means a longer modeled persistence timescale. Neighboring samples contain more redundant information.

What the theorem radius means:

It is a bound on relative covariance estimation error after accounting for temporal dependence and nuisance removal.

What it does not mean:

A larger radius at stronger correlation does not mean the physical system is less organized. It means the finite record contains less independent information for estimating covariance under that model.

---

# Proposition 46, Experiment AF

Figure: `design_specific_ar1_envelope.svg`

Mathematical question:

Does nuisance rank alone describe how much stochastic information survives projection?

Physical picture:

Two sets of removed drift modes can have the same number of columns but interact very differently with the temporal covariance modes of the measured process.

What the figure means:

Using only nuisance rank can declare a problem uninformative even when the actual removed temporal shapes leave substantial fluctuation information intact.

Physical lesson:

The geometry of what is removed matters, not only how many nuisance directions are removed.

---

# Proposition 47, Experiment AG

Figure: `weighted_wishart_matrix_chernoff.svg`

Mathematical question:

Can covariance uncertainty be bounded directly using the complete temporal eigenvalue profile?

Physical picture:

The measured fluctuation record contains collective temporal modes with different strengths.

What the plotted radius means:

It measures worst-case relative covariance uncertainty under the theorem.

A smaller radius means the statistical certification is tighter. It does not mean the physical system itself has become quieter or more coherent.

Why `radius < 1` is highlighted:

That threshold places covariance estimation inside a perturbative regime needed by later inverse-covariance and information calculations.

It is not a physical critical point.

---

# Proposition 48, Experiment AH

Figure: `uniform_matrix_chernoff_ar1.svg`

Mathematical question:

Can the Proposition 47 covariance guarantee remain valid when `phi` is uncertain?

Physical picture:

The experiment does not know the exact relaxation time, only a calibrated interval of possible temporal persistence.

What the figure means:

The theorem propagates that uncertainty through the complete projected temporal spectrum rather than plugging in one guessed correlation coefficient.

Physical lesson:

A covariance claim should remain valid over the range of temporal-memory models that the experiment cannot distinguish.

---

# Proposition 49, Experiment AI

Figure: `compact_temporal_family.svg`

Mathematical question:

Can covariance concentration handle a whole multi-parameter family of temporal models?

Physical picture:

A real experiment may not justify a single temporal kernel. Several combinations of persistence and fast noise can remain plausible.

What cover refinement means:

A finite mathematical cover is made geometrically finer so every physically admissible covariance in the declared family lies close to a represented cover point.

What the falling radius means:

The deterministic approximation of the temporal family is becoming tighter.

It is not evidence that the underlying physical process changes when the grid is refined. Only the mathematical representation of uncertainty changes.

---

# Proposition 50, Experiment AJ

Figure: `calibrated_temporal_family.svg`

Mathematical question:

How does additional independent calibration data change uncertainty about temporal dynamics?

Physical picture:

The target physical system is held fixed. Only the amount of independent information used to estimate its temporal-memory parameters is increased.

What the x-axis means:

More calibration channels mean more independent realizations of the same controlled temporal process.

What the falling covariance radius means:

Temporal-model uncertainty is shrinking, so the target covariance can be certified more tightly.

It does not mean the target system becomes physically more stable when calibration channels are added.

---

# Proposition 51, Experiment AK

Figure: `evalue_temporal_confidence_set.svg`

Mathematical question:

Which combinations of `phi` and `eta` remain compatible with the complete calibration residual likelihood?

Physical picture:

Each point in the plane represents a different effective temporal-memory model.

- horizontal direction: persistence parameter `phi`;
- vertical direction: temporally uncorrelated fraction `eta`.

The accepted region means:

Those parameter values are not rejected by the finite-sample e-value construction at the declared confidence level.

The region does **not** mean:

- a posterior probability density;
- a consciousness landscape;
- an energy surface;
- a free-energy landscape;
- a causal map.

The plotted grid is a visualization of the exact continuum e-value function. Proposition 51's probability statement is not restricted to displayed grid points.

---

# Proposition 52, Experiment AL under development

Proposition 52 is being developed to turn the irregular Proposition 51 continuum set into a finite certified outer cover.

The intended physical reading is:

1. calibration data define which temporal-memory models remain possible;
2. a deterministic geometric theorem safely encloses every such model;
3. that complete temporal uncertainty is propagated into an independent target covariance estimate;
4. only after that covariance is certified should it be used in moving-boundary scores.

Two different geometric radii are required:

- a projected eigenvalue radius controlling collective fluctuation modes after nuisance removal;
- a normalization radius controlling the total projected fluctuation scale.

These are statistical certification quantities, not physical observables.

---

# How to read any future figure

Before interpreting a chart, ask five questions.

1. **What is measured?** Is the axis a physical observable, a model parameter, an estimation error, or a theorem bound?
2. **What are the units?** If the quantity is dimensionless, why?
3. **What changed physically?** Did the simulated system change, or did only sample size, calibration information, or mathematical resolution change?
4. **What is proved?** Is the figure illustrating a theorem, or is the visual pattern itself only empirical?
5. **What conclusion is forbidden?** What physical or consciousness interpretation would require an additional bridge?

This discipline is now part of the repository's documentation standard.