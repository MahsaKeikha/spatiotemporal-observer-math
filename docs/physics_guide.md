# Physics guide

This page explains the physical meaning of the mathematical objects used in the repository. It is intended to be read before the theorem ladder if the equations feel detached from the physical problem.

The main purpose is simple:

> **Before asking whether a moving subsystem can be identified mathematically, state what is physically moving, what is being measured, what interactions couple the measurements, what fluctuations are unresolved, and what evidence could falsify the model.**

The mathematics in this repository is conditional on a declared physical observation model. It does not turn a statistical pattern into a physical object by itself, and it does not identify consciousness by notation alone.

## 1. The physical problem in one picture

Imagine a large dynamical system with many measurable degrees of freedom. Depending on the application, those degrees of freedom could be:

- voltages on an electrical network;
- displacements or velocities in a mechanical array;
- pressure or velocity measurements in a fluid;
- firing-rate or field-potential channels in a neural recording;
- concentrations in a biochemical network;
- positions and internal states in a multi-agent system;
- generic sensor channels in a coupled physical process.

The full measured state at time `t` is written

\[
X_t=(X_t^{(1)},\ldots,X_t^{(n)}).
\]

The repository does **not** assume in advance that the same coordinates always form the subsystem of interest. Instead, it asks whether the dynamics support a moving candidate set

\[
S_t\subseteq\{1,\ldots,n\}.
\]

The sequence

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1})
\]

is called an observer world-tube.

The word `world-tube` is an analogy to the history of an extended object through time. It is not a claim that the construction is a relativistic spacetime world tube. Here the object being followed is a changing set of measured coordinates.

A useful concrete mental model is a coherent structure moving across a sensor field. A vortex moving across a fluid sensor array, a localized mechanical mode moving through a lattice, or a coordinated activity pattern moving across measurement channels can all produce a changing subset of coordinates that remains dynamically related even though its physical membership changes.

![Physics pipeline](physics_pipeline.svg)

## 2. The population dynamics and their physical meaning

The main exact model is

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t).
\]

This equation is a local stochastic dynamical model.

| Symbol | Mathematical role | Physical reading |
| --- | --- | --- |
| \(X_t\) | measured state vector | the physical observables recorded at time `t` |
| \(A_t\) | linear transition operator | effective coupling and propagation between measured degrees of freedom over one sampling interval |
| \(\varepsilon_t\) | unresolved random input | unresolved environmental forcing, omitted degrees of freedom, process noise, or other stochastic input represented by the model |
| \(Q_t\) | innovation covariance | covariance structure of that unresolved input |
| \(S_t\) | candidate coordinate set | a proposed physical subsystem boundary at time `t` |

The matrix \(A_t\) should not be interpreted as a fundamental law unless the application justifies that interpretation. In many experiments it is an effective linearization of more complicated dynamics over a chosen sampling interval.

Likewise, Gaussian noise is a modeling assumption, not a statement that microscopic physics is Gaussian. It is used because it makes conditional information, covariance propagation, and finite-sample concentration analytically tractable.

## 3. What makes a candidate subsystem physically interesting?

The implemented objective uses four structural ideas. Their physical interpretation is more important than their names.

### Internal integration

A candidate should contain components that are not merely sitting next to one another. Its internal parts should carry predictive information about one another.

Physical reading: the proposed subsystem contains coupled degrees of freedom that participate in a common dynamical organization.

A random collection of unrelated sensors should score poorly even if the sensors are individually active.

### Environmental insulation

A candidate should not require the rest of the measured system to explain every next-step change.

Physical reading: after the candidate's own state is known, the external coordinates should add comparatively little predictive information about the candidate's immediate evolution.

This does **not** require physical isolation. Open systems exchange matter, energy, and information with their surroundings. The operational question is whether the candidate has enough internal predictive closure to be distinguished from an arbitrary cut through the full system.

### Persistence

A candidate's present state should retain predictive structure into its future state.

Physical reading: the organization is not a one-frame fluctuation. Some collective modes survive long enough to define a temporally persistent structure.

### Transport

If the physical structure moves, the identity of the relevant coordinates may change. The information carried by the old coordinates should be transferred into the new coordinates.

Physical reading: a persistent pattern can move through a medium or sensor array without requiring the same measurement channels to belong to it forever.

This is the reason a moving boundary is needed at all.

## 4. Why covariance appears everywhere

For a multivariate fluctuating system, covariance describes how measured deviations co-vary:

\[
\Sigma=\mathbb E[(X-\mu)(X-\mu)^\top].
\]

The diagonal entries measure fluctuation variance in individual coordinates. The off-diagonal entries measure how pairs fluctuate together.

The eigenvectors of \(\Sigma\) identify collective fluctuation directions, while the eigenvalues quantify variance along those directions.

It is safer to call these quantities **fluctuation modes** or **variance modes**. They are not automatically physical energy modes. An energy interpretation requires an additional physical model connecting the measured coordinates and covariance to a Hamiltonian, temperature, power spectrum, or other energetic quantity.

Covariance is central here because, in a Gaussian model, many predictive information quantities can be written exactly in terms of covariance blocks. That makes it possible to propagate measurement uncertainty all the way into boundary scores and path recovery.

## 5. Why repeated measurements are not independent

A physical system has memory. If a sensor is high now, it is often likely to remain high a moment later. Treating every time sample as independent would therefore exaggerate how much information a finite record contains.

A simple temporal model is AR(1):

\[
R_\phi(i,j)=\phi^{|i-j|},
\qquad 0\le\phi<1.
\]

Here \(\phi\) controls persistence.

- \(\phi=0\): neighboring samples have no modeled temporal correlation.
- moderate \(\phi\): disturbances relax over several samples.
- \(\phi\) close to 1: the process has long temporal memory.

If samples are separated by a physical interval \(\Delta t\), a useful AR(1) relaxation-time interpretation is

\[
\tau=-\frac{\Delta t}{\log\phi},
\]

when the AR(1) model is physically appropriate.

The two-parameter family used in recent propositions is

\[
R_{\phi,\eta}
=(1-\eta)R_\phi+\eta I.
\]

The parameter \(\eta\) is a temporally uncorrelated fraction inside this model family.

Physical reading:

- \(\phi\) controls the persistence timescale of the correlated part;
- \(\eta\) controls how much variance is assigned to a fast, uncorrelated component.

This is still an effective temporal model. A real physical system may require multiple relaxation times, oscillatory kernels, colored noise, nonstationarity, or a continuous spectral density. Those are natural future generalizations.

## 6. What the nuisance subspace means physically

A measured record can contain large deterministic trends that are not the fluctuating dynamics we want to infer.

The recent theory writes such a trend as

\[
HB,
\]

where the columns of \(H\) are declared temporal shapes.

Examples include:

- a constant sensor baseline;
- linear drift from temperature or calibration;
- slow polynomial drift;
- known acquisition artifacts;
- a predeclared motion or stimulation profile.

The projector

\[
P_H=I-H(H^\top H)^{-1}H^\top
\]

removes those declared shapes exactly.

Physical reading: before estimating stochastic fluctuation geometry, subtract only the deterministic modes that were declared in advance as nuisance structure.

This matters because a large drift can create enormous apparent covariance even when the underlying fluctuating process has not changed.

The nuisance design must be fixed before examining the same stochastic record unless a separate adaptive-selection argument is provided. Otherwise the projection itself can overfit the noise.

## 7. What Propositions 41 through 52 are doing physically

The recent theorem sequence can be read as a single measurement-physics problem rather than as twelve unrelated inequalities.

| Proposition | Mathematical step | Physical question |
| ---: | --- | --- |
| 41 | dependent Gaussian covariance concentration | How much independent information is really present when the measured process has memory? |
| 42 | mean-centered normalization | How does removing an unknown baseline change the amount of usable fluctuation information? |
| 43 | AR(1) calibration from increments | Can the temporal persistence timescale be learned from the record instead of assumed? |
| 44 | nuisance-subspace projection | Can known drift shapes be removed without corrupting the fluctuation covariance? |
| 45 | estimated dependence plus nuisance projection | Can temporal-memory uncertainty and deterministic drift removal be handled together? |
| 46 | design-specific temporal geometry | Can the actual drift geometry replace a crude rank-only worst case? |
| 47 | direct Gaussian matrix concentration | Can the whole covariance matrix be certified using its physical fluctuation modes rather than a loose directional net? |
| 48 | uniform matrix bound over AR(1) uncertainty | Does the covariance certificate remain valid when the relaxation parameter is not known exactly? |
| 49 | compact temporal-family cover | Can the same reasoning cover a whole physically admissible family of temporal kernels? |
| 50 | two-parameter calibration | Can both persistence and fast uncorrelated variance be learned from independent calibration data? |
| 51 | full-likelihood e-value set | Can all calibration residuals define a joint finite-sample region of physically compatible temporal parameters? |
| 52 | certified outer cover and target composition | Can that continuum calibration region be converted into a finite safe family and propagated into an independent target covariance certificate? |

The important point is that these propositions are **measurement-certification machinery**. They are not a separate theory of consciousness. Their job is to prevent temporal memory, drift, calibration uncertainty, and finite record length from creating a false observer boundary later in the pipeline.

## 8. Why the relative covariance radius matters

Many recent theorems control a quantity of the form

\[
\left\|
\Sigma^{-1/2}(\widehat\Sigma-\Sigma)\Sigma^{-1/2}
\right\|_2
\le\epsilon.
\]

This is a relative operator-norm statement.

Physical reading: every collective fluctuation direction is estimated with a controlled multiplicative distortion after scaling by the true covariance geometry.

When \(\epsilon<1\), several important facts become available:

- the empirical covariance cannot cross through zero along a direction that has positive true variance;
- inverse covariance quantities remain perturbatively controllable;
- Gaussian conditional-information calculations can be stabilized;
- downstream score changes can be bounded instead of guessed.

The value `1` is therefore not a magical physical phase transition. It is a mathematical threshold that makes a useful perturbation regime available.

## 9. A complete physical reading of the pipeline

The project can be read from left to right as follows.

### Step 1: choose physical observables

Specify what each coordinate measures, its units, sensor bandwidth, sampling interval, and spatial or functional location.

### Step 2: write an effective dynamical model

Specify which couplings are represented by \(A_t\), which unresolved processes are represented by \(Q_t\), and over what timescale the linear approximation is intended to hold.

### Step 3: separate deterministic nuisance structure from fluctuations

Declare the nuisance design \(H\) before using the same record for stochastic inference.

### Step 4: characterize temporal memory

Estimate or constrain the family \(R_\theta\) describing correlation across repeated samples.

### Step 5: certify fluctuation covariance

Use finite-sample matrix probability to bound how far \(\widehat\Sigma\) can be from the population covariance.

### Step 6: score candidate physical boundaries

Evaluate internal integration, environmental insulation, persistence, and transport for each allowed candidate subsystem.

### Step 7: follow the best boundary through time

Optimize the complete path \(\mathcal W\), not each frame independently.

### Step 8: quantify ambiguity

Compare the best path with the strongest competitor. If the margin is small, the data do not strongly distinguish the proposed boundary.

### Step 9: test identifiability

Ask whether a different physical model could produce the same observables while implying a different boundary. If yes, passive observation alone cannot resolve the ambiguity.

### Step 10: only then discuss interpretation

A persistent, identifiable observer-like subsystem is still a dynamical structure. Any statement about consciousness requires additional bridge hypotheses and independent empirical tests.

## 10. A concrete thought experiment

Consider a two-dimensional grid of sensors measuring a fluctuating physical medium. A localized coherent pattern moves from left to right.

At one time the strongest internally coupled region may involve sensors `(0,1,2)`. A moment later the same physical pattern may be best represented by `(1,2,3)`, then `(2,3,4)`.

A fixed-boundary analysis can miss the persistence because it insists that identity means identical sensor membership.

The world-tube approach instead asks whether there is a path of changing coordinate sets for which:

1. internal measurements predict one another strongly;
2. outside measurements add comparatively little predictive information;
3. the internal state predicts its own future organization;
4. information is transported into the next physical location;
5. the path remains distinguishable from competing paths after finite-sample uncertainty is included.

That is the operational physical problem the repository is solving.

It is general enough to apply to many coupled systems, but any application must supply its own physical mapping from coordinates to observables.

## 11. Terminology that should not be over-interpreted

### Observer

Means a candidate persistent subsystem under the declared objective. It does not mean a conscious subject by definition.

### World-tube

Means a time-indexed path of candidate coordinate sets. It is inspired by the language of extended objects through time, but it is not automatically a relativistic construction.

### Action and action margin

The repository uses an optimization objective and the difference between the best and competing paths. This is **not** physical action in units of joule-seconds unless a future derivation explicitly connects the objective to a physical action functional.

### Information

Mutual information and related quantities measure statistical dependence. They are not automatically thermodynamic entropy, free energy, causal influence, semantic information, or subjective information.

### Integration

Means a declared statistical property of the candidate dynamics. It should not be equated with phenomenal unity without an additional tested hypothesis.

## 12. Units and dimensional accountability

A physical application should state units explicitly.

- \(X_t\) carries the units of the measured observables.
- covariance carries squared observable units.
- \(Q_t\) carries the same covariance units.
- \(A_t\) maps units at one sample to units at the next and may be dimensionless only when the coordinate convention permits it.
- correlation coefficients, canonical correlations, and normalized covariance errors are dimensionless.
- mutual information is dimensionless when measured in nats or bits.

If different physical observables with different units are combined, the coordinate scaling must be declared. A result that changes under arbitrary unit conversion without an explicit reason is physically suspect.

This is one reason representation-invariance results are an important structural frontier for the project.

## 13. Physics accountability checklist

Before applying the framework to an experimental system, document all of the following.

### Observables

- What does each coordinate measure?
- What are its units?
- What is the sampling interval?
- What is the sensor bandwidth and filtering pipeline?
- Is the coordinate basis physically meaningful or chosen for convenience?

### Dynamics

- What physical interaction is represented by \(A_t\)?
- Over what time interval is linearization plausible?
- Which omitted mechanisms are absorbed into \(Q_t\)?
- Are there conservation laws or symmetries the fitted model should obey?

### Boundary

- What makes a candidate coordinate set physically contiguous or admissible?
- May membership change arbitrarily, or only through local transport?
- Does the candidate family encode actual geometry?

### Temporal statistics

- Is AR(1) physically adequate?
- Is one relaxation time enough?
- Is the process stationary during the analyzed window?
- Are oscillations, long-memory effects, or colored noise visible in residual diagnostics?

### Nuisance structure

- Which trends are removed?
- Were they declared before inspecting the same stochastic residuals?
- Could the projection remove genuine physical dynamics?

### Validation

- Does the fitted model reproduce held-out correlation structure?
- Do residuals violate Gaussianity or stationarity strongly enough to matter?
- Does the inferred boundary survive changes in sampling rate, units, sensors, and coordinate representation?
- Can an intervention perturb the proposed subsystem differently from a competing boundary?

If these questions are not answered, the mathematics may still be correct for the stated model, but the physical interpretation is incomplete.

## 14. Where the consciousness question enters, and where it does not

The present physics layer asks whether a persistent subsystem can be operationally identified from dynamical organization and finite measurements.

That is already a difficult physical inference problem.

A consciousness interpretation would require substantially more. At minimum, one would need a bridge explaining why specific observer-like dynamical properties should correspond to conscious properties, and then test predictions that distinguish that bridge from competing explanations.

The repository therefore keeps three statements separate:

1. **Mathematical statement:** a theorem follows from explicit assumptions.
2. **Physical statement:** an experimental system is adequately described by those assumptions and mapped observables.
3. **Consciousness statement:** an additional bridge connects the physical structure to conscious experience.

Only the first is established by proof alone. The second requires physical validation. The third requires a separate scientific theory and evidence.

See the [interpretation protocol](interpretation_protocol.md) for the formal obligations placed on any future bridge.

## 15. How to read the repository from here

If you are approaching the project from physics, the recommended order is:

1. this Physics Guide;
2. the [research overview](research_overview.md);
3. the moving-boundary figures on the [front page](../README.md);
4. the [assumption ledger](assumption_ledger.md);
5. only then the detailed proposition proofs.

The theorem pages should be read as certification layers supporting the physical inference pipeline, not as isolated equations.