# Proposition 54: second-order certified outer cover for irregular-time relaxation calibration

## 1. Problem

Proposition 53B gives a finite-sample continuum confidence set for a physical exponential relaxation time \(\tau\) observed on arbitrary increasing timestamps. Its first certified finite outer cover uses a cell-local bound on the absolute first derivative of the log likelihood.

That certificate is valid but can be much wider than the actual continuum e-value set because it pays the largest possible slope anywhere in each cell, even when the likelihood slope at the cell center is much smaller.

Proposition 54 keeps the Proposition 53B confidence theorem unchanged and sharpens only the deterministic geometry used to cover the continuum set.

## 2. Calibration model inherited from Proposition 53B

Let

\[
t_0<t_1<\cdots<t_{N-1}
\]

be fixed timestamps and let \(m\) independent standardized Gaussian calibration channels share one physical relaxation time \(\tau_*\). For gap

\[
d_i=t_{i+1}-t_i,
\]

the exact local transition coefficient is

\[
a_i(\tau)=\exp(-d_i/\tau).
\]

Define the observed transition statistics

\[
A_i=\sum_{j=1}^m X_{ij}^2,
\qquad
B_i=\sum_{j=1}^m X_{ij}X_{i+1,j},
\qquad
C_i=\sum_{j=1}^m X_{i+1,j}^2.
\]

Up to terms independent of \(\tau\), the exact irregular-time Gaussian log likelihood is

\[
\ell(\tau)=\sum_i \ell_i(a_i(\tau)),
\]

with

\[
\ell_i(a)
=-\frac m2\log(1-a^2)
-\frac{C_i-2aB_i+a^2A_i}{2(1-a^2)}.
\]

Let \(q\) be the fixed mixture density from Proposition 53B and define

\[
\log e_\tau=\log q-\ell(\tau).
\]

For confidence level \(1-\alpha\), the exact continuum confidence set is

\[
\mathcal C_\alpha
=\left\{\tau:\log e_\tau<\log(1/\alpha)\right\}.
\]

Proposition 53B already proves

\[
\Pr_{\tau_*}\{\tau_*\in\mathcal C_\alpha\}\ge 1-\alpha.
\]

Proposition 54 does not alter that probability statement.

## 3. Exact first derivative

For one transition term,

\[
\frac{\partial \ell_i}{\partial a}
=
\frac{
-A_i a+B_i(a^2+1)-C_i a+m a(1-a^2)
}{(1-a^2)^2}.
\]

Also,

\[
\frac{d a_i}{d\tau}
=
\frac{d_i}{\tau^2}e^{-d_i/\tau}.
\]

Therefore

\[
\boxed{
\ell'(\tau)
=
\sum_i
\frac{\partial \ell_i}{\partial a}
\frac{d a_i}{d\tau}
}.
\]

This derivative is evaluated exactly at each cell center.

## 4. A deterministic second-derivative bound

Differentiating once more with respect to \(a\) gives

\[
\frac{\partial^2\ell_i}{\partial a^2}
=
\frac{
2B_i(a^3+3a)+m(1-a^4)-(A_i+C_i)(3a^2+1)
}{(1-a^2)^3}.
\]

The transition coefficient also satisfies

\[
\frac{d^2 a_i}{d\tau^2}
=
\frac{d_i}{\tau^3}e^{-d_i/\tau}
\left(\frac{d_i}{\tau}-2\right).
\]

Hence

\[
\ell''(\tau)
=
\sum_i
\left[
\frac{\partial^2\ell_i}{\partial a^2}
\left(\frac{d a_i}{d\tau}\right)^2
+
\frac{\partial\ell_i}{\partial a}
\frac{d^2a_i}{d\tau^2}
\right].
\]

Consider one cell \([L,U]\). Put

\[
a_{i,\min}=e^{-d_i/L},
\qquad
a_{i,\max}=e^{-d_i/U}.
\]

Because \(0<a<1\), the denominator \((1-a^2)\) is smallest at \(a_{i,\max}\). Taking absolute values term by term gives deterministic upper bounds for both \(|\partial\ell_i/\partial a|\) and \(|\partial^2\ell_i/\partial a^2|\) over the complete cell.

For the time derivatives, set \(x=d_i/\tau\). Then

\[
\left|\frac{da_i}{d\tau}\right|
=
\frac{x^2e^{-x}}{d_i},
\]

whose only interior maximizer is \(x=2\), and

\[
\left|\frac{d^2a_i}{d\tau^2}\right|
=
\frac{x^3|x-2|e^{-x}}{d_i^2},
\]

whose interior stationary points are

\[
x=3-\sqrt3,
\qquad
x=3+\sqrt3.
\]

Checking those candidates together with the two cell endpoints gives exact scalar suprema for the transition time derivatives. Combining the bounds through the chain rule produces a computable number \(M_{[L,U]}\) such that

\[
\boxed{
|\ell''(\tau)|\le M_{[L,U]}
\quad\text{for every }\tau\in[L,U].
}
\]

No probability statement is used in this step. The bound is deterministic conditional on the observed calibration record.

## 5. Second-order cell certificate

Let a cell have center \(c\) and radius \(r\). Taylor's theorem gives, for every \(\tau\) in the cell,

\[
\ell(\tau)
\le
\ell(c)+|\ell'(c)|r+\frac12 M_{[L,U]}r^2.
\]

Since \(\log e_\tau=\log q-\ell(\tau)\),

\[
\boxed{
\log e_\tau
\ge
\log e_c-|\ell'(c)|r-\frac12M_{[L,U]}r^2.
}
\]

Define the deterministic lower certificate

\[
L_{[L,U]}
=
\log e_c-|\ell'(c)|r-\frac12M_{[L,U]}r^2.
\]

A cell is excluded only if

\[
L_{[L,U]}\ge \log(1/\alpha).
\]

Otherwise it is retained.

Let \(\mathcal O^{(2)}_\alpha\) be the union of retained cells.

## 6. Proposition 54

Under the Proposition 53B calibration assumptions and for any fixed finite partition of the declared relaxation-time interval,

\[
\boxed{
\mathcal C_\alpha
\subseteq
\mathcal O^{(2)}_\alpha.
}
\]

Consequently,

\[
\boxed{
\Pr_{\tau_*}\{\tau_*\in\mathcal O^{(2)}_\alpha\}
\ge 1-\alpha.
}
\]

### Proof

Take any \(\tau\in\mathcal C_\alpha\), and let \([L,U]\) be the partition cell containing it. The Taylor bound proves

\[
L_{[L,U]}\le \log e_\tau.
\]

Because \(\tau\in\mathcal C_\alpha\),

\[
\log e_\tau<\log(1/\alpha).
\]

Therefore

\[
L_{[L,U]}<\log(1/\alpha),
\]

so the cell cannot be excluded. Thus every point of \(\mathcal C_\alpha\) lies in a retained cell and

\[
\mathcal C_\alpha\subseteq\mathcal O^{(2)}_\alpha.
\]

The probability statement follows immediately from Proposition 53B. QED.

## 7. Independent target composition

Suppose the calibration record and target record are independent. Conditional on the calibration record, the second-order retained cover is deterministic. Use each retained cell center as a temporal representative on the target timestamp grid.

Every admissible \(\tau\) lies within one cell radius of its representative. Over the retained physical-time span, Proposition 53A supplies a deterministic operator-Lipschitz constant for

\[
K_\tau(i,j)=e^{-|t_i-t_j|/\tau}.
\]

This gives the Proposition 49 eigenvalue and normalization cover radii. The resulting target covariance event has conditional probability at least the declared covariance confidence. Independence therefore gives the same product-confidence composition as Proposition 53B.

## 8. Experiment AO

Experiment AO reuses exactly the Experiment AN calibration and target geometry:

- true \(\tau=0.78\) s;
- 96 independent calibration channels;
- 32 irregular calibration timestamps;
- declared interval \([0.40,1.25]\) s;
- 160 fixed cells;
- calibration confidence \(0.975\);
- target covariance confidence \(0.975\);
- 120 irregular target timestamps;
- rank-2 affine target nuisance design.

The 2001-point diagnostic visualization accepts approximately

\[
[0.69155,0.84455]\ \mathrm{s}.
\]

The Proposition 53B first-order certificate retains

\[
[0.495625,1.1065625]\ \mathrm{s}
\]

with 115 of 160 cells.

The Proposition 54 second-order certificate retains only 31 cells and contracts the certified span to

\[
\boxed{
[0.686875,0.8515625]\ \mathrm{s}.
}
\]

Its width is about 73 percent smaller than the first-order certified width while still being a theorem-backed outer cover rather than a diagnostic grid interval.

With the same 1024-point numerical theta search used in Experiment AN, the downstream Proposition 49 covariance radius improves from

\[
3.1554895445
\]

to approximately

\[
\boxed{2.4208901285}.
\]

This is a substantial improvement but it remains above one.

## 9. The oracle barrier exposed by Proposition 54

To determine whether the remaining radius is caused by uncertainty in \(\tau\), Experiment AO also evaluates the target theorem with the true \(\tau=0.78\) s supplied exactly and with both temporal covering radii set to zero.

The oracle target covariance radius is still approximately

\[
\boxed{2.1672468952>1}.
\]

Therefore no refinement of the \(\tau\) outer cover alone can push this particular Proposition 49 target certificate below one. The dominant limitation is now strong temporal dependence in the target record itself.

This is the main diagnostic conclusion of Proposition 54.

## 10. Next proof target

Proposition 53A already proves that for a known \(\tau\), the irregular exponential covariance has an exact lower-bidiagonal innovation whitener \(W_\tau\) satisfying

\[
W_\tau K_\tau W_\tau^\mathsf T=I.
\]

The next theorem should therefore propagate a calibrated physical-time confidence set through the whitening map rather than apply covariance concentration directly to the strongly correlated raw target record.

The desired structure is:

1. calibrate \(\tau\) on an independent record;
2. retain a certified continuum family using Proposition 54;
3. construct candidate innovation whiteners \(W_\tau\);
4. control whitening mismatch uniformly over the retained \(\tau\)-family;
5. remove the transformed nuisance design;
6. apply an iid or near-iid matrix concentration theorem to the whitened target record.

That attacks the actual effective-information bottleneck identified by the oracle calculation.

## 11. Scope

Proposition 54 remains conditional on the Proposition 53B model:

- stationary standardized Gaussian calibration channels;
- one shared exponential relaxation time;
- independent calibration channels;
- fixed common calibration timestamps;
- a relaxation-time interval declared before calibration;
- independent calibration and target records for product-confidence composition.

It does not establish that a real system has one exponential timescale. It does not identify an observer boundary by itself, and it does not establish consciousness.
