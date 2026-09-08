# Proposition 49 API and assumption audit

This page is the implementation-facing audit companion to [Proposition 49](proposition_49_compact_temporal_family.md). It separates the reusable concentration API from the model-specific cover construction and states the assumptions that must be justified before the result is applied.

## Public module

The Proposition 49 API is intentionally isolated in

```python
observer_math.compact_temporal_family
```

so the generic finite-cover theorem does not depend on a particular temporal parameterization.

### Generic compact-family certificate

```python
from observer_math.compact_temporal_family import (
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)

bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
    block_dimension=4,
    block_count=1,
    temporal_covariance_grid=cover_matrices,
    nuisance_design=H,
    eigenvalue_covering_radius=delta_lambda,
    normalization_covering_radius=delta_d,
    confidence=0.975,
)

print(bound.covariance_relative_error)
```

The caller supplies a finite collection of temporal covariance matrices and two deterministic continuum radii. The function compresses each cover point to the nuisance-orthogonal subspace, computes the full projected eigenvalue spectra, inflates those spectra by the declared operator covering radius, and evaluates the direct Gaussian matrix Chernoff envelope.

The returned `GaussianCompactTemporalFamilyMatrixChernoffBound` exposes the cover size, nuisance rank, projected temporal rank, normalization interval, spectral cap, oracle-normalized upper and lower deviations, final normalization ratios, final relative covariance radius, and the selected dimensionless Chernoff parameters.

### Two-parameter AR(1) plus white-noise cover

```python
from observer_math.compact_temporal_family import (
    gaussian_ar1_white_noise_temporal_cover,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)

cover = gaussian_ar1_white_noise_temporal_cover(
    H,
    lower_autocorrelation=0.45,
    upper_autocorrelation=0.72,
    lower_white_noise_fraction=0.00,
    upper_white_noise_fraction=0.05,
    autocorrelation_grid_size=17,
    white_noise_fraction_grid_size=9,
)

bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
    4,
    1,
    cover.temporal_covariance_grid,
    H,
    eigenvalue_covering_radius=cover.projected_eigenvalue_covering_radius,
    normalization_covering_radius=cover.projected_normalization_covering_radius,
    confidence=0.975,
)
```

The helper certifies the product-grid family

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I
\]

using analytic coordinatewise operator Lipschitz bounds. The helper returns both the raw temporal operator covering radius and the projected operator and normalization radii supplied to the generic theorem.

## Assumption ledger for Proposition 49

| Assumption | Why it is required | Failure mode |
| --- | --- | --- |
| The target record is exactly Gaussian with covariance separable as `R tensor Sigma` after the declared nuisance mean is removed | Proposition 47's weighted Gaussian Wishart representation and exact matrix mgf | A non-Gaussian or nonseparable target can have different matrix tails |
| The nuisance design is fixed before inspecting the target record and has full column rank below `N` | Makes the orthogonal projection deterministic and preserves positive residual rank | Adaptive nuisance selection can invalidate the stated concentration event |
| Every temporal cover matrix is finite, symmetric, and positive semidefinite | Required for a valid temporal covariance and nonnegative projected eigenvalues | The matrix-mgf monotonicity argument no longer represents a covariance model |
| Every admissible compressed covariance `U.T @ R @ U` lies within `delta_lambda` in operator norm of at least one compressed cover point | This is the Weyl bridge from a finite cover to the complete family | An understated operator radius can leave admissible eigenvalue profiles outside the mgf envelope |
| Every admissible projected normalization lies within `delta_d` of the corresponding cover-point normalization | Controls the unknown denominator of the observable covariance estimator | An understated normalization radius can make the final relative error too small |
| The resulting lower normalization `d_-` is strictly positive | The projected covariance estimator divides by this information scale | A nonpositive lower bound makes the certificate vacuous |
| The cover, its radii, the block family, and the confidence level are declared independently of the target covariance realization | Keeps Proposition 49 a fixed-family concentration statement | Data-dependent tuning requires separate calibration or sample splitting |
| The finite Chernoff theta sets are deterministic and remain inside their admissible domains | Each candidate theta must itself define a valid Chernoff inequality | An inadmissible upper-tail theta can cross the Gaussian mgf singularity |

## Additional assumptions for the Experiment AI corollary

The analytic helper `gaussian_ar1_white_noise_temporal_cover` additionally assumes:

- `0 <= phi_lower <= phi_upper < 1`;
- `0 <= eta_lower <= eta_upper <= 1`;
- the temporal family is exactly `(1 - eta) R_phi + eta I` throughout the declared rectangle;
- the product-grid spacings are those returned by the helper;
- the row-sum derivative bounds used by the helper dominate the complete parameter rectangle.

The helper is a deterministic geometry result. It does not estimate `phi` or `eta` from the target record.

## Probability accounting

The finite cover does **not** introduce a union bound over cover points. For each admissible temporal covariance, the deterministic cover and Weyl's inequality dominate its complete projected spectrum by an inflated cover spectrum. The maximum over cover spectra is taken before the matrix probability inequality is applied.

Consequently, refining the deterministic cover can improve the covariance radius without paying an additional failure probability proportional to the number of cover points.

If a future procedure estimates a random temporal-family confidence set from data, its calibration failure probability must be composed separately with the Proposition 49 covariance failure probability. That composition is the immediate next statistical frontier.

## Reproduce Experiment AI

The numerical record is regenerated with

```bash
python examples/compact_temporal_family.py
```

The committed publication SVG is rendered deterministically from the JSON record with

```bash
python examples/render_compact_temporal_family.py
```

The theorem checks are

```bash
pytest tests/test_compact_temporal_family.py
```

See [Experiment AI JSON](compact_temporal_family.json), the [publication figure](compact_temporal_family.svg), and the [proof](proposition_49_compact_temporal_family.md).
