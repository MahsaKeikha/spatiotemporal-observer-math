# Self-Certifying Moving-Boundary Observer

## Scientific object

The extension developed here treats adaptive measurement as part of the
moving-boundary inference problem rather than as a generic sensing add-on.

At measurement step (k), define the observer state

[
mathfrak O_k =
(widehat W_k,mathcal C_k,widehatDelta_{A,k},U_k,
mathbf S_k,mathcal E_k).
]

The components are:

- (widehat W_k): current leading world-tube hypothesis;
- (mathcal C_k): retained structurally plausible competitor family;
- (widehatDelta_{A,k}): leading-versus-runner-up path-action margin;
- (U_k): a valid bound on complete path-action uncertainty under the
  applicable Research I covariance/score perturbation result;
- (mathbf S_k=(S_k(r):rinmathcal C_ksetminus{widehat W_k})):
  pairwise signed sequential evidence gaps;
- (mathcal E_k): observational equivalence relation induced by the
  admissible measurement family.

The state is intentionally richer than a point estimate. It records what the
observer currently prefers, what alternatives remain, how fragile the
structural ordering is, how much predictive evidence is still owed, and which
alternatives cannot be separated by available measurements.

## Three epistemic regimes

The observer distinguishes three mathematically different outcomes.

### Recoverable now

A candidate is structurally certified only when the applicable path-action
uncertainty condition is satisfied. In the symmetric per-path-error form,

[
widehatDelta_{A,k}>2U_k.
]

If sequential evidence is also required by the declared protocol, every
retained nonequivalent competitor must additionally satisfy its evidence gate.

### Resolvable with more measurement

At least one competitor remains unresolved, but an admissible action has
positive action-conditioned discrimination against it:

[
sup_{ainmathcal A}
D_{mathrm{KL}}(f_p^a|f_r^a)>0.
]

AM8-AM11 then quantify expected evidence progress and an information budget for
resolution.

### Observationally unidentifiable under the action family

For some distinct retained pair,

[
f_p^a=f_r^aquad	ext{for every admissible }a.
]

AM9 shows that adaptive sensing cannot accumulate likelihood evidence between
that pair. The scientifically correct representation is an equivalence class
or ABSTAIN, not forced classification.

## Dual-deficit acquisition

A measurement can be useful for two different reasons:

1. it can reduce uncertainty in the structural score/action calculation;
2. it can discriminate predictive laws of retained structural competitors.

These quantities must not be silently treated as identical.

For an admissible action (a), define a structural uncertainty reduction

[
R_U(a)
=
U_k-mathbb E[U_{k+1}midmathcal F_k,a],
]

when the chosen covariance-certification construction supplies a valid
post-measurement uncertainty update.

For competitor (r), AM8 gives the exact expected signed-evidence-gap
reduction

[
R_S(a;r)
=
D_{mathrm{KL}}(f_p^a|f_r^a).
]

Let (q_{k,j}) be the world-tube disagreement weights and (h_j(a)) the
visibility of coordinate (j). Define structural disagreement coverage

[
R_C(a)=sum_j q_{k,j}h_j(a).
]

A general certificate-aware acquisition score is therefore

[
V_k(a)
=
eta_U R_U(a)
+
eta_S min_{rinmathcal C_ksetminus[p]} R_S(a;r)
+
eta_C R_C(a)
-
lambda_E C_E(a)
-
lambda_{mathrm{sw}} C_{mathrm{sw}}(a,a_k).
]

This expression is a research objective, not yet an optimality theorem.
The (R_U) term must not be used numerically until a valid action-dependent
uncertainty update has been derived for the relevant covariance estimator.

## AM12: joint certificate sufficiency

Let (p) be the current leading world tube and suppose:

1. for every retained path (r
e p), the estimated action errors satisfy
   (|widehat A(p)-A(p)|le U_k) and
   (|widehat A(r)-A(r)|le U_k);
2. (widehatDelta_{A,k}
   =widehat A(p)-max_{r
e p}widehat A(r)>2U_k);
3. for every retained nonequivalent competitor (r), the declared sequential
   evidence gate (L_k(p,r)ge h_r) is satisfied.

Then (p) is the unique population-action maximizer among the retained
candidate family, and every declared pairwise sequential evidence gate against
nonequivalent retained competitors is satisfied.

### Proof

For any retained (r
e p),

[
A(p)-A(r)
ge
widehat A(p)-U_k-[widehat A(r)+U_k]
ge
widehatDelta_{A,k}-2U_k>0.
]

Hence (p) has strictly larger population action than every retained
competitor. Condition 3 is already the definition of satisfaction of the
declared pairwise evidence gates. The two conclusions are logically distinct:
the first is a deterministic structural-ordering certificate conditional on
the error bounds, while the second is a sequential evidence statement under
the predictive testing model.

AM12 does not establish validity if the retained candidate family excludes a
relevant population competitor. Candidate localization therefore requires its
own coverage guarantee.

## AM13: equivalence-aware certification obstruction

Suppose a distinct retained competitor (r) is observationally equivalent to
(p) under every admissible action, and the protocol requires a positive
sequential evidence threshold against every distinct retained competitor.

Then full singleton certification of (p) is impossible under that protocol.

### Proof

AM9 gives (L_N(p,r)=0) almost surely for every (N). Every positive threshold
(h_r=log(1/alpha_r)) remains unmet. Therefore the conjunction of all
required evidence gates cannot hold.

The appropriate output is certification of an observational equivalence class
when structurally justified, or abstention. This prevents a measurement system
from converting an identifiability failure into artificial certainty.

## Candidate-family coverage is a first-class requirement

A localized competitor set makes computation and active sensing tractable, but
it introduces a failure mode: the omitted path may be the true population
competitor. Any future end-to-end theorem must therefore separate

[
	ext{candidate coverage}
+
	ext{structural ordering}
+
	ext{predictive evidence}
+
	ext{equivalence handling}.
]

The research program is incomplete until all four are controlled.

## Falsification program

A credible self-certifying observer must be tested in regimes designed to make
it fail:

- local evidence already dominates, where active transport/sensing should add
  little;
- transport-informative ambiguity;
- continuity-confounded motion;
- transport-null dynamics;
- near-symmetric world tubes with very small KL;
- exact observational equivalence;
- sensor dropout and heterogeneous noise;
- model misspecification;
- abrupt structural motion;
- slowly drifting structural motion;
- candidate-localization failure;
- covariance uncertainty large enough to defeat the structural certificate.

Success means reporting the correct regime, including negative and abstaining
outcomes, not merely maximizing path-recovery accuracy.

## Claim discipline

The construction combines established ingredients with Research I's
moving-world-tube object. KL-directed sensing, sequential likelihood ratios,
anytime-valid evidence, dynamic support recovery, and active experiment design
have substantial prior literatures. The research-specific contribution must be
judged at the level of the integrated moving-boundary certification problem,
not by relabeling those ingredients as new.

Priority or first-of-kind claims require a dedicated closest-literature audit.


## Action-dependent structural uncertainty: exact Gaussian covariance update

The dual-deficit objective requires a mathematically valid (R_U(a)), not a
heuristic confidence bonus. A first exact case is available when the observer
maintains a Gaussian covariance belief and a measurement action selects a
linear observation.

Let the current latent state satisfy

[
Xmidmathcal F_ksimmathcal N(m_k,P_k),
]

and let action (a) produce

[
Y=H_aX+V,qquad Vsimmathcal N(0,R_a),quad R_asucc0.
]

The posterior covariance is

[
P_k^+(a)
=
P_k-P_kH_a^	op
(H_aP_kH_a^	op+R_a)^{-1}
H_aP_k.
]

This covariance does not depend on the realized measurement value in the
linear-Gaussian model.

### AM14: positive-semidefinite uncertainty contraction

For every admissible action,

[
0preceq P_k^+(a)preceq P_k.
]

Consequently, for every vector (v),

[
v^	op P_k^+(a)vle v^	op P_kv,
]

and every monotone spectral uncertainty functional, including
(operatorname{tr}(P)) and (lambda_{max}(P)), cannot increase.

**Proof.** The removed term is
(P_kH_a^	op(H_aP_kH_a^	op+R_a)^{-1}H_aP_k), which is positive
semidefinite. The remaining inequalities follow directly.

This gives an exact action-dependent uncertainty reduction

[
R_{mathrm{tr}}(a)
=
operatorname{tr}(P_k)-operatorname{tr}(P_k^+(a))ge0.
]

It is an uncertainty reduction for the Gaussian latent-state covariance. It is
not automatically the Research I complete path-action error radius (U_k).
A theorem connecting the two requires sensitivity of the observer action to
the covariance blocks used by the world-tube score.

## Structural sensitivity map

Let (g(Sigma)) denote a scalar world-tube action difference between the
current leader and a retained competitor, evaluated from the relevant
covariance blocks. At a covariance (Sigma_k), define a local sensitivity

[
G_k=
abla_Sigma g(Sigma_k).
]

For a small covariance perturbation (E),

[
g(Sigma_k+E)-g(Sigma_k)
=
langle G_k,Eangle_F+o(|E|_F).
]

If a valid local remainder bound is available,

[
|o(|E|_F)|le c_k|E|_F^2,
]

then an action that preferentially reduces covariance uncertainty in directions
aligned with (G_k) directly targets uncertainty in the structural decision,
rather than merely reducing total covariance variance.

This suggests the sensitivity-weighted criterion

[
R_G(a)
=
operatorname{tr}!left[
G_k^	op G_k
left(P_k-P_k^+(a)ight)
ight],
]

when dimensions and the covariance parameterization make this contraction
well-defined. This expression is presently a design target, not a theorem for
the full Research I score.

## AM15: scalar directional variance reduction

For a scalar linear functional (Z=v^	op X), define its posterior variance
under action (a) as

[
U_v^+(a)=v^	op P_k^+(a)v.
]

Then the exact reduction is

[
R_v(a)
=
v^	op P_kH_a^	op
(H_aP_kH_a^	op+R_a)^{-1}
H_aP_kv
ge0.
]

Thus if a local structural decision is known to depend on a specific linear
direction (v), maximizing (R_v(a)) exactly maximizes the one-step reduction
of posterior variance in that direction within the declared Gaussian model.

AM15 is deliberately narrower than a complete world-tube uncertainty theorem.
Its role is to establish a rigorous building block from which score-specific
sensitivity results can be derived.

## The two-information geometry

The closed-loop observer now exposes two distinct action-dependent geometries:

[
mathcal I_{mathrm{est}}(a)
quad	ext{from covariance/Fisher-information contraction},
]

and

[
mathcal I_{mathrm{disc}}(a;r)
=
D_{mathrm{KL}}(f_p^a|f_r^a)
quad	ext{from competitor discrimination}.
]

An action can be excellent for estimating the current state while poor for
distinguishing world-tube competitors, or vice versa. The scientifically
interesting acquisition problem is therefore not generic information
maximization but allocation across these two geometries subject to structural
disagreement and measurement cost.

A future theorem should characterize the Pareto frontier

[
left(
R_U(a),
min_r D_{mathrm{KL}}(f_p^a|f_r^a),
R_C(a)
ight),qquad ainmathcal A,
]

and identify conditions under which one action improves all three quantities
or a genuine tradeoff is unavoidable.

## Literature boundary for the next theorem

Adaptive experimental design already uses expected and observed Fisher
information to improve estimator precision. Controlled sensing and active
sequential hypothesis testing already use action-dependent information
divergence to reduce decision delay. Therefore neither covariance contraction
nor KL-directed sensing is claimed as new in isolation.

The research-specific question is whether the covariance sensitivity of a
*moving world-tube structural decision* can be coupled to competitor-specific
sequential discrimination in one certifying acquisition rule, including
explicit observational-equivalence and abstention behavior.


## From covariance contraction to path-action certification

Let \(\theta\) collect the covariance blocks on which a retained pairwise world-tube action difference depends, and define

\[
g_{p,r}(\theta)=A_\theta(p)-A_\theta(r).
\]

Suppose the current estimate is \(\widehat\theta_k\), and a valid confidence region after action \(a\) is

\[
\mathcal B_{k+1}(a)=\{\theta:\|\theta-\widehat\theta_{k+1}\|_{\mathsf M(a)}\le \rho_{k+1}(a)\}.
\]

Define the robust pairwise lower margin

\[
\underline g_{k+1}(p,r;a)=\inf_{\theta\in\mathcal B_{k+1}(a)}g_{p,r}(\theta).
\]

This is the appropriate structural-certification target: an action is useful when it improves the worst-case path ordering, not merely when it reduces an unrelated state covariance.

### AM16: robust-margin certificate

If, on an event \(E_{k+1}(a)\), the true covariance parameter \(\theta_\star\) belongs to \(\mathcal B_{k+1}(a)\), then

\[
\underline g_{k+1}(p,r;a)>0
\]

implies \(A_{\theta_\star}(p)>A_{\theta_\star}(r)\) on that event. If the same strict inequality holds for every retained \(r\ne p\), then \(p\) is the unique population-action maximizer over the retained family on \(E_{k+1}(a)\).

**Proof.** Membership of \(\theta_\star\) in the confidence region gives

\[
g_{p,r}(\theta_\star)\ge
\inf_{\theta\in\mathcal B_{k+1}(a)}g_{p,r}(\theta)
=\underline g_{k+1}(p,r;a)>0.
\]

Apply this to every retained competitor.

AM16 is distribution-agnostic after the confidence region has been established. The statistical burden is isolated in constructing a valid action-dependent region.

## AM17: Lipschitz sufficient certificate

Assume \(g_{p,r}\) is \(L_{p,r}\)-Lipschitz on the relevant confidence region:

\[
|g_{p,r}(\theta)-g_{p,r}(\theta')|\le L_{p,r}\|\theta-\theta'\|.
\]

If \(\|\theta-\widehat\theta_k\|\le\rho_k\), then

\[
g_{p,r}(\theta_\star)\ge g_{p,r}(\widehat\theta_k)-L_{p,r}\rho_k.
\]

Therefore

\[
\boxed{g_{p,r}(\widehat\theta_k)>L_{p,r}\rho_k}
\]

is sufficient to certify \(p\) over \(r\). Across all retained competitors, a sufficient singleton certificate is

\[
\min_{r\ne p}\left[g_{p,r}(\widehat\theta_k)-L_{p,r}\rho_k\right]>0.
\]

This can be sharper than a common \(2U_k\) bound when pair-specific sensitivities are available.

## Certificate-directed value of a measurement

Define expected robust-margin gain

\[
R_{\mathrm{cert}}(a)=
\mathbb E\!\left[\min_{r\ne p}\underline g_{k+1}(p,r;a)\mid\mathcal F_k\right]
-\min_{r\ne p}\underline g_k(p,r).
\]

A certificate-directed acquisition objective is

\[
a_{k+1}^\star\in\arg\max_{a\in\mathcal A}
\left\{
\eta_g R_{\mathrm{cert}}(a)
+\eta_s\min_{r\ne p}D_{\mathrm{KL}}(f_p^a\|f_r^a)
-\lambda C(a)
\right\}.
\]

Both terms now have direct certification meanings: one targets worst-case structural ordering, and the other targets sequential predictive evidence. This remains a proposed acquisition rule until action-dependent confidence regions and its performance properties are established.

## What remains before an end-to-end theorem

The principal unresolved mathematical step is now precise: construct an action-dependent confidence region for the covariance blocks used by the actual Research I observer factors under heterogeneous adaptive measurement, then bound \(L_{p,r}\) or the robust infimum tightly enough to be useful.

A complete theorem would combine time-uniform confidence-region validity with a policy-dependent information condition that drives the robust retained-family margin positive whenever the true structure is identifiable. Observationally equivalent cases remain exempt by AM9 and AM13.


## AM18: factorwise-to-path certificate under action-dependent radii

The Research I path action is assembled from local observer scores, transport scores, and continuity terms. This structure permits a rigorous bridge from action-dependent uncertainty radii to the complete path decision without requiring a single undifferentiated covariance radius.

Write

\[
A(p)=\sum_{t=0}^{T-1}\Omega_t(S_t)
+\chi\sum_{t=0}^{T-2}\Theta_t(S_t\to S_{t+1})
-\lambda\sum_{t=0}^{T-2}d_J(S_t,S_{t+1}).
\]

The Jaccard term is deterministic once a candidate path is specified, so statistical uncertainty enters through \(\Omega\) and \(\Theta\).

Suppose an admissible measurement design \(a\) yields simultaneous valid bounds

\[
|\widehat\Omega_t(S)-\Omega_t(S)|\le e_{\Omega,t,S}(a)
\]

and

\[
|\widehat\Theta_t(S\to R)-\Theta_t(S\to R)|
\le e_{\Theta,t,S,R}(a)
\]

for every factor used by a retained candidate family.

Define the path-specific action radius

\[
E_a(p)
=
\sum_{t=0}^{T-1}e_{\Omega,t,S_t}(a)
+
|\chi|
\sum_{t=0}^{T-2}e_{\Theta,t,S_t,S_{t+1}}(a).
\]

Then

\[
|\widehat A(p)-A(p)|\le E_a(p).
\]

### Proposition AM18

For two retained paths \(p\) and \(r\), if

\[
\widehat A(p)-E_a(p)
>
\widehat A(r)+E_a(r),
\]

then \(A(p)>A(r)\) on the simultaneous factor-bound event.

If

\[
\widehat A(p)-E_a(p)
>
\max_{r\ne p}\left[\widehat A(r)+E_a(r)\right],
\]

then \(p\) is the unique population-action maximizer over the retained family on that event.

**Proof.** The factorwise triangle inequality gives
\(A(p)\ge\widehat A(p)-E_a(p)\) and
\(A(r)\le\widehat A(r)+E_a(r)\). The strict interval separation gives the pairwise ordering. Apply it to every retained competitor for the second claim.

AM18 is important because it identifies exactly what an adaptive measurement must improve: not generic state variance, but the uncertainty radii of the specific local and transport factors appearing on the leading and competing world tubes.

## Certificate pressure map

For a leading path \(p\) and competitor \(r\), define their robust separation

\[
C_a(p,r)
=
\widehat A(p)-\widehat A(r)-E_a(p)-E_a(r).
\]

A negative value identifies an unresolved pair. Decompose its uncertainty burden over time and factors:

\[
B_{\Omega,t}(p,r;a)
=
e_{\Omega,t,S_t^p}(a)+e_{\Omega,t,S_t^r}(a),
\]

\[
B_{\Theta,t}(p,r;a)
=
|\chi|\left[
e_{\Theta,t,S_t^p,S_{t+1}^p}(a)
+
e_{\Theta,t,S_t^r,S_{t+1}^r}(a)
\right].
\]

These quantities form a certificate-pressure map over the moving world tubes. A measurement action should preferentially reduce the factor radii that dominate the hardest unresolved pair.

This produces a structural analogue of competitor-directed sensing: the world-tube geometry tells the system not only which coordinates disagree, but which uncertain score factors currently prevent certification.

## AM19: exact value of radius contraction for a fixed estimated margin

Consider a one-step design comparison in which the current estimated path actions are held fixed while the candidate measurement design changes only the certified factor radii. For pair \(p,r\),

\[
C_a(p,r)=
\widehat A(p)-\widehat A(r)-E_a(p)-E_a(r).
\]

For two designs \(a\) and \(b\),

\[
C_a(p,r)-C_b(p,r)
=
[E_b(p)+E_b(r)]-[E_a(p)+E_a(r)].
\]

Therefore, conditional on the same estimated action values, maximizing robust pairwise separation is exactly equivalent to minimizing the sum of the two path-specific uncertainty radii.

This result is algebraic and deliberately conditional. In a genuine adaptive experiment, a new observation can change both the estimated actions and their radii. The end-to-end analysis must account for both effects.

## Toward an action-dependent covariance-block radius

Let \(Z_{t,S}\) denote the Gaussian vector used to compute a particular Research I factor, with covariance \(\Sigma_{t,S}\). Under a measurement design \(a\), suppose \(m_{t,S}(a)\) effective independent innovation samples are available after the declared temporal whitening/calibration step. A relative covariance event has the form

\[
\left\|
\Sigma_{t,S}^{-1/2}
(\widehat\Sigma_{t,S}-\Sigma_{t,S})
\Sigma_{t,S}^{-1/2}
\right\|_2
\le
\varepsilon_{t,S}(a).
\]

Existing Research I perturbation maps can then convert \(\varepsilon_{t,S}(a)\) into bounds for information and canonical-correlation factors. The active-measurement problem becomes scientifically concrete if the acquisition policy controls \(m_{t,S}(a)\), sensor noise, or block visibility and therefore changes \(\varepsilon_{t,S}(a)\).

The next derivation must use the exact covariance-concentration inequality and factor perturbation functions already established in Research I rather than introducing an incompatible surrogate. The goal is an explicit computable map

\[
a
\longmapsto
\varepsilon_{t,S}(a)
\longmapsto
(e_{\Omega},e_{\Theta})
\longmapsto
E_a(p)
\longmapsto
C_a(p,r).
\]

Once this map is validated, certificate-directed sensing becomes an end-to-end consequence of the original observer mathematics rather than a parallel heuristic.


## Executable certificate pipeline

The adaptive extension now has a package-level implementation in
\`observer_math.active_measurement\`. The implementation deliberately reuses
the established Research I relative-covariance perturbation machinery rather
than introducing a second uncertainty calculus.

For a retained path \(p\), candidate-local relative covariance radii are mapped
to local observer-score radii \(e_{\Omega,t}\), while edge radii are mapped to
transport-score radii \(e_{\Theta,t}\). The complete action uncertainty is

\[
E_a(p)=\sum_t e_{\Omega,t}(a)+|\chi|\sum_t e_{\Theta,t}(a).
\]

For leader \(p\) and retained competitor \(r\), define the robust separation

\[
C_a(p,r)=\widehat A(p)-E_a(p)-\widehat A(r)-E_a(r).
\]

A positive value certifies ordering of that pair whenever the supplied
simultaneous covariance events and their propagated factor bounds hold. A
singleton structural certificate requires positive separation against every
retained competitor and valid candidate-family coverage.

This structural certificate is intentionally distinct from predictive
evidence. The current executable benchmark therefore requires both robust
structural separation and a positive sequential evidence gate. Exact
observational equivalence blocks singleton certification even when covariance
uncertainty contracts.

The matched-budget benchmark in
\`examples/matched_budget_certification_benchmark.py\` compares fixed, random,
KL-directed, certificate-pressure-directed, and joint acquisition under an
identical scalar-measurement budget. It is a synthetic methodological test,
not a biological model. Numerical claims should be reported only after the
benchmark and its tests have been executed in a verified environment.
