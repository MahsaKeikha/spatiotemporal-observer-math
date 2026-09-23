# Proposition 75: scalable robust-evidence minimization on a certified boundary graph

Let a retained layered world-tube graph contain the admissible paths after physical certification. Suppose an already-valid path-specific evidence quantity has the declared positive factorization

E(p) = product_t e_t(p_t) product_t g_t(p_t,p_{t+1}),

with all factors strictly positive.

Then

log E(p) = sum_t log e_t(p_t) + sum_t log g_t(p_t,p_{t+1}).

Therefore the robust envelope

E_rob = inf_{p in R} E(p)

can be computed exactly by shortest-path dynamic programming on the retained layered graph. The recurrence is

m_0(j) = log e_0(j)

for retained initial nodes, and

m_t(j) = log e_t(j) + min_i [m_{t-1}(i) + log g_{t-1}(i,j)]

over retained predecessor edges. The final minimum is min_j m_{T-1}(j). Backpointers recover a minimizing path.

The complexity is O(T C^2) in the dense layered representation and does not enumerate the potentially exponential set of complete world-tubes.

## Critical validity boundary

P75 is a computational theorem. It does not establish that an arbitrary product of local quantities is an e-value. Path-specific evidence validity must be established separately under appropriate conditional or sequential assumptions. P75 only states that, once a valid positive factorization is declared, the worst-case retained-path value can be computed exactly and scalably.
