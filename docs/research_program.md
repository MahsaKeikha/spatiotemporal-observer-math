# Research program

This page is a working queue. Items are ordered by what the present results need,
not by how ambitious they sound.

## Immediate problem: recovery from finite data

The current calculation starts from exact covariances. Real data provide a
finite trajectory, so \(A_t\), \(Q_t\), or the joint covariance must be
estimated. The next experiment should answer a concrete question:

> How many observations are required before the recovered path and its
> runner-up margin stabilize?

The experiment should vary sample length, dimension, condition number, and
regularization. Bootstrap path frequencies can be reported, but they must not be
confused with the deterministic radius already implemented. A useful theoretical
result would propagate a covariance concentration bound through log determinant,
conditional mutual information, canonical correlation, and finally the path
margin.

Completion criterion: recovery curves with uncertainty bands on held-out random
systems, plus a documented regime in which the method fails.

## Immediate problem: a benchmark that is difficult to win

The existing moving module is smooth, fixed in size, and analytically observed.
A credible benchmark needs at least the following axes:

| Axis | Cases to include |
| --- | --- |
| Signal | internal coupling from indistinguishable to dominant |
| Noise | independent, correlated, anisotropic, and time varying |
| Motion | no motion, gradual replacement, abrupt jumps, split, and merge |
| Observation | complete, missing variables, latent common drive |
| Dynamics | linear Gaussian, nonlinear, and non-Gaussian |
| Candidate family | correct size, wrong size, and variable size |

Weights must be selected on training families and evaluated on separately
generated test families. A method that requires knowledge of the planted path to
choose \(\chi\) or \(\lambda\) has not solved the identification problem.

Completion criterion: versioned benchmark generator, fixed evaluation protocol,
and all seeds recorded.

## Mathematical problem: planted-path recovery

The natural theorem is not simply that dynamic programming returns an optimum;
that part is exact already. The harder statement is that the intended path is the
optimum under interpretable assumptions on the dynamics.

One route is to derive a local separation condition. Let \(p^*\) be the planted
path. If every deviation segment loses more local and transport score than it
can gain by reducing continuity cost, then \(p^*\) is the unique maximizer. The
useful version must express that separation in terms of \(A_t\), \(Q_t\), and
candidate overlap rather than in terms of scores assumed after the fact.

Completion criterion: a theorem with non-vacuous parameters, a matching failure
example near its boundary, and a numerical check of tightness.

## Comparative problem: what is gained by moving the boundary?

The relevant alternatives do not all solve the same problem, so comparison must
separate objectives from outputs.

- A fixed-cut method should be evaluated on the best single boundary across the
  full horizon.
- Dynamic community detection should receive the same time-indexed coupling
  information where possible.
- Dynamical independence should be compared on information closure and the
  macroscopic process it extracts.
- Integrated-information decompositions should be evaluated on the same
  multivariate transitions without implying that their information atoms are
  interchangeable with the present score.

The important outcome is not a single leaderboard. It is a map of cases in which
the methods agree, disagree for a principled reason, or become mathematically
equivalent.

Completion criterion: identical generative systems, explicit hyperparameter
budgets, and no claim of advantage when the objectives differ.

## Geometric problem: factorization paths

The quantum extension needs a well-defined configuration space before it needs a
large simulation. For total Hilbert dimension \(n=de\), candidate factorizations
can be represented by global unitaries, but local transformations in
\(U(d)\otimes U(e)\) should not create a new physical factorization. The main
questions are:

1. What is the exact quotient after stabilizers and discrete factor exchange are
   included?
2. Which metric is operationally justified rather than merely convenient?
3. Can a connection separate local-basis motion from system-environment mixing?
4. Does the resulting transport have nontrivial holonomy, and what would that
   mean for a closed path of representations?

Completion criterion: a finite-dimensional construction checked on two-qubit
and two-qutrit examples, including explicit gauge transformations that leave all
reported quantities unchanged.

## Physical problem: avoiding dynamically empty factorizations

Independence can be maximized by a representation in which little happens. The
current classical score addresses this by multiplying insulation with internal
cross-prediction and persistence. The quantum analogue must make the same trade
without inserting a preferred basis by hand.

Completion criterion: reproduce a case where separability alone selects a
dynamically trivial factorization, then show precisely when the path functional
selects a nontrivial alternative. A counterexample in which it still fails is
equally important.

## Empirical contact

Application to neural, biological, or artificial-agent data should wait until
the finite-sample and latent-confounder tests are in place. When that point is
reached, the first empirical question should be whether the inferred path is
stable and predictively useful, not whether it indicates consciousness.

## Completed foundation

- exact stationary and nonstationary Gaussian covariance calculations
- static and conditional Gaussian information quantities
- weakest-cut directed integration
- representation-invariant canonical transport within source and target blocks
- environmental leakage across a changing boundary
- exact global and runner-up world-tube inference
- deterministic perturbation certificate
- correlation-only and external-drive controls
- one planted moving-boundary calculation and regularization scan
