"""Minimal covariance block geometry for observer factors.

Proposition 59 separates the covariance variables required by each factor instead
of assigning the maximum observer block to every calculation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObserverFactorBlockGeometry:
    """Minimal declared block dimensions for fixed-size candidate boundaries."""

    node_count: int
    subset_size: int
    integration_dimension: int
    local_independence_dimension: int
    local_persistence_dimension: int
    transport_independence_dimension: int
    transport_persistence_dimension: int

    @property
    def maximum_dimension(self) -> int:
        return max(
            self.integration_dimension,
            self.local_independence_dimension,
            self.local_persistence_dimension,
            self.transport_independence_dimension,
            self.transport_persistence_dimension,
        )


def observer_factor_block_geometry(
    node_count: int,
    subset_size: int,
) -> ObserverFactorBlockGeometry:
    """Return covariance dimensions sufficient for each observer factor.

    For a candidate S of size s:
    * integration and local persistence use (X_t^S, X_(t+1)^S), dimension 2s;
    * local environmental independence uses (X_t, X_(t+1)^S), dimension n+s;
    * transport persistence U -> S uses (X_t^U, X_(t+1)^S), dimension 2s;
    * transport environmental independence conditions on U against its present
      complement, so it uses all X_t plus X_(t+1)^S, dimension n+s.

    The function records sufficient variable sets. It does not claim that a
    smaller representation is impossible under additional model structure.
    """
    if node_count < 2:
        raise ValueError("node_count must be at least two")
    if not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    small = 2 * subset_size
    full = node_count + subset_size
    return ObserverFactorBlockGeometry(
        node_count=node_count,
        subset_size=subset_size,
        integration_dimension=small,
        local_independence_dimension=full,
        local_persistence_dimension=small,
        transport_independence_dimension=full,
        transport_persistence_dimension=small,
    )
