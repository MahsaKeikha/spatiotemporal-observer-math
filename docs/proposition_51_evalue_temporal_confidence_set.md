# Proposition 51: finite-sample e-value confidence sets for temporal covariance parameters

Proposition 50 calibrates a two-parameter temporal family by constructing separate finite-sample intervals for lag-1 and lag-2 correlations and then propagating those intervals through a nonlinear parameter map. That route is rigorous, but it loses joint information because the two lag statistics are treated through rectangular interval arithmetic.

Proposition 51 takes a different route. It uses the full Gaussian residual likelihood of the calibration record and constructs a confidence set directly in parameter space.

The main result is finite sample and continuum valued. A parameter grid is not part of the probability proof.

The result remains conditional on the declared Gaussian temporal model. It does not establish a claim about consciousness.

## 1. Calibration model

Let

\[
Y^{(1)},\ldots,Y^{(M)}\in\mathbb R^N
\]

be independent Gaussian calibration channels. Channel \(j\) may have its own arbitrary unknown constant mean:

\[
\mathbb E Y^{(j)}=\mu_j\mathbf 1.
\]

All channels share temporal covariance

\[
R_{\phi,\eta}
=(1-\eta)R_\phi+\eta I,
\]

where

\[
(R_\phi)_{ab}=\phi^{|a-b|},
\]

and the declared parameter box is

\[
\Theta
=
[\phi_-,\phi_+]\times[\eta_-,\eta_+],
\]

with

\[
0\le\phi_-\le\phi_+<1,
\qquad
0\le\eta_-\le\eta_+<1.
\]

## 2. Remove constant channel means exactly

Choose a fixed matrix

\[
H\in\mathbb R^{d\times N}
\]

before inspecting the calibration data, with

\[
HH^\mathsf T=I_d,
\qquad
H\mathbf 1=0.
\]

The implementation uses orthonormal Helmert contrasts. With \(d=N-1\), the rows span the complete orthogonal complement of the constant direction. A smaller fixed \(d\) deliberately discards some information but does not change the validity argument.

Define

\[
Z^{(j)}=HY^{(j)}.
\]

Then the unknown mean disappears exactly:

\[
\mathbb E Z^{(j)}
=
H\mu_j\mathbf 1
=0.
\]

For parameter \(\theta=(\phi,\eta)\), let

\[
C_\theta
=HR_{\phi,\eta}H^\mathsf T.
\]

Thus

\[
Z^{(j)}\sim\mathcal N(0,C_\theta)
\]

independently across channels.

This reduction is exact. No channel mean is estimated.

## 3. Residual likelihood

Let

\[
Z=[Z^{(1)},\ldots,Z^{(M)}]
\]

and define the residual scatter matrix

\[
S=ZZ^\mathsf T.
\]

Ignoring the Gaussian normalization constant that is common to every parameter value, the joint log-likelihood kernel is

\[
\ell_\theta(Z)
=
-\frac{M}{2}\log\det C_\theta
-\frac12\operatorname{tr}(C_\theta^{-1}S).
\]

The implementation evaluates this expression with a matrix solve rather than an explicit inverse.

## 4. Fix a proper mixture density before seeing the data

Choose any finite set of parameter points

\[
\theta_1,\ldots,\theta_K\in\Theta
\]

before observing the calibration record, together with positive weights

\[
w_k>0,
\qquad
\sum_{k=1}^K w_k=1.
\]

Let

\[
p_\theta(z)
\]

denote the complete residual density under parameter \(\theta\), and define the fixed mixture density

\[
q(z)
=
\sum_{k=1}^K w_k p_{\theta_k}(z).
\]

The implementation currently uses equal weights on a deterministic product grid inside the declared parameter box. That choice affects power and numerical geometry. It does not affect the validity identity below.

The true parameter does not need to be one of the mixture points.

## 5. Pointwise e-values

For every continuum parameter value \(\theta\in\Theta\), define

\[
e_\theta(Z)
=
\frac{q(Z)}{p_\theta(Z)}.
\]

If \(\theta\) is the true parameter, then

\[
\mathbb E_\theta e_\theta(Z)
=
\int
\frac{q(z)}{p_\theta(z)}
p_\theta(z)\,dz
=
\int q(z)\,dz
=1.
\]

This identity is exact.

It is also the entire reason the confidence-set construction works.

## 6. The continuum confidence set

Let \(\alpha\in(0,1)\). Markov's inequality gives

\[
\Pr_\theta\left(
e_\theta(Z)\ge\frac1\alpha
\right)
\le\alpha.
\]

Therefore define

\[
\mathcal C_\alpha(Z)
=
\left\{
\theta\in\Theta:
 e_\theta(Z)<\frac1\alpha
\right\}.
\]

Then, for every true \(\theta\in\Theta\),

\[
\Pr_\theta\left(
\theta\in\mathcal C_\alpha(Z)
\right)
\ge1-\alpha.
\]

No parameter-grid union bound appears in this statement.

No asymptotic approximation appears in this statement.

No independence assumption between lag-1 and lag-2 summaries appears because Proposition 51 does not reduce the record to separate lag summaries.

## Proposition 51

**Proposition 51 (finite-sample Gaussian temporal-family e-value confidence set).**

Assume:

1. the calibration channels are independent Gaussian channels;
2. each channel has an arbitrary constant temporal mean;
3. all channels share one temporal covariance \(R_\theta\) from a declared family \(\{R_\theta:\theta\in\Theta\}\);
4. a fixed row-orthonormal contrast \(H\) annihilates the constant direction;
5. every compressed covariance \(C_\theta=HR_\theta H^\mathsf T\) is positive definite;
6. the mixture density \(q\) is a proper density fixed independently of the calibration observations.

For every \(\alpha\in(0,1)\), the random set

\[
\mathcal C_\alpha(Z)
=
\left\{
\theta\in\Theta:
q(Z)/p_\theta(Z)<1/\alpha
\right\}
\]

contains the true parameter with probability at least \(1-\alpha\).

The theorem remains valid when \(q\) is a finite mixture whose support does not contain the true parameter.

### Proof

Fix any true parameter \(\theta\in\Theta\). The contrast removes every channel mean, so the residual data have density \(p_\theta\). Because \(q\) is a proper density,

\[
\mathbb E_\theta\left[
\frac{q(Z)}{p_\theta(Z)}
\right]
=
\int q(z)\,dz
=1.
\]

Markov's inequality implies

\[
\Pr_\theta\left(
\frac{q(Z)}{p_\theta(Z)}
\ge\frac1\alpha
\right)
\le\alpha.
\]

The complementary event is exactly

\[
\theta\in\mathcal C_\alpha(Z).
\]

Therefore

\[
\Pr_\theta(
\theta\in\mathcal C_\alpha(Z)
)
\ge1-\alpha.
\]

This holds for every \(\theta\in\Theta\). \(\square\)

## 7. Why the result is genuinely joint

Proposition 50 first constructs two marginal correlation intervals and then maps their Cartesian product into parameter space. Proposition 51 evaluates one likelihood ratio for the complete residual record at every candidate parameter.

The resulting set can therefore be curved, tilted, disconnected, or otherwise nonrectangular. Its geometry is determined by the full residual likelihood rather than by coordinatewise interval arithmetic.

This does not automatically make Proposition 51 smaller for every dataset. The mixture density, contrast dimension, and realized record all affect its geometry. The theorem provides coverage, not a universal dominance statement over every other valid confidence procedure.

## 8. What the numerical grid means

The public API can evaluate

\[
\log e_\theta(Z)
\]

at any admissible continuum parameter value.

For figures, the repository also evaluates that exact pointwise function on a deterministic grid. The displayed accepted grid points satisfy

\[
\log e_\theta(Z)
<
\log(1/\alpha)
\]

at those points.

A plotted grid is not an outer confidence cover of the continuum set. Points between grid locations are governed by the continuum theorem but are not automatically represented by their nearest plotted point.

This distinction is important for the next step of the research program. A future result can build a certified adaptive outer cover of \(\mathcal C_\alpha(Z)\) and then feed that cover into Proposition 49 for an independent target covariance record.

## 9. Experiment AK

Experiment AK compares the geometry of Proposition 50 and Proposition 51 on one controlled two-parameter calibration problem. The controlled truth is

\[
(\phi,\eta)=(0.60,0.04),
\]

inside the declared box

\[
\phi\in[0.40,0.80],
\qquad
\eta\in[0,0.25].
\]

The calibration record has length 100. Proposition 51 uses 30 fixed Helmert contrasts, a 7 by 5 equal-weight mixture grid, and a 33 by 26 visualization grid. Only the number of independent calibration channels changes.

The exact numerical record is stored separately in `evalue_temporal_confidence_set.json`.

The main quantity shown by the experiment is the shape of the evaluated e-value set. It is not presented as a certified continuum outer boundary.

At 256 channels, Proposition 50's rectangular propagation spans approximately

\[
\phi\in[0.510,0.701],
\qquad
\eta\in[0,0.216],
\]

while the accepted Proposition 51 visualization points span approximately

\[
\phi\in[0.55,0.65],
\qquad
\eta\in[0,0.12].
\]

The difference is especially visible in the white-noise direction, which remained prior-limited in Experiment AJ.

The figure and numerical record also report the accepted grid fraction and the log e-value at the controlled true parameter as calibration information grows.

The experiment is a scale and geometry study. The coverage proof is Proposition 51 itself.

## 10. Limits and next theorem

Proposition 51 still assumes:

- exact Gaussian calibration channels;
- independence across calibration channels;
- one common temporal covariance family;
- constant channel means removed by a fixed contrast;
- a correctly declared temporal family;
- a mixture density fixed independently of the observed calibration record.

The theorem does not yet convert the irregular continuum confidence set into a certified finite temporal covariance cover for Proposition 49.

That is the natural next theorem. It should construct an adaptive outer cover that is guaranteed to contain the complete e-value confidence set, then compose that random cover with the independent-target matrix concentration theorem.

A second direction is broader: replace the specific AR(1) plus white-noise family by a richer covariance or spectral-density model while preserving the same e-value principle.
