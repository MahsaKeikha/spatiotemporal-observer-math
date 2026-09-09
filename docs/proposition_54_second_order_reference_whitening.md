# Proposition 54: second-order physical-time certification with reference whitening

## 1. Question

Proposition 53B calibrates a physical exponential relaxation time directly on irregular timestamps with finite-sample coverage. Its first deterministic outer cover is valid but conservative. On Experiment AN, the retained physical-time interval is much wider than the exact continuum e-value geometry, and the resulting raw target covariance radius is above one.

Proposition 54 asks two linked questions:

1. Can the continuum relaxation-time set be certified more tightly without changing its finite-sample coverage guarantee?
2. Can the exact irregular-time Markov whitener from Proposition 53A be used, with calibration uncertainty still present, to restore a subunit target covariance certificate?

The answer to both is yes under the declared Gaussian exponential-relaxation model.

## 2. Calibration model

Let fixed timestamps satisfy

\[
t_0<t_1<\cdots<t_{N-1},
\]

and let independent standardized Gaussian calibration channels share one physical relaxation time \(\tau_*\). For

\[
d_i=t_{i+1}-t_i,
\qquad
\alpha_i(\tau)=e^{-d_i/\tau},
\]

the exact local Gaussian transitions are

\[
X_{i+1}=\alpha_i(\tau)X_i+
\sqrt{1-\alpha_i(\tau)^2}\,\varepsilon_i.
\]

Proposition 53B defines an exact continuum e-value

\[
e_\tau=\frac{q}{p_\tau},
\]

where \(q\) is a proper mixture density fixed before calibration data are observed. Therefore, for the true parameter,

\[
\mathbb E_{\tau_*}[e_{\tau_*}]=1,
\]

and

\[
\mathcal C_\alpha
=
\{\tau:e_\tau<1/\alpha\}
\]

satisfies

\[
\Pr_{\tau_*}\{\tau_*\in\mathcal C_\alpha\}\ge 1-\alpha.
\]

Proposition 54 does not modify this probability theorem. It sharpens the deterministic containment of \(\mathcal C_\alpha\).

## 3. Exact curvature of the irregular-time likelihood

Write the tau-dependent log likelihood kernel as

\[
\ell(\tau)=\sum_i \ell_i(\alpha_i(\tau)).
\]

For each transition, the observed sufficient statistics are

\[
A_i=\sum_j X_{ij}^2,
\qquad
B_i=\sum_j X_{ij}X_{i+1,j},
\qquad
C_i=\sum_j X_{i+1,j}^2.
\]

With \(m\) calibration channels,

\[
\ell_i(a)
=-\frac m2\log(1-a^2)
-\frac{C_i-2aB_i+a^2A_i}{2(1-a^2)}.
\]

The implementation differentiates this exact local likelihood with respect to \(a\), then applies the chain rule using

\[
\alpha_i'(\tau)=\frac{d_i}{\tau^2}e^{-d_i/\tau},
\]

and

\[
\alpha_i''(\tau)
=
\frac{d_i}{\tau^3}e^{-d_i/\tau}
\left(\frac{d_i}{\tau}-2\right).
\]

This produces the exact \(\ell''(\tau)\), together with a deterministic data-dependent bound

\[
|\ell''(\tau)|\le M_{[a,b]}
\]

for every \(\tau\) in a declared cell \([a,b]\).

The scalar suprema needed for the time derivatives are finite and explicit. For \(x=d_i/\tau\),

\[
|\alpha_i'(\tau)|=\frac{x^2e^{-x}}{d_i},
\]

whose interior maximizer is \(x=2\). Likewise,

\[
|\alpha_i''(\tau)|
=
\frac{x^3|x-2|e^{-x}}{d_i^2},
\]

whose relevant interior stationary points are \(x=3-\sqrt3\) and \(x=3+\sqrt3\), together with interval endpoints.

## 4. Second-order outer cover

Let

\[
f(\tau)=\log e_\tau.
\]

Since \(\log q\) is constant in \(\tau\),

\[
f''(\tau)=-\ell''(\tau).
\]

On a cell \([a,b]\), let \(L(\tau)\) be the line joining the endpoint values \(f(a)\) and \(f(b)\). The standard interpolation remainder gives

\[
|f(\tau)-L(\tau)|
\le
\frac{M_{[a,b]}(b-a)^2}{8}.
\]

Because every convex combination of two endpoint values is at least their minimum,

\[
f(\tau)
\ge
\min\{f(a),f(b)\}
-
\frac{M_{[a,b]}(b-a)^2}{8}.
\]

Define

\[
B_{[a,b]}
=
\min\{f(a),f(b)\}
-
\frac{M_{[a,b]}(b-a)^2}{8}.
\]

A cell is excluded only if

\[
B_{[a,b]}\ge \log(1/\alpha).
\]

Let \(\mathcal O^{(2)}_\alpha\) be the union of retained cells.

### Statement 54A

For any fixed finite partition of the declared physical-time interval,

\[
\boxed{
\mathcal C_\alpha\subseteq\mathcal O^{(2)}_\alpha
}
\]

and therefore

\[
\boxed{
\Pr_{\tau_*}\{\tau_*\in\mathcal O^{(2)}_\alpha\}
\ge 1-\alpha.
}
\]

### Proof

If \(\tau\in\mathcal C_\alpha\), then \(f(\tau)<\log(1/\alpha)\). The interpolation inequality gives \(B_{[a,b]}\le f(\tau)\) for the cell containing \(\tau\). Hence that cell cannot satisfy the exclusion rule. Every point in \(\mathcal C_\alpha\) is therefore contained in a retained cell. The coverage statement follows from Proposition 53B. QED.

## 5. Reference whitening of the independent target record

Now consider an independent target record on arbitrary increasing target timestamps \(s_0,\ldots,s_{T-1}\), with fixed nuisance design \(H\).

Choose a reference time \(\tau_{\rm ref}\) using only the calibration outer cover. By default, the implementation uses the midpoint between the retained lower and upper extremes. Since this choice is made without target data, conditioning on the calibration record preserves the target concentration argument.

Proposition 53A gives the exact lower-bidiagonal innovation whitener

\[
W_{\rm ref}=W_{\tau_{\rm ref}}
\]

satisfying

\[
W_{\rm ref}K_{\tau_{\rm ref}}W_{\rm ref}^{\mathsf T}=I.
\]

After whitening, the target nuisance design becomes

\[
H_{\rm ref}=W_{\rm ref}H.
\]

For any still-compatible \(\tau\), define the transformed temporal covariance

\[
S_\tau
=
W_{\rm ref}K_\tau W_{\rm ref}^{\mathsf T}.
\]

At \(\tau=\tau_{\rm ref}\), this is exactly identity. Across a retained cell, it remains close to the cell-center transformed covariance.

## 6. Second-order target cover after whitening

For each retained calibration cell with center \(c\) and radius \(r\), differentiate the exponential covariance entrywise:

\[
K_\tau(i,j)=e^{-|s_i-s_j|/\tau}.
\]

The center derivative is transformed exactly:

\[
S_c'
=
W_{\rm ref}K_c'W_{\rm ref}^{\mathsf T}.
\]

A deterministic entrywise second-derivative envelope over the complete cell is propagated through \(|W_{\rm ref}|\). This yields a cellwise operator radius

\[
\delta_{2,c}
=
r\|S_c'\|_2+
\frac{r^2}{2}M_{2,c}
\]

such that

\[
\|S_\tau-S_c\|_2\le \delta_{2,c}
\]

throughout the cell.

The projected normalization

\[
d(\tau)=\operatorname{tr}(P_{H_{\rm ref}}S_\tau)
\]

receives a separate scalar Taylor certificate

\[
|d(\tau)-d(c)|
\le
r|d'(c)|+
\frac{r^2}{2}M_{d,c}.
\]

Taking the maxima over retained cells gives deterministic values \(\delta_2\) and \(\delta_d\) satisfying exactly the two compact-family cover assumptions of Proposition 49.

### Statement 54B

Conditional on the independent calibration record, Proposition 49 applied to the reference-whitened target family yields a target covariance event with probability at least \(1-\beta\). Therefore

\[
\boxed{
\Pr\{\text{calibration cover valid and target covariance event holds}\}
\ge
(1-\alpha)(1-\beta)
}
\]

when calibration and target records are independent.

The target theorem is uniform over every \(\tau\) in the retained Proposition 54 calibration cover.

## 7. Experiment AO

Experiment AO keeps the controlled calibration and target geometry of Experiment AN:

- true relaxation time: \(0.78\) s;
- calibration channels: 96;
- calibration timestamps: 32 irregular samples;
- target timestamps: 120 irregular samples;
- rank-2 affine target nuisance design;
- calibration confidence: 0.975;
- covariance confidence: 0.975;
- combined confidence: \(0.950625\);
- second-order calibration partition: 160 cells.

The exact e-value diagnostic interval is approximately

\[
[0.69155,0.84455]\ \mathrm{s}.
\]

The first-order Proposition 53B outer cover retains 115 cells. Proposition 54 retains only 31 cells, with certified extremes

\[
\boxed{[0.686875,0.8515625]\ \mathrm{s}}.
\]

The calibration-derived reference is

\[
\tau_{\rm ref}=0.76921875\ \mathrm{s}.
\]

The exact whitening identity is satisfied numerically to about

\[
1.9\times10^{-15}.
\]

For the reference-whitened retained family, the certified temporal operator covering radius is

\[
0.008495864441166266,
\]

and the projected-normalization covering radius is

\[
0.46699818384400943.
\]

The resulting Proposition 49 relative covariance radius is

\[
\boxed{0.6899552435608669<1}.
\]

This closes the specific above-one target-certificate bottleneck exposed by Experiment AN.

A dense deterministic visibility check over retained cells records maximum transformed temporal operator error

\[
0.004307444510228646,
\]

which is about 50.7 percent of its certificate. The maximum observed normalization error is

\[
0.46697971324957166,
\]

which is about 99.996 percent of its certificate. The latter shows that the scalar normalization certificate is tight on this controlled geometry rather than carrying a large hidden slack factor.

## 8. What changed mathematically

The improvement does not come from pretending the target record has more independent raw samples. Instead, the theorem uses the exact Markov structure supplied by the declared physical model.

The sequence is:

1. infer a finite-sample physical-time confidence set on an independent calibration record;
2. certify that continuum set with second-order interpolation geometry;
3. choose a reference relaxation time from calibration only;
4. apply the exact Proposition 53A innovation whitener at that reference;
5. transform the fixed target nuisance design by the same whitener;
6. certify the residual whitened temporal family uniformly by local Taylor bounds;
7. apply Proposition 49 to the resulting compact near-identity temporal family.

At the reference value, the temporal covariance is exactly identity. Away from it, the theorem pays only the certified calibration-compatible mismatch.

## 9. Scope and nonclaims

Proposition 54 requires the assumptions inherited from Propositions 53A, 53B, and 49:

- standardized Gaussian calibration channels;
- one shared stationary exponential relaxation time;
- a fixed common calibration timestamp grid;
- a physical-time interval declared independently of target data;
- calibration independent of the target record;
- separable Gaussian target fluctuations under the declared temporal model;
- a fixed target nuisance design chosen without target-data adaptation;
- positive projected normalization throughout the certified target cover.

The theorem does not establish that a real physical system follows one exponential relaxation law. It does not by itself identify an observer boundary. It does not establish consciousness or subjective experience.

The result is a conditional finite-sample certification theorem for the declared physical and statistical model.
