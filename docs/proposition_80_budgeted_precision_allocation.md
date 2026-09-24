# Proposition 80: exact budgeted precision allocation on a declared library

P78 measures the downstream effect of one uncertainty intervention. P79 finds the least tightening on one declared radius grid that reaches a target. P80 addresses the next engineering question: when several interventions can be purchased under a finite budget, which declared combination produces the smallest certified ambiguity?

Let \(\mathcal L=\{1,\ldots,m\}\) be a finite intervention library. Intervention \(i\) has declared positive cost \(c_i\). For a selected subset \(S\subseteq\mathcal L\), the complete certificate pipeline is rerun and returns certified ambiguity \(A(S)\) and a declared secondary score \(R(S)\). For budget \(B\) and optional cardinality limit \(K\), P80 evaluates every feasible subset

\[
\mathcal F(B,K)=\left\{S:\sum_{i\in S}c_i\le B,\ |S|\le K\right\}
\]

and returns the deterministic lexicographic optimum

\[
\operatorname*{argmin}_{S\in\mathcal F(B,K)}
\left(A(S),R(S),\sum_{i\in S}c_i,|S|,S\right).
\]

The primary objective is minimum certified ambiguity. The secondary score, total cost, cardinality, and intervention identifiers only break ties in the declared order.

## Why the full pipeline is rerun

Precision interventions can change retained nodes, retained edges, the identity of the limiting path, and the marginal value of later interventions. P80 therefore does not add single-block sensitivities as if they were independent derivatives. Every candidate allocation is evaluated jointly through the same certificate pipeline.

For a library of size \(m\) and cardinality limit \(K\), the direct method evaluates at most

\[
\sum_{k=0}^{K}\binom{m}{k}
\]

subsets. This is exact for the declared finite library but combinatorial. Screening, branch-and-bound, or validated submodular structure would be needed for much larger libraries.

## Scientific boundary

P80 is exact only over the declared intervention library, cost map, budget, candidate family, and evaluator. It does not prove that radius reduction is physically achievable, that nominal cost equals hardware cost, or that a screened library contains the global optimum. Without a separately proved structural condition, no claim of submodularity or greedy optimality is made.
