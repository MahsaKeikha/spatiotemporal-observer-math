# Proposition 76: decision-bottleneck localization on the limiting world-tube

P75 returns a retained world-tube that minimizes a declared positive factorized path-evidence quantity. P76 turns that computational result into an engineering diagnostic.

For the limiting path p*, write

log E(p*) = sum_t log e_t(p*_t) + sum_t log g_t(p*_t,p*_{t+1}).

Each node and transition therefore has an additive log contribution. P76 reports those contributions and ranks them from smallest to largest. This identifies which declared factor is most suppressive along the current limiting path.

If the current robust evidence is E_rob and a declared decision threshold is h, then under the restricted intervention model in which exactly one binding multiplicative factor changes while all other factors and the minimizing path remain fixed, the minimum required multiplier is

m_required = max(1, h / E_rob).

This is a local sensitivity calculation, not a claim that changing a physical sensor by the same multiplier changes evidence by that amount.

## Engineering use

The result provides a diagnostic handoff:

limiting world-tube -> weakest node/transition evidence factor -> required evidence-factor improvement -> upstream physical provenance.

The next layer must connect the reported node/transition back to the covariance or measurement block that controls whether the competing physical boundary remains admissible.

## Scope

Ranking factor contributions is exact for the declared factorization. The single-factor multiplier is conditional on a fixed limiting path and fixed remaining factors. After an intervention, the robust minimizer may switch to another retained path; the full P75 dynamic program must then be rerun. P76 does not equate evidence-factor sensitivity with sensor sensitivity.
