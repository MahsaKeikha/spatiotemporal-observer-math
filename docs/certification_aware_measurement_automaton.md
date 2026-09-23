# Certification-Aware Measurement Automaton

This page turns the adaptive-measurement mathematics into an explicit device state machine while preserving the scientific boundary between physical measurement, structural inference, and interpretation.

## 1. Device state

At measurement step \(k\), define

\[
Z_k=
(\widehat{\mathcal W}_k,\mathcal C_k,\Delta_k,\mathbf E_k,a_k,m_k),
\]

where \(\widehat{\mathcal W}_k\) is the current leading moving-boundary hypothesis, \(\mathcal C_k\) is the retained competitor family, \(\Delta_k\) is the path/action margin, \(\mathbf E_k\) stores pairwise sequential evidence, \(a_k\) is the sensing configuration, and \(m_k\) is the supervisory mode.

## 2. Four modes

The measurement supervisor uses four logically distinct modes.

### DISCOVER

Use a broad admissible sensing configuration while the candidate family is insufficiently localized.

### RESOLVE

Use competitor-directed sensing when a small set of plausible world-tube hypotheses remains unresolved.

### TRACK

Use a lower-cost tracking configuration after the declared evidence conditions supporting the selected structure have been met.

### ABSTAIN

Preserve ambiguity when admissible sensing cannot distinguish the retained hypotheses or when model/certificate assumptions fail.

These are measurement-control modes, not consciousness states.

## 3. Transition logic

A conservative transition map is

\[
m_{k+1}=
\begin{cases}
\text{ABSTAIN}, & \text{if validity diagnostics fail},\\
\text{DISCOVER}, & \text{if }|\mathcal C_k|\text{ is large or unlocalized},\\
\text{TRACK}, & \text{if all declared competitor evidence gates pass},\\
\text{RESOLVE}, & \text{otherwise}.
\end{cases}
\]

A TRACK state is therefore entered because the operational structural decision is sufficiently supported under the declared model, not because the system is declared conscious.

## 4. Evidence gate

For leader \(p\) and retained competitors \(r_i\), assign \(\alpha_i>0\). Define

\[
g_k(p)=
\min_i
\left[
L_k(p,r_i)-\log(1/\alpha_i)
\right].
\]

The evidence gate passes when

\[
g_k(p)\ge0.
\]

The minimum identifies the hardest unresolved competitor and provides a natural target for RESOLVE-mode sensing.

## 5. Resolution deficit

Define the nonnegative deficit

\[
R_k(p)
=
\max_i
\left[
\log(1/\alpha_i)-L_k(p,r_i)
\right]_+.
\]

This is an operational distance-to-evidence-threshold. It is not a probability of correctness.

A sensing action can be evaluated by its expected reduction in this deficit,

\[
\mathcal V_k(a)
=
\mathbb E[
R_k(p)-R_{k+1}(p)
\mid\mathcal F_k,a
].
\]

This produces a device-level objective that is aligned with the actual certification gate rather than with an unrelated generic information score.

## 6. Proposition AM7: monotone evidence deficit under deterministic positive increments

Suppose the leader and competitor set remain fixed over an interval and every pairwise evidence increment satisfies

\[
\ell_{k+1}(p,r_i)\ge0
\qquad\text{for all retained }r_i.
\]

Then

\[
R_{k+1}(p)\le R_k(p).
\]

If, for every currently threshold-limiting competitor, the increment is strictly positive, the corresponding individual deficit strictly decreases until it reaches zero.

**Proof.**
For every \(i\),

\[
L_{k+1}(p,r_i)=L_k(p,r_i)+\ell_{k+1}(p,r_i)\ge L_k(p,r_i).
\]

Hence each term \([\log(1/\alpha_i)-L_{k+1}(p,r_i)]_+\) is no larger than its previous value. Taking the maximum preserves the inequality. The strict statement follows for an individual positive deficit when its evidence increment is strictly positive. \(\square\)

AM7 is a deterministic bookkeeping result. Real likelihood increments can be negative, so it is not a stochastic convergence theorem.

## 7. Action hierarchy

The supervisor can now use a hierarchy of sensing policies:

1. **coverage policy:** target structural disagreement;
2. **predictive policy:** target noise-normalized predictive separation;
3. **robust policy:** target the hardest retained competitor;
4. **gate-directed policy:** target expected reduction in \(R_k\).

This hierarchy keeps simple policies available as transparent baselines while exposing the progressively richer use of Research I structure.

## 8. Re-entry from TRACK

TRACK must not be absorbing. New measurements can weaken model adequacy, reveal a structural transition, or create a new near competitor.

A device should therefore return to RESOLVE or DISCOVER when declared diagnostics indicate that the tracked structural hypothesis no longer explains the observed dynamics within its model assumptions.

The exact re-entry statistic must be defined and validated before it is promoted to a theorem.

## 9. Safe behavior under observational equivalence

If two retained hypotheses produce identical predictive laws for every admissible action, active sensing cannot resolve them.

The automaton should then remain in ABSTAIN or report an equivalence class rather than selecting a labeled boundary. This connects the physical device directly to the symmetry-aware identifiability layer of Research I.

## 10. Validation requirements

A reproducible implementation should report:

- fraction of time in DISCOVER, RESOLVE, TRACK, and ABSTAIN;
- sensing cost by mode;
- number of measurements before TRACK entry;
- false TRACK entries under declared alternatives;
- re-entry frequency after structural motion;
- boundary/path recovery;
- hardest-competitor evidence trajectory;
- resolution deficit trajectory;
- behavior for an observationally equivalent pair.

The same random seeds and physical dynamics must be used across policy comparisons.

## 11. Scientific interpretation

The automaton controls the **measurement process**. It does not classify consciousness states. Its purpose is to make the physical acquisition system responsive to the uncertainty and identifiability structure already exposed by the moving-boundary mathematics.
