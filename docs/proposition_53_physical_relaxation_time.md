# Proposition 53: sampling-consistent physical relaxation time

## Physical question

A measured physical process can be sampled quickly, slowly, or at irregular times. A physically meaningful temporal parameter should not become a different property of the system merely because the acquisition clock changes.

For a simple exponentially relaxing stationary process, the natural physical parameter is a relaxation time

\[
\tau>0,
\]

with units of time.

The central question is:

> **Can the temporal covariance model be written so that the same physical relaxation time survives changes in sampling interval, time units, missing samples, and irregular measurement times, while still entering the finite-sample covariance certification machinery developed earlier in the repository?**

Proposition 53 answers that question for the exponential relaxation kernel. The extension below also proves that, on an arbitrary increasing time grid, the dense covariance has an exact nearest-neighbor Gaussian Markov representation.

This is a sampling-physics theorem. It does not assert that every real system has a single exponential relaxation time. Oscillatory dynamics, multiple decay times, colored forcing, nonstationarity, and nonlinear memory can require richer temporal models.

## Measurement model

Let physical sample times be

\[
t_1<t_2<\cdots<t_N.
\]

For a declared relaxation time \(\tau>0\), define

\[
K_\tau(t_i,t_j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

The corresponding temporal covariance matrix is

\[
R_\tau
=
\left[K_\tau(t_i,t_j)\right]_{i,j=1}^N.
\]

The diagonal entries are one, so this is a correlation model. The physical time differences \(|t_i-t_j|\), rather than the integer difference between sample labels, determine temporal similarity.

## Statement 1: uniform sampling gives the AR(1) form exactly

Suppose

\[
t_i=i\Delta t.
\]

Then

\[
R_\tau(i,j)
=
\exp\left(-\frac{|i-j|\Delta t}{\tau}\right)
=
\phi_{\Delta t}^{|i-j|},
\]

where

\[
\boxed{
\phi_{\Delta t}
=
\exp\left(-\frac{\Delta t}{\tau}\right)
}.
\]

Therefore the discrete AR(1) coefficient is a sampling-dependent representation of the physical relaxation time, not the physical time constant itself.

Whenever \(0<\phi_{\Delta t}<1\),

\[
\boxed{
\tau
=
-\frac{\Delta t}{\log\phi_{\Delta t}}
}.
\]

### Physical meaning

If the experimenter changes \(\Delta t\), the numerical value of \(\phi\) changes even when the physical process is unchanged. The recovered \(\tau\) should remain the same if a one-timescale exponential relaxation model is appropriate.

## Statement 2: exact coarse-sampling consistency

If the same process is observed every \(k\)-th fine sample, then the coarse sampling interval is \(k\Delta t\) and

\[
\phi_{k\Delta t}
=
\exp\left(-\frac{k\Delta t}{\tau}\right)
=
\left(
\exp\left(-\frac{\Delta t}{\tau}\right)
\right)^k.
\]

Hence

\[
\boxed{
\phi_{k\Delta t}
=
\phi_{\Delta t}^k
}.
\]

The covariance matrix obtained by taking every \(k\)-th row and column of the fine-grid covariance is exactly the covariance built directly on the coarse grid.

### Physical meaning

Correlation estimates obtained at multiple sampling scales should be compatible with one common \(\tau\) within uncertainty if the single exponential relaxation model is a reasonable description.

Systematic violation of this relation is evidence against that temporal model.

## Statement 3: time-unit invariance

Let \(c>0\) be a change of time unit, for example seconds to milliseconds. Then

\[
t_i' = c t_i,
\qquad
\tau'=c\tau.
\]

The kernel is unchanged:

\[
K_{\tau'}(t_i',t_j')
=
\exp\left(
-\frac{|ct_i-ct_j|}{c\tau}
\right)
=
K_\tau(t_i,t_j).
\]

Therefore

\[
\boxed{
R_{c\tau}(ct_1,\ldots,ct_N)
=R_\tau(t_1,\ldots,t_N)
}.
\]

### Physical meaning

Changing the unit used to write time cannot change the inferred temporal covariance geometry.

## Statement 4: irregular sample times are admissible

The exponential kernel is positive semidefinite on arbitrary finite sets of real sample times.

For \(x\in\mathbb R\),

\[
e^{-|x|/\tau}
=
\frac{1}{2\pi}
\int_{-\infty}^{\infty}
\frac{2\tau}{1+\tau^2\omega^2}
 e^{i\omega x}
\,d\omega.
\]

For any real coefficients \(a_1,\ldots,a_N\),

\[
\sum_{i,j}a_i a_j
K_\tau(t_i,t_j)
=
\frac{1}{2\pi}
\int_{-\infty}^{\infty}
\frac{2\tau}{1+\tau^2\omega^2}
\left|
\sum_j a_j e^{i\omega t_j}
\right|^2
\,d\omega
\ge 0.
\]

Thus \(R_\tau\) is positive semidefinite for any declared strictly increasing sample-time grid.

### Physical meaning

Missing observations or irregular acquisition times do not require the model to invent an integer sample distance. The covariance uses actual elapsed physical time.

## Statement 5: a certified continuum bound in relaxation time

For a pair of sample times, write

\[
d=|t_i-t_j|.
\]

The derivative of one covariance entry with respect to \(\tau\) is

\[
\frac{\partial}{\partial\tau}
 e^{-d/\tau}
=
\frac{d}{\tau^2}e^{-d/\tau}.
\]

For fixed \(d>0\), the magnitude

\[
g_d(\tau)
=
\frac{d}{\tau^2}e^{-d/\tau}
\]

has its unconstrained maximum at \(\tau=d/2\).

For a declared interval \(\tau\in[\tau_-,\tau_+]\), define

\[
M_{ij}
=
\sup_{\tau\in[\tau_-,\tau_+]}
\frac{|t_i-t_j|}{\tau^2}
\exp\left(-\frac{|t_i-t_j|}{\tau}\right)
\]

and

\[
L_\tau
=
\max_i\sum_j M_{ij}.
\]

Then for any \(\tau,\tau'\in[\tau_-,\tau_+]\),

\[
\boxed{
\|R_\tau-R_{\tau'}\|_2
\le
L_\tau |\tau-\tau'|
}.
\]

The entrywise derivative bound follows from the mean-value theorem. Symmetry then allows the operator norm to be bounded by the maximum absolute row sum.

## Statement 6: a finite physical-time cover

Choose a grid

\[
\tau_1<\cdots<\tau_G
\]

covering \([\tau_-,\tau_+]\), with maximum neighboring spacing

\[
h=\max_g(\tau_{g+1}-\tau_g).
\]

Every admissible \(\tau\) lies within \(h/2\) of a nearest grid point, so

\[
\boxed{
\min_g
\|R_\tau-R_{\tau_g}\|_2
\le
\frac{L_\tau h}{2}
}.
\]

This gives a deterministic operator covering radius

\[
\delta_\tau
=
\frac{L_\tau h}{2}.
\]

No probability union over grid points is required. The grid is a deterministic geometric representation of a continuum family.

## Statement 7: nuisance projection and Proposition 49 composition

Let \(H\) be a fixed full-rank nuisance design with rank \(q\), and let \(P_H\) be its orthogonal complement projector.

Projection cannot increase the operator norm, so

\[
\|P_H(R_\tau-R_{\tau_g})P_H\|_2
\le
\delta_\tau.
\]

Every \(R_\tau\) has trace \(N\). Writing \(Q_H=I-P_H\), with rank \(q\), gives

\[
\left|
\operatorname{tr}
\left(P_H(R_\tau-R_{\tau_g})\right)
\right|
=
\left|
\operatorname{tr}
\left(Q_H(R_\tau-R_{\tau_g})\right)
\right|
\le
q\delta_\tau.
\]

Therefore the physical relaxation-time family supplies the deterministic quantities required by Proposition 49:

\[
\delta_{\mathrm{eig}}
=\delta_\tau,
\qquad
\delta_{\mathrm{norm}}
=q\delta_\tau.
\]

A declared physical interval in \(\tau\) can therefore be propagated into the compact-family Gaussian matrix concentration theorem.

---

# Exact irregular-grid Gaussian Markov structure

The following statements strengthen Proposition 53 without introducing a new proposition number. They expose the local stochastic structure hidden inside the dense exponential covariance.

For consecutive timestamps define

\[
\Delta_i=t_{i+1}-t_i>0,
\qquad
\alpha_i
=
\exp\left(-\frac{\Delta_i}{\tau}\right),
\qquad i=1,\ldots,N-1.
\]

Then \(0<\alpha_i<1\).

## Statement 8: exact irregular-grid transition factorization

Let \(X_1\sim\mathcal N(0,1)\). For \(i=1,\ldots,N-1\), define

\[
\boxed{
X_{i+1}
=
\alpha_i X_i
+
\sqrt{1-\alpha_i^2}\,\varepsilon_i
}
\]

where \(\varepsilon_1,\ldots,\varepsilon_{N-1}\) are independent standard Gaussian variables and are independent of \(X_1\).

Then every \(X_i\) has variance one, and for \(i<j\),

\[
\operatorname{Cov}(X_i,X_j)
=
\prod_{k=i}^{j-1}\alpha_k.
\]

Because physical time intervals add,

\[
\prod_{k=i}^{j-1}\alpha_k
=
\exp\left(
-\frac{1}{\tau}
\sum_{k=i}^{j-1}(t_{k+1}-t_k)
\right)
=
\exp\left(-\frac{t_j-t_i}{\tau}\right).
\]

Therefore

\[
\boxed{
\operatorname{Cov}(X_i,X_j)
=K_\tau(t_i,t_j)
}.
\]

### Proof of unit variance

Assume \(\operatorname{Var}(X_i)=1\). Then

\[
\operatorname{Var}(X_{i+1})
=
\alpha_i^2
+
(1-\alpha_i^2)
=1.
\]

Induction from \(X_1\) proves unit variance for every sample.

### Proof of the covariance product

For \(i<j\), repeatedly condition forward. Every innovation after time \(i\) is independent of \(X_i\), so only the propagated state term contributes to covariance. Hence

\[
\operatorname{Cov}(X_i,X_j)
=
\alpha_i\alpha_{i+1}\cdots\alpha_{j-1}.
\]

This equals the exponential physical-time kernel by telescoping the elapsed intervals.

### Physical meaning

The model has no hidden integer lag on an irregular grid. Each observed gap has its own local transition coefficient. Long-range correlation is the product of the physically elapsed local transitions.

## Statement 9: exact innovation whitening

Define a lower-bidiagonal matrix \(W_\tau\) by

\[
(W_\tau)_{11}=1,
\]

and, for \(i=1,\ldots,N-1\),

\[
(W_\tau)_{i+1,i}
=
-\frac{\alpha_i}{\sqrt{1-\alpha_i^2}},
\qquad
(W_\tau)_{i+1,i+1}
=
\frac{1}{\sqrt{1-\alpha_i^2}}.
\]

Applying this matrix to the sampled process gives

\[
W_\tau X
=
\begin{pmatrix}
X_1\\
\varepsilon_1\\
\vdots\\
\varepsilon_{N-1}
\end{pmatrix}.
\]

Therefore

\[
\boxed{
W_\tau R_\tau W_\tau^\mathsf T
=I_N
}.
\]

### Multivariate corollary

If an \(N\times p\) Gaussian record has separable covariance

\[
R_\tau\otimes\Sigma,
\]

then applying \(W_\tau\) along the temporal axis gives independent temporal rows with common spatial covariance \(\Sigma\):

\[
\boxed{
(W_\tau\otimes I_p)
(R_\tau\otimes\Sigma)
(W_\tau^\mathsf T\otimes I_p)
=
I_N\otimes\Sigma
}.
\]

This is an exact temporal whitening result, not an asymptotic approximation.

## Statement 10: the exact precision matrix is tridiagonal

Since

\[
W_\tau R_\tau W_\tau^\mathsf T=I,
\]

we have

\[
\boxed{
R_\tau^{-1}
=W_\tau^\mathsf T W_\tau
}.
\]

Write

\[
v_i=1-\alpha_i^2.
\]

Then the precision matrix \(Q_\tau=R_\tau^{-1}\) has entries

\[
(Q_\tau)_{11}
=\frac{1}{v_1},
\]

\[
(Q_\tau)_{NN}
=\frac{1}{v_{N-1}},
\]

and for \(2\le i\le N-1\),

\[
(Q_\tau)_{ii}
=
\frac{1}{v_{i-1}}
+
\frac{\alpha_i^2}{v_i}.
\]

The only nonzero off-diagonal entries are

\[
\boxed{
(Q_\tau)_{i,i+1}
=(Q_\tau)_{i+1,i}
=-\frac{\alpha_i}{v_i}
}.
\]

All entries with \(|i-j|>1\) are exactly zero.

### Physical meaning

The covariance matrix is dense because temporal influence propagates through many steps. The precision matrix is sparse because, conditional on the immediately neighboring state, there is no additional Gaussian conditional dependence on distant timestamps under this model.

For an \(N\)-sample scalar record, the precision matrix has at most

\[
3N-2
\]

nonzero entries instead of \(N^2\).

## Statement 11: exact determinant factorization

Because \(W_\tau\) is lower triangular,

\[
\det(W_\tau)
=
\prod_{i=1}^{N-1}
\frac{1}{\sqrt{1-\alpha_i^2}}.
\]

From

\[
W_\tau R_\tau W_\tau^\mathsf T=I,
\]

we obtain

\[
\det(R_\tau)
=
\det(W_\tau)^{-2}.
\]

Therefore

\[
\boxed{
\det(R_\tau)
=
\prod_{i=1}^{N-1}(1-\alpha_i^2)
}
\]

and

\[
\boxed{
\log\det(R_\tau)
=
\sum_{i=1}^{N-1}
\log(1-\alpha_i^2)
}.
\]

### Computational meaning

For a fixed \(\tau\), the transition coefficients, innovation variances, whitening transform, and log determinant can all be evaluated from adjacent time gaps. The dense \(N\times N\) covariance does not need to be inverted to obtain the exact precision or determinant structure.

This is particularly useful for later likelihood-based calibration on long or irregular records.

## Statement 12: deleting intermediate samples preserves the physical semigroup

Consider three physical times \(t_1<t_2<t_3\). Define

\[
\alpha_{12}=e^{-(t_2-t_1)/\tau},
\qquad
\alpha_{23}=e^{-(t_3-t_2)/\tau}.
\]

The direct coarse transition from \(t_1\) to \(t_3\) is

\[
\alpha_{13}
=e^{-(t_3-t_1)/\tau}
=
\boxed{\alpha_{12}\alpha_{23}}.
\]

The two innovation variances also compose exactly:

\[
\alpha_{23}^2(1-\alpha_{12}^2)
+
(1-\alpha_{23}^2)
=
1-(\alpha_{12}\alpha_{23})^2
=
1-\alpha_{13}^2.
\]

Therefore removing an intermediate observation does not change the declared physical model. It produces exactly the transition law associated with the larger elapsed time.

### Physical meaning

This is the irregular-grid version of the coarse-sampling consistency in Statement 2. Missing samples alter which local transition is observed, but they do not require a new relaxation time.

---

## Experiment AM extension: dense covariance, sparse temporal structure

[![Proposition 53 irregular-grid Markov factorization](physical_relaxation_markov.svg)](physical_relaxation_sampling.json)

For the committed 13-time-point irregular record at \(\tau=0.8\) s:

| Diagnostic | Recorded value |
| --- | ---: |
| Maximum covariance product error | \(1.11\times10^{-16}\) |
| Precision inverse maximum error | \(1.90\times10^{-15}\) |
| Whitening identity maximum error | \(8.32\times10^{-16}\) |
| Precision Gram maximum error | \(1.78\times10^{-15}\) |
| Dense vs innovation log-determinant error | \(1.78\times10^{-15}\) |
| Nonzero precision entries | **37 of 169** |

The numerical errors are floating-point diagnostics. The exact equalities come from Statements 8 through 12.

## Literature context

The exponential covariance is the classical stationary Ornstein-Uhlenbeck relaxation kernel. Uhlenbeck and Ornstein provide the physical stochastic-relaxation lineage. Doob's early rigorous work on Brownian motion and stochastic equations is relevant to the Gaussian Markov-process lineage used by the exact transition interpretation here.

See the [Bibliography and Citation Map](bibliography.md) for complete source roles. The irregular-grid factorization, whitening matrix, precision formulas, and determinant identities are derived directly on this page for the declared kernel.

## What Proposition 53 changes conceptually

Earlier AR(1) results used \(\phi\) because it is convenient on a uniformly sampled discrete record. Proposition 53 makes the physical hierarchy explicit:

\[
\boxed{
\text{physical relaxation time }\tau
\longrightarrow
\text{sampling schedule}
\longrightarrow
\text{local transition coefficients}
\longrightarrow
\text{covariance and precision geometry}
}
\]

The same physical \(\tau\) now controls uniform sampling, coarse sampling, irregular timestamps, missing observations, exact temporal whitening, and sparse conditional structure.

## Falsification and failure conditions

A physical application should not use Proposition 53 merely because an exponential kernel is convenient. The model should be questioned when, for example:

1. estimates from different sampling intervals imply incompatible relaxation times beyond uncertainty;
2. empirical covariance shows oscillatory sign changes that a positive exponential kernel cannot reproduce;
3. more than one relaxation scale is visible;
4. temporal statistics change over the observation window;
5. residuals show structured colored forcing not represented by the model;
6. irregular-sampling predictions fail on held-out time separations;
7. innovations produced by the fitted \(W_\tau\) retain systematic temporal dependence;
8. the empirical conditional-dependence structure is not compatible with a nearest-neighbor temporal precision model.

The last two checks are new consequences of the Markov factorization. They create direct model-failure diagnostics rather than merely new computational formulas.

## What is not established

Proposition 53 does not establish that a physical system has one true relaxation time. It does not establish that all irregularly sampled processes are Markov. The Markov conclusion is specific to the declared exponential Gaussian covariance model.

It does not identify an observer boundary. It does not turn covariance eigenmodes into energies. It does not establish consciousness.

It establishes a sampling-consistent physical parameterization, a certified continuum cover, and an exact local Gaussian representation for that declared temporal model.

## Reproduction and implementation

Implementation: [`src/observer_math/physical_relaxation.py`](../src/observer_math/physical_relaxation.py)

Claim-level tests: [`tests/test_physical_relaxation.py`](../tests/test_physical_relaxation.py)

Experiment AM: [`examples/physical_relaxation_sampling.py`](../examples/physical_relaxation_sampling.py)

Machine-readable record: [`physical_relaxation_sampling.json`](physical_relaxation_sampling.json)

Sampling-consistency figure: [`physical_relaxation_sampling.svg`](physical_relaxation_sampling.svg)

Markov-factorization figure: [`physical_relaxation_markov.svg`](physical_relaxation_markov.svg)

Markov figure renderer: [`examples/render_physical_relaxation_markov.py`](../examples/render_physical_relaxation_markov.py)
