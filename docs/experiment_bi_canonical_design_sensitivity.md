# Experiment BI: canonical moving-module precision-design sensitivity

BI moves P78/P79 from the controlled policy example to the canonical 7-node, subset-size-3 moving-module benchmark used by BD.

The baseline simultaneous covariance radius is 0.0005. BI then tightens one candidate-time covariance uncertainty block at a time to 0.0002 or 0.0001 and reruns the same P58 to P70 to P69 certificate pipeline. For every intervention it records the exact retained complete-path count, retained nodes, retained edges, and the stronger P58 unique-recovery flag.

This experiment asks a concrete design question:

> Can localized improvement of one declared physical uncertainty block materially reduce certified world-tube ambiguity, or is broad precision improvement required?

The answer is determined by the generated machine-readable record, not assumed in advance.

## Numerical result

The baseline graph retains 52,178,875 complete paths, 175 nodes, and 4,892 edges. Of the 350 single-block interventions, 279 reduce both retained paths and retained edges, but none establishes unique recovery.

At radius 0.0002, 117 of 175 blocks reduce ambiguity. The mean path-count reduction is 99,288 and the largest is 764,225. At radius 0.0001, 162 of 175 blocks reduce ambiguity. The mean reduction is 273,425 and the largest is 1,484,350.

The strongest single intervention is the block at time 1 for candidate 34, corresponding to candidate subset [4, 5, 6], tightened to radius 0.0001. It reduces the retained path count from 52,178,875 to 50,694,525 and removes 48 retained edges. This is a 2.845 percent ambiguity reduction, meaningful for workload and design prioritization but far from a unique-recovery certificate.

The effect is heterogeneous across time. Time 2 has the largest mean reduction, while the largest individual reduction occurs at time 1. Stronger tightening from 0.0002 to 0.0001 never increases retained paths or edges for any of the 175 paired blocks in this declared sweep. The result supports targeted precision allocation, but it also shows that no single local improvement closes the canonical recovery problem.

## Boundary

A candidate-time covariance radius is a mathematical uncertainty block. BI does not equate it with one physical sensor, acquisition cost, or achievable hardware precision. Those interpretations require an explicit measurement model and cost map.
