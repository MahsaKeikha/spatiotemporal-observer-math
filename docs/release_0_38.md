# Release 0.38.0

Release date: 2026-09-08

## Main result

Release 0.38.0 adds Proposition 50, which learns a finite-sample confidence rectangle for the two-parameter temporal covariance family

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I
\]

from independent standardized Gaussian calibration channels, then composes that random rectangle with Proposition 49 for an independent target record.

The calibration uses lag-1 and lag-2 increment energies. Constant channel means cancel exactly. The proof derives increment-specific spectral bounds rather than applying a generic raw-process spectral penalty.

## Numerical record

Experiment AJ holds the target sample count, dimension, nuisance design, confidence split, and Proposition 49 cover resolution fixed while increasing only the number of independent calibration channels.

| Calibration channels | Calibrated `phi` interval | Proposition 50 covariance radius |
| ---: | --- | ---: |
| 16 | `[0.487, 0.750]` | `1.117` |
| 32 | `[0.504, 0.737]` | `1.054` |
| 64 | `[0.517, 0.679]` | `0.871` |
| 128 | `[0.545, 0.659]` | `0.814` |
| 256 | `[0.559, 0.640]` | `0.772` |

The full declared-family Proposition 49 radius for the same target problem is `1.142`. The calibrated certificate crosses below one at 64 calibration channels.

At 64 channels, the increment-specific lag-1 correlation error radius is about `0.021`, compared with about `0.091` under a generic spectral-product bound. The lag-2 comparison is about `0.035` versus `0.108`.

Two independent 96-trial target-record visibility checks recorded maximum relative covariance errors `0.438` and `0.409`, below the corresponding theorem radii `0.871` and `0.772`. These simulations show numerical scale; they are not the proof.

## Research discipline

This release also adds an explicit [observer-to-consciousness interpretation protocol](interpretation_protocol.md). It separates proved observer-structure mathematics from any future consciousness bridge hypothesis and lists the additional obligations such a bridge would need to meet: identifiability, representation invariance, causal discriminability, temporal identity, counterfactual robustness, external empirical anchoring, falsifiability, and control of competing explanations.

No result in this release is presented as a proof or measurement of phenomenal consciousness.

## Software and documentation

- adds `src/observer_math/calibrated_temporal_family.py`;
- adds five Proposition 50 claim-level tests;
- exposes both Proposition 49 and Proposition 50 APIs at the package root;
- adds Experiment AJ, committed JSON results, a publication SVG, and deterministic renderer;
- adds the complete Proposition 50 proof page;
- records release version `0.38.0` in package and citation metadata.

## Verification target

The release candidate contains 50 propositions, 36 experiments through AJ, 23 committed scientific figures, and 166 claim-level tests before final release integration. CI is required on Python 3.10, 3.11, and 3.12 before merge.
