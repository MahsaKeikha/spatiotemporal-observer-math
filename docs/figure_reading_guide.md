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

The experiment does not know the exact relaxation behavior, only a calibrated interval of possible temporal persistence.

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

# Proposition 52, Experiment AL

Figure: `certified_evalue_outer_cover.svg`

Mathematical question:

Can the exact Proposition 51 continuum confidence set be represented by a finite retained family that is safe to use in an independent target covariance theorem?

Physical picture:

A calibration experiment constrains the possible temporal memory of a physical process. A separate target record shares the same temporal parameters but also contains a declared affine nuisance drift. We want the target covariance certificate to remain valid for every temporal-memory model that the calibration experiment has not ruled out.

### Panel 1: temporal-memory ranges

The horizontal axis is `phi`, the persistence parameter in the effective AR(1) component.

The declared family spans `0.30` to `0.70`. The P51 grid visualization accepts points whose displayed `phi` span is about `0.4233` to `0.58`. The P52 certified outer cover is intentionally wider, about `0.3733` to `0.69`, because it must safely contain the complete continuum P51 confidence set, including between-grid points.

The wider P52 range is not a defect. It is the cost of replacing a picture by a theorem-certified finite enclosure.

### Panel 2: retained and excluded cells

The fixed `121 x 61` parameter grid contains 7,381 cells. Proposition 52 retains 5,325 and rigorously excludes 2,056.

A retained cell is not declared true. It is simply not safe to rule out under the stated finite-sample criterion.

An excluded cell is removed only after the likelihood perturbation bound proves that every parameter in that cell lies outside the exact Proposition 51 confidence set.

### Panel 3: target covariance error

The independent target visibility study shows median relative error about `0.116`, 95th percentile about `0.304`, and maximum about `0.544` across 128 controlled trials.

The theorem radius is about `0.899816`.

The observed trial errors are diagnostics. The theorem radius comes from the proof, not from fitting a bound around those 128 trials.

The value one is shown because a radius below one places several later covariance perturbation formulas in their usable regime. It is not a physical phase transition.

### Panel 4: physical inference chain

The panel shows the intended use order:

1. collect an independent temporal calibration record;
2. build the P51 continuum confidence set;
3. certify a P52 finite outer cover of every still-compatible temporal model;
4. collect an independent target record;
5. remove the predeclared nuisance drift;
6. certify the target covariance over the complete retained temporal family.

For Experiment AL the calibration and target confidence levels are both `0.975`, giving the product lower bound

\[
0.975^2=0.950625.
\]

What the figure does not show:

It does not identify a consciousness state, an energy threshold, or an observer boundary. Proposition 52 certifies a measurement ingredient that later boundary calculations may use.

---

# Proposition 53, Experiment AM

Figure: `physical_relaxation_sampling.svg`

Mathematical question:

Can one temporal parameter describe the same exponential relaxation process when the acquisition rate, timestamp spacing, or time unit changes?

Physical picture:

A process has a declared relaxation time \(\tau=0.8\) s. We observe the same model using different sampling clocks.

The exact relationship is

\[
\phi_{\Delta t}
=
\exp\left(-\frac{\Delta t}{\tau}\right).
\]

### Panel A: sampling rate versus one-step correlation

The one-step AR(1) coefficient changes from about `0.6065` at 2.5 Hz to about `0.9692` at 40 Hz.

This is expected. The sample-to-sample gap becomes shorter at higher sampling rates, so adjacent observations are more strongly correlated.

The change in `phi` does not mean the underlying declared process changed.

### Panel B: recovered physical relaxation time

Each sampling rate maps back through

\[
\tau
=
-\frac{\Delta t}{\log\phi_{\Delta t}}
\]

to the same value, `0.8 s`, up to floating-point roundoff.

This is the physical invariance Proposition 53 is designed to expose.

### Panel C: certified continuum cover in physical time

The declared interval is

\[
\tau\in[0.55,1.05]\ \mathrm{s}.
\]

The orange curve is the analytic operator covering radius. The blue curve is a dense numerical evaluation used only to show scale.

As the deterministic \(\tau\)-grid is refined from 5 to 65 points, the certified radius decreases from about `0.4160` to `0.0260`.

The blue curve lying below the orange curve is a numerical consistency check. The theorem comes from the analytic derivative bound, not from the dense grid.

### Panel D: irregular timestamps

Each dot is an actual acquisition time. The covariance entry between two measurements is computed from their elapsed physical separation:

\[
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

No integer lag is invented for missing or irregular samples.

The time-unit invariance error shown in the figure is at floating-point scale. Expressing the same timestamps and \(\tau\) in milliseconds instead of seconds leaves the covariance matrix unchanged.

What the figure does not establish:

It does not show that every physical system has one exponential relaxation time. It does not show that a fitted \(\tau\) is a universal intrinsic constant. It does not identify an observer boundary or consciousness state. A real application must test the exponential kernel against multi-timescale, oscillatory, nonstationary, and other alternatives.

---

# Proposition 55, Experiment AP

Figure: `quadratic_relaxation_calibration.svg`

**Panel A** compares certified physical-time width under the first-order and quadratic calibration enclosures. The shrinking orange curve means the deterministic representation of the same finite-sample confidence set is tighter. It does not mean the physical process changed.

**Panel B** shows the declared interval, the first-order retained interval, the quadratic retained interval, and the controlled true relaxation time. The interval is a confidence enclosure for a model parameter measured in seconds.

**Panel C** compares downstream target covariance theorem radii. The line at one is a mathematical perturbation threshold, not a physical phase transition.

**Panel D** highlights the key negative diagnostic: even exact knowledge of tau leaves the current target theorem at radius about `2.167`. Therefore calibration uncertainty is no longer the dominant bottleneck on this benchmark.

The figure does not measure energy, consciousness, integration, or physical organization directly.

---

# How to read any future figure

Before interpreting a chart, ask five questions.

1. **What is measured?** Is the axis a physical observable, a model parameter, an estimation error, or a theorem bound?
2. **What are the units?** If the quantity is dimensionless, why?
3. **What changed physically?** Did the simulated system change, or did only sample size, calibration information, sampling schedule, or mathematical resolution change?
4. **What is proved?** Is the figure illustrating a theorem, or is the visual pattern itself only empirical?
5. **What conclusion is forbidden?** What physical or consciousness interpretation would require an additional bridge?

This discipline is part of the repository's documentation standard.
