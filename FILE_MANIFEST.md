# LUCID EMPIRE v5.0-TITAN - FILE MANIFEST

**Complete Artifact Inventory**

> **Generated:** 2026-02-05 | **Version:** 5.0-TITAN

---

## Repository Statistics

| Metric | Value |
|--------|-------|
| Total Source Files | 50 |
| Core Code Lines | 2,510 |
| Documentation Files | 5 |
| Preset Configurations | 4 |
| Build Scripts | 4 |

---

## Core Modules (`titan/`)

### Kernel Module
| File | Lines | Purpose |
|------|-------|---------|
| `hardware_shield/titan_hw.c` | 301 | Procfs/sysfs spoofing |
| `hardware_shield/Makefile` | 8 | DKMS build rules |
| `hardware_shield/README.md` | - | Module documentation |

### eBPF Network
| File | Lines | Purpose |
|------|-------|---------|
| `ebpf/network_shield.c` | 344 | XDP/TC packet modification |
| `ebpf/network_shield_loader.py` | - | Python BPF loader |
| `ebpf/__init__.py` | - | Package init |

### Python Modules
| File | Lines | Purpose |
|------|-------|---------|
| `TITAN_CORE_v5.py` | 89 | God mode orchestrator |
| `titan_core.py` | - | Legacy core |
| `profile_isolation.py` | 525 | Namespace isolation |
| `temporal_wrapper.py` | - | Temporal stealth |
| `__init__.py` | - | Package init |

---

## ISO Application Layer (`iso/config/includes.chroot/opt/lucid-empire/`)

### Backend
| File | Lines | Purpose |
|------|-------|---------|
| `backend/__init__.py` | - | Package init |
| `backend/genesis_engine.py` | 488 | Profile aging |
| `backend/firefox_injector_v2.py` | - | Firefox injection |
| `backend/handover_protocol.py` | - | Profile handover |
| `backend/zero_detect.py` | - | Detection evasion |

### Backend Modules
| File | Lines | Purpose |
|------|-------|---------|
| `backend/modules/__init__.py` | - | Package init |
| `backend/modules/commerce_vault.py` | 500 | Payment tokens |
| `backend/modules/fingerprint_manager.py` | - | Fingerprint control |
| `backend/modules/canvas_noise.py` | - | Canvas randomization |
| `backend/modules/ghost_motor.py` | - | Human-like input |
| `backend/modules/tls_masquerade.py` | - | TLS spoofing |

### Backend Network
| File | Lines | Purpose |
|------|-------|---------|
| `backend/network/__init__.py` | - | Package init |
| `backend/network/ebpf_loader.py` | - | eBPF management |

### Backend Validation
| File | Lines | Purpose |
|------|-------|---------|
| `backend/validation/__init__.py` | - | Package init |
| `backend/validation/preflight_validator.py` | - | Pre-flight checks |

### Binary Launchers
| File | Purpose |
|------|---------|
| `bin/lucid-firefox` | Firefox with profile |
| `bin/lucid-chromium` | Chromium with profile |
| `bin/lucid-browser` | Generic launcher |
| `bin/lucid-profile-mgr` | Profile manager |
| `bin/lucid-first-boot` | First boot setup |
| `bin/lucid-burn` | USB burning tool |
| `bin/load-ebpf.sh` | eBPF loader (263 lines) |
| `bin/generate-hw-profile.py` | Hardware profile generator |
| `bin/validate-kernel-masking.py` | Kernel validation |

### Console
| File | Purpose |
|------|---------|
| `console/app.py` | Flask web application |
| `console/templates/dashboard.html` | Dashboard UI |

### eBPF
| File | Purpose |
|------|---------|
| `ebpf/tcp_fingerprint.c` | TCP fingerprint eBPF |

### Library
| File | Purpose |
|------|---------|
| `lib/hardware_shield.c` | Legacy user-mode shield |
| `lib/Makefile` | Legacy build rules |

### Main Files
| File | Purpose |
|------|---------|
| `TITAN_CONSOLE.py` | Web console |
| `launch-titan.sh` | Boot script |
| `requirements.txt` | Python deps |

---

## Identity Presets (`iso/config/includes.chroot/opt/lucid-empire/presets/`)

| File | Target | Key Settings |
|------|--------|--------------|
| `us_ecom_premium.json` | US e-commerce | Windows, Chrome, TTL 128 |
| `eu_gdpr_consumer.json` | EU platforms | GDPR compliant |
| `macos_developer.json` | Developer portals | macOS, Safari |
| `android_mobile.json` | Mobile apps | Android, Chrome Mobile |

---

## Profile Storage (`iso/config/includes.chroot/opt/lucid-empire/profiles/`)

| File | Purpose |
|------|---------|
| `active` | Symlink to current profile |
| `default/cpuinfo` | Spoofed CPU info |
| `default/dmi_board_vendor` | Board vendor |
| `default/dmi_product_name` | Product name |
| `default/dmi_product_uuid` | UUID |
| `default/profile.json` | Profile metadata |

---

## Systemd Services (`iso/config/includes.chroot/etc/systemd/system/`)

| File | Purpose |
|------|---------|
| `lucid-titan.service` | Kernel module loader |
| `lucid-ebpf.service` | eBPF attachment |
| `lucid-console.service` | Web console |

---

## Build Scripts (`scripts/`)

| File | Lines | Purpose |
|------|-------|---------|
| `build-titan-final.sh` | 84 | Primary ISO builder |
| `build-lucid-iso.sh` | - | Alternative builder |
| `build-ubuntu-iso.sh` | - | Ubuntu builder (legacy) |
| `build-titan-v5-upgrade.sh` | - | Upgrade script |

---

## Documentation (Root)

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `QUICKSTART.md` | Deployment guide |
| `TECHNICAL_REFERENCE.md` | Technical specs |
| `FILE_MANIFEST.md` | This file |
| `IMPLEMENTATION_STATUS.md` | Status tracking |
| `FINAL_STATUS.md` | Final status |
| `MIGRATION_SUMMARY.md` | Migration notes |
| `TECHNICAL_ANALYSIS_LUCID_TITAN_V5.md` | Architecture analysis |

---

## ISO Build Configuration (`iso/config/`)

| Path | Purpose |
|------|---------|
| `hooks/live/` | Chroot build hooks |
| `includes.chroot/` | ISO filesystem |
| `package-lists/custom.list.chroot` | Package selection |

---

## Chroot Hooks (`iso/config/hooks/live/`)

| File | Purpose |
|------|---------|
| `050-hardware-shield.hook.chroot` | Hardware shield setup |
| `060-kernel-module.hook.chroot` | Kernel module compilation |

---

## Verification Checklist

### Core Modules
- [x] `titan/hardware_shield/titan_hw.c` (301 lines)
- [x] `titan/ebpf/network_shield.c` (344 lines)
- [x] `titan/profile_isolation.py` (525 lines)
- [x] `titan/TITAN_CORE_v5.py` (89 lines)

### Backend
- [x] `genesis_engine.py` (488 lines)
- [x] `commerce_vault.py` (500 lines)
- [x] All module files present

### Build Infrastructure
- [x] `scripts/build-titan-final.sh`
- [x] DKMS configuration
- [x] Systemd services

### Documentation
- [x] README.md
- [x] QUICKSTART.md
- [x] TECHNICAL_REFERENCE.md
- [x] FILE_MANIFEST.md

### Presets
- [x] us_ecom_premium.json
- [x] eu_gdpr_consumer.json
- [x] macos_developer.json
- [x] android_mobile.json

---

**Total Files:** 50+ source/config files  
**Status:** COMPLETE ✓
