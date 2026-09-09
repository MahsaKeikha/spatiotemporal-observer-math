# Release 0.43.0 research record

## Proposition 54 and Experiment AO

Release 0.43.0 adds a second-order physical-time calibration layer and a calibration-derived reference-whitening target certificate.

The release extends the irregular-time exponential-relaxation program without changing the finite-sample e-value coverage theorem of Proposition 53B.

## Main theorem

Proposition 54 has two linked parts.

First, it replaces the first-derivative cell certificate used by Proposition 53B with a second-order interpolation certificate based on a deterministic cellwise bound on the exact irregular-time Gaussian log-likelihood curvature. For each fixed cell, every point of the exact continuum e-value confidence set remains inside the retained cell union. The finite-sample calibration confidence is therefore unchanged.

Second, it chooses a reference relaxation time from the calibration cover only and applies the exact Proposition 53A innovation whitener to the independent target timestamp grid. The transformed nuisance design is fixed by the same calibration-derived whitener. Local first and second derivatives of the transformed temporal covariance then provide a compact-family cover for Proposition 49.

## Experiment AO

The controlled configuration reuses the physical-time problem of Experiment AN:

- true relaxation time: `0.78 s`;
- declared calibration interval: `[0.40, 1.25] s`;
- 96 independent calibration channels;
- 32 irregular calibration samples;
- 160 calibration cells;
- 120 irregular target samples;
- rank-2 affine target nuisance design;
- calibration confidence: `0.975`;
- covariance confidence: `0.975`;
- combined confidence: `0.950625`.

The diagnostic continuum e-value interval is approximately

`[0.69155, 0.84455] s`.

The Proposition 53B first-order outer cover retains 115 cells. Proposition 54 retains 31 cells, with certified extremes

`[0.686875, 0.8515625] s`.

The calibration-derived reference relaxation time is

`0.76921875 s`.

The reference whitener satisfies its exact identity to about `1.9e-15` in the committed numerical record.

The final certified target values are:

| Quantity | Experiment AO |
| --- | ---: |
| temporal cover radius | `0.008495864441166266` |
| normalization cover radius | `0.46699818384400943` |
| projected degrees lower bound | `107.18510598216754` |
| projected degrees upper bound | `131.05861668414013` |
| projected spectral norm bound | `1.1239110530935237` |
| oracle relative error inside Proposition 49 | `0.5360349382281793` |
| final relative covariance radius | **`0.6899552435608669`** |

Thus the same controlled target geometry that had a raw relative covariance radius of `3.155489544511118` in Experiment AN now enters the subunit regime:

\[
\boxed{0.6899552435608669<1}.
\]

## Visibility checks

The deterministic dense retained-family check records:

- maximum transformed temporal operator error: `0.004307444510228646`;
- operator error divided by its certificate: `0.5070048539566085`;
- maximum projected-normalization error: `0.46697971324957166`;
- normalization error divided by its certificate: `0.9999604482520987`.

These checks are diagnostics, not the proof. The guarantee comes from the Proposition 53B e-value event, Proposition 54 deterministic continuum containment, the reference-whitened Taylor cover, and Proposition 49 target concentration.

## Reproducibility surface

Release 0.43.0 includes:

- theorem implementation: `src/observer_math/second_order_relaxation.py`;
- six claim-level tests: `tests/test_second_order_relaxation.py`;
- full proof page: `docs/proposition_54_second_order_reference_whitening.md`;
- Experiment AO script: `examples/second_order_reference_whitening.py`;
- machine-readable record: `docs/second_order_reference_whitening.json`;
- deterministic publication renderer: `examples/render_second_order_reference_whitening.py`;
- publication figure: `docs/second_order_reference_whitening.svg`.

## Verified research-state target

After release integration and final CI, the intended public record is:

- **54 propositions**;
- **41 reproducible experiments, A-Z and AA-AO**;
- **29 scientific result figures**;
- **201 claim-level tests**;
- Python 3.10, 3.11, and 3.12 CI;
- research-software version **0.43.0**.

These counts should be treated as verified only after the exact release head and merged `main` both pass the full CI matrix.

## Scope

This release remains conditional on independent standardized Gaussian calibration channels, one exponential relaxation time, a fixed target nuisance design, separable Gaussian target fluctuations, and calibration independence from the target record.

It does not establish that a real system has one exponential timescale, does not identify an observer boundary by itself, and does not establish consciousness.
