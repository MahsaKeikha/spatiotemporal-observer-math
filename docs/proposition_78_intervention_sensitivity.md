# Proposition 78: certified single-block intervention sensitivity

P77 records which physical uncertainty blocks feed a decision-limiting graph element. P78 defines the next engineering operation: tighten one declared block uncertainty, rerun the complete certificate/evidence pipeline, and compare the resulting ambiguity and robust evidence.

For block k with baseline radius delta_k and a proposed tightened radius delta'_k <= delta_k, define the pipeline output

Phi(delta) = (N_R(delta), E_rob(delta)).

The intervention outcome is

Delta N_k = N_R(delta) - N_R(delta with delta_k replaced by delta'_k),

Delta E_k = E_rob(delta with delta_k replaced by delta'_k) - E_rob(delta).

The important point is procedural: these changes are obtained by rerunning the graph certificate and robust-evidence calculation. They are not inferred from a local score derivative.

## Engineering meaning

P78 converts provenance into an experiment-design primitive. It asks whether improving the precision assigned to a specific physical uncertainty block actually changes the certified boundary ambiguity or downstream robust evidence.

A block can therefore be classified empirically within a declared intervention range as decision-relevant or currently nonbinding. This classification is conditional on the model, candidate family, certificate, downstream evidence construction, and intervention range.

## Scope

P78 does not say that a physical sensor can in practice achieve the proposed uncertainty reduction, nor that the block is causally sufficient. It is an in-silico certified intervention on the uncertainty model. Hardware feasibility, acquisition cost, and causal perturbation must be assessed separately.
