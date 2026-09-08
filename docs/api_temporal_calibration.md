# Temporal calibration API

This page collects the public interfaces introduced by Propositions 41 through 52. It is intentionally separate from the older general API guide so a reader can follow the temporal-dependence theorem ladder in one place.

The mathematical assumptions are summarized here, but the complete application rules remain in the [assumption ledger](assumption_ledger.md). For physical meanings of the temporal parameters and covariance quantities, start with the [Physics Guide](physics_guide.md).

## Proposition 44: fixed nuisance projection

```python
from observer_math import (
    gaussian_ar1_projected_temporal_envelope,
    gaussian_projected_relative_covariance_error_bound,
    separable_gaussian_projected_covariance,
    temporal_nuisance_projector,
)
```

Use this layer when the target mean lies in a fixed temporal design `H` and the temporal covariance factor is known.

The projector is

\[
P_H=I-H(H^\mathsf TH)^{-1}H^\mathsf T.
\]

The estimator divides `X.T @ P_H @ X` by the exact projected normalization. See [Proposition 44](proposition_44_nuisance_projection.md).

## Proposition 45: estimated AR(1) with nuisance projection

```python
from observer_math import (
    gaussian_calibrated_ar1_projected_covariance_bound,
    gaussian_estimated_ar1_projected_covariance_bound,
    separable_gaussian_estimated_ar1_projected_covariance,
)
```

This layer combines the Proposition 43 AR(1) calibration interval with a fixed target nuisance subspace. It propagates uncertainty in both temporal dependence and the projected covariance normalization.

See [Proposition 45](proposition_45_estimated_ar1_nuisance_projection.md).

## Proposition 46: design-specific AR(1) interval geometry

```python
from observer_math import (
    gaussian_ar1_design_uniform_envelope,
    gaussian_calibrated_ar1_design_projected_covariance_bound,
    gaussian_estimated_ar1_design_projected_covariance_bound,
)
```

This result uses the actual nuisance design over the full AR(1) interval instead of replacing the design by its rank.

See [Proposition 46](proposition_46_design_specific_ar1_envelope.md).

## Proposition 47: direct matrix concentration

```python
from observer_math import (
    gaussian_projected_weighted_wishart_matrix_bound,
    gaussian_weighted_wishart_matrix_bound,
    projected_temporal_eigenvalues,
)
```

This result works with the complete nonnegative projected temporal eigenvalue profile and evaluates a direct Gaussian matrix concentration bound.

See [Proposition 47](proposition_47_weighted_wishart_matrix_chernoff.md).

## Proposition 48: interval-uniform matrix concentration

```python
from observer_math import (
    gaussian_ar1_uniform_matrix_chernoff_bound,
    gaussian_calibrated_ar1_uniform_matrix_chernoff_bound,
    separable_gaussian_calibrated_ar1_uniform_matrix_covariance,
)
```

This layer makes Proposition 47 uniform over a calibrated AR(1) interval by controlling every projected temporal eigenvalue between deterministic grid points.

See [Proposition 48](proposition_48_uniform_matrix_chernoff_ar1.md).

## Proposition 49: compact temporal covariance families

```python
from observer_math import (
    gaussian_ar1_white_noise_temporal_cover,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
```

The concentration theorem no longer depends specifically on AR(1). The caller supplies a deterministic finite cover of the temporal covariance family together with valid operator and normalization remainders.

The included two-parameter helper constructs a cover for

\[
R_{\phi,\eta}
=(1-\eta)R_\phi+\eta I.
\]

See [Proposition 49](proposition_49_compact_temporal_family.md).

## Proposition 50: observable two-parameter calibration

```python
from observer_math import (
    gaussian_ar1_white_noise_increment_norm_bounds,
    gaussian_ar1_white_noise_increment_parameter_interval,
    gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound,
    separable_gaussian_calibrated_ar1_white_noise_projected_covariance,
)
```

A typical calibration call is:

```python
bound = gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound(
    standardized_calibration_observations,
    block_dimension=4,
    block_count=1,
    nuisance_design=target_nuisance_design,
    lower_autocorrelation=0.45,
    upper_autocorrelation=0.75,
    lower_white_noise_fraction=0.0,
    upper_white_noise_fraction=0.05,
    calibration_confidence=0.9875,
    covariance_confidence=0.9875,
)
```

The calibration record and target covariance record must be independent for the reported product-confidence composition. The two records must share the same temporal parameters.

See [Proposition 50](proposition_50_calibrated_temporal_family.md).

## Proposition 51: full-likelihood e-value confidence set

Proposition 51 lives in its dedicated public module:

```python
from observer_math.evalue_temporal_family import (
    GaussianAR1WhiteNoiseEValueGrid,
    GaussianAR1WhiteNoiseEValueModel,
    gaussian_ar1_white_noise_evalue_grid,
    gaussian_ar1_white_noise_evalue_model,
    gaussian_ar1_white_noise_log_evalue,
    gaussian_helmert_contrast,
)
```

Build the observed-data e-value model:

```python
model = gaussian_ar1_white_noise_evalue_model(
    standardized_calibration_observations,
    lower_autocorrelation=0.40,
    upper_autocorrelation=0.80,
    lower_white_noise_fraction=0.0,
    upper_white_noise_fraction=0.25,
    confidence=0.9875,
    contrast_dimension=30,
    mixture_autocorrelation_grid_size=7,
    mixture_white_noise_fraction_grid_size=5,
)
```

Evaluate the exact pointwise continuum function at any admissible parameter:

```python
log_evalue = gaussian_ar1_white_noise_log_evalue(
    model,
    autocorrelation=0.60,
    white_noise_fraction=0.04,
)

accepted = log_evalue < model.log_evalue_threshold
```

The pointwise confidence set is

\[
\mathcal C_\alpha(Z)
=
\left\{
(\phi,\eta):
\log e_{\phi,\eta}(Z)<\log(1/\alpha)
\right\}.
\]

For plotting and diagnostics, evaluate the same exact function on a deterministic grid:

```python
grid = gaussian_ar1_white_noise_evalue_grid(
    model,
    autocorrelation_grid_size=33,
    white_noise_fraction_grid_size=26,
)
```

`grid.accepted_mask` describes only the evaluated grid points. It is not a certified outer cover of the full continuum set. Proposition 51's probability statement applies to the continuum set itself.

The mixture grid used to define `q` is also not a test grid. It is the support of a proper numerator density fixed before seeing the calibration data. The true parameter does not need to lie on that support.

See [Proposition 51](proposition_51_evalue_temporal_confidence_set.md) and [Experiment AK](evalue_temporal_confidence_set.json).

## Proposition 52: certified outer cover and independent target covariance

Proposition 52 lives in a dedicated public module:

```python
from observer_math.evalue_outer_cover import (
    GaussianEValueOuterCoverMatrixChernoffBound,
    GaussianEValueTemporalOuterCover,
    gaussian_ar1_white_noise_evalue_outer_cover,
    gaussian_evalue_outer_cover_matrix_chernoff_bound,
    gaussian_log_likelihood_cell_variation_bound,
    separable_gaussian_evalue_outer_cover_projected_covariance,
)
```

First turn the Proposition 51 continuum confidence set into a certified retained-cell cover:

```python
outer = gaussian_ar1_white_noise_evalue_outer_cover(
    model,
    autocorrelation_grid_size=121,
    white_noise_fraction_grid_size=61,
)
```

A cell is discarded only when a deterministic likelihood perturbation bound proves that every parameter inside the cell is rejected by the exact Proposition 51 e-value rule. Therefore the retained cells contain the complete Proposition 51 continuum confidence set.

For an independent target record with a fixed nuisance design:

```python
bound = gaussian_evalue_outer_cover_matrix_chernoff_bound(
    model,
    block_dimension=1,
    block_count=1,
    nuisance_design=target_nuisance_design,
    outer_autocorrelation_grid_size=121,
    outer_white_noise_fraction_grid_size=61,
    covariance_confidence=0.975,
)

estimate = separable_gaussian_evalue_outer_cover_projected_covariance(
    target_observations,
    target_nuisance_design,
    bound,
)
```

The target composition deliberately carries two geometric radii:

- `target_eigenvalue_covering_radius` controls the nuisance-compressed temporal spectrum used by the matrix concentration theorem;
- `target_normalization_covering_radius` controls the projected trace normalization using the raw temporal operator radius and the equal-trace family identity.

Do not substitute one radius for the other.

The reported combined confidence is the product of calibration and target covariance confidence because the target record must be independent of the calibration record and share the same true temporal parameter.

See [Proposition 52](proposition_52_certified_evalue_outer_cover.md), [Experiment AL](certified_evalue_outer_cover.json), and the [physics-first figure](certified_evalue_outer_cover.svg).

## Confidence accounting summary

| Result | Calibration and target relation | Confidence rule |
| --- | --- | --- |
| Proposition 43 | Same record may be reused | Add failure probabilities with a union bound |
| Proposition 48 | Calibration interval feeds a target covariance theorem | Follow the theorem's stated failure-budget composition |
| Proposition 50 | Calibration and target records are independent | Product lower bound is justified by conditioning and independence |
| Proposition 51 | Calibration confidence set only | One e-value at the true parameter, no parameterwise union bound |
| Proposition 52 | Certified calibration cover feeds an independent target record | Deterministic cell containment plus product confidence by record independence |

## Interpretation rule

These APIs calibrate temporal covariance and observer-like dynamical structure under explicit probabilistic assumptions. They do not measure or prove consciousness. Any later bridge to consciousness must be introduced separately under the [interpretation protocol](interpretation_protocol.md).