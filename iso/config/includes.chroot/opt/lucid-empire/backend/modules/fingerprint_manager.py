# =============================================================================
# LUCID EMPIRE v5.0-TITAN :: Fingerprint Manager
# =============================================================================
# Unified browser fingerprint synthesis engine.
# Coordinates Canvas, WebGL, Audio, and Navigator fingerprint components.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# Source: Technical Documentation [cite: 1, 4]
# =============================================================================

import hashlib
import random
from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class WebGLConfig:
    """WebGL fingerprint configuration."""
    vendor: str
    renderer: str
    unmasked_vendor: str
    unmasked_renderer: str
    shader_precision_vertex_high_float: tuple  # (range_min, range_max, precision)
    shader_precision_fragment_high_float: tuple
    max_texture_size: int
    max_viewport_dims: tuple
    aliased_line_width_range: tuple
    aliased_point_size_range: tuple


@dataclass
class AudioConfig:
    """AudioContext fingerprint configuration."""
    sample_rate: int
    channel_count: int
    noise_amplitude: float  # Profile-specific noise


@dataclass
class NavigatorConfig:
    """Navigator object configuration."""
    user_agent: str
    platform: str
    hardware_concurrency: int
    device_memory: int
    language: str
    languages: List[str]
    vendor: str
    max_touch_points: int
    do_not_track: str


class FingerprintManager:
    """
    Unified browser fingerprint synthesis manager.
    
    Coordinates all fingerprint components to create a consistent,
    believable hardware profile:
    - Canvas fingerprint (Perlin noise)
    - WebGL parameters (GPU masking)
    - Audio fingerprint (deterministic drift)
    - Navigator properties (user agent, hardware)
    
    All components derive from profile seeds for consistency.
    
    Source: Technical Documentation [cite: 1, 4]
    """
    
    # Common GPU configurations for spoofing
    GPU_PROFILES = {
        "nvidia_high": {
            "vendor": "Google Inc. (NVIDIA)",
            "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "unmasked_vendor": "NVIDIA Corporation",
            "unmasked_renderer": "NVIDIA GeForce RTX 3080/PCIe/SSE2"
        },
        "nvidia_mid": {
            "vendor": "Google Inc. (NVIDIA)",
            "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "unmasked_vendor": "NVIDIA Corporation",
            "unmasked_renderer": "NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2"
        },
        "amd_high": {
            "vendor": "Google Inc. (AMD)",
            "renderer": "ANGLE (AMD, AMD Radeon RX 6800 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "unmasked_vendor": "ATI Technologies Inc.",
            "unmasked_renderer": "AMD Radeon RX 6800 XT"
        },
        "intel_integrated": {
            "vendor": "Google Inc. (Intel)",
            "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "unmasked_vendor": "Intel Inc.",
            "unmasked_renderer": "Intel(R) UHD Graphics 630"
        },
        "apple_m1": {
            "vendor": "Apple Inc.",
            "renderer": "Apple M1",
            "unmasked_vendor": "Apple Inc.",
            "unmasked_renderer": "Apple M1"
        }
    }
    
    # User agent templates
    USER_AGENTS = {
        "chrome_120_win": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "chrome_120_mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "chrome_120_linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "firefox_121_win": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "firefox_121_mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"
    }
    
    def __init__(
        self,
        canvas_seed: int,
        webgl_seed: int,
        audio_seed: int,
        canvas_enabled: bool = True,
        webgl_enabled: bool = True,
        audio_enabled: bool = True,
        target_os: str = "windows",
        target_browser: str = "chrome_120"
    ):
        """
        Initialize fingerprint manager.
        
        Args:
            canvas_seed: Seed for canvas noise generation
            webgl_seed: Seed for WebGL parameter selection
            audio_seed: Seed for audio fingerprint noise
            canvas_enabled: Enable canvas fingerprinting protection
            webgl_enabled: Enable WebGL fingerprinting protection
            audio_enabled: Enable audio fingerprinting protection
            target_os: Target operating system (windows, mac, linux)
            target_browser: Target browser (chrome_120, firefox_121)
        """
        self.canvas_seed = canvas_seed
        self.webgl_seed = webgl_seed
        self.audio_seed = audio_seed
        
        self.canvas_enabled = canvas_enabled
        self.webgl_enabled = webgl_enabled
        self.audio_enabled = audio_enabled
        
        self.target_os = target_os
        self.target_browser = target_browser
        
        # Initialize components
        self._init_canvas_config()
        self._init_webgl_config()
        self._init_audio_config()
        self._init_navigator_config()
    
    def _init_canvas_config(self):
        """Initialize canvas fingerprint configuration."""
        from .canvas_noise import CanvasNoiseGenerator
        self.canvas_generator = CanvasNoiseGenerator(
            seed=self.canvas_seed,
            noise_intensity=0.02,
            affected_channels="rgb"
        )
    
    def _init_webgl_config(self):
        """Initialize WebGL fingerprint configuration."""
        rng = random.Random(self.webgl_seed)
        
        # Select GPU profile based on seed
        if self.target_os == "mac":
            gpu_key = "apple_m1"
        else:
            gpu_keys = ["nvidia_high", "nvidia_mid", "amd_high", "intel_integrated"]
            gpu_key = rng.choice(gpu_keys)
        
        gpu = self.GPU_PROFILES[gpu_key]
        
        self.webgl_config = WebGLConfig(
            vendor=gpu["vendor"],
            renderer=gpu["renderer"],
            unmasked_vendor=gpu["unmasked_vendor"],
            unmasked_renderer=gpu["unmasked_renderer"],
            shader_precision_vertex_high_float=(127, 127, 23),
            shader_precision_fragment_high_float=(127, 127, 23),
            max_texture_size=16384,
            max_viewport_dims=(16384, 16384),
            aliased_line_width_range=(1, 1),
            aliased_point_size_range=(1, 1024)
        )
    
    def _init_audio_config(self):
        """Initialize audio fingerprint configuration."""
        rng = random.Random(self.audio_seed)
        
        # Generate profile-specific audio noise amplitude
        noise_amplitude = rng.uniform(0.00001, 0.0001)
        
        self.audio_config = AudioConfig(
            sample_rate=44100,
            channel_count=2,
            noise_amplitude=noise_amplitude
        )
    
    def _init_navigator_config(self):
        """Initialize navigator configuration."""
        rng = random.Random(self.canvas_seed)  # Use canvas seed for consistency
        
        # Select appropriate user agent
        if "chrome" in self.target_browser:
            if self.target_os == "windows":
                ua = self.USER_AGENTS["chrome_120_win"]
                platform = "Win32"
            elif self.target_os == "mac":
                ua = self.USER_AGENTS["chrome_120_mac"]
                platform = "MacIntel"
            else:
                ua = self.USER_AGENTS["chrome_120_linux"]
                platform = "Linux x86_64"
            vendor = "Google Inc."
        else:
            if self.target_os == "windows":
                ua = self.USER_AGENTS["firefox_121_win"]
                platform = "Win32"
            else:
                ua = self.USER_AGENTS["firefox_121_mac"]
                platform = "MacIntel"
            vendor = ""
        
        # Generate hardware profile
        hardware_configs = [
            (8, 8),   # 8 cores, 8GB RAM
            (8, 16),  # 8 cores, 16GB RAM
            (12, 16), # 12 cores, 16GB RAM
            (16, 32), # 16 cores, 32GB RAM
        ]
        cores, memory = rng.choice(hardware_configs)
        
        self.navigator_config = NavigatorConfig(
            user_agent=ua,
            platform=platform,
            hardware_concurrency=cores,
            device_memory=memory,
            language="en-US",
            languages=["en-US", "en"],
            vendor=vendor,
            max_touch_points=0,
            do_not_track="1"
        )
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get complete fingerprint configuration for browser injection.
        
        This configuration is passed to Camoufox for runtime fingerprinting.
        """
        config = {
            "canvas": {
                "enabled": self.canvas_enabled,
                "config": self.canvas_generator.get_config() if self.canvas_enabled else {}
            },
            "webgl": {
                "enabled": self.webgl_enabled,
                "vendor": self.webgl_config.vendor,
                "renderer": self.webgl_config.renderer,
                "unmasked_vendor": self.webgl_config.unmasked_vendor,
                "unmasked_renderer": self.webgl_config.unmasked_renderer,
                "shader_precision": {
                    "vertex_high_float": list(self.webgl_config.shader_precision_vertex_high_float),
                    "fragment_high_float": list(self.webgl_config.shader_precision_fragment_high_float)
                },
                "max_texture_size": self.webgl_config.max_texture_size,
                "max_viewport_dims": list(self.webgl_config.max_viewport_dims)
            },
            "audio": {
                "enabled": self.audio_enabled,
                "sample_rate": self.audio_config.sample_rate,
                "channel_count": self.audio_config.channel_count,
                "noise_amplitude": self.audio_config.noise_amplitude
            },
            "navigator": {
                "user_agent": self.navigator_config.user_agent,
                "platform": self.navigator_config.platform,
                "hardware_concurrency": self.navigator_config.hardware_concurrency,
                "device_memory": self.navigator_config.device_memory,
                "language": self.navigator_config.language,
                "languages": self.navigator_config.languages,
                "vendor": self.navigator_config.vendor,
                "max_touch_points": self.navigator_config.max_touch_points,
                "do_not_track": self.navigator_config.do_not_track
            }
        }
        
        return config
    
    def get_fingerprint_hash(self) -> str:
        """
        Calculate expected fingerprint hash.
        
        This hash should remain constant for the same profile
        across different sessions.
        """
        # Combine all fingerprint-contributing factors
        components = [
            self.navigator_config.user_agent,
            self.webgl_config.vendor,
            self.webgl_config.renderer,
            str(self.canvas_seed),
            str(self.audio_config.noise_amplitude)
        ]
        
        combined = "|".join(components)
        return hashlib.sha256(combined.encode()).hexdigest()[:32]
    
    def validate_consistency(self) -> Dict[str, bool]:
        """
        Validate that fingerprint components are internally consistent.
        
        Checks that:
        - User agent matches platform
        - WebGL vendor matches renderer
        - Hardware specs are realistic
        """
        results = {}
        
        # Check UA/Platform consistency
        ua = self.navigator_config.user_agent
        platform = self.navigator_config.platform
        
        if "Windows" in ua and platform != "Win32":
            results["ua_platform_match"] = False
        elif "Macintosh" in ua and platform != "MacIntel":
            results["ua_platform_match"] = False
        elif "Linux" in ua and "Linux" not in platform:
            results["ua_platform_match"] = False
        else:
            results["ua_platform_match"] = True
        
        # Check WebGL consistency
        vendor = self.webgl_config.vendor.lower()
        renderer = self.webgl_config.renderer.lower()
        
        if "nvidia" in vendor and "nvidia" not in renderer:
            results["webgl_vendor_match"] = False
        elif "amd" in vendor and "amd" not in renderer:
            results["webgl_vendor_match"] = False
        elif "intel" in vendor and "intel" not in renderer:
            results["webgl_vendor_match"] = False
        else:
            results["webgl_vendor_match"] = True
        
        # Check hardware specs are realistic
        cores = self.navigator_config.hardware_concurrency
        memory = self.navigator_config.device_memory
        
        results["hardware_realistic"] = (
            cores in [2, 4, 6, 8, 10, 12, 14, 16, 24, 32] and
            memory in [2, 4, 8, 16, 32, 64]
        )
        
        results["all_valid"] = all(results.values())
        return results
