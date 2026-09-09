# Proposition 57: robust innovation whitening under calibrated physical-time uncertainty

## Physical question

Proposition 56 established a sharp target covariance result when the physical relaxation time is known exactly. On the controlled target schedule, exact local innovation coordinates changed the known-\(\tau\) raw-time radius from

\[
2.1672468952
\]

to

\[
0.4364662463<1.
\]

The physically relevant question is harder:

> What happens when the relaxation time is not known exactly, but is only constrained by a finite-sample calibration experiment?

Proposition 57 answers this without returning to the raw-time covariance estimator. One working physical timescale is chosen using an independent calibration record. Its Proposition 53 innovation whitener is applied to the target measurements and nuisance design. The residual temporal covariance induced by every still-admissible true relaxation time is then certified uniformly.

With the trace-specific normalization certificate documented below, Experiment AR gives

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

at target covariance confidence `0.975`. Combined with the independent Proposition 55 calibration confidence `0.975`, the joint lower confidence bound is

\[
\boxed{0.950625}.
\]

This result removes the exact-target-\(\tau\) assumption from Proposition 56 for the declared one-timescale separable Gaussian model.

[Experiment AR figure](robust_innovation_whitened_target.svg) | [machine-readable result](robust_innovation_whitened_target.json) | [implementation](../src/observer_math/robust_innovation_whitening.py) | [claim-level tests](../tests/test_robust_innovation_whitening.py)

---

# 1. Research lineage and attribution

The conceptual starting point of the repository is Max Tegmark's observer-factorization question in [Tegmark 2015](bibliography.md#tegmark-2015). The word `observer` is operational here: the project studies persistent moving subsystems inferred from dynamics, not subjective experience.

Proposition 57 belongs to the measurement-certification chain required before a moving-subsystem score can be trusted:

\[
\text{physical-time model}
\xrightarrow{\mathrm{P53}}
\text{finite-sample }\tau\text{ calibration}
\xrightarrow{\mathrm{P55}}
\text{innovation representation}
\xrightarrow{\mathrm{P56}}
\boxed{\text{uniform uncertain-}\tau\text{ target inference, P57}}.
\]

Relevant external foundations are:

- exponential Gaussian relaxation and Markov-process context: [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and [Doob 1942](bibliography.md#doob-1942);
- Gaussian covariance sampling: [Wishart 1928](bibliography.md#wishart-1928);
- matrix concentration: [Tropp 2012](bibliography.md#tropp-2012);
- matrix perturbation tools: [Bhatia 1997](bibliography.md#bhatia-1997);
- finite-sample e-value calibration used upstream: [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021), [Shafer 2021](bibliography.md#shafer-2021), and [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023).

The fixed working whitener, transformed-family cover, and trace-specific normalization certificate below are repository constructions. No external citation is intended to attribute these particular statements to those authors.

---

# 2. Calibration input

Let an independent calibration record produce a finite-sample confidence set for the physical relaxation time \(\tau_*\).

For Experiment AR, Proposition 55 supplies the retained hull

\[
\boxed{
\tau_*\in[0.686875,0.8515625]\ \mathrm{s}
}
\]

with calibration confidence

\[
1-\alpha=0.975.
\]

The hull width is

\[
0.1646875\ \mathrm{s}.
\]

Proposition 57 uses the complete hull. It does not exploit gaps between retained calibration cells. This is conservative and keeps the target statement transparent.

---

# 3. Target measurement model

Let the independent target record be

\[
Y\in\mathbb R^{N\times d}
\]

with declared separable Gaussian model

\[
\boxed{
Y=HB+E,
\qquad
\operatorname{vec}(E)
\sim
\mathcal N(0,R_{\tau_*}\otimes\Gamma_*).
}
\]

Here:

- \(H\in\mathbb R^{N\times q}\) is a fixed, predeclared, full-rank nuisance design;
- \(B\) contains unknown nuisance coefficients;
- \(R_{\tau_*}\) is the exponential temporal covariance on the actual target timestamps;
- \(\Gamma_*\) is the spatial covariance to be certified.

For Experiment AR,

\[
N=120,
\qquad
q=2,
\qquad
N-q=118.
\]

Calibration and target records are independent as required by the finite-sample composition.

---

# 4. One working physical timescale

Choose a working relaxation time using calibration information only. Experiment AR uses the midpoint

\[
\boxed{
\tau_0
=
\frac{0.686875+0.8515625}{2}
=
0.76921875\ \mathrm{s}.
}
\]

Let \(W_0\) be the exact Proposition 53 innovation whitener associated with \(\tau_0\):

\[
\boxed{
W_0R_{\tau_0}W_0^{\mathsf T}=I.
}
\]

Apply the same transformation to measurements and nuisance design:

\[
Z=W_0Y,
\qquad
G=W_0H.
\]

Let

\[
P_G=I-G(G^{\mathsf T}G)^{-1}G^{\mathsf T}.
\]

If the true relaxation time were exactly \(\tau_0\), the residual stochastic coordinates would reduce to the unit-weight geometry of Proposition 56.

For an uncertain true \(\tau\), the transformed temporal covariance is instead

\[
\boxed{
C_\tau=W_0R_\tau W_0^{\mathsf T}.
}
\]

The target problem is therefore to certify the complete compact family

\[
\mathcal C
=
\left\{
C_\tau:
\tau\in[\tau_-,\tau_+]
\right\}.
\]

---

# 5. Operator cover for the transformed family

Proposition 53 supplies a deterministic operator-Lipschitz bound

\[
\|R_\tau-R_{\tau'}\|_2
\le
L_R|\tau-\tau'|.
\]

Because the working whitener is fixed,

\[
\begin{aligned}
\|C_\tau-C_{\tau'}\|_2
&=
\|W_0(R_\tau-R_{\tau'})W_0^{\mathsf T}\|_2\\
&\le
\|W_0\|_2^2
\|R_\tau-R_{\tau'}\|_2\\
&\le
\boxed{
L_C|\tau-\tau'|,
}
\end{aligned}
\]

where

\[
\boxed{
L_C=\|W_0\|_2^2L_R.
}
\]

For a uniform relaxation-time grid with maximum spacing \(h\), every admissible true \(\tau\) is within \(h/2\) of a grid point. Therefore

\[
\boxed{
\delta_\lambda
=
\frac{h}{2}L_C
}
\]

is a valid operator covering radius for the transformed family.

After compression through the nuisance complement, Weyl's inequality gives the same radius for the ordered projected temporal eigenvalues.

This operator cover is unchanged by the trace tightening introduced below.

---

# 6. Trace-specific normalization cover

Proposition 49 also needs a deterministic cover for the projected temporal normalization. Define

\[
\boxed{
d(\tau)
=
\operatorname{tr}(P_GC_\tau)
=
\operatorname{tr}(P_GW_0R_\tau W_0^{\mathsf T}).
}
\]

A valid but loose bound is obtained from

\[
|d(\tau)-d(\tau')|
\le
(N-q)\|C_\tau-C_{\tau'}\|_2.
\]

The implementation previously used this rank-times-operator inequality. It is correct, but it treats the trace as though every residual eigenvalue could move simultaneously in the worst possible direction at the full operator radius.

The sharper certificate follows from differentiating the scalar normalization directly.

Define

\[
M=W_0^{\mathsf T}P_GW_0.
\]

Then

\[
d(\tau)
=
\operatorname{tr}(MR_\tau).
\]

For the exponential kernel,

\[
R_\tau(i,j)
=
e^{-D_{ij}/\tau},
\qquad
D_{ij}=|t_i-t_j|,
\]

and

\[
\frac{\partial R_\tau(i,j)}{\partial\tau}
=
\frac{D_{ij}}{\tau^2}
e^{-D_{ij}/\tau}.
\]

For fixed distance \(D>0\), the scalar derivative magnitude

\[
f_D(\tau)
=
\frac{D}{\tau^2}e^{-D/\tau}
\]

has its unconstrained maximum at

\[
\tau=\frac{D}{2}.
\]

Therefore its exact supremum on \([\tau_-,\tau_+]\) is obtained by clipping \(D/2\) to the declared interval.

Let

\[
D'_{ij}
=
\sup_{\tau\in[\tau_-,\tau_+]}
\left|
\frac{\partial R_\tau(i,j)}{\partial\tau}
\right|.
\]

Then

\[
\begin{aligned}
|d'(\tau)|
&=
\left|
\sum_{i,j}M_{ij}
\frac{\partial R_\tau(i,j)}{\partial\tau}
\right|\\
&\le
\sum_{i,j}|M_{ij}|D'_{ij}.
\end{aligned}
\]

Define the trace-specific Lipschitz constant

\[
\boxed{
L_d
=
\sum_{i,j}|M_{ij}|D'_{ij}.
}
\]

By the mean-value theorem,

\[
\boxed{
|d(\tau)-d(\tau')|
\le
L_d|\tau-\tau'|.
}
\]

Hence the certified normalization-cover radius is

\[
\boxed{
\delta_d
=
\frac{h}{2}L_d.
}
\]

This is a deterministic continuum certificate. It is not an empirical fit and it spends no probability budget.

## Why this is preferable

The operator cover and trace cover answer different mathematical questions:

| Quantity | What must be controlled | Certificate |
| --- | --- | --- |
| projected eigenvalues | operator displacement of the covariance family | \(\delta_\lambda=(h/2)L_C\) |
| projected normalization | scalar displacement of \(d(\tau)=\operatorname{tr}(P_GC_\tau)\) | \(\delta_d=(h/2)L_d\) |

Using a trace-specific functional bound is both more accurate and more transparent than forcing the scalar trace through a worst-case rank-times-operator inequality.

---

# 7. Uniform matrix concentration

At each deterministic grid point, compress the transformed covariance through the nuisance complement and compute its nonnegative temporal eigenvalues.

Proposition 49 combines:

1. the finite transformed covariance grid;
2. the eigenvalue covering radius \(\delta_\lambda\);
3. the trace-specific normalization covering radius \(\delta_d\);
4. the Proposition 47 Gaussian matrix-mgf factors.

The target covariance estimator is

\[
\boxed{
\widehat\Gamma_{57}
=
\frac{Z^{\mathsf T}P_GZ}{d_0},
}
\]

where \(d_0\) is the deterministic reference normalization returned by the covered temporal family.

The theorem supplies \(\varepsilon_{57}\) such that, uniformly for every

\[
\tau_*\in[\tau_-,\tau_+],
\]

\[
\boxed{
\Pr\left[
\left\|
\Gamma_*^{-1/2}
(\widehat\Gamma_{57}-\Gamma_*)
\Gamma_*^{-1/2}
\right\|_2
\le
\varepsilon_{57}
\right]
\ge
1-\beta.
}
\]

For Experiment AR,

\[
1-\beta=0.975.
\]

---

# 8. Composition with finite-sample calibration

Let

\[
A=\{\tau_*\in[\tau_-,\tau_+]\}
\]

be the Proposition 55 calibration event. Then

\[
\Pr(A)\ge1-\alpha.
\]

The interval and working whitener depend only on the independent calibration record. Conditional on that record, the target theorem is uniform over the complete retained interval. Therefore, whenever \(A\) occurs, the target success probability is at least \(1-\beta\).

Hence

\[
\Pr(A\cap B)
\ge
(1-\alpha)(1-\beta).
\]

With

\[
1-\alpha=1-\beta=0.975,
\]

we obtain

\[
\boxed{
0.975^2=0.950625.
}
\]

No independence between different candidate \(\tau\) values is needed. The target theorem is already uniform over the continuum.

---

# 9. Experiment AR

Experiment AR reuses the target timestamp schedule from Experiments AP and AQ so the change in the certificate is directly interpretable.

## 9.1 Input

| Quantity | Value |
| --- | ---: |
| Proposition 55 calibrated hull | \([0.686875,0.8515625]\) s |
| Working relaxation time | \(0.76921875\) s |
| Target timestamps | 120 |
| Nuisance rank | 2 |
| Residual innovation degrees of freedom | 118 |
| Calibration confidence | 0.975 |
| Target covariance confidence | 0.975 |
| Combined confidence lower bound | 0.950625 |

## 9.2 Operator geometry

The 1025-point cover has maximum relaxation-time spacing

\[
h=0.0001608276\ \mathrm{s}.
\]

The raw covariance operator-Lipschitz constant is

\[
L_R=29.94950\ \mathrm{s}^{-1},
\]

and

\[
\|W_0\|_2=5.15015.
\]

Thus

\[
L_C=794.38212\ \mathrm{s}^{-1}
\]

and

\[
\boxed{
\delta_\lambda=0.0638793.
}
\]

## 9.3 Trace geometry

The trace-specific derivative certificate gives

\[
\boxed{
L_d=176.55489\ \mathrm{s}^{-1}
}
\]

and therefore

\[
\boxed{
\delta_d=0.01419745.
}
\]

The older rank-times-operator certificate was

\[
(N-q)\delta_\lambda
\approx7.53776.
\]

It remains mathematically valid, but it is superseded here by the tighter trace-functional certificate.

The certified projected normalization interval is now

\[
\boxed{
107.32460
\le d(\tau)\le
131.07280.
}
\]

The midpoint reference normalization remains

\[
\boxed{
d_0=119.19870.
}
\]

The fact that \(d_0\) is unchanged is expected: replacing a symmetric cover radius around the minimum and maximum changes the interval width but not the midpoint of those two extremal grid values.

The certified spectral bound remains

\[
1.18360.
\]

## 9.4 Final radius

The Proposition 49 oracle deviations under the covered transformed family are

\[
0.5638077
\]

and

\[
0.4360857.
\]

After the certified normalization range is included, the final upper and lower deviations are

\[
0.7195880
\]

and

\[
0.4922606.
\]

Therefore

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

[![Experiment AR](robust_innovation_whitened_target.svg)](robust_innovation_whitened_target.json)

---

# 10. Comparison with previous target bounds

| Target theorem | Physical-time information | Relative covariance radius |
| --- | --- | ---: |
| Proposition 55 raw-time calibrated target | finite-sample calibrated interval | 2.41488 |
| Proposition 55 raw-time oracle diagnostic | exact true \(\tau\) supplied | 2.16725 |
| Proposition 56 innovation target | exact true \(\tau\) supplied | 0.43647 |
| **Proposition 57 robust innovation target** | **finite-sample calibrated interval** | **0.71959** |

Relative to the Proposition 55 calibrated raw-time theorem,

\[
\boxed{
1-
\frac{0.7195879984}{2.4148799294}
\approx70.2\%.
}
\]

The cost of removing the exact-\(\tau\) assumption is still visible: the uniform robust radius is larger than the exact-\(\tau\) P56 radius. The uncertainty is therefore not treated as free.

---

# 11. Pointwise diagnostics

Pointwise calculations are included only to show where the uniform theorem is conservative. They are not substitutes for the uniform guarantee.

| True \(\tau\) used for diagnostic | Projected temporal trace | Pointwise radius |
| ---: | ---: | ---: |
| 0.686875 s | 131.05860 | 0.57955 |
| 0.76921875 s | 118.00000 | 0.42202 |
| 0.780000 s | 116.48323 | 0.40375 |
| 0.8515625 s | 107.33879 | 0.40353 |

The uniform radius `0.71959` is larger because it protects the complete calibrated continuum simultaneously using deterministic between-grid operator and trace envelopes.

The remaining gap between the pointwise diagnostics and the uniform theorem is a tightness opportunity, not a validity problem.

---

# 12. Physical interpretation

The target record has strong temporal memory. In raw-time coordinates, that memory produces an uneven temporal spectrum and a loose covariance theorem.

A working innovation transform uses the calibrated physical model to move the complete admissible family into a neighborhood of independent innovation geometry.

If \(\tau_0\ne\tau_*\), the transformed process is not perfectly white. Proposition 57 does not ignore this mismatch. It certifies the residual covariance family induced by every calibrated true timescale.

The operator cover controls how far the projected eigenvalues may move. The trace-specific cover separately controls how the total projected temporal normalization may move. Keeping those two roles distinct is both mathematically cleaner and physically easier to interpret.

In short:

> Proposition 56 asks what happens under exact physical whitening. Proposition 57 asks how much of that information advantage survives when the physical timescale itself is only finitely known.

On Experiment AR, enough of the advantage survives to keep the finite-sample covariance radius well below one.

---

# 13. What Proposition 57 does not claim

The theorem does not claim:

- that one stationary exponential relaxation time is universal;
- that the midpoint is the optimal working timescale for every design;
- that the Proposition 55 hull is the smallest possible calibrated set;
- that the current operator or trace envelopes are globally optimal;
- that \(\varepsilon<1\) alone certifies world-tube recovery;
- that covariance geometry identifies consciousness.

It is a finite-sample covariance theorem conditional on the declared measurement model.

---

# 14. Failure conditions and falsification

A physical application should test the assumptions that make innovation whitening meaningful. Relevant failure diagnostics include:

- residual temporal correlation inconsistent with the certified transformed family;
- multiple relaxation times;
- oscillatory or nonmonotone temporal covariance;
- time-varying relaxation behavior;
- heavy-tailed or non-Gaussian innovations;
- nonseparable space-time covariance;
- calibration-to-target population mismatch;
- nuisance modes selected adaptively from the same target noise.

If these diagnostics fail, the appropriate response is to enlarge or replace the temporal model rather than interpret a narrow certificate as physical truth.

---

# 15. Relationship to Proposition 58

The trace tightening improves P57, but it does not remove the observer-scale bottleneck found by Proposition 58.

Proposition 58 returns covariance uncertainty to the original moving-boundary objective and shows that block dimension and simultaneous candidate structure become dominant at observer scale. The scalar P57 result is therefore a necessary measurement milestone, not the endpoint of the research program.

The current structural frontier remains:

- factor-specific covariance blocks;
- screen-first simultaneity reduction;
- candidate-local uncertainty radii;
- direct score-margin concentration.

---

# 16. Reproducibility and audit trail

Implementation:

- [`src/observer_math/robust_innovation_whitening.py`](../src/observer_math/robust_innovation_whitening.py)

Claim-level tests:

- [`tests/test_robust_innovation_whitening.py`](../tests/test_robust_innovation_whitening.py)

Experiment:

- [`examples/robust_innovation_whitened_target.py`](../examples/robust_innovation_whitened_target.py)

Deterministic renderer:

- [`examples/render_robust_innovation_whitened_target.py`](../examples/render_robust_innovation_whitened_target.py)

Machine-readable result:

- [`docs/robust_innovation_whitened_target.json`](robust_innovation_whitened_target.json)

Visible figure:

- [`docs/robust_innovation_whitened_target.svg`](robust_innovation_whitened_target.svg)

The probability guarantee comes from the analytic transformed-family operator cover, the analytic trace-specific normalization cover, Proposition 49 matrix concentration, Proposition 55 calibration coverage, and calibration-target separation. The pointwise calculations and figure are diagnostics and visualizations, not substitutes for the theorem.
