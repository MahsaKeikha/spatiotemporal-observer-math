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


## 12. Device supervisory layer

The sequential evidence process now feeds a [Certification-Aware Measurement Automaton](certification_aware_measurement_automaton.md). The automaton separates DISCOVER, RESOLVE, TRACK, and ABSTAIN measurement modes, defines an explicit evidence gate and resolution deficit, and keeps TRACK reversible when later measurements indicate structural change or model inadequacy.


## AM8: KL drift of the signed certification gap

For a fixed retained competitor (r), let

[
h_r=log(1/alpha_r),qquad
S_k(r)=h_r-L_k(p,r).
]

The quantity (S_k(r)) is a signed distance to the pairwise evidence threshold.
It is positive before the threshold is crossed and nonpositive after crossing.

**Proposition AM8.** Under the declared generating law (p), predictable action
selection, and the same integrability conditions used in AM4,

[
mathbb E_p[S_{k+1}(r)midmathcal F_k]
=
S_k(r)
-
D_{mathrm{KL}}!left(
f_{p,k+1}^{a_{k+1}}
middle|
f_{r,k+1}^{a_{k+1}}
ight).
]

Hence

[
S_k(r)-mathbb E_p[S_{k+1}(r)midmathcal F_k]
=
D_{mathrm{KL}}!left(
f_{p,k+1}^{a_{k+1}}
middle|
f_{r,k+1}^{a_{k+1}}
ight)ge 0.
]

**Proof.** By definition,
(S_{k+1}(r)=S_k(r)-ell_{k+1}(p,r)). Conditional on
(mathcal F_k), the action (a_{k+1}) is fixed because it is predictable.
AM4 gives
(mathbb E_p[ell_{k+1}(p,r)midmathcal F_k]
=D_{mathrm{KL}}(f_p^{a_{k+1}}|f_r^{a_{k+1}})).
Substitution proves the identity.

This result gives a precise interpretation of KL-directed measurement:
for a fixed competitor, maximizing the conditional KL divergence exactly
maximizes the expected one-step reduction of the signed evidence gap. It does
not by itself establish globally optimal sensing, minimum stopping time, or
optimality when the identity of the active competitor changes.

## AM9: observational-equivalence impossibility under adaptive sensing

Let (p) and (r) be two retained structural hypotheses. Suppose that for
every time (k), every history reached by the policy, and every admissible
action selected there,

[
f_{p,k}(cdotmidmathcal F_{k-1},a_k)
=
f_{r,k}(cdotmidmathcal F_{k-1},a_k)
quad	ext{almost surely}.
]

**Proposition AM9.** Under this condition,

[
ell_k(p,r)=0quad	ext{a.s.},qquad
L_N(p,r)=0quad	ext{a.s. for every }N.
]

Consequently, no positive likelihood-ratio threshold
(log(1/alpha)), (0<alpha<1), can be crossed by evidence between the
pair using any policy restricted to those admissible actions.

**Proof.** Equality of the action-conditioned predictive densities makes their
likelihood ratio one almost surely at every step. Its logarithm is zero.
Summation gives (L_N=0). Since (log(1/alpha)>0), threshold crossing is
impossible.

AM9 is deliberately an impossibility result. Adaptivity cannot create
information that is absent from every admissible observation kernel. In the
measurement automaton, such a pair must remain unresolved, be represented by
an observational equivalence class, or trigger ABSTAIN.

## Relation to established controlled-sensing theory

KL-directed experiment selection and adaptive sequential hypothesis testing
are established ideas. The contribution pursued here is therefore not a claim
to have invented KL-maximizing sensing or likelihood-ratio stopping. The
research-specific object is the composition

[
	ext{moving world-tube inference}
	o
	ext{runner-up structural geometry}
	o
	ext{action-conditioned discrimination}
	o
	ext{sequential evidence}
	o
	ext{certify or abstain}.
]

The novelty question for this composition must be evaluated against the
closest controlled-sensing, active-hypothesis-testing, dynamic-support, and
time-varying-structure literature before any priority claim is made.


## AM10: information budget for closing a certified evidence gap

AM8 gives a one-step drift identity. Iterating it gives a finite-horizon
information accounting law.

Fix a retained competitor (r) and define the signed gap
(S_k(r)=h_r-L_k(p,r)), where (h_r=log(1/alpha_r)). For a predictable
sequence of future measurement actions (a_{k+1:k+m}), define the conditional
cumulative discrimination budget

[
B_{k,m}(r)
=
sum_{i=1}^{m}
mathbb E_p!left[
D_{mathrm{KL}}!left(
f_{p,k+i}^{a_{k+i}}middle|f_{r,k+i}^{a_{k+i}}
ight)
middle|mathcal F_k
ight].
]

**Proposition AM10.** Under the assumptions of AM8,

[
mathbb E_p[S_{k+m}(r)midmathcal F_k]
=
S_k(r)-B_{k,m}(r).
]

Therefore (B_{k,m}(r)ge S_k(r)) is necessary and sufficient for the
*expected signed gap* at horizon (k+m) to be nonpositive.

**Proof.** Apply AM8 at each future step, take conditional expectations with
respect to (mathcal F_k), and telescope.

This is an expectation statement, not a threshold-crossing probability bound.
It does not imply that the evidence threshold is crossed by time (k+m) with
high probability.

For a finite retained competitor set (mathcal R_k), define

[
S_k^{max}=max_{rinmathcal R_k} S_k(r).
]

A sensing plan that aims to close every expected pairwise gap must allocate
enough action-conditioned information that
(B_{k,m}(r)ge S_k(r)) for every retained (r). This exposes a measurable
resource requirement: unresolved structural alternatives consume an explicit
future discrimination budget.

## AM11: a lower bound under bounded per-measurement discrimination

Suppose for a fixed competitor (r) every admissible action satisfies

[
D_{mathrm{KL}}!left(f_p^amiddle|f_r^aight)le kappa_r
]

almost surely for some finite (kappa_r). Then after (m) additional
measurements,

[
B_{k,m}(r)le mkappa_r.
]

**Proposition AM11.** If the current signed gap is (S_k(r)>0), any policy
whose expected signed gap is nonpositive after (m) additional measurements
must satisfy

[
mge rac{S_k(r)}{kappa_r}.
]

For integer measurement counts,

[
mge leftlceilrac{S_k(r)}{kappa_r}ightceil.
]

If (kappa_r=0), AM9 applies and no finite number of admissible measurements
can close the gap.

This is a resource lower bound under the declared predictive models. It is not
a minimax lower bound over all possible models, and it is not a guarantee on
the realized stopping time.

## Connecting structural margin and evidence state

Research I already separates the population path margin from uncertainty in
the estimated path action. The active-measurement layer should preserve that
separation. Let

[
widehatDelta_{A,k}
=
widehat A_k(p^{(1)})-widehat A_k(p^{(2)})
]

be the current empirical winner-versus-runner-up action margin, and let
(U_k) denote a valid bound on the complete path-action uncertainty under the
chosen covariance-certification construction. A deterministic structural
certificate has the generic form

[
widehatDelta_{A,k}>2U_k,
]

provided (U_k) bounds the absolute action error of each compared path under
the exact assumptions of the corresponding Research I perturbation result.

This condition and the sequential evidence gate answer different questions:

- the action-margin certificate asks whether covariance/score uncertainty can
  reverse the inferred structural ordering;
- the sequential likelihood evidence asks whether future observations
  discriminate the retained predictive hypotheses.

A strong closed-loop device should require both when both are scientifically
relevant. It should not substitute a large likelihood ratio for a failed
structural uncertainty certificate, or vice versa.

This distinction creates the next testable target: quantify how an admissible
measurement action changes (U_k), (widehatDelta_{A,k}), and the
competitor-specific evidence gaps simultaneously.
