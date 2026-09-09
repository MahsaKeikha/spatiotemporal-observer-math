# Release 0.47.1 research correction record

Date: 2026-09-08

## Scope

Release 0.47.1 is a **patch-level theorem and documentation correction**. It does not introduce a new proposition or experiment. The research record remains:

- 58 propositions;
- 45 reproducible experiments, A-Z and AA-AS;
- 33 scientific result figures;
- 223 claim-level tests.

The patch has two purposes:

1. tighten the deterministic projected-normalization cover used by Proposition 57;
2. reorganize the public documentation so the physics, equations, citations, proofs, experiments, figures, and interpretation boundaries are readable as one scientific program.

---

# 1. Proposition 57 correction

Proposition 57 uses one working relaxation time \(\tau_0\) from the independently calibrated Proposition 55 interval and transforms the target temporal covariance by

\[
C_\tau=W_0R_\tau W_0^{\mathsf T}.
\]

The transformed operator cover remains exactly the same as in the original Proposition 57 construction.

The earlier implementation bounded uncertainty in the projected temporal normalization by multiplying the transformed operator-cover radius by the residual rank. That inequality is valid but unnecessarily coarse.

Define the projected temporal normalization

\[
d(\tau)
=
\operatorname{tr}
\left(
P_GW_0R_\tau W_0^{\mathsf T}
\right).
\]

For the exponential physical-time family

\[
R_\tau(i,j)
=
\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\]

we have

\[
\frac{\partial R_\tau(i,j)}{\partial\tau}
=
\frac{|t_i-t_j|}{\tau^2}
\exp\left(-\frac{|t_i-t_j|}{\tau}\right).
\]

Therefore

\[
\boxed{
\frac{d}{d\tau}d(\tau)
=
\operatorname{tr}
\left(
P_GW_0
\frac{\partial R_\tau}{\partial\tau}
W_0^{\mathsf T}
\right)
}
\]

and a deterministic supremum of the absolute derivative over the calibrated interval gives a direct trace-specific Lipschitz certificate.

For grid spacing \(h\), the projected-normalization covering radius becomes

\[
\boxed{
\delta_d
=
\frac{h}{2}
\sup_{\tau\in[\tau_-,\tau_+]}
\left|
\frac{d}{d\tau}d(\tau)
\right|.
}
\]

This changes only the deterministic trace enclosure. The transformed operator and eigenvalue cover used by the matrix concentration theorem is unchanged.

---

# 2. Corrected Experiment AR certificate

The calibrated physical-time hull remains

\[
\tau\in[0.686875,0.8515625]\ \mathrm{s}
\]

with calibration confidence `0.975`.

The target schedule remains:

\[
N=120,
\qquad
q=2,
\qquad
N-q=118.
\]

The working relaxation time remains

\[
\tau_0=0.76921875\ \mathrm{s}.
\]

The transformed eigenvalue covering radius remains approximately

\[
0.0638793.
\]

The projected-normalization covering radius tightens from the original coarse value

\[
7.53776
\]

to approximately

\[
\boxed{0.01419745}.
\]

The resulting uniform relative covariance certificate is

\[
\boxed{
\varepsilon_{57}=0.7195879984<1.
}
\]

at combined calibration-target confidence lower bound

\[
\boxed{0.950625}.
\]

Relative to the Proposition 55 calibrated raw-time radius `2.4148799294`, the corrected Proposition 57 result is approximately a

\[
\boxed{70.2\%}
\]

reduction.

The original Proposition 57 numerical record `0.8677117535` remains part of the historical release record but is superseded by this tighter certificate.

---

# 3. Documentation architecture correction

The public documentation is reorganized around a physics-first reading order:

```text
physical question
    -> measured observables
    -> effective stochastic dynamics
    -> covariance geometry
    -> integration / insulation / persistence / transport
    -> moving world-tube objective
    -> identifiability and recovery
    -> finite-sample measurement certification
    -> experimental and figure record
    -> interpretation boundary
```

The main README now opens with a one-minute scientific thesis rather than a release-history narrative.

The Physics Guide places physical meaning beside the corresponding mathematics.

The Physics + Mathematics + Citation Map identifies, equation by equation, whether a construction is:

- a repository observation model;
- a standard mathematical identity;
- an external mathematical or statistical method;
- a repository definition;
- a repository theorem;
- or a numerical experiment.

The Visual Research Guide explains every scientific figure in terms of what is shown, why it matters, and where the associated theorem or numerical record can be verified.

---

# 4. Citation and attribution standard

The primary conceptual source remains:

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270.**

DOI: `10.1016/j.chaos.2015.03.014`.

The repository explicitly separates Tegmark's observer-factorization question from the independent mathematical developments introduced here, including time-dependent subsystem boundaries, world-tube optimization, recovery, identifiability, physical-time calibration, innovation whitening, and covariance-to-world-tube certification.

The full source-role map is maintained in:

- [`bibliography.md`](bibliography.md);
- [`physics_mathematics_citation_map.md`](physics_mathematics_citation_map.md);
- [`../references.bib`](../references.bib);
- [`../CITATION.cff`](../CITATION.cff).

A citation is not treated as endorsement, and external sources are cited only for the concepts or methods they actually supply.

---

# 5. Interpretation boundary

This patch does not change the interpretation policy.

The repository establishes conditional mathematical statements about dynamical subsystem identification under explicit assumptions. It does not establish that a recovered subsystem is conscious, that the operational score measures subjective experience, or that the declared Gaussian or exponential temporal models are universal physical laws.

Any future observer-to-consciousness claim requires additional bridge assumptions and independent empirical evidence under the [Interpretation Protocol](interpretation_protocol.md).

---

# 6. Verification map

Implementation:

- `src/observer_math/robust_innovation_whitening.py`

Claim-level theorem tests:

- `tests/test_robust_innovation_whitening.py`

Artifact checkpoint tests:

- `tests/test_robust_innovation_whitening_artifact.py`

Experiment generator:

- `examples/robust_innovation_whitened_target.py`

Deterministic figure renderer:

- `examples/render_robust_innovation_whitened_target.py`

Machine-readable result:

- `docs/robust_innovation_whitened_target.json`

Visible figure:

- `docs/robust_innovation_whitened_target.svg`

Detailed proof:

- `docs/proposition_57_robust_innovation_whitening.md`

The patch is complete only when the repository CI verifies the test suite and lint checks across the declared Python matrix.
