# Bibliography and citation map

This page records the literature that materially informs the conceptual framing, mathematical foundations, statistical methods, and physical-process models used in **Spatiotemporal Observer Mathematics**.

Each reference is assigned a specific role so the provenance of the research remains transparent. The source structure distinguishes:

- **conceptual lineage**, which motivates the scientific question;
- **mathematical foundations**, which supply standard identities, geometry, probability laws, or algorithms;
- **statistical methodology**, which supplies concentration, calibration, or confidence constructions;
- **physical-process lineage**, which motivates the temporal stochastic models;
- **repository development**, where definitions, propositions, proofs, and computational constructions are introduced in this research program.

Machine-readable BibTeX is maintained in [`references.bib`](../references.bib). Equation-level provenance is summarized in the [Physics + Mathematics + Citation Map](physics_mathematics_citation_map.md).

---

# 1. Primary conceptual source

## Tegmark 2015

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270.**

- DOI: https://doi.org/10.1016/j.chaos.2015.03.014
- Technical preprint: https://arxiv.org/abs/1401.1219

**Role in this repository:** Primary conceptual source for the observer-factorization question. Tegmark asks why an observer should correspond to one factorization of the physical world rather than another and studies information, integration, independence, and dynamics as candidate organizing principles. This repository takes that factorization problem as its starting point and develops a time-dependent inference framework for moving subsystem boundaries, world-tube optimization, recovery, identifiability, finite-sample measurement certification, physical-time calibration, innovation inference, and covariance-to-world-tube propagation.

The relationship is therefore one of **conceptual lineage followed by a distinct time-dependent mathematical development**. The detailed correspondence is given in [README Section 13](../README.md#13-relationship-to-tegmarks-observer-factorization-question).

<a id="related-tegmark-work-tegmark-2016"></a>

## Tegmark 2016

**Max Tegmark. "Improved Measures of Integrated Information." _PLOS Computational Biology_ 12(11) (2016): e1005123.**

- DOI: https://doi.org/10.1371/journal.pcbi.1005123
- Preprint: https://arxiv.org/abs/1601.02626

**Role:** Related work on the classification and construction of integrated-information measures across factorization choices, probability distributions, and comparison measures. It provides relevant context for treating integration as one ingredient in a broader dynamical subsystem score. The moving world-tube, transport functional, recovery theory, and finite-sample measurement program are developed separately in this repository.

---

# 2. Integrated-information lineage

The following sources provide historical and conceptual context for integration as an organizing principle in dynamical systems. The operational integration, insulation, persistence, and transport functionals used in this repository are defined separately in the mathematical framework.

## Tononi 2004

**Giulio Tononi. "An Information Integration Theory of Consciousness." _BMC Neuroscience_ 5 (2004): 42.**

- DOI: https://doi.org/10.1186/1471-2202-5-42

**Role:** Foundational integrated-information theory background, establishing integration and differentiation as central conceptual themes.

## Balduzzi and Tononi 2008

**David Balduzzi and Giulio Tononi. "Integrated Information in Discrete Dynamical Systems: Motivation and Theoretical Framework." _PLOS Computational Biology_ 4(6) (2008): e1000091.**

- DOI: https://doi.org/10.1371/journal.pcbi.1000091

**Role:** Dynamical-systems development of integrated-information ideas and useful context for analyzing organization through temporal rather than purely static structure.

## Oizumi, Albantakis, and Tononi 2014

**Masafumi Oizumi, Larissa Albantakis, and Giulio Tononi. "From the Phenomenology to the Mechanisms of Consciousness: Integrated Information Theory 3.0." _PLOS Computational Biology_ 10(5) (2014): e1003588.**

- DOI: https://doi.org/10.1371/journal.pcbi.1003588

**Role:** Later integrated-information framework providing conceptual context for distinguishing the repository's operational subsystem functionals from formal IIT measures.

---

# 3. Information theory, multivariate statistics, geometry, and optimization

## Shannon 1948

**Claude E. Shannon. "A Mathematical Theory of Communication." _Bell System Technical Journal_ 27 (1948).**

- Part I, 27(3): 379-423. DOI: https://doi.org/10.1002/j.1538-7305.1948.tb01338.x
- Part II, 27(4): 623-656. DOI: https://doi.org/10.1002/j.1538-7305.1948.tb00917.x

**Role:** Foundational information-theoretic source for entropy and mutual information. The Gaussian mutual-information and conditional-mutual-information expressions used here are standard consequences of this framework together with multivariate Gaussian entropy identities.

## Cover and Thomas 2006

**Thomas M. Cover and Joy A. Thomas. _Elements of Information Theory_, 2nd ed. Wiley, 2006.**

- DOI: https://doi.org/10.1002/047174882X

**Role:** Standard reference for entropy, mutual information, conditional mutual information, data processing, and related information-theoretic identities used throughout the derivations.

## Hotelling 1936

**Harold Hotelling. "Relations Between Two Sets of Variates." _Biometrika_ 28(3-4) (1936): 321-377.**

- DOI: https://doi.org/10.1093/biomet/28.3-4.321

**Role:** Classical source for canonical correlation analysis. Canonical correlations enter the persistence and transport functionals because their whitened geometry is invariant under invertible linear coordinate changes made separately within the compared blocks.

## Jaccard 1901

**Paul Jaccard. "Etude comparative de la distribution florale dans une portion des Alpes et du Jura." _Bulletin de la Societe Vaudoise des Sciences Naturelles_ 37(142) (1901): 547-579.**

- DOI: https://doi.org/10.5169/seals-266450

**Role:** Original source for the set-overlap coefficient now known as the Jaccard index. The repository uses Jaccard distance as the declared continuity geometry between successive candidate memberships.

## Bellman 1952

**Richard Bellman. "On the Theory of Dynamic Programming." _Proceedings of the National Academy of Sciences_ 38(8) (1952): 716-719.**

- DOI: https://doi.org/10.1073/pnas.38.8.716

**Role:** Classical dynamic-programming foundation. The finite-horizon world-tube optimizer uses a max-sum dynamic program together with a two-best extension for exact runner-up recovery.

## Wishart 1928

**John Wishart. "The Generalised Product Moment Distribution in Samples from a Normal Multivariate Population." _Biometrika_ 20A(1-2) (1928): 32-52.**

- DOI: https://doi.org/10.1093/biomet/20a.1-2.32

**Role:** Classical source for the Wishart distribution underlying exact Gaussian sample-covariance laws. Proposition 56 reduces the innovation-whitened residual covariance to a Wishart law under its stated model.

## Aitken 1936

**A. C. Aitken. "On Least Squares and Linear Combination of Observations." _Proceedings of the Royal Society of Edinburgh_ 55 (1936): 42-48.**

- DOI: https://doi.org/10.1017/S0370164600014346

**Role:** Classical generalized least-squares lineage relevant to covariance-aware nuisance fitting. Proposition 56 applies nuisance removal after transformation into the temporal covariance geometry supplied by the physical-time model.

## Lancaster 1965

**H. O. Lancaster. "The Helmert Matrices." _The American Mathematical Monthly_ 72(1) (1965): 4-12.**

- DOI: https://doi.org/10.1080/00029890.1965.11970483

**Role:** Standard reference for Helmert matrices and orthogonal Helmert contrasts. Proposition 51 uses a fixed Helmert contrast to remove an arbitrary constant channel mean before constructing the residual Gaussian likelihood and e-value confidence set.

## Bhatia 1997

**Rajendra Bhatia. _Matrix Analysis_. Graduate Texts in Mathematics 169. Springer, 1997.**

- DOI: https://doi.org/10.1007/978-1-4612-0653-8

**Role:** Standard matrix-analysis reference for operator norms, eigenvalue perturbation, matrix functions, and related tools used throughout covariance perturbation, temporal-family covering, and the Proposition 58 covariance-to-factor bridge.

---

# 4. Gaussian concentration and random-matrix foundations

## Davidson and Szarek 2001

**Kenneth R. Davidson and Stanislaw J. Szarek. "Local Operator Theory, Random Matrices and Banach Spaces." In _Handbook of the Geometry of Banach Spaces_, Vol. 1, 317-366. Elsevier, 2001.**

- DOI: https://doi.org/10.1016/S1874-5849(01)80010-3

**Role:** Concentration source used in the early sample-covariance recovery route, including Proposition 9 and its descendants.

## Laurent and Massart 2000

**Beatrice Laurent and Pascal Massart. "Adaptive Estimation of a Quadratic Functional by Model Selection." _The Annals of Statistics_ 28(5) (2000): 1302-1338.**

- DOI: https://doi.org/10.1214/aos/1015957395

**Role:** Source for chi-square concentration inequalities used in the temporally dependent Gaussian calibration layer.

## Hsu, Kakade, and Zhang 2012

**Daniel Hsu, Sham M. Kakade, and Tong Zhang. "A Tail Inequality for Quadratic Forms of Subgaussian Random Vectors." _Electronic Communications in Probability_ 17(52) (2012): 1-6.**

- DOI: https://doi.org/10.1214/ECP.v17-2079
- Preprint: https://arxiv.org/abs/1110.2842

**Role:** Quadratic-form concentration reference for Gaussian and subgaussian temporal quadratic forms used in the dependent-sampling layer.

## Tropp 2012

**Joel A. Tropp. "User-Friendly Tail Bounds for Sums of Random Matrices." _Foundations of Computational Mathematics_ 12 (2012): 389-434.**

- DOI: https://doi.org/10.1007/s10208-011-9099-z

**Role:** Matrix Laplace-transform and matrix Chernoff foundation used in Proposition 47 and propagated through Propositions 48, 49, 50, and 52-57. Proposition 47 derives the Gaussian rank-one matrix moment used by this repository and then applies the matrix-Laplace strategy. Proposition 58 subsequently propagates simultaneous covariance radii into the observer objective through a deterministic composition theorem.

---

# 5. E-values and finite-sample confidence sets

## Vovk and Wang 2021

**Vladimir Vovk and Ruodu Wang. "E-values: Calibration, Combination, and Applications." _The Annals of Statistics_ 49(3) (2021): 1736-1754.**

- DOI: https://doi.org/10.1214/20-AOS2020
- Preprint: https://arxiv.org/abs/1912.06116

**Role:** Primary modern e-value reference relevant to Proposition 51 and the physical-time confidence-set sequence. The repository constructs likelihood-ratio e-values and inverts the resulting finite-sample tests to obtain continuum parameter confidence sets.

## Shafer 2021

**Glenn Shafer. "Testing by Betting: A Strategy for Statistical and Scientific Communication." _Journal of the Royal Statistical Society: Series A_ 184(2) (2021): 407-431.**

- DOI: https://doi.org/10.1111/rssa.12647

**Role:** Broader statistical context for interpreting nonnegative betting evidence and likelihood-ratio style e-values.

## Vovk and Wang 2023

**Vladimir Vovk and Ruodu Wang. "Confidence and Discoveries with E-values." _Statistical Science_ 38(2) (2023): 329-354.**

- DOI: https://doi.org/10.1214/22-STS874

**Role:** Context for confidence regions obtained from e-values and their place in the broader finite-sample statistical literature.

---

# 6. Physical relaxation and continuous-time stochastic dynamics

## Uhlenbeck and Ornstein 1930

**G. E. Uhlenbeck and L. S. Ornstein. "On the Theory of the Brownian Motion." _Physical Review_ 36 (1930): 823-841.**

- DOI: https://doi.org/10.1103/PhysRev.36.823

**Role:** Classical stochastic-relaxation lineage relevant to Proposition 53. The stationary Ornstein-Uhlenbeck process provides the canonical continuous-time Gaussian setting with exponential temporal correlation. The repository adopts the exponential kernel as a declared physical-time covariance model and develops its irregular-grid inference consequences explicitly.

## Doob 1942

**J. L. Doob. "The Brownian Movement and Stochastic Equations." _Annals of Mathematics_, Second Series, 43(2) (1942): 351-369.**

- DOI: https://doi.org/10.2307/1968873

**Role:** Classical Gaussian Markov-process lineage relevant to the irregular-grid transition structure in Proposition 53. The transition, whitening, precision, determinant, and missing-sample identities used in this repository are derived from the declared exponential covariance kernel.

---

# 7. Proposition-to-literature map

The table below identifies where external literature enters the current theorem program.

| Repository layer | Main external sources | Source role |
| --- | --- | --- |
| Observer-factorization question | Tegmark 2015 | Primary conceptual source |
| Integrated-information measure context | Tegmark 2016 | Related conceptual and mathematical context |
| Integration lineage | Tononi 2004; Balduzzi and Tononi 2008; Oizumi et al. 2014 | Historical and conceptual context |
| Gaussian information quantities | Shannon 1948; Cover and Thomas 2006 | Standard information-theoretic foundation |
| Canonical persistence and transport | Hotelling 1936; Bhatia 1997 | Multivariate-statistics and matrix foundation |
| Candidate-membership continuity | Jaccard 1901 | Set-overlap geometry |
| World-tube optimization and runner-up path | Bellman 1952 | Dynamic-programming foundation |
| Early Gaussian covariance recovery, including P9 | Wishart 1928; Davidson and Szarek 2001 | Gaussian covariance law and concentration |
| Dependent Gaussian concentration, P41-P46 | Laurent and Massart 2000; Hsu et al. 2012 | Quadratic-form concentration |
| Matrix concentration, P47-P50 and P52-P57 | Tropp 2012; Bhatia 1997 | Matrix-Laplace method and matrix analysis |
| Fixed mean removal in P51 | Lancaster 1965 | Helmert-contrast construction |
| E-value confidence construction, P51-P55 | Vovk and Wang 2021; Shafer 2021; Vovk and Wang 2023 | Finite-sample statistical methodology |
| Sampling-consistent exponential relaxation, P53-P57 | Uhlenbeck and Ornstein 1930 | Physical stochastic-process lineage |
| Irregular-grid Gaussian Markov structure, P53 | Doob 1942; Uhlenbeck and Ornstein 1930 | Gaussian Markov and relaxation context |
| Covariance-aware nuisance fitting, P56 | Aitken 1936; Wishart 1928 | Generalized least-squares and Gaussian covariance context |
| Robust transformed temporal-family cover, P57 | Bhatia 1997; Tropp 2012; P49/P53 internal results | Matrix perturbation and concentration methodology |
| Covariance-to-world-tube bridge, P58 | Shannon 1948; Cover and Thomas 2006; Hotelling 1936; Bhatia 1997; Bellman 1952 | Standard ingredients combined by the repository theorem |

---

# 8. How to cite this repository

Software citation metadata are maintained in [`CITATION.cff`](../CITATION.cff), which GitHub can render into standard citation formats.

A minimal repository citation is:

> Mahsa Keikha. _Spatiotemporal Observer Mathematics_. Version 0.47.1. 2026. https://github.com/MahsaKeikha/spatiotemporal-observer-math

For manuscript use, cite the repository together with the external source corresponding to the method or conceptual lineage being used. In particular, Tegmark 2015 should accompany discussion of the observer-factorization origin; Shannon and Cover-Thomas support information-theoretic identities; Hotelling supports canonical-correlation geometry; Bellman supports the dynamic-programming lineage; Tropp supports the matrix-Laplace concentration framework; Vovk-Wang supports the e-value methodology; and Uhlenbeck-Ornstein and Doob provide the principal stochastic-process lineage for the physical-time sequence.

Repository-specific definitions and propositions should be cited to this repository and, where appropriate, their dedicated proof records.

---

# 9. Citation maintenance standard

The bibliography is updated whenever a proposition materially uses an external theorem, statistical construction, physical model, or conceptual framework.

The citation architecture uses three primary source labels:

1. **Conceptual source:** motivates the scientific question or interpretation of a mathematical object.
2. **Mathematical or statistical source:** supplies a standard theorem, identity, probability law, geometry, or method used in a derivation or algorithm.
3. **Repository development:** identifies definitions, propositions, proofs, and computational constructions developed in this research program.

This provenance structure keeps the intellectual lineage and the repository's mathematical contribution visible at the point where each enters the work.
