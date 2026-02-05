# Firefox Profile Injector v2.0 - LSNG Edition

## Technical Documentation

Based on **Firefox Profile Storage Research Guide** specifications.

---

## Overview

The Firefox Profile Injector v2.0 implements the full Firefox storage architecture as documented in Mozilla's source code. This includes:

- **Mozilla 64-bit URL Hash** - Required for `places.sqlite` indexing
- **rev_host Generation** - Reversed hostnames with trailing dots
- **LSNG (Local Storage Next Generation)** - Modern localStorage format
- **Snappy Compression** - For localStorage values
- **Quota Manager Metadata** - `.metadata-v2` files
- **Visit Type Distribution** - Natural browsing patterns

---

## Core Algorithms

### 1. Mozilla URL Hash

```python
from backend.modules import mozilla_url_hash

url = "https://www.google.com"
hash_value = mozilla_url_hash(url)  # Returns 64-bit signed integer
```

**Implementation**: Uses a variant of DJB2 hash with MurmurHash3 finalization. Without valid hashes, Firefox cannot index or retrieve history entries.

### 2. Reversed Hostname (rev_host)

```python
from backend.modules import generate_rev_host

rev = generate_rev_host("www.google.com")
# Result: "moc.elgoog.www."
```

**Purpose**: Enables efficient B-Tree prefix searches for subdomain queries.

### 3. PRTime Conversion

```python
from backend.modules import to_prtime, from_prtime
from datetime import datetime

# Convert datetime to PRTime (microseconds since epoch)
prtime = to_prtime(datetime.now())

# Convert back
dt = from_prtime(prtime)
```

### 4. GUID Generation

```python
from backend.modules import generate_firefox_guid

guid = generate_firefox_guid()  # 12-char URL-safe Base64
# Example: "2dObCw6Viol1"
```

---

## LSNG Storage

### Origin Sanitization

```python
from backend.modules import sanitize_origin, desanitize_origin

# URL to folder name
folder = sanitize_origin("https://example.com:8080")
# Result: "https+++example.com+8080"

# Folder to URL
url = desanitize_origin(folder)
# Result: "https://example.com:8080"
```

### Directory Structure

```
profile/
└── storage/
    └── default/
        └── https+++example.com/
            ├── .metadata-v2      # Quota Manager metadata
            ├── .metadata         # Legacy metadata
            └── ls/
                ├── data.sqlite   # Key-value storage
                └── usage         # Size tracking
```

### Snappy Compression

```python
from backend.modules import compress_value_snappy

value = "large string data here..."
compressed_blob, compression_type = compress_value_snappy(value)
# compression_type: 0=uncompressed, 1=snappy
```

---

## Usage Examples

### Complete Profile Injection

```python
from backend.modules import FirefoxProfileInjectorV2

# Initialize injector
injector = FirefoxProfileInjectorV2(
    profile_path="C:/Users/.../Profiles/abc123.default-release",
    aging_days=90
)

# Age the profile (sets times.json)
injector.age_profile()

# Generate realistic history with natural visit type distribution
history_count = injector.generate_realistic_history(
    days=90,
    persona='shopper'  # or 'developer', 'general'
)
print(f"Injected {history_count} history entries")
```

### Cookie Injection

```python
from backend.modules import FirefoxProfileInjectorV2, CookieEntryV2

injector = FirefoxProfileInjectorV2(profile_path)

# Create commerce cookie
cookie = CookieEntryV2(
    name='__stripe_mid',
    value='v3|1720000000000|abc123def456',
    host='.stripe.com',
    base_domain='stripe.com',
    path='/',
    secure=True,
    same_site=0,  # 0=None, 1=Lax, 2=Strict
    origin_attributes=''  # For container tabs: ^userContextId=1
)

injector.inject_cookie(cookie)
```

### LocalStorage Injection (LSNG)

```python
from backend.modules import FirefoxProfileInjectorV2, LocalStorageEntryV2

injector = FirefoxProfileInjectorV2(profile_path)

# Inject localStorage with automatic Snappy compression
entry = LocalStorageEntryV2(
    origin='https://stripe.com',
    key='device_id',
    value=json.dumps({'id': 'abc123', 'created': 1720000000})
)

injector.inject_local_storage(entry)
```

### Commerce Cookies Bundle

```python
from backend.modules import create_commerce_cookies_v2

# Generate Stripe, Adyen, PayPal trust cookies
cookies = create_commerce_cookies_v2(
    profile_uuid='unique-profile-id',
    aging_days=90
)

for cookie in cookies:
    injector.inject_cookie(cookie)
```

---

## Visit Type Distribution

The injector uses a natural distribution based on real user behavior:

| Type | Name | Percentage |
|------|------|------------|
| 1 | TRANSITION_LINK | 65% |
| 2 | TRANSITION_TYPED | 15% |
| 3 | TRANSITION_BOOKMARK | 5% |
| 4 | TRANSITION_EMBED | 3% |
| 5 | TRANSITION_REDIRECT_PERMANENT | 4% |
| 6 | TRANSITION_REDIRECT_TEMPORARY | 4% |
| 7 | TRANSITION_DOWNLOAD | 1% |
| 8 | TRANSITION_FRAMED_LINK | 2% |
| 9 | TRANSITION_RELOAD | 1% |

**Critical**: Profiles with 100% `TRANSITION_TYPED` (type 2) are flagged as bot-generated by anti-fraud systems.

---

## Database Schemas

### cookies.sqlite (moz_cookies)

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| baseDomain | TEXT | eTLD+1 (e.g., "google.com") |
| originAttributes | TEXT | Container/partition key |
| name | TEXT | Cookie name |
| value | TEXT | Cookie value |
| host | TEXT | Cookie host (with leading dot) |
| path | TEXT | Cookie path |
| expiry | INTEGER | Unix timestamp (seconds) |
| lastAccessed | INTEGER | PRTime (microseconds) |
| creationTime | INTEGER | PRTime (microseconds) |
| isSecure | INTEGER | HTTPS only flag |
| isHttpOnly | INTEGER | No JS access flag |
| sameSite | INTEGER | 0=None, 1=Lax, 2=Strict |

### places.sqlite (moz_places)

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| url | LONGVARCHAR | Full URL |
| title | LONGVARCHAR | Page title |
| rev_host | LONGVARCHAR | Reversed hostname with dot |
| visit_count | INTEGER | Total visits |
| hidden | INTEGER | Hidden from history |
| typed | INTEGER | User typed this URL |
| frecency | INTEGER | Frequency+Recency score |
| last_visit_date | INTEGER | PRTime |
| guid | TEXT | 12-char unique ID |
| url_hash | INTEGER | Mozilla 64-bit hash |

### LSNG data.sqlite

| Column | Type | Description |
|--------|------|-------------|
| key | TEXT | localStorage key |
| utf16_length | INTEGER | Original value length |
| conversion_type | INTEGER | Character encoding |
| compression_type | INTEGER | 0=raw, 1=snappy |
| value | BLOB | Compressed/raw value |

---

## Dependencies

```
pip install python-snappy  # Optional: for LSNG compression
pip install lz4            # Optional: for sessionstore recovery
```

---

## Integration with TITAN_CONSOLE

```python
from backend.modules import FirefoxProfileInjectorV2

class ProfileFabricator:
    def fabricate_firefox_profile(self, config):
        injector = FirefoxProfileInjectorV2(
            profile_path=config['profile_path'],
            aging_days=config.get('aging_days', 90)
        )
        
        # 1. Age profile
        injector.age_profile()
        
        # 2. Generate history
        injector.generate_realistic_history(
            persona=config.get('persona', 'general')
        )
        
        # 3. Inject commerce cookies
        from backend.modules import create_commerce_cookies_v2
        for cookie in create_commerce_cookies_v2(config['uuid']):
            injector.inject_cookie(cookie)
        
        # 4. Inject localStorage
        injector.inject_local_storage(LocalStorageEntryV2(
            origin='https://stripe.com',
            key='__stripe_deviceId',
            value=config['stripe_device_id']
        ))
```

---

## Version

- **Version**: 2.0.0-LSNG
- **Based on**: Firefox Profile Storage Research Guide
- **Author**: LUCID EMPIRE
- **Module**: `backend/modules/firefox_injector_v2.py`
