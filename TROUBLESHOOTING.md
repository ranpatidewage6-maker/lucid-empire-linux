# 🔧 LUCID EMPIRE - TROUBLESHOOTING GUIDE

**Version:** 2.0.0 | **Status:** ✅ 100% OPERATIONAL

## Common Issues and Solutions

---

### Installation Issues

#### "Python not detected"
**Cause:** Python is not installed or not in PATH.

**Solution:**
1. Download Python 3.10+ from [python.org](https://python.org)
2. During installation, check ✅ "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

---

#### "PyQt6 not installed"
**Cause:** GUI framework not installed.

**Solution:**
```powershell
pip install PyQt6 requests
```

---

#### "pip install fails"
**Cause:** Network issues or permission problems.

**Solutions:**
```powershell
# Try with --user flag
pip install --user -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

#### "Playwright browsers not installed"
**Cause:** Browser binaries not downloaded.

**Solution:**
```powershell
python -m playwright install
```

---

### Control Panel Issues

#### Control Panel won't start
**Cause:** Missing dependencies or Python errors.

**Solutions:**
1. Check Python version: `python --version` (need 3.10+)
2. Install dependencies: `pip install PyQt6 requests`
3. Run directly to see errors:
   ```powershell
   python lucid_control_panel.py
   ```

---

#### "No profiles found"
**Cause:** Profile directory empty or doesn't exist.

**Solutions:**
1. Check if `lucid_profile_data/` exists
2. Generate a new profile using the control panel
3. Click "REFRESH PROFILES" button

---

#### Profile dropdown is empty
**Cause:** Backend not running or profiles not loaded.

**Solutions:**
1. Click "REFRESH PROFILES"
2. Click "START BACKEND API" then refresh
3. Generate a new profile

---

### Browser Launch Issues

#### "Profile not found" error
**Cause:** Selected profile doesn't exist on disk.

**Solutions:**
1. Check profile exists in `lucid_profile_data/`
2. Verify profile name spelling
3. Generate a new profile
4. Refresh profile list

---

#### Camoufox won't launch
**Cause:** Playwright browsers not installed or Camoufox module missing.

**Solutions:**
1. Install Playwright browsers:
   ```powershell
   python -m playwright install
   ```
2. Click "INSTALL DEPENDENCIES" in control panel
3. Check for errors in system log

---

#### Browser launches but closes immediately
**Cause:** Profile corruption or missing files.

**Solutions:**
1. Generate a fresh profile
2. Delete corrupted profile folder
3. Check system log for specific errors

---

#### "Failed to launch Firefox" error
**Cause:** Fallback browser not available.

**Solutions:**
1. Install Firefox browser
2. Ensure Playwright is installed
3. Run: `python -m playwright install firefox`

---

### Backend API Issues

#### "Backend not responding"
**Cause:** API server not running.

**Solutions:**
1. Click "START BACKEND API" in control panel
2. Or run manually:
   ```powershell
   python -m uvicorn backend.lucid_api:app --port 8000
   ```

---

#### "Connection refused" errors
**Cause:** Backend not started or wrong port.

**Solutions:**
1. Ensure backend is running on port 8000
2. Check firewall settings
3. Verify no other service using port 8000

---

#### API returns 500 errors
**Cause:** Backend code error.

**Solutions:**
1. Check terminal for Python traceback
2. Ensure all dependencies installed
3. Run verification: `python verify_integration.py`

---

### Profile Generation Issues

#### Profile generation hangs
**Cause:** Long-running operation or network issues.

**Solutions:**
1. Wait for completion (can take 30+ seconds)
2. Check system log for progress
3. Cancel and retry

---

#### Generated profile is empty
**Cause:** Generation failed silently.

**Solutions:**
1. Check `lucid_profile_data/[profile_name]/` for files
2. Look for `profile_metadata.json`
3. Regenerate the profile

---

### Import Errors

#### "ModuleNotFoundError: No module named 'backend'"
**Cause:** Running from wrong directory.

**Solution:**
Run from project root:
```powershell
cd "e:\camoufox\New folder\lucid-empire-new"
python -m uvicorn backend.lucid_api:app --port 8000
```

---

#### "ModuleNotFoundError: No module named 'camoufox'"
**Cause:** Camoufox library not in path.

**Solution:**
The control panel automatically adds the path. If running manually:
```python
import sys
sys.path.append("./camoufox/pythonlib")
from camoufox.sync_api import Camoufox
```

---

### Virtual Environment Issues

#### "venv not found"
**Cause:** Virtual environment not created.

**Solution:**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

#### Dependencies not found after install
**Cause:** Not using virtual environment.

**Solution:**
```powershell
# Activate venv first
.\venv\Scripts\activate

# Then run
python lucid_control_panel.py
```

---

## Diagnostic Commands

### Check Python
```powershell
python --version
# Expected: Python 3.10.x or higher
```

### Check pip packages
```powershell
pip list | findstr "PyQt6 fastapi playwright"
```

### Check Node.js (optional)
```powershell
node --version
npm --version
```

### Run verification script
```powershell
python verify_integration.py
```

### Check profile directory
```powershell
dir lucid_profile_data
```

### Test API manually
```powershell
curl http://localhost:8000/api/health
```

---

## Log Locations

| Component | Log Location |
|-----------|--------------|
| Control Panel | Displayed in GUI "SYSTEM LOG" |
| Backend API | Terminal/console output |
| Browser | Camoufox developer console |

---

## Reset Procedures

### Reset Control Panel
1. Close the control panel
2. Delete `__pycache__` folders
3. Restart: `python lucid_control_panel.py`

### Reset Virtual Environment
```powershell
# Delete old venv
rmdir /s /q venv

# Create fresh venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Reset Profile Data
```powershell
# Backup first!
# Then delete specific profile
rmdir /s /q "lucid_profile_data\[profile_name]"
```

---

## Getting Help

1. **Check System Log** - Most errors appear in the GUI log
2. **Run Verification** - `python verify_integration.py`
3. **Check Terminal** - Run commands manually to see full errors
4. **Review Documentation** - See other docs in `docs/` folder

---

**Authority:** Dva.12  
**Last Updated:** February 2, 2026
