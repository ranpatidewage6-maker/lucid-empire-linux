# LUCID EMPIRE v5.0.0-TITAN
## One-Click Anti-Detect Browser Installation Guide

---

## 🚀 QUICK START

### Windows
```batch
# Double-click or run:
INSTALL_LUCID_WINDOWS.bat
```

### Linux / macOS
```bash
chmod +x INSTALL_LUCID_LINUX.sh
./INSTALL_LUCID_LINUX.sh
```

### Direct Python (Any OS)
```bash
python LUCID_INSTALLER.py        # GUI mode
python LUCID_INSTALLER.py --cli  # CLI mode
```

---

## 📋 WHAT GETS INSTALLED

| Component | Description |
|-----------|-------------|
| **Python venv** | Isolated Python environment |
| **Camoufox** | Anti-detect Firefox fork with 31 C++ patches |
| **Playwright** | Browser automation framework |
| **Dependencies** | FastAPI, HTTPX, Faker, Pydantic, etc. |
| **Trajectory Model** | GAN-based human mouse movement |
| **Profiles** | Pre-configured browser identities |

---

## 🖥️ SYSTEM REQUIREMENTS

### Windows
- Windows 10 or 11
- Python 3.9+ (from python.org or Microsoft Store)
- 2GB+ free disk space
- Admin rights recommended

### Linux
- Ubuntu 20.04+, Debian 11+, Fedora 35+, Arch
- Python 3.9+ with pip
- python3-tk for GUI mode
- 2GB+ free disk space

### macOS
- macOS 11 (Big Sur) or later
- Python 3.9+ (via Homebrew recommended)
- python-tk for GUI mode
- 2GB+ free disk space

---

## 📦 INSTALLATION PHASES

The installer runs through 6 phases:

1. **SYSTEM CHECK** - Verify OS, Python, disk space
2. **PYTHON ENVIRONMENT** - Create/verify virtual environment
3. **DEPENDENCIES** - Install Python packages from requirements.txt
4. **CAMOUFOX BROWSER** - Download/configure anti-detect browser
5. **ASSETS & MODELS** - Setup trajectory model and profiles
6. **VERIFICATION** - Run final checks

---

## 🌐 LAUNCHING THE BROWSER

After installation, launch the browser with:

```bash
# Basic launch with profile
python launch_lucid_browser.py --profile Titan_SoftwareEng_USA_001

# Launch with target URL (auto-navigate)
python launch_lucid_browser.py --profile Titan_SoftwareEng_USA_001 --url "https://example.com"

# Launch with proxy
python launch_lucid_browser.py --profile Titan_SoftwareEng_USA_001 --proxy "user:pass@host:port"

# List available profiles
python launch_lucid_browser.py --list-profiles

# Headless mode
python launch_lucid_browser.py --profile <name> --headless
```

---

## 📁 FILE STRUCTURE

```
lucid-empire-new/
├── LUCID_INSTALLER.py          # Main GUI/CLI installer
├── INSTALL_LUCID_WINDOWS.bat   # Windows one-click launcher
├── INSTALL_LUCID_LINUX.sh      # Linux/macOS one-click launcher
├── launch_lucid_browser.py     # Browser launcher
├── verify_capabilities.py      # Verification script
├── requirements.txt            # Python dependencies
├── venv/                       # Python virtual environment
├── camoufox/
│   └── bin/
│       └── camoufox-win/       # Browser binary (Windows)
│       └── camoufox-linux/     # Browser binary (Linux)
├── assets/
│   └── models/
│       └── ghost_motor_v5.pkl  # Trajectory model
├── lucid_profile_data/         # Browser profiles
│   ├── Titan_SoftwareEng_USA_001/
│   ├── Titan_Doctor_NY_001/
│   └── ...
└── backend/
    ├── firefox_injector.py     # Cookie/history injection
    ├── warming_engine.py       # Profile warming
    └── ...
```

---

## ✅ VERIFICATION

Run the verification script to confirm all components:

```bash
python verify_capabilities.py
```

Expected output:
```
VERIFICATION SUMMARY: 12/12 COMPONENTS PASS
  [OK] Cookie Domains (315 domains)
  [OK] Biometric Mimicry
  [OK] Genesis Engine
  [OK] Camoufox Binary
  [OK] Trajectory Model
  [OK] Profile Manager
  [OK] Warming Engine
  [OK] Validation Modules
  [OK] Target URL Navigation
  [OK] Platform Launchers
  [OK] Profile Data (11 profiles)
  [OK] Network Stealth

ALL 44 CAPABILITIES VERIFIED OPERATIONAL
LUCID EMPIRE v5.0.0 IS 100% READY FOR PRODUCTION
```

---

## 🔧 TROUBLESHOOTING

### "Python not found"
- Windows: Install from https://python.org or Microsoft Store
- Linux: `sudo apt install python3 python3-pip`
- macOS: `brew install python3`

### "tkinter not available"
- The installer will fall back to CLI mode
- To enable GUI:
  - Ubuntu: `sudo apt install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
  - macOS: `brew install python-tk`

### "Camoufox binary not found"
- Run the installer again - it will download the binary
- Or manually run: `python -c "from camoufox.sync_api import Camoufox"`

### Browser launch fails
1. Check profiles: `python launch_lucid_browser.py --list-profiles`
2. Run verification: `python verify_capabilities.py`
3. Try headless mode: `python launch_lucid_browser.py --profile <name> --headless`

---

## 🛡️ SECURITY FEATURES

- **Canvas Fingerprinting**: Randomized per-profile
- **WebGL Fingerprinting**: Vendor/renderer spoofing
- **WebRTC**: Real IP leak protection
- **Audio Fingerprinting**: Noise injection
- **Timezone**: Synced with proxy location
- **Locale**: Language/region matching
- **Cookie Aging**: 315+ trusted domains pre-baked
- **History Injection**: Realistic browsing patterns
- **Mouse Movement**: GAN-based human trajectories
- **Typing Patterns**: Variable delays and errors

---

## 📞 SUPPORT

For issues or questions, check:
1. [CAPABILITY_VERIFICATION_REPORT.md](CAPABILITY_VERIFICATION_REPORT.md)
2. [docs_LUCID_DESIRED_OUTCOME_DETAILED.md.txt](docs_LUCID_DESIRED_OUTCOME_DETAILED.md.txt)
3. [README.md](README.md)

---

**LUCID EMPIRE v5.0.0-TITAN**  
*Anti-Detect Browser System*  
*100% Operational*
