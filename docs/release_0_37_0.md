# Release 0.37.0: compact temporal-family matrix concentration

Release 0.37.0 advances the dependent-Gaussian covariance frontier from a calibrated one-parameter AR(1) interval to arbitrary compact temporal covariance families represented by deterministic finite covers.

## Proposition 49

Proposition 49 isolates the direct matrix-concentration mechanism from temporal-family parameterization.

For a target model

\[
X=HB+R^{1/2}Z\Sigma^{1/2},
\]

let `U` span the orthogonal complement of the fixed nuisance design. The theorem assumes a finite cover such that every admissible temporal covariance has a compressed matrix `U.T @ R @ U` within a declared operator radius of a cover point and a projected normalization within a declared scalar radius.

Weyl's inequality controls every ordered projected temporal eigenvalue. The exact Gaussian matrix-mgf factors developed in Proposition 47 and shown monotone in Proposition 48 then turn the inflated finite spectra into one family-wide matrix Chernoff bound.

The finite cover does not consume a probability union bound. It is deterministic geometry used to construct the worst-case mgf before the concentration inequality is applied.

## Two-parameter corollary

The release includes a rigorous product-grid cover for

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I.
\]

This adds a white-noise fraction `eta` to the AR(1) coefficient `phi` while retaining unit marginal temporal variance. Analytic coordinatewise Lipschitz bounds certify both the projected spectral covering radius and the projected normalization radius.

## Experiment AI

Experiment AI fixes `N=400`, spatial dimension four, one covariance block, an affine nuisance design, 97.5% covariance confidence, `phi in [0.45, 0.72]`, and `eta in [0, 0.05]`.

| Cover | Cover points | Proposition 49 | Sphere-net family | Reduction |
| --- | ---: | ---: | ---: | ---: |
| `5 x 3` | 15 | 1.104 | 3.002 | 63.2% |
| `9 x 5` | 45 | 0.957 | 2.572 | 62.8% |
| `17 x 9` | 153 | 0.891 | 2.358 | 62.2% |

The same temporal family crosses from an unusable relative covariance radius above one to a usable radius below one by refining only the deterministic cover geometry. Sample count, confidence, spatial dimension, and parameter rectangle remain fixed.

Two 96-trial seeded target-record checks with a large unknown affine mean produced 192 of 192 recorded covariance errors inside the final `0.891` radius. These trials are scale checks, not the proof.

## Verification

Five Proposition 49 claim-level tests check:

1. exact reduction to Proposition 47 for a single zero-radius cover point;
2. dense containment of the two-parameter family by the analytic product cover;
3. domination of dense exact known-parameter Proposition 47 bounds;
4. improvement over the corresponding sphere-net family certificate;
5. monotonic degradation when the declared cover radii are widened.

The release candidate contains 49 propositions, 35 reproducible experiments, 22 committed scientific figures, and 161 claim-level tests.

## Reproducibility record

- proof: `docs/proposition_49_compact_temporal_family.md`
- API and assumptions: `docs/proposition_49_api_and_assumptions.md`
- implementation: `src/observer_math/compact_temporal_family.py`
- tests: `tests/test_compact_temporal_family.py`
- experiment: `examples/compact_temporal_family.py`
- machine-readable results: `docs/compact_temporal_family.json`
- publication figure: `docs/compact_temporal_family.svg`
- deterministic figure renderer: `examples/render_compact_temporal_family.py`

## Next frontier

Proposition 49 assumes a deterministic temporal-family cover is valid independently of the target covariance record. The next statistical target is an observable finite-sample confidence set for a multi-parameter or nonparametric temporal covariance family, with its calibration failure probability composed explicitly with the Proposition 49 covariance event.
