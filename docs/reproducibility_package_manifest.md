# Reproducibility package manifest

Branch: research-i-device-observer-extension

Core extension modules:
- src/observer_math/active_measurement.py
- src/observer_math/finite_sample_certificate.py
- src/observer_math/certificate_decomposition.py
- src/observer_math/certificate_sensitivity.py
- src/observer_math/data_split.py
- src/observer_math/reacquisition_ledger.py
- src/observer_math/repair_semantics.py
- src/observer_math/decision_diagnostics.py
- src/observer_math/finite_sample_observer.py

Primary deterministic benchmark:
- examples/moving_module_certificate_curve.py

Validation:
- tests/test_certificate_decomposition.py
- tests/test_certificate_sensitivity.py
- tests/test_data_split.py
- tests/test_reacquisition_ledger.py
- .github/workflows/research-i-extension.yml

Scientific status:
See docs/research_i_maturity_audit.md. Numerical outputs are results only after
the corresponding executable benchmark and validation run complete.
