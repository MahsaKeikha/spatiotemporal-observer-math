# Proposition 52: certified outer cover of a continuum temporal confidence set

## Physical question

Suppose a physical process has temporal memory, and suppose a separate calibration experiment has already produced a finite-sample Proposition 51 confidence set for the admissible temporal covariance parameters.

The target experiment is independent, but it is assumed to share the same temporal-memory parameters.

The practical question is:

> **How can uncertainty about temporal memory be carried from calibration into a trustworthy covariance estimate for the target record without pretending that a plotting grid is the continuum confidence set?**

This matters because the covariance matrix is later used to compute Gaussian information quantities and candidate-boundary scores. If the temporal uncertainty is handled incorrectly, a boundary can appear more certain than the measurements justify.

Proposition 52 supplies the missing bridge. It converts the exact Proposition 51 continuum confidence set into a finite certified outer cover, then composes that cover with Proposition 49 for an independent target covariance record.

The result is conditional on the declared model family and independence assumptions. It is measurement-certification machinery. It is not a consciousness theorem.

## Measurement model

The calibration family is

\[
R_{\phi,\eta}
=
(1-\eta)R_\phi+\eta I,
\]

where

\[
R_\phi(i,j)=\phi^{|i-j|}.
\]

The parameter \(\phi\) describes persistence of the correlated temporal component. The parameter \(\eta\) describes the fraction assigned to a temporally uncorrelated component inside this effective model.

Proposition 51 first removes an arbitrary constant mean from each calibration channel with a fixed orthonormal contrast. Let \(C_{\phi,\eta}\) denote the resulting compressed temporal covariance and let

\[
e_{\phi,\eta}(Z)
=
\frac{q(Z)}{p_{\phi,\eta}(Z)}
\]

be the Proposition 51 e-value.

For confidence level \(1-\alpha\), the exact continuum confidence set is

\[
\mathcal C_\alpha(Z)
=
\left\{
(\phi,\eta):
\log e_{\phi,\eta}(Z)<\log(1/\alpha)
\right\}.
\]

Proposition 51 proves

\[
\Pr_{\phi_*,\eta_*}
\left[
(\phi_*,\eta_*)\in\mathcal C_\alpha(Z)
\right]
\ge 1-\alpha.
\]

The set is a continuum set. Evaluating the e-value on a grid is useful for visualization, but grid acceptance alone does not certify what happens between grid points.

## Fixed parameter cells

Before using the observed calibration data for exclusion, choose fixed grids

\[
\phi_1,\ldots,\phi_J,
\qquad
\eta_1,\ldots,\eta_K.
\]

They partition the declared parameter box into clipped cells around centers

\[
\theta_{jk}=(\phi_j,\eta_k).
\]

The geometry of these cells is fixed by the declared parameter box and the grid sizes. The calibration data decide only which cells can be proved impossible.

This distinction is important. The cover is data-adaptive in retention, but it is not an unconstrained data-adaptive partition.

## Local covariance motion inside a cell

Let \(B\) be a row-orthonormal compression, and write

\[
C(\phi,\eta)=B R_{\phi,\eta} B^\top.
\]

For a cell centered at \((\phi_0,\eta_0)\), the exact decomposition is

\[
C(\phi,\eta)-C(\phi_0,\eta_0)
=
(1-\eta)
B(R_\phi-R_{\phi_0})B^\top
+
(\eta-\eta_0)
B(I-R_{\phi_0})B^\top.
\]

The implementation evaluates the first AR(1) derivative after compression at the cell center. A raw second-derivative row-sum bound controls how much that derivative can change across the cell. This gives a cell-specific deterministic radius

\[
\delta_{jk}^{\mathrm{cal}}
\]

such that every parameter point inside cell \((j,k)\) satisfies

\[
\left\|
C(\phi,\eta)-C(\phi_j,\eta_k)
\right\|_2
\le
\delta_{jk}^{\mathrm{cal}}.
\]

Using local compressed geometry is materially sharper than assigning every cell the same worst-case raw temporal radius.

## A uniform likelihood variation bound

Let the compressed covariance at a cell center be \(C_0\), and define

\[
m=\lambda_{\min}(C_0).
\]

Suppose every covariance in that cell obeys

\[
\|C-C_0\|_2\le\delta<m.
\]

Let \(M\) be the number of independent calibration channels, let \(d\) be the residual contrast dimension, and let

\[
S=ZZ^\top
\]

be the residual scatter matrix.

For the Gaussian residual log likelihood,

\[
\ell(C)
=-\frac{M}{2}\log\det C
-\frac12\operatorname{tr}(C^{-1}S)
+\text{constant},
\]

the following deterministic bound holds:

\[
|\ell(C)-\ell(C_0)|
\le
\frac{Md}{2}
\left[
-\log\left(1-\frac{\delta}{m}\right)
\right]
+
\frac{\operatorname{tr}(S)}{2}
\frac{\delta}{m(m-\delta)}.
\]

Call the right-hand side \(V(C_0,\delta)\).

### Why the determinant term is controlled

Write

\[
C=C_0^{1/2}(I+E)C_0^{1/2}.
\]

Because

\[
\|E\|_2
\le
\frac{\delta}{m}<1,
\]

every eigenvalue of \(I+E\) lies in

\[
\left[1-\frac{\delta}{m},
1+\frac{\delta}{m}\right].
\]

Therefore

\[
|\log\det C-\log\det C_0|
\le
 d
\left[-\log\left(1-\frac{\delta}{m}\right)\right].
\]

Multiplying by \(M/2\) gives the determinant contribution.

### Why the inverse term is controlled

The resolvent identity gives

\[
C^{-1}-C_0^{-1}
=
C^{-1}(C_0-C)C_0^{-1}.
\]

Since

\[
\lambda_{\min}(C)
\ge m-\delta,
\]

we have

\[
\|C^{-1}-C_0^{-1}\|_2
\le
\frac{\delta}{m(m-\delta)}.
\]

Because \(S\) is positive semidefinite,

\[
\left|
\operatorname{tr}
\left[(C^{-1}-C_0^{-1})S\right]
\right|
\le
\operatorname{tr}(S)
\|C^{-1}-C_0^{-1}\|_2.
\]

This gives the inverse contribution.

## Certified cell exclusion

At a cell center \(\theta_{jk}\), compute the exact Proposition 51 log e-value

\[
L_{jk}=\log e_{\theta_{jk}}(Z).
\]

Let \(V_{jk}\) be the likelihood variation bound for that cell.

The cell is excluded only if

\[
L_{jk}-V_{jk}
\ge
\log(1/\alpha).
\]

For any point \(\theta\) inside that cell,

\[
\log e_\theta(Z)
\ge
L_{jk}-V_{jk},
\]

so every point in an excluded cell lies outside the Proposition 51 confidence set.

Therefore the union of retained cells, denoted \(\mathcal O_\alpha(Z)\), satisfies the deterministic containment

\[
\boxed{
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z)
}.
\]

This is the central Proposition 52 outer-cover statement.

The numerical grid is no longer merely a visualization. The retained cells form a certified outer representation of the complete continuum confidence set.

## Consequence for the true temporal parameter

On the Proposition 51 calibration event,

\[
(\phi_*,\eta_*)
\in
\mathcal C_\alpha(Z).
\]

Since

\[
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z),
\]

the true temporal parameter belongs to one retained Proposition 52 cell on the same event.

Thus

\[
\Pr
\left[
(\phi_*,\eta_*)
\in
\mathcal O_\alpha(Z)
\right]
\ge 1-\alpha.
\]

No new stochastic union bound over cells is required. The cells are part of a deterministic containment argument applied after the Proposition 51 confidence set has been constructed.

## Target measurement model

Now consider an independent target record

\[
X=HB+R_{\phi_*,\eta_*}^{1/2}Y\Sigma^{1/2},
\]

where

- \(H\) is a fixed declared nuisance design;
- \(B\) contains unknown nuisance coefficients;
- \(R_{\phi_*,\eta_*}\) is the same temporal covariance family member governing the calibration and target records;
- \(Y\) has independent standard Gaussian entries;
- \(\Sigma\) is the spatial covariance to estimate.

Let

\[
P_H=I-H(H^\top H)^{-1}H^\top.
\]

The nuisance contribution disappears exactly because

\[
P_HH=0.
\]

The target covariance estimator is

\[
\widehat\Sigma
=
\frac{X^\top P_H X}{d_{\mathrm{ref}}},
\]

where \(d_{\mathrm{ref}}\) is the reference projected normalization supplied by the Proposition 49 family bound.

## Two target-cover radii are required

The target composition uses two different geometric controls.

### Eigenvalue-cover radius

Let \(U\) span the orthogonal complement of the nuisance design. The matrix probability theorem depends on the compressed temporal spectrum

\[
U^\top R U.
\]

For each retained parameter cell, Proposition 52 computes a target compressed radius. The final eigenvalue-cover radius is

\[
\delta_{\mathrm{eig}}
=
\max_{\text{retained cells}}
\left\|
U^\top(R-R_j)U
\right\|_2
\]

under the cellwise deterministic bounds.

### Normalization-cover radius

The projected normalization is

\[
d(R)=\operatorname{tr}(P_HR).
\]

Every covariance in the declared temporal family has trace equal to the target sample count. Therefore for \(\Delta R=R-R_j\),

\[
\operatorname{tr}(\Delta R)=0.
\]

Writing

\[
P_H=I-Q_H,
\]

where \(Q_H\) is the projector onto the nuisance space and has rank \(q\),

\[
\operatorname{tr}(P_H\Delta R)
=-\operatorname{tr}(Q_H\Delta R).
\]

Hence

\[
\left|
\operatorname{tr}(P_H\Delta R)
\right|
\le
q\|\Delta R\|_2.
\]

The normalization cover therefore uses

\[
\delta_{\mathrm{norm}}
=
q
\max_{\text{retained cells}}
\|R-R_j\|_2,
\]

not the compressed eigenvalue radius.

Keeping these two radii separate is necessary. The compressed radius is sharper for projected eigenvalue geometry, while the trace-normalization proof requires the raw temporal operator radius.

## Composition with Proposition 49

Condition on the calibration record.

Once the retained cells are observed, their centers and deterministic radii are fixed. On the calibration coverage event, the true target temporal covariance lies in one of those retained cells.

Proposition 49 can therefore be applied conditionally to the independent target record using

- retained temporal covariance centers as the finite cover;
- \(\delta_{\mathrm{eig}}\) for projected eigenvalue motion;
- \(\delta_{\mathrm{norm}}\) for projected normalization motion.

If Proposition 49 supplies target covariance confidence \(1-\beta\), then conditional on a valid calibration cover,

\[
\Pr
\left[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
\le
\varepsilon_{52}
\;\middle|\;
\text{calibration record}
\right]
\ge
1-\beta.
\]

Because the target record is independent of the calibration record, the joint success probability is at least

\[
\boxed{
(1-\alpha)(1-\beta)
}.
\]

This product form uses record independence. It does not assume independence between individual statistics computed inside the same calibration record.

## Proposition 52 statement

Under the assumptions listed below:

1. the exact Proposition 51 continuum confidence set is contained in the retained Proposition 52 cells;
2. the true temporal parameter belongs to the retained outer cover with probability at least the Proposition 51 calibration confidence;
3. conditional on the calibration record and its coverage event, Proposition 49 gives a target covariance certificate over the retained family;
4. for an independent target record, the final calibration-plus-covariance confidence is at least the product of the two confidence levels.

The implemented bound returns

\[
\varepsilon_{52}
=
\texttt{covariance\_relative\_error}
\]

for the relative operator error

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2.
\]

## Physical interpretation

The proposition can be read without the cell geometry language.

A separate calibration experiment tells us which temporal-memory models remain physically compatible with the observed fluctuations.

Instead of choosing one fitted memory parameter and pretending it is exact, Proposition 52 carries the full finite-sample uncertainty set forward.

It then asks whether every still-compatible temporal model leads to a target covariance close enough to the finite cover used by the matrix concentration theorem.

If the answer is yes, the target covariance estimate receives one confidence statement that already accounts for uncertainty in temporal memory and nuisance drift.

This is useful because downstream Gaussian information calculations depend on covariance geometry. The theorem prevents a narrow fitted temporal model from creating false precision in later boundary scores.

## Experiment AL

Experiment AL uses a controlled two-parameter temporal family with

\[
\phi_*=0.50,
\qquad
\eta_*=0.01,
\]

a calibration record of 48 time samples across 256 independent channels, and the declared box

\[
\phi\in[0.30,0.70],
\qquad
\eta\in[0,0.05].
\]

A `121 x 61` fixed outer-cover grid contains 7,381 cells.

For the committed deterministic calibration record:

- 5,325 cells are retained;
- 2,056 cells are certified excluded;
- the retained fraction is about 0.72145;
- the target eigenvalue-cover radius is about 0.031704;
- the target normalization-cover radius is about 0.070386;
- the combined confidence lower bound is 0.950625;
- the final target relative covariance radius is about 0.899816, which is below one.

The target visibility study uses 128 independently generated target records under the controlled true parameter. All displayed errors lie below the theorem radius, with maximum observed relative error about 0.543631.

Those target trials are a visibility check. They are not the proof of coverage. The proof is the Proposition 51 e-value guarantee, deterministic cell containment, and conditional Proposition 49 matrix concentration for the independent target record.

## Why a radius below one is useful

A bound

\[
\left\|
\Sigma^{-1/2}
(\widehat\Sigma-\Sigma)
\Sigma^{-1/2}
\right\|_2
<1
\]

keeps the estimated covariance inside a perturbative positive-definite regime relative to the true covariance geometry.

That makes later inverse-covariance and Gaussian information perturbation arguments available.

The number one is a mathematical perturbation threshold. It is not a physical phase transition.

## Assumptions

The current proposition requires all of the following.

1. **Correct temporal family.** The calibration and target temporal covariances belong to the declared AR(1) plus white-noise family and declared parameter box.
2. **Shared temporal parameter.** Calibration and target records share the same true \((\phi,\eta)\).
3. **Independent records.** The target record is independent of the calibration record for the product confidence composition.
4. **Gaussian calibration model.** Proposition 51 uses the stated residual Gaussian likelihood.
5. **Independent calibration channels.** The likelihood model treats the calibration channels as independent conditional on the shared temporal covariance.
6. **Fixed contrast.** The calibration mean-removal contrast is declared independently of the stochastic observations.
7. **Positive compressed covariance.** Cell-center compressed covariance matrices must remain positive definite, and the cell radius must remain below the relevant minimum eigenvalue for a finite likelihood variation bound.
8. **Fixed target nuisance design.** The columns of \(H\) are declared before using the target stochastic record, unless a separate adaptive-selection theorem is supplied.
9. **Gaussian separable target model.** Proposition 49 is applied under its stated separable Gaussian target assumptions.

## Failure conditions and diagnostics

A certified numerical result is meaningful only while the physical measurement model remains defensible.

Useful failure checks include:

- residual temporal autocorrelation inconsistent with the declared family;
- evidence for oscillatory or multi-timescale memory that an AR(1) kernel cannot represent;
- cross-channel dependence in the calibration record beyond the independence model;
- time-varying temporal parameters between calibration and target experiments;
- nuisance modes selected adaptively from the same target noise without correction;
- non-Gaussian residuals severe enough to invalidate the likelihood or matrix concentration model;
- target covariance structure that is not separable into the declared temporal and spatial factors.

A failed diagnostic should narrow the scope of the theorem or motivate a richer model. It should not be hidden by making the parameter box arbitrarily wide.

## What this proposition does not establish

Proposition 52 does not identify a physical observer boundary by itself.

It certifies one statistical ingredient used later by the moving-boundary pipeline: the covariance of a target fluctuating record when temporal memory and nuisance trends are uncertain.

It does not establish consciousness, subjective experience, agency, semantic information, thermodynamic closure, or a unique physical subsystem boundary.

Any future consciousness interpretation remains a separate bridge problem under the repository's [interpretation protocol](interpretation_protocol.md).

## Reproduction

Run

```bash
python examples/certified_evalue_outer_cover.py
```

The implementation is in

```text
src/observer_math/evalue_outer_cover.py
```

Claim-level tests are in

```text
tests/test_evalue_outer_cover.py
```

For the physical meaning of the covariance, temporal memory, nuisance projection, and theorem radius, see the [Physics Guide](physics_guide.md).