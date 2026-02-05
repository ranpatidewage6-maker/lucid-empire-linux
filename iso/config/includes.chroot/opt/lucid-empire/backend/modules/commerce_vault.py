"""
LUCID EMPIRE v5.0-TITAN - Commerce Vault
=========================================
Trust token generation and management for e-commerce platforms.
Generates Stripe, PayPal, and Adyen compatible trust artifacts.
"""

import hashlib
import hmac
import json
import secrets
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TrustToken:
    """E-commerce platform trust token."""
    platform: str
    token_id: str
    device_id: str
    created_at: datetime
    last_used: datetime
    usage_count: int = 0
    trust_score: float = 0.8
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "token_id": self.token_id,
            "device_id": self.device_id,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat(),
            "usage_count": self.usage_count,
            "trust_score": self.trust_score,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrustToken":
        return cls(
            platform=data["platform"],
            token_id=data["token_id"],
            device_id=data["device_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_used=datetime.fromisoformat(data["last_used"]),
            usage_count=data.get("usage_count", 0),
            trust_score=data.get("trust_score", 0.8),
            metadata=data.get("metadata", {}),
        )


class CommerceVault:
    """
    Manages e-commerce trust tokens and device fingerprints.
    
    Generates and stores trust artifacts for:
    - Stripe (device fingerprinting, fraud detection bypass)
    - PayPal (FPTI tokens, risk assessment)
    - Adyen (risk scoring, device binding)
    """
    
    # Platform-specific prefixes
    PLATFORM_PREFIXES = {
        "stripe": "pm_",
        "paypal": "PP_",
        "adyen": "AD_",
        "braintree": "BT_",
        "square": "SQ_",
    }
    
    def __init__(self, vault_path: Path, profile_seed: str):
        """
        Initialize commerce vault.
        
        Args:
            vault_path: Path to vault storage directory
            profile_seed: Profile-specific seed for deterministic generation
        """
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.profile_seed = profile_seed
        self.seed_bytes = hashlib.sha256(profile_seed.encode()).digest()
        
        self._tokens: Dict[str, TrustToken] = {}
        self._load_tokens()
    
    def _load_tokens(self) -> None:
        """Load tokens from vault storage."""
        tokens_file = self.vault_path / "tokens.json"
        if tokens_file.exists():
            with open(tokens_file) as f:
                data = json.load(f)
            for token_data in data.get("tokens", []):
                token = TrustToken.from_dict(token_data)
                self._tokens[f"{token.platform}:{token.token_id}"] = token
    
    def _save_tokens(self) -> None:
        """Save tokens to vault storage."""
        tokens_file = self.vault_path / "tokens.json"
        data = {
            "profile_seed": self.profile_seed,
            "tokens": [t.to_dict() for t in self._tokens.values()],
        }
        with open(tokens_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def generate_stripe_token(self, aging_days: int = 90) -> TrustToken:
        """
        Generate Stripe-compatible trust token.
        
        Stripe uses device fingerprinting via stripe.js which collects:
        - Device ID
        - Browser fingerprint
        - Behavioral signals
        """
        # Deterministic device ID from seed
        device_id = hashlib.sha256(f"{self.profile_seed}:stripe:device".encode()).hexdigest()[:32]
        
        # Token ID (payment method style)
        token_id = f"pm_{secrets.token_hex(12)}"
        
        # Calculate creation time based on aging
        created_at = datetime.now() - timedelta(days=aging_days)
        
        # Generate realistic metadata
        metadata = {
            "muid": hashlib.sha256(f"{self.profile_seed}:stripe:muid".encode()).hexdigest()[:24],
            "guid": hashlib.sha256(f"{self.profile_seed}:stripe:guid".encode()).hexdigest()[:24],
            "sid": hashlib.sha256(f"{self.profile_seed}:stripe:sid".encode()).hexdigest()[:24],
            "source": "stripe.js",
            "version": "v3",
        }
        
        token = TrustToken(
            platform="stripe",
            token_id=token_id,
            device_id=device_id,
            created_at=created_at,
            last_used=datetime.now() - timedelta(days=1),
            usage_count=aging_days // 10,  # Simulate periodic usage
            trust_score=min(0.95, 0.7 + (aging_days / 365) * 0.25),  # Higher score with age
            metadata=metadata,
        )
        
        self._tokens[f"stripe:{token_id}"] = token
        self._save_tokens()
        
        return token
    
    def generate_paypal_token(self, aging_days: int = 90) -> TrustToken:
        """
        Generate PayPal-compatible trust token.
        
        PayPal uses FPTI (First Party Tracking Infrastructure) which tracks:
        - Device fingerprint
        - Session history
        - Risk signals
        """
        device_id = hashlib.sha256(f"{self.profile_seed}:paypal:device".encode()).hexdigest()[:32]
        token_id = f"PP_{secrets.token_urlsafe(16)}"
        
        created_at = datetime.now() - timedelta(days=aging_days)
        
        metadata = {
            "fpti_ba": hashlib.sha256(f"{self.profile_seed}:paypal:fpti".encode()).hexdigest()[:32],
            "risk_session": hashlib.sha256(f"{self.profile_seed}:paypal:risk".encode()).hexdigest()[:24],
            "correlation_id": str(uuid.uuid4()),
            "client_id": f"AW{secrets.token_urlsafe(20)}",
        }
        
        token = TrustToken(
            platform="paypal",
            token_id=token_id,
            device_id=device_id,
            created_at=created_at,
            last_used=datetime.now() - timedelta(hours=12),
            usage_count=aging_days // 7,
            trust_score=min(0.92, 0.65 + (aging_days / 365) * 0.27),
            metadata=metadata,
        )
        
        self._tokens[f"paypal:{token_id}"] = token
        self._save_tokens()
        
        return token
    
    def generate_adyen_token(self, aging_days: int = 90) -> TrustToken:
        """
        Generate Adyen-compatible trust token.
        
        Adyen uses Risk Assessment data including:
        - Device fingerprint
        - Shopper reference
        - Risk scoring
        """
        device_id = hashlib.sha256(f"{self.profile_seed}:adyen:device".encode()).hexdigest()[:40]
        token_id = f"AD_{secrets.token_hex(16)}"
        
        created_at = datetime.now() - timedelta(days=aging_days)
        
        # Adyen-specific metadata
        metadata = {
            "shopper_reference": hashlib.sha256(f"{self.profile_seed}:adyen:shopper".encode()).hexdigest()[:16],
            "recurring_detail_reference": secrets.token_hex(16),
            "device_fingerprint": device_id,
            "risk_score": max(0, min(100, 100 - (aging_days // 3))),  # Lower risk with age
        }
        
        token = TrustToken(
            platform="adyen",
            token_id=token_id,
            device_id=device_id,
            created_at=created_at,
            last_used=datetime.now() - timedelta(days=2),
            usage_count=aging_days // 14,
            trust_score=min(0.90, 0.60 + (aging_days / 365) * 0.30),
            metadata=metadata,
        )
        
        self._tokens[f"adyen:{token_id}"] = token
        self._save_tokens()
        
        return token
    
    def get_token(self, platform: str, token_id: Optional[str] = None) -> Optional[TrustToken]:
        """
        Get a trust token.
        
        Args:
            platform: Platform name (stripe, paypal, adyen)
            token_id: Specific token ID, or None for most recent
        """
        if token_id:
            return self._tokens.get(f"{platform}:{token_id}")
        
        # Find most recent for platform
        platform_tokens = [t for k, t in self._tokens.items() if k.startswith(f"{platform}:")]
        if platform_tokens:
            return max(platform_tokens, key=lambda t: t.last_used)
        
        return None
    
    def record_usage(self, platform: str, token_id: str) -> None:
        """Record token usage."""
        key = f"{platform}:{token_id}"
        if key in self._tokens:
            self._tokens[key].last_used = datetime.now()
            self._tokens[key].usage_count += 1
            self._save_tokens()
    
    def get_all_tokens(self) -> List[TrustToken]:
        """Get all tokens."""
        return list(self._tokens.values())
    
    def generate_device_fingerprint(self, platform: str) -> str:
        """
        Generate platform-specific device fingerprint.
        
        Args:
            platform: Target platform
        
        Returns:
            Device fingerprint string
        """
        base = hashlib.sha256(f"{self.profile_seed}:{platform}:fingerprint".encode()).hexdigest()
        
        if platform == "stripe":
            return base[:32]
        elif platform == "paypal":
            return base[:40]
        elif platform == "adyen":
            return f"df_{base[:38]}"
        else:
            return base[:32]
    
    def generate_session_id(self, platform: str) -> str:
        """Generate a session ID for a platform."""
        timestamp = int(time.time() * 1000)
        data = f"{self.profile_seed}:{platform}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:24]
    
    def export_cookies(self, platform: str) -> List[Dict[str, Any]]:
        """
        Export trust-related cookies for a platform.
        
        Returns cookies that would be set by the platform's
        fraud detection systems.
        """
        token = self.get_token(platform)
        if not token:
            return []
        
        cookies = []
        expiry = int((datetime.now() + timedelta(days=365)).timestamp())
        creation = int(token.created_at.timestamp() * 1000000)
        
        if platform == "stripe":
            cookies.extend([
                {
                    "name": "__stripe_mid",
                    "value": token.metadata.get("muid", ""),
                    "domain": ".stripe.com",
                    "path": "/",
                    "expiry": expiry,
                    "creation_time": creation,
                },
                {
                    "name": "__stripe_sid",
                    "value": token.metadata.get("sid", ""),
                    "domain": ".stripe.com",
                    "path": "/",
                    "expiry": expiry,
                    "creation_time": creation,
                },
            ])
        
        elif platform == "paypal":
            cookies.extend([
                {
                    "name": "FPTI",
                    "value": token.metadata.get("fpti_ba", ""),
                    "domain": ".paypal.com",
                    "path": "/",
                    "expiry": expiry,
                    "creation_time": creation,
                },
                {
                    "name": "risk_session",
                    "value": token.metadata.get("risk_session", ""),
                    "domain": ".paypal.com",
                    "path": "/",
                    "expiry": expiry,
                    "creation_time": creation,
                },
            ])
        
        return cookies
