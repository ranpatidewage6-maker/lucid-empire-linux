"""
LUCID EMPIRE v5.0-TITAN - Pre-Flight Validator
===============================================
8-point validation matrix for profile integrity checks.
"""

import json
import os
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class ValidationResult:
    """Result of a validation check."""
    name: str
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "severity": self.severity,
        }


class PreFlightValidator:
    """
    8-Point Pre-Flight Validation Matrix.
    
    Validates profile integrity before browser launch:
    1. Profile files exist and are valid
    2. Browser state is consistent
    3. Network configuration is ready
    4. eBPF programs loaded (if required)
    5. Time offset configured
    6. Fingerprint seeds generated
    7. Cookies properly aged
    8. No conflicting profiles active
    """
    
    def __init__(self, profile_path: Path):
        self.profile_path = Path(profile_path)
        self.results: List[ValidationResult] = []
    
    def validate_all(self) -> Tuple[bool, List[ValidationResult]]:
        """
        Run all validation checks.
        
        Returns:
            (all_passed, results)
        """
        self.results = []
        
        # Run all checks
        self._check_profile_files()
        self._check_browser_databases()
        self._check_network_config()
        self._check_ebpf_status()
        self._check_time_offset()
        self._check_fingerprint_seeds()
        self._check_cookie_integrity()
        self._check_no_conflicts()
        
        all_passed = all(r.passed or r.severity != "error" for r in self.results)
        return all_passed, self.results
    
    def _add_result(self, name: str, passed: bool, message: str, severity: str = "error"):
        """Add a validation result."""
        self.results.append(ValidationResult(name, passed, message, severity))
    
    def _check_profile_files(self) -> None:
        """Check 1: Profile files exist and are valid."""
        profile_json = self.profile_path / "profile.json"
        
        if not profile_json.exists():
            self._add_result(
                "Profile Files",
                False,
                f"profile.json not found at {profile_json}",
                "error"
            )
            return
        
        try:
            with open(profile_json) as f:
                data = json.load(f)
            
            # Check required fields
            required = ["profile_id", "profile_name"]
            missing = [f for f in required if f not in data]
            
            if missing:
                self._add_result(
                    "Profile Files",
                    False,
                    f"Missing required fields: {', '.join(missing)}",
                    "error"
                )
            else:
                self._add_result(
                    "Profile Files",
                    True,
                    f"Profile '{data.get('profile_name')}' loaded successfully",
                    "info"
                )
        except json.JSONDecodeError as e:
            self._add_result(
                "Profile Files",
                False,
                f"Invalid JSON in profile.json: {e}",
                "error"
            )
    
    def _check_browser_databases(self) -> None:
        """Check 2: Browser SQLite databases are valid."""
        db_files = ["places.sqlite", "cookies.sqlite"]
        
        for db_name in db_files:
            db_path = self.profile_path / db_name
            
            if not db_path.exists():
                self._add_result(
                    f"Database: {db_name}",
                    False,
                    f"{db_name} not found",
                    "warning"
                )
                continue
            
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) FROM sqlite_master")
                conn.close()
                
                self._add_result(
                    f"Database: {db_name}",
                    True,
                    f"{db_name} is valid",
                    "info"
                )
            except sqlite3.Error as e:
                self._add_result(
                    f"Database: {db_name}",
                    False,
                    f"{db_name} corrupted: {e}",
                    "error"
                )
    
    def _check_network_config(self) -> None:
        """Check 3: Network configuration is ready."""
        network_conf = self.profile_path / "network.conf"
        
        if not network_conf.exists():
            self._add_result(
                "Network Config",
                False,
                "network.conf not found",
                "warning"
            )
            return
        
        try:
            content = network_conf.read_text()
            config = {}
            for line in content.strip().split("\n"):
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
            
            required = ["TTL", "WINDOW_SIZE"]
            missing = [k for k in required if k not in config]
            
            if missing:
                self._add_result(
                    "Network Config",
                    False,
                    f"Missing network params: {', '.join(missing)}",
                    "warning"
                )
            else:
                self._add_result(
                    "Network Config",
                    True,
                    f"Network configured: TTL={config['TTL']}, Window={config['WINDOW_SIZE']}",
                    "info"
                )
        except Exception as e:
            self._add_result(
                "Network Config",
                False,
                f"Failed to read network config: {e}",
                "error"
            )
    
    def _check_ebpf_status(self) -> None:
        """Check 4: eBPF programs loaded."""
        try:
            # Check if bpftool is available and programs are loaded
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Check for XDP programs
            if "xdp" in result.stdout.lower():
                self._add_result(
                    "eBPF Status",
                    True,
                    "XDP program detected on network interface",
                    "info"
                )
            else:
                self._add_result(
                    "eBPF Status",
                    True,
                    "No XDP program loaded (optional for basic operation)",
                    "warning"
                )
        except (subprocess.SubprocessError, FileNotFoundError):
            self._add_result(
                "eBPF Status",
                True,
                "Could not check eBPF status (non-critical)",
                "warning"
            )
    
    def _check_time_offset(self) -> None:
        """Check 5: Time offset configured for profile aging."""
        time_offset_file = self.profile_path / "time_offset"
        
        if not time_offset_file.exists():
            # Check profile.json for aging_days
            profile_json = self.profile_path / "profile.json"
            if profile_json.exists():
                with open(profile_json) as f:
                    data = json.load(f)
                aging_days = data.get("aging_days", 0)
                if aging_days > 0:
                    self._add_result(
                        "Time Offset",
                        True,
                        f"Profile aging: {aging_days} days (offset file will be generated)",
                        "info"
                    )
                else:
                    self._add_result(
                        "Time Offset",
                        True,
                        "No profile aging configured",
                        "warning"
                    )
            else:
                self._add_result(
                    "Time Offset",
                    False,
                    "time_offset not found and no aging_days in profile",
                    "warning"
                )
            return
        
        try:
            offset = time_offset_file.read_text().strip()
            self._add_result(
                "Time Offset",
                True,
                f"Time offset configured: {offset}",
                "info"
            )
        except Exception as e:
            self._add_result(
                "Time Offset",
                False,
                f"Failed to read time offset: {e}",
                "error"
            )
    
    def _check_fingerprint_seeds(self) -> None:
        """Check 6: Fingerprint seeds are generated."""
        profile_json = self.profile_path / "profile.json"
        
        if not profile_json.exists():
            self._add_result(
                "Fingerprint Seeds",
                False,
                "Cannot check seeds - profile.json missing",
                "error"
            )
            return
        
        with open(profile_json) as f:
            data = json.load(f)
        
        seeds = ["canvas_seed", "audio_seed", "webgl_seed"]
        found = [s for s in seeds if data.get(s)]
        missing = [s for s in seeds if not data.get(s)]
        
        if missing:
            self._add_result(
                "Fingerprint Seeds",
                False,
                f"Missing seeds: {', '.join(missing)}",
                "warning"
            )
        else:
            self._add_result(
                "Fingerprint Seeds",
                True,
                f"All fingerprint seeds present ({len(found)}/3)",
                "info"
            )
    
    def _check_cookie_integrity(self) -> None:
        """Check 7: Cookies are properly aged."""
        cookies_db = self.profile_path / "cookies.sqlite"
        
        if not cookies_db.exists():
            self._add_result(
                "Cookie Integrity",
                True,
                "No cookies database (will be created)",
                "warning"
            )
            return
        
        try:
            conn = sqlite3.connect(str(cookies_db))
            cursor = conn.cursor()
            
            # Check for cookies
            cursor.execute("SELECT COUNT(*) FROM moz_cookies")
            count = cursor.fetchone()[0]
            
            if count == 0:
                self._add_result(
                    "Cookie Integrity",
                    True,
                    "No cookies in database",
                    "warning"
                )
            else:
                # Check cookie ages
                cursor.execute("SELECT MIN(creationTime), MAX(creationTime) FROM moz_cookies")
                min_time, max_time = cursor.fetchone()
                
                if min_time and max_time:
                    # Convert from microseconds
                    min_date = datetime.fromtimestamp(min_time / 1000000)
                    max_date = datetime.fromtimestamp(max_time / 1000000)
                    age_days = (datetime.now() - min_date).days
                    
                    self._add_result(
                        "Cookie Integrity",
                        True,
                        f"{count} cookies spanning {age_days} days",
                        "info"
                    )
                else:
                    self._add_result(
                        "Cookie Integrity",
                        True,
                        f"{count} cookies found",
                        "info"
                    )
            
            conn.close()
        except sqlite3.Error as e:
            self._add_result(
                "Cookie Integrity",
                False,
                f"Database error: {e}",
                "error"
            )
    
    def _check_no_conflicts(self) -> None:
        """Check 8: No conflicting profiles are active."""
        # Check for lock files or running Browser instances
        lock_file = self.profile_path / ".parentlock"
        
        if lock_file.exists():
            self._add_result(
                "Profile Conflicts",
                False,
                "Profile appears to be in use (.parentlock exists)",
                "error"
            )
        else:
            self._add_result(
                "Profile Conflicts",
                True,
                "No profile conflicts detected",
                "info"
            )
    
    def get_summary(self) -> Dict[str, any]:
        """Get validation summary."""
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed and r.severity == "error")
        warnings = sum(1 for r in self.results if not r.passed and r.severity == "warning")
        
        return {
            "total_checks": len(self.results),
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "ready": failed == 0,
            "results": [r.to_dict() for r in self.results],
        }
