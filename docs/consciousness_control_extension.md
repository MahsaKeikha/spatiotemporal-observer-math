# Consciousness-to-control extension boundary

Research I remains a mathematical consciousness-measurement program. Its core question is whether a time-dependent subsystem boundary can be inferred and certified from stochastic dynamics using operational measurements. The control-systems extension does not replace that question. It asks what a measurement device can safely do **after** it has produced a boundary estimate and an uncertainty/certification state.

## Scientific architecture

Keep three layers distinct:

1. **Consciousness-related measurement hypothesis.** Research I defines operational dynamical quantities and a moving-boundary inference problem. These quantities are measurements or candidate correlates under the declared model. They are not, by themselves, proof that consciousness has been measured.
2. **Certified structural observer.** The existing theorem chain determines when a moving subsystem estimate is recoverable, identifiable only up to symmetry, uncertain, or uncertified.
3. **Device supervisory control.** A downstream controller may use the observer output and its confidence state to select measurement settings, sampling schedules, sensing channels, stimulation/actuation settings where ethically and experimentally appropriate, or a safe/abstaining mode.

This creates a closed measurement-control loop without converting an operational consciousness hypothesis into an established physical fact.

## Device-level state

A useful augmented device state is

\[
z_k=(\hat x_k,\hat S_k,c_k,m_k),
\]

where \(\hat x_k\) is the estimated dynamical state, \(\hat S_k\) is the inferred subsystem boundary, \(c_k\) is a certification/confidence state, and \(m_k\) is the current device mode.

The controller should depend on certification:

\[
u_k=\pi(\hat x_k,\hat S_k,c_k,m_k).
\]

An uncertified structural estimate must not silently be treated as ground truth.

## Supervisory modes

The device-control extension should distinguish at least:

- **measurement mode:** collect the nominal sensor set;
- **information-seeking mode:** adapt sensing/sampling to reduce structural uncertainty;
- **tracking mode:** follow a sufficiently supported moving boundary;
- **abstain/safe mode:** avoid boundary-dependent actions when certification is inadequate.

A later physical-device implementation may refine these modes, but the mathematics should preserve the distinction between estimating, certifying, and acting.

## Control objective

A device-oriented objective should not be "maximize consciousness." A defensible engineering objective is multi-term:

\[
J=\sum_k \bigl(
\ell_{\mathrm{track},k}
+\gamma_u\lVert u_k\rVert^2
+\gamma_c\ell_{\mathrm{uncert},k}
+\gamma_s\ell_{\mathrm{switch},k}
\bigr),
\]

subject to plant/device dynamics, measurement constraints, safety limits, and a certification gate.

Depending on the physical device, \(u_k\) may represent sensor selection, sampling rate, gain/range configuration, excitation, or another explicitly modeled actuator. The repository must not imply a specific medical or consciousness-modifying actuation channel until that channel is actually defined and validated.

## Research questions for the extension

The strongest continuity with Research I comes from questions that use its existing mathematics rather than attaching an unrelated controller:

**RQ1. Certification-aware control.** How should the device change mode when the moving-boundary certificate becomes weak or fails?

**RQ2. Active measurement.** Can the controller choose the next sensing configuration to reduce uncertainty in the boundary decision while respecting measurement cost and safety constraints?

**RQ3. Boundary-aware tracking.** When the dynamically relevant subsystem moves, does conditioning control/measurement decisions on \(\hat S_k\) improve tracking or information acquisition relative to fixed-boundary and conventional multiple-model baselines?

**RQ4. Stability under structural-estimation error.** Under what explicit mismatch and switching assumptions can stability or bounded performance be guaranteed when \(\hat S_k\neq S_k\)?

**RQ5. Abstention.** Can a safe mode preserve device constraints when the structural estimate is observationally nonidentifiable or finite-sample certification fails?

## Contribution boundary

The control extension may legitimately contribute new engineering mathematics if it derives results that depend on the Research I structure, for example:

- a certification-gated supervisory policy;
- a stability/performance theorem with structural-estimation mismatch;
- an information-seeking sensing policy tied to the world-tube uncertainty;
- a bound connecting boundary error to closed-loop performance degradation;
- an abstention/safe-mode guarantee when the certificate fails.

These are extension targets, not established results until proved and tested.

## Validation ladder

A device claim should progress through:

```text
mathematical model
  -> synthetic closed-loop benchmark
  -> hardware-in-the-loop or recorded-device replay
  -> benchtop device validation
  -> human/clinical validation only under the appropriate protocol
```

Simulation can validate algorithms against a declared model. It cannot establish that an operational score is a consciousness measure in humans.

## Terminology discipline

Use **consciousness-related measurement**, **operational observer score**, **candidate subsystem boundary**, or **structural estimate** when that is what the evidence supports.

Reserve stronger biological or experiential interpretations for results supported by the corresponding experimental evidence.

## Connection to the existing program

The original world-tube inference remains upstream. The control extension begins at its output:

\[
\text{signals}
\rightarrow
\text{dynamical features}
\rightarrow
\text{moving-boundary inference}
\rightarrow
\text{certification / abstention}
\rightarrow
\text{device supervisory decision}
\rightarrow
\text{new measurements}.
\]

This preserves the consciousness research lineage while making the engineering extension a natural consequence of the measurement problem rather than a separate control benchmark.
