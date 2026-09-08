# Proposition 53: sampling-consistent physical relaxation time

## Physical question

A measured physical process can be sampled quickly, slowly, or at irregular times. A physically meaningful temporal parameter should not become a different property of the system merely because the acquisition clock changes.

For a simple exponentially relaxing stationary process, the natural physical parameter is a relaxation time

\[
\tau>0,
\]

with units of time.

The central question is:

> **Can the temporal covariance model be written so that the same physical relaxation time survives changes in sampling interval, time units, and irregular measurement times, while still entering the finite-sample covariance certification machinery developed earlier in the repository?**

Proposition 53 answers that question for the exponential relaxation kernel.

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

This identity is experimentally useful. Correlation estimates obtained at multiple sampling scales should be compatible with one common \(\tau\) within uncertainty if the single exponential relaxation model is a reasonable description.

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

This is a basic dimensional-consistency requirement for a physical parameterization.

## Statement 4: irregular sample times are admissible

The exponential kernel is positive semidefinite on arbitrary finite sets of real sample times.

One way to see this is through its nonnegative spectral representation. For \(x\in\mathbb R\),

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

has its unconstrained maximum at

\[
\tau=\frac d2.
\]

For a declared interval

\[
\tau\in[\tau_-,\tau_+],
\]

the exact scalar maximum is therefore obtained by clipping \(d/2\) to that interval.

Let

\[
M_{ij}
=
\sup_{\tau\in[\tau_-,\tau_+]}
\frac{|t_i-t_j|}{\tau^2}
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

Define

\[
L_\tau
=
\max_i\sum_j M_{ij}.
\]

Then for any \(\tau,\tau'\in[\tau_-,\tau_+]\), the mean-value theorem gives entrywise bounds and symmetry gives

\[
\boxed{
\|R_\tau-R_{\tau'}\|_2
\le
L_\tau |\tau-\tau'|
}.
\]

### Why the matrix norm is controlled

The entrywise difference matrix is symmetric. Its operator norm is bounded by its maximum absolute row sum. Applying the scalar derivative supremum entry by entry gives the stated bound.

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

Every \(R_\tau\) has unit diagonal and therefore trace \(N\). Hence

\[
\operatorname{tr}(R_\tau-R_{\tau_g})=0.
\]

Writing \(Q_H=I-P_H\), with rank \(q\),

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

Therefore the physical relaxation-time family supplies exactly the two deterministic quantities required by Proposition 49:

\[
\delta_{\mathrm{eig}}
=\delta_\tau,
\qquad
\delta_{\mathrm{norm}}
=q\delta_\tau.
\]

A declared physical interval in \(\tau\) can therefore be propagated into the compact-family Gaussian matrix concentration theorem.

## What Proposition 53 changes conceptually

Earlier AR(1) results used \(\phi\) because it is convenient on a uniformly sampled discrete record. Proposition 53 makes the physical hierarchy explicit:

\[
\boxed{
\text{physical relaxation time }\tau
\longrightarrow
\text{sampling schedule}
\longrightarrow
\text{discrete covariance geometry}
}
\]

rather than treating the sample-index coefficient as fundamental.

This is a small but important change in what the model considers physically meaningful.

## Falsification and failure conditions

A physical application should not use Proposition 53 merely because an exponential kernel is convenient. The model should be questioned when, for example:

1. estimates from different sampling intervals imply incompatible relaxation times beyond uncertainty;
2. empirical covariance shows oscillatory sign changes that a positive exponential kernel cannot reproduce;
3. more than one relaxation scale is visible;
4. temporal statistics change over the observation window;
5. residuals show structured colored forcing not represented by the model;
6. irregular-sampling predictions fail on held-out time separations.

A failure of these checks is evidence that the single exponential relaxation family is too simple for that experiment.

## What is not established

Proposition 53 does not establish that a physical system has one true relaxation time. It does not identify an observer boundary. It does not turn covariance eigenmodes into energies. It does not establish consciousness.

It establishes a sampling-consistent physical parameterization and a certified way to carry a declared relaxation-time interval into the existing covariance-certification layer.

## Reproduction and implementation

Implementation: [`src/observer_math/physical_relaxation.py`](../src/observer_math/physical_relaxation.py)

Claim-level tests: [`tests/test_physical_relaxation.py`](../tests/test_physical_relaxation.py)

Experiment AM: [`examples/physical_relaxation_sampling.py`](../examples/physical_relaxation_sampling.py)

Machine-readable record: [`physical_relaxation_sampling.json`](physical_relaxation_sampling.json)

Figure: [`physical_relaxation_sampling.svg`](physical_relaxation_sampling.svg)
