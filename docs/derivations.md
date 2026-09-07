# Derivations and computational definitions

This note fixes the notation used by the code. All random variables are real,
all logarithms in information quantities are base two, and covariance matrices
are assumed positive definite unless a limiting argument is stated.

## 1. Time-varying Gaussian dynamics

Let \(X_t\in\mathbb R^n\) obey

\[
X_{t+1}=A_tX_t+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal N(0,Q_t),
\qquad
\varepsilon_t\perp X_t.
\]

If \(\Sigma_t=\operatorname{Cov}(X_t)\), then

\[
\Sigma_{t+1}=A_t\Sigma_tA_t^\mathsf T+Q_t,
\qquad
\operatorname{Cov}(X_t,X_{t+1})=\Sigma_tA_t^\mathsf T.
\]

Thus the adjacent-time joint covariance is

\[
\Gamma_t=
\begin{pmatrix}
\Sigma_t & \Sigma_tA_t^\mathsf T\\
A_t\Sigma_t & \Sigma_{t+1}
\end{pmatrix}.
\]

Nothing in this recursion requires \(A_t\) or \(Q_t\) to be constant. The
stationary helper in the package is used only when a fixed model is explicitly
requested or when an initial covariance is needed.

## 2. Gaussian information quantities

For a Gaussian vector \(Z\in\mathbb R^k\) with covariance \(\Sigma_Z\),

\[
h(Z)=\frac{1}{2}\log_2\left[(2\pi e)^k\det\Sigma_Z\right].
\]

The constants cancel in mutual information. For subvectors \(X\) and \(Y\),

\[
I(X;Y)=\frac{1}{2}\log_2
\frac{\det\Sigma_X\det\Sigma_Y}{\det\Sigma_{XY}}.
\]

For a conditioning vector \(Z\),

\[
I(X;Y\mid Z)=\frac{1}{2}\log_2
\frac{
\det\Sigma_{XZ}\det\Sigma_{YZ}
}{
\det\Sigma_Z\det\Sigma_{XYZ}
}.
\]

The implementation evaluates log determinants from eigenvalues rather than
forming determinants directly. Eigenvalues below
\(10^{-12}\max(1,\lambda_{\max})\) are floored. This prevents numerical failure
near singularity, but it also means results for badly conditioned covariances
must be treated as regularized quantities.

## 3. Internal directed integration

Take a candidate subsystem \(S\subset\{0,\ldots,n-1\}\). For every nontrivial
bipartition \(S=U\sqcup V\), define

\[
J_t(U,V)=
I(X^{t+1}_U;X^t_V\mid X^t_U)
+I(X^{t+1}_V;X^t_U\mid X^t_V).
\]

Each term asks whether one side improves prediction of the other side's future
after that side's own present is known. The weakest internal cut is

\[
\mathcal J_t(S)=\frac{1}{|S|}
\min_{U\sqcup V=S}J_t(U,V).
\]

Only one of the two labelings \((U,V)\) and \((V,U)\) is evaluated. The search is
exponential in \(|S|\), which is acceptable for the small exact examples here
but not for large systems. A singleton has no nontrivial bipartition and is
assigned zero directed integration.

For comparison, the code also records the weakest instantaneous mutual
information,

\[
\mathcal I_t(S)=\frac{1}{|S|}
\min_{U\sqcup V=S}I(X^t_U;X^t_V).
\]

This static value is diagnostic only. It does not enter the final score.

## 4. Environmental leakage

Let \(\bar S\) be the variables outside \(S\). The fixed-boundary leakage is

\[
\mathcal L_t(S)=\frac{1}{|S|}
I(X^{t+1}_S;X^t_{\bar S}\mid X^t_S).
\]

It measures predictive input from the current environment that is not already
contained in the subsystem's present. It does not measure every possible form
of dependence on the environment. In particular, it ignores future-to-future
coupling and latent variables not represented in \(X_t\).

The two information rates are mapped to \([0,1]\):

\[
G_t(S)=1-2^{-\mathcal J_t(S)},
\qquad
K_t(S)=2^{-\mathcal L_t(S)}.
\]

The first map increases from zero with integration. The second decreases from
one with leakage. Their exponential forms keep the units explicit: one bit per
node maps to \(1/2\) in either direction.

## 5. Predictive persistence

Let \(C_{XY}=\operatorname{Cov}(X,Y)\). The canonical correlations between
vectors \(X\) and \(Y\) are the singular values of

\[
M=\Sigma_X^{-1/2}C_{XY}\Sigma_Y^{-1/2}.
\]

If \(r=\min(\dim X,\dim Y)\), define

\[
P(X,Y)=\frac{1}{r}\sum_{i=1}^r\rho_i^2.
\]

For a fixed boundary, \(X=X_S^t\) and \(Y=X_S^{t+1}\). Canonical correlations
are unchanged by invertible linear coordinate transformations made separately
inside \(X\) and \(Y\). This is why the code uses them instead of a Euclidean
difference between covariance entries or transition coefficients.

The local score is the geometric mean

\[
\Omega_t(S)=\left[G_t(S)K_t(S)P(X_S^t,X_S^{t+1})\right]^{1/3}.
\]

The geometric mean makes any zero factor decisive and keeps the score in
\([0,1]\). The equal exponents are a modeling choice, not a theorem. They should
eventually be tested against weighted alternatives.

## 6. Transport between different boundaries

For source \(S\) at time \(t\) and target \(R\) at time \(t+1\), transport
persistence is

\[
P_t(S\to R)=P(X_S^t,X_R^{t+1}).
\]

The corresponding leakage is conditioned on the entire source representation:

\[
L_t(S\to R)=\frac{1}{|R|}
I(X_R^{t+1};X_{\bar S}^t\mid X_S^t).
\]

The implemented transition score is

\[
\Theta_t(S\to R)=
\sqrt{P_t(S\to R)\,2^{-L_t(S\to R)}}.
\]

A high canonical correlation is therefore insufficient when the same future
target is substantially predicted by variables outside the proposed source.
This definition is directional: \(\Theta_t(S\to R)\) need not equal
\(\Theta_t(R\to S)\), and the reverse expression generally refers to a
different pair of times.

The package retains `structural_transport` as a transparent coefficient-based
baseline. It is coordinate dependent and is not used in the reported
nonstationary experiment.

## 7. World-tube objective

Let \(\mathcal C=\{S^{(1)},\ldots,S^{(C)}\}\) be a finite candidate set. A path
is \(p=(j_0,\ldots,j_{T-1})\), where \(j_t\) selects one candidate at time \(t\).
For local weight one, transport weight \(\chi\), and continuity weight
\(\lambda\), the discrete action is

\[
A(p)=
\sum_{t=0}^{T-1}\Omega_t(S^{(j_t)})
+\chi\sum_{t=0}^{T-2}\Theta_t(S^{(j_t)}\to S^{(j_{t+1})})
-\lambda\sum_{t=0}^{T-2}d_J(S^{(j_t)},S^{(j_{t+1})}),
\]

where

\[
d_J(S,R)=1-\frac{|S\cap R|}{|S\cup R|}
\]

is Jaccard distance. This regularizer expresses a weak preference for material
continuity without requiring permanent membership.

## 8. Exact dynamic program

Define \(V_t(j)\) as the best action of a partial path ending at candidate \(j\)
at time \(t\). Then

\[
V_0(j)=\Omega_0(S^{(j)}),
\]

and

\[
V_t(j)=\Omega_t(S^{(j)})+
\max_i\left[
V_{t-1}(i)+\chi\Theta_{t-1}(S^{(i)}\to S^{(j)})
-\lambda d_J(S^{(i)},S^{(j)})
\right].
\]

Backpointers recover the global optimum. The runtime is \(O(TC^2)\); exhaustive
enumeration would require \(C^T\) paths. The certificate routine keeps the best
two distinct partial histories ending at every candidate, which is sufficient
to recover the exact global runner-up with the same asymptotic complexity.

## 9. Robustness certificate

Let \(m\) be the action difference between the best and second-best paths. If
every local and raw transport score is perturbed by at most \(\epsilon\), the
action of a path can change by at most

\[
B\epsilon=\left[T+|\chi|(T-1)\right]\epsilon.
\]

The difference between two paths can therefore change by at most
\(2B\epsilon\). The winning path is certified unchanged whenever

\[
\epsilon<\frac{m}{2[T+|\chi|(T-1)]}.
\]

This bound concerns errors in already-computed scores. Turning it into a
confidence statement about finite data requires a separate perturbation bound
from estimated covariances to information scores.

## 10. Recovery conditions

Two different recovery statements are implemented.

The componentwise condition asks the planted initial state and every planted
edge to beat all alternatives separately. If the smallest component margin is
positive, the sum of those components is uniquely maximized by the planted
path. This condition is easy to inspect but can fail even when the planted path
is the correct global optimum.

The finite-sample condition begins with the exact population action margin
\(m\). If estimated scores have uniform errors \(\epsilon_L\) and
\(\epsilon_\Theta\), then any action difference changes by at most

\[
2\left[T\epsilon_L+|\chi|(T-1)\epsilon_\Theta\right].
\]

The population path is therefore retained when \(m\) is larger than this
quantity. If the uniform error event has probability at least \(1-\alpha\), the
same probability lower bound applies to path recovery. Full statements and
proofs are in [Proved results and open problems](proofs_and_conjectures.md).

For the conditional-information part, a spectral covariance error
\(\eta<m=\lambda_{\min}(\Gamma)\) gives the explicit bound

\[
|\widehat I(X;Y\mid Z)-I(X;Y\mid Z)|
\leq
\frac{d_X+d_Y+2d_Z}{\ln 2}
\left[-\ln\left(1-\frac{\eta}{m}\right)\right].
\]

Proposition 8 supplies the corresponding perturbation bound for mean squared
canonical correlation. Proposition 9 combines both bounds with Gaussian
sample-covariance concentration and the path margin. Its global cube-root bound
is valid near zero-score candidates but extremely conservative in the current
experiment.

Proposition 10 replaces the cube-root or square-root Hölder step by a local
Lipschitz bound whenever the relevant population factors remain above their
error radii. Proposition 11 assigns these errors to individual candidates and
compares the population path's lower action against the exact maximum upper
action of every competitor. Proposition 12 constructs the entire certificate
from \(A_t,Q_t,\Sigma_0\), the candidate family, and the action weights.

## 11. Identifiability rather than label recovery

A coordinate label is not automatically a physical identity. The implemented
orbit map takes a finite group \(G\) of admissible node relabelings and replaces
a path \(p\) by a canonical representative of \([p]=\{gp:g\in G\}\). If the
trajectory law and action are invariant under \(G\), only this orbit can be
identified from the objective.

The stronger obstruction is distributional. If two models have incompatible
correct path orbits but observation laws within total variation \(\tau\), the
sum of their recovery probabilities is at most \(1+\tau\). Thus the maximin
success probability is at most \((1+\tau)/2\). At \(\tau=0\), no observational
algorithm can exceed one-half success on both models without additional
assumptions or interventions.

## 12. Near-competitor graph

Given score-error radii, the population winner has the lower action
\(L^*=A(p^*)-b(p^*)\). A forward-backward max-sum pass computes the largest
inflated action \(U_{tj}\) of a path constrained to every state \((t,j)\), and
similarly for every edge. States and edges with \(U<L^*\) cannot occur in an
empirical winner on the error event. This converts an exponential path family
into a sufficient time-indexed subgraph without enumerating paths.

## 13. Closed-form moving-clique family

For the structured transition in Proposition 16, choosing
\(Q_t=I-A_tA_t^\mathsf T\) preserves \(\Sigma_t=I\). Every conditional
information determinant becomes the determinant of an equicorrelated residual
matrix. A \(k\)-row residual after conditioning on \(r\) active columns has
determinant

\[
D(k,r)=(1-d_r+o_r)^{k-1}[1-d_r-(k-1)o_r],
\]

where \(d_r=\alpha^2+(r-1)\beta^2\) and
\(o_r=2\alpha\beta+(r-2)\beta^2\). These determinants give the exact weakest-cut
integration. Identity covariance also reduces persistence to normalized
transition energy, \(\alpha^2+(s-1)\beta^2\). The final recovery inequality
compares this closed-form local score with the maximum two incident-edge gain.
For equal-size consecutive boundaries with overlap \(r\), their Jaccard distance
is \(1-r/(2s-r)\), so the sufficient condition explicitly rewards smoothly
overlapping motion.

## 14. Perturbation neighborhood of the moving-clique family

Write the actual dynamics as \(A_t=A_t^0+E_t\) and
\(Q_t=Q_t^0+F_t\), with operator-norm radii \(\gamma\) and \(\nu\). The base
covariance remains the identity, but the actual covariance need not. If
\(\rho=\|A_t^0\|_2\), \(a=\rho+\gamma<1\), and

\[
c=2\rho\gamma+\gamma^2+\nu,
\]

then its deviation is controlled by the finite-horizon recursion

\[
\delta_0=0,
\qquad
\delta_{t+1}=a^2\delta_t+c.
\]

The cross-covariance block differs from its base value by at most
\(a\delta_t+\gamma\). Combining this with the two diagonal-block bounds gives
an explicit operator-norm radius \(\eta_t\) for each adjacent covariance. This
single radius can be propagated through all principal covariance blocks used by
the score.

The resulting robust theorem uses three factor errors: \(e_G\) for directed
integration, \(e_K\) for insulation, and \(e_P\) for canonical persistence.
The planted score is lower bounded through the positive-factor result. For an
incorrect candidate, isolating one outside node gives a cut whose base
conditional cross-covariances vanish in both directions. Perturbing the
conditional covariance formula and whitening its two residual blocks gives a
partial canonical-correlation bound \(z_\eta\). The incorrect integration and
score are then bounded by

\[
G_{\mathrm{wrong}}\leq1-(1-z_\eta^2)^{1/s},
\qquad
\Omega_{\mathrm{wrong}}leq G_{\mathrm{wrong}}^{1/3}.
\]

The integration bound is second order in \(z_\eta\) near zero. This asymmetry
is why the proof uses a positive-factor perturbation bound for the planted score
and a zero-cut partial-correlation bound for incorrect scores.

The derivation is finite horizon and deterministic. It does not assume that the
perturbations are random, independent across time, or aligned with the planted
module. Its cost is conservatism: arbitrary operator-norm directions are
protected simultaneously.

## 15. Candidate-local covariance compression

The global radius \(\eta_t\) protects directions that a particular candidate
score never uses. For a coordinate set \(D\), principal compression gives

\[
\|\Pi_D(\Gamma_t-\Gamma_t^0)\Pi_D^\mathsf T\|_2
\leq \|\Gamma_t-\Gamma_t^0\|_2.
\]

The inequality can be strict when the perturbation is spatially structured.
The support-resolved certificate therefore recomputes the spectral error on
three kinds of blocks: the planted present-future block used by integration and
persistence, the planted present-population/future-subset block used by
leakage, and each incorrect candidate's present-future block. The same
log-determinant and partial-correlation lemmas then apply without changing
their proofs.

This localization also retains the candidate's base-block spectrum. That
spectrum depends on \(|C\cap S_t^*|\), so candidates with different planted
overlap need not receive the same bound. Finally, the path proof charges the
actual planted-edge bound to its incident mismatched times. Endpoints incur one
charge and interior times at most two, instead of imposing the worst two-edge
charge at every time.

The calculation needs the realized \(A_t,Q_t\) and enumerates
\(\binom ns\) candidates. It is consequently an exact diagnostic for small
families, not a scalable or purely radius-based guarantee.

## 16. Row-local bounds before covariance propagation

The realized compression can itself be bounded from the perturbation matrices.
For \(\Delta_t=\Sigma_t-I\), the identity

\[
\Delta_{t+1}=A_t\Delta_tA_t^\mathsf T+H_t,
\qquad
H_t=A_tA_t^\mathsf T+Q_t-I,
\]

separates amplification of earlier covariance error from the new forcing. The
global recursion

\[
\delta_{t+1}=\|A_t\|_2^2\delta_t+\|H_t\|_2
\]

controls the first term. After selecting rows \(D\), the sharper one-step
quantity

\[
\|\Pi_DA_t\|_2^2\delta_t+
\|\Pi_DH_t\Pi_D^\mathsf T\|_2
\]

controls the next state covariance only where candidate \(D\) will use it.
Combining present, future, and cross-covariance block bounds through the
largest eigenvalue of a two-by-two nonnegative matrix gives the complete
candidate joint radius in Proposition 21.

This procedure never computes \(\Sigma_t\). It still uses a global scalar
\(\delta_t\) for influence arriving through unselected coordinates, but keeps
row-local transition norms, local forcing, and within-candidate transition
perturbations. A supplied candidate family reduces the calculation from
\(\binom ns\) subsets to its declared members. The resulting claim is only
relative to that family unless it is complete.

## 17. Overlap classes as sufficient statistics for the bound

For the covariance-preserving moving clique, a candidate's base transition
norms depend only on \(q=|C\cap S_t^*|\). The same remains true for conservative
perturbation control when row, within-candidate, and local-noise norms are
supplied as class budgets. This converts a list of \(\binom ns\) candidate
radii into at most \(s+1\) rows per time.

The only temporal complication is that the current covariance error was
created under the preceding planted boundary. It therefore depends on a pair
\((p,q)\) of consecutive overlaps. Four disjoint occupancy cells determine
whether the pair is possible: the planted intersection, the previous-only and
current-only regions, and the outside region. Proposition 22 eliminates the
cell count to obtain a closed integer interval for the shared occupancy. A
pair is feasible precisely when that interval contains an integer.

The resulting certificate needs \(O(Ts^2)\) class-pair checks. This is a
complexity statement about evaluating valid budgets, not about obtaining them.
Exact class maxima can still be expensive for unstructured matrices. Scalable
applications must derive them from assumptions such as bounded row energy,
sparsity, locality, or graph degree. The small committed example enumerates
candidates only to audit that the compressed bound dominates every member.

## 18. Two-type sparse comparison matrices

An entry bound alone scales with block dimension, while a degree bound alone
does not control amplitude. Proposition 23 combines them. For each block of a
matrix, its maximum row sum is bounded by entry magnitude times row degree,
and its maximum column sum is bounded by entry magnitude times column degree.
Their geometric mean controls the block spectral norm.

The four block norms form a nonnegative two-by-two comparison matrix. Its
spectral norm bounds the full operator because the Euclidean norms of the two
input groups behave as a two-dimensional vector under block multiplication.
Substituting the population counts \((s,n-s)\) gives global bounds. Substituting
the candidate counts \((q,s-q)\) on the row side or on both sides gives the
row-local and within-candidate budgets required by Proposition 22.

This step uses only entry envelopes and support degrees relative to the
planted inside/outside partition. It does not inspect the matrices or list the
candidates. The price is conservatism: signs, cancellation, detailed support
geometry, and correlations among blocks are discarded.

## 19. Block-local covariance propagation

The scalar covariance radius in Propositions 19 through 23 forgets where an
error originates. A block comparison matrix retains that information. Its
entry \(D_t(a,b)\) bounds the spectral norm of the covariance-error block
between coordinate groups \(V_a\) and \(V_b\).

If \(B_t(a,b)\) bounds the corresponding block of the transition, block
multiplication gives

\[
D_{t+1}=B_tD_tB_t^\mathsf T+G_t.
\]

This is ordinary nonnegative matrix arithmetic on the block graph. Zeros are
meaningful: multiplication cannot create support outside time-respecting paths.
A forcing term at a remote graph block therefore has an exact finite influence
cone. The global spectral bound can become positive immediately while a local
joint-covariance bound remains zero until that cone arrives.

The cross-covariance error uses one transition rather than two, giving
\(C_t=B_tD_t+R_t\). Present and future block restrictions are assembled into
one comparison matrix whose spectral norm bounds the local adjacent-joint
error. This makes the output directly usable by the covariance-to-score
perturbation results.

## 20. Moving partitions as a layered block graph

A common refinement is unnecessary when the partition changes. At time \(t\),
let \(D_t\) be square on the current \(m_t\) blocks and let \(B_t\) be a
rectangular \(m_{t+1}\times m_t\) comparison from current blocks to future
blocks. The same recursion remains conformable:

\[
D_{t+1}=B_tD_tB_t^\mathsf T+G_t.
\]

This construction works directly on a layered graph. A split is represented
by several future rows receiving edges from one present column. A merge is
represented by one future row receiving edges from several present columns.
Reassignment changes only the edges between two adjacent layers. None of these
operations requires tracking a node's complete membership history.

The support expansion is a sum over paired directed paths through this layered
graph. Consequently, a local covariance block can become nonzero only after
both sides of the forcing block have a time-respecting route to it. The
rectangular cross recursion \(C_t=B_tD_t+R_t\) supplies the corresponding
present-to-future joint bound.

## 21. Choices that are still choices

Several parts of the construction are intentionally exposed rather than hidden
inside the implementation:

- the minimum bipartition rather than an average or soft minimum
- per-node normalization
- the exponential maps from bits to bounded factors
- equal weighting inside each geometric mean
- Jaccard distance for physical membership
- a finite, fixed-size candidate family

Changing any of them defines a related but different model. A useful extension
must show which conclusions survive those changes.
