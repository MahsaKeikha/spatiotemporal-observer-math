# Release 0.41.0 research record

Release 0.41.0 adds Proposition 53 and Experiment AM.

## Research state

| Record | 0.41.0 state |
| --- | ---: |
| Propositions | **53** |
| Reproducible experiments | **39, A-Z and AA-AM** |
| Scientific result figures | **26** |
| Claim-level tests | **183** |
| Supported CI matrix | **Python 3.10, 3.11, 3.12** |

## Proposition 53

Proposition 53 introduces a sampling-consistent physical parameterization for the exponential temporal covariance model.

For physical sample times \(t_i\),

\[
R_\tau(i,j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

For uniform sampling interval \(\Delta t\), this reduces exactly to the AR(1) form with

\[
\phi_{\Delta t}
=
\exp\left(-\frac{\Delta t}{\tau}\right).
\]

The physical parameter \(\tau\) has units of time. The discrete coefficient \(\phi_{\Delta t}\) depends on the acquisition interval.

The proposition proves:

1. exact equivalence with uniformly sampled AR(1) covariance;
2. exact coarse-sampling consistency \(\phi_{k\Delta t}=\phi_{\Delta t}^k\);
3. invariance under a change of time units;
4. positive-semidefinite covariance on irregular sample times;
5. an analytic operator-Lipschitz bound over a declared relaxation-time interval;
6. a deterministic finite cover that composes with Proposition 49.

Proof: [Proposition 53](proposition_53_physical_relaxation_time.md).

## Experiment AM

Experiment AM uses a controlled relaxation time

\[
\tau=0.8\ \mathrm{s}.
\]

Sampling the same declared model at 40 Hz, 20 Hz, 10 Hz, 5 Hz, and 2.5 Hz produces different one-step correlations, but every value maps back to the same relaxation time.

The experiment also checks irregular timestamps and compares the analytic continuum covering radius with dense numerical evaluation over

\[
\tau\in[0.55,1.05]\ \mathrm{s}.
\]

[![Experiment AM](physical_relaxation_sampling.svg)](proposition_53_physical_relaxation_time.md)

Machine-readable result: [JSON](physical_relaxation_sampling.json).

Reproduction script: [`examples/physical_relaxation_sampling.py`](../examples/physical_relaxation_sampling.py).

Figure renderer: [`examples/render_physical_relaxation_sampling.py`](../examples/render_physical_relaxation_sampling.py).

## Physical interpretation

The release makes one hierarchy explicit:

\[
\boxed{
\text{physical relaxation time }\tau
\longrightarrow
\text{sampling schedule}
\longrightarrow
\text{discrete correlation }\phi
}
\]

This matters because a parameter intended to describe the physical process should not change merely because the same process is recorded at a different sampling rate.

## Scope and nonclaims

Proposition 53 is conditional on the exponential relaxation model. It does not establish that every real system has one relaxation time. It does not establish that every observed covariance is exponential. It does not identify an observer boundary, and it does not establish consciousness.

A real application should test the exponential model against multiple sampling scales, irregular-time predictions, stationarity, spectral structure, and residual temporal dependence.
