"""Reference systems used to test the proposed measures."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatMatrix = NDArray[np.float64]


def _scale_radius(matrix: FloatMatrix, target: float = 0.86) -> FloatMatrix:
    radius = float(np.max(np.abs(np.linalg.eigvals(matrix))))
    if radius == 0.0:
        return matrix
    return matrix * (target / radius)


def ring_system(node_count: int = 6, coupling: float = 0.22) -> tuple[FloatMatrix, FloatMatrix]:
    """Stable local dynamics on a ring with independent process noise."""
    if node_count < 3:
        raise ValueError("node_count must be at least three")
    transition = np.eye(node_count) * 0.48
    for node in range(node_count):
        transition[node, (node - 1) % node_count] = coupling
        transition[node, (node + 1) % node_count] = coupling
    return _scale_radius(transition), np.eye(node_count) * 0.18


def block_system(
    block_sizes: tuple[int, ...] = (3, 3),
    *,
    internal_coupling: float = 0.25,
    external_coupling: float = 0.015,
) -> tuple[FloatMatrix, FloatMatrix]:
    """Coupled modules with strong internal and weak external dynamics."""
    if len(block_sizes) < 2 or any(size < 2 for size in block_sizes):
        raise ValueError("provide at least two blocks, each containing at least two nodes")
    node_count = sum(block_sizes)
    transition = np.eye(node_count) * 0.42
    labels = np.concatenate(
        [np.full(size, block_index) for block_index, size in enumerate(block_sizes)]
    )
    for target in range(node_count):
        for source in range(node_count):
            if target == source:
                continue
            transition[target, source] = (
                internal_coupling if labels[target] == labels[source] else external_coupling
            )
    noise = np.eye(node_count) * 0.16
    return _scale_radius(transition), noise


def correlated_but_uncoupled_system(
    node_count: int = 4,
    *,
    memory: float = 0.65,
    noise_correlation: float = 0.55,
) -> tuple[FloatMatrix, FloatMatrix]:
    """Static correlation without cross-node dynamical influence."""
    if not 0 <= noise_correlation < 1:
        raise ValueError("noise_correlation must lie in [0, 1)")
    transition = np.eye(node_count) * memory
    noise = np.full((node_count, node_count), noise_correlation)
    np.fill_diagonal(noise, 1.0)
    noise *= 0.2
    return transition, noise


def moving_module_systems(
    node_count: int = 7,
    module_size: int = 3,
    step_count: int = 5,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[FloatMatrix, FloatMatrix], ...]]:
    """Time-varying systems with a contiguous planted active module."""
    if module_size < 2 or node_count < module_size:
        raise ValueError("require 2 <= module_size <= node_count")
    if step_count < 1 or step_count > node_count - module_size + 1:
        raise ValueError("step_count exceeds the available contiguous module positions")
    planted_path = tuple(
        tuple(range(start, start + module_size)) for start in range(step_count)
    )
    systems = []
    for active in planted_path:
        transition = np.eye(node_count) * 0.32
        for target in active:
            transition[target, target] = 0.46
            for source in active:
                if source != target:
                    transition[target, source] = 0.18
        systems.append((_scale_radius(transition, 0.84), np.eye(node_count) * 0.18))
    return planted_path, tuple(systems)


def covariance_preserving_moving_cliques(
    node_count: int = 7,
    module_size: int = 3,
    step_count: int = 5,
    *,
    self_memory: float = 0.3,
    internal_coupling: float = 0.2,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[FloatMatrix, FloatMatrix], ...]]:
    """Moving cliques with exact unit covariance at every time."""
    if module_size < 2 or node_count < module_size:
        raise ValueError("require 2 <= module_size <= node_count")
    if step_count < 1 or step_count > node_count - module_size + 1:
        raise ValueError("step_count exceeds the available contiguous module positions")
    active_longitudinal = self_memory + (module_size - 1) * internal_coupling
    active_transverse = self_memory - internal_coupling
    if max(abs(self_memory), abs(active_longitudinal), abs(active_transverse)) >= 1.0:
        raise ValueError("transition spectral norm must be below one")

    planted_path = tuple(
        tuple(range(start, start + module_size)) for start in range(step_count)
    )
    systems = []
    for active in planted_path:
        transition = np.eye(node_count) * self_memory
        for target in active:
            for source in active:
                if source != target:
                    transition[target, source] = internal_coupling
        noise = np.eye(node_count) - transition @ transition.T
        systems.append((transition, noise))
    return planted_path, tuple(systems)


def perturbed_covariance_preserving_moving_cliques(
    node_count: int = 7,
    module_size: int = 3,
    step_count: int = 5,
    *,
    self_memory: float = 0.3,
    internal_coupling: float = 0.2,
    external_coupling_norm: float = 1e-5,
    noise_perturbation_norm: float = 1e-6,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[FloatMatrix, FloatMatrix], ...]]:
    """Perturb moving cliques by external coupling and anisotropic noise.

    At each time, the transition perturbation connects the planted module to
    its complement and is scaled to the requested operator norm. The diagonal
    noise perturbation has the requested operator norm and is not isotropic.
    This deterministic construction is intended for theorem checks, not as a
    general benchmark model.
    """
    if not np.isfinite(external_coupling_norm) or not np.isfinite(
        noise_perturbation_norm
    ):
        raise ValueError("perturbation norms must be finite")
    if external_coupling_norm < 0.0 or noise_perturbation_norm < 0.0:
        raise ValueError("perturbation norms must be nonnegative")
    planted_path, base_systems = covariance_preserving_moving_cliques(
        node_count,
        module_size,
        step_count,
        self_memory=self_memory,
        internal_coupling=internal_coupling,
    )
    if external_coupling_norm > 0.0 and node_count == module_size:
        raise ValueError("positive external coupling requires an outside node")

    systems = []
    anisotropy = np.linspace(-1.0, 1.0, node_count)
    for time, (active, (base_transition, base_noise)) in enumerate(
        zip(planted_path, base_systems, strict=True)
    ):
        outside = tuple(node for node in range(node_count) if node not in active)
        direction = np.zeros((node_count, node_count))
        for target in active:
            for source in outside:
                direction[target, source] = 1.0 + 0.1 * (target + source + time)
                direction[source, target] = -0.4
        direction_norm = float(np.linalg.norm(direction, ord=2))
        transition_perturbation = (
            np.zeros_like(direction)
            if direction_norm == 0.0
            else external_coupling_norm * direction / direction_norm
        )
        noise_perturbation = noise_perturbation_norm * np.diag(anisotropy)
        transition = base_transition + transition_perturbation
        noise = base_noise + noise_perturbation
        if np.linalg.eigvalsh(noise)[0] <= 0.0:
            raise ValueError("noise perturbation makes a process covariance singular")
        systems.append((transition, noise))
    return planted_path, tuple(systems)
