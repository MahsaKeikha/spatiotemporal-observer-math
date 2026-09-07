# Space, time, and observer identity

The words *space*, *time*, and *observer* are easy to place beside one another
and difficult to connect without changing their meanings. This note states the
connection being investigated here and, equally importantly, where the
connection is still missing.

## 1. Space as a locality structure

In an ordinary physical model, space is supplied before the dynamics: variables
carry positions, nearby variables interact strongly, and distant variables
interact weakly. In a factorization problem, that order can be reversed. One can
ask whether a tensor-product structure is preferred because the Hamiltonian is
approximately local in that structure.

For a classical transition kernel, a first analogue is an interaction graph.
Given variables \(X_t^1,\ldots,X_t^n\), define the directed predictive weight

\[
w_{i\to j}^{(t)}=
I\!\left(X_{t+1}^j;X_t^i\mid X_t^{\{1,\ldots,n\}\setminus\{i\}}\right).
\]

This definition asks whether variable \(i\) adds unique one-step prediction of
variable \(j\) after the other present variables are known. A symmetrized graph
could use

\[
w_{ij}^{(t)}=w_{i\to j}^{(t)}+w_{j\to i}^{(t)}.
\]

Graph geodesic, resistance, or diffusion distance can then supply an induced
notion of proximity. None is automatically the correct physical distance. The
test is whether a low-dimensional, stable geometry reconstructs the interaction
structure better than an arbitrary graph does.

This graph construction is not yet implemented in the package. It is recorded
because it offers a classical test of the broader statement that perceived
locality may be tied to a factorization in which interactions become sparse and
structured.

## 2. Time as ordered predictive composition

The present model assumes an external index \(t\). It does not derive time. What
it does provide is a way to compare representations along an ordered sequence
of transition kernels

\[
K_{t:t+2}=K_{t+1:t+2}\circ K_{t:t+1}.
\]

An observer world-tube is compatible with this ordering because its transport
term compares a source representation under \(K_{t:t+1}\) with a target
representation one step later. Reversing the path generally changes both the
conditional leakage and the transition score.

A stronger treatment of temporal direction would introduce the forward and
time-reversed path measures. For a trajectory \(x_{0:T}\), a candidate entropy
production is

\[
\sigma[x_{0:T}]
=\log\frac{p(x_{0:T})}{p^{\mathrm R}(x_{T:0})}.
\]

One can then ask whether high-scoring world-tubes carry a stable internal arrow
of time, for example through positive expected entropy production or asymmetric
predictive information. That relationship has not been established.

## 3. Identity as transport, not material sameness

If the same physical variables must remain inside the boundary, identity is
reduced to membership. The present construction instead separates two notions:

- **material continuity**, represented by Jaccard overlap
- **organizational continuity**, represented by canonical predictive transport

These can disagree. A process may retain most of its variables while losing its
predictive organization, or move into new variables while preserving a
predictive representation. The world-tube action makes the trade visible rather
than deciding it by definition.

The exact runner-up is important here. If many materially different paths have
nearly the same action, the calculation does not support a sharply individuated
identity. The action margin is therefore part of the result, not merely a
numerical diagnostic.

## 4. Where consciousness enters, and where it does not

Integration, insulation, persistence, and nontrivial dynamics may be relevant
to theories of consciousness. Their presence is not sufficient to establish
phenomenal experience. The current mathematics identifies a type of organized
dynamical process and says nothing direct about whether there is something it is
like to be that process.

Any future bridge would need an additional statement with empirical content.
For example, one might hypothesize that changes in reported conscious level are
better predicted by world-tube stability than by fixed-boundary integration.
That would be a testable neuroscientific claim. It is not a consequence of the
definitions and is not made here.

## 5. The combined geometric picture

The long-term mathematical object is a curve of factorizations

\[
\gamma:t\mapsto F_t,
\qquad
F_t:\mathcal H\cong\mathcal H_{S_t}\otimes\mathcal H_{E_t}.
\]

Three structures would then meet in one construction:

1. A factorization \(F_t\) defines candidate objects and a notion of locality.
2. Dynamics transports states and observables between consecutive
   factorizations.
3. An action selects paths that retain integrated, insulated organization while
   paying for genuine factorization drift.

A schematic continuous action would have the form

\[
\mathcal A[\gamma]=
\int_0^T
\left[
\alpha\,\mathcal J(F_t)
-\beta\,\mathcal L(F_t)
+\chi\,\mathcal P(F_t,\dot F_t)
-\lambda\|\dot F_t^{\mathrm{hor}}\|_g^2
\right]dt.
\]

Here \(\dot F_t^{\mathrm{hor}}\) is intended to remove local-basis motion and
retain only motion that changes the factorization. At present, this equation is
a specification problem, not an implemented model. Each symbol still requires
a quantum definition that is gauge invariant and operationally motivated.

## 6. Questions that decide whether this picture is useful

- Does conditional-predictive geometry recover ordinary spatial locality in
  systems where the answer is known?
- Can organizational transport remain high when material overlap is zero, and
  can that result be distinguished from common external drive?
- Does the path margin collapse in systems with genuinely ambiguous identity?
- Is there a connection on factorization space whose parallel transport has an
  observable operational meaning?
- Can the classical Gaussian action be obtained as a limit of a quantum
  relative-entropy or Fisher-information construction?
- Does an internal arrow of time follow from the same path that maximizes
  organized predictive persistence, or are the two independent?

Negative answers would be informative. They would show which parts of the
space-time-observer analogy are mathematical structure and which are only
suggestive language.
