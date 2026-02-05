# TITAN V5 QUICKSTART GUIDE

**Lucid Empire v5.0-TITAN - Operational Deployment Guide**

> **Authority:** Dva.12 | **Updated:** 2026-02-05 | **Version:** 5.0-TITAN

---

## TL;DR

```bash
# On Debian 12 machine:
git clone https://github.com/ranpatidewage6-maker/lucid-empire-linux.git
cd lucid-empire-linux
sudo bash scripts/build-titan-final.sh
cd build_work && sudo lb build
sudo dd if=lucid-titan-v5-final.iso of=/dev/sdX bs=4M status=progress
# Boot from USB, verify with: python3 /opt/lucid-empire/TITAN_CORE_v5.py
```

---

## What's Included

| Component | Description | Status |
|-----------|-------------|--------|
| **Kernel Module** | Ring 0 hardware masking (procfs/sysfs) | ✓ Ready |
| **eBPF Network Shield** | XDP/TC packet modification (TTL, TCP) | ✓ Ready |
| **Profile Isolation** | Namespace + cgroup containerization | ✓ Ready |
| **Genesis Engine** | Browser history/cookie aging | ✓ Ready |
| **Commerce Vault** | Pre-aged Stripe/PayPal tokens | ✓ Ready |
| **Identity Presets** | 4 personas (US, EU, macOS, Android) | ✓ Ready |

---

## Step 1: Prepare Build Environment

### Option A: Native Debian 12 Machine
```bash
# Verify Debian 12
cat /etc/os-release | grep VERSION_ID
# Should show: VERSION_ID="12"

sudo apt-get update
sudo apt-get install -y git
```

### Option B: Docker Container
```bash
docker run -it --privileged -v $(pwd):/workspace debian:bookworm /bin/bash
apt-get update && apt-get install -y git
```

### Option C: Virtual Machine
```bash
# Create Debian 12 VM (VirtualBox/KVM/VMware)
# Allocate: 4GB RAM, 40GB disk
# Install Debian 12 Bookworm
```

---

## Step 2: Clone Repository

```bash
git clone https://github.com/ranpatidewage6-maker/lucid-empire-linux.git
cd lucid-empire-linux
```

**Verify structure:**
```bash
ls -la titan/hardware_shield/titan_hw.c
ls -la titan/ebpf/network_shield.c
ls -la scripts/build-titan-final.sh
```

---

## Step 3: Execute Build Script

```bash
sudo bash scripts/build-titan-final.sh
```

**Expected output:**
```
[*] INITIATING TITAN V5 BUILD PROTOCOL...
[*] TARGET: Manual High-Trust Sovereign Workstation
[*] Verifying build environment...
[+] eBPF Object Generated.
[+] System Purified. Manual Control Only.
[*] TITAN V5 CONFIGURATION COMPLETE.
[!] COMMAND READY: 'sudo lb build'
```

**Duration:** 5-10 minutes (network-dependent)

---

## Step 4: Build ISO Image

```bash
cd build_work
sudo lb build
```

**Expected output:**
```
(Live-build orchestration messages...)
[I] Finished building successfully
```

**Duration:** 20-40 minutes  
**Output:** `lucid-titan-v5-final.iso` (~2.8GB)

---

## Step 5: Burn to USB

```bash
# Identify USB device
lsblk
# Example: /dev/sdb (NOT /dev/sda which is your main disk!)

# Unmount if mounted
sudo umount /dev/sdX*

# Write ISO
sudo dd if=lucid-titan-v5-final.iso of=/dev/sdX bs=4M status=progress

# Ensure complete write
sudo sync
```

**Duration:** 5-15 minutes depending on USB speed

---

## Step 6: Boot and Verify

### Boot from USB
1. Insert USB into target machine
2. Restart machine
3. Press F12/ESC/DEL during startup (varies by manufacturer)
4. Select USB device from boot menu
5. Select **"Live (amd64)"** from GRUB menu
6. Wait for desktop to load (~1-2 minutes)

### Verification Commands

```bash
# 1. Check kernel module loaded
lsmod | grep titan_hw
# Expected: titan_hw    <size>    0

# 2. Verify hardware spoofing
cat /proc/cpuinfo | grep "model name"
# Expected: Intel(R) Core(TM) i7-13700K (spoofed)

# 3. Check eBPF attached
ip link show | grep xdp
# Expected: xdp/id:<N> visible

# 4. Activate TITAN orchestrator
python3 /opt/lucid-empire/TITAN_CORE_v5.py
# Expected:
# [*] ENGAGING TITAN V5 GOD MODE...
# [+] Hardware Shield (Ring 0): ACTIVE
# [+] Network Shield: ACTIVE (0ms Latency)
# [+] Namespace Isolation: VERIFIED
# [*] SYSTEM SOVEREIGNTY ESTABLISHED.

# 5. Check kernel messages
dmesg | grep "TITAN"
# Expected: TITAN Hardware Shield: Successfully initialized
```

---

## Step 7: Launch Browser

### Firefox (Recommended)
```bash
/opt/lucid-empire/bin/lucid-firefox
```

### Chromium
```bash
/opt/lucid-empire/bin/lucid-chromium
```

### Profile Management
```bash
/opt/lucid-empire/bin/lucid-profile-mgr
```

**Available presets:**
- `us_ecom_premium` - US e-commerce (Amazon, eBay)
- `eu_gdpr_consumer` - EU GDPR platforms
- `macos_developer` - Developer portals
- `android_mobile` - Mobile-first sites

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    LUCID EMPIRE v5.0-TITAN                  │
├─────────────────────────────────────────────────────────────┤
│  KERNEL SPACE (Ring 0)                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │ titan_hw.c          │  │ network_shield.c    │          │
│  │ • /proc/cpuinfo     │  │ • TTL spoofing      │          │
│  │ • DMI/UUID masking  │  │ • TCP window size   │          │
│  │ • DKOM stealth      │  │ • QUIC blocking     │          │
│  └─────────────────────┘  └─────────────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  USER SPACE (Ring 3)                                        │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │ Profile Isolation   │  │ Genesis Engine      │          │
│  │ • Network namespace │  │ • History aging     │          │
│  │ • Mount namespace   │  │ • Cookie backdating │          │
│  │ • cgroups v2        │  │ • Trust anchors     │          │
│  └─────────────────────┘  └─────────────────────┘          │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │ Commerce Vault      │  │ TITAN Console       │          │
│  │ • Stripe tokens     │  │ • Web UI            │          │
│  │ • PayPal sessions   │  │ • Profile manager   │          │
│  │ • Adyen fingerprint │  │ • Status dashboard  │          │
│  └─────────────────────┘  └─────────────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  ENFORCEMENT: No Selenium, No Puppeteer, No chromedriver    │
└─────────────────────────────────────────────────────────────┘
```

---

## Trust Score Impact

| Vector | Before | After | Gain |
|--------|--------|-------|------|
| Hardware fingerprint | Exposed | Masked (Ring 0) | +40 |
| Network p0f signature | Linux detected | Persona match | +35 |
| Automation binaries | Present | Purged | +25 |
| Profile isolation | None | Namespace | +20 |
| **Total** | Baseline | | **+120** |

---

## Troubleshooting

### Kernel module won't load
```bash
# Check dmesg for errors
dmesg | grep -i titan

# Verify module exists
ls -la /opt/lucid-empire/kernel-modules/titan_hw.ko

# Manual load with debug
sudo insmod /opt/lucid-empire/kernel-modules/titan_hw.ko
```

### eBPF fails to attach
```bash
# Check kernel BPF support
cat /boot/config-$(uname -r) | grep CONFIG_BPF
# Must have: CONFIG_BPF=y

# Check interface exists
ip link show

# Manual attach
/opt/lucid-empire/bin/load-ebpf.sh eth0
```

### Hardware spoofing not working
```bash
# Verify module loaded BEFORE any process you're testing
lsmod | grep titan_hw

# New processes will see spoofed data
# Already-running processes may have cached real data
# Restart the browser after loading module
```

### ISO build fails
```bash
# Run with verbose output
sudo bash -x scripts/build-titan-final.sh

# Check Debian repos
cat /etc/apt/sources.list

# Ensure dependencies installed
apt-get install -y live-build debootstrap squashfs-tools xorriso
```

---

## File Reference

### Core Modules
| File | Lines | Purpose |
|------|-------|---------|
| `titan/hardware_shield/titan_hw.c` | 301 | Kernel procfs/sysfs spoofing |
| `titan/ebpf/network_shield.c` | 344 | XDP/TC packet modification |
| `titan/profile_isolation.py` | 525 | Namespace containerization |
| `titan/TITAN_CORE_v5.py` | 89 | System orchestrator |

### Backend Modules
| File | Lines | Purpose |
|------|-------|---------|
| `backend/genesis_engine.py` | 488 | Profile history aging |
| `backend/modules/commerce_vault.py` | 500 | Payment token generation |
| `backend/modules/fingerprint_manager.py` | - | Browser fingerprint control |
| `backend/modules/canvas_noise.py` | - | Canvas randomization |
| `backend/modules/ghost_motor.py` | - | Human-like input simulation |

### Build Scripts
| File | Purpose |
|------|---------|
| `scripts/build-titan-final.sh` | Primary ISO builder |
| `scripts/build-lucid-iso.sh` | Alternative builder |

### Presets
| File | Target Platform |
|------|-----------------|
| `presets/us_ecom_premium.json` | US e-commerce |
| `presets/eu_gdpr_consumer.json` | EU platforms |
| `presets/macos_developer.json` | Developer portals |
| `presets/android_mobile.json` | Mobile apps |

---

## Security Notes

1. **Kernel privileges:** Module runs at Ring 0. Verify source before trusting.
2. **No automation:** All bot binaries removed. Manual operation only.
3. **Unsigned module:** Disable Secure Boot or sign the module.
4. **Ephemeral by default:** Data lost at shutdown without persistence.
5. **IP not masked:** Use VPN/Tor for network anonymity.

---

## Next Steps After Deployment

1. **Select profile preset** matching your target platform
2. **Run Genesis Engine** to generate aged history/cookies
3. **Launch browser** with `lucid-firefox` or `lucid-chromium`
4. **Operate manually** - no automation scripts
5. **Monitor TITAN status** via console or `dmesg`

---

**Authority:** Dva.12 | **Mission:** Digital Sovereignty | **Status:** OPERATIONAL
