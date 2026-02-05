"""
LUCID EMPIRE v5.0-TITAN - Canvas Noise Generator
=================================================
Deterministic canvas fingerprint manipulation using Perlin noise.
Generates consistent per-profile noise patterns.
"""

import hashlib
import math
import struct
from typing import List, Tuple, Optional


class PerlinNoise:
    """2D Perlin noise generator for deterministic canvas noise."""
    
    def __init__(self, seed: int = 0):
        self.seed = seed
        self.perm = self._generate_permutation(seed)
    
    def _generate_permutation(self, seed: int) -> List[int]:
        """Generate seeded permutation table."""
        import random
        random.seed(seed)
        perm = list(range(256))
        random.shuffle(perm)
        return perm + perm  # Duplicate for overflow
    
    def _fade(self, t: float) -> float:
        """Smoothstep fade function."""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, a: float, b: float, t: float) -> float:
        """Linear interpolation."""
        return a + t * (b - a)
    
    def _grad(self, hash_val: int, x: float, y: float) -> float:
        """Calculate gradient."""
        h = hash_val & 3
        if h == 0:
            return x + y
        elif h == 1:
            return -x + y
        elif h == 2:
            return x - y
        else:
            return -x - y
    
    def noise(self, x: float, y: float) -> float:
        """
        Generate 2D Perlin noise at coordinates.
        
        Returns value in range [-1, 1]
        """
        # Grid cell coordinates
        xi = int(x) & 255
        yi = int(y) & 255
        
        # Relative position in cell
        xf = x - int(x)
        yf = y - int(y)
        
        # Fade curves
        u = self._fade(xf)
        v = self._fade(yf)
        
        # Hash coordinates
        aa = self.perm[self.perm[xi] + yi]
        ab = self.perm[self.perm[xi] + yi + 1]
        ba = self.perm[self.perm[xi + 1] + yi]
        bb = self.perm[self.perm[xi + 1] + yi + 1]
        
        # Blend gradients
        x1 = self._lerp(self._grad(aa, xf, yf), self._grad(ba, xf - 1, yf), u)
        x2 = self._lerp(self._grad(ab, xf, yf - 1), self._grad(bb, xf - 1, yf - 1), u)
        
        return self._lerp(x1, x2, v)
    
    def octave_noise(self, x: float, y: float, octaves: int = 4, persistence: float = 0.5) -> float:
        """Generate multi-octave Perlin noise."""
        total = 0.0
        frequency = 1.0
        amplitude = 1.0
        max_value = 0.0
        
        for _ in range(octaves):
            total += self.noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2
        
        return total / max_value


class CanvasNoiseGenerator:
    """
    Generates deterministic canvas fingerprint noise.
    
    Uses Perlin noise with profile-specific seeds to create
    consistent but unique canvas modifications.
    """
    
    def __init__(self, profile_seed: str):
        """
        Initialize with profile-specific seed.
        
        Args:
            profile_seed: Unique seed (typically profile UUID)
        """
        self.seed_hash = int(hashlib.sha256(profile_seed.encode()).hexdigest()[:8], 16)
        self.perlin = PerlinNoise(self.seed_hash)
        
        # Profile-specific noise parameters
        import random
        random.seed(self.seed_hash)
        self.noise_intensity = random.uniform(0.01, 0.03)
        self.color_offset = (
            random.randint(-2, 2),
            random.randint(-2, 2),
            random.randint(-2, 2),
        )
        self.frequency_scale = random.uniform(0.01, 0.05)
    
    def generate_pixel_noise(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Generate RGB noise for a specific pixel.
        
        Args:
            x: Pixel X coordinate
            y: Pixel Y coordinate
        
        Returns:
            (r_delta, g_delta, b_delta) to add to original pixel
        """
        # Generate base noise
        noise_val = self.perlin.octave_noise(
            x * self.frequency_scale,
            y * self.frequency_scale,
            octaves=3
        )
        
        # Scale to pixel delta range
        base_delta = int(noise_val * 5)  # -5 to +5 range
        
        # Apply per-channel offsets
        r_delta = base_delta + self.color_offset[0]
        g_delta = base_delta + self.color_offset[1]
        b_delta = base_delta + self.color_offset[2]
        
        return (r_delta, g_delta, b_delta)
    
    def apply_to_image_data(self, image_data: bytes, width: int, height: int) -> bytes:
        """
        Apply noise to raw RGBA image data.
        
        Args:
            image_data: Raw RGBA image bytes
            width: Image width
            height: Image height
        
        Returns:
            Modified RGBA image bytes
        """
        data = bytearray(image_data)
        
        for y in range(height):
            for x in range(width):
                idx = (y * width + x) * 4
                
                r_delta, g_delta, b_delta = self.generate_pixel_noise(x, y)
                
                # Apply deltas with clamping
                data[idx] = max(0, min(255, data[idx] + r_delta))
                data[idx + 1] = max(0, min(255, data[idx + 1] + g_delta))
                data[idx + 2] = max(0, min(255, data[idx + 2] + b_delta))
                # Alpha unchanged
        
        return bytes(data)
    
    def get_fingerprint_modifier(self) -> dict:
        """
        Get parameters for JavaScript canvas fingerprint modification.
        
        Returns JavaScript-compatible configuration.
        """
        return {
            "seed": self.seed_hash,
            "intensity": self.noise_intensity,
            "colorOffset": {
                "r": self.color_offset[0],
                "g": self.color_offset[1],
                "b": self.color_offset[2],
            },
            "frequencyScale": self.frequency_scale,
        }
    
    def generate_toDataURL_noise(self, original_hash: str) -> str:
        """
        Generate a modified hash for canvas.toDataURL() fingerprint.
        
        Args:
            original_hash: Original canvas data hash
        
        Returns:
            Modified hash incorporating profile noise
        """
        combined = f"{original_hash}:{self.seed_hash}"
        return hashlib.sha256(combined.encode()).hexdigest()


class WebGLNoiseGenerator:
    """
    Generates WebGL fingerprint noise parameters.
    """
    
    def __init__(self, profile_seed: str):
        self.seed_hash = int(hashlib.sha256(profile_seed.encode()).hexdigest()[:8], 16)
        
        import random
        random.seed(self.seed_hash)
        
        # Slightly vary WebGL parameters
        self.precision_offset = random.uniform(-0.0001, 0.0001)
        self.render_offset = random.randint(-1, 1)
    
    def get_webgl_noise_params(self) -> dict:
        """Get WebGL noise parameters."""
        return {
            "precisionOffset": self.precision_offset,
            "renderOffset": self.render_offset,
            "seed": self.seed_hash,
        }


class AudioNoiseGenerator:
    """
    Generates audio fingerprint noise parameters.
    """
    
    def __init__(self, profile_seed: str):
        self.seed_hash = int(hashlib.sha256(profile_seed.encode()).hexdigest()[:8], 16)
        
        import random
        random.seed(self.seed_hash)
        
        # Audio context variations
        self.sample_rate_modifier = random.choice([0, 0, 0, 100, -100])
        self.channel_count_modifier = 0
        self.oscillator_detune = random.uniform(-0.5, 0.5)
        self.compressor_threshold = random.uniform(-0.1, 0.1)
    
    def get_audio_noise_params(self) -> dict:
        """Get audio fingerprint noise parameters."""
        return {
            "sampleRateModifier": self.sample_rate_modifier,
            "oscillatorDetune": self.oscillator_detune,
            "compressorThresholdOffset": self.compressor_threshold,
            "seed": self.seed_hash,
        }
