# Proposition 55: quadratic finite-sample relaxation calibration

## Physical question

A physical relaxation time \(\tau\) is inferred from an irregularly sampled calibration experiment. Proposition 53B gives a valid continuum confidence set for \(\tau\), and Proposition 54 separates calibration resolution from target-cover resolution.

The remaining calibration question is:

> Can the observed local shape of the calibration likelihood certify a much tighter physical-time interval without changing the finite-sample confidence statement?

Proposition 55 answers yes for the declared Gaussian exponential-relaxation model.

The theorem uses the exact observed-data slope of the continuum log e-value at each calibration-cell center together with a rigorous cell-local curvature bound. Taylor's theorem then gives a quadratic lower enclosure over the complete cell. A cell is discarded only when that lower enclosure proves that every \(\tau\) inside the cell is rejected by the original Proposition 53B continuum test.

The probability statement is unchanged. Only the deterministic representation of the already valid confidence set becomes tighter.

---

# 1. Measurement model

Let the calibration channels be independent standardized realizations observed at increasing physical times

\[
t_1<\cdots<t_N.
\]

For a candidate physical relaxation time \(\tau>0\), the exponential kernel is

\[
R_\tau(i,j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

Equivalently, adjacent observations satisfy the exact irregular-grid transition law

\[
X_{i+1}
=
\alpha_i(\tau)X_i
+
\sqrt{1-\alpha_i(\tau)^2}\,\varepsilon_i,
\qquad
\alpha_i(\tau)
=
\exp\left(-\frac{t_{i+1}-t_i}{\tau}\right).
\]

Proposition 53B defines a proper continuum e-value

\[
e_\tau(Z)
=
\frac{q(Z)}{p_\tau(Z)},
\]

where \(q\) is fixed before observing the calibration record. For the true \(\tau_*\),

\[
\mathbb E_{\tau_*}[e_{\tau_*}(Z)]=1.
\]

Therefore the continuum confidence set

\[
\mathcal C_\alpha(Z)
=
\left\{
\tau:
\log e_\tau(Z)<\log(1/\alpha)
\right\}
\]

has finite-sample coverage at least \(1-\alpha\).

Proposition 55 does not alter this construction.

---

# 2. Exact observed-data slope

After the record is observed, the mixture numerator \(q(Z)\) is constant as a function of candidate \(\tau\). Hence

\[
\frac{d}{d\tau}\log e_\tau(Z)
=
-
\frac{d}{d\tau}\log p_\tau(Z).
\]

For one adjacent gap

\[
d_i=t_{i+1}-t_i,
\qquad
\alpha_i=e^{-d_i/\tau},
\]

we have

\[
\alpha_i'(\tau)
=
\frac{d_i}{\tau^2}e^{-d_i/\tau}.
\]

The implementation evaluates the derivative of the exact Gaussian innovation likelihood analytically from the sufficient transition sums

\[
\sum_m X_{i,m}^2,
\qquad
\sum_m X_{i,m}X_{i+1,m},
\qquad
\sum_m X_{i+1,m}^2.
\]

Summing the chain-rule contribution of every irregular time gap gives the exact observed-data derivative

\[
\boxed{
\ell'(\tau)
=
\frac{d}{d\tau}\log e_\tau(Z)
}.
\]

This is not a numerical finite difference. The claim-level tests compare the analytic derivative with a centered numerical derivative only as a verification check.

## Physical meaning

The slope answers a local physical-time question:

> If the candidate relaxation time is moved slightly away from this value, how rapidly does the observed calibration record become more or less compatible with the model?

A steep slope means the data distinguish nearby relaxation times strongly at that location. A shallow slope means nearby timescales are harder to separate.

---

# 3. Cell-local curvature bound

Let a calibration cell be

\[
I_j=[a_j,b_j]
\]

with center

\[
c_j=\frac{a_j+b_j}{2}
\]

and radius

\[
r_j=\frac{b_j-a_j}{2}.
\]

Proposition 55 computes a deterministic bound

\[
M_j
\ge
\sup_{\tau\in I_j}
\left|
\frac{d^2}{d\tau^2}
\log e_\tau(Z)
\right|.
\]

The bound is obtained transition by transition through the exact irregular-grid coefficient \(\alpha_i(\tau)\).

For

\[
\alpha(\tau)=e^{-d/\tau},
\]

the second derivative can be written in terms of \(x=d/\tau\). The absolute scalar curvature has analytic stationary points at

\[
x=3-\sqrt 3
\qquad\text{and}\qquad
x=3+\sqrt 3.
\]

The implementation checks these critical points whenever they lie inside the transformed cell and also checks the interval endpoints. This produces a closed deterministic bound on the transition coefficient curvature.

The Gaussian likelihood contribution is then bounded through the chain rule using the declared channel count and the observed transition sufficient statistics.

## Physical meaning

The curvature describes how quickly the local sensitivity itself changes as the candidate physical timescale moves through a cell.

The theorem does not interpret curvature as an energy or a physical force. It is curvature of the finite-sample statistical compatibility function with respect to the physical parameter \(\tau\).

---

# 4. Quadratic cell certificate

Taylor's theorem gives, for every \(\tau\in I_j\),

\[
\log e_\tau(Z)
\ge
\log e_{c_j}(Z)
-
|\ell'(c_j)|r_j
-
\frac12 M_j r_j^2.
\]

Define the certified lower enclosure

\[
L_j
=
\log e_{c_j}(Z)
-
|\ell'(c_j)|r_j
-
\frac12 M_j r_j^2.
\]

If

\[
L_j
\ge
\log(1/\alpha),
\]

then every point in that cell is rejected by Proposition 53B. The cell can therefore be removed safely.

A cell is retained whenever this exclusion inequality cannot be proved.

Let the retained union be

\[
\mathcal O^{(2)}_\alpha(Z).
\]

Then

\[
\boxed{
\mathcal C_\alpha(Z)
\subseteq
\mathcal O^{(2)}_\alpha(Z)
}.
\]

This is the Proposition 55 calibration statement.

## Why no new probability penalty appears

The e-value theorem already supplies the probability statement for \(\mathcal C_\alpha(Z)\).

The quadratic cells are a deterministic outer enclosure of that random continuum set after the calibration record is observed. The cell calculations do not introduce another stochastic test and therefore do not spend another confidence budget.

---

# 5. Time-unit covariance of the certificate

If physical time is rescaled by a constant \(c>0\),

\[
t_i\mapsto ct_i,
\qquad
\tau\mapsto c\tau,
\]

then the physical covariance is unchanged.

The Proposition 55 derivatives transform as

\[
\ell'_{c\text{-units}}(c\tau)
=
\frac1c\ell'_{\text{original}}(\tau),
\]

and

\[
M_{c\text{-units}}
=
\frac1{c^2}M_{\text{original}}.
\]

Because the cell radius scales as \(cr\), the two correction terms

\[
|\ell'|r
\qquad\text{and}\qquad
\frac12Mr^2
\]

remain invariant.

Therefore the retained cell pattern is unchanged by expressing the same physical times in seconds, milliseconds, or another consistent unit.

This invariance is covered by a dedicated claim-level test.

---

# 6. Independent target composition

The quadratic calibration cover can be propagated to the same independent target-covariance layer used by Proposition 54.

Let

\[
[\tau_-,\tau_+]
\]

be the smallest interval containing the retained quadratic cells. A separate target grid covers that interval. Proposition 49 then supplies a covariance certificate conditional on the calibration record.

If calibration and target records are independent, with confidence levels \(1-\alpha\) and \(1-\beta\), the combined lower bound remains

\[
\boxed{
(1-\alpha)(1-\beta)
}.
\]

The current target implementation still uses the Proposition 54 first-order temporal operator envelope on the smaller Proposition 55 retained interval. Proposition 55 therefore improves calibration geometry while leaving the target matrix-concentration theorem itself unchanged.

This distinction becomes important in Experiment AP.

---

# 7. Experiment AP

Experiment AP reuses the physical-time benchmark introduced in Experiments AN and AO.

The controlled configuration is:

- true physical relaxation time: \(\tau_*=0.78\) s;
- declared interval: \([0.40,1.25]\) s;
- calibration confidence: \(0.975\);
- target covariance confidence: \(0.975\);
- combined confidence lower bound: \(0.950625\);
- 96 independent calibration channels;
- 32 irregular calibration timestamps;
- 120 target timestamps on a different schedule;
- target nuisance rank: \(2\).

## 7.1 Certified interval contraction

At the same cell resolutions, the first-order Proposition 53B outer cover and the Proposition 55 quadratic cover are:

| Cells | First-order width | Quadratic width |
| ---: | ---: | ---: |
| 40 | 0.850000 s | 0.255000 s |
| 80 | 0.850000 s | 0.191250 s |
| 160 | 0.6109375 s | 0.1646875 s |
| 320 | 0.44359375 s | 0.15671875 s |
| 640 | 0.33203125 s | 0.1540625 s |

At 160 cells, Proposition 55 retains

\[
\boxed{
\tau\in[0.686875,0.8515625]\ \mathrm{s}
}
\]

instead of the first-order interval

\[
[0.495625,1.1065625]\ \mathrm{s}.
\]

The certified width contracts by approximately

\[
\boxed{73.0\%}.
\]

The true controlled value \(0.78\) s remains inside the retained interval.

## 7.2 Target covariance radius

Using 160 quadratic calibration cells and a 65-point target cover, the final target covariance relative-error radius is

\[
\boxed{
\varepsilon_{55}=2.4148799294322116
}.
\]

For comparison,

\[
\varepsilon_{53B}=3.155489544511118,
\]

and

\[
\varepsilon_{54}=2.572074694777741.
\]

Thus the quadratic calibration layer removes a substantial part of the earlier deterministic calibration looseness.

It still does not cross the perturbative threshold one.

---

# 8. Known-\(\tau\) oracle diagnostic

Experiment AP also evaluates the existing target covariance theorem in an intentionally unrealistic oracle condition: the true physical relaxation time \(\tau_*=0.78\) s is supplied exactly.

The temporal cover then contains only one covariance matrix and both temporal covering radii are zero.

Even in that condition, the current Proposition 49 target theorem gives

\[
\boxed{
\varepsilon_{\mathrm{oracle}}
=2.167246895150515
>1.
}
\]

This is not a usable calibration method. It is a diagnostic floor for the present target concentration machinery on this benchmark.

## What this proves about the current bottleneck

For this target configuration, temporal-parameter uncertainty is no longer the dominant reason the final radius exceeds one.

Even perfect knowledge of \(\tau\) does not make the current target theorem enter the \(\varepsilon<1\) regime.

Therefore further calibration sharpening alone cannot close this benchmark.

The next mathematical improvement must change the target covariance concentration layer, the target measurement design, the target amount of independent information, or some combination of these.

This negative diagnostic is part of the result. It prevents the project from spending additional theorem complexity on the wrong bottleneck.

---

# 9. Physical interpretation

Proposition 55 should be read as a statement about **how sharply an irregular-time calibration experiment constrains one declared physical timescale**.

It says that the finite-sample likelihood can contain much more local geometric information than a first-order global derivative envelope captures.

It does not say:

- that every physical process has one exponential relaxation time;
- that the fitted \(\tau\) is a universal constant;
- that likelihood curvature is a physical energy landscape;
- that a narrower \(\tau\) interval means a system is more conscious or more organized;
- that the target covariance is already known accurately enough for all later observer calculations.

The last point is especially important because the oracle target radius remains above one.

---

# 10. Failure conditions and falsification

The theorem is conditional on the declared one-timescale stationary Gaussian exponential-relaxation model and independent standardized calibration channels.

A physical application should challenge those assumptions directly. Relevant diagnostics include:

- residual temporal correlation after innovation whitening;
- evidence for multiple relaxation times;
- oscillatory or nonmonotone autocorrelation;
- time-varying relaxation behavior;
- heavy-tailed or non-Gaussian innovations;
- dependence between calibration channels;
- target/calibration mismatch;
- sensitivity to the declared nuisance design.

If these diagnostics fail, a narrow Proposition 55 interval is not evidence that the real physical system has been correctly described.

---

# 11. Reproducibility

Implementation:

- `src/observer_math/relaxation_curvature.py`
- `src/observer_math/quadratic_relaxation_target.py`

Claim-level tests:

- `tests/test_relaxation_curvature.py`

Experiment:

- `examples/quadratic_relaxation_calibration.py`

Machine-readable record:

- `docs/quadratic_relaxation_calibration.json`

The numerical experiment illustrates theorem scale. The continuum containment statement comes from the analytic derivative, curvature bound, and Taylor enclosure, not from the displayed numerical grid.
