# Temporal calibration API

This page collects the public interfaces introduced by Propositions 41 through 53. It is intentionally separate from the older general API guide so a reader can follow the temporal-dependence theorem ladder in one place.

The mathematical assumptions are summarized here, but the complete application rules remain in the [Assumption Ledger](assumption_ledger.md). For physical meanings of the temporal parameters and covariance quantities, start with the [Physics Guide](physics_guide.md).

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

See [Proposition 44](proposition_44_nuisance_projection.md).

## Proposition 45: estimated AR(1) with nuisance projection

```python
from observer_math import (
    gaussian_calibrated_ar1_projected_covariance_bound,
    gaussian_estimated_ar1_projected_covariance_bound,
    separable_gaussian_estimated_ar1_projected_covariance,
)
```

This layer combines the Proposition 43 AR(1) calibration interval with a fixed target nuisance subspace.

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

For plotting and diagnostics, evaluate the same exact function on a deterministic grid. The evaluated mask is only a view of the continuum function, not a certified outer cover.

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

A cell is discarded only when a deterministic likelihood perturbation bound proves that every parameter inside the cell is rejected by the exact Proposition 51 e-value rule.

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
```

The target composition deliberately carries separate eigenvalue and normalization cover radii. Do not substitute one for the other.

See [Proposition 52](proposition_52_certified_evalue_outer_cover.md), [Experiment AL](certified_evalue_outer_cover.json), and the [physics-first figure](certified_evalue_outer_cover.svg).

## Proposition 53: physical relaxation time, sampling consistency, and exact Markov structure

Proposition 53 lives in the dedicated public module `observer_math.physical_relaxation`.

```python
from observer_math.physical_relaxation import (
    ExponentialRelaxationMarkovFactorization,
    ExponentialRelaxationTemporalCover,
    GaussianRelaxationTimeMatrixChernoffBound,
    exponential_relaxation_covariance,
    exponential_relaxation_markov_factorization,
    exponential_relaxation_operator_lipschitz_bound,
    exponential_relaxation_temporal_cover,
    gaussian_relaxation_time_matrix_chernoff_bound,
    relaxation_autocorrelation,
    relaxation_time_from_autocorrelation,
    uniform_exponential_relaxation_covariance,
)
```

### Convert between physical time and discrete correlation

```python
tau_seconds = 0.8
sample_interval_seconds = 0.05

phi = relaxation_autocorrelation(
    sample_interval_seconds,
    tau_seconds,
)

recovered_tau = relaxation_time_from_autocorrelation(
    phi,
    sample_interval_seconds,
)
```

Under the model,

\[
\phi_{\Delta t}=e^{-\Delta t/\tau},
\qquad
\tau=-\frac{\Delta t}{\log\phi_{\Delta t}}.
\]

### Build covariance on irregular physical timestamps

```python
sample_times = np.array([0.0, 0.04, 0.11, 0.19, 0.33, 0.52, 0.76])
R = exponential_relaxation_covariance(
    sample_times,
    relaxation_time=0.8,
)
```

The covariance uses actual elapsed time:

\[
R_{ij}=\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

### Factor an irregular record into exact local innovations

```python
factor = exponential_relaxation_markov_factorization(
    sample_times,
    relaxation_time=0.8,
)

alpha = factor.step_correlations
innovation_variances = factor.innovation_variances
W = factor.whitening_matrix
Q = factor.precision_matrix
logdet = factor.covariance_log_determinant
```

For every adjacent gap,

\[
\alpha_i
=
\exp\left(-\frac{t_{i+1}-t_i}{\tau}\right).
\]

The returned object satisfies the exact identities

\[
W R_\tau W^\mathsf T=I,
\qquad
Q=R_\tau^{-1}=W^\mathsf T W,
\]

with tridiagonal `Q`, and

\[
\log\det R_\tau
=
\sum_i\log(1-\alpha_i^2).
\]

For a separable multivariate record with temporal factor \(R_\tau\), apply `W` along the temporal axis to obtain independent temporal innovations while preserving the spatial covariance factor.

The exact whitener is also a model diagnostic: if a fitted \(\tau\) is appropriate, the transformed residual record should not retain systematic temporal dependence under the declared Gaussian model.

### Build a certified relaxation-time family cover

```python
cover = exponential_relaxation_temporal_cover(
    sample_times,
    nuisance_design,
    lower_relaxation_time=0.55,
    upper_relaxation_time=1.05,
    relaxation_time_grid_size=33,
)
```

The analytic operator radius covers every \(\tau\) in the declared interval, including values between grid points.

### Compose with Proposition 49

```python
bound = gaussian_relaxation_time_matrix_chernoff_bound(
    sample_times,
    nuisance_design,
    block_dimension=4,
    block_count=1,
    lower_relaxation_time=0.55,
    upper_relaxation_time=1.05,
    relaxation_time_grid_size=33,
    confidence=0.975,
)
```

The deterministic \(\tau\)-grid is geometry, not a collection of stochastic tests. Refining it changes approximation tightness, not the confidence accounting.

See [Proposition 53](proposition_53_physical_relaxation_time.md), [Experiment AM](physical_relaxation_sampling.json), the [sampling-physics figure](physical_relaxation_sampling.svg), and the [irregular-grid Markov figure](physical_relaxation_markov.svg).

## Confidence accounting summary

| Result | Calibration and target relation | Confidence rule |
| --- | --- | --- |
| Proposition 43 | Same record may be reused | Add failure probabilities with a union bound |
| Proposition 48 | Calibration interval feeds a target covariance theorem | Follow the theorem's stated failure-budget composition |
| Proposition 50 | Calibration and target records are independent | Product lower bound is justified by conditioning and independence |
| Proposition 51 | Calibration confidence set only | One e-value at the true parameter, no parameterwise union bound |
| Proposition 52 | Certified calibration cover feeds an independent target record | Deterministic cell containment plus product confidence by record independence |
| Proposition 53 | Declared physical \(\tau\)-interval represented by a deterministic cover | No probability penalty for cover points; Proposition 49 supplies the covariance confidence statement |

## Interpretation rule

These APIs calibrate temporal covariance and observer-like dynamical structure under explicit probabilistic assumptions. They do not measure or prove consciousness. Any later bridge to consciousness must be introduced separately under the [Interpretation Protocol](interpretation_protocol.md).

## Physical-time irregular calibration API : Proposition 53B

The `observer_math.irregular_relaxation_evalue` module exposes exact irregular-time likelihood, continuum e-value evaluation, cell-local certified outer covers, and independent target-family composition. The principal public symbols are `GaussianIrregularRelaxationEValueModel`, `GaussianIrregularRelaxationEValueGrid`, `GaussianIrregularRelaxationEValueOuterCover`, `GaussianIrregularRelaxationTargetBound`, `gaussian_irregular_relaxation_evalue_model`, `gaussian_irregular_relaxation_log_evalue`, `gaussian_irregular_relaxation_evalue_grid`, `gaussian_irregular_relaxation_evalue_outer_cover`, and `gaussian_irregular_relaxation_target_matrix_chernoff_bound`. They are also exported from the package root in release 0.42.0.


## Proposition 54 two-scale irregular relaxation cover

Public functions:

- `gaussian_irregular_relaxation_two_scale_target_bound`
- `gaussian_optimized_irregular_relaxation_two_scale_target_bound`

Public result types:

- `GaussianIrregularRelaxationTwoScaleTargetBound`
- `GaussianOptimizedIrregularRelaxationTwoScaleTargetBound`

The first function certifies a fine calibration outer cover and then covers its retained physical-time interval with a separately chosen target grid. The second selects the target grid size from a declared candidate set using calibration-derived geometry and target design information only. No target observations are used for that selection.

## Proposition 55: quadratic relaxation calibration

Public package-root imports:

```python
from observer_math import (
    GaussianIrregularRelaxationQuadraticOuterCover,
    GaussianIrregularRelaxationQuadraticTargetBound,
    gaussian_irregular_relaxation_log_evalue_derivative,
    gaussian_irregular_relaxation_log_evalue_second_derivative_bound,
    gaussian_irregular_relaxation_quadratic_outer_cover,
    gaussian_irregular_relaxation_quadratic_target_bound,
)
```

The quadratic outer cover is a deterministic enclosure of the already valid Proposition 53B continuum e-value set. It uses the exact observed-data derivative at each cell center and a rigorous cell-local second-derivative bound. It does not consume an additional probability budget.

The quadratic target helper composes the retained interval with the existing target covariance machinery. Experiment AP shows that this improves the target radius but does not remove the known-tau oracle floor of the current concentration theorem.
