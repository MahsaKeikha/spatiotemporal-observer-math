# Proposition 64: Measurement uncertainty to path-action intervals

## Purpose

P58 already maps simultaneous covariance uncertainty into candidate-local local-score and transport-score radii. P63 safely compresses a path family once valid action intervals are available. P64 closes the missing deterministic interface between them.

For path p, let the nominal action be

Ahat(p) = sum_t lhat(t,p_t) + chi sum_t thetahat(t,p_t,p_{t+1}) - lambda sum_t d(p_t,p_{t+1}).

Suppose the upstream covariance-to-score bridge supplies simultaneous radii eL(t,S) and eT(t,U,S). Define

E(p) = sum_t eL(t,p_t) + |chi| sum_t eT(t,p_t,p_{t+1}).

Then, on the same simultaneous upstream event,

A(p) lies in [Ahat(p)-E(p), Ahat(p)+E(p)].

No new probability budget is spent because P64 is deterministic conditional on the score-radius event.

## Composition with P63

Feed these intervals directly into P63. Let Lstar be the largest certified lower action bound. For tolerance eta, any path with upper bound below Lstar-eta is safely removable. Therefore the chain is now

measurement covariance event -> P58 factor/score radii -> P64 path-action intervals -> P63 certified compression -> P62 boundary-robust downstream evidence.

This is the first explicit end-to-end uncertainty interface from measurement geometry to downstream boundary-robust testing.

## Why it is useful

The system now distinguishes three outcomes:

1. Measurement precision is sufficient to eliminate many physical paths.
2. Measurement precision is insufficient, so several paths must remain.
3. Remaining boundary ambiguity materially changes the downstream conclusion under P62.

Those outcomes have different engineering responses: improve measurement precision, redesign the measured state/environment, or retain ambiguity in the scientific conclusion.

## Scope

P64 does not improve the upstream covariance concentration theorem. It preserves and exposes its uncertainty at the path level. It does not claim that a retained world-tube is conscious, and it does not allow unresolved competitors to be discarded for convenience.
