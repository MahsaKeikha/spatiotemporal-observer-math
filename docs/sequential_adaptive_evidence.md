# Sequential Evidence for Adaptive Measurement

The active-measurement extension becomes operational when the device has both a rule for choosing the next measurement and a rule for deciding when the accumulated evidence is sufficient to stop resolving a pair of competing structural hypotheses.

This page develops a finite-horizon evidence identity and a conservative stopping rule for **declared predictive models**.

## 1. Adaptive measurement history

Let

\[
\mathcal F_{k-1}
=
\sigma(Y_1,a_1,\ldots,Y_{k-1},a_{k-1})
\]

be the information available before selecting action \(a_k\). The action may be adaptive:

\[
a_k=\pi_k(\mathcal F_{k-1}).
\]

For two retained hypotheses \(p\) and \(r\), let

\[
f_{p,k}(\cdot\mid\mathcal F_{k-1},a_k),
\qquad
f_{r,k}(\cdot\mid\mathcal F_{k-1},a_k)
\]

be their declared conditional predictive densities for the next physical measurement.

Define the accumulated log evidence

\[
L_N(p,r)
=
\sum_{k=1}^{N}
\ell_k(p,r),
\]

with

\[
\ell_k(p,r)
=
\log
\frac{
f_{p,k}(Y_k\mid\mathcal F_{k-1},a_k)
}{
f_{r,k}(Y_k\mid\mathcal F_{k-1},a_k)
}.
\]

## 2. Proposition AM4: adaptive expected-evidence decomposition

Assume the data are generated according to the declared conditional predictive law of \(p\), and all displayed conditional KL divergences are integrable. Then

\[
\boxed{
\mathbb E_p[L_N(p,r)]
=
\sum_{k=1}^{N}
\mathbb E_p
\left[
D_{\mathrm{KL}}
\left(
f_{p,k}(\cdot\mid\mathcal F_{k-1},a_k)
\;\|\;
f_{r,k}(\cdot\mid\mathcal F_{k-1},a_k)
\right)
\right].
}
\]

The identity remains valid when \(a_k\) is chosen adaptively from the past.

**Proof.**
Condition on \(\mathcal F_{k-1}\). Since \(a_k\) is determined by the available history, it is fixed under this conditional expectation. Therefore

\[
\mathbb E_p[
\ell_k(p,r)
\mid
\mathcal F_{k-1}
]
=
D_{\mathrm{KL}}
\left(
f_{p,k}(\cdot\mid\mathcal F_{k-1},a_k)
\;\|\;
f_{r,k}(\cdot\mid\mathcal F_{k-1},a_k)
\right).
\]

Taking expectations and summing over \(k\) gives the result. \(\square\)

### Meaning

AM4 supplies the exact bridge between one-step predictive discrimination and accumulated expected evidence. An active sensing policy can therefore be compared by the discrimination it accumulates against the surviving competitor family, not only by the number of channels it samples.

AM4 does not by itself give a high-probability stopping time.

## 3. Likelihood-ratio evidence process

Define

\[
E_N(r:p)
=
\exp[-L_N(p,r)]
=
\prod_{k=1}^{N}
\frac{
f_{r,k}(Y_k\mid\mathcal F_{k-1},a_k)
}{
f_{p,k}(Y_k\mid\mathcal F_{k-1},a_k)
}.
\]

## 4. Proposition AM5: adaptive likelihood-ratio martingale

Under hypothesis \(p\), assuming the conditional densities are normalized and the likelihood ratios are well defined,

\[
\boxed{
\mathbb E_p[
E_N(r:p)
\mid
\mathcal F_{N-1}
]
=
E_{N-1}(r:p).
}
\]

Hence \(E_N(r:p)\) is a nonnegative martingale with \(E_p[E_N]=1\).

**Proof.**
Conditioning on \(\mathcal F_{N-1}\),

\[
\mathbb E_p
\left[
\frac{f_{r,N}(Y_N\mid\mathcal F_{N-1},a_N)}
{f_{p,N}(Y_N\mid\mathcal F_{N-1},a_N)}
\middle|
\mathcal F_{N-1}
\right]
=
\int f_{r,N}(y\mid\mathcal F_{N-1},a_N)\,dy
=1.
\]

Multiplying by the \(\mathcal F_{N-1}\)-measurable factor \(E_{N-1}(r:p)\) gives the claim. \(\square\)

This result is valid for adaptive sensing because the action is chosen before observing \(Y_N\).

## 5. Proposition AM6: anytime-safe rejection of a declared hypothesis

Reverse the ratio and define

\[
E_N(p:r)
=
\prod_{k=1}^{N}
\frac{
f_{p,k}(Y_k\mid\mathcal F_{k-1},a_k)
}{
f_{r,k}(Y_k\mid\mathcal F_{k-1},a_k)
}.
\]

Under hypothesis \(r\), \(E_N(p:r)\) is a nonnegative unit-mean martingale. Therefore, for \(0<\alpha<1\),

\[
\boxed{
\Pr_r
\left(
\sup_{N\ge1}E_N(p:r)\ge\frac1\alpha
\right)
\le\alpha.
}
\]

Equivalently,

\[
\Pr_r
\left(
\exists N:
L_N(p,r)\ge\log(1/\alpha)
\right)
\le\alpha.
\]

**Proof.**
The martingale property follows from AM5 with \(p\) and \(r\) exchanged. Ville's inequality for nonnegative supermartingales gives the displayed crossing bound. \(\square\)

### Device interpretation

If the device declares that \(r\) has been rejected in favor of \(p\) the first time

\[
L_N(p,r)\ge\log(1/\alpha),
\]

then, **when \(r\) is the declared data-generating model**, the probability that this evidence threshold is ever crossed is at most \(\alpha\).

This is an anytime-valid model-discrimination statement. It is not a guarantee that \(p\) is biologically true, and it is not a posterior probability.

## 6. Multiple retained competitors

Suppose the leading hypothesis \(p\) is compared with a finite retained set

\[
\mathcal R=\{r_1,\ldots,r_M\}.
\]

Assign error budgets \(\alpha_i>0\) with

\[
\sum_{i=1}^{M}\alpha_i\le\alpha.
\]

A conservative certification rule requires

\[
L_N(p,r_i)
\ge
\log(1/\alpha_i)
\qquad
\text{for every }i.
\]

For each individual competitor \(r_i\), the corresponding false-rejection crossing probability is controlled by \(\alpha_i\) when that competitor is the declared generating model.

The allocation \(\alpha_i\) is part of the device design. Uniform allocation \(\alpha_i=\alpha/M\) is simple but may be conservative.

This section deliberately does not convert pairwise guarantees into a stronger composite-model statement without additional assumptions.

## 7. Active sensing objective aligned with sequential evidence

AM4 suggests selecting the next action to increase expected evidence against the hardest surviving competitor:

\[
a_{k+1}
\in
\arg\max_{a\in\mathcal A}
\min_{r\in\mathcal R_k}
D_{\mathrm{KL}}
\left(
f_{p,k+1}^{a}
\|f_{r,k+1}^{a}
\right)
-
\lambda_EC_E(a)
-
\lambda_SC_S(a,a_k).
\]

AM6 supplies an evidence threshold whose type-I crossing interpretation remains valid despite adaptive action selection, provided the predictive models used in the likelihood ratio are the declared conditional laws.

The combination creates a coherent loop:

\[
\boxed{
\text{choose an informative measurement}
\rightarrow
\text{observe}
\rightarrow
\text{update evidence}
\rightarrow
\text{remove/reweight competitors}
\rightarrow
\text{choose again}.
}
\]

## 8. Connection to the moving-boundary observer

The retained hypotheses need not represent arbitrary models. In Research I they can be localized world-tube competitors generated by the existing path objective and near-competitor structure.

The resulting device architecture is

\[
\text{world-tube inference}
\rightarrow
\text{near competitors}
\rightarrow
\text{action-dependent predictive laws}
\rightarrow
\text{active sensing}
\rightarrow
\text{sequential evidence}
\rightarrow
\text{certify or abstain}.
\]

This is the mathematical point at which the moving-boundary observer begins to control its own measurement process.

## 9. What remains to be proved

The following stronger statements are **not** established by AM4-AM6:

- an upper bound on expected time to certification;
- optimality of the max-min KL sensing policy;
- validity under estimated or misspecified predictive densities without correction;
- composite-hypothesis validity for a data-dependent competitor set without an appropriate construction;
- a direct finite-sample bridge from the existing covariance certificate to the sequential likelihood-ratio certificate;
- closed-loop physical-device stability.

Each requires a separate result.

## 10. Reproducible validation target

The first sequential benchmark should freeze a family of competing moving-boundary models and compare equal-budget policies by:

- cumulative conditional KL against the hardest competitor;
- number of measurements to threshold crossing;
- fraction remaining uncertified at a fixed horizon;
- wrong-model threshold crossings;
- sensing expenditure;
- structural path recovery;
- abstention frequency.

The simulation must also include a deliberately observationally equivalent pair. For that pair the device should fail to accumulate discriminating evidence and should remain unresolved rather than manufacturing certainty.

## 11. Consciousness research boundary

These propositions certify evidence accumulation between declared predictive models of physical measurements. They do not certify consciousness itself. Their role in the broader program is to make the measurement process responsive to unresolved structure while preserving the distinction between operational dynamical evidence and phenomenological interpretation.
