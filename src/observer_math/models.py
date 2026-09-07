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
