# Research program

This page is a working queue. Items are ordered by what the present results need,
not by how ambitious they sound.

## Immediate problem: useful confidence bounds for finite data

The first finite-sample benchmark estimates adjacent covariances from
independent trajectory ensembles. Proposition 9 now gives an analytical
end-to-end confidence guarantee, but its global worst-case constants are far too
large to describe the observed recovery curve. The next question is:

> Which local spectral and score margins determine the practical number of
> observations required for path recovery?

Propositions 7 through 12 propagate Gaussian sample-covariance concentration
through conditional mutual information, canonical persistence, positive-factor
score stability, and an exact adversarial-path comparison. Candidate-local
spectra reduce the example's 95% sufficient count from
\(1.263\times10^{19}\) to \(3.132\times10^{12}\). The bound remains roughly ten
orders of magnitude above the empirical scale. Proposition 15 now identifies a
provably sufficient near-competitor graph. Propositions 32 and 33 now give an
independent two-stage route from Gaussian screening concentration to a random
safe graph and then to retained-block certification. Its zero-safe local-score
radius still contracts too slowly to explain the empirical scale. A separate
treatment is also needed for one dependent time series because the current
simulation uses independent trajectories.

Completion criterion: a valid screened concentration theorem, numerical
coverage checks across signal regimes, and a documented account of every
remaining source of looseness.

## Immediate problem: a benchmark that is difficult to win

The existing moving module is smooth, fixed in size, and easy to distinguish
locally once covariance estimates stabilize. The finite-sample comparison shows
that independent local selection can outperform the full transport objective on
this family. A benchmark that tests transport itself therefore needs at least
the following axes:

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

Proposition 5 now gives a transparent score-space sufficient condition, and the
current example shows that it is not necessary. The useful next version must
express separation in terms of \(A_t\), \(Q_t\), and candidate overlap rather
than in terms of scores assumed after the fact.

Propositions 17 through 19 extend the exact moving-clique result to a uniform
finite-horizon neighborhood with bounded external coupling and anisotropic
process noise. Incorrect candidates may now have positive local scores. The
zero-cut partial-correlation bound gives the correct quadratic local scaling,
but still controls every incorrect candidate through one global covariance
radius. Proposition 20 gives a realized-system refinement based on candidate
overlap, local covariance compression, and exact incident edge penalties. The
row-local recursion in Proposition 21 derives conservative local errors from
the structured perturbation matrices without propagating the actual
covariance, and can operate on a declared reduced candidate family. The next
two results replace full perturbation matrices by graph-degree summaries and
then propagate covariance errors on fixed or changing block partitions.
Rectangular comparisons between consecutive layers avoid a common refinement
when blocks split, merge, or change membership. The next recovery theorem
now connects these layered local radii directly to candidate-local score and
action margins. Proposition 27 combines this result with overlap classes
without explicitly listing candidate block unions when factors are exactly
class-constant. Proposition 28 replaces exact symmetry by componentwise factor
intervals, expands them using separate local and edge covariance envelopes, and
retains the \(O(TK^2)\) mismatch-state calculation. Proposition 29 now derives
those intervals from representative covariance models and certified class
residual radii. Proposition 30 obtains the residual radii from moving block
transition, forcing, and cross-error comparisons plus future class selections.
Proposition 31 now permits source-specific present compression while charging
a certified conditional-information tail for the omitted environment.
Proposition 32 composes any proved first-stage screening event with an
independent certification sample and reports the product confidence.
Proposition 33 now derives that first-stage event from screening-sample Gaussian
covariance bounds and propagates it through the complete score. The next
priority is to measure coverage and retained-graph size across signal regimes,
then replace the zero-safe worst-case radius by a sharper factor-aware bound
without losing post-selection validity.

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
- componentwise planted-path recovery theorem
- finite-sample recovery theorem conditional on uniform score bounds
- explicit covariance-to-Gaussian-CMI perturbation bound
- explicit covariance-to-canonical-persistence perturbation bound
- end-to-end Gaussian path-recovery guarantee with a computable sample threshold
- positive-factor geometric-score perturbation theorem
- candidate-local exact adversarial-path recovery certificate
- direct parameter-to-certificate computation from \(A_t,Q_t,\Sigma_0\)
- path identifiability modulo an admissible permutation group
- total-variation impossibility bound for incompatible observational models
- sufficient near-competitor state-edge graph with \(O(TC^2)\) screening
- closed-form moving-clique score and action-margin theorem in \(\alpha,\beta,Q_t\)
- covariance propagation and planted-path recovery under bounded external
  transition coupling and anisotropic process noise
- support-resolved recovery from candidate-local covariance blocks and exact
  incident planted-edge penalties
- a priori row-local recovery from structured perturbation matrices without
  actual covariance propagation
- matrix-free recovery from overlap-indexed perturbation budgets with
  \(O(Ts^2)\) certificate evaluation over the complete fixed-size family
- direct derivation of those budgets from two-type entry bounds and bounded
  row and column support, without storing perturbation matrices
- block-local covariance and adjacent-joint perturbation propagation with an
  exact finite-horizon influence-cone guarantee
- moving-partition covariance influence cones using rectangular comparisons,
  without common refinement or membership-history enumeration
- deterministic propagation of moving-partition covariance radii through all
  observer-score factors and the adversarial path-recovery dynamic program
- class-compressed robust recovery with a mismatch-state dynamic program and
  arbitrary-size overlap multiplicities
- interval-certified class recovery allowing bounded within-class factor
  heterogeneity and signed transport weights
- covariance-residual derivation of factor intervals with separate population
  heterogeneity and observation-error stages
- structural derivation of class covariance residuals from moving block
  comparison envelopes and declared future class geometry
- source-specific environmental screening with an explicit omitted conditional
  information penalty
- independent sample-split confidence composition with explicit stagewise
  failure budgets and a minimal certification-sample threshold
- Gaussian first-split screening safety derived from covariance concentration,
  factor perturbation, and a two-stage triangle inequality
- empirical covariance estimation from independent trajectory ensembles
- finite-sample recovery curves with Wilson intervals across 192 trials
- fixed, independent-local, continuity-only, and coefficient-transport baselines
- correlation-only and external-drive controls
- one planted moving-boundary calculation and regularization scan
