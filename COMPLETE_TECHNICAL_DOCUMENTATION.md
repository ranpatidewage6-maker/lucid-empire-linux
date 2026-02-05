# 🛡️ LUCID EMPIRE v5.0.0-TITAN

## Complete Technical Documentation & Research Guide

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  LUCID EMPIRE v5.0.0-TITAN                                                   ║
║  Anti-Detect Browser System | Sovereign Reality Fabrication Station          ║
║  Zero Detect Upgrade: JA4 Bypass | Canvas Noise | Ghost Motor GAN            ║
║  Authority: Dva.12 | Classification: ZERO DETECT                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Document Version:** 5.0.0  
**Last Updated:** February 5, 2026  
**Author:** LUCID EMPIRE Development Team  
**Classification:** Research & Development Documentation

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Core Components](#3-core-components)
4. [Zero Detect System](#4-zero-detect-system)
5. [Firefox Profile Injection](#5-firefox-profile-injection)
6. [Genesis Engine](#6-genesis-engine)
7. [LSNG (Local Storage Next Gen)](#7-lsng-local-storage-next-gen)
8. [Commerce Trust System](#8-commerce-trust-system)
9. [Workflows](#9-workflows)
10. [API Reference](#10-api-reference)
11. [Research Background](#11-research-background)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Executive Summary

### What is LUCID EMPIRE?

LUCID EMPIRE is an advanced anti-detect browser system designed for research into browser fingerprinting, anti-fraud systems, and profile isolation. It creates "aged" browser profiles that appear to have existed for 90+ days, bypassing temporal detection vectors used by modern anti-fraud systems.

### Key Capabilities

| Capability | Description | Detection Vector Addressed |
|------------|-------------|---------------------------|
| **Profile Aging** | Backdate profiles to 90+ days | New profile detection |
| **Cookie Injection** | Direct SQLite injection with PRTime | Runtime cookie manipulation detection |
| **History Generation** | Natural visit patterns with Mozilla URL hash | Empty history detection |
| **LSNG Storage** | Proper localStorage with Snappy compression | Storage inconsistency |
| **TLS Fingerprinting** | JA4/JA3/HTTP2 masquerading | Network fingerprint analysis |
| **Canvas Noise** | Deterministic Perlin noise injection | Canvas fingerprint uniqueness |
| **Ghost Motor** | GAN-inspired mouse trajectories | Bot behavior patterns |

### Why Direct SQL Injection?

Modern anti-fraud systems detect browser automation in multiple ways:

```
┌────────────────────────────────────────────────────────────────────┐
│                    DETECTION VECTORS                                │
├────────────────────────────────────────────────────────────────────┤
│  ❌ Playwright/Selenium cookies → Runtime timestamp = "now"        │
│  ❌ JavaScript localStorage → No Snappy compression                │
│  ❌ Automated history → All visits typed, no link clicks           │
│  ❌ New profile → times.json shows creation = session start        │
│                                                                     │
│  ✅ Direct SQL Injection → Timestamps in PRTime microseconds       │
│  ✅ LSNG with .metadata-v2 → Quota Manager validates               │
│  ✅ Natural visit distribution → 70% link, 20% typed, 10% bookmark │
│  ✅ Backdated times.json → Profile appears 90 days old             │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LUCID EMPIRE ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │   GENESIS    │───▶│   FIREFOX    │───▶│   CAMOUFOX   │                  │
│   │   ENGINE     │    │   INJECTOR   │    │   BROWSER    │                  │
│   │              │    │              │    │              │                  │
│   │ JSON Artifacts│   │ SQLite DBs   │    │ Live Profile │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│          │                   │                   │                           │
│          ▼                   ▼                   ▼                           │
│   ┌──────────────────────────────────────────────────────┐                  │
│   │                  ZERO DETECT LAYER                    │                  │
│   ├──────────────────────────────────────────────────────┤                  │
│   │  TLS Masquerade │ Canvas Noise │ Ghost Motor │ Vault │                  │
│   └──────────────────────────────────────────────────────┘                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
lucid-empire-new/
├── TITAN_CONSOLE.py              # Main GUI application
├── lucid_genesis_engine.py       # Profile artifact generator
├── lucid_firefox_injector.py     # Direct SQLite injector
├── verify_full_system.py         # System verification suite
│
├── backend/
│   ├── __init__.py
│   ├── zero_detect.py            # Unified Zero Detect engine
│   │
│   ├── modules/
│   │   ├── __init__.py           # Module exports
│   │   ├── canvas_noise.py       # Perlin noise fingerprint injection
│   │   ├── ghost_motor.py        # GAN-inspired mouse trajectories
│   │   ├── commerce_vault.py     # Trust token generation
│   │   ├── firefox_injector.py   # Profile injection v1
│   │   └── firefox_injector_v2.py # Profile injection v2 (LSNG)
│   │
│   ├── network/
│   │   └── tls_masquerade.py     # JA4/JA3/HTTP2 fingerprinting
│   │
│   ├── validation/
│   │   └── preflight_validator.py # 8-point validation matrix
│   │
│   └── core/
│       └── cortex.py             # Core orchestration
│
├── lucid_profile_data/           # Generated profiles
│   └── {profile_name}/
│       ├── metadata.json
│       ├── commerce_cookies.json
│       ├── browsing_history.json
│       ├── commerce_vault.json
│       ├── form_history.json
│       ├── times.json
│       ├── cookies.sqlite
│       ├── places.sqlite
│       ├── formhistory.sqlite
│       └── storage/default/      # LSNG storage
│
├── docs/                         # Documentation
├── research_reports/             # Research findings
└── camoufox/                     # Browser engine
```

---

## 3. Core Components

### 3.1 TITAN_CONSOLE.py

**Purpose:** Main graphical user interface for profile management and browser control.

**Features:**
- Profile creation wizard
- Zero Detect configuration
- Browser launch management
- Real-time validation status

**Usage:**
```bash
python TITAN_CONSOLE.py
```

### 3.2 Genesis Engine (lucid_genesis_engine.py)

**Purpose:** Generates JSON artifacts containing profile data before SQLite injection.

**Why Separate Generation?**
- Reproducibility: Same seed = same profile
- Auditing: JSON files are human-readable
- Modularity: Generation logic separate from injection

**Command Line:**
```bash
python lucid_genesis_engine.py --profile "Profile_001" --persona shopper --age 90
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--profile` | Profile name | `Profile_<timestamp>` |
| `--persona` | Browsing pattern (shopper/developer/general) | `shopper` |
| `--age` | Profile age in days | `90` |
| `--seed` | Random seed for reproducibility | Random UUID |

**Output Files:**
```
lucid_profile_data/{profile}/
├── metadata.json         # Profile configuration
├── commerce_cookies.json # Stripe, Adyen, PayPal cookies
├── browsing_history.json # Browsing history entries
├── commerce_vault.json   # LocalStorage data
└── form_history.json     # Form autofill data
```

### 3.3 Firefox Injector (lucid_firefox_injector.py)

**Purpose:** Performs direct SQLite injection into Firefox profile databases.

**Why Direct SQLite?**
```
Browser API (Playwright/Selenium):
  cookies.add({...}) → Cookie.creationTime = Date.now()
  
Direct SQLite:
  INSERT INTO moz_cookies (creationTime) VALUES (prtime_90_days_ago)
```

**Command Line:**
```bash
python lucid_firefox_injector.py --profile "Profile_001"
```

**Databases Modified:**
| Database | Table | Purpose |
|----------|-------|---------|
| `cookies.sqlite` | `moz_cookies` | Trust cookies (Stripe, Adyen, PayPal) |
| `places.sqlite` | `moz_places`, `moz_historyvisits` | Browsing history |
| `formhistory.sqlite` | `moz_formhistory` | Form autofill |
| `storage/default/*/ls/data.sqlite` | `data` | LocalStorage (LSNG) |

---

## 4. Zero Detect System

### 4.1 Overview

The Zero Detect system addresses all major fingerprinting vectors:

```
┌───────────────────────────────────────────────────────────────────┐
│                      ZERO DETECT STACK                             │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Layer 5: Behavioral      │ Ghost Motor GAN (mouse/keyboard)     │
│  Layer 4: Application     │ Commerce Vault (trust tokens)        │
│  Layer 3: Storage         │ LSNG + Snappy + Quota Manager        │
│  Layer 2: Browser         │ Canvas/WebGL/Audio Noise             │
│  Layer 1: Network         │ TLS/JA4/HTTP2 Fingerprinting         │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

### 4.2 TLS Masquerade (backend/network/tls_masquerade.py)

**Purpose:** Match TLS fingerprints of legitimate browsers.

**Detection Vector Addressed:**
- JA3: SSL/TLS fingerprint based on ClientHello
- JA4: Enhanced fingerprint including ALPN and extensions
- HTTP/2: SETTINGS frame, header order, stream priorities

**How It Works:**
```python
from backend.network.tls_masquerade import TLSMasqueradeManager

masquerader = TLSMasqueradeManager()
config = masquerader.get_chrome_120_profile()

# Returns:
# - Cipher suites matching Chrome 120
# - TLS extensions in correct order
# - ALPN protocols (h2, http/1.1)
# - HTTP/2 SETTINGS values
```

**Chrome 120 JA4 Fingerprint:**
```
t13d1517h2_8daaf6152771_b0da82dd1658
```

### 4.3 Canvas Noise (backend/modules/canvas_noise.py)

**Purpose:** Inject deterministic Perlin noise into canvas fingerprints.

**Detection Vector Addressed:**
- Canvas fingerprinting (getImageData hash)
- WebGL fingerprinting
- Audio fingerprinting

**Key Principle: Determinism**
```
Same Profile UUID → Same Noise Pattern → Same Fingerprint Hash

Profile A: UUID=abc123 → Canvas Hash: 0x7F3A2B
Profile A: UUID=abc123 → Canvas Hash: 0x7F3A2B (same!)
Profile B: UUID=def456 → Canvas Hash: 0x9C4D1E (different)
```

**Implementation:**
```python
from backend.modules import CanvasNoiseInjector, CanvasNoiseConfig

# Create config from profile UUID (deterministic)
config = CanvasNoiseConfig.from_profile_uuid("profile-uuid-12345")
injector = CanvasNoiseInjector(config)

# Inject noise into image data
noisy_data = injector.inject_noise(original_image_data)
```

**Perlin Noise Algorithm:**
```python
def perlin_noise(x, y, seed):
    """
    Generate smooth, continuous noise for sub-pixel modifications.
    
    Parameters:
    - x, y: Pixel coordinates
    - seed: Profile-derived seed
    
    Returns:
    - Float in range [-1, 1]
    """
    # Gradient vectors at grid points
    # Interpolate between gradients
    # Result: Smooth noise that varies by position
```

### 4.4 Ghost Motor GAN (backend/modules/ghost_motor.py)

**Purpose:** Generate human-like mouse trajectories and keyboard patterns.

**Detection Vector Addressed:**
- Bot detection via mouse movement analysis
- Linear paths (bots) vs curved paths (humans)
- Constant velocity (bots) vs variable velocity (humans)
- Lack of micro-tremors and overshoots

**Trajectory Generation:**
```python
from backend.modules import GhostMotorGAN, TrajectoryConfig

config = TrajectoryConfig(
    base_speed=800.0,        # pixels/second
    speed_variance=0.3,      # ±30% variance
    overshoot_probability=0.15,
    tremor_enabled=True,
    tremor_amplitude=0.5,    # pixels
    curvature_factor=0.3
)

motor = GhostMotorGAN(config)
trajectory = motor.generate_trajectory(
    start=(100, 100),
    end=(500, 400)
)

# Returns list of points with timestamps:
# [Point(x=100, y=100, t=0.0), Point(x=105, y=98, t=0.02), ...]
```

**Human Movement Characteristics:**
```
┌─────────────────────────────────────────────────────────────────┐
│                     BOT vs HUMAN MOVEMENT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BOT:                        HUMAN (Ghost Motor):               │
│  ────────────────────        ────────────────────               │
│  • Straight lines            • Curved Bézier paths              │
│  • Constant velocity         • Acceleration/deceleration        │
│  • No overshoot              • 15% overshoot probability        │
│  • Pixel-perfect targets     • Micro-tremor (hand shake)        │
│  • Uniform timing            • Variable timing                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.5 Commerce Vault (backend/modules/commerce_vault.py)

**Purpose:** Generate authentic-looking commerce trust tokens.

**Detection Vector Addressed:**
- New device detection by payment processors
- Missing or invalid trust tokens
- Token age analysis

**Supported Platforms:**
| Platform | Cookies | LocalStorage Keys |
|----------|---------|-------------------|
| Stripe | `__stripe_mid`, `__stripe_sid` | `m`, `deviceId` |
| Adyen | `_RP_UID`, `adyen_session` | `risk_device_id`, `dfValue` |
| PayPal | `TLTSID`, `nsid` | `clientId`, `fpti` |
| Checkout.com | `cko_device_id` | `deviceId`, `riskFingerprint` |

**Token Generation:**
```python
from backend.modules import CommerceVault

vault = CommerceVault(profile_uuid="unique-profile-id")
tokens = vault.generate_all_tokens(age_days=90)

# Stripe __stripe_mid format:
# v3|{timestamp_ms}|{device_hash}
# Example: v3|1699300000000|a1b2c3d4e5f6
```

### 4.6 Preflight Validator (backend/validation/preflight_validator.py)

**Purpose:** 8-point validation before browser launch.

**Validation Checks:**
| Check | Description | Failure Action |
|-------|-------------|----------------|
| 1. IP Reputation | Check IP against blacklists | Abort |
| 2. JA4 Consistency | Verify TLS fingerprint matches target | Warn |
| 3. Canvas Hash | Verify deterministic noise | Regenerate |
| 4. WebGL Hash | Verify WebGL fingerprint | Regenerate |
| 5. Audio Hash | Verify audio fingerprint | Regenerate |
| 6. Cookie Age | Verify cookies are properly backdated | Re-inject |
| 7. History Volume | Verify sufficient history entries | Generate more |
| 8. Storage Integrity | Verify LSNG structure | Repair |

---

## 5. Firefox Profile Injection

### 5.1 Database Schemas

#### cookies.sqlite (moz_cookies)

```sql
CREATE TABLE moz_cookies (
    id INTEGER PRIMARY KEY,
    baseDomain TEXT,           -- eTLD+1 (e.g., "stripe.com")
    originAttributes TEXT,     -- Container/partition key
    name TEXT,                 -- Cookie name
    value TEXT,                -- Cookie value
    host TEXT,                 -- Host with leading dot
    path TEXT,                 -- Cookie path
    expiry INTEGER,            -- Unix timestamp (seconds)
    lastAccessed INTEGER,      -- PRTime (microseconds)
    creationTime INTEGER,      -- PRTime (microseconds) ← KEY FIELD
    isSecure INTEGER,
    isHttpOnly INTEGER,
    inBrowserElement INTEGER,
    sameSite INTEGER,          -- 0=None, 1=Lax, 2=Strict
    rawSameSite INTEGER,
    schemeMap INTEGER
);
```

**Critical: PRTime Format**
```
Unix Timestamp (seconds):     1699300000
PRTime (microseconds):        1699300000000000

Conversion: PRTime = Unix × 1,000,000
```

#### places.sqlite (moz_places + moz_historyvisits)

```sql
CREATE TABLE moz_places (
    id INTEGER PRIMARY KEY,
    url LONGVARCHAR,
    title LONGVARCHAR,
    rev_host LONGVARCHAR,      -- Reversed hostname with trailing dot
    visit_count INTEGER,
    hidden INTEGER,
    typed INTEGER,
    frecency INTEGER,          -- Frequency + Recency score
    last_visit_date INTEGER,   -- PRTime
    guid TEXT,                 -- 12-char Firefox GUID
    url_hash INTEGER,          -- Mozilla 64-bit hash ← CRITICAL
    foreign_count INTEGER
);

CREATE TABLE moz_historyvisits (
    id INTEGER PRIMARY KEY,
    from_visit INTEGER,
    place_id INTEGER,
    visit_date INTEGER,        -- PRTime
    visit_type INTEGER,        -- 1=Link, 2=Typed, 3=Bookmark, etc.
    session INTEGER
);
```

### 5.2 Mozilla URL Hash Algorithm

**Why URL Hash Matters:**
- Firefox uses `url_hash` as primary lookup key
- Without valid hash, autocomplete fails
- Invalid hash = "broken" profile to fingerprinters

**Implementation:**
```python
def mozilla_url_hash(url: str) -> int:
    """
    Calculate Mozilla's 64-bit URL hash.
    Based on DJB2 with MurmurHash3 finalization.
    """
    h = 0
    for char in url.encode('utf-8'):
        h = ((h << 5) - h + char) & 0xFFFFFFFFFFFFFFFF
    
    # MurmurHash3 finalization
    h ^= (h >> 33)
    h = (h * 0xFF51AFD7ED558CCD) & 0xFFFFFFFFFFFFFFFF
    h ^= (h >> 33)
    h = (h * 0xC4CEB9FE1A85EC53) & 0xFFFFFFFFFFFFFFFF
    h ^= (h >> 33)
    
    # Convert to signed 64-bit
    if h >= 0x8000000000000000:
        h -= 0x10000000000000000
    
    return h
```

### 5.3 Reversed Hostname (rev_host)

**Purpose:** Enables efficient B-Tree prefix searches.

**Format:**
```
Original:     www.google.com
rev_host:     moc.elgoog.www.    ← Note trailing dot

Query all google.com subdomains:
  WHERE rev_host LIKE 'moc.elgoog.%'
```

**Implementation:**
```python
def generate_rev_host(hostname: str) -> str:
    return ".".join(reversed(hostname.split("."))) + "."
```

### 5.4 Visit Type Distribution

**Why Distribution Matters:**
```
BOT PROFILE:                  HUMAN PROFILE:
─────────────                 ─────────────
TYPED: 100%                   LINK: 70%
                              TYPED: 20%
                              BOOKMARK: 10%
```

**Visit Type Constants:**
| Type | Name | Description |
|------|------|-------------|
| 1 | TRANSITION_LINK | User clicked a link |
| 2 | TRANSITION_TYPED | User typed URL |
| 3 | TRANSITION_BOOKMARK | Opened from bookmark |
| 4 | TRANSITION_EMBED | Embedded frame |
| 5 | TRANSITION_REDIRECT_PERMANENT | 301 redirect |
| 6 | TRANSITION_REDIRECT_TEMPORARY | 302 redirect |
| 7 | TRANSITION_DOWNLOAD | Download initiated |
| 8 | TRANSITION_FRAMED_LINK | Link in frame |
| 9 | TRANSITION_RELOAD | Page reload |

---

## 6. Genesis Engine

### 6.1 Artifact Generation Pipeline

```
┌───────────────────────────────────────────────────────────────────┐
│                    GENESIS ENGINE PIPELINE                         │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Input:                                                            │
│    • Profile name                                                  │
│    • Persona (shopper/developer/general)                          │
│    • Age in days                                                   │
│    • Random seed (optional)                                        │
│                                                                    │
│  Processing:                                                       │
│    1. Generate deterministic Profile UUID from seed                │
│    2. Generate commerce cookies with backdated timestamps          │
│    3. Generate browsing history with natural patterns              │
│    4. Generate LocalStorage vault data                             │
│    5. Generate form autofill history                               │
│                                                                    │
│  Output:                                                           │
│    • metadata.json                                                 │
│    • commerce_cookies.json                                         │
│    • browsing_history.json                                         │
│    • commerce_vault.json                                           │
│    • form_history.json                                             │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

### 6.2 Persona Browsing Patterns

**Shopper Persona:**
```python
SHOPPER_SITES = [
    {"url": "https://www.amazon.com", "weight": 20},
    {"url": "https://www.ebay.com", "weight": 15},
    {"url": "https://www.walmart.com", "weight": 12},
    {"url": "https://www.target.com", "weight": 10},
    # ... more shopping sites
]
```

**Developer Persona:**
```python
DEVELOPER_SITES = [
    {"url": "https://github.com", "weight": 25},
    {"url": "https://stackoverflow.com", "weight": 20},
    {"url": "https://developer.mozilla.org", "weight": 15},
    # ... more developer sites
]
```

### 6.3 Timestamp Aging

**Time Calculations:**
```python
now = time.time()                    # Current Unix timestamp
age_seconds = 90 * 86400             # 90 days in seconds
creation_time = now - age_seconds    # 90 days ago

# Convert to Firefox formats
prtime = int(creation_time * 1_000_000)  # PRTime (microseconds)
cookie_expiry = int(now + 31536000)       # 1 year from now (seconds)
times_json = int(creation_time * 1000)    # Milliseconds
```

---

## 7. LSNG (Local Storage Next Gen)

### 7.1 Directory Structure

Firefox stores LocalStorage in a specific directory structure:

```
profile/storage/default/
├── https+++stripe.com/
│   ├── .metadata             # Legacy metadata
│   ├── .metadata-v2          # Quota Manager metadata ← CRITICAL
│   └── ls/
│       ├── data.sqlite       # Key-value storage
│       └── usage             # Size tracking
│
├── https+++adyen.com/
│   ├── .metadata-v2
│   └── ls/data.sqlite
│
└── https+++paypal.com/
    ├── .metadata-v2
    └── ls/data.sqlite
```

### 7.2 Origin Sanitization

**URL to Folder Name:**
```
https://stripe.com       → https+++stripe.com
https://example.com:8080 → https+++example.com+8080
http://localhost:3000    → http+++localhost+3000
```

**Implementation:**
```python
def sanitize_origin(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port
    
    result = f"{scheme}+++{host}"
    if port:
        result += f"+{port}"
    return result
```

### 7.3 .metadata-v2 File Format

**Without this file, Firefox considers the storage corrupt.**

```python
def create_metadata_v2(origin: str, creation_time: int) -> bytes:
    """
    Binary format:
    - 8 bytes: creation time (PRTime, little-endian uint64)
    - 4 bytes: flags (usually 0)
    - N bytes: origin string (null-terminated UTF-8)
    """
    data = struct.pack('<Q', creation_time)  # 8 bytes
    data += struct.pack('<I', 0)             # 4 bytes
    data += origin.encode('utf-8') + b'\x00' # null-terminated
    return data
```

### 7.4 LSNG data.sqlite Schema

```sql
CREATE TABLE data (
    key TEXT PRIMARY KEY,
    utf16_length INTEGER NOT NULL DEFAULT 0,
    conversion_type INTEGER NOT NULL DEFAULT 0,  -- 0=UTF-8, 1=UTF-16
    compression_type INTEGER NOT NULL DEFAULT 0, -- 0=None, 1=Snappy
    last_access_time INTEGER,
    value BLOB  -- Optionally Snappy-compressed
);
```

**Value Encoding:**
```python
# Uncompressed UTF-16 LE (compression_type=0)
value_bytes = value_str.encode('utf-16-le')

# Snappy compressed (compression_type=1)
import snappy
value_bytes = snappy.compress(value_str.encode('utf-16-le'))
```

---

## 8. Commerce Trust System

### 8.1 Why Commerce Tokens Matter

Payment processors build trust profiles based on:
1. **Device consistency** - Same device ID across sessions
2. **Token age** - Older tokens = established device
3. **Behavioral signals** - Normal browsing patterns

### 8.2 Stripe Tokens

**__stripe_mid (Machine ID):**
```
Format: v3|{timestamp_ms}|{device_hash}
Example: v3|1699300000000|a1b2c3d4e5f67890

- v3: Token version
- timestamp_ms: Creation time in milliseconds
- device_hash: 16-char device fingerprint hash
```

**__stripe_sid (Session ID):**
```
Format: v2|{session_hash}|{timestamp}
Example: v2|8f3c47e0d7467842914324891|1738766400

- v2: Token version
- session_hash: 24-char session identifier
- timestamp: Current Unix timestamp
```

### 8.3 Adyen Tokens

**_RP_UID (Risk Platform UID):**
```
Format: {uid}-{timestamp_hex}-{random}
Example: a1b2c3d4e5f6-67890abc-12345678

- uid: 12-char device identifier
- timestamp_hex: Creation time in hex
- random: 8-char random suffix
```

### 8.4 PayPal Tokens

**TLTSID (Trust Layer Session ID):**
```
Format: {hash}
Example: a1b2c3d4e5f67890a1b2c3d4e5f67890

- 32-char SHA-256 hash derived from profile UUID
```

---

## 9. Workflows

### 9.1 Complete Profile Creation Workflow

```
Step 1: Generate Artifacts
─────────────────────────
$ python lucid_genesis_engine.py --profile "MyProfile" --persona shopper --age 90

Output:
  ✓ metadata.json (314 bytes)
  ✓ commerce_cookies.json (2178 bytes)
  ✓ browsing_history.json (188244 bytes)
  ✓ commerce_vault.json (578 bytes)
  ✓ form_history.json (493 bytes)


Step 2: Inject into Profile
───────────────────────────
$ python lucid_firefox_injector.py --profile "MyProfile"

Output:
  ✓ Profile aged to 90 days ago (times.json)
  ✓ Injected 9 cookies (cookies.sqlite)
  ✓ Injected 20 URLs, 1143 visits (places.sqlite)
  ✓ Injected LSNG storage (storage/default/)
  ✓ Injected 3 form entries (formhistory.sqlite)


Step 3: Launch Browser
──────────────────────
$ python TITAN_CONSOLE.py
  → Select "MyProfile"
  → Click "Launch Browser"


Step 4: Verification
────────────────────
$ python verify_injection.py

Output:
  ✓ Profile created: 2025-11-07 (90 days ago)
  ✓ Cookies backdated to 2025-11-07
  ✓ Visit distribution: LINK=70%, TYPED=20%, BOOKMARK=10%
  ✓ LSNG structure valid with .metadata-v2
```

### 9.2 Programmatic Usage

```python
# Full pipeline in code

from lucid_genesis_engine import GenesisEngine
from lucid_firefox_injector import FirefoxInjector
from backend.modules import FirefoxProfileInjectorV2

# 1. Generate artifacts
engine = GenesisEngine(
    profile_name="API_Profile",
    persona="shopper",
    age_days=90,
    seed="reproducible-seed"
)
engine.generate_all()

# 2. Inject into profile
injector = FirefoxInjector(
    artifacts_path="lucid_profile_data/API_Profile",
    target_profile="lucid_profile_data/API_Profile"
)
injector.inject_all()

# 3. Additional custom injection
from backend.modules import (
    FirefoxProfileInjectorV2,
    HistoryEntryV2,
    CookieEntryV2,
    LocalStorageEntryV2
)

profile = FirefoxProfileInjectorV2("lucid_profile_data/API_Profile")

# Custom history entry
profile.inject_history(HistoryEntryV2(
    url="https://custom-site.com",
    title="Custom Site",
    visit_type=1
))

# Custom cookie
profile.inject_cookie(CookieEntryV2(
    name="custom_cookie",
    value="custom_value",
    host=".custom-site.com"
))

# Custom localStorage
profile.inject_local_storage(LocalStorageEntryV2(
    origin="https://custom-site.com",
    key="custom_key",
    value="custom_value"
))
```

---

## 10. API Reference

### 10.1 Genesis Engine API

```python
class GenesisEngine:
    def __init__(
        self,
        profile_name: str,
        persona: str = "shopper",
        age_days: int = 90,
        seed: str = None
    ):
        """
        Initialize Genesis Engine.
        
        Args:
            profile_name: Name for the profile directory
            persona: Browsing pattern (shopper/developer/general)
            age_days: How old the profile should appear
            seed: Random seed for reproducibility
        """
    
    def generate_commerce_cookies(self) -> List[Dict]:
        """Generate commerce trust cookies."""
    
    def generate_browsing_history(self) -> List[Dict]:
        """Generate realistic browsing history."""
    
    def generate_commerce_vault(self) -> Dict:
        """Generate LocalStorage vault data."""
    
    def generate_form_history(self) -> List[Dict]:
        """Generate form autofill history."""
    
    def generate_all(self) -> Dict[str, Any]:
        """Generate all artifacts and save to disk."""
```

### 10.2 Firefox Injector API

```python
class FirefoxInjector:
    def __init__(
        self,
        artifacts_path: Path,
        target_profile: Path = None
    ):
        """
        Initialize Firefox Injector.
        
        Args:
            artifacts_path: Path to Genesis Engine output
            target_profile: Path to Firefox profile (default: artifacts_path)
        """
    
    def inject_cookies(self):
        """Inject cookies into cookies.sqlite."""
    
    def inject_history(self):
        """Inject history into places.sqlite."""
    
    def inject_local_storage(self):
        """Inject LSNG localStorage."""
    
    def inject_form_history(self):
        """Inject form history into formhistory.sqlite."""
    
    def age_profile(self):
        """Backdate profile creation time in times.json."""
    
    def inject_all(self) -> Dict:
        """Perform complete injection pipeline."""
```

### 10.3 Firefox Injector V2 API

```python
class FirefoxProfileInjectorV2:
    def __init__(
        self,
        profile_path: str,
        aging_days: int = 90
    ):
        """
        Initialize V2 injector with LSNG support.
        
        Args:
            profile_path: Path to Firefox profile
            aging_days: Number of days to backdate artifacts
        """
    
    def inject_cookie(self, cookie: CookieEntryV2) -> bool:
        """Inject a single cookie with full schema support."""
    
    def inject_history(self, entry: HistoryEntryV2) -> Optional[int]:
        """Inject history entry with proper url_hash and rev_host."""
    
    def inject_local_storage(self, entry: LocalStorageEntryV2) -> bool:
        """Inject LSNG localStorage with Snappy compression."""
    
    def age_profile(self) -> bool:
        """Backdate profile in times.json."""
    
    def generate_realistic_history(
        self,
        days: int = None,
        persona: str = 'general'
    ) -> int:
        """Generate realistic browsing history."""
```

### 10.4 Utility Functions

```python
# Time conversion
from backend.modules import to_prtime, from_prtime
prtime = to_prtime(datetime.now())  # → 1738766400000000
dt = from_prtime(prtime)            # → datetime object

# URL hash
from backend.modules import mozilla_url_hash
hash_val = mozilla_url_hash("https://google.com")  # → 64-bit int

# Reversed hostname
from backend.modules import generate_rev_host
rev = generate_rev_host("www.google.com")  # → "moc.elgoog.www."

# GUID generation
from backend.modules import generate_firefox_guid
guid = generate_firefox_guid()  # → "a1B2c3D4e5F6"

# Origin sanitization
from backend.modules import sanitize_origin
folder = sanitize_origin("https://stripe.com")  # → "https+++stripe.com"
```

---

## 11. Research Background

### 11.1 Browser Fingerprinting

Browser fingerprinting is a technique used to identify users based on their browser configuration:

**Passive Fingerprinting:**
- User-Agent string
- Accept headers
- Screen resolution
- Timezone

**Active Fingerprinting:**
- Canvas rendering
- WebGL renderer info
- Audio processing
- Font enumeration

**Network Fingerprinting:**
- TLS cipher suites (JA3/JA4)
- HTTP/2 SETTINGS
- IP geolocation

### 11.2 Anti-Fraud Detection Vectors

Modern anti-fraud systems check for:

1. **Temporal Anomalies**
   - Profile created "now" vs 90 days ago
   - Cookie timestamps matching session start
   - Empty history on established account

2. **Behavioral Anomalies**
   - All history entries typed (no link clicks)
   - Linear mouse movements
   - Constant typing speed

3. **Fingerprint Anomalies**
   - Unique canvas hash across sessions
   - Mismatched TLS fingerprint
   - Known VM/automation signatures

### 11.3 Firefox Storage Architecture Research

Based on analysis of Firefox source code and database schemas:

**Key Findings:**
1. Firefox uses PRTime (microseconds) not Unix timestamps
2. URL hash is required for autocomplete functionality
3. rev_host enables efficient subdomain queries
4. LSNG requires .metadata-v2 for Quota Manager validation
5. Snappy compression is optional but recommended

**Reference Materials:**
- `mozilla-central/toolkit/components/places/Database.cpp`
- `mozilla-central/dom/localstorage/ActorsParent.cpp`
- `mozilla-central/netwerk/cookie/CookieStorage.cpp`

---

## 12. Troubleshooting

### 12.1 Common Issues

**Issue: Profile not aging correctly**
```
Symptom: times.json shows current date
Solution: Ensure inject_all() or age_profile() is called
Check: cat lucid_profile_data/Profile/times.json
```

**Issue: Cookies not appearing in browser**
```
Symptom: Browser shows no cookies after injection
Causes:
  1. Profile path mismatch
  2. cookies.sqlite locked by running browser
  3. Missing baseDomain field
Solution: Close browser, verify path, check injection logs
```

**Issue: History autocomplete not working**
```
Symptom: Address bar doesn't suggest injected URLs
Causes:
  1. Invalid url_hash
  2. Missing rev_host
  3. frecency too low
Solution: Verify url_hash calculation, check places.sqlite schema
```

**Issue: LSNG not recognized**
```
Symptom: LocalStorage appears empty
Causes:
  1. Missing .metadata-v2 file
  2. Invalid origin folder name
  3. Corrupted data.sqlite
Solution: Verify directory structure, regenerate metadata files
```

### 12.2 Verification Commands

```bash
# Full system verification
python verify_full_system.py

# Injection verification
python verify_injection.py

# Test production pipeline
python test_production.py

# Check specific database
sqlite3 lucid_profile_data/Profile/cookies.sqlite "SELECT * FROM moz_cookies LIMIT 5"

# Check LSNG structure
ls -la lucid_profile_data/Profile/storage/default/
```

### 12.3 Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with verbose output
python lucid_genesis_engine.py --profile "Debug" --verbose
python lucid_firefox_injector.py --profile "Debug" --verbose
```

---

## Appendix A: File Formats

### A.1 metadata.json
```json
{
  "profile_name": "Titan_Ops_001",
  "profile_uuid": "8f3c47e0-d746-7842-9143-248916cbc298",
  "persona": "shopper",
  "age_days": 90,
  "seed": "reproducible-seed",
  "generated_at": "2026-02-05T14:25:44",
  "created_at": "2025-11-07T14:25:44",
  "version": "5.0.0-TITAN",
  "authority": "Dva.12"
}
```

### A.2 commerce_cookies.json
```json
[
  {
    "name": "__stripe_mid",
    "value": "v3|1699300000000|a1b2c3d4e5f67890",
    "domain": "stripe.com",
    "path": "/",
    "secure": true,
    "httpOnly": false,
    "sameSite": "Lax",
    "created": "2025-11-07T10:00:00",
    "lastAccessed": "2025-12-23T10:00:00"
  }
]
```

### A.3 browsing_history.json
```json
[
  {
    "url": "https://www.amazon.com",
    "title": "Amazon.com: Online Shopping",
    "visit_count": 5,
    "visit_time": "2025-11-15T14:30:00",
    "visit_type": 1,
    "typed": false
  }
]
```

---

## Appendix B: Constants Reference

### B.1 Visit Types
```python
TRANSITION_LINK = 1
TRANSITION_TYPED = 2
TRANSITION_BOOKMARK = 3
TRANSITION_EMBED = 4
TRANSITION_REDIRECT_PERMANENT = 5
TRANSITION_REDIRECT_TEMPORARY = 6
TRANSITION_DOWNLOAD = 7
TRANSITION_FRAMED_LINK = 8
TRANSITION_RELOAD = 9
```

### B.2 SameSite Values
```python
SAMESITE_NONE = 0
SAMESITE_LAX = 1
SAMESITE_STRICT = 2
```

### B.3 PRTime Conversion
```python
# Unix seconds to PRTime
prtime = unix_timestamp * 1_000_000

# PRTime to Unix seconds
unix_timestamp = prtime / 1_000_000

# Milliseconds (times.json) to PRTime
prtime = milliseconds * 1_000
```

---

## Appendix C: Security Considerations

This software is provided for **research and educational purposes only**. 

**Intended Use Cases:**
- Browser fingerprinting research
- Anti-fraud system analysis
- Privacy protection studies
- Browser automation testing

**Not Intended For:**
- Fraudulent activities
- Terms of service violations
- Identity theft
- Any illegal activities

Users are responsible for ensuring compliance with applicable laws and terms of service.

---

**Document End**

*LUCID EMPIRE v5.0.0-TITAN | Authority: Dva.12 | Classification: ZERO DETECT*
