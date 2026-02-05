# =============================================================================
# LUCID EMPIRE v5.0-TITAN :: Commerce Vault
# =============================================================================
# Trust token generation for payment gateways (Stripe, Adyen, PayPal).
# Creates aged device identifiers that establish commerce reputation.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# Source: Technical Documentation [cite: 1, 8]
# =============================================================================

import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List


@dataclass
class StripeTokens:
    """Stripe commerce trust tokens."""
    machine_id: str      # __stripe_mid
    session_id: str      # __stripe_sid
    device_hash: str
    creation_time: int   # Unix timestamp (ms)


@dataclass
class AdyenTokens:
    """Adyen RevenueProtect tokens."""
    rp_uid: str          # _RP_UID
    risk_device_id: str  # risk_device_id
    df_value: str        # dfValue
    creation_time: int


@dataclass
class PayPalTokens:
    """PayPal commerce tokens."""
    akdc: str            # AKDC cookie
    ts_c: str            # Timestamp cookie
    creation_time: int


class CommerceVault:
    """
    Commerce trust token generator for payment gateway reputation.
    
    Generates aged, deterministic tokens for:
    - Stripe Radar (__stripe_mid, __stripe_sid)
    - Adyen RevenueProtect (_RP_UID, risk_device_id, dfValue)
    - PayPal (AKDC)
    
    Tokens are derived from profile UUID for consistency across sessions.
    
    Source: Technical Documentation [cite: 1, 8]
    """
    
    def __init__(
        self,
        profile_uuid: str,
        seed: int,
        age_days: int = 90
    ):
        """
        Initialize Commerce Vault.
        
        Args:
            profile_uuid: Profile UUID for deterministic token generation
            seed: Random seed for additional entropy
            age_days: Token age in days (for backdating)
        """
        self.profile_uuid = profile_uuid
        self.seed = seed
        self.age_days = age_days
        
        # Calculate creation timestamp (backdated)
        self.creation_date = datetime.now() - timedelta(days=age_days)
        self.creation_timestamp_ms = int(self.creation_date.timestamp() * 1000)
        self.creation_timestamp_s = int(self.creation_date.timestamp())
        
        # Generate device hash (consistent for this profile)
        self.device_hash = self._generate_device_hash()
        
        # Pre-generate all tokens
        self._stripe_tokens = self._generate_stripe_tokens()
        self._adyen_tokens = self._generate_adyen_tokens()
        self._paypal_tokens = self._generate_paypal_tokens()
    
    def _hash(self, data: str) -> str:
        """Generate SHA-256 hash."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _generate_device_hash(self) -> str:
        """
        Generate consistent device fingerprint hash.
        
        This hash represents the "device identity" and should be
        consistent across all commerce platforms.
        """
        return self._hash(f"{self.profile_uuid}:device:{self.seed}")[:32]
    
    def _generate_stripe_tokens(self) -> StripeTokens:
        """
        Generate Stripe Radar trust tokens.
        
        Stripe uses:
        - __stripe_mid: Machine ID (persistent device fingerprint)
        - __stripe_sid: Session ID (per-session identifier)
        
        Format: v3|timestamp_ms|device_hash_segment
        
        Source: Technical Documentation [cite: 8.1]
        """
        # Machine ID format: v3|creation_timestamp|hash_segment
        machine_id = f"v3|{self.creation_timestamp_ms}|{self.device_hash[:16]}"
        
        # Session ID format: hash_segment_current_timestamp
        session_id = f"{self.device_hash[16:32]}_{int(time.time() * 1000)}"
        
        return StripeTokens(
            machine_id=machine_id,
            session_id=session_id,
            device_hash=self.device_hash,
            creation_time=self.creation_timestamp_ms
        )
    
    def _generate_adyen_tokens(self) -> AdyenTokens:
        """
        Generate Adyen RevenueProtect tokens.
        
        Adyen uses:
        - _RP_UID: Risk Prevention User ID
        - risk_device_id: Device identifier
        - dfValue: Device fingerprint value
        
        Source: Technical Documentation [cite: 8.1]
        """
        # Generate Adyen-specific hashes
        adyen_hash = self._hash(f"{self.profile_uuid}:adyen:{self.seed}")
        
        rp_uid = f"adyen_{adyen_hash[:24]}"
        risk_device_id = f"d_{adyen_hash[24:44]}"
        df_value = self._hash(f"{self.profile_uuid}:adyen_df:{self.seed}")[:40]
        
        return AdyenTokens(
            rp_uid=rp_uid,
            risk_device_id=risk_device_id,
            df_value=df_value,
            creation_time=self.creation_timestamp_ms
        )
    
    def _generate_paypal_tokens(self) -> PayPalTokens:
        """
        Generate PayPal commerce tokens.
        
        PayPal uses:
        - AKDC: Account Key Device Cookie
        - ts_c: Timestamp cookie
        
        Source: Technical Documentation [cite: 8.1]
        """
        paypal_hash = self._hash(f"{self.profile_uuid}:paypal:{self.seed}")
        
        akdc = f"akdc_{paypal_hash[:16]}_{self.creation_timestamp_ms}"
        ts_c = str(self.creation_timestamp_ms)
        
        return PayPalTokens(
            akdc=akdc,
            ts_c=ts_c,
            creation_time=self.creation_timestamp_ms
        )
    
    def get_tokens(self, platform: str = "all") -> Dict[str, Any]:
        """
        Get commerce tokens for specified platform(s).
        
        Args:
            platform: Platform name (stripe, adyen, paypal, all)
            
        Returns:
            Dict containing requested tokens
        """
        result = {}
        
        if platform in ("stripe", "all"):
            result["stripe"] = {
                "__stripe_mid": self._stripe_tokens.machine_id,
                "__stripe_sid": self._stripe_tokens.session_id,
                "device_hash": self._stripe_tokens.device_hash,
                "creation_time": self._stripe_tokens.creation_time
            }
        
        if platform in ("adyen", "all"):
            result["adyen"] = {
                "_RP_UID": self._adyen_tokens.rp_uid,
                "risk_device_id": self._adyen_tokens.risk_device_id,
                "dfValue": self._adyen_tokens.df_value,
                "creation_time": self._adyen_tokens.creation_time
            }
        
        if platform in ("paypal", "all"):
            result["paypal"] = {
                "AKDC": self._paypal_tokens.akdc,
                "ts_c": self._paypal_tokens.ts_c,
                "creation_time": self._paypal_tokens.creation_time
            }
        
        return result
    
    def get_cookies(self, platform: str = "all") -> List[Dict[str, Any]]:
        """
        Get tokens formatted as browser cookies.
        
        Args:
            platform: Platform name (stripe, adyen, paypal, all)
            
        Returns:
            List of cookie dictionaries ready for injection
        """
        cookies = []
        now_timestamp = int(time.time())
        expiry = now_timestamp + (365 * 24 * 3600)  # 1 year expiry
        
        if platform in ("stripe", "all"):
            cookies.append({
                "name": "__stripe_mid",
                "value": self._stripe_tokens.machine_id,
                "host": ".stripe.com",
                "path": "/",
                "expiry": expiry,
                "creation_time_prtime": self._stripe_tokens.creation_time * 1000,
                "secure": True,
                "http_only": False,
                "same_site": 0
            })
            cookies.append({
                "name": "__stripe_sid",
                "value": self._stripe_tokens.session_id,
                "host": ".stripe.com",
                "path": "/",
                "expiry": now_timestamp + (30 * 60),  # 30 min session
                "creation_time_prtime": int(time.time() * 1_000_000),
                "secure": True,
                "http_only": False,
                "same_site": 0
            })
        
        if platform in ("paypal", "all"):
            cookies.append({
                "name": "AKDC",
                "value": self._paypal_tokens.akdc,
                "host": ".paypal.com",
                "path": "/",
                "expiry": expiry,
                "creation_time_prtime": self._paypal_tokens.creation_time * 1000,
                "secure": True,
                "http_only": True,
                "same_site": 1
            })
            cookies.append({
                "name": "ts_c",
                "value": self._paypal_tokens.ts_c,
                "host": ".paypal.com",
                "path": "/",
                "expiry": expiry,
                "creation_time_prtime": self._paypal_tokens.creation_time * 1000,
                "secure": True,
                "http_only": False,
                "same_site": 0
            })
        
        return cookies
    
    def get_local_storage(self, platform: str = "all") -> List[Dict[str, Any]]:
        """
        Get tokens formatted for localStorage injection.
        
        Args:
            platform: Platform name (stripe, adyen, paypal, all)
            
        Returns:
            List of localStorage entries ready for LSNG injection
        """
        entries = []
        
        if platform in ("stripe", "all"):
            entries.append({
                "origin": "https://stripe.com",
                "key": "__stripe_mid",
                "value": self._stripe_tokens.machine_id
            })
            entries.append({
                "origin": "https://js.stripe.com",
                "key": "__stripe_mid",
                "value": self._stripe_tokens.machine_id
            })
        
        if platform in ("adyen", "all"):
            entries.append({
                "origin": "https://adyen.com",
                "key": "risk_device_id",
                "value": self._adyen_tokens.risk_device_id
            })
            entries.append({
                "origin": "https://adyen.com",
                "key": "dfValue",
                "value": self._adyen_tokens.df_value
            })
            entries.append({
                "origin": "https://checkoutshopper-live.adyen.com",
                "key": "adyen-checkout-device_id",
                "value": self._adyen_tokens.risk_device_id
            })
        
        return entries
    
    def export(self) -> Dict[str, Any]:
        """
        Export complete vault data for storage.
        """
        return {
            "profile_uuid": self.profile_uuid,
            "age_days": self.age_days,
            "creation_date": self.creation_date.isoformat(),
            "device_hash": self.device_hash,
            "tokens": self.get_tokens("all"),
            "cookies": self.get_cookies("all"),
            "local_storage": self.get_local_storage("all")
        }
    
    def get_trust_score_factors(self) -> Dict[str, Any]:
        """
        Get factors that contribute to commerce trust score.
        
        These are the signals that fraud detection systems look for.
        """
        return {
            "device_age_days": self.age_days,
            "has_stripe_mid": True,
            "has_adyen_rp": True,
            "has_paypal_akdc": True,
            "consistent_device_hash": True,
            "token_timestamps_valid": True,
            "estimated_trust_level": "HIGH" if self.age_days >= 90 else "MEDIUM"
        }
