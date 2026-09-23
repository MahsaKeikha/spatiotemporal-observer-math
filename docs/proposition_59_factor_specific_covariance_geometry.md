# Proposition 59: factor-specific covariance geometry

## Question

Proposition 58 deliberately used one sufficient observer block,

\[
B_{t,S}=(X_t,X_{t+1}^S),
\]

of dimension \(n+s\) for every factor. That construction is convenient because one block supports all local factors and all incoming transport edges. It is not the smallest covariance geometry required by every factor.

The next question is therefore precise:

> Which variables are actually required by each observer factor, and how much of the Proposition 58 dimensional penalty can be removed without changing the observer objective?

Proposition 59 answers this at the level of declared covariance variables.

## Statement

Let every candidate boundary have size \(s\) inside an \(n\)-coordinate measured state. For candidate \(S\) and source candidate \(U\):

1. directed integration inside \(S\) is determined by the joint covariance of
   \((X_t^S,X_{t+1}^S)\), dimension \(2s\);
2. local persistence of \(S\) is determined by the same \(2s\)-dimensional block;
3. local environmental leakage into future \(S\), conditioned on present \(S\), is determined by
   \((X_t,X_{t+1}^S)\), dimension \(n+s\);
4. transport persistence from \(U\) to \(S\) is determined by
   \((X_t^U,X_{t+1}^S)\), dimension \(2s\);
5. transport environmental leakage uses the present source and its present complement. Since these partition all present coordinates, it is determined by
   \((X_t,X_{t+1}^S)\), dimension \(n+s\).

Therefore the factor-specific sufficient dimensions are

\[
\boxed{
d_I=d_{P,\mathrm{local}}=d_{P,\mathrm{transport}}=2s,
\qquad
d_{E,\mathrm{local}}=d_{E,\mathrm{transport}}=n+s.
}
\]

These are sufficient variable sets for the existing definitions. The proposition does not assert minimality under every additional structural model.

## Proof

The result follows directly from the arguments of the implemented factor definitions.

For integration, both directed conditional mutual informations partition only the candidate coordinates at the present and future time. No coordinate in \(\bar S\) enters either conditional information calculation.

Canonical persistence uses the covariance of the two compared blocks and their cross-covariance. Local persistence compares present \(S\) with future \(S\); transport persistence compares present \(U\) with future \(S\). Both therefore require two \(s\)-coordinate blocks.

For local environmental leakage,

\[
I(X_{t+1}^S;X_t^{\bar S}\mid X_t^S),
\]

the three variable groups are future \(S\), present \(\bar S\), and present \(S\). Their union is \((X_t,X_{t+1}^S)\).

For transport leakage,

\[
I(X_{t+1}^S;X_t^{\bar U}\mid X_t^U),
\]

the source and its present environment partition the full present state. Its union is again \((X_t,X_{t+1}^S)\). This proves the stated sufficient dimensions.

## Experiment AT: dimension decomposition on the moving-module benchmark

For the controlled benchmark,

\[
n=7,\qquad s=3,\qquad T=5,\qquad C=35.
\]

Proposition 58 used \(d=10\) for all 175 time-candidate blocks. Proposition 59 separates the factors into:

| Factor | Sufficient dimension |
| --- | ---: |
| local integration | 6 |
| local persistence | 6 |
| transport persistence | 6 |
| local environmental independence | 10 |
| transport environmental independence | 10 |

Using the same exact-\(\tau\), unit-weight Proposition 47 diagnostic at 118 residual innovation degrees and 0.975 covariance confidence gives

\[
\varepsilon_{6,175}=1.4091111266,
\]

while

\[
\varepsilon_{10,175}=1.8573569119.
\]

Thus factor-specific geometry produces a real tightening for integration and persistence, but it does **not** yet place those 175 simultaneous six-dimensional blocks inside the relative perturbation regime. The six-dimensional radius first drops below one at 215 residual innovation degrees:

\[
\varepsilon_{6,175}(215)=0.9980728827,
\]

compared with 346 residual degrees for the ten-dimensional family.

More importantly, environmental leakage still requires the \(n+s=10\) block under the present score definition. Factor-specific geometry alone therefore cannot remove the dominant observer-scale bottleneck.

## Scientific conclusion

This is a useful negative result. It rules out an easy but incomplete explanation of Proposition 58's conservatism.

The current bottleneck is not merely that integration and persistence were unnecessarily assigned a ten-dimensional covariance block. Those factors can be localized to dimension six, but environmental leakage retains the full present-state conditioning geometry.

The next theorem should therefore target structure in the leakage term itself: safe environmental screening, conditional sparsity, or a direct score/action comparison that does not require a uniform inverse-covariance certificate for every full leakage block.

## Reproducibility

Implementation: `src/observer_math/factor_geometry.py`

Claim-level tests: `tests/test_factor_geometry.py`

Experiment: `examples/factor_specific_covariance_audit.py`

Machine-readable record: `docs/factor_specific_covariance_audit.json`
