# Research overview

This page is the shortest complete account of the project in its present form.
It gathers the mathematical question, the chain of proved results, the numerical
evidence, the code that produces it, and the limits of the interpretation in one
place. Detailed proofs and experimental records remain in their dedicated
documents; links below lead directly to those records.

## The problem being studied

Suppose the observed state is a time-indexed random vector
\(X_t\in\mathbb R^n\). Instead of fixing a subsystem in advance, let a candidate
boundary be a coordinate subset \(S_t\) that may change with time. A complete
candidate history is

\[
\mathcal W=(S_0,S_1,\ldots,S_{T-1}).
\]

The project asks when such a path can be identified from three observable forms
of organization: predictive interaction across the candidate's internal cut,
insulation from predictive drive outside the candidate, and persistence of its
predictive structure into the next state. The term *observer world-tube* is a
name for this mathematical object. It is not a claim that the selected subsystem
is conscious.

The implemented model is the nonstationary linear Gaussian process

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad \varepsilon_t\sim\mathcal N(0,Q_t),
\]

for which adjacent covariances, conditional mutual informations, and canonical
correlations can be evaluated exactly.

## Score and path objective

For candidate \(S\) at time \(t\), the local score is

\[
\Omega_t(S)=\bigl(G_t(S)K_t(S)P_t(S)\bigr)^{1/3}.
\]

Here \(G\) is weakest-cut directed integration, \(K\) is insulation from the
present environment, and \(P\) is canonical-correlation persistence. Each
factor lies in \([0,1]\). For an edge from \(S\) to \(R\),

\[
\Theta_t(S,R)=\bigl(K_t(S,R)P_t(S,R)\bigr)^{1/2}
\]

measures transported predictive organization. The complete finite-horizon
action is

\[
\mathcal A(\mathcal W)
=\sum_{t=0}^{T-1}\Omega_t(S_t)
+\chi\sum_{t=0}^{T-2}\Theta_t(S_t,S_{t+1})
-\lambda\sum_{t=0}^{T-2}d_J(S_t,S_{t+1}),
\]

where \(d_J\) is Jaccard distance. Dynamic programming returns the exact
maximizer and exact runner-up within the declared candidate family. The action
margin between them is the starting point for every recovery certificate.

## Evidence chain

The mathematical development is cumulative:

1. exact Gaussian covariance and information identities define the score;
2. exact path optimization supplies the winner and its margin;
3. covariance perturbation bounds control every score factor;
4. adversarial dynamic programs propagate local error budgets through the full
   path objective;
5. block and overlap-class recursions replace candidate enumeration by
   structural envelopes;
6. Gaussian concentration connects finite samples to covariance radii;
7. independent sample splitting separates data-dependent screening from final
   certification;
8. boundary-adaptive bounds improve the screen when a zero integration factor
   is known structurally rather than inferred from the same data.

Each arrow in this chain carries explicit assumptions. The
[assumption ledger](assumption_ledger.md) records what fails if any one of them
is violated.

## Theorem index

All statements below are proved in
[Proved results and open problems](proofs_and_conjectures.md). They are
sufficient results under their stated assumptions; they are not presented as
necessary conditions.

| No. | Result | What it establishes |
| ---: | --- | --- |
| 1 | Nonstationary adjacent covariance | Exact covariance recursion and adjacent-state covariance for time-varying linear Gaussian dynamics. |
| 2 | Representation invariance of canonical transport | Canonical transport is unchanged by invertible coordinate changes within source and target blocks. |
| 3 | Bounded transport score | The defined transport factors and score remain in the unit interval. |
| 4 | Finite-horizon path robustness certificate | A positive action margin yields a deterministic uniform score-error radius preserving the optimizer. |
| 5 | Componentwise planted-path recovery | Local and incident-edge advantages imply unique global recovery of a declared planted path. |
| 6 | Finite-sample recovery from uniform score bounds | A simultaneous score event and a deterministic margin combine into a recovery probability. |
| 7 | Covariance perturbation bound for Gaussian CMI | Spectral covariance error gives an explicit conditional-mutual-information error bound. |
| 8 | Canonical-persistence perturbation bound | Covariance error controls canonical correlations and the persistence factor. |
| 9 | End-to-end Gaussian sample-complexity guarantee | Gaussian covariance concentration propagates to a complete path-recovery sample bound. |
| 10 | Positive-factor stability of geometric scores | Away from zero factors, local and transport geometric means obey locally Lipschitz bounds. |
| 11 | Localized finite-sample path certificate | Candidate-specific blocks and an adversarial path calculation sharpen the global certificate. |
| 12 | Parameter-level linear-Gaussian certificate | Transition and noise perturbations propagate directly to a finite-horizon recovery condition. |
| 13 | Objective identifiability modulo symmetry | Recovery is defined on equivalence classes when admissible symmetries preserve the objective. |
| 14 | Two-model impossibility bound | Observationally identical models with incompatible labels impose a one-half maximin ceiling. |
| 15 | Sufficient near-competitor graph | Forward-backward score envelopes safely discard states and edges that cannot challenge the winner. |
| 16 | Symbolic recovery for covariance-preserving moving cliques | Closed-form factors and a recovery margin are obtained for a moving-clique family. |
| 17 | Covariance propagation around the moving-clique family | Transition and noise perturbations produce explicit finite-horizon covariance radii. |
| 18 | Quadratic CMI bound at zero conditional cross-covariance | Conditional mutual information grows quadratically with covariance error at an exact conditional-independence boundary. |
| 19 | Robust recovery with external coupling and anisotropic noise | The moving-clique recovery result survives a declared nonzero perturbation neighborhood. |
| 20 | Support-resolved finite-horizon recovery | Candidate-local covariance blocks and exact incident-edge budgets sharpen the robust margin. |
| 21 | A priori row-local recovery | Row-restricted transition and forcing budgets give local recovery bounds without realized covariance propagation. |
| 22 | Overlap-class recovery without candidate enumeration | Candidate calculations compress to overlap classes with an exact feasible-edge rule. |
| 23 | Structural budgets from block sparsity | Entry sizes and block degrees yield operator-norm budgets through a small comparison matrix. |
| 24 | Block-local covariance influence cones | A fixed block graph preserves finite-speed support information in covariance-error propagation. |
| 25 | Moving-partition covariance influence cones | Rectangular comparisons extend localized propagation to blocks that split, merge, or move. |
| 26 | Moving-partition path-recovery certificate | Moving-partition covariance radii propagate through every score and the adversarial path objective. |
| 27 | Class-compressed robust path recovery | Exact factor symmetry permits robust recovery with class states rather than candidate lists. |
| 28 | Interval-certified class recovery | Componentwise factor intervals replace exact within-class symmetry. |
| 29 | Covariance-residual derivation of class intervals | Representative covariances and spectral residuals generate valid factor intervals. |
| 30 | Block-structural residual class recovery | Moving block envelopes generate the covariance residuals required by class recovery. |
| 31 | Screened-environment structural recovery | Source-specific present compression is valid when omitted conditional information is explicitly charged. |
| 32 | Independent sample-split confidence composition | A safe first split and independent certification split combine with product confidence. |
| 33 | Gaussian first-split screening safety | Fixed Gaussian candidate blocks give a complete concentration-to-screen guarantee. |
| 34 | Positive-factor refinement of Gaussian screening | Empirical factors with positive lower endpoints receive sharper local Lipschitz radii. |
| 35 | Structural-null screening at the score boundary | A predeclared exact integration null receives a quadratic boundary bound and a safe, tighter state radius. |

## Experiment index

Exact commands, parameters, tables, and qualifications are in
[Reproducible results](reproducible_results.md).

| ID | Calculation | Principal recorded outcome |
| --- | --- | --- |
| A | Fixed modular structure | Planted blocks rank first; a correlated-noise control has positive static dependence but zero directed observer score. |
| B | Changing-boundary world-tube | All 5 planted boundaries are recovered; action margin `0.126421`, certified uniform radius `0.010535`. |
| C | Finite-sample recovery | Exact recovery rises from `0.313` at 80 trajectories to `1.000` at 640; an easy local baseline remains competitive. |
| D | Exchangeable non-identifiability | Permutation-related paths tie, the labeled margin is zero, and the two-model maximin ceiling is `0.500`. |
| E | Symbolic moving-clique recovery | Symbolic margin lower bound `0.130806`; exact margin `0.175335`; 3 of 3 boundaries recovered. |
| F | Robust symbolic recovery | Nonzero cross-boundary and anisotropic-noise perturbations retain an exact margin of `0.175280`; several increasingly local certificates are compared. |
| G | Block-sparse structural recovery | Six overlap classes represent `8,250,291,250,200` candidates and retain a positive margin `0.045031`. |
| H | Localized influence cone | A remote covariance perturbation leaves the observed block radius exactly zero until graph distance seven. |
| I | Moving-partition influence cone | The zero persists through changing block counts `4 -> 3 -> 4 -> 2 -> 3` until the declared layered route arrives. |
| J | Moving-partition recovery | Local moving-partition errors feed the full adversarial path certificate and retain positive robust slack. |
| K | Class-compressed robust recovery | Six classes replace a candidate family with more than eight trillion members per layer. |
| L | Heterogeneous interval-class recovery | Nonzero within-class factor widths retain robust slack `0.449062`. |
| M | Covariance-residual-derived intervals | Representative models plus residuals produce the intervals and robust slack `0.530115`. |
| N | Block-structured residual recovery | Primitive block envelopes produce residuals and robust slack `0.801508`. |
| O | Screened-environment recovery | Screened covariance radius `2.500e-08` versus `6.250e-05` for the full environment; slack `0.799524`. |
| P | Independent sample-split accounting | 25 retained versus 10,000 unscreened blocks; minimum certification counts `80,182` and `107,350`; combined confidence `0.950625`. |
| Q | Gaussian-safe first-split screening | At \(10^{12}\) observations, a 60-state/576-edge graph reduces to 5 states and 4 edges under the zero-safe theorem. |
| R | Positive-factor refinement | At \(10^7\) observations, the refined graph has 4 states and 3 edges while the zero-safe graph remains at 16 and 48. |
| S | Exact-Wishart screen calibration | All 64 trials cover each declared event at five scales; the 64-of-64 Wilson interval is only `[0.943376, 1]`, and graph reduction remains conservative. |
| T | Structural-null boundary screen | At \(8\times10^{10}\) observations, a predeclared null mask reduces the safe graph from 40 states/231 edges to 6 states/5 edges while retaining the population path. |

These are controlled synthetic calculations. Large combinatorial counts show
that the compressed certificate does not enumerate candidates; they do not by
themselves establish empirical realism. Likewise, very large nominal sample
counts expose conservatism in the available inequalities rather than propose a
practical data-collection plan.

## Strongest current conclusions

| Question | Current answer | Status |
| --- | --- | --- |
| Can the declared finite path objective be optimized exactly? | Yes, including its exact runner-up and margin. | Exact algorithmic result |
| Can bounded score perturbations be converted into path recovery? | Yes, globally, locally, and through class-compressed adversarial path bounds. | Deterministic theorem |
| Can covariance error be propagated through CMI and canonical correlation? | Yes, with explicit spectral conditions and constants. | Deterministic theorem |
| Can a complete finite-sample confidence statement be made? | Yes for independent Gaussian observations and declared spectral envelopes. | Statistical theorem; conservative |
| Can data-dependent screening be certified? | Yes with an independently sampled certification stage. | Statistical theorem |
| Can exact structural zeros improve the difficult score-boundary rate? | Yes. The local-score error improves from the generic \(N^{-1/6}\) boundary rate to \(N^{-1/3}\) under a correct predeclared null. | Proposition 35 |
| Does the score identify a unique boundary in every model? | No. Exchangeable models give a proved non-identifiability counterexample. | Impossibility theorem |
| Does a high score prove consciousness? | No. That interpretation is neither defined nor supported by these results. | Explicit scope boundary |

## The new structural-null result

The Gaussian calibration revealed a specific obstruction: most incorrect
candidates in that construction have an exactly zero population integration
factor. A generic cube-root perturbation bound treats this boundary with a
Hölder inequality and contracts only as \(N^{-1/6}\).

When the zero is a structural property fixed before seeing the screening data,
Proposition 18 gives a quadratic conditional-information perturbation bound.
Proposition 35 propagates it through the local score. This changes the boundary
rate to \(N^{-1/3}\) and permits a materially smaller safe graph in Experiment
T. The mask is an assumption, not an estimated label: declaring a genuinely
positive-integration state to be null can understate its error and invalidate
the guarantee. A regression test contains that false-null counterexample.

## Reproducing and auditing the project

Set up the environment from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,viz]"
python -m pytest
python -m ruff check .
```

Then run the newest calculation:

```bash
python examples/structural_null_screen_experiment.py
```

The audit trail is organized as follows:

| Need | Location |
| --- | --- |
| Definitions and objective | [Mathematical framework](mathematical_framework.md) |
| Complete derivations | [Derivations](derivations.md) |
| Theorem statements and proofs | [Proved results and open problems](proofs_and_conjectures.md) |
| Assumptions and failure consequences | [Assumption ledger](assumption_ledger.md) |
| Experimental construction rules | [Experimental protocol](experimental_protocol.md) |
| Exact outputs and commands | [Reproducible results](reproducible_results.md) |
| Public Python interface | [API guide](api.md) |
| Core implementation | [`src/observer_math`](../src/observer_math) |
| Claim-level regression tests | [`tests`](../tests) |
| Executable studies | [`examples`](../examples) |
| Machine-readable calibration data | [`gaussian_screen_calibration.json`](gaussian_screen_calibration.json) |

## What remains unresolved

The principal limitations are substantive, not presentational:

- the strongest statistical results assume independent Gaussian observations;
- exact or bounded spectral envelopes are inputs to the current guarantees;
- the available finite-sample constants remain far from empirical recovery
  scales on the initial benchmark;
- a structural-null mask must be justified independently of the screening data;
- the benchmark family is synthetic and does not yet test latent common drive,
  missing variables, nonlinear dynamics, or variable-size boundaries;
- comparative work against external methods has not yet been completed; and
- the quantum factorization geometry remains a research program rather than an
  implemented theorem.

The next statistical step is a trajectory-coupled calibration over varied
conditioning and coupling regimes, followed by directional covariance bounds
that retain matrix structure lost by a spectral norm. The next modeling step is
a preregistered benchmark in which temporal transport is necessary rather than
merely available. These targets, including completion criteria, are maintained
in the [research program](research_program.md).

## Interpretation

This repository establishes a rigorous framework for a moving-boundary
identification problem and tests it on transparent synthetic systems. It does
not establish phenomenal consciousness, sentience, agency, moral status, or a
privileged decomposition of nature. Its useful contribution is narrower: the
definitions, assumptions, sufficient conditions, counterexamples, algorithms,
and numerical checks are explicit enough to be inspected and challenged.
