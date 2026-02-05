# 🚀 LUCID EMPIRE - GitHub Codespaces Setup Guide

## Quick Start (One-Click Setup)

### Step 1: Open Terminal in Codespace
Press `` Ctrl+` `` or go to **Terminal → New Terminal**

### Step 2: Run the Installer
```bash
# Make installer executable and run
chmod +x INSTALL_LUCID_LINUX.sh
./INSTALL_LUCID_LINUX.sh
```

**OR** run Python installer directly:
```bash
python3 LUCID_INSTALLER.py --cli
```

---

## Manual Setup (Step-by-Step)

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Camoufox Browser
```bash
pip install camoufox
python -c "from camoufox.sync_api import Camoufox; print('Camoufox OK')"
```

### 4. Install Playwright (Firefox)
```bash
playwright install firefox
```

### 5. Generate Trajectory Model (for biometric mimicry)
```bash
python scripts/generate_trajectory_model.py
```

### 6. Verify Installation
```bash
python verify_capabilities.py
```

---

## Running LUCID Browser in Codespace

### Option A: Headless Mode (Recommended for Codespaces)
```bash
python launch_lucid_browser.py --headless --url "https://example.com"
```

### Option B: With VNC/noVNC (For Visual Mode)
Codespaces supports forwarded ports. If you need visual browser:

```bash
# Install display dependencies
sudo apt-get update
sudo apt-get install -y xvfb

# Run with virtual display
xvfb-run python launch_lucid_browser.py --url "https://example.com"
```

### Option C: API Server Mode
```bash
# Start the API server
python backend/server.py

# API will be available at forwarded port (usually 5000)
```

---

## Codespace-Specific Configuration

### Environment Variables
Create a `.env` file or set in Codespace secrets:
```bash
export LUCID_HEADLESS=true
export LUCID_PROFILE_DIR="./lucid_profile_data"
export LUCID_LOG_LEVEL="INFO"
```

### Port Forwarding
The following ports may need forwarding:
- `5000` - API Server
- `8080` - Dashboard (if running)

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Install all | `./INSTALL_LUCID_LINUX.sh` |
| Activate venv | `source venv/bin/activate` |
| Run browser (headless) | `python launch_lucid_browser.py --headless` |
| Run API server | `python backend/server.py` |
| Verify installation | `python verify_capabilities.py` |
| Generate trajectory | `python scripts/generate_trajectory_model.py` |

---

## Troubleshooting in Codespaces

### Issue: "No module named 'camoufox'"
```bash
pip install camoufox playwright
playwright install firefox
```

### Issue: "Display not available"
```bash
# Use headless mode
python launch_lucid_browser.py --headless
```

### Issue: "Permission denied"
```bash
chmod +x *.sh
chmod +x INSTALL_LUCID_LINUX.sh
```

### Issue: "venv not found"
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Expected Output After Setup

```
============================================================
LUCID EMPIRE - Capability Verification
============================================================
[✓] Camoufox Browser Engine     - PASS
[✓] Firefox Injector            - PASS
[✓] Profile Manager             - PASS
[✓] Biometric Mimicry           - PASS
[✓] Warming Engine              - PASS
[✓] Blacklist Validator         - PASS
[✓] Commerce Injector           - PASS
[✓] Network Stealth             - PASS
[✓] Genesis Engine              - PASS
[✓] Cortex Controller           - PASS
[✓] Time Displacement           - PASS
[✓] Profile Store               - PASS
============================================================
RESULT: 12/12 COMPONENTS OPERATIONAL
STATUS: 100% READY
============================================================
```

---

## File Structure After Installation

```
lucid-empire-new/
├── venv/                    # Python virtual environment
├── assets/models/           # GAN trajectory models
│   └── ghost_motor_v5.pkl
├── lucid_profile_data/      # Browser profiles
├── camoufox/bin/            # Camoufox browser binary
└── logs/                    # Operation logs
```

---

## Support

- **Documentation:** See `docs/` folder
- **API Reference:** See `docs/API_REFERENCE.md`
- **Troubleshooting:** See `docs/TROUBLESHOOTING.md`

---

*LUCID EMPIRE v5.0.0-TITAN | GitHub Codespaces Compatible*
