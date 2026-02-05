# =============================================================================
# LUCID EMPIRE v5.0-TITAN :: Canvas Noise Generator
# =============================================================================
# Deterministic Perlin noise injection for canvas fingerprint synthesis.
# Creates consistent, unique fingerprints that pass entropy analysis.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# Source: Technical Documentation [cite: 1, 4]
# =============================================================================

import math
import random
from typing import List, Tuple, Optional


class PerlinNoise:
    """
    Perlin noise generator for deterministic canvas noise.
    
    Perlin noise produces smooth, natural-looking gradients that appear
    organic rather than purely random, which is key to defeating
    entropy analysis detection.
    """
    
    def __init__(self, seed: int):
        """Initialize with seed for deterministic output."""
        self.seed = seed
        self.rng = random.Random(seed)
        
        # Generate permutation table
        self.p = list(range(256))
        self.rng.shuffle(self.p)
        self.p = self.p + self.p  # Double it for overflow
        
    def _fade(self, t: float) -> float:
        """Smoothstep function for interpolation."""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, a: float, b: float, t: float) -> float:
        """Linear interpolation."""
        return a + t * (b - a)
    
    def _grad(self, hash_val: int, x: float, y: float) -> float:
        """Calculate gradient contribution."""
        h = hash_val & 3
        if h == 0:
            return x + y
        elif h == 1:
            return -x + y
        elif h == 2:
            return x - y
        else:
            return -x - y
    
    def noise2d(self, x: float, y: float) -> float:
        """
        Generate 2D Perlin noise value at (x, y).
        
        Returns value in range [-1, 1].
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
        aa = self.p[self.p[xi] + yi]
        ab = self.p[self.p[xi] + yi + 1]
        ba = self.p[self.p[xi + 1] + yi]
        bb = self.p[self.p[xi + 1] + yi + 1]
        
        # Blend gradients
        x1 = self._lerp(self._grad(aa, xf, yf), self._grad(ba, xf - 1, yf), u)
        x2 = self._lerp(self._grad(ab, xf, yf - 1), self._grad(bb, xf - 1, yf - 1), u)
        
        return self._lerp(x1, x2, v)


class CanvasNoiseGenerator:
    """
    Deterministic canvas noise generator for fingerprint synthesis.
    
    Modern detection systems use entropy analysis to detect random noise
    injection. This generator uses Perlin noise seeded with the profile
    UUID to create:
    - Consistent fingerprints across sessions (same profile = same hash)
    - Unique fingerprints per profile (different profiles = different hashes)
    - Natural-looking noise that passes entropy analysis
    
    Source: Technical Documentation [cite: 1, 4.1]
    """
    
    def __init__(
        self,
        seed: int,
        noise_intensity: float = 0.02,
        affected_channels: str = "rgb"
    ):
        """
        Initialize canvas noise generator.
        
        Args:
            seed: Deterministic seed (derived from profile UUID)
            noise_intensity: Fraction of pixels to modify (default 2%)
            affected_channels: Which color channels to modify (rgb, r, g, b)
        """
        self.seed = seed
        self.noise_intensity = noise_intensity
        self.affected_channels = affected_channels
        
        # Initialize Perlin noise generator
        self.perlin = PerlinNoise(seed)
        
        # Pre-compute noise patterns for performance
        self._noise_cache = {}
    
    def _should_modify_pixel(self, x: int, y: int, width: int, height: int) -> bool:
        """
        Determine if a pixel should be modified based on Perlin noise.
        
        Uses Perlin noise to create organic clusters of modified pixels
        rather than uniformly random distribution.
        """
        # Scale coordinates for noise sampling
        scale = 0.1
        noise_val = self.perlin.noise2d(x * scale, y * scale)
        
        # Convert to probability (0 to 1)
        probability = (noise_val + 1) / 2 * self.noise_intensity * 2
        
        # Deterministic "random" check based on position
        rng = random.Random(self.seed + x * width + y)
        return rng.random() < probability
    
    def _modify_channel(self, value: int, x: int, y: int, channel: str) -> int:
        """
        Apply deterministic noise to a color channel value.
        
        Modifies the least significant bit(s) to create subtle
        but consistent changes.
        """
        # Generate position-specific modification
        channel_offset = {"r": 0, "g": 1, "b": 2, "a": 3}.get(channel, 0)
        rng = random.Random(self.seed + x * 10000 + y * 100 + channel_offset)
        
        # XOR with least significant bit
        if rng.random() < 0.5:
            return value ^ 0x01
        return value
    
    def apply_to_rgba_data(
        self,
        data: List[int],
        width: int,
        height: int
    ) -> List[int]:
        """
        Apply deterministic noise to RGBA pixel data.
        
        This method modifies raw pixel data as would be retrieved from
        canvas.getImageData().data.
        
        Args:
            data: Flat array of RGBA values (r, g, b, a, r, g, b, a, ...)
            width: Canvas width
            height: Canvas height
            
        Returns:
            Modified pixel data with consistent noise applied
        """
        result = list(data)
        
        for y in range(height):
            for x in range(width):
                if not self._should_modify_pixel(x, y, width, height):
                    continue
                
                # Calculate pixel offset in data array
                offset = (y * width + x) * 4
                
                # Apply noise to selected channels
                if 'r' in self.affected_channels:
                    result[offset] = self._modify_channel(result[offset], x, y, 'r')
                if 'g' in self.affected_channels:
                    result[offset + 1] = self._modify_channel(result[offset + 1], x, y, 'g')
                if 'b' in self.affected_channels:
                    result[offset + 2] = self._modify_channel(result[offset + 2], x, y, 'b')
        
        return result
    
    def get_noise_pattern(self, width: int, height: int) -> List[Tuple[int, int, int]]:
        """
        Pre-generate noise pattern for canvas injection.
        
        Returns list of (x, y, channel_mask) tuples indicating which
        pixels/channels should be modified.
        """
        cache_key = (width, height)
        if cache_key in self._noise_cache:
            return self._noise_cache[cache_key]
        
        pattern = []
        for y in range(height):
            for x in range(width):
                if self._should_modify_pixel(x, y, width, height):
                    # Generate channel mask
                    channel_mask = 0
                    if 'r' in self.affected_channels:
                        channel_mask |= 1
                    if 'g' in self.affected_channels:
                        channel_mask |= 2
                    if 'b' in self.affected_channels:
                        channel_mask |= 4
                    
                    pattern.append((x, y, channel_mask))
        
        self._noise_cache[cache_key] = pattern
        return pattern
    
    def get_config(self) -> dict:
        """
        Export noise configuration for browser integration.
        
        This config is passed to Camoufox for runtime noise injection.
        """
        return {
            "enabled": True,
            "seed": self.seed,
            "intensity": self.noise_intensity,
            "channels": self.affected_channels,
            "algorithm": "perlin",
            "consistency": "deterministic"
        }
    
    def calculate_expected_hash(self, width: int, height: int) -> str:
        """
        Calculate the expected canvas hash after noise application.
        
        This allows pre-flight validation to verify noise is being
        applied correctly.
        """
        import hashlib
        
        # Generate simplified representation for hashing
        pattern = self.get_noise_pattern(width, height)
        pattern_str = str(sorted(pattern))
        
        return hashlib.sha256(pattern_str.encode()).hexdigest()[:16]
