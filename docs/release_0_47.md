# Release 0.47.0 research record

Date: 2026-09-08

## Research addition

Release 0.47.0 adds **Proposition 58**, relative covariance uncertainty propagated to observer world-tube recovery, and **Experiment AS**, the observer-scale covariance-to-world-tube certification audit.

This release returns the finite-sample measurement program to the original moving-boundary question that motivated the repository.

Propositions 53 through 57 established sampling-consistent physical time, finite-sample relaxation-time calibration, exact innovation whitening, and robust scalar covariance certification under calibrated physical-time uncertainty. Proposition 58 asks what happens when that covariance uncertainty is propagated into the actual multivariate observer score and the complete moving path.

## Main theorem idea

At dynamical time \(t\), let \(S\) be a future candidate subsystem of size \(s\) inside a measured state with \(n\) coordinates. Define the observer covariance block

\[
\boxed{
B_{t,S}=(X_t,X_{t+1}^{S}).
}
\]

Its dimension is

\[
\boxed{d_{\mathrm{obs}}=n+s.}
\]

This one target-indexed block contains the covariance submatrices needed for:

- directed integration inside the candidate;
- environmental leakage into the future candidate;
- persistence;
- transport from every current source candidate into that future target.

If there are \(T\) dynamical times and \(C\) candidate boundaries, the simultaneous covariance count is therefore

\[
\boxed{B_{\mathrm{obs}}=TC,}
\]

not the raw number of candidate-to-candidate edges.

Proposition 58 starts from simultaneous candidate-local relative covariance events

\[
\left\|
\Sigma_{t,S}^{-1/2}
(\widehat\Sigma_{t,S}-\Sigma_{t,S})
\Sigma_{t,S}^{-1/2}
\right\|_2
\le\delta_{t,S}<1.
\]

It deterministically propagates those radii through integration, environmental independence, canonical persistence, local observer scores, transport scores, and the complete world-tube action. A positive recovery slack certifies the population path on the same covariance event. No additional probability budget is spent by the bridge itself.

Declared exact structural integration nulls can use the repository's sharper null-specific perturbation bound.

## Experiment AS benchmark

The controlled moving-module problem uses

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
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

The raw candidate-edge count is 4,900, but those edges reuse the same 175 target-indexed observer covariance blocks.

The planted and recovered population path is

```text
(0,1,2) -> (1,2,3) -> (2,3,4) -> (3,4,5) -> (4,5,6)
```

with:

- population action: `1.2543238015160432`;
- runner-up action: `1.127902183014015`;
- population action margin: `0.12642161850202815`;
- exact runner-up uniform score radius: `0.010535134875169013`;
- declared structural integration-null states: `120` out of `175`.

## Observer-scale concentration diagnostic

The scalar exact-tau Proposition 56 benchmark has relative covariance radius

\[
0.4364443814.
\]

At the actual observer scale, with block dimension 10, simultaneous block count 175, and 118 residual innovation degrees, the same exact-tau unit-weight matrix theorem gives

\[
\boxed{
\varepsilon_{\mathrm{observer}}=1.8573569119>1.
}
\]

This is outside the relative perturbation regime used by Proposition 58.

The current matrix theorem first enters \(\varepsilon<1\) at 346 residual innovation degrees:

\[
\varepsilon_{345}=1.0007464318,
\qquad
\boxed{\varepsilon_{346}=0.9991303523.}
\]

With nuisance rank two, that entry point corresponds to 348 target rows.

Crossing one does not by itself certify the world-tube path. It only makes the current relative-covariance perturbation layer admissible.

## End-to-end conservatism diagnostic

On the same controlled population world-tube, the largest current **uniform** relative covariance radius that certifies the population path through the generic Proposition 58 factor-perturbation chain is approximately

\[
\boxed{
\delta_{\mathrm{path}}=0.0001109829747.
}
\]

Under the current unit-weight matrix bound, reaching that very small uniform radius would require approximately

\[
21,165,400,697
\]

residual innovation degrees.

This number is **not a physical sample requirement**. It is a conservatism diagnostic for the present proof chain. Its role is to show where the next mathematical improvement should occur.

## What Experiment AS changes

The scalar covariance bottleneck and the observer-scale bottleneck are not the same problem.

Experiment AS shows that the next frontier is dimensional and structural:

1. factor-specific covariance blocks rather than one maximum-dimensional observer block for every factor;
2. screen-first simultaneity reduction so distant competitors do not consume the strongest covariance guarantee;
3. candidate-local covariance radii rather than one global worst case;
4. direct concentration of score differences or action margins rather than repeated generic factor-by-factor perturbation;
5. richer temporal models only after the observer-scale structural bottleneck is understood.

The negative diagnostic is part of the result. It prevents the program from continuing to sharpen physical-time calibration when the dominant limitation has moved elsewhere.

## Visual documentation

The release adds a dedicated four-panel scientific figure:

[![Experiment AS](observer_bridge_dimension_audit.svg)](proposition_58_observer_bridge.md)

Panel A returns to the planted moving world-tube and shows the actual observer-block geometry. Panel B compares scalar and observer-scale covariance radii. Panel C locates the current matrix-theorem entry point into \(\varepsilon<1\). Panel D records the end-to-end proof-conservatism diagnostic and the next theorem directions.

The release also adds the [Visual Research Guide](visual_research_guide.md), which organizes the complete scientific figure record from physical observables through Proposition 58 and provides separate reading routes for physicists, mathematicians, statisticians, and readers coming from Tegmark's work.

## New files

Implementation:

- `src/observer_math/observer_bridge.py`

Claim-level tests:

- `tests/test_observer_bridge.py`

Experiment and renderer:

- `examples/observer_bridge_dimension_audit.py`
- `examples/render_observer_bridge_dimension_audit.py`

Documentation and results:

- `docs/proposition_58_observer_bridge.md`
- `docs/observer_bridge_dimension_audit.json`
- `docs/observer_bridge_dimension_audit.svg`
- `docs/visual_research_guide.md`

## Research record

| Item | 0.47.0 state |
| --- | ---: |
| Propositions | 58 |
| Reproducible experiments | 45, A-Z and AA-AS |
| Scientific result figures | 33 |
| Claim-level tests | 223 |
| CI matrix | Python 3.10, 3.11, 3.12 |

The physics pipeline remains an explanatory diagram and is not included in the 33 scientific-result figure count.

## Interpretation boundary

Proposition 58 certifies a moving subsystem path only under a simultaneous covariance event and the declared observer-score model. It does not establish that every physical system has a unique observer boundary, and it does not establish consciousness.

The observer notation remains operational. Any future connection to subjective experience requires additional hypotheses and tests under the [Interpretation Protocol](interpretation_protocol.md).

## Next theorem frontier

The immediate mathematical frontier is now localized observer-scale certification:

> **Can the covariance geometry actually needed by the near-competitive observer factors be certified directly enough that the world-tube action margin, rather than a chain of global worst-case intermediate bounds, becomes the main object of concentration?**

That question follows directly from Experiment AS and is the appropriate next step for the current research program.
