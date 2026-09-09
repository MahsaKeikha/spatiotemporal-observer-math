# Release 0.46.0 research record

Date: 2026-09-08

## Research addition

Release 0.46.0 adds **Proposition 57**, robust innovation whitening under calibrated physical-time uncertainty, and **Experiment AR**.

The release closes the exact-relaxation-time limitation recorded in Proposition 56.

Proposition 55 had already calibrated the physical relaxation time to the finite-sample hull

\[
[0.686875,0.8515625]\ \mathrm{s}
\]

at confidence `0.975`. Proposition 56 then showed that if the exact target relaxation time were known, innovation whitening reduced the target covariance radius from the old raw-time oracle value `2.1672468952` to `0.4364443814 < 1`.

The open question was whether that gain survives when the true physical timescale is only finitely known.

## Main theorem idea

Choose one working relaxation time from the independent calibration result. Experiment AR uses the midpoint

\[
\tau_0=0.76921875\ \mathrm{s}.
\]

Let \(W_0\) be the exact Proposition 53 innovation whitener for \(\tau_0\). For any still-admissible true relaxation time \(\tau\), define the transformed temporal covariance

\[
C_\tau=W_0R_\tau W_0^\mathsf T.
\]

Proposition 53 supplies

\[
\|R_\tau-R_{\tau'}\|_2
\le
L_R|\tau-\tau'|.
\]

Therefore

\[
\|C_\tau-C_{\tau'}\|_2
\le
\|W_0\|_2^2L_R|\tau-\tau'|.
\]

A finite cover of the calibrated \(\tau\)-interval, together with Weyl eigenvalue control and a conservative projected-trace envelope, turns the complete transformed covariance family into a valid Proposition 49 compact-family matrix-concentration problem.

The target covariance estimator uses the same fixed working whitener for all target records and the deterministic reference normalization certified by the transformed family.

## Experiment AR benchmark

Experiment AR carries forward the target schedule from Experiments AP and AQ:

- calibrated relaxation-time hull: `[0.686875, 0.8515625] s`;
- working relaxation time: `0.76921875 s`;
- target sample count: `120`;
- nuisance rank: `2`;
- residual rank: `118`;
- calibration confidence: `0.975`;
- target covariance confidence: `0.975`;
- combined confidence lower bound: `0.950625`;
- displayed block dimension: `1`;
- displayed block count: `1`.

The 1025-point transformed-family cover has:

- maximum tau spacing: `0.00016082763671887434 s`;
- raw covariance operator-Lipschitz bound: `29.949498594791883 s^-1`;
- working-whitener operator norm: `5.15015088828919`;
- transformed operator-Lipschitz bound: `794.3821231568684 s^-1`;
- transformed eigenvalue covering radius: `0.06387929975952046`;
- transformed projected-normalization covering radius: `7.537757371623415`.

The certified projected temporal range is

\[
99.80104\le d_\tau\le138.59636,
\]

with deterministic reference normalization

\[
119.19870.
\]

The final uniform relative covariance radius is

\[
\boxed{
\varepsilon_{57}=0.8677117534900387<1.
}
\]

## Comparison

| Target theorem | Physical-time information | Relative covariance radius |
| --- | --- | ---: |
| Proposition 55 raw-time calibrated target | finite-sample calibrated interval | 2.41488 |
| Proposition 55 raw-time oracle diagnostic | exact true tau | 2.16725 |
| Proposition 56 innovation target | exact true tau | 0.43647 |
| **Proposition 57 robust innovation target** | **finite-sample calibrated interval** | **0.86771** |

Proposition 57 reduces the radius by approximately `64.1%` relative to the Proposition 55 calibrated raw-time target theorem while removing the exact-target-tau assumption.

The uncertainty is not free: the robust radius is larger than the exact-tau Proposition 56 radius. The scientifically important result is that it remains below one.

## Pointwise diagnostics

Pointwise evaluations of the fixed working whitener give radii between approximately `0.404` and `0.580` at the four recorded diagnostic timescales. The theorem reports the larger uniform radius `0.86771` because it also protects every between-grid timescale and the projected normalization continuum.

Those pointwise calculations diagnose conservatism. They are not substitutes for the uniform theorem.

## Scope

The theorem is conditional on:

- exact separable Gaussian space-time covariance;
- the declared stationary one-timescale exponential relaxation family;
- a calibration interval obtained independently of the target record;
- strictly increasing target timestamps;
- a fixed predeclared full-rank nuisance design;
- applying the same working whitener to target measurements and nuisance design;
- covariance blocks declared before the concentration statement is evaluated.

Relevant falsification diagnostics include residual temporal structure outside the certified transformed family, multiple or drifting relaxation times, oscillatory temporal covariance, non-Gaussian innovations, nonseparable covariance, and calibration-to-target mismatch.

## New files

Implementation:

- `src/observer_math/robust_innovation_whitening.py`

Claim-level tests:

- `tests/test_robust_innovation_whitening.py`
- `tests/test_robust_innovation_whitening_artifact.py`

Experiment and renderer:

- `examples/robust_innovation_whitened_target.py`
- `examples/render_robust_innovation_whitened_target.py`

Documentation and results:

- `docs/proposition_57_robust_innovation_whitening.md`
- `docs/robust_innovation_whitened_target.json`
- `docs/robust_innovation_whitened_target.svg`

## Research record

| Item | 0.46.0 state |
| --- | ---: |
| Propositions | 57 |
| Reproducible experiments | 44, A-Z and AA-AR |
| Scientific result figures | 32 |
| Claim-level tests | 219 |
| CI matrix | Python 3.10, 3.11, 3.12 |

## Next theorem frontier

The immediate covariance bottleneck is now closed on the controlled benchmark even when the physical relaxation time is only finitely calibrated.

The next conceptual bridge is back to the original observer-identification problem:

> Can the certified covariance uncertainty after robust innovation whitening be propagated through integration, insulation, persistence, transport, and world-tube recovery without discarding its structure in an unnecessarily large generic error bound?

A parallel technical frontier is to tighten Proposition 57 itself by replacing the conservative residual-rank trace envelope with a sharper design-specific transformed-family normalization certificate.
