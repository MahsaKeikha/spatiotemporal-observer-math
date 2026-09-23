# Experiment BI: canonical moving-module precision-design sensitivity

BI moves P78/P79 from the controlled policy example to the canonical 7-node, subset-size-3 moving-module benchmark used by BD.

The baseline simultaneous covariance radius is 0.0005. BI then tightens one candidate-time covariance uncertainty block at a time to 0.0002 or 0.0001 and reruns the same P58 to P70 to P69 certificate pipeline. For every intervention it records the exact retained complete-path count, retained nodes, retained edges, and the stronger P58 unique-recovery flag.

This experiment asks a concrete design question:

> Can localized improvement of one declared physical uncertainty block materially reduce certified world-tube ambiguity, or is broad precision improvement required?

The answer is determined by the generated machine-readable record, not assumed in advance.

## Boundary

A candidate-time covariance radius is a mathematical uncertainty block. BI does not equate it with one physical sensor, acquisition cost, or achievable hardware precision. Those interpretations require an explicit measurement model and cost map.
