# Proposition 72: ambiguity cardinality and robust evidence are separate inferential objects

P71 provides an exact count of complete paths in the certified retained graph. P62/P66 provide worst-case downstream e-evidence over a retained physical-boundary set. P72 formalizes how these quantities should be reported together without turning path counts into probabilities.

For a retained set R with path-specific valid e-values E_p,

N_R = |R|

is the ambiguity cardinality, while

E_rob(R) = inf over p in R of E_p

is the robust evidence value.

There is no factor of N_R in this definition and no assumption that retained paths are equally probable. Cardinality measures how many physical alternatives remain; the infimum identifies the evidence bottleneck among them.

Therefore reducing N_R need not increase E_rob. Removing non-binding alternatives can reduce ambiguity while leaving robust evidence unchanged. E_rob increases only when the currently binding weak-evidence alternatives are certified away or their own evidence changes.

This distinction prevents a common but invalid interpretation: a smaller retained path fraction is not automatically stronger statistical evidence.

## Scientific boundary

P72 does not assign a prior, posterior, or probability mass to retained world-tubes. Any probabilistic weighting of physical alternatives would require a separately justified model and is outside this proposition.
