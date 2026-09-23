# Gaussian Predictive Discrimination for Active Measurement

Competitor-directed sensing becomes statistically meaningful when the device can quantify how well a proposed sensing action separates the predictive laws of two surviving moving-boundary hypotheses.

This page develops that quantity for a declared linear-Gaussian predictive model.

## 1. Action-dependent predictive laws

For a retained world-tube hypothesis \(p\), suppose the one-step latent predictive state is

\[
X_{t+1}\mid\mathcal F_t,p
\sim
\mathcal N(m_p,P_p).
\]

Under sensing action \(a\),

\[
Y_{t+1}=H_aX_{t+1}+V_{t+1},
\qquad
V_{t+1}\sim\mathcal N(0,R_a),
\]

with \(R_a\succ0\). Therefore

\[
Y_{t+1}\mid\mathcal F_t,p,a
\sim
\mathcal N(\mu_p^a,\Sigma_p^a),
\]

where

\[
\mu_p^a=H_am_p,
\qquad
\Sigma_p^a=H_aP_pH_a^{\mathsf T}+R_a.
\]

Thus a physical sensing choice changes the statistical distinguishability of the surviving structural hypotheses.

## 2. Exact pairwise Gaussian separation

For two retained hypotheses \(p\) and \(r\), define

\[
\mathcal D_t^{\mathrm{KL}}(p,r;a)
=
D_{\mathrm{KL}}
\left(
\mathcal N(\mu_p^a,\Sigma_p^a)
\;\|\;
\mathcal N(\mu_r^a,\Sigma_r^a)
\right).
\]

For measurement dimension \(d_a\),

\[
\boxed{
\mathcal D_t^{\mathrm{KL}}(p,r;a)
=
\frac12
\left[
\operatorname{tr}\!\left((\Sigma_r^a)^{-1}\Sigma_p^a\right)
+
(\mu_r^a-\mu_p^a)^{\mathsf T}
(\Sigma_r^a)^{-1}
(\mu_r^a-\mu_p^a)
-d_a
+
\log\frac{\det\Sigma_r^a}{\det\Sigma_p^a}
\right].
}
\]

This is an action-dependent predictive discrimination score. It is not a consciousness score.

## 3. Equal-covariance specialization

When the competing predictive laws share covariance \(P_p=P_r=P\), they also share

\[
\Sigma_a=H_aPH_a^{\mathsf T}+R_a.
\]

Then the divergence reduces to

\[
\boxed{
\mathcal D_t^{\mathrm{KL}}(p,r;a)
=
\frac12
\delta_{pr}^{\mathsf T}
H_a^{\mathsf T}
\Sigma_a^{-1}
H_a
\delta_{pr},
}
\]

where

\[
\delta_{pr}=m_p-m_r.
\]

The measurement device should therefore favor sensing directions that expose predictive differences after accounting for measurement and predictive covariance.

## 4. Proposition AM2: exact optimal single-channel sensor

Assume coordinate sensing with one selected channel \(j\),

\[
H_j=e_j^{\mathsf T},
\]

independent measurement noise variance \(r_j>0\), and equal predictive covariance \(P\) under the two hypotheses. Then

\[
\mathcal D_t^{\mathrm{KL}}(p,r;j)
=
\frac12
\frac{(m_{p,j}-m_{r,j})^2}{P_{jj}+r_j}.
\]

Therefore every maximizer

\[
\boxed{
j^*
\in
\arg\max_j
\frac{(m_{p,j}-m_{r,j})^2}{P_{jj}+r_j}
}
\]

is an optimal one-channel action for pairwise KL discrimination.

**Proof.**
For \(H_j=e_j^{\mathsf T}\), the equal-covariance predictive measurement variance is the scalar \(P_{jj}+r_j\), while the predictive mean difference is \(m_{p,j}-m_{r,j}\). Substitution into the equal-covariance Gaussian KL expression gives the stated formula. The factor \(1/2\) is common to every channel, so maximizing KL divergence is equivalent to maximizing the displayed signal-to-uncertainty ratio. \(\square\)

## 5. Interpretation of AM2

AM2 sharpens disagreement coverage. A coordinate can belong to the symmetric difference of two candidate boundaries yet be a poor measurement if the hypotheses make nearly identical predictions there or if its uncertainty/noise is large.

The resulting hierarchy is

\[
\text{set disagreement}
\rightarrow
\text{predictive disagreement}
\rightarrow
\text{noise-normalized predictive discrimination}.
\]

This gives the adaptive device a principled progression from structural geometry to measurement statistics.

## 6. Proposition AM3: zero-discrimination impossibility for an action

For any two hypotheses \(p,r\) and action \(a\),

\[
\mathcal D_t^{\mathrm{KL}}(p,r;a)=0
\]

if and only if their action-conditioned Gaussian predictive laws are identical:

\[
\mu_p^a=\mu_r^a,
\qquad
\Sigma_p^a=\Sigma_r^a.
\]

**Proof.**
KL divergence between probability distributions is nonnegative and equals zero exactly when the two distributions agree almost everywhere. Nonsingular Gaussian laws are identical exactly when their means and covariance matrices are equal. \(\square\)

**Device consequence.** If every admissible action produces the same predictive law under \(p\) and \(r\), no policy based only on the next measurement can distinguish those hypotheses at that step. The correct response is preservation of ambiguity, not forced classification.

## 7. Hardest-competitor sensing

Let \(p^{(1)}\) be the current leading path and \(\mathcal C_t\) the retained competitor family. Define

\[
\Gamma_t(a)
=
\min_{r\in\mathcal C_t\setminus\{p^{(1)}\}}
\mathcal D_t^{\mathrm{KL}}(p^{(1)},r;a).
\]

A robust active measurement rule is

\[
a_{t+1}
\in
\arg\max_{a\in\mathcal A}
\left[
\Gamma_t(a)
-\lambda_EC_E(a)
-\lambda_SC_S(a,a_t)
\right].
\]

Unlike disagreement coverage, \(\Gamma_t(a)\) asks whether the proposed physical measurement statistically separates the winner from **every retained near competitor**.

## 8. Certification target

The next theoretical layer is sequential rather than one-step. For measurements acquired under actions \(a_1,\ldots,a_N\), the accumulated log-likelihood ratio between two declared predictive models is

\[
L_N(p,r)
=
\sum_{k=1}^{N}
\log
\frac{
f_p(Y_k\mid\mathcal F_{k-1},a_k)
}{
f_r(Y_k\mid\mathcal F_{k-1},a_k)
}.
\]

Under appropriate conditional-model assumptions, its expected increment under \(p\) is the corresponding conditional KL divergence. This suggests a direct bridge between active sensing and time-to-separation.

That bridge is a research target, not yet promoted here to a finite-sample stopping theorem.

## 9. Required computational experiment

A reproducible benchmark should construct competing moving-boundary hypotheses for which:

1. some disagreement coordinates have weak predictive separation;
2. some have strong predictive separation;
3. measurement noise differs across channels;
4. the sensing budget is strictly smaller than the full sensor set.

Compare:

- full sensing;
- random budget-matched sensing;
- set-disagreement sensing;
- AM2 noise-normalized predictive sensing;
- hardest-competitor sensing.

Report boundary recovery, candidate-set contraction, accumulated pairwise discrimination, time to a predeclared certification threshold, sensing cost, and abstention frequency.

## 10. Scientific boundary

AM2 and AM3 are results about discrimination between declared Gaussian predictive models. They do not establish that either model is a biological theory of consciousness. Their role is narrower and operational: once Research I has produced competing structural hypotheses, the physical measurement device can choose observations that are mathematically informative for resolving those hypotheses.


## 11. Sequential evidence extension

The one-step Gaussian discrimination score now feeds a separate [Sequential Evidence for Adaptive Measurement](sequential_adaptive_evidence.md) layer. That development proves an adaptive expected-evidence decomposition, the likelihood-ratio martingale identity under predictable sensing actions, and an anytime-valid threshold for rejecting a declared competing predictive model. Stronger claims about expected stopping time, composite hypotheses, misspecification, and physical-device stability remain explicit open problems.
