"""
LUCID EMPIRE v5.0-TITAN Backend
===============================
Kernel-level anti-detection system with eBPF network manipulation,
temporal displacement, and advanced fingerprint fabrication.
"""

__version__ = "5.0.0-TITAN"
__codename__ = "SOVEREIGN REALITY"

from .zero_detect import ZeroDetectEngine, ZeroDetectProfile
from .genesis_engine import GenesisEngine
from .firefox_injector_v2 import FirefoxProfileInjectorV2

__all__ = [
    'ZeroDetectEngine',
    'ZeroDetectProfile', 
    'GenesisEngine',
    'FirefoxProfileInjectorV2',
]
