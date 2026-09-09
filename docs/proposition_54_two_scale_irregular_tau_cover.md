# Proposition 54: two-scale certified relaxation-time cover

## Purpose

Proposition 53B gives a finite-sample continuum confidence set for a physical exponential relaxation time on irregular timestamps. Its certified finite outer cover can be made finer by using more calibration cells, but directly sending every retained calibration cell into Proposition 49 also increases the target temporal-cover cardinality.

Proposition 54 separates those two numerical resolutions.

A fine grid is used only to certify the calibration confidence set. A second, independently chosen target grid then covers the resulting retained physical-time interval. This preserves finite-sample validity while allowing calibration resolution and target concentration complexity to be tuned separately.

## Setup

Let the calibration model and its continuum e-value confidence set be those of Proposition 53B. Let

\[
\mathcal C_\alpha(Z)
=
\left\{
\tau:\log e_\tau(Z)<\log(1/\alpha)
\right\}.
\]

Let a deterministic cell certificate produce a finite retained outer cover

\[
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z).
\]

Write

\[
\tau_-
=
\inf \mathcal O_\alpha(Z),
\qquad
\tau_+
=
\sup \mathcal O_\alpha(Z).
\]

The interval

\[
I_Z=[\tau_-,\tau_+]
\]

is therefore also a valid outer cover, even when the retained cell set itself is disconnected.

Let the independent target record have increasing timestamps

\[
s_1<\cdots<s_N
\]

and a fixed nuisance design \(H\in\mathbb R^{N\times q}\). Define

\[
P_H=I-H(H^\mathsf T H)^{-1}H^\mathsf T.
\]

For the exponential physical-time family,

\[
R_\tau(i,j)
=
\exp\left(-\frac{|s_i-s_j|}{\tau}\right).
\]

## Statement

Choose any integer \(K\ge 2\) using only the calibration record and declared target timestamps/design, not the target observations. Put equally spaced representatives

\[
\tau_k
=
\tau_-+
\frac{k-1}{K-1}(\tau_+-\tau_-),
\qquad k=1,\ldots,K.
\]

Their spacing is

\[
h=\frac{\tau_+-\tau_-}{K-1}.
\]

Every \(\tau\in I_Z\) lies within \(h/2\) of at least one representative.

Suppose

\[
\|R_\tau-R_{\tau'}\|_2
\le
L_Z |\tau-\tau'|
\]

for every \(\tau,\tau'\in I_Z\), where \(L_Z\) is the analytic exponential-family operator-Lipschitz constant evaluated on the retained interval.

Define

\[
\delta_\lambda
=
L_Z\frac h2.
\]

Then every retained temporal covariance matrix is within operator distance \(\delta_\lambda\) of a target representative.

Because orthogonal projection is contractive,

\[
\|P_H(R_\tau-R_{\tau_k})P_H\|_2
\le
\delta_\lambda.
\]

Hence Weyl's inequality gives the same additive radius for every ordered projected temporal eigenvalue.

The projected normalization is

\[
d_H(\tau)=\operatorname{tr}(P_H R_\tau).
\]

All exponential correlation matrices have unit diagonal, so

\[
\operatorname{tr}(R_\tau-R_{\tau_k})=0.
\]

Writing \(Q_H=I-P_H\), whose rank is \(q\), gives

\[
\begin{aligned}
d_H(\tau)-d_H(\tau_k)
&=
\operatorname{tr}(P_H(R_\tau-R_{\tau_k}))\\
&=-\operatorname{tr}(Q_H(R_\tau-R_{\tau_k})).
\end{aligned}
\]

Therefore

\[
\boxed{
|d_H(\tau)-d_H(\tau_k)|
\le
q\delta_\lambda
}
\]

and the normalization covering radius is

\[
\delta_d=q\delta_\lambda.
\]

Applying Proposition 49 to the \(K\) target representatives with covering radii \(\delta_\lambda\) and \(\delta_d\) yields a simultaneous target covariance certificate conditional on the calibration record.

If the calibration confidence is \(1-\alpha\) and the conditional target covariance confidence is \(1-\beta\), independence of calibration and target records gives combined confidence

\[
\boxed{
(1-\alpha)(1-\beta)
}.
\]

## Calibration-only selection of K

Let \(K_1,\ldots,K_m\) be a fixed candidate set. For each \(K_j\), compute the deterministic Proposition 49 radius using only:

- the calibration-derived interval \(I_Z\);
- the declared target timestamps;
- the declared nuisance design;
- the target block dimension and block count;
- the requested target confidence level.

No target observations enter this calculation.

Therefore one may choose

\[
K_*
=
\arg\min_{K_j}
\varepsilon(K_j)
\]

without an additional union bound over \(K_j\). Conditional on the calibration record and declared target design, the selected target theorem is still a single valid Proposition 49 certificate.

## Why the theorem is genuinely two-scale

The calibration cell count and the target cover point count play different roles.

The calibration grid exists only to prove

\[
\mathcal C_\alpha(Z)\subseteq\mathcal O_\alpha(Z).
\]

Increasing its resolution can shrink the certified physical-time interval without increasing the target union factor.

The target grid exists only to cover the already certified interval. Its cardinality can therefore be chosen to balance the geometric covering error against the matrix concentration penalty.

This removes the artificial requirement that one numerical grid perform both jobs.

# Experiment AO

Experiment AO reuses the exact deterministic physical-time problem from Experiment AN:

- true relaxation time: \(0.78\) s;
- declared interval: \([0.40,1.25]\) s;
- 96 independent calibration channels;
- 32 irregular calibration samples;
- 120 target samples on a different timestamp grid;
- nuisance rank \(q=2\);
- calibration confidence: \(0.975\);
- covariance confidence: \(0.975\);
- combined confidence: \(0.950625\).

## Calibration resolution

| Calibration cells | Certified lower | Certified upper | Certified width |
| ---: | ---: | ---: | ---: |
| 160 | 0.495625 s | 1.1065625 s | 0.6109375 s |
| 320 | 0.56203125 s | 1.005625 s | 0.44359375 s |
| 640 | 0.60984375 s | 0.941875 s | 0.33203125 s |
| 1280 | 0.643046875 s | 0.9013671875 s | 0.2583203125 s |
| 2560 | 0.66396484375 s | 0.8761328125 s | 0.21216796875 s |

The increasingly fine calibration certificate moves toward the much narrower likelihood-compatible region observed in Experiment AN, while preserving the same finite-sample coverage argument.

## Target cover search at 1280 calibration cells

| Target points K | Approximate relative covariance radius |
| ---: | ---: |
| 5 | 2.9763059 |
| 7 | 2.8245141 |
| 9 | 2.7536898 |
| 13 | 2.6861966 |
| 17 | 2.6536877 |
| 25 | 2.6219980 |
| 33 | 2.6064589 |
| 49 | 2.5911230 |
| 65 | 2.5835311 |

The calibration-only search selects \(K=65\).

The final 1024-theta evaluation gives

\[
\boxed{
\varepsilon_{54}=2.572074694777741
}.
\]

The Proposition 53B baseline on the same physical problem was

\[
\varepsilon_{53B}=3.155489544511118.
\]

Thus Proposition 54 reduces the radius by

\[
0.5834148497333773,
\]

or approximately

\[
\boxed{18.49\%}.
\]

The final target eigenvalue covering radius decreases from approximately

\[
0.10916
\]

to

\[
0.06363.
\]

## What Proposition 54 closes

It closes the artificial coupling between calibration certification resolution and target temporal-cover resolution.

It also shows empirically, on the exact Experiment AN problem, that this coupling was responsible for a meaningful but limited part of the previous looseness.

## What Proposition 54 does not close

The final covariance radius remains

\[
\boxed{2.572074694777741>1}.
\]

Therefore Proposition 54 does not yet unlock inverse-covariance or other downstream perturbation theorems that require \(\varepsilon<1\).

The remaining bottleneck is now more sharply localized. Adding target cover points gives diminishing returns. The next proof target should improve one or both of:

1. the deterministic outer-cover geometry for the e-value confidence set;
2. the operator envelope used to propagate a local physical-time interval to the target temporal covariance.

A natural next direction is a local curvature or second-order certificate that replaces a first-derivative worst-case bound by a certified quadratic enclosure near each cell center.

## Reproducibility

- implementation: `src/observer_math/two_scale_relaxation_cover.py`
- claim tests: `tests/test_two_scale_relaxation_cover.py`
- experiment: `examples/two_scale_irregular_tau_cover.py`
- machine-readable record: `docs/two_scale_irregular_tau_cover.json`

## Scope

The result remains conditional on the Gaussian exponential-relaxation calibration model, standardized independent calibration channels, fixed declared target timestamps and nuisance design, and independence of calibration and target records.

It does not establish that a real process has one exponential relaxation time. It does not infer an observer boundary. It does not establish consciousness.
