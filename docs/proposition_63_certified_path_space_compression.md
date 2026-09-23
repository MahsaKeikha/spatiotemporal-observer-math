# Proposition 63: Certified Path-Space Compression

## Usability problem

P62 can require downstream evaluation over many admissible world-tubes. P63 safely reduces that workload using simultaneous Research I action intervals rather than heuristic top-k selection.

Let A(p) be the population world-tube action and suppose the upstream certificate gives L_p <= A(p) <= U_p simultaneously. Define L_star = max_q L_q. For tolerance eta >= 0 retain

R_eta = {p : U_p >= L_star - eta}.

## Result

On the simultaneous interval-coverage event, every path whose true action is within eta of the true optimum is retained.

Proof: if A_star=max_q A(q), then L_star <= A_star. An eta-near-optimal p has A(p) >= A_star-eta >= L_star-eta. Since A(p) <= U_p, U_p >= L_star-eta, so p is retained.

## Engineering meaning

This is certificate-preserving hypothesis-space compression. It never removes a path merely because its point estimate ranks poorly. If uncertainty intervals overlap the best certified lower bound, the competitor remains visible.

The operational chain is: dynamic-program path space -> simultaneous action intervals -> certified retained set -> P62 boundary-robust evidence.

## Scientific boundary

The guarantee is conditional on simultaneous validity of the supplied action intervals. P63 does not create those intervals, does not claim that retained paths are true boundaries, and does not strengthen downstream evidence by deleting unresolved competitors.
