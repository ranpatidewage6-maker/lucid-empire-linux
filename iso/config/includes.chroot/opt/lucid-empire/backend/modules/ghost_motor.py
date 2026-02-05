"""
LUCID EMPIRE v5.0-TITAN - Ghost Motor GAN
==========================================
GAN-based mouse trajectory synthesis implementing:
- Fitts's Law for realistic movement timing
- Micro-tremors and drift simulation
- Natural overshoot and correction patterns
- Per-profile deterministic behavior
"""

import hashlib
import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional, Generator


@dataclass
class MousePoint:
    """A point in a mouse trajectory."""
    x: float
    y: float
    timestamp: float
    velocity: float = 0.0
    acceleration: float = 0.0


class GhostMotorGAN:
    """
    Generates human-like mouse movements using behavioral modeling.
    
    Based on research into human motor control:
    - Fitts's Law: MT = a + b * log2(D/W + 1)
    - Minimum jerk trajectory
    - Micro-tremor injection (8-12 Hz)
    - Natural overshoot patterns
    """
    
    # Fitts's Law parameters (calibrated from human data)
    FITTS_A = 50  # Base time (ms)
    FITTS_B = 150  # Movement time per bit
    
    # Tremor parameters
    TREMOR_FREQUENCY = 10  # Hz
    TREMOR_AMPLITUDE = 1.5  # pixels
    
    # Speed variation
    MIN_SPEED = 0.5
    MAX_SPEED = 2.0
    
    def __init__(self, seed: Optional[str] = None):
        if seed:
            self._seed = int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16)
            random.seed(self._seed)
        else:
            self._seed = None
        
        # Personal characteristics (consistent per seed)
        self.speed_factor = random.uniform(0.8, 1.2)
        self.tremor_intensity = random.uniform(0.5, 1.5)
        self.overshoot_tendency = random.uniform(0.1, 0.3)
        self.pause_probability = random.uniform(0.02, 0.08)
    
    def generate_trajectory(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        target_width: float = 20.0
    ) -> List[MousePoint]:
        """
        Generate a human-like mouse trajectory between two points.
        
        Args:
            start: Starting (x, y) coordinates
            end: Ending (x, y) coordinates
            target_width: Width of the target (affects precision)
        
        Returns:
            List of MousePoint objects forming the trajectory
        """
        sx, sy = start
        ex, ey = end
        
        # Calculate distance
        distance = math.sqrt((ex - sx) ** 2 + (ey - sy) ** 2)
        
        if distance < 1:
            return [MousePoint(ex, ey, time.time())]
        
        # Fitts's Law: calculate movement time
        movement_time = self._fitts_time(distance, target_width)
        movement_time *= self.speed_factor
        
        # Number of points based on movement time (60 FPS)
        num_points = max(int(movement_time / 16.67), 5)
        
        trajectory = []
        start_time = time.time()
        
        # Add overshoot if tendency triggers
        if random.random() < self.overshoot_tendency:
            # Calculate overshoot point
            overshoot_dist = distance * random.uniform(0.02, 0.08)
            angle = math.atan2(ey - sy, ex - sx)
            overshoot_x = ex + overshoot_dist * math.cos(angle)
            overshoot_y = ey + overshoot_dist * math.sin(angle)
            
            # Generate to overshoot, then correction
            main_trajectory = self._minimum_jerk_trajectory(
                sx, sy, overshoot_x, overshoot_y, int(num_points * 0.85), start_time
            )
            correction = self._minimum_jerk_trajectory(
                overshoot_x, overshoot_y, ex, ey, int(num_points * 0.15),
                main_trajectory[-1].timestamp if main_trajectory else start_time
            )
            trajectory = main_trajectory + correction
        else:
            trajectory = self._minimum_jerk_trajectory(sx, sy, ex, ey, num_points, start_time)
        
        # Add micro-tremors
        trajectory = self._add_tremors(trajectory)
        
        # Add occasional micro-pauses
        trajectory = self._add_pauses(trajectory)
        
        return trajectory
    
    def _fitts_time(self, distance: float, width: float) -> float:
        """Calculate movement time using Fitts's Law."""
        index_of_difficulty = math.log2(distance / width + 1)
        return self.FITTS_A + self.FITTS_B * index_of_difficulty
    
    def _minimum_jerk_trajectory(
        self,
        sx: float, sy: float,
        ex: float, ey: float,
        num_points: int,
        start_time: float
    ) -> List[MousePoint]:
        """
        Generate minimum jerk trajectory (smoothest possible movement).
        
        Based on Flash & Hogan (1985) minimum jerk model.
        """
        trajectory = []
        duration = num_points * 16.67 / 1000  # Convert to seconds
        
        for i in range(num_points):
            t = i / (num_points - 1) if num_points > 1 else 1
            
            # Minimum jerk position formula
            # x(t) = x0 + (x1 - x0) * (10t³ - 15t⁴ + 6t⁵)
            tau = 10 * t**3 - 15 * t**4 + 6 * t**5
            
            x = sx + (ex - sx) * tau
            y = sy + (ey - sy) * tau
            
            # Add slight randomness (motor noise)
            noise = random.gauss(0, 0.5)
            x += noise
            y += noise
            
            timestamp = start_time + (i * 16.67 / 1000)
            
            # Calculate velocity
            if i > 0:
                prev = trajectory[-1]
                dt = timestamp - prev.timestamp
                if dt > 0:
                    velocity = math.sqrt((x - prev.x)**2 + (y - prev.y)**2) / dt
                else:
                    velocity = 0
            else:
                velocity = 0
            
            trajectory.append(MousePoint(x, y, timestamp, velocity))
        
        return trajectory
    
    def _add_tremors(self, trajectory: List[MousePoint]) -> List[MousePoint]:
        """Add physiological tremor to trajectory."""
        if not trajectory:
            return trajectory
        
        for i, point in enumerate(trajectory):
            # 8-12 Hz tremor
            phase = i * (2 * math.pi * self.TREMOR_FREQUENCY / 60)
            tremor_x = self.TREMOR_AMPLITUDE * self.tremor_intensity * math.sin(phase + random.uniform(0, 0.5))
            tremor_y = self.TREMOR_AMPLITUDE * self.tremor_intensity * math.cos(phase + random.uniform(0, 0.5))
            
            point.x += tremor_x
            point.y += tremor_y
        
        return trajectory
    
    def _add_pauses(self, trajectory: List[MousePoint]) -> List[MousePoint]:
        """Add micro-pauses during movement."""
        if len(trajectory) < 10:
            return trajectory
        
        result = []
        for i, point in enumerate(trajectory):
            result.append(point)
            
            # Add micro-pause at random points
            if random.random() < self.pause_probability and 0.2 < i / len(trajectory) < 0.8:
                pause_duration = random.uniform(0.01, 0.05)
                pause_point = MousePoint(
                    point.x + random.gauss(0, 0.2),
                    point.y + random.gauss(0, 0.2),
                    point.timestamp + pause_duration,
                    0
                )
                result.append(pause_point)
        
        return result
    
    def generate_click_timing(self) -> Tuple[float, float]:
        """
        Generate realistic click down/up timing.
        
        Returns:
            (down_duration, inter_click_delay)
        """
        # Click duration: typically 80-150ms
        down_duration = random.gauss(100, 20) / 1000
        down_duration = max(0.05, min(0.2, down_duration))
        
        # Double-click delay (if applicable): 100-300ms
        inter_click = random.gauss(180, 40) / 1000
        
        return down_duration, inter_click
    
    def generate_scroll_pattern(
        self,
        distance: int,
        direction: str = "down"
    ) -> Generator[Tuple[int, float], None, None]:
        """
        Generate realistic scroll pattern.
        
        Args:
            distance: Total scroll distance in pixels
            direction: "up" or "down"
        
        Yields:
            (scroll_delta, delay) tuples
        """
        remaining = abs(distance)
        sign = -1 if direction == "up" else 1
        
        while remaining > 0:
            # Variable scroll amount (typically 100-200 pixels per event)
            scroll_amount = min(remaining, random.randint(80, 160))
            remaining -= scroll_amount
            
            # Variable delay between scrolls
            delay = random.uniform(0.02, 0.08)
            
            yield (sign * scroll_amount, delay)
            
            # Occasional pause
            if random.random() < 0.1:
                yield (0, random.uniform(0.1, 0.3))
    
    def generate_typing_pattern(
        self,
        text: str,
        wpm: float = 60.0
    ) -> Generator[Tuple[str, float], None, None]:
        """
        Generate realistic typing pattern.
        
        Args:
            text: Text to type
            wpm: Words per minute (average)
        
        Yields:
            (character, delay_before) tuples
        """
        # Base delay per character (adjusted for WPM)
        base_delay = 60.0 / (wpm * 5)  # 5 characters per word average
        
        prev_char = None
        for char in text:
            # Adjust delay based on character type
            delay = base_delay * random.uniform(0.7, 1.3)
            
            # Longer delay after punctuation
            if prev_char in ".!?":
                delay *= random.uniform(2.0, 4.0)
            elif prev_char == " ":
                delay *= random.uniform(0.8, 1.0)
            
            # Occasional typo hesitation
            if random.random() < 0.02:
                delay *= random.uniform(2.0, 3.0)
            
            yield (char, delay)
            prev_char = char
