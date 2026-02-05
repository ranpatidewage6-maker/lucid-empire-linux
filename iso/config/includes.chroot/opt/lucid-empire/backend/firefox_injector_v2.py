# =============================================================================
# LUCID EMPIRE v5.0-TITAN :: Firefox Profile Injector v2 (LSNG Edition)
# =============================================================================
# Direct SQLite injection for Firefox profiles with LSNG support.
# Implements Mozilla's internal storage formats for bit-perfect injection.
#
# Authority: Dva.12 | Classification: ZERO DETECT
# Source: Firefox Profile Storage Research Guide [cite: 7]
# =============================================================================

import hashlib
import json
import os
import sqlite3
import struct
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import random

# Try to import snappy for LSNG compression
try:
    import snappy
    SNAPPY_AVAILABLE = True
except ImportError:
    SNAPPY_AVAILABLE = False
    print("[Warning] python-snappy not available. LSNG compression disabled.")


@dataclass
class CookieEntryV2:
    """
    Firefox cookie entry for injection into cookies.sqlite.
    """
    name: str
    value: str
    host: str
    path: str = "/"
    expiry: int = 0  # Unix timestamp
    creation_time_prtime: int = 0  # PRTime (microseconds)
    last_accessed_prtime: int = 0
    secure: bool = True
    http_only: bool = False
    same_site: int = 0  # 0=None, 1=Lax, 2=Strict
    origin_attributes: str = ""  # For container tabs
    
    @property
    def base_domain(self) -> str:
        """Extract eTLD+1 from host."""
        host = self.host.lstrip(".")
        parts = host.split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return host


@dataclass
class HistoryEntryV2:
    """
    Firefox history entry for injection into places.sqlite.
    """
    url: str
    title: str
    visit_time_prtime: int  # PRTime (microseconds)
    visit_type: int = 1  # 1=LINK, 2=TYPED, 3=BOOKMARK
    frecency: int = 100
    
    @property
    def rev_host(self) -> str:
        """Generate reversed hostname with trailing dot."""
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        host = parsed.netloc.split(":")[0]  # Remove port
        if host.startswith("www."):
            host = host[4:]
        return host[::-1] + "."


@dataclass
class LocalStorageEntryV2:
    """
    Firefox localStorage entry for LSNG injection.
    """
    origin: str  # e.g., "https://stripe.com"
    key: str
    value: str


class FirefoxProfileInjectorV2:
    """
    Direct SQLite injection for Firefox profiles with LSNG support.
    
    Implements:
    - Mozilla 64-bit URL hashing for places.sqlite
    - PRTime timestamp handling
    - Reversed hostname generation
    - LSNG localStorage with Snappy compression
    - Quota Manager metadata generation
    
    Source: Firefox Profile Storage Research Guide [cite: 7]
    """
    
    # Visit type constants
    TRANSITION_LINK = 1
    TRANSITION_TYPED = 2
    TRANSITION_BOOKMARK = 3
    TRANSITION_EMBED = 4
    TRANSITION_REDIRECT_PERMANENT = 5
    TRANSITION_REDIRECT_TEMPORARY = 6
    TRANSITION_DOWNLOAD = 7
    TRANSITION_FRAMED_LINK = 8
    
    def __init__(self, profile_path: str, aging_days: int = 90):
        self.profile_path = Path(profile_path)
        self.aging_days = aging_days
        self.now = datetime.now()
        self.start_date = self.now - timedelta(days=aging_days)
        self.rng = random.Random()
        
        # Ensure profile directory exists
        self.profile_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def mozilla_url_hash(url: str) -> int:
        """
        Generate Mozilla's 64-bit URL hash.
        
        Uses a variant of DJB2 hash with MurmurHash3 finalization.
        Without valid hashes, Firefox cannot index history entries.
        
        Source: Firefox Profile Storage Research Guide [cite: 7.1]
        """
        # DJB2 hash variant
        h = 5381
        for char in url.encode('utf-8'):
            h = ((h << 5) + h + char) & 0xFFFFFFFFFFFFFFFF
        
        # MurmurHash3 finalization
        h ^= h >> 33
        h = (h * 0xFF51AFD7ED558CCD) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 33
        h = (h * 0xC4CEB9FE1A85EC53) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 33
        
        # Convert to signed 64-bit
        if h >= 0x8000000000000000:
            h -= 0x10000000000000000
        
        return h
    
    @staticmethod
    def generate_rev_host(hostname: str) -> str:
        """
        Generate reversed hostname with trailing dot.
        
        Example: "www.google.com" -> "moc.elgoog.www."
        
        Source: Firefox Profile Storage Research Guide [cite: 7.1]
        """
        if hostname.startswith("www."):
            hostname = hostname[4:]
        return hostname[::-1] + "."
    
    @staticmethod
    def to_prtime(dt: datetime) -> int:
        """Convert datetime to PRTime (microseconds since Unix epoch)."""
        return int(dt.timestamp() * 1_000_000)
    
    @staticmethod
    def from_prtime(prtime: int) -> datetime:
        """Convert PRTime to datetime."""
        return datetime.fromtimestamp(prtime / 1_000_000)
    
    @staticmethod
    def generate_firefox_guid() -> str:
        """
        Generate a 12-character Firefox GUID.
        
        Uses URL-safe Base64 characters.
        """
        import base64
        random_bytes = os.urandom(9)
        return base64.urlsafe_b64encode(random_bytes).decode()[:12]
    
    @staticmethod
    def sanitize_origin(url: str) -> str:
        """
        Sanitize origin URL to LSNG folder name format.
        
        Example: "https://example.com:8080" -> "https+++example.com+8080"
        
        Source: Firefox Profile Storage Research Guide [cite: 7.3]
        """
        # Remove trailing slash
        url = url.rstrip("/")
        # Replace :// with +++
        url = url.replace("://", "+++")
        # Replace : with +
        url = url.replace(":", "+")
        return url
    
    @staticmethod
    def desanitize_origin(folder: str) -> str:
        """
        Convert LSNG folder name back to origin URL.
        
        Example: "https+++example.com+8080" -> "https://example.com:8080"
        """
        # Find the protocol separator
        if "+++" in folder:
            protocol, rest = folder.split("+++", 1)
            # Replace remaining + with :
            rest = rest.replace("+", ":", 1)  # Only first one is port
            return f"{protocol}://{rest}"
        return folder
    
    @staticmethod
    def compress_value_snappy(value: str) -> Tuple[bytes, int]:
        """
        Compress localStorage value using Snappy compression.
        
        Returns:
            Tuple of (compressed_blob, compression_type)
            compression_type: 0=uncompressed, 1=snappy
        """
        if not SNAPPY_AVAILABLE:
            return value.encode('utf-8'), 0
        
        # Convert to UTF-16LE (Firefox's internal string format)
        utf16_data = value.encode('utf-16-le')
        
        # Compress with Snappy
        compressed = snappy.compress(utf16_data)
        
        # Only use compression if it's smaller
        if len(compressed) < len(utf16_data):
            return compressed, 1
        else:
            return utf16_data, 0
    
    def age_profile(self) -> bool:
        """
        Age the profile by creating/updating times.json.
        
        This file tells Firefox when the profile was created.
        """
        times_path = self.profile_path / "times.json"
        times_data = {
            "created": self.to_prtime(self.start_date),
            "firstUse": self.to_prtime(self.start_date + timedelta(minutes=5))
        }
        
        with open(times_path, 'w') as f:
            json.dump(times_data, f)
        
        print(f"[Injector] Profile aged to {self.start_date.isoformat()}")
        return True
    
    def _init_places_db(self) -> sqlite3.Connection:
        """Initialize or open places.sqlite database."""
        db_path = self.profile_path / "places.sqlite"
        conn = sqlite3.connect(str(db_path))
        
        # Create tables if they don't exist
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS moz_places (
                id INTEGER PRIMARY KEY,
                url TEXT,
                title TEXT,
                rev_host TEXT,
                visit_count INTEGER DEFAULT 0,
                hidden INTEGER DEFAULT 0,
                typed INTEGER DEFAULT 0,
                frecency INTEGER DEFAULT -1,
                last_visit_date INTEGER,
                guid TEXT,
                foreign_count INTEGER DEFAULT 0,
                url_hash INTEGER DEFAULT 0,
                description TEXT,
                preview_image_url TEXT,
                origin_id INTEGER
            );
            
            CREATE TABLE IF NOT EXISTS moz_historyvisits (
                id INTEGER PRIMARY KEY,
                from_visit INTEGER,
                place_id INTEGER,
                visit_date INTEGER,
                visit_type INTEGER,
                session INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS moz_origins (
                id INTEGER PRIMARY KEY,
                prefix TEXT NOT NULL,
                host TEXT NOT NULL,
                frecency INTEGER NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS moz_places_url_hashindex ON moz_places (url_hash);
            CREATE INDEX IF NOT EXISTS moz_places_hostindex ON moz_places (rev_host);
            CREATE INDEX IF NOT EXISTS moz_historyvisits_placedateindex 
                ON moz_historyvisits (place_id, visit_date);
        """)
        
        return conn
    
    def _init_cookies_db(self) -> sqlite3.Connection:
        """Initialize or open cookies.sqlite database."""
        db_path = self.profile_path / "cookies.sqlite"
        conn = sqlite3.connect(str(db_path))
        
        # Create table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS moz_cookies (
                id INTEGER PRIMARY KEY,
                originAttributes TEXT NOT NULL DEFAULT '',
                name TEXT,
                value TEXT,
                host TEXT,
                path TEXT,
                expiry INTEGER,
                lastAccessed INTEGER,
                creationTime INTEGER,
                isSecure INTEGER,
                isHttpOnly INTEGER,
                inBrowserElement INTEGER DEFAULT 0,
                sameSite INTEGER DEFAULT 0,
                rawSameSite INTEGER DEFAULT 0,
                schemeMap INTEGER DEFAULT 0,
                CONSTRAINT moz_uniqueid UNIQUE (name, host, path, originAttributes)
            )
        """)
        
        return conn
    
    def _init_formhistory_db(self) -> sqlite3.Connection:
        """Initialize or open formhistory.sqlite database."""
        db_path = self.profile_path / "formhistory.sqlite"
        conn = sqlite3.connect(str(db_path))
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS moz_formhistory (
                id INTEGER PRIMARY KEY,
                fieldname TEXT NOT NULL,
                value TEXT NOT NULL,
                timesUsed INTEGER,
                firstUsed INTEGER,
                lastUsed INTEGER,
                guid TEXT
            )
        """)
        
        return conn
    
    def inject_history_entry(self, entry: HistoryEntryV2) -> bool:
        """
        Inject a single history entry into places.sqlite.
        """
        conn = self._init_places_db()
        cursor = conn.cursor()
        
        try:
            # Generate URL hash
            url_hash = self.mozilla_url_hash(entry.url)
            
            # Generate GUID
            guid = self.generate_firefox_guid()
            
            # Insert into moz_places
            cursor.execute("""
                INSERT OR REPLACE INTO moz_places 
                (url, title, rev_host, visit_count, typed, frecency, 
                 last_visit_date, guid, url_hash)
                VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?)
            """, (
                entry.url,
                entry.title,
                entry.rev_host,
                1 if entry.visit_type == self.TRANSITION_TYPED else 0,
                entry.frecency,
                entry.visit_time_prtime,
                guid,
                url_hash
            ))
            
            place_id = cursor.lastrowid
            
            # Insert into moz_historyvisits
            cursor.execute("""
                INSERT INTO moz_historyvisits 
                (place_id, visit_date, visit_type, from_visit, session)
                VALUES (?, ?, ?, 0, 0)
            """, (place_id, entry.visit_time_prtime, entry.visit_type))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"[Injector] Error injecting history: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def inject_cookie(self, cookie: CookieEntryV2) -> bool:
        """
        Inject a single cookie into cookies.sqlite.
        """
        conn = self._init_cookies_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO moz_cookies
                (originAttributes, name, value, host, path, expiry,
                 lastAccessed, creationTime, isSecure, isHttpOnly, sameSite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cookie.origin_attributes,
                cookie.name,
                cookie.value,
                cookie.host,
                cookie.path,
                cookie.expiry,
                cookie.last_accessed_prtime or cookie.creation_time_prtime,
                cookie.creation_time_prtime,
                1 if cookie.secure else 0,
                1 if cookie.http_only else 0,
                cookie.same_site
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"[Injector] Error injecting cookie: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def inject_local_storage(self, entry: LocalStorageEntryV2) -> bool:
        """
        Inject a localStorage entry into LSNG storage.
        
        Creates the proper directory structure with:
        - .metadata-v2 file for Quota Manager
        - data.sqlite with compressed values
        
        Source: Firefox Profile Storage Research Guide [cite: 7.3]
        """
        # Sanitize origin to folder name
        origin_folder = self.sanitize_origin(entry.origin)
        
        # Create directory structure
        storage_path = self.profile_path / "storage" / "default" / origin_folder / "ls"
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Create .metadata-v2 file (Quota Manager requirement)
        metadata_path = storage_path.parent / ".metadata-v2"
        if not metadata_path.exists():
            self._create_metadata_v2(metadata_path, entry.origin)
        
        # Open or create data.sqlite
        db_path = storage_path / "data.sqlite"
        conn = sqlite3.connect(str(db_path))
        
        try:
            # Create table if it doesn't exist
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data (
                    key TEXT PRIMARY KEY,
                    utf16_length INTEGER NOT NULL DEFAULT 0,
                    conversion_type INTEGER NOT NULL DEFAULT 0,
                    compression_type INTEGER NOT NULL DEFAULT 0,
                    last_access_time INTEGER NOT NULL DEFAULT 0,
                    value BLOB NOT NULL
                )
            """)
            
            # Compress value
            compressed_value, compression_type = self.compress_value_snappy(entry.value)
            utf16_length = len(entry.value)
            
            # Insert data
            conn.execute("""
                INSERT OR REPLACE INTO data 
                (key, utf16_length, conversion_type, compression_type, 
                 last_access_time, value)
                VALUES (?, ?, 0, ?, ?, ?)
            """, (
                entry.key,
                utf16_length,
                compression_type,
                self.to_prtime(self.now),
                compressed_value
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"[Injector] Error injecting localStorage: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def _create_metadata_v2(self, path: Path, origin: str):
        """
        Create a .metadata-v2 file for Quota Manager validation.
        
        The file format is:
        - 8 bytes: timestamp (PRTime)
        - 1 byte: persistence (0=temporary, 1=default)
        - 4 bytes: origin suffix length
        - origin suffix string (if length > 0)
        - 1 byte: is app flag
        
        Source: Firefox Profile Storage Research Guide [cite: 7.3]
        """
        with open(path, 'wb') as f:
            # Timestamp (PRTime) - 8 bytes, little-endian
            timestamp = self.to_prtime(self.start_date)
            f.write(struct.pack('<Q', timestamp))
            
            # Persistence type - 1 byte (1 = default storage)
            f.write(struct.pack('B', 1))
            
            # Origin suffix length - 4 bytes (0 for no suffix)
            f.write(struct.pack('<I', 0))
            
            # Is app flag - 1 byte (0 = not an app)
            f.write(struct.pack('B', 0))
    
    def inject_form_history(self, fieldname: str, value: str, times_used: int = 1) -> bool:
        """
        Inject a form history entry for autofill.
        """
        conn = self._init_formhistory_db()
        cursor = conn.cursor()
        
        try:
            first_used = self.to_prtime(self.start_date + timedelta(days=self.rng.randint(1, 30)))
            last_used = self.to_prtime(self.now - timedelta(days=self.rng.randint(1, 7)))
            guid = self.generate_firefox_guid()
            
            cursor.execute("""
                INSERT OR REPLACE INTO moz_formhistory
                (fieldname, value, timesUsed, firstUsed, lastUsed, guid)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fieldname, value, times_used, first_used, last_used, guid))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"[Injector] Error injecting form history: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def generate_realistic_history(
        self,
        history_entries: List[Dict[str, Any]],
        persona: str = "shopper"
    ) -> int:
        """
        Inject a list of history entries from Genesis Engine.
        
        Args:
            history_entries: List of history dicts from Genesis Engine
            persona: Browsing persona for frecency calculation
            
        Returns:
            Number of successfully injected entries
        """
        injected = 0
        
        for entry_data in history_entries:
            from urllib.parse import urlparse
            parsed = urlparse(entry_data["url"])
            hostname = parsed.netloc.split(":")[0]
            if hostname.startswith("www."):
                hostname = hostname[4:]
            
            entry = HistoryEntryV2(
                url=entry_data["url"],
                title=entry_data.get("title", ""),
                visit_time_prtime=entry_data["visit_time_prtime"],
                visit_type=entry_data.get("visit_type", 1),
                frecency=self._calculate_frecency(
                    entry_data["visit_time_prtime"],
                    entry_data.get("visit_type", 1)
                )
            )
            
            if self.inject_history_entry(entry):
                injected += 1
        
        print(f"[Injector] Injected {injected}/{len(history_entries)} history entries")
        return injected
    
    def _calculate_frecency(self, visit_time_prtime: int, visit_type: int) -> int:
        """
        Calculate frecency score based on visit recency and type.
        
        Firefox uses frecency (frequency + recency) for URL bar suggestions.
        """
        now_prtime = self.to_prtime(self.now)
        age_days = (now_prtime - visit_time_prtime) / (1_000_000 * 86400)
        
        # Type weights
        type_weight = {
            1: 100,   # LINK
            2: 200,   # TYPED
            3: 140,   # BOOKMARK
            4: 0,     # EMBED
            5: 0,     # REDIRECT
        }.get(visit_type, 100)
        
        # Decay based on age
        if age_days < 4:
            recency_weight = 100
        elif age_days < 14:
            recency_weight = 70
        elif age_days < 31:
            recency_weight = 50
        elif age_days < 90:
            recency_weight = 30
        else:
            recency_weight = 10
        
        return int(type_weight * recency_weight / 100)
    
    def inject_commerce_cookies(self, commerce_cookies: List[Dict[str, Any]]) -> int:
        """
        Inject commerce cookies from Genesis Engine artifacts.
        """
        injected = 0
        
        for cookie_data in commerce_cookies:
            cookie = CookieEntryV2(
                name=cookie_data["name"],
                value=cookie_data["value"],
                host=cookie_data["host"],
                path=cookie_data.get("path", "/"),
                expiry=cookie_data.get("expiry", 0),
                creation_time_prtime=cookie_data["creation_time_prtime"],
                secure=cookie_data.get("secure", True),
                http_only=cookie_data.get("http_only", False),
                same_site=cookie_data.get("same_site", 0)
            )
            
            if self.inject_cookie(cookie):
                injected += 1
        
        print(f"[Injector] Injected {injected}/{len(commerce_cookies)} cookies")
        return injected
    
    def inject_commerce_vault(self, commerce_vault: Dict[str, Any]) -> int:
        """
        Inject commerce vault tokens into localStorage (LSNG).
        """
        injected = 0
        
        # Stripe tokens
        if "stripe" in commerce_vault:
            stripe = commerce_vault["stripe"]
            
            # __stripe_mid as cookie
            self.inject_cookie(CookieEntryV2(
                name="__stripe_mid",
                value=stripe["__stripe_mid"],
                host=".stripe.com",
                path="/",
                expiry=int((self.now + timedelta(days=365)).timestamp()),
                creation_time_prtime=stripe["creation_time"] * 1000,
                secure=True,
                http_only=False,
                same_site=0
            ))
            injected += 1
            
            # Device ID in localStorage
            self.inject_local_storage(LocalStorageEntryV2(
                origin="https://stripe.com",
                key="__stripe_mid",
                value=stripe["__stripe_mid"]
            ))
            injected += 1
        
        # Adyen tokens
        if "adyen" in commerce_vault:
            adyen = commerce_vault["adyen"]
            
            self.inject_local_storage(LocalStorageEntryV2(
                origin="https://adyen.com",
                key="risk_device_id",
                value=adyen["risk_device_id"]
            ))
            injected += 1
            
            self.inject_local_storage(LocalStorageEntryV2(
                origin="https://adyen.com",
                key="dfValue",
                value=adyen["dfValue"]
            ))
            injected += 1
        
        # PayPal tokens
        if "paypal" in commerce_vault:
            paypal = commerce_vault["paypal"]
            
            self.inject_cookie(CookieEntryV2(
                name="AKDC",
                value=paypal["AKDC"],
                host=".paypal.com",
                path="/",
                expiry=int((self.now + timedelta(days=365)).timestamp()),
                creation_time_prtime=paypal["creation_time"] * 1000,
                secure=True,
                http_only=True,
                same_site=1
            ))
            injected += 1
        
        print(f"[Injector] Injected {injected} commerce vault tokens")
        return injected
    
    def inject_from_genesis_artifacts(self, artifacts_path: Path) -> Dict[str, int]:
        """
        Inject all artifacts generated by Genesis Engine.
        
        Args:
            artifacts_path: Path to the Genesis Engine artifact directory
            
        Returns:
            Dict with counts of injected items
        """
        results = {
            "history": 0,
            "cookies": 0,
            "commerce_vault": 0,
            "form_history": 0
        }
        
        # Age the profile first
        self.age_profile()
        
        # Inject browsing history
        history_file = artifacts_path / "browsing_history.json"
        if history_file.exists():
            with open(history_file) as f:
                history = json.load(f)
            results["history"] = self.generate_realistic_history(history)
        
        # Inject cookies
        cookies_file = artifacts_path / "commerce_cookies.json"
        if cookies_file.exists():
            with open(cookies_file) as f:
                cookies = json.load(f)
            results["cookies"] = self.inject_commerce_cookies(cookies)
        
        # Inject commerce vault
        vault_file = artifacts_path / "commerce_vault.json"
        if vault_file.exists():
            with open(vault_file) as f:
                vault = json.load(f)
            results["commerce_vault"] = self.inject_commerce_vault(vault)
        
        # Inject form history
        form_file = artifacts_path / "form_history.json"
        if form_file.exists():
            with open(form_file) as f:
                form_data = json.load(f)
            for entry in form_data:
                if self.inject_form_history(
                    entry["fieldname"], 
                    entry["value"],
                    entry.get("times_used", 1)
                ):
                    results["form_history"] += 1
        
        print(f"[Injector] Full injection complete: {results}")
        return results
