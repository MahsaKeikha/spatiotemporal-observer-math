# Release 0.40.0

Release 0.40.0 adds Proposition 52, Experiment AL, and a physics-first documentation layer for the observer program.

## Proposition 52

Proposition 51 constructs an exact continuum confidence set for the two-parameter temporal covariance family

\[
R_{\phi,\eta}=(1-\eta)R_\phi+\eta I.
\]

Proposition 52 converts that continuum set into a finite certified outer cover that can be used by Proposition 49 for an independent target covariance record.

A fixed parameter grid partitions the declared family into cells. A cell is discarded only when a deterministic Gaussian likelihood perturbation bound proves that every parameter in the cell lies outside the exact Proposition 51 confidence set.

If \(\mathcal C_\alpha(Z)\) is the Proposition 51 continuum set and \(\mathcal O_\alpha(Z)\) is the union of retained Proposition 52 cells, the theorem proves

\[
\mathcal C_\alpha(Z)
\subseteq
\mathcal O_\alpha(Z).
\]

This containment is deterministic after the calibration record is observed. It does not introduce a stochastic union penalty over parameter cells.

For the target covariance composition, Proposition 52 keeps two geometric remainders separate:

- a nuisance-compressed operator radius controlling projected temporal eigenvalues;
- a raw temporal operator radius, multiplied by nuisance rank, controlling projected trace normalization through the equal-trace family identity.

The distinction is required by the proof and is guarded by claim-level regression tests.

## Physical interpretation

The physical problem is not to assign meaning to a confidence grid. It is to carry uncertainty about a measured system's temporal memory into a separate covariance estimate without creating false precision.

A calibration experiment identifies which effective temporal-memory models remain compatible with the data. Proposition 52 encloses every such model in a finite certified family. An independent target record can then be certified across that whole family after a fixed nuisance drift is projected away.

The result certifies a measurement ingredient used by the moving-boundary pipeline. It does not identify an observer boundary by itself and it does not establish consciousness.

## Experiment AL

The committed controlled experiment uses

- true `phi = 0.50`;
- true `eta = 0.01`;
- 48 calibration time samples;
- 256 independent calibration channels;
- declared `phi` range `0.30` to `0.70`;
- declared `eta` range `0` to `0.05`;
- a `121 x 61` fixed outer-cover grid;
- 120 target samples;
- a rank-2 affine target nuisance design;
- calibration confidence `0.975`;
- target covariance confidence `0.975`.

The 7,381 outer-cover cells split into

- 5,325 retained cells;
- 2,056 certified excluded cells.

The target composition gives

- eigenvalue-cover radius `0.03170414963221639`;
- normalization-cover radius `0.07038592646700755`;
- combined confidence lower bound `0.9506249999999999`;
- relative covariance radius `0.8998157009696983`.

A separate 128-trial target visibility study has median relative error `0.11590478018790801`, 95th percentile `0.3044539913501027`, and maximum `0.5436312227709283`. All 128 displayed errors lie below the theorem radius.

The trial study is not the proof. The theorem guarantee comes from the Proposition 51 e-value confidence set, deterministic cell containment, and conditional Proposition 49 matrix concentration for the independent target record.

## Physics documentation

Release 0.40.0 also adds a missing explanatory layer between the equations and the physical problem.

The new [Physics Guide](physics_guide.md) explains:

- what `X_t`, `A_t`, `Q_t`, and `S_t` mean physically;
- why a moving candidate boundary is needed;
- how integration, insulation, persistence, and transport are read as dynamical properties;
- why covariance appears in the Gaussian observer objective;
- how AR(1) persistence can be related to an effective relaxation time when the model is appropriate;
- what nuisance projection removes;
- what a relative covariance radius means;
- why covariance eigenvalues are not automatically energies;
- which physical diagnostics can falsify the declared measurement model.

The [Figure Reading Guide](figure_reading_guide.md) separates structural figures, calibration figures, and certification figures and states explicitly what each plot does and does not support.

The contributor standard now requires physical accountability whenever a physical reading is intended.

## Research record

After this release, the repository records:

- 52 propositions;
- 38 reproducible experiments, A through Z and AA through AL;
- 25 scientific result figures;
- 177 claim-level tests.

The supported CI matrix remains Python 3.10, 3.11, and 3.12.

The separate physics pipeline is an explanatory diagram and is not included in the scientific-result figure count.

## Main files added

- `src/observer_math/evalue_outer_cover.py`
- `tests/test_evalue_outer_cover.py`
- `docs/proposition_52_certified_evalue_outer_cover.md`
- `examples/certified_evalue_outer_cover.py`
- `docs/certified_evalue_outer_cover.json`
- `examples/render_certified_evalue_outer_cover.py`
- `docs/certified_evalue_outer_cover.svg`
- `docs/physics_guide.md`
- `docs/physics_pipeline.svg`
- `docs/figure_reading_guide.md`

## Interpretation boundary

This release strengthens finite-sample measurement certification and physical documentation. It does not prove or measure consciousness. Any future observer-to-consciousness interpretation remains a separate bridge hypothesis under the repository's [Interpretation Protocol](interpretation_protocol.md).