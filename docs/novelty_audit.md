# Relation to existing work

This note records the comparison that motivated the current construction. It is
not a priority claim. If an equivalent objective over changing subsystem paths
already exists, the scope of this project should be revised accordingly.

## The comparison being tested

Four ingredients appear together in the implemented optimization:

1. a weakest-cut measure of internal dynamical cross-prediction
2. conditional prediction entering from outside the proposed source boundary
3. basis-invariant predictive transport from one boundary to the next
4. a path cost for changing physical membership

None of these ingredients is new by itself. The narrower question is whether
their combination defines a useful subsystem-identification problem when the
identity of the subsystem is allowed to move.

## State-of-matter and factorization approach

The primary reference organizes the problem around information, integration,
independence, dynamics, utility, and the choice of tensor factorization. It also
shows why optimizing independence alone can lead to a dynamically unhelpful
basis. The present project takes that tension as its starting constraint.

The change made here is to optimize a sequence of subsystem choices rather than
one factorization. The current Gaussian implementation is classical and should
not be read as a derivation of the proposed quantum geometry.

## Geometric integrated information

Geometric integrated information measures departure from a partitioned model
using information geometry. That supplies a principled way to compare intact
and disconnected dynamics. The weakest-cut conditional-information term used
here is not the same quantity. Its role is narrower: it supplies one local score
inside a larger path problem.

A useful future comparison would replace the present local integration term with
a geometric integrated-information term while leaving transport and path
regularization unchanged. If the selected paths are stable under that
replacement, the world-tube result may not depend strongly on the particular
local integration measure.

## Dynamical independence and information closure

Dynamical independence asks when a macroscopic process is informationally closed
with respect to microscopic dynamics. This is the closest conceptual neighbor
to the leakage term. Both are concerned with whether the proposed process has
predictive dependence on variables outside it.

The present construction additionally requires internal cross-prediction and
links different source and target boundaries through time. The substantive
comparison is whether a dynamically independent macroscopic process, evaluated
at consecutive times, already induces the same path. That has not been tested.

## Integrated information decomposition

Integrated information decomposition separates temporal information into
redundant, unique, and synergistic atoms. It offers a much finer account of how
information is shared than the scalar score used here. The current project does
not reproduce or replace those atoms.

One open route is to define transport not from mean squared canonical
correlation, but from the subset of temporal atoms that can be assigned to a
source representation and recovered in a target representation. That may expose
cases in which a high canonical correlation is mostly redundant rather than
structurally informative.

## Time-dependent community detection

Multilayer community methods infer communities whose node membership changes
across network layers. Their interlayer coupling plays a role similar to the
Jaccard continuity penalty. The important difference is the source of the edge
score: the current transition reward is computed from a joint probability law
and explicitly conditions on variables outside the source boundary.

This distinction needs an experiment, not an assertion. Both methods should be
run on the same moving-module families, including cases where graph weight and
conditional predictive dependence disagree.

## Causal emergence and coarse-graining

Causal-emergence methods compare descriptions at different scales and can favor
a macro-level causal model over a micro-level one. The current candidate family
selects subsets rather than arbitrary coarse-grainings. It therefore searches a
smaller and differently structured space.

Allowing learned coarse-graining maps in place of subsets could connect these
problems. It would also remove the simple Jaccard geometry, so the path cost
would need to be defined on representations rather than memberships.

## Relativity and selection of quantum subsystems

Work on virtual subsystems, observable-induced tensor-product structures, and
quantum reference frames makes clear that subsystem structure is not generally
fixed by a bare Hilbert space. Recent searches for classical subsystems ask
which factorizations make robust quasi-classical behavior possible for a given
Hamiltonian.

The proposed geometric extension asks a different question: how should one
compare factorizations at adjacent times, after quotienting out local basis
changes? This remains an open construction. Until the quotient, metric, and
transport law are explicit, it is only a research direction.

## What would narrow or end this line of work

The present formulation should be narrowed if prior work is found that is
mathematically equivalent after a change of notation. It should be abandoned or
substantially altered if any of the following persist under careful testing:

- the path changes under an invertible reparameterization internal to a source
  or target
- structureless or externally driven nulls score as strongly as planted paths
- recovery requires choosing weights with knowledge of the answer
- the moving-boundary objective adds no predictive or recovery value over a
  fixed boundary
- the quantum path length depends on local basis labels that should be gauge
  equivalent

## References used in this comparison

1. Max Tegmark, "Consciousness as a State of Matter," *Chaos, Solitons &
   Fractals* 76 (2015), 238-270.
   [doi:10.1016/j.chaos.2015.03.014](https://doi.org/10.1016/j.chaos.2015.03.014)
2. M. Oizumi, N. Tsuchiya, and S. Amari, "Unified framework for information
   integration based on information geometry," *PNAS* 113 (2016), 14817-14822.
   [doi:10.1073/pnas.1603583113](https://doi.org/10.1073/pnas.1603583113)
3. L. Barnett and A. K. Seth, "Dynamical independence: Discovering emergent
   macroscopic processes in complex dynamical systems," *Physical Review E*
   108 (2023), 014304.
   [doi:10.1103/PhysRevE.108.014304](https://doi.org/10.1103/PhysRevE.108.014304)
4. P. A. M. Mediano et al., "Integrated information decomposition unveils major
   structural and dynamical differences among cortical areas," *PNAS* 122
   (2025), e2423297122.
   [doi:10.1073/pnas.2423297122](https://doi.org/10.1073/pnas.2423297122)
5. P. J. Mucha et al., "Community structure in time-dependent, multiscale, and
   multiplex networks," *Science* 328 (2010), 876-878.
   [doi:10.1126/science.1184819](https://doi.org/10.1126/science.1184819)
6. E. I. Hoel, "When the map is better than the territory," *Entropy* 19
   (2017), 188. [doi:10.3390/e19050188](https://doi.org/10.3390/e19050188)
7. A. Vanrietvelde et al., "A change of perspective: switching quantum reference
   frames via a perspective-neutral framework," *Quantum* 4 (2020), 225.
   [doi:10.22331/q-2020-01-27-225](https://doi.org/10.22331/q-2020-01-27-225)
8. P. Zanardi, D. A. Lidar, and S. Lloyd, "Quantum tensor product structures are
   observable induced," *Physical Review Letters* 92 (2004), 060402.
   [doi:10.1103/PhysRevLett.92.060402](https://doi.org/10.1103/PhysRevLett.92.060402)
9. "A Search for Classical Subsystems in Quantum Worlds," arXiv:2403.10895.
   [arXiv](https://arxiv.org/abs/2403.10895)
10. "Decompositions of Hilbert Space as Instances of Time," arXiv:1609.01295.
    [arXiv](https://arxiv.org/abs/1609.01295)
