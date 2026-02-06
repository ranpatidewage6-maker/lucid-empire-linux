"""
Lucid Empire v5.0-TITAN Framework

A sophisticated identity synthesis and anti-detection system that operates
at the kernel, browser, and application layers to create mathematically
consistent digital identities.

Modules:
- titan_core: Central controller and orchestration
- ebpf: Kernel-level network packet manipulation
- profile_isolation: Linux namespace-based process isolation
- temporal_wrapper: libfaketime integration for time displacement

Source: Unified Agent [cite: 1]
"""

from .titan_core import (
    TitanController,
    GenesisEngine,
    TemporalDisplacement,
    BrowserProfile,
    Persona,
    ProfilePhase,
)

__version__ = "5.0.0"
__codename__ = "TITAN"
__author__ = "Lucid Empire Project"

__all__ = [
    "TitanController",
    "GenesisEngine",
    "TemporalDisplacement",
    "BrowserProfile",
    "Persona",
    "ProfilePhase",
]
