# =============================================================================
# LUCID EMPIRE v5.0-TITAN :: Genesis Engine
# =============================================================================
# Profile fabrication and identity synthesis engine.
# Generates 90-day aged browser profiles with temporal displacement.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# Source: Technical Documentation [cite: 1, 3]
# =============================================================================

import hashlib
import json
import random
import uuid
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import sqlite3


@dataclass
class IdentityCore:
    """
    Core identity information for a synthesized persona.
    Used for form autofill and behavioral pattern generation.
    """
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    zip_code: str
    email: str
    phone: str
    dob: str = ""


@dataclass
class ProxyConfig:
    """
    Network tunnel configuration.
    """
    protocol: str  # socks5, http, https
    host: str
    port: int
    username: str = ""
    password: str = ""
    
    @property
    def full_string(self) -> str:
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"


@dataclass 
class CommerceTrustAnchor:
    """
    Commerce trust anchor data (hashed, never stored in plaintext).
    """
    pan_hash: str  # SHA-256 hash of PAN
    exp_month: int
    exp_year: int
    name: str
    last_four: str


class GenesisEngine:
    """
    Central orchestrator for identity synthesis and profile fabrication.
    
    The Genesis Engine coordinates:
    - UUID generation and deterministic seeding
    - Temporal displacement (90-day aging)
    - Browsing history generation (3-phase aging)
    - Commerce trust anchor creation
    - Profile artifact generation
    
    Source: Technical Documentation [cite: 1, 3]
    """
    
    VERSION = "5.0.0-TITAN"
    
    # Persona-specific browsing patterns
    PERSONA_SITES = {
        "shopper": {
            "trust_anchors": [
                "https://www.google.com",
                "https://www.facebook.com",
                "https://www.microsoft.com",
                "https://www.linkedin.com"
            ],
            "warming": [
                "https://www.amazon.com",
                "https://www.ebay.com",
                "https://www.walmart.com",
                "https://www.target.com",
                "https://www.bestbuy.com",
                "https://www.costco.com",
                "https://www.homedepot.com"
            ],
            "general": [
                "https://www.youtube.com",
                "https://www.reddit.com",
                "https://www.twitter.com",
                "https://www.instagram.com",
                "https://news.ycombinator.com"
            ]
        },
        "developer": {
            "trust_anchors": [
                "https://www.google.com",
                "https://github.com",
                "https://stackoverflow.com",
                "https://www.linkedin.com"
            ],
            "warming": [
                "https://www.npmjs.com",
                "https://pypi.org",
                "https://docs.python.org",
                "https://developer.mozilla.org",
                "https://aws.amazon.com",
                "https://cloud.google.com"
            ],
            "general": [
                "https://www.youtube.com",
                "https://www.reddit.com",
                "https://news.ycombinator.com",
                "https://dev.to",
                "https://medium.com"
            ]
        },
        "professional": {
            "trust_anchors": [
                "https://www.google.com",
                "https://www.microsoft.com",
                "https://www.linkedin.com",
                "https://outlook.office.com"
            ],
            "warming": [
                "https://www.salesforce.com",
                "https://slack.com",
                "https://www.bloomberg.com",
                "https://www.wsj.com",
                "https://www.forbes.com"
            ],
            "general": [
                "https://www.youtube.com",
                "https://www.nytimes.com",
                "https://www.cnn.com",
                "https://www.bbc.com"
            ]
        },
        "gamer": {
            "trust_anchors": [
                "https://www.google.com",
                "https://www.twitch.tv",
                "https://discord.com",
                "https://store.steampowered.com"
            ],
            "warming": [
                "https://www.epicgames.com",
                "https://www.ea.com",
                "https://www.playstation.com",
                "https://www.xbox.com",
                "https://www.nvidia.com"
            ],
            "general": [
                "https://www.youtube.com",
                "https://www.reddit.com",
                "https://www.twitter.com",
                "https://www.ign.com"
            ]
        }
    }
    
    # Visit type distribution (natural browsing patterns)
    VISIT_TYPE_WEIGHTS = {
        1: 0.65,  # TRANSITION_LINK (65%)
        2: 0.20,  # TRANSITION_TYPED (20%)
        3: 0.05,  # TRANSITION_BOOKMARK (5%)
        4: 0.05,  # TRANSITION_EMBED (5%)
        5: 0.05   # TRANSITION_REDIRECT_PERMANENT (5%)
    }
    
    def __init__(self, profile_dir: Optional[Path] = None):
        self.profile_dir = profile_dir or Path("./lucid_profile_data")
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.current_profile = None
        self.rng = None
        
    def _init_rng(self, seed: int):
        """Initialize the random number generator with profile seed."""
        self.rng = random.Random(seed)
    
    def _derive_seed(self, profile_uuid: str, purpose: str) -> int:
        """Derive a deterministic seed for a specific purpose."""
        combined = f"{profile_uuid}:{purpose}"
        hash_bytes = hashlib.sha256(combined.encode()).digest()
        return int.from_bytes(hash_bytes[:8], 'little')
    
    def _to_prtime(self, dt: datetime) -> int:
        """Convert datetime to PRTime (microseconds since Unix epoch)."""
        return int(dt.timestamp() * 1_000_000)
    
    def _generate_visit_type(self) -> int:
        """Generate a visit type based on natural distribution."""
        rand = self.rng.random()
        cumulative = 0
        for visit_type, weight in self.VISIT_TYPE_WEIGHTS.items():
            cumulative += weight
            if rand <= cumulative:
                return visit_type
        return 1  # Default to TRANSITION_LINK
    
    def create_profile(
        self,
        profile_name: str,
        persona: str = "shopper",
        age_days: int = 90,
        identity: Optional[IdentityCore] = None,
        proxy: Optional[ProxyConfig] = None,
        trust_anchor: Optional[CommerceTrustAnchor] = None,
        target_site: Optional[str] = None,
        timezone: str = "America/New_York"
    ) -> Dict[str, Any]:
        """
        Create a new synthesized profile with full temporal displacement.
        
        The fabrication process follows three phases:
        - Phase 1 (Inception): T-90 to T-60 days - Trust anchor establishment
        - Phase 2 (Warming): T-60 to T-30 days - Persona-specific browsing
        - Phase 3 (Kill Chain): T-30 to T-0 days - Target site engagement
        
        Args:
            profile_name: Unique profile identifier
            persona: Browsing persona (shopper, developer, professional, gamer)
            age_days: Profile age in days
            identity: Optional identity information for form autofill
            proxy: Optional proxy configuration
            trust_anchor: Optional commerce trust anchor
            target_site: Optional target site for kill chain phase
            timezone: Target timezone
            
        Returns:
            Dict containing complete profile configuration
        """
        print(f"[Genesis] Creating profile: {profile_name}")
        print(f"[Genesis] Persona: {persona}, Age: {age_days} days")
        
        # Generate unique profile UUID
        profile_uuid = str(uuid.uuid4())
        seed = self._derive_seed(profile_uuid, "genesis")
        self._init_rng(seed)
        
        # Calculate timeline
        now = datetime.now()
        start_date = now - timedelta(days=age_days)
        
        # Create profile directory
        profile_path = self.profile_dir / profile_name
        profile_path.mkdir(parents=True, exist_ok=True)
        
        # Generate profile metadata
        metadata = {
            "profile_uuid": profile_uuid,
            "profile_name": profile_name,
            "persona": persona,
            "age_days": age_days,
            "start_date": start_date.isoformat(),
            "created_at": now.isoformat(),
            "timezone": timezone,
            "libfaketime_offset": f"-{age_days}d",
            "seeds": {
                "genesis": seed,
                "canvas": self._derive_seed(profile_uuid, "canvas"),
                "webgl": self._derive_seed(profile_uuid, "webgl"),
                "audio": self._derive_seed(profile_uuid, "audio"),
                "ghost_motor": self._derive_seed(profile_uuid, "ghost_motor"),
                "commerce": self._derive_seed(profile_uuid, "commerce")
            }
        }
        
        # Add identity if provided
        if identity:
            metadata["identity"] = {
                "first_name": identity.first_name,
                "last_name": identity.last_name,
                "address": identity.address,
                "city": identity.city,
                "state": identity.state,
                "zip_code": identity.zip_code,
                "email": identity.email,
                "phone": identity.phone,
                "dob": identity.dob
            }
        
        # Add proxy configuration if provided
        if proxy:
            metadata["proxy"] = {
                "protocol": proxy.protocol,
                "host": proxy.host,
                "port": proxy.port,
                "full_string": proxy.full_string
            }
        
        # Generate browsing history artifacts
        print("[Genesis] Generating browsing history...")
        history = self._generate_browsing_history(
            persona=persona,
            start_date=start_date,
            end_date=now,
            target_site=target_site
        )
        
        # Generate cookies artifacts
        print("[Genesis] Generating cookie history...")
        cookies = self._generate_cookies(
            persona=persona,
            start_date=start_date,
            end_date=now,
            profile_uuid=profile_uuid
        )
        
        # Generate commerce vault tokens
        print("[Genesis] Generating commerce vault tokens...")
        commerce_vault = self._generate_commerce_vault(
            profile_uuid=profile_uuid,
            start_date=start_date,
            trust_anchor=trust_anchor
        )
        
        # Generate form history
        print("[Genesis] Generating form history...")
        form_history = self._generate_form_history(identity) if identity else []
        
        # Generate times.json (Firefox profile age marker)
        times_data = {
            "created": self._to_prtime(start_date),
            "firstUse": self._to_prtime(start_date + timedelta(minutes=5))
        }
        
        # Save all artifacts
        self._save_artifact(profile_path, "metadata.json", metadata)
        self._save_artifact(profile_path, "browsing_history.json", history)
        self._save_artifact(profile_path, "commerce_cookies.json", cookies)
        self._save_artifact(profile_path, "commerce_vault.json", commerce_vault)
        self._save_artifact(profile_path, "form_history.json", form_history)
        self._save_artifact(profile_path, "times.json", times_data)
        
        print(f"[Genesis] Profile artifacts saved to: {profile_path}")
        print(f"[Genesis] Generated {len(history)} history entries")
        print(f"[Genesis] Generated {len(cookies)} cookies")
        
        self.current_profile = metadata
        return metadata
    
    def _generate_browsing_history(
        self,
        persona: str,
        start_date: datetime,
        end_date: datetime,
        target_site: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate browsing history following the 3-phase aging protocol.
        
        Phase 1 (Inception): Trust anchor establishment
        Phase 2 (Warming): Persona-specific browsing
        Phase 3 (Kill Chain): Target engagement
        """
        history = []
        sites = self.PERSONA_SITES.get(persona, self.PERSONA_SITES["shopper"])
        
        total_days = (end_date - start_date).days
        phase1_end = start_date + timedelta(days=total_days * 0.33)
        phase2_end = start_date + timedelta(days=total_days * 0.66)
        
        # Phase 1: Inception (T-90 to T-60) - Trust anchors
        current_date = start_date
        while current_date < phase1_end:
            # Generate 2-5 visits per day
            visits_today = self.rng.randint(2, 5)
            for _ in range(visits_today):
                site = self.rng.choice(sites["trust_anchors"])
                visit_time = current_date + timedelta(
                    hours=self.rng.randint(8, 22),
                    minutes=self.rng.randint(0, 59)
                )
                history.append({
                    "url": site,
                    "title": self._get_site_title(site),
                    "visit_time": visit_time.isoformat(),
                    "visit_time_prtime": self._to_prtime(visit_time),
                    "visit_type": self._generate_visit_type(),
                    "phase": "inception"
                })
            current_date += timedelta(days=1)
        
        # Phase 2: Warming (T-60 to T-30) - Persona-specific
        while current_date < phase2_end:
            visits_today = self.rng.randint(5, 15)
            all_sites = sites["trust_anchors"] + sites["warming"] + sites["general"]
            for _ in range(visits_today):
                site = self.rng.choice(all_sites)
                visit_time = current_date + timedelta(
                    hours=self.rng.randint(6, 23),
                    minutes=self.rng.randint(0, 59)
                )
                history.append({
                    "url": site,
                    "title": self._get_site_title(site),
                    "visit_time": visit_time.isoformat(),
                    "visit_time_prtime": self._to_prtime(visit_time),
                    "visit_type": self._generate_visit_type(),
                    "phase": "warming"
                })
            current_date += timedelta(days=1)
        
        # Phase 3: Kill Chain (T-30 to T-0) - Target engagement
        while current_date < end_date:
            visits_today = self.rng.randint(8, 20)
            all_sites = sites["warming"] + sites["general"]
            if target_site:
                # Add target site with higher frequency
                all_sites = all_sites + [target_site] * 3
            
            for _ in range(visits_today):
                site = self.rng.choice(all_sites)
                visit_time = current_date + timedelta(
                    hours=self.rng.randint(6, 23),
                    minutes=self.rng.randint(0, 59)
                )
                history.append({
                    "url": site,
                    "title": self._get_site_title(site),
                    "visit_time": visit_time.isoformat(),
                    "visit_time_prtime": self._to_prtime(visit_time),
                    "visit_type": self._generate_visit_type(),
                    "phase": "kill_chain"
                })
            current_date += timedelta(days=1)
        
        # Sort by visit time
        history.sort(key=lambda x: x["visit_time_prtime"])
        return history
    
    def _generate_cookies(
        self,
        persona: str,
        start_date: datetime,
        end_date: datetime,
        profile_uuid: str
    ) -> List[Dict[str, Any]]:
        """
        Generate aged cookies for trust establishment.
        """
        cookies = []
        sites = self.PERSONA_SITES.get(persona, self.PERSONA_SITES["shopper"])
        
        # Trust anchor cookies
        for site in sites["trust_anchors"]:
            domain = site.replace("https://", "").replace("www.", "").split("/")[0]
            cookie_time = start_date + timedelta(
                days=self.rng.randint(0, 5),
                hours=self.rng.randint(8, 22)
            )
            
            # Generate standard tracking cookies
            cookies.append({
                "name": "_ga",
                "value": f"GA1.2.{self.rng.randint(1000000000, 9999999999)}.{int(cookie_time.timestamp())}",
                "host": f".{domain}",
                "path": "/",
                "creation_time_prtime": self._to_prtime(cookie_time),
                "expiry": int((cookie_time + timedelta(days=730)).timestamp()),
                "secure": True,
                "http_only": False,
                "same_site": 0
            })
            
            cookies.append({
                "name": "_gid",
                "value": f"GA1.2.{self.rng.randint(1000000000, 9999999999)}",
                "host": f".{domain}",
                "path": "/",
                "creation_time_prtime": self._to_prtime(cookie_time),
                "expiry": int((cookie_time + timedelta(days=1)).timestamp()),
                "secure": True,
                "http_only": False,
                "same_site": 0
            })
        
        return cookies
    
    def _generate_commerce_vault(
        self,
        profile_uuid: str,
        start_date: datetime,
        trust_anchor: Optional[CommerceTrustAnchor] = None
    ) -> Dict[str, Any]:
        """
        Generate commerce trust tokens for payment gateways.
        
        Includes tokens for:
        - Stripe (__stripe_mid, __stripe_sid)
        - Adyen (_RP_UID, risk_device_id)
        - PayPal (AKDC)
        """
        commerce_seed = self._derive_seed(profile_uuid, "commerce")
        creation_time = int(start_date.timestamp() * 1000)
        
        # Generate deterministic device IDs
        device_hash = hashlib.sha256(f"{profile_uuid}:device".encode()).hexdigest()[:32]
        
        vault = {
            "stripe": {
                "__stripe_mid": f"v3|{creation_time}|{device_hash[:16]}",
                "__stripe_sid": f"{device_hash[16:32]}_{int(datetime.now().timestamp() * 1000)}",
                "creation_time": creation_time,
                "device_hash": device_hash
            },
            "adyen": {
                "_RP_UID": f"adyen_{device_hash[:24]}",
                "risk_device_id": f"d_{device_hash[:20]}",
                "dfValue": hashlib.sha256(f"{profile_uuid}:adyen_df".encode()).hexdigest()[:40],
                "creation_time": creation_time
            },
            "paypal": {
                "AKDC": f"akdc_{device_hash[:16]}_{creation_time}",
                "ts_c": str(creation_time),
                "creation_time": creation_time
            }
        }
        
        # Add trust anchor metadata if provided
        if trust_anchor:
            vault["trust_anchor"] = {
                "pan_hash": trust_anchor.pan_hash,
                "last_four": trust_anchor.last_four,
                "exp": f"{trust_anchor.exp_month:02d}/{trust_anchor.exp_year}",
                "name": trust_anchor.name
            }
        
        return vault
    
    def _generate_form_history(self, identity: IdentityCore) -> List[Dict[str, Any]]:
        """
        Generate form autofill history based on identity.
        """
        return [
            {"fieldname": "first-name", "value": identity.first_name, "times_used": 5},
            {"fieldname": "last-name", "value": identity.last_name, "times_used": 5},
            {"fieldname": "email", "value": identity.email, "times_used": 8},
            {"fieldname": "tel", "value": identity.phone, "times_used": 3},
            {"fieldname": "address-line1", "value": identity.address, "times_used": 3},
            {"fieldname": "address-city", "value": identity.city, "times_used": 3},
            {"fieldname": "address-state", "value": identity.state, "times_used": 3},
            {"fieldname": "postal-code", "value": identity.zip_code, "times_used": 3}
        ]
    
    def _get_site_title(self, url: str) -> str:
        """Get a realistic page title for a URL."""
        titles = {
            "google.com": "Google",
            "facebook.com": "Facebook",
            "microsoft.com": "Microsoft – Cloud, Computers, Apps & Gaming",
            "linkedin.com": "LinkedIn",
            "amazon.com": "Amazon.com: Online Shopping",
            "ebay.com": "Electronics, Cars, Fashion | eBay",
            "youtube.com": "YouTube",
            "github.com": "GitHub",
            "stackoverflow.com": "Stack Overflow",
            "twitch.tv": "Twitch",
            "discord.com": "Discord"
        }
        
        for domain, title in titles.items():
            if domain in url:
                return title
        return "Website"
    
    def _save_artifact(self, profile_path: Path, filename: str, data: Any):
        """Save a profile artifact to disk."""
        filepath = profile_path / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def hash_pan(pan: str) -> str:
    """
    Hash a PAN (card number) for secure storage.
    Never store PANs in plaintext.
    """
    return hashlib.sha256(pan.encode()).hexdigest()


def create_trust_anchor(pan: str, exp: str, name: str) -> CommerceTrustAnchor:
    """
    Create a commerce trust anchor from card data.
    
    Args:
        pan: Card number (will be hashed)
        exp: Expiration in MM/YY format
        name: Cardholder name
        
    Returns:
        CommerceTrustAnchor instance
    """
    exp_parts = exp.split("/")
    return CommerceTrustAnchor(
        pan_hash=hash_pan(pan),
        exp_month=int(exp_parts[0]),
        exp_year=int(exp_parts[1]) + 2000 if len(exp_parts[1]) == 2 else int(exp_parts[1]),
        name=name,
        last_four=pan[-4:]
    )
