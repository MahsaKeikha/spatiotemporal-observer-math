# Release 0.45.0 research record

Date: 2026-09-08

## Research addition

Release 0.45.0 adds **Proposition 56**, exact innovation-whitened target covariance concentration, and **Experiment AQ**.

The release follows directly from the negative diagnostic in Proposition 55. On the Experiment AP target schedule, even supplying the true physical relaxation time exactly to the previous raw-time target theorem left the relative covariance radius at

\[
\varepsilon_{\mathrm{raw\ oracle}}=2.167246895150515>1.
\]

That result showed that further calibration tightening alone could not close the benchmark.

Proposition 56 therefore changes the target estimator itself.

## Main theorem idea

Under the declared separable Gaussian target model

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)\sim\mathcal N(0,R_\tau\otimes\Gamma),
\]

Proposition 53 supplies the exact irregular-grid temporal whitener

\[
W_\tau R_\tau W_\tau^\mathsf T=I.
\]

Transform both the measurements and the predeclared nuisance design:

\[
Z=W_\tau Y,
\qquad
G=W_\tau H.
\]

After residualization with

\[
P_G=I-G(G^\mathsf TG)^{-1}G^\mathsf T,
\]

define

\[
\widehat\Gamma_{\mathrm{IW}}
=
\frac{1}{N-q}Z^\mathsf TP_GZ.
\]

Because \(P_G\) is an orthogonal projector of rank \(N-q\),

\[
\boxed{
(N-q)\widehat\Gamma_{\mathrm{IW}}
\sim\operatorname{Wishart}_d(\Gamma,N-q)
}.
\]

Proposition 47 therefore applies with exactly \(N-q\) unit temporal weights.

## Experiment AQ benchmark

Experiment AQ reuses the target schedule from Experiment AP:

- physical relaxation time: `0.78 s`;
- target sample count: `120`;
- nuisance rank: `2`;
- residual innovation degrees of freedom: `118`;
- covariance confidence: `0.975`;
- displayed block dimension: `1`;
- displayed block count: `1`.

The old known-tau raw-time oracle had

- projected temporal trace: `84.34348989587866`;
- maximum projected temporal eigenvalue: `14.524615089393357`;
- relative covariance radius: `2.167246895150515`.

The innovation-whitened theorem has

- temporal trace: `118`;
- temporal spectral norm: `1`;
- relative covariance radius: `0.4364443814369348`;
- radius reduction: `79.86180612769438%`;
- perturbative threshold status: `0.4364443814369348 < 1`.

The exact whitening identity is satisfied on the committed benchmark at operator error approximately `5.20e-15`.

A 512-trial seeded scalar visibility check recorded all 512 relative covariance errors below the Proposition 56 matrix radius. This repeated simulation is not the proof; the guarantee comes from the exact Wishart reduction and Proposition 47.

## Scope

The theorem is conditional on:

- exact separable Gaussian covariance;
- the declared one-timescale stationary exponential relaxation model;
- exact knowledge of target \(\tau\);
- strictly increasing target timestamps;
- a fixed predeclared full-rank nuisance design;
- applying the same temporal whitener to both measurements and nuisance design;
- covariance blocks declared before the concentration statement is evaluated.

A wrong working timescale leaves residual temporal dependence. Release 0.45.0 does not yet propagate the finite-sample Proposition 55 \(\tau\) set through the innovation whitener.

## New files

Implementation:

- `src/observer_math/innovation_whitening.py`

Claim-level tests:

- `tests/test_innovation_whitening.py`

Experiment and renderer:

- `examples/innovation_whitened_target.py`
- `examples/render_innovation_whitened_target.py`

Documentation and results:

- `docs/proposition_56_innovation_whitened_target.md`
- `docs/innovation_whitened_target.json`
- `docs/innovation_whitened_target.svg`

## Research record

| Item | 0.45.0 state |
| --- | ---: |
| Propositions | 56 |
| Reproducible experiments | 43, A-Z and AA-AQ |
| Scientific result figures | 31 |
| Claim-level tests | 211 |
| CI matrix | Python 3.10, 3.11, 3.12 |

## Next theorem frontier

The next target is to connect Proposition 55 and Proposition 56 directly by controlling the whitening mismatch

\[
W_{\widetilde\tau}R_\tau W_{\widetilde\tau}^\mathsf T-I
\]

uniformly over a certified true/working timescale pair, while also controlling the transformed nuisance geometry.

The goal is to retain as much as possible of the 118-innovation information gain without assuming exact target \(\tau\).
