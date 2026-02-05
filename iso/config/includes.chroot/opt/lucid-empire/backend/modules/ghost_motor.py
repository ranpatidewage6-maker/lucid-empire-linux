# =============================================================================
# LUCID EMPIRE v5.0-TITAN :: Ghost Motor GAN
# =============================================================================
# Generative Adversarial Network for human-like mouse trajectory synthesis.
# Defeats behavioral biometrics used by PerimeterX, BioCatch, and similar systems.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# Source: Technical Documentation [cite: 1, 6]
# =============================================================================

import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
import hashlib


@dataclass
class TrajectoryPoint:
    """
    A single point in a mouse trajectory.
    """
    x: float
    y: float
    timestamp: float  # Milliseconds since trajectory start
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.timestamp)


@dataclass
class GhostMotorConfig:
    """
    Configuration for Ghost Motor trajectory generation.
    """
    # Tremor simulation (physiological hand jitter)
    tremor_frequency_hz: float = 10.0  # 8-12 Hz typical human tremor
    tremor_amplitude_px: float = 1.0   # 0.5-2 pixels
    
    # Overshoot simulation (motor control errors)
    overshoot_probability: float = 0.15  # 15% chance
    overshoot_distance_factor: float = 0.1  # 10% of target distance
    
    # Velocity profile (Fitts's Law)
    min_speed_px_ms: float = 0.5
    max_speed_px_ms: float = 3.0
    
    # Click behavior
    click_offset_std: float = 3.0  # Gaussian offset from center
    
    # Timing
    min_duration_ms: float = 100
    max_duration_ms: float = 800


class GhostMotorGAN:
    """
    Generative Adversarial Network-inspired mouse trajectory synthesizer.
    
    Creates human-like mouse movements that pass behavioral biometric checks:
    - Entropic curvature (non-linear paths)
    - Variable velocity (Fitts's Law compliance)
    - Overshoot and correction patterns
    - Micro-tremor simulation
    - Natural click point distribution
    
    Source: Technical Documentation [cite: 1, 6]
    """
    
    def __init__(self, seed: Optional[int] = None, config: Optional[GhostMotorConfig] = None):
        """
        Initialize Ghost Motor GAN.
        
        Args:
            seed: Random seed for deterministic trajectory generation
            config: Configuration parameters
        """
        self.seed = seed or int(time.time() * 1000)
        self.rng = random.Random(self.seed)
        self.config = config or GhostMotorConfig()
        
        # Pre-compute tremor phase offsets for natural variation
        self._tremor_phase_offset = self.rng.uniform(0, 2 * math.pi)
    
    def _apply_fitts_law(self, distance: float, target_width: float = 20) -> float:
        """
        Calculate movement time using Fitts's Law.
        
        Fitts's Law: MT = a + b * log2(2D/W)
        
        Where:
        - MT = movement time
        - D = distance to target
        - W = target width
        - a, b = empirically derived constants
        """
        a = 50  # Base time (ms)
        b = 150  # Scaling factor
        
        if distance < 1:
            return a
        
        # Index of difficulty
        id_value = math.log2(2 * distance / target_width)
        
        # Movement time with some randomness
        mt = a + b * id_value
        mt *= self.rng.uniform(0.8, 1.2)  # Add natural variation
        
        return max(self.config.min_duration_ms, min(self.config.max_duration_ms, mt))
    
    def _generate_bezier_control_points(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float]
    ) -> List[Tuple[float, float]]:
        """
        Generate Bezier curve control points with human-like curvature.
        
        Unlike robotic linear or simple Bezier curves, human movements
        have entropic curvature influenced by motor control noise.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Perpendicular offset for curvature
        perp_x = -dy / distance if distance > 0 else 0
        perp_y = dx / distance if distance > 0 else 0
        
        # Human curvature tends to curve toward the dominant hand
        # Using random but consistent deviation
        curvature = self.rng.gauss(0, distance * 0.15)
        
        # Control point 1 (at 1/3 of the path)
        cp1 = (
            start[0] + dx * 0.33 + perp_x * curvature * self.rng.uniform(0.5, 1.5),
            start[1] + dy * 0.33 + perp_y * curvature * self.rng.uniform(0.5, 1.5)
        )
        
        # Control point 2 (at 2/3 of the path)
        cp2 = (
            start[0] + dx * 0.66 + perp_x * curvature * self.rng.uniform(0.3, 0.8),
            start[1] + dy * 0.66 + perp_y * curvature * self.rng.uniform(0.3, 0.8)
        )
        
        return [start, cp1, cp2, end]
    
    def _bezier_point(
        self,
        control_points: List[Tuple[float, float]],
        t: float
    ) -> Tuple[float, float]:
        """
        Calculate point on cubic Bezier curve at parameter t.
        """
        p0, p1, p2, p3 = control_points
        
        # Cubic Bezier formula
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        t2 = t * t
        t3 = t2 * t
        
        x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
        y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
        
        return (x, y)
    
    def _apply_tremor(self, x: float, y: float, timestamp: float) -> Tuple[float, float]:
        """
        Apply physiological micro-tremor to coordinates.
        
        Human hands exhibit natural tremor at 8-12 Hz with 0.5-2 pixel amplitude.
        This is a key differentiator from robotic movements.
        """
        # Tremor is sinusoidal with the configured frequency
        t_seconds = timestamp / 1000.0
        tremor_angle = (2 * math.pi * self.config.tremor_frequency_hz * t_seconds + 
                       self._tremor_phase_offset)
        
        # Apply tremor in both X and Y with slight phase difference
        amplitude = self.config.tremor_amplitude_px * self.rng.uniform(0.5, 1.5)
        tremor_x = amplitude * math.sin(tremor_angle)
        tremor_y = amplitude * math.sin(tremor_angle + math.pi * 0.3)
        
        return (x + tremor_x, y + tremor_y)
    
    def _generate_velocity_profile(self, num_points: int) -> List[float]:
        """
        Generate a velocity profile following Fitts's Law.
        
        Human movement velocity follows a "slow-fast-slow" pattern:
        - Initial acceleration
        - Cruise phase at maximum velocity
        - Deceleration as target is approached
        
        This is fundamentally different from constant-velocity robotic motion.
        """
        profile = []
        for i in range(num_points):
            t = i / max(1, num_points - 1)
            
            # Bell-shaped velocity curve (Gaussian-like)
            # Peak velocity at t=0.4 (slightly before midpoint - human tendency)
            velocity = math.exp(-((t - 0.4) ** 2) / 0.1)
            
            # Add small random variations
            velocity *= self.rng.uniform(0.85, 1.15)
            
            profile.append(velocity)
        
        # Normalize
        max_vel = max(profile) if profile else 1
        return [v / max_vel for v in profile]
    
    def _generate_overshoot(
        self,
        end: Tuple[float, float],
        approach_angle: float
    ) -> Tuple[float, float]:
        """
        Generate overshoot point when motor control error occurs.
        
        ~15% of human movements overshoot the target and correct.
        """
        distance = self.config.overshoot_distance_factor * self.rng.uniform(10, 30)
        
        # Overshoot in the direction of movement
        overshoot_x = end[0] + distance * math.cos(approach_angle)
        overshoot_y = end[1] + distance * math.sin(approach_angle)
        
        return (overshoot_x, overshoot_y)
    
    def generate_trajectory(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        target_width: float = 20
    ) -> List[Tuple[float, float, float]]:
        """
        Generate a human-like mouse trajectory from start to end.
        
        The trajectory includes:
        - Naturally curved path (Bezier with entropic control points)
        - Variable velocity (Fitts's Law)
        - Micro-tremor simulation
        - Optional overshoot and correction
        
        Args:
            start: Starting coordinates (x, y)
            end: Target coordinates (x, y)
            target_width: Width of target element for Fitts's Law
            
        Returns:
            List of (x, y, timestamp_ms) tuples
        """
        trajectory = []
        
        # Calculate distance and duration
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < 1:
            # Target is very close, just return simple movement
            return [(start[0], start[1], 0), (end[0], end[1], 50)]
        
        # Calculate movement duration using Fitts's Law
        duration = self._apply_fitts_law(distance, target_width)
        
        # Determine if we should simulate overshoot
        will_overshoot = self.rng.random() < self.config.overshoot_probability
        
        # Generate control points for main path
        control_points = self._generate_bezier_control_points(start, end)
        
        # Generate velocity profile
        num_points = max(10, int(duration / 10))  # Roughly 10ms per point
        velocity_profile = self._generate_velocity_profile(num_points)
        
        # Generate trajectory points
        current_time = 0
        accumulated_distance = 0
        
        for i in range(num_points):
            t = i / max(1, num_points - 1)
            
            # Get base position from Bezier curve
            x, y = self._bezier_point(control_points, t)
            
            # Apply micro-tremor
            x, y = self._apply_tremor(x, y, current_time)
            
            trajectory.append((x, y, current_time))
            
            # Update time based on velocity profile
            if i < num_points - 1:
                base_dt = duration / num_points
                velocity_factor = velocity_profile[i]
                # Slower = more time, faster = less time
                dt = base_dt * (2 - velocity_factor)
                current_time += dt
        
        # Add overshoot and correction if applicable
        if will_overshoot and distance > 50:
            approach_angle = math.atan2(dy, dx)
            overshoot_point = self._generate_overshoot(end, approach_angle)
            
            # Add overshoot point
            overshoot_time = current_time + self.rng.uniform(20, 50)
            trajectory.append((*overshoot_point, overshoot_time))
            
            # Add correction back to target
            correction_time = overshoot_time + self.rng.uniform(30, 80)
            final_x = end[0] + self.rng.gauss(0, 2)
            final_y = end[1] + self.rng.gauss(0, 2)
            trajectory.append((final_x, final_y, correction_time))
        
        return trajectory
    
    def generate_click_offset(self, button_width: float, button_height: float) -> Tuple[float, float]:
        """
        Generate a human-like click offset from button center.
        
        Humans don't click exactly in the center of buttons.
        Click distribution follows a 2D Gaussian around the center.
        """
        # Gaussian offset - humans tend to click slightly toward center-left
        offset_x = self.rng.gauss(-button_width * 0.05, button_width * 0.15)
        offset_y = self.rng.gauss(0, button_height * 0.15)
        
        # Clamp to button bounds
        offset_x = max(-button_width/2 * 0.8, min(button_width/2 * 0.8, offset_x))
        offset_y = max(-button_height/2 * 0.8, min(button_height/2 * 0.8, offset_y))
        
        return (offset_x, offset_y)
    
    def generate_keystroke_timing(self, text: str) -> List[Tuple[str, float]]:
        """
        Generate human-like keystroke timing for typing text.
        
        Human typing has:
        - Variable inter-key intervals
        - Faster timing for common digraphs
        - Occasional pauses
        """
        result = []
        current_time = 0
        
        # Common fast digraphs (keys typed quickly in succession)
        fast_digraphs = {'th', 'he', 'in', 'er', 'an', 'on', 'en', 'at', 'es', 'ed'}
        
        for i, char in enumerate(text):
            # Base interval (WPM ~ 40-60 for typical user)
            base_interval = self.rng.uniform(80, 200)
            
            # Check for fast digraph
            if i > 0:
                digraph = text[i-1:i+1].lower()
                if digraph in fast_digraphs:
                    base_interval *= 0.6
            
            # Occasional pause (thinking, looking at keyboard)
            if self.rng.random() < 0.05:
                base_interval += self.rng.uniform(200, 500)
            
            result.append((char, current_time))
            current_time += base_interval
        
        return result
    
    def get_config(self) -> dict:
        """
        Export Ghost Motor configuration for browser integration.
        """
        return {
            "enabled": True,
            "seed": self.seed,
            "tremor_hz": self.config.tremor_frequency_hz,
            "tremor_amplitude": self.config.tremor_amplitude_px,
            "overshoot_probability": self.config.overshoot_probability
        }
