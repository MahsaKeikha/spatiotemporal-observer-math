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
