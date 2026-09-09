# Bibliography and citation map

This page records the external literature that materially informs the conceptual framing, mathematical definitions, statistical tools, and physical interpretation used in this repository.

It is intentionally more explicit than a conventional short reference list. Each source is assigned a role so a reader can distinguish:

- the primary conceptual source that initiated the project;
- related Tegmark work that is scientifically adjacent but not the source of the project;
- broader consciousness and integrated-information lineage;
- classical mathematical foundations used by the definitions and algorithms;
- concentration and random-matrix results used directly in finite-sample proofs;
- modern e-value literature relevant to Propositions 51 and 52;
- physical stochastic-process literature relevant to Proposition 53.

A citation on this page does not imply endorsement of this repository by the cited author. It also does not mean that every theorem here is contained in the cited source. The repository develops its own statements and proofs, and the role of each reference is stated below.

Machine-readable BibTeX is available in [`references.bib`](../references.bib).

---

# 1. Primary conceptual source

## Tegmark 2015

**Max Tegmark. "Consciousness as a State of Matter." _Chaos, Solitons & Fractals_ 76 (2015): 238-270.**

- DOI: https://doi.org/10.1016/j.chaos.2015.03.014
- Technical preprint: https://arxiv.org/abs/1401.1219

**Role in this repository:** This is the primary conceptual source and starting point for the project. Tegmark asks why an observer perceives one factorization of the physical world rather than another and studies information, integration, independence, and dynamics as candidate organizing principles. The present repository takes that factorization and observer-identification problem as its starting question and develops a separate operational program for time-dependent subsystem boundaries, moving world-tubes, finite-sample recovery, identifiability, temporal calibration, and physical representation tests.

This is the paper from which the central research question of the repository began. The current results are not reproductions of Tegmark's derivations, and no endorsement by Tegmark is implied. The relationship is primary conceptual lineage followed by independent mathematical development.

## Related Tegmark work: Tegmark 2016

**Max Tegmark. "Improved Measures of Integrated Information." _PLoS Computational Biology_ 12(11) (2016): e1005123.**

- DOI: https://doi.org/10.1371/journal.pcbi.1005123
- Preprint: https://arxiv.org/abs/1601.02626

**Role:** Related Tegmark literature on how integrated-information measures can be classified by factorization choice, probability distributions, and comparison measures. This paper is useful context for the repository's decision to treat integration as one operational factor rather than to identify a single integration functional with consciousness. It is not the primary source of this project and is not claimed as the source of the world-tube objective or the later propositions.

---

# 2. Integrated-information and consciousness lineage

These papers are included because Tegmark's 2015 paper explicitly builds on the integrated-information tradition and because the repository uses integration as one operational ingredient in its observer-like score. The repository does not implement IIT Phi and does not claim that its score is a measure of consciousness.

## Tononi 2004

**Giulio Tononi. "An Information Integration Theory of Consciousness." _BMC Neuroscience_ 5 (2004): 42.**

- DOI: https://doi.org/10.1186/1471-2202-5-42

**Role:** Foundational integrated-information theory background. It motivates the scientific importance of asking whether information is both differentiated and integrated, but it is not the source of the repository's specific world-tube objective.

## Balduzzi and Tononi 2008

**David Balduzzi and Giulio Tononi. "Integrated Information in Discrete Dynamical Systems: Motivation and Theoretical Framework." _PLoS Computational Biology_ 4(6) (2008): e1000091.**

- DOI: https://doi.org/10.1371/journal.pcbi.1000091

**Role:** Important dynamical-systems development of integrated-information ideas. It is useful context for the repository's emphasis on dynamical rather than purely static organization.

## Oizumi, Albantakis, and Tononi 2014

**Masafumi Oizumi, Larissa Albantakis, and Giulio Tononi. "From the Phenomenology to the Mechanisms of Consciousness: Integrated Information Theory 3.0." _PLoS Computational Biology_ 10(5) (2014): e1003588.**

- DOI: https://doi.org/10.1371/journal.pcbi.1003588

**Role:** Later IIT framework included for conceptual completeness and for clearly separating this repository's operational observer mathematics from formal IIT claims.

---

# 3. Information theory, multivariate statistics, geometry, and optimization

## Shannon 1948

**Claude E. Shannon. "A Mathematical Theory of Communication." _Bell System Technical Journal_ 27 (1948).**

- Part I, 27(3): 379-423. DOI: https://doi.org/10.1002/j.1538-7305.1948.tb01338.x
- Part II, 27(4): 623-656. DOI: https://doi.org/10.1002/j.1538-7305.1948.tb00917.x

**Role:** Foundational information-theoretic source for entropy and mutual information. The Gaussian mutual-information and conditional-mutual-information expressions used by the repository are standard consequences of this framework together with multivariate Gaussian entropy formulas.

## Cover and Thomas 2006

**Thomas M. Cover and Joy A. Thomas. _Elements of Information Theory_, 2nd ed. Wiley, 2006.**

- DOI: https://doi.org/10.1002/047174882X

**Role:** Standard reference for entropy, mutual information, conditional mutual information, data processing, and related information-theoretic identities used throughout the derivations.

## Hotelling 1936

**Harold Hotelling. "Relations Between Two Sets of Variates." _Biometrika_ 28(3-4) (1936): 321-377.**

- DOI: https://doi.org/10.1093/biomet/28.3-4.321

**Role:** Classical source for canonical correlation analysis. Canonical correlations are used in the persistence and transport components because they are invariant under invertible linear coordinate changes made separately inside the compared blocks.

## Jaccard 1901

**Paul Jaccard. "Etude comparative de la distribution florale dans une portion des Alpes et du Jura." _Bulletin de la Societe Vaudoise des Sciences Naturelles_ 37(142) (1901): 547-579.**

- DOI: https://doi.org/10.5169/seals-266450

**Role:** Original source for the set-overlap coefficient now known as the Jaccard index. The repository uses Jaccard distance, one minus the overlap coefficient, as the declared material-continuity geometry between successive candidate subsystem memberships in the world-tube objective. The choice of this geometry is part of the repository definition, not a claim that Jaccard distance is the unique physically correct boundary metric.

## Bellman 1952

**Richard Bellman. "On the Theory of Dynamic Programming." _Proceedings of the National Academy of Sciences_ 38(8) (1952): 716-719.**

- DOI: https://doi.org/10.1073/pnas.38.8.716

**Role:** Classical dynamic-programming foundation. The repository's exact finite-horizon world-tube optimizer uses a max-sum dynamic program and a two-best extension to recover the exact runner-up path.

## Wishart 1928

**John Wishart. "The Generalised Product Moment Distribution in Samples from a Normal Multivariate Population." _Biometrika_ 20A(1-2) (1928): 32-52.**

- DOI: https://doi.org/10.1093/biomet/20a.1-2.32

**Role:** Classical source for the Wishart distribution underlying exact Gaussian sample-covariance laws used in the finite-sample recovery layer.

## Lancaster 1965

**H. O. Lancaster. "The Helmert Matrices." _The American Mathematical Monthly_ 72(1) (1965): 4-12.**

- DOI: https://doi.org/10.1080/00029890.1965.11970483

**Role:** Standard reference for the Helmert matrix and orthogonal Helmert contrasts. Proposition 51 uses a fixed Helmert contrast to remove an arbitrary constant channel mean exactly before constructing the residual Gaussian likelihood and e-value confidence set.

## Bhatia 1997

**Rajendra Bhatia. _Matrix Analysis_. Graduate Texts in Mathematics 169. Springer, 1997.**

- DOI: https://doi.org/10.1007/978-1-4612-0653-8

**Role:** Standard matrix-analysis reference for operator norms, eigenvalue interlacing, spectral perturbation, matrix functions, and related tools used repeatedly in covariance perturbation and temporal-family arguments.

---

# 4. Gaussian concentration and random-matrix foundations

These references are especially important because several finite-sample results depend directly on their concentration inequalities or on the matrix-Laplace method.

## Davidson and Szarek 2001

**Kenneth R. Davidson and Stanislaw J. Szarek. "Local Operator Theory, Random Matrices and Banach Spaces." In _Handbook of the Geometry of Banach Spaces_, Vol. 1, 317-366. Elsevier, 2001.**

- DOI: https://doi.org/10.1016/S1874-5849(01)80010-3

**Role:** Direct concentration source already invoked in the proof record. The Gaussian extreme-singular-value inequality is used in the early sample-covariance concentration route, including Proposition 9 and descendants.

## Laurent and Massart 2000

**Beatrice Laurent and Pascal Massart. "Adaptive Estimation of a Quadratic Functional by Model Selection." _The Annals of Statistics_ 28(5) (2000): 1302-1338.**

- DOI: https://doi.org/10.1214/aos/1015957395

**Role:** Direct source for chi-square concentration inequalities used in the temporally dependent Gaussian calibration layer.

## Hsu, Kakade, and Zhang 2012

**Daniel Hsu, Sham M. Kakade, and Tong Zhang. "A Tail Inequality for Quadratic Forms of Subgaussian Random Vectors." _Electronic Communications in Probability_ 17(52) (2012): 1-6.**

- DOI: https://doi.org/10.1214/ECP.v17-2079
- Preprint: https://arxiv.org/abs/1110.2842

**Role:** Direct quadratic-form concentration reference for Gaussian and subgaussian temporal quadratic forms. It supports the concentration route used in the dependent-sampling propositions.

## Tropp 2012

**Joel A. Tropp. "User-Friendly Tail Bounds for Sums of Random Matrices." _Foundations of Computational Mathematics_ 12 (2012): 389-434.**

- DOI: https://doi.org/10.1007/s10208-011-9099-z

**Role:** Foundational reference for the matrix Laplace-transform and matrix Chernoff methodology used in Proposition 47 and propagated through Propositions 48, 49, 50, and 52. Proposition 47 derives the particular rank-one Gaussian matrix moment used by this repository and then applies the matrix-Laplace strategy.

---

# 5. E-values and finite-sample confidence sets

## Vovk and Wang 2021

**Vladimir Vovk and Ruodu Wang. "E-values: Calibration, Combination, and Applications." _The Annals of Statistics_ 49(3) (2021): 1736-1754.**

- DOI: https://doi.org/10.1214/20-AOS2020
- Preprint: https://arxiv.org/abs/1912.06116

**Role:** Primary modern e-value reference relevant to Proposition 51. The repository uses a likelihood-ratio e-value whose expectation under the tested parameter is one, then inverts the finite-sample test to obtain a continuum confidence set.

## Shafer 2021

**Glenn Shafer. "Testing by Betting: A Strategy for Statistical and Scientific Communication." _Journal of the Royal Statistical Society: Series A_ 184(2) (2021): 407-431.**

- DOI: https://doi.org/10.1111/rssa.12647

**Role:** Broader conceptual and statistical background for interpreting nonnegative betting evidence and likelihood-ratio style e-values.

## Vovk and Wang 2023

**Vladimir Vovk and Ruodu Wang. "Confidence and Discoveries with E-values." _Statistical Science_ 38(2) (2023): 329-354.**

- DOI: https://doi.org/10.1214/22-STS874

**Role:** Directly relevant background for confidence regions obtained from e-values. Proposition 51 is self-contained, but this paper places e-value confidence sets in the broader statistical literature.

---

# 6. Physical relaxation and continuous-time stochastic dynamics

## Uhlenbeck and Ornstein 1930

**G. E. Uhlenbeck and L. S. Ornstein. "On the Theory of the Brownian Motion." _Physical Review_ 36 (1930): 823-841.**

- DOI: https://doi.org/10.1103/PhysRev.36.823

**Role:** Classical stochastic-relaxation lineage relevant to Proposition 53. The stationary Ornstein-Uhlenbeck process is the canonical continuous-time Gaussian process with exponential temporal correlation. Proposition 53 does not assume that every physical system is Ornstein-Uhlenbeck; it uses the exponential kernel as a declared model and proves sampling consistency for that model.

## Doob 1942

**J. L. Doob. "The Brownian Movement and Stochastic Equations." _Annals of Mathematics_, Second Series, 43(2) (1942): 351-369.**

- DOI: https://doi.org/10.2307/1968873

**Role:** Classical rigorous Gaussian Markov-process lineage relevant to the exact irregular-grid transition interpretation added to Proposition 53. The repository does not import a Doob theorem to obtain its formulas: Statements 8 through 12 derive the transition, whitening, precision, determinant, and missing-sample identities directly from the declared exponential covariance kernel. This citation records historical stochastic-process context rather than outsourcing the proof.

---

# 7. Proposition-to-literature map

The table below indicates the most important external foundations for each part of the repository. "Background" means the repository uses a standard concept from that literature. "Direct" means a named inequality, method, or statistical construction materially enters a proof or algorithm.

| Repository layer | Main external sources | Role |
| --- | --- | --- |
| Conceptual factorization and observer question | Tegmark 2015 | Primary conceptual source |
| Integration-measure context | Tegmark 2016 | Related Tegmark background |
| Integration and consciousness context | Tononi 2004; Balduzzi and Tononi 2008; Oizumi et al. 2014 | Background and conceptual lineage |
| Gaussian information scores | Shannon 1948; Cover and Thomas 2006 | Background |
| Canonical persistence and transport | Hotelling 1936; Bhatia 1997 | Background |
| Material continuity between candidate memberships | Jaccard 1901 | Direct geometry used by the world-tube objective |
| World-tube optimization | Bellman 1952 | Algorithmic foundation |
| Early Gaussian covariance recovery, including Proposition 9 | Wishart 1928; Davidson and Szarek 2001 | Direct |
| Dependent Gaussian concentration, Propositions 41-46 | Laurent and Massart 2000; Hsu et al. 2012 | Direct |
| Matrix concentration, Propositions 47-50 and 52 | Tropp 2012; Bhatia 1997 | Direct method and matrix background |
| Fixed mean removal in Proposition 51 | Lancaster 1965 | Direct Helmert-contrast method |
| E-value confidence construction, Propositions 51-52 | Vovk and Wang 2021; Shafer 2021; Vovk and Wang 2023 | Direct statistical lineage |
| Sampling-consistent exponential relaxation, Proposition 53 | Uhlenbeck and Ornstein 1930 | Physical stochastic-process lineage |
| Irregular-grid Gaussian Markov structure, Proposition 53 Statements 8-12 | Doob 1942; Uhlenbeck and Ornstein 1930 | Historical Markov and relaxation lineage; proof is self-contained here |

---

# 8. How to cite this repository

The software citation metadata are maintained in [`CITATION.cff`](../CITATION.cff). GitHub can render that file directly into common citation formats.

For a manuscript that uses a specific theorem, experiment, or implementation from this repository, cite the repository itself and also cite the external source appropriate to the method when the scientific context calls for it.

A minimal repository citation is:

> Mahsa Keikha. _Spatiotemporal Observer Mathematics_. Version 0.41.1. 2026. https://github.com/MahsaKeikha/spatiotemporal-observer-math

If discussing the conceptual origin of the project, cite Tegmark 2015 explicitly in addition to the repository.

If discussing integration-measure design or the broader measure-selection problem, Tegmark 2016 is useful related context, but it should not replace the primary Tegmark 2015 citation for this project's origin.

If discussing the world-tube continuity term, cite Jaccard 1901 for the underlying set-overlap geometry.

If discussing Proposition 47 or its descendants, cite Tropp 2012 for the matrix concentration lineage.

If discussing Proposition 51, cite Lancaster 1965 for the Helmert contrast and Vovk and Wang 2021 for the e-value lineage. Where confidence-set context is relevant, Vovk and Wang 2023 is also appropriate.

If discussing Proposition 53 as a physical exponential-relaxation model, cite Uhlenbeck and Ornstein 1930 as the classical stochastic-process lineage. If discussing the exact Gaussian Markov interpretation of the irregular-grid extension, Doob 1942 is useful historical context in addition to the self-contained Proposition 53 derivation.

---

# 9. Citation maintenance policy

This bibliography should be updated whenever a new proposition materially relies on an external theorem, statistical construction, physical model, or conceptual framework.

The repository distinguishes three citation statements:

1. **Primary conceptual source:** the work that directly motivated the research question.
2. **Direct mathematical or statistical source:** a theorem, inequality, distributional fact, geometry, or method materially used in a derivation or algorithm.
3. **Background lineage:** literature that places a concept in its scientific history but is not being claimed as the source of a new proposition.

That distinction is part of the audit trail. It keeps attribution complete without implying that the new results are copied from, endorsed by, or already contained in the cited literature.
