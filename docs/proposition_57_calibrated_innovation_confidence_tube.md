# Proposition 57: calibrated innovation-whitened covariance confidence tube

## Physical question

Proposition 56 solved the target concentration bottleneck when the physical relaxation time is known exactly. On the Experiment AQ target schedule, exact local innovation whitening changed the covariance radius from

\[
2.1672468952
\]

to

\[
\boxed{0.4364443814<1}.
\]

The remaining assumption was exact knowledge of the target relaxation time \(\tau\).

Proposition 55 already gives a finite-sample calibrated outer cover for \(\tau\). The next physical-statistical question is therefore:

> Can uncertainty about the physical relaxation time be carried through the innovation whitener without collapsing the analysis back to the much looser raw-time covariance bound?

Proposition 57 answers yes by changing the output from one plug-in covariance ball to a **joint confidence tube over physical relaxation time and spatial covariance**.

The key point is simple:

- calibration determines which physical timescales remain admissible;
- each admissible timescale defines its own exact local innovation whitener;
- each candidate whitener defines its own Proposition 56 covariance center;
- the target matrix radius is the same Proposition 56 radius for every candidate;
- the union of those candidate-wise balls is the calibrated covariance confidence region.

No single estimated \(\tau\) is substituted for the unknown physical parameter.

---

# 1. Place in the research program

The primary conceptual starting point of this repository remains Max Tegmark's factorization and observer-identification question in [Tegmark 2015](bibliography.md#tegmark-2015). Proposition 57 is not a consciousness theorem. It belongs to the finite-sample measurement-certification layer required before the moving-subsystem scores can be treated as statistically stable.

The immediate mathematical lineage is:

\[
\text{Proposition 53}
\rightarrow
\text{Proposition 55}
\rightarrow
\text{Proposition 56}
\rightarrow
\boxed{\text{Proposition 57}}.
\]

- Proposition 53 supplies the physical-time exponential kernel and exact irregular-grid Markov whitener.
- Proposition 55 supplies a finite-sample outer cover for the unknown physical relaxation time.
- Proposition 56 supplies exact known-\(\tau\) innovation-whitened covariance concentration.
- Proposition 57 composes the calibration set and the target covariance theorem without selecting one plug-in timescale.

The e-value calibration lineage is documented under [Vovk and Wang 2021](bibliography.md#vovk-and-wang-2021) and [Vovk and Wang 2023](bibliography.md#vovk-and-wang-2023). The Gaussian covariance law ultimately uses the classical [Wishart 1928](bibliography.md#wishart-1928) distribution, while the matrix-valued finite-sample radius uses the matrix-Laplace methodology documented under [Tropp 2012](bibliography.md#tropp-2012). The physical exponential-relaxation and Gaussian Markov context is recorded under [Uhlenbeck and Ornstein 1930](bibliography.md#uhlenbeck-and-ornstein-1930) and [Doob 1942](bibliography.md#doob-1942).

---

# 2. Two independent records

Proposition 57 uses two statistically distinct records.

## 2.1 Calibration record

The calibration experiment produces a Proposition 55 quadratic outer cover

\[
\mathcal O_\alpha(Z_{\mathrm{cal}})
\]

for the unknown physical relaxation time \(\tau_*\).

Proposition 55 is built on the continuum e-value confidence set

\[
\mathcal C_\alpha(Z_{\mathrm{cal}})
\]

and proves the deterministic containment

\[
\mathcal C_\alpha(Z_{\mathrm{cal}})
\subseteq
\mathcal O_\alpha(Z_{\mathrm{cal}}).
\]

Because the e-value confidence set has coverage at least \(1-\alpha\),

\[
\Pr\left[
\tau_*\in\mathcal O_\alpha(Z_{\mathrm{cal}})
\right]
\ge 1-\alpha.
\]

For the benchmark carried forward from Experiment AP, using 160 calibration cells,

\[
\boxed{
\mathcal O_{0.025}
\subseteq
[0.686875,0.8515625]\ \mathrm{s}
}
\]

with 31 retained cells. The controlled true value is

\[
\tau_*=0.78\ \mathrm{s}.
\]

The interval above is the hull of the retained cells. The theorem itself keeps the complete retained-cell union.

## 2.2 Target record

The independent target record is

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

Here

- \(H\in\mathbb R^{N\times q}\) is a fixed full-rank nuisance design;
- \(B\) contains unknown deterministic nuisance coefficients;
- \(R_{\tau_*}\) is the exponential temporal covariance on the actual target timestamps;
- \(\Gamma_*\) is the spatial covariance to be certified.

Calibration and target records are assumed independent for the product-confidence statement below.

---

# 3. Candidate-wise physical whitening

For every candidate relaxation time \(\tau>0\), Proposition 53 defines the exact lower-bidiagonal innovation whitener

\[
W_\tau R_\tau W_\tau^\mathsf T=I.
\]

Apply the same physical transformation to the target measurements and nuisance design:

\[
Z_\tau=W_\tau Y,
\qquad
G_\tau=W_\tau H.
\]

Define

\[
P_{G_\tau}
=
I-G_\tau(G_\tau^\mathsf TG_\tau)^{-1}G_\tau^\mathsf T.
\]

The candidate covariance center is

\[
\boxed{
\widehat\Gamma_{\mathrm{IW}}(\tau)
=
\frac{1}{N-q}
Z_\tau^\mathsf T P_{G_\tau} Z_\tau
}.
\]

This is a deterministic function of the observed target record and the candidate physical timescale.

If \(\tau=\tau_*\), Proposition 56 proves

\[
(N-q)\widehat\Gamma_{\mathrm{IW}}(\tau_*)
\sim
\operatorname{Wishart}_d(\Gamma_*,N-q).
\]

Therefore, for declared block dimension \(d\), block count \(B\), and target confidence \(1-\beta\), Proposition 47 gives a radius \(\varepsilon_\beta\) satisfying

\[
\Pr\left[
\left\|
\Gamma_*^{-1/2}
(\widehat\Gamma_{\mathrm{IW}}(\tau_*)-\Gamma_*)
\Gamma_*^{-1/2}
\right\|_2
\le\varepsilon_\beta
\right]
\ge 1-\beta.
\]

The value of \(\varepsilon_\beta\) depends on \(N-q\), \(d\), \(B\), and the requested confidence. It does **not** depend on the numerical value of \(\tau_*\).

For the Experiment AR scalar benchmark,

\[
N=120,
\qquad
q=2,
\qquad
N-q=118,
\]

and

\[
\boxed{
\varepsilon_{0.025}=0.4364443814.
}
\]

---

# 4. Candidate covariance balls

For a candidate \(\tau\), define the relative covariance ball

\[
\mathcal B_\beta(\tau;Y)
=
\left\{
\Gamma\succ0:
\left\|
\Gamma^{-1/2}
(\widehat\Gamma_{\mathrm{IW}}(\tau)-\Gamma)
\Gamma^{-1/2}
\right\|_2
\le\varepsilon_\beta
\right\}.
\]

This ball should be interpreted conditionally:

> If this candidate \(\tau\) is the true physical relaxation time, then its corresponding covariance ball has the Proposition 56 target guarantee.

Proposition 57 does not claim that every candidate ball covers \(\Gamma_*\) simultaneously.

That distinction is essential.

---

# 5. Joint calibrated confidence tube

Define

\[
\boxed{
\mathcal J_{\alpha,\beta}
=
\left\{
(\tau,\Gamma):
\tau\in\mathcal O_\alpha(Z_{\mathrm{cal}}),
\quad
\Gamma\in\mathcal B_\beta(\tau;Y)
\right\}.
}
\]

This is the Proposition 57 confidence tube.

Its centerline is

\[
\tau
\mapsto
\widehat\Gamma_{\mathrm{IW}}(\tau),
\]

and every candidate section has the same Proposition 56 matrix radius \(\varepsilon_\beta\).

## Proposition 57 coverage statement

If the calibration record and target record are independent, then under the declared Gaussian exponential-relaxation model,

\[
\boxed{
\Pr\left[
(\tau_*,\Gamma_*)
\in
\mathcal J_{\alpha,\beta}
\right]
\ge
(1-\alpha)(1-\beta).
}
\]

For

\[
1-\alpha=1-\beta=0.975,
\]

the combined lower bound is

\[
\boxed{0.950625}.
\]

---

# 6. Proof

Let

\[
A
=
\left\{
\tau_*\in\mathcal O_\alpha(Z_{\mathrm{cal}})
\right\}.
\]

By Proposition 55,

\[
\Pr(A)\ge1-\alpha.
\]

Let

\[
B
=
\left\{
\Gamma_*\in\mathcal B_\beta(\tau_*;Y)
\right\}.
\]

At the true \(\tau_*\), Proposition 56 gives exact innovation whitening, exact nuisance residual rank \(N-q\), and the Wishart reduction. Therefore

\[
\Pr(B)\ge1-\beta.
\]

The records are independent, so

\[
\Pr(A\cap B)
=
\Pr(A)\Pr(B)
\ge
(1-\alpha)(1-\beta).
\]

Whenever both events occur,

\[
\tau_*\in\mathcal O_\alpha
\]

and

\[
\Gamma_*\in\mathcal B_\beta(\tau_*;Y).
\]

By definition,

\[
(\tau_*,\Gamma_*)
\in
\mathcal J_{\alpha,\beta}.
\]

This proves the statement.

---

# 7. Why there is no continuum multiplicity penalty

The confidence tube may contain many candidate values of \(\tau\), even a continuum of them.

Proposition 57 does **not** require the target covariance event

\[
\Gamma_*\in\mathcal B_\beta(\tau;Y)
\]

to hold simultaneously for every candidate \(\tau\).

It requires that event only at the one physical value \(\tau_*\).

The calibration event says that the true \(\tau_*\) is somewhere inside the retained set. The target event says that the covariance ball corresponding to that true value covers \(\Gamma_*\).

Therefore no Bonferroni factor, grid-cardinality penalty, or union bound over candidate timescales is introduced.

This is why Proposition 57 preserves the Proposition 56 local matrix radius rather than replacing it with a much larger simultaneous-over-\(\tau\) radius.

---

# 8. Projection onto spatial covariance

If only \(\Gamma\) is of interest, project the joint tube onto covariance space:

\[
\boxed{
\mathcal G_{\alpha,\beta}(Y,Z_{\mathrm{cal}})
=
\bigcup_{\tau\in\mathcal O_\alpha(Z_{\mathrm{cal}})}
\mathcal B_\beta(\tau;Y).
}
\]

Then

\[
\Pr\left[
\Gamma_*\in\mathcal G_{\alpha,\beta}
\right]
\ge
(1-\alpha)(1-\beta).
\]

The cost of uncertain physical time appears through movement of the covariance center

\[
\widehat\Gamma_{\mathrm{IW}}(\tau)
\]

across the retained \(\tau\)-set.

This keeps two forms of uncertainty separate:

1. **target sampling uncertainty**, represented by \(\varepsilon_\beta\);
2. **physical-timescale uncertainty**, represented by the family of admissible centers.

They are not the same quantity and should not be collapsed into one number unless an additional outer-bounding theorem is introduced.

---

# 9. Scalar specialization

For \(d=1\), write

\[
\widehat\gamma(\tau)
=
\widehat\Gamma_{\mathrm{IW}}(\tau).
\]

When \(\varepsilon_\beta<1\), the relative covariance inequality is equivalent to

\[
\boxed{
\frac{\widehat\gamma(\tau)}{1+\varepsilon_\beta}
\le
\gamma
\le
\frac{\widehat\gamma(\tau)}{1-\varepsilon_\beta}.
}
\]

Thus the scalar confidence tube can be drawn directly as a lower and upper curve over the calibrated \(\tau\)-set.

A numerical grid may be used to visualize that continuum tube. Such a grid is a rendering device only. The theorem is the set-valued continuum statement above.

---

# 10. Experiment AR

Experiment AR reuses the controlled calibration and target schedules from Experiments AP and AQ.

## Controlled configuration

- true physical relaxation time: \(0.78\) s;
- calibration confidence: \(0.975\);
- target covariance confidence: \(0.975\);
- combined confidence lower bound: \(0.950625\);
- 96 independent calibration channels;
- 32 irregular calibration timestamps;
- 120 target timestamps on a separate schedule;
- target nuisance rank: 2;
- residual innovation degrees of freedom: 118;
- scalar target block for the visible confidence-tube illustration.

The Proposition 55 quadratic calibration layer retains 31 of 160 cells with hull

\[
[0.686875,0.8515625]\ \mathrm{s}.
\]

For every candidate timescale in those retained cells, the Proposition 57 section uses the same matrix-Chernoff relative radius

\[
\boxed{0.4364443814<1}.
\]

This is the same candidate-wise target radius as Proposition 56.

## One independent target record

For the deterministic display target used in Experiment AR, the exact true-\(\tau\) covariance center is approximately

\[
\widehat\gamma(0.78)=0.89415.
\]

Across the retained \(\tau\)-set, a dense numerical visibility grid gives covariance centers approximately between

\[
0.79300
\]

and

\[
0.97231.
\]

At the true \(\tau\), the scalar Proposition 57 section is approximately

\[
[0.62247,1.58662].
\]

The dense-grid visible projection of the complete displayed tube is approximately

\[
[0.55206,1.72531].
\]

The last interval is a visualization summary of the numerical candidate grid. It is not substituted for the exact continuum-set definition in the theorem.

## Seeded visibility check

A 512-trial target simulation evaluates the Proposition 56 section at the controlled true value \(\tau_*=0.78\) s. The repeated-trial calculation is only a visibility check of theorem scale. The finite-sample coverage statement comes from the Proposition 55 calibration event, exact Proposition 56 Wishart reduction at the true \(\tau\), and independence of the two records.

---

# 11. What Proposition 57 changes

The previous raw-time calibrated target theorem attempted to certify one covariance estimator uniformly over a temporal family. On this benchmark its radius remained above one.

Proposition 57 takes a different route.

It does not ask one whitener to be correct for every possible \(\tau\).

Instead, it preserves the physical model uncertainty explicitly:

\[
\text{calibrated physical-time set}
\quad\longrightarrow\quad
\text{family of exact candidate whiteners}
\quad\longrightarrow\quad
\text{joint covariance confidence tube}.
\]

The local concentration statement therefore retains the \(N-q\) innovation information identified by Proposition 56.

---

# 12. What Proposition 57 does not claim

The theorem does not claim:

- that the one-timescale exponential model is universally correct;
- that every candidate \(\tau\) in the outer cover is equally plausible;
- that every candidate covariance ball covers the true covariance simultaneously;
- that a dense plotting grid is a certified discretization of the continuum tube;
- that the projected covariance union is necessarily narrow enough for every downstream observer score;
- that covariance certification alone establishes an observer or consciousness.

The theorem is a finite-sample uncertainty-propagation result inside the declared model.

---

# 13. Failure conditions and falsification

The assumptions inherited from Propositions 53, 55, and 56 remain active:

- exact separable Gaussian covariance \(R_\tau\otimes\Gamma\);
- a stationary one-timescale exponential temporal kernel;
- strictly increasing physical timestamps;
- independent calibration and target records for the product-confidence statement;
- independent standardized calibration channels under the calibration model;
- a fixed predeclared full-rank target nuisance design;
- correct application of the same candidate whitener to target measurements and nuisance design;
- covariance blocks declared before evaluation of the target concentration guarantee.

Relevant falsification diagnostics include:

- residual serial structure after whitening at candidate timescales;
- multiple relaxation times;
- oscillatory or nonmonotone temporal covariance;
- drifting \(\tau\);
- heavy-tailed or non-Gaussian innovations;
- nonseparable space-time covariance;
- calibration-to-target temporal-law mismatch;
- target nuisance modes selected adaptively from the target noise.

If these diagnostics fail, the confidence tube may be mathematically valid for the declared model while the declared model itself is physically inappropriate.

---

# 14. Next mathematical frontier

Proposition 57 produces a statistically valid **set-valued** covariance object.

The next question is no longer how to make \(\tau\) look known. It is:

> Can the downstream information factors, world-tube scores, and recovery margins be evaluated uniformly over the Proposition 57 covariance confidence tube without replacing that structured tube by one unnecessarily large spherical covariance radius?

That is the natural next bridge back from measurement certification to the original moving-boundary observer-recovery problem.

---

# 15. Reproducibility

Implementation:

- `src/observer_math/calibrated_innovation_whitening.py`

Claim-level tests:

- `tests/test_calibrated_innovation_whitening.py`

Experiment:

- `examples/calibrated_innovation_confidence_tube.py`

Machine-readable record:

- `docs/calibrated_innovation_confidence_tube.json`

Visible figure:

- `docs/calibrated_innovation_confidence_tube.svg`

The numerical experiment illustrates theorem geometry. The probability statement comes from Proposition 55 calibration coverage, Proposition 56 exact innovation-whitened Wishart concentration at the true physical timescale, and independence of calibration and target records.