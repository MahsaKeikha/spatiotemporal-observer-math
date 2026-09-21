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
