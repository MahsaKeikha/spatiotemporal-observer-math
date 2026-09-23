# Proposition 79: minimum certified precision intervention on a declared monotone sweep

P78 evaluates the effect of tightening one physical uncertainty block. P79 turns that operation into a design query.

Given a block k with baseline uncertainty radius delta_k, a declared finite set of achievable candidate radii, and a downstream evidence threshold h, evaluate the complete certification pipeline at radii from the least tightening to the strongest tightening. Under the declared monotonicity condition that robust evidence does not decrease as this block radius is tightened over the sweep, the first radius satisfying

E_rob(delta_k') >= h

is the minimum tightening on that declared grid that changes the evidence decision.

The reported design quantity is

Delta delta_k = delta_k - delta_k'.

## Why a grid result is useful

The method does not pretend that a differentiable local sensitivity exists across graph-topology changes. Candidate radii can instead come from hardware specifications, calibration levels, acquisition durations, or certified covariance designs. P79 asks which available design level is the first one that changes the downstream certified decision.

## Scientific boundary

This is a minimum only over the declared candidate grid and only for a sweep whose recomputed robust evidence satisfies the stated monotonicity condition. It is not a global continuous optimum, and the theorem does not assert monotonicity for arbitrary models. If the full rerun violates monotonicity, the implementation rejects the shortcut and the design points must be treated individually.
