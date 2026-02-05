# =============================================================================
# LUCID EMPIRE v5.0-TITAN Backend
# =============================================================================
# Central backend module for the TITAN anti-detection architecture.
# 
# This module provides kernel-level network sovereignty, browser fingerprint
# synthesis, and behavioral biometrics for achieving Zero Detect status.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# =============================================================================

__version__ = "5.0.0-TITAN"
__author__ = "LUCID EMPIRE Development Team"

from .zero_detect import ZeroDetectEngine, ZeroDetectProfile
from .genesis_engine import GenesisEngine
from .firefox_injector_v2 import FirefoxProfileInjectorV2

__all__ = [
    "ZeroDetectEngine",
    "ZeroDetectProfile", 
    "GenesisEngine",
    "FirefoxProfileInjectorV2",
]
