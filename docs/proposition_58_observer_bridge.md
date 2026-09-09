# Proposition 58: relative covariance uncertainty to world-tube recovery

## Physical question

The research program began with a moving-boundary question:

> If a subsystem is allowed to move through a larger physical system, when can its boundary be inferred from the dynamics rather than fixed in advance?

The primary conceptual starting point is Tegmark's factorization and observer-identification question in [Tegmark 2015](bibliography.md#tegmark-2015). Propositions 41 through 57 then developed a finite-sample measurement layer for temporal dependence, physical relaxation time, irregular sampling, and innovation-whitened covariance certification.

Proposition 57 reached a relative covariance radius below one for a scalar target block even when the physical relaxation time was known only through the finite-sample Proposition 55 calibration interval.

That does not yet answer the original observer question. Observer identification uses multivariate covariance blocks to evaluate integration, insulation, persistence, transport, and the complete moving world-tube objective.

The next question is therefore:

> Given a simultaneous relative covariance certificate for the blocks actually used by the observer score, can that uncertainty be propagated all the way to a rigorous path-recovery statement without spending another probability budget?

Proposition 58 answers yes.

It also exposes the next tightness frontier. On the original seven-coordinate moving-module benchmark, the required observer blocks have dimension ten and there are 175 such blocks. At that actual scale, the exact-relaxation-time Proposition 56 innovation oracle has radius

\[
\boxed{
\varepsilon_{\mathrm{oracle,obs}}
=1.8573569119>1
}
\]

with 118 residual innovation degrees of freedom.

Thus the scalar success of Propositions 56 and 57 does not automatically imply observer-scale certification. The next bottleneck is dimensional and structural, not another refinement of physical-time calibration.

---

# 1. Observer covariance blocks

Let the physical state have \(n\) measured coordinates and let every candidate subsystem contain \(s\) coordinates. At dynamical time \(t\), let

\[
S\subseteq\{1,\ldots,n\},
\qquad |S|=s.
\]

The adjacent-state covariance is ordered as

\[
\operatorname{Cov}(X_t,X_{t+1}).
\]

For a future candidate \(S\), define the observer block

\[
\boxed{
B_{t,S}
=
\bigl(X_t, X_{t+1}^{S}\bigr)
}
\]

with dimension

\[
\boxed{d_{\mathrm{obs}}=n+s.}
\]

This one block contains every covariance submatrix required for:

- directed integration inside \(S\);
- environmental leakage into future \(S\);
- persistence of \(S\);
- transport from any current source candidate into future target \(S\).

The last point is important. A transport score from source \(U\) to future target \(S\) uses the future target, the present source, and the present environment relative to \(U\). The source and its environment partition all present coordinates. Therefore the complete transport calculation is a principal calculation inside

\[
(X_t,X_{t+1}^{S}),
\]

independent of which source \(U\) is being tested.

If there are \(T\) dynamical times and \(C\) candidate boundaries, the simultaneous covariance count is consequently

\[
\boxed{B_{\mathrm{obs}}=TC,}
\]

not the much larger number of candidate-to-candidate edges.

For Experiment AS,

\[
n=7,
\qquad
s=3,
\qquad
T=5,
\qquad
C={7\choose3}=35,
\]

so

\[
\boxed{d_{\mathrm{obs}}=10,\qquad B_{\mathrm{obs}}=175.}
\]

There are 4,900 raw candidate edges, but they do not require 4,900 distinct covariance blocks.

---

# 2. Simultaneous relative covariance event

For each observer block let \(\Sigma_{t,S}\) be the population covariance and \(\widehat\Sigma_{t,S}\) its estimator. Proposition 58 starts from the simultaneous event

\[
\boxed{
\left\|
\Sigma_{t,S}^{-1/2}
(\widehat\Sigma_{t,S}-\Sigma_{t,S})
\Sigma_{t,S}^{-1/2}
\right\|_2
\le
\delta_{t,S}
<1
}
\]

for every declared time-candidate block.

The condition \(\delta_{t,S}<1\) is not interpreted as a physical transition. It is the perturbative condition under which the covariance remains uniformly positive definite relative to the population geometry and the inverse-covariance information calculations are controlled.

Proposition 57 is one way to supply such radii under the declared separable Gaussian exponential-relaxation measurement model. Proposition 58 is deliberately modular: any future theorem that supplies valid candidate-local relative radii can feed the same observer bridge.

---

# 3. Information-factor propagation

The Gaussian information quantities are standard consequences of multivariate information theory; see [Shannon 1948](bibliography.md#shannon-1948) and [Cover and Thomas 2006](bibliography.md#cover-and-thomas-2006). Canonical persistence is based on canonical correlation; see [Hotelling 1936](bibliography.md#hotelling-1936).

For one candidate-local radius \(\delta<1\), define

\[
L(\delta)=-\log(1-\delta).
\]

The existing relative-covariance perturbation chain gives the following factor radii.

## 3.1 Integration factor

For the directed-integration factor

\[
g_I=1-2^{-I_{\mathrm{dir}}/s},
\]

a valid generic error radius is

\[
\boxed{
e_I(\delta)
=
\min\{1,4L(\delta)\}.
}
\]

## 3.2 Independence factor

For environmental leakage

\[
g_E=2^{-I(X_{t+1}^{S};X_t^{\bar S}\mid X_t^S)/s},
\]

the relative-event bound gives

\[
\boxed{
e_E(\delta)
=
\min\left\{
1,
\frac{n+2s}{s}L(\delta)
\right\}.
}
\]

## 3.3 Persistence factor

Let

\[
a=(1-\delta)^{-1/2},
\qquad
b=a-1.
\]

The canonical-persistence perturbation used by the repository is

\[
e_P(\delta)
=
\min\left\{
1,
2\left[
ba(1+2\delta)+2\delta a+b
\right]
\right\}.
\]

This bound is condition-number independent because the event is stated in population-whitened coordinates.

---

# 4. From factors to local and transport scores

The local observer score is

\[
\ell_{t,S}
=
(g_Ig_Eg_P)^{1/3},
\]

and the transport score is

\[
\theta_t(U,S)
=
(g_Eg_P)^{1/2}.
\]

For nonnegative factors in \([0,1]\), the repository's positive-factor product-root perturbation theorem supplies both a zero-safe Holder bound and, when factor lower bounds remain positive, a sharper local Lipschitz bound. Proposition 58 uses the minimum valid bound candidate by candidate rather than replacing every state by one global worst case.

This detail matters because a moving-boundary problem can contain structurally very different candidates.

---

# 5. Declared structural integration nulls

Some candidates can have an exact population conditional-independence structure that forces their directed-integration factor to zero.

When such a null is declared independently of the covariance noise, the generic first-order integration error can be replaced by the repository's relative structural-null bound. The conditional canonical-correlation radius is

\[
\rho_0(\delta)
=
\frac{\delta}{1-\delta}.
\]

For \(\rho_0<1\), the resulting Gaussian conditional-information error is quadratic near zero. Since the other two local factors are at most one, the local-score error at an integration null is bounded by the cube root of the null integration-factor radius.

Experiment AS records 120 exact integration-null candidate states out of 175 population states on the controlled moving-module model.

This refinement is deterministic. It does not spend an additional failure probability.

---

# 6. Exact interval world-tube comparison

The population world-tube action has the form

\[
A(p)
=
\sum_{t=0}^{T-1}\ell_t(p_t)
+
\chi\sum_{t=0}^{T-2}\theta_t(p_t,p_{t+1})
-
\lambda\sum_{t=0}^{T-2}d(p_t,p_{t+1}).
\]

The continuity geometry \(d\) is treated as exact. The repository uses Jaccard distance for this declared geometry; see [Jaccard 1901](bibliography.md#jaccard-1901).

Let \(e^\ell_{t,S}\) and \(e^\theta_t(U,S)\) be the candidate-specific score radii obtained above. Then every path has action error

\[
E(p)
=
\sum_t e^\ell_{t,p_t}
+
|\chi|
\sum_t e^\theta_t(p_t,p_{t+1}).
\]

If \(p_*\) is the population-optimal path, define

\[
A_*^-
=
A(p_*)-E(p_*),
\]

and

\[
A_{\mathrm{comp}}^+
=
\max_{p\ne p_*}
\left[A(p)+E(p)\right].
\]

Proposition 58 certifies recovery whenever

\[
\boxed{
A_*^- > A_{\mathrm{comp}}^+.
}
\]

The competitor maximum is evaluated exactly by the same finite-horizon dynamic-programming structure used by the world-tube optimizer. Dynamic programming lineage is recorded at [Bellman 1952](bibliography.md#bellman-1952).

No path enumeration is required.

---

# 7. Probability composition

Proposition 58 adds no stochastic event.

Suppose a previous theorem establishes the complete simultaneous covariance event with probability at least

\[
1-\alpha.
\]

If Proposition 58 returns positive recovery slack on that event, then the same population world-tube is recovered with probability at least

\[
\boxed{1-\alpha.}
\]

If calibration and target covariance were obtained from independent records with respective confidence levels \(1-\alpha\) and \(1-\beta\), as in the Proposition 55 to Proposition 57 chain, then the existing combined lower bound

\[
(1-\alpha)(1-\beta)
\]

is inherited unchanged by the path statement.

There is no additional union bound over paths because the covariance event is already simultaneous over the declared observer blocks and the path comparison is deterministic conditional on that event.

---

# 8. Experiment AS: original moving-module geometry

Experiment AS returns to the first moving-module benchmark rather than introducing a new observer model.

The population problem has

\[
(0,1,2)
\to
(1,2,3)
\to
(2,3,4)
\to
(3,4,5)
\to
(4,5,6).
\]

The world-tube optimizer recovers that exact path.

The recorded population actions are

\[
A_*=1.2543238015,
\]

\[
A_{(2)}=1.1279021830,
\]

with margin

\[
\boxed{
\Delta_A=0.1264216185.
}
\]

The corresponding uniform raw score radius from the original exact runner-up certificate is

\[
0.0105351349.
\]

These are properties of the population world-tube objective, not finite-sample probabilities.

---

# 9. Observer-scale dimension audit

Proposition 56 showed that exact innovation whitening turns the target covariance problem into a Wishart problem with \(r=N-q\) unit temporal weights. The classical Wishart lineage is [Wishart 1928](bibliography.md#wishart-1928), and the matrix-Laplace concentration route used by Proposition 47 is based on [Tropp 2012](bibliography.md#tropp-2012).

For the Experiment AQ and AR target schedule,

\[
N=120,
\qquad
q=2,
\qquad
r=118.
\]

For a scalar block and one declared block, the 1024-point theta evaluation gives

\[
\varepsilon_{1,1}=0.4364443814.
\]

At the actual observer scale,

\[
d=10,
\qquad
B=175,
\]

the same exact-\(\tau\) innovation oracle gives

\[
\boxed{
\varepsilon_{10,175}=1.8573569119.
}
\]

Therefore the current relative covariance-to-information perturbation theorem cannot yet be invoked on all observer blocks at this sample scale, even before adding relaxation-time uncertainty.

This is an oracle diagnostic. It isolates dimensionality and simultaneity from calibration uncertainty.

---

# 10. Entry into the relative perturbation regime

Keeping the same block dimension, block count, confidence, and exact-\(\tau\) unit-weight matrix theorem, the smallest residual innovation count for which the numerical Proposition 47 radius falls below one is

\[
\boxed{r=346.}
\]

At that point

\[
\varepsilon_{346}=0.9991303523,
\]

whereas at \(r=345\),

\[
\varepsilon_{345}=1.0007464318.
\]

With nuisance rank two, this corresponds to \(N=348\) target rows merely to enter the current relative perturbation regime.

Crossing one is not the same as certifying the world-tube. It only makes the current inverse-covariance perturbation layer admissible.

---

# 11. Current end-to-end conservatism diagnostic

Using the complete current factor perturbation chain, candidate-specific score errors, the 120 declared structural integration nulls, and exact interval dynamic programming, the largest **uniform** relative covariance radius that still certifies the population path on this benchmark is approximately

\[
\boxed{
\delta_{\mathrm{path}}
=1.1098297465\times10^{-4}.
}
\]

If the current Proposition 47 unit-weight matrix bound is asked to reach that radius simultaneously for \(d=10\) and \(B=175\), the 1024-point theta diagnostic crosses that value at approximately

\[
\boxed{
r=21{,}165{,}400{,}697.
}
\]

This number must **not** be interpreted as a physical sample requirement.

It is a measurement of conservatism in the present theorem composition. The empirical moving-module experiments recover the planted path at vastly smaller sample scales under their own independent-trajectory sampling model. The two sampling models are different, so the counts should not be compared as if they were identical experiments.

The scientific conclusion is narrower and more useful:

> The temporal-calibration bottleneck has been displaced. The dominant remaining looseness lies in simultaneous high-dimensional covariance concentration and the propagation of those radii through information factors and path margins.

---

# 12. What Proposition 58 establishes

Proposition 58 establishes a rigorous modular bridge:

\[
\boxed{
\text{covariance event}
\Rightarrow
\text{factor intervals}
\Rightarrow
\text{score intervals}
\Rightarrow
\text{world-tube action intervals}
\Rightarrow
\text{path recovery when slack}>0.
}
\]

It also establishes an important negative result for the current benchmark:

- scalar covariance certification below one is not enough;
- exact knowledge of the physical relaxation time is not enough at the current observer-scale dimension and simultaneous block count;
- further refinement of the Proposition 55 relaxation-time interval cannot solve this observer-scale bottleneck by itself.

---

# 13. Next mathematical frontier

The Experiment AS diagnostic points to a specific next theorem rather than an open-ended search.

The highest-value improvements are now:

1. **factor-specific covariance blocks:** integration, leakage, and persistence do not all require the same maximum block dimension;
2. **screen-first simultaneity reduction:** earlier structural screening can reduce the number of covariance blocks that need the tightest certificate;
3. **candidate-local radii:** different observer candidates need not inherit one worst-case covariance radius;
4. **direct score-margin concentration:** avoid paying separately for factor perturbations when a sharper direct action comparison is available;
5. **structural-null exploitation:** preserve exact conditional-independence geometry wherever it is declared by the physical model.

This is the next natural route back toward a practically selective finite-sample theorem for the original moving-boundary problem.

---

# 14. Scope and failure conditions

Proposition 58 is conditional on:

- valid simultaneous relative covariance events for the declared observer blocks;
- relative radii below one wherever inverse-covariance perturbation is used;
- Gaussian information-factor definitions used by the repository;
- candidate boundaries and covariance blocks declared consistently;
- structural integration nulls, when used, being justified independently of the covariance noise;
- the declared world-tube score and material-continuity geometry;
- no unaccounted data-dependent candidate selection outside the certified screening rules.

The theorem does not prove that the observer score is consciousness. It does not prove that the moving-module benchmark is a model of a conscious system. The word `observer` remains operational, as defined in the repository's [Interpretation Protocol](interpretation_protocol.md).

---

# 15. Reproducibility

Implementation:

- `src/observer_math/observer_bridge.py`

Claim-level tests:

- `tests/test_observer_bridge.py`

Experiment:

- `examples/observer_bridge_dimension_audit.py`

Machine-readable record:

- `docs/observer_bridge_dimension_audit.json`

The numerical thresholds in Experiment AS are diagnostics of the current theorem chain. The probability implication in Proposition 58 comes from deterministic propagation of an already valid simultaneous covariance event and does not depend on the displayed numerical grid.
