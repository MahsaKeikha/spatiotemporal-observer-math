# Proposition 57: robust innovation whitening under calibrated physical-time uncertainty

## Physical question

Proposition 56 established a sharp result when the physical relaxation time is known exactly. For the Experiment AQ target schedule, transforming the temporally correlated record into its exact local Gaussian innovations changed the target covariance radius from

\[
2.1672468952
\]

to

\[
0.4364443814<1.
\]

The unresolved physical question was unavoidable:

> What happens when the relaxation time is not known exactly, but has only been constrained by a finite-sample calibration experiment?

Proposition 57 answers this without returning to the original raw-time covariance estimator.

A single working relaxation time is chosen from the independently calibrated interval. Its exact Proposition 53 innovation whitener is then applied to the target record. Every still-admissible true relaxation time produces a transformed temporal covariance close to identity. Proposition 57 certifies that entire transformed covariance family and proves a uniform target covariance guarantee over it.

On the Experiment AR benchmark, the result remains inside the perturbative regime:

\[
\boxed{
\varepsilon_{57}=0.8677117535<1.
}
\]

This closes the exact-\(\tau\) limitation recorded at the end of Proposition 56 for the declared one-timescale Gaussian model.

---

# 1. Research lineage

The conceptual starting point of the repository remains Max Tegmark's observer-factorization question in [Tegmark 2015](bibliography.md#tegmark-2015). The word `observer` remains operational: the project studies persistent moving subsystems inferred from dynamics, not subjective experience.

Proposition 57 belongs to the measurement-certification chain required before those moving-subsystem scores can be trusted:

\[
\text{physical-time model}
\xrightarrow{\text{P53}}
\text{finite-sample }\tau\text{ calibration}
\xrightarrow{\text{P55}}
\text{exact innovation whitening}
\xrightarrow{\text{P56}}
\boxed{\text{robust whitening over uncertain }\tau\text{, P57}}.
\]

Its technical foundations are already mapped in the repository bibliography:

- exponential Gaussian relaxation and Markov structure: [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930), [Doob 1942](bibliography.md#doob-1942);
- e-value calibration: [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021), [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023);
- Gaussian covariance sampling: [Wishart 1928](bibliography.md#wishart-1928);
- matrix concentration: [Tropp 2012](bibliography.md#tropp-2012).

The particular composition below, including the fixed working innovation whitener and certified transformed temporal family, is the construction developed in this repository.

---

# 2. Calibration input

Let an independent calibration record produce a finite-sample confidence set for the physical relaxation time \(\tau_*\).

For Experiment AR, Proposition 55 supplies a quadratic outer cover whose retained-cell hull is

\[
\boxed{
\tau_*\in[0.686875,0.8515625]\ \mathrm{s}
}
\]

with calibration confidence at least

\[
1-\alpha=0.975.
\]

The hull width is

\[
0.1646875\ \mathrm{s}.
\]

Proposition 57 deliberately uses the full hull rather than exploiting gaps between retained cells. This is conservative and keeps the target theorem simple.

---

# 3. Target measurement model

The target record is

\[
Y\in\mathbb R^{N\times d}
\]

with declared model

\[
Y=HB+E,
\qquad
\operatorname{vec}(E)
\sim
\mathcal N(0,R_{\tau_*}\otimes\Gamma_*).
\]

Here:

- \(H\in\mathbb R^{N\times q}\) is a fixed full-rank nuisance design;
- \(B\) contains unknown deterministic nuisance coefficients;
- \(R_{\tau_*}\) is the exponential temporal covariance on the actual target timestamps;
- \(\Gamma_*\) is the spatial covariance to be certified.

For Experiment AR:

\[
N=120,
\qquad
q=2,
\qquad
N-q=118.
\]

The calibration record and target record are independent.

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
W_0R_{\tau_0}W_0^{\mathsf T}=I.
\]

Apply exactly the same physical transformation to the measurements and nuisance design:

\[
Z=W_0Y,
\qquad
G=W_0H.
\]

Let

\[
P_G
=
I-G(G^{\mathsf T}G)^{-1}G^{\mathsf T}.
\]

If the true relaxation time happened to equal \(\tau_0\), then

\[
P_GW_0EW_0^{\mathsf T}P_G
\]

would reduce to the unit-weight innovation geometry of Proposition 56.

For uncertain \(\tau_*\), the temporal covariance in the working innovation coordinates is instead

\[
\boxed{
C_\tau
=
W_0R_\tau W_0^{\mathsf T}.
}
\]

The central task is therefore to certify the compact family

\[
\left\{C_\tau:\tau\in[\tau_-,\tau_+]\right\}.
\]

---

# 5. Deterministic transformed-family cover

Proposition 53 supplies an operator-Lipschitz bound for the physical covariance family:

\[
\|R_\tau-R_{\tau'}\|_2
\le
L_R|\tau-\tau'|.
\]

Multiplication by the fixed working whitener gives

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
\|W_0\|_2^2L_R|\tau-\tau'|.
}
\end{aligned}
\]

Define

\[
L_C=\|W_0\|_2^2L_R.
\]

For a uniform grid of admissible relaxation times with maximum spacing \(h\), every true \(\tau\) lies within \(h/2\) of a grid point. Hence

\[
\boxed{
\delta_\lambda
=
\frac{h}{2}L_C
}
\]

is a valid operator covering radius for the transformed temporal family.

After nuisance projection, Weyl's inequality gives the same radius for every ordered projected temporal eigenvalue.

The projected temporal trace has rank at most \(N-q\), so

\[
\boxed{
\delta_d
=(N-q)\delta_\lambda
}
\]

is a valid deterministic normalization-cover radius.

This trace step is intentionally conservative. It avoids making a stronger geometry-specific claim than the proof supports.

---

# 6. Uniform matrix concentration

At each deterministic grid point, compress the transformed covariance through the nuisance complement and compute its nonnegative temporal eigenvalues.

Proposition 49 then combines:

1. the finite transformed covariance grid;
2. the eigenvalue covering radius \(\delta_\lambda\);
3. the normalization covering radius \(\delta_d\);
4. Proposition 47's exact Gaussian matrix-mgf factors.

The result is a covariance estimator

\[
\boxed{
\widehat\Gamma_{57}
=
\frac{Z^{\mathsf T}P_GZ}{d_0}
}
\]

where \(d_0\) is the deterministic reference normalization returned by the certified transformed family.

The theorem supplies \(\varepsilon_{57}\) such that, uniformly for every true

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

# 7. Composition with finite-sample calibration

Let

\[
A=\{\tau_*\in[\tau_-,\tau_+]\}
\]

be the Proposition 55 calibration event, so

\[
\Pr(A)\ge1-\alpha.
\]

The interval and the working whitener are functions of the calibration record only. Conditional on that record, the target data remain independent.

Whenever \(A\) occurs, the Proposition 57 target theorem is uniform over the complete interval containing \(\tau_*\). Therefore the conditional target success probability is at least \(1-\beta\).

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

the combined confidence lower bound is

\[
\boxed{
0.975^2=0.950625.
}
\]

No independence between different candidate \(\tau\) values is needed. The target theorem is already uniform over the transformed family.

---

# 8. Experiment AR

Experiment AR uses the same target timestamp schedule as Experiments AP and AQ so that the change in the bound can be interpreted directly.

## 8.1 Certified input

| Quantity | Value |
| --- | ---: |
| Proposition 55 calibrated hull | \([0.686875,0.8515625]\) s |
| Working relaxation time | \(0.76921875\) s |
| Target timestamps | 120 |
| Nuisance rank | 2 |
| Residual rank | 118 |
| Calibration confidence | 0.975 |
| Target confidence | 0.975 |
| Combined confidence | 0.950625 |

## 8.2 Transformed-family geometry

The 1025-point certified cover has maximum relaxation-time spacing

\[
0.0001608276\ \mathrm{s}.
\]

The deterministic bounds are

\[
L_R=29.94950\ \mathrm{s}^{-1},
\]

\[
\|W_0\|_2=5.15015,
\]

and therefore

\[
L_C=794.38212\ \mathrm{s}^{-1}.
\]

The resulting transformed eigenvalue covering radius is

\[
\delta_\lambda=0.0638793,
\]

and the conservative projected-normalization covering radius is

\[
\delta_d=7.53776.
\]

The certified projected temporal geometry is

\[
d_- = 99.80104,
\qquad
d_+ = 138.59636,
\]

with reference normalization

\[
\boxed{
d_0=119.19870.
}
\]

The certified spectral bound is

\[
1.18360.
\]

## 8.3 Final radius

The upper and lower final deviations are

\[
0.8677118
\]

and

\[
0.5553784,
\]

respectively. Thus

\[
\boxed{
\varepsilon_{57}=0.8677117535<1.
}
\]

This is the key finite-sample result of Experiment AR.

---

# 9. Comparison with the previous target bounds

| Target theorem | Assumption about \(\tau\) | Relative covariance radius |
| --- | --- | ---: |
| Proposition 55 raw-time calibrated target | finite-sample calibrated interval | 2.41488 |
| Proposition 55 raw-time oracle diagnostic | exact true \(\tau\) supplied | 2.16725 |
| Proposition 56 innovation target | exact true \(\tau\) supplied | 0.43647 |
| **Proposition 57 robust innovation target** | **finite-sample calibrated interval** | **0.86771** |

Relative to the Proposition 55 calibrated raw-time target theorem, Proposition 57 reduces the radius by approximately

\[
\boxed{64.1\%}.
\]

The price of removing the exact-\(\tau\) assumption is visible: the radius increases from roughly \(0.436\) to \(0.868\). But it remains below one.

That distinction is scientifically important. The result does not claim that uncertainty is free. It shows that the innovation representation retains enough information for the finite-sample guarantee to remain usable on this benchmark.

---

# 10. Pointwise diagnostics

Pointwise calculations are included only to show where the uniform theorem is conservative. They are not substitutes for the uniform guarantee.

| True \(\tau\) used for diagnostic | Projected temporal trace | Pointwise radius |
| ---: | ---: | ---: |
| 0.686875 s | 131.05860 | 0.57955 |
| 0.76921875 s | 118.00000 | 0.42202 |
| 0.780000 s | 116.48323 | 0.40375 |
| 0.8515625 s | 107.33879 | 0.40353 |

The certified uniform radius \(0.86771\) is larger because it must protect the complete continuum using deterministic between-grid and normalization envelopes.

This gap identifies a future tightness opportunity, not a validity problem.

---

# 11. Physical interpretation

The physical content of Proposition 57 is representation-sensitive but parameter-honest.

The target record has strong temporal memory. In raw time coordinates, that memory produces highly uneven temporal eigenvalues and a loose covariance theorem. A working innovation transform converts the calibrated family into a neighborhood of independent innovation geometry.

When the working timescale is not exactly the true one, the transformed process is not perfectly white. Proposition 57 does not ignore that mismatch. It certifies the complete family of residual temporal covariances induced by every calibrated true timescale.

In that sense:

> Proposition 56 asks what happens under exact physical whitening. Proposition 57 asks how much of that advantage survives when the physical timescale itself is only finitely known.

On Experiment AR, enough of the advantage survives to keep the covariance radius below one.

---

# 12. What Proposition 57 does not claim

The theorem does not claim:

- that the exponential one-timescale model is universal;
- that the midpoint is an optimal working timescale for every design;
- that the Proposition 55 retained hull is the smallest possible calibrated set;
- that the current Lipschitz and trace envelopes are tight;
- that \(\varepsilon<1\) alone guarantees world-tube recovery;
- that covariance geometry identifies consciousness.

It is a finite-sample covariance theorem conditional on the declared measurement model.

---

# 13. Failure conditions and falsification

A physical application should test the assumptions that make innovation whitening meaningful. Relevant failure diagnostics include:

- residual temporal correlation inconsistent with the certified transformed family;
- multiple relaxation times;
- oscillatory or nonmonotone temporal covariance;
- time-varying relaxation behavior;
- heavy-tailed or non-Gaussian innovations;
- nonseparable spatial-temporal covariance;
- calibration-to-target population mismatch;
- target nuisance modes chosen adaptively from the target noise.

If these diagnostics fail, the appropriate response is to enlarge or replace the temporal model rather than interpret a narrow certificate as physical truth.

---

# 14. Next mathematical frontier

Proposition 57 closes the immediate target-covariance bottleneck for calibrated \(\tau\) on the controlled benchmark.

Two mathematically distinct improvements now become worthwhile:

1. tighten the robust transformed-family certificate itself, especially the conservative projected-trace envelope;
2. propagate the resulting structured covariance uncertainty into the information factors, world-tube scores, and path-recovery margins of the original observer-identification problem.

The second direction is the more important conceptual bridge: it returns the measurement-certification work to the repository's original moving-boundary question.

---

# 15. Reproducibility

Implementation:

- `src/observer_math/robust_innovation_whitening.py`

Claim-level tests:

- `tests/test_robust_innovation_whitening.py`

Experiment:

- `examples/robust_innovation_whitened_target.py`

Machine-readable result:

- `docs/robust_innovation_whitened_target.json`

Visible figure:

- `docs/robust_innovation_whitened_target.svg`

The pointwise calculations and figure are numerical diagnostics. The finite-sample continuum guarantee comes from the analytic transformed-family cover, Proposition 49 matrix concentration, Proposition 55 calibration coverage, and independence of calibration and target records.