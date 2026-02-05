# LUCID EMPIRE v5.0.0-TITAN
## Quick Reference Card

### Genesis Engine
```bash
# Create profile with shopper persona, 90-day aging
python lucid_genesis_engine.py --profile "ProfileName" --persona shopper --age 90

# Options:
#   --profile NAME    Profile name (default: auto-generated)
#   --persona TYPE    shopper | developer | general (default: shopper)
#   --age DAYS        Profile age in days (default: 90)
#   --seed STRING     Random seed for reproducibility
```

### Firefox Injector
```bash
# Inject artifacts into profile
python lucid_firefox_injector.py --profile "ProfileName"
```

### Verification
```bash
# Full system verification (34 tests)
python verify_full_system.py

# Injection verification
python verify_injection.py
```

### TITAN Console (GUI)
```bash
python TITAN_CONSOLE.py
```

---

## Key Paths

| Item | Path |
|------|------|
| Profile Data | `lucid_profile_data/{profile}/` |
| Cookies DB | `lucid_profile_data/{profile}/cookies.sqlite` |
| History DB | `lucid_profile_data/{profile}/places.sqlite` |
| LSNG Storage | `lucid_profile_data/{profile}/storage/default/` |
| Documentation | `COMPLETE_TECHNICAL_DOCUMENTATION.md` |

---

## Timestamp Formats

| Format | Use Case | Example |
|--------|----------|---------|
| Unix (seconds) | Cookie expiry | `1738766400` |
| PRTime (µs) | Firefox timestamps | `1738766400000000` |
| Milliseconds | times.json | `1738766400000` |

Conversion:
- PRTime = Unix × 1,000,000
- Milliseconds = Unix × 1,000

---

## Visit Types

| Type | Value | Description |
|------|-------|-------------|
| LINK | 1 | Clicked a link |
| TYPED | 2 | Typed URL |
| BOOKMARK | 3 | From bookmark |
| EMBED | 4 | Embedded frame |
| REDIRECT_PERM | 5 | 301 redirect |
| REDIRECT_TEMP | 6 | 302 redirect |
| DOWNLOAD | 7 | Download |
| FRAMED_LINK | 8 | Link in frame |
| RELOAD | 9 | Page reload |

Natural distribution: 70% LINK, 20% TYPED, 10% BOOKMARK

---

## Commerce Tokens

| Platform | Cookie | Format |
|----------|--------|--------|
| Stripe | `__stripe_mid` | `v3\|{timestamp_ms}\|{device_hash}` |
| Stripe | `__stripe_sid` | `v2\|{session_hash}\|{timestamp}` |
| Adyen | `_RP_UID` | `{uid}-{timestamp_hex}-{random}` |
| PayPal | `TLTSID` | 32-char SHA-256 hash |

---

## Zero Detect Modules

```python
from backend.modules import (
    CanvasNoiseInjector,      # Canvas fingerprint noise
    GhostMotorGAN,            # Human-like mouse movement
    CommerceVault,            # Trust token generation
    FirefoxProfileInjectorV2, # LSNG injection
)

from backend.network import TLSMasqueradeManager  # JA4/JA3/HTTP2

from backend.validation import PreFlightValidator  # 8-point validation
```

---

*LUCID EMPIRE v5.0.0-TITAN | Authority: Dva.12 | Classification: ZERO DETECT*
