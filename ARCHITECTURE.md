# 🏗️ LUCID EMPIRE - SYSTEM ARCHITECTURE

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LUCID EMPIRE v5.0 TITAN                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 USER INTERFACE LAYER                       │  │
│  │                                                           │  │
│  │  ┌─────────────────────┐    ┌─────────────────────────┐   │  │
│  │  │  Control Panel      │    │  React Dashboard        │   │  │
│  │  │  (PyQt6)            │    │  (Optional)             │   │  │
│  │  │  - Profile Select   │    │  - Web-based UI         │   │  │
│  │  │  - Profile Generate │    │  - Advanced features    │   │  │
│  │  │  - Browser Launch   │    │  - Real-time logs       │   │  │
│  │  └─────────────────────┘    └─────────────────────────┘   │  │
│  │            │                          │                   │  │
│  └────────────┼──────────────────────────┼───────────────────┘  │
│               │                          │                      │
│               ▼                          ▼                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    API LAYER (FastAPI)                     │  │
│  │                                                           │  │
│  │  Endpoints:                                               │  │
│  │  ├─ GET  /api/health           Health check              │  │
│  │  ├─ GET  /api/aged-profiles    List profiles             │  │
│  │  ├─ POST /api/browser/launch   Launch Camoufox           │  │
│  │  ├─ GET  /api/profiles         Profile management        │  │
│  │  └─ POST /api/profiles         Create profile            │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│               │                                                 │
│               ▼                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    CORE MODULES                            │  │
│  │                                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ Genesis     │  │ Commerce    │  │ Biometric   │       │  │
│  │  │ Engine      │  │ Injector    │  │ Mimicry     │       │  │
│  │  │             │  │             │  │             │       │  │
│  │  │ 90-day      │  │ Trust       │  │ Human-like  │       │  │
│  │  │ aging       │  │ anchors     │  │ behavior    │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  │                                                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ Profile     │  │ Time        │  │ eBPF        │       │  │
│  │  │ Store       │  │ Displacement│  │ Network     │       │  │
│  │  │             │  │             │  │ Shield      │       │  │
│  │  │ Filesystem  │  │ libfaketime │  │ Kernel-     │       │  │
│  │  │ management  │  │ integration │  │ level mask  │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│               │                                                 │
│               ▼                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 BROWSER LAYER (Camoufox)                   │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Camoufox Browser (Firefox Fork)                    │  │  │
│  │  │                                                     │  │  │
│  │  │  Anti-Fingerprinting:                               │  │  │
│  │  │  ├─ Hardware masking (GPU, CPU, WebGL)              │  │  │
│  │  │  ├─ Canvas fingerprint protection                   │  │  │
│  │  │  ├─ Audio context noise                             │  │  │
│  │  │  ├─ Timezone spoofing                               │  │  │
│  │  │  └─ WebRTC leak protection                          │  │  │
│  │  │                                                     │  │  │
│  │  │  Profile Loading:                                   │  │  │
│  │  │  ├─ persistent_context=True                         │  │  │
│  │  │  ├─ user_data_dir=profile_path                      │  │  │
│  │  │  └─ Full history/cookies/commerce loaded            │  │  │
│  │  │                                                     │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│               │                                                 │
│               ▼                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 DATA LAYER (Filesystem)                    │  │
│  │                                                           │  │
│  │  lucid_profile_data/                                      │  │
│  │  ├── Titan_SoftwareEng_USA_001/                          │  │
│  │  │   ├── prefs.js              (Firefox preferences)     │  │
│  │  │   ├── places.sqlite         (History database)        │  │
│  │  │   ├── cookies.sqlite        (Cookie storage)          │  │
│  │  │   ├── formhistory.sqlite    (Autofill data)          │  │
│  │  │   ├── commerce_vault.json   (Payment tokens)          │  │
│  │  │   └── profile_metadata.json (Profile info)            │  │
│  │  ├── Phantom_Student_130/                                │  │
│  │  └── ... (more profiles)                                 │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. User Interface Layer

#### Control Panel (Primary)
- **Technology:** PyQt6
- **File:** `lucid_control_panel.py` (1008 lines)
- **Purpose:** Self-contained GUI for all operations
- **Features:**
  - Profile selection dropdown
  - Profile generation form
  - Browser launch button
  - System log display
  - Dependency installation

#### Platform-Specific Control Panels
- **Windows:** `platforms/windows/lucid_control_panel_windows.py`
- **Linux:** `platforms/linux/lucid_control_panel_linux.py`

#### React Dashboard
- **Technology:** React 18 + Vite + Tailwind
- **Directory:** `frontend/`
- **Purpose:** Web-based primary interface
- **Features:**
  - PreFlightPanel with 5 status indicators
  - Real-time API polling
  - Profile generation wizard
  - Launch orchestration

#### Dashboard (Alternative)
- **Directory:** `dashboard/`
- **Files:** `app.py` (CustomTkinter), `main.py` (CLI)
- **Purpose:** Alternative GUI interfaces

---

### 2. API Layer

#### FastAPI Server
- **File:** `backend/server.py` (817 lines)
- **Port:** 8000
- **Purpose:** RESTful API for all backend operations

#### Key Endpoints
| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/api/health` | GET | Health check |
| `/api/generate` | POST | Generate profile |
| `/api/launch` | POST | Launch browser |
| `/api/preflight` | POST | Run 5 pre-flight checks |
| `/api/blacklist-check` | POST | Check IP reputation |
| `/api/archive` | POST | Archive profile to ZIP |
| `/api/incinerate` | POST | Secure delete profile |
| `/api/archives` | GET | List archived profiles |
| `/api/warm` | POST | Warm target site |
| `/api/inject` | POST | Inject cookies/history |

#### Request Flow
```
React Dashboard → HTTP Request → FastAPI → Core Modules → Response
```

---

### 3. Core Modules

#### Genesis Engine
- **File:** `backend/core/genesis_engine.py`
- **Lines:** 385
- **Purpose:** 90-day profile aging simulation

**Phases:**
1. INCEPTION (T-90d) - Trust anchor establishment
2. WARMING (T-60d) - Browsing history generation
3. KILL_CHAIN (T-30d) - Commerce injection
4. FINALIZE (T-0d) - Profile sealing

#### Commerce Injector
- **File:** `modules/commerce_injector.py`
- **Lines:** 84
- **Purpose:** Trust anchor and payment token injection

**Platforms:**
- Shopify payment injection
- Stripe token injection
- Custom domain handlers

#### Biometric Mimicry
- **File:** `modules/biometric_mimicry.py`
- **Lines:** 400+
- **Purpose:** Human-like browsing behavior

**Functions:**
- `human_scroll()` - Variable speed scrolling
- `human_mouse_move()` - Bézier curve trajectories
- `human_type()` - Keystroke latency (80-150ms)
- `human_click()` - Click duration variance

#### Profile Store
- **File:** `backend/core/profile_store.py`
- **Purpose:** Profile creation and filesystem management

**Classes:**
- `ProfileFactory` - Deterministic hardware generation
- `ProfileStore` - Filesystem operations
- `PersonaFactory` - Persona derivation logic

#### Time Displacement
- **File:** `backend/core/time_displacement.py`
- **Purpose:** libfaketime integration for temporal manipulation

**Features:**
- Unix timestamp manipulation
- JavaScript Date() hijacking
- Geo-matched timezone sync

#### eBPF Network Shield
- **File:** `backend/network/ebpf_loader.py`
- **Purpose:** Kernel-level network masking (Linux only)

**Features:**
- TTL spoofing (Windows = 128)
- Window size manipulation
- Outbound packet rewriting

#### Firefox Profile Injector (NEW v2.0.0)
- **File:** `backend/firefox_injector.py` (917 lines)
- **Purpose:** SQLite injection for Firefox profiles

**Features:**
- Cookie injection (cookies.sqlite)
- History injection (places.sqlite)
- Form history injection (formhistory.sqlite)
- localStorage vault injection

#### Blacklist Validator (NEW v2.0.0)
- **File:** `backend/blacklist_validator.py` (352 lines)
- **Purpose:** IP reputation checking

**Features:**
- DNSBL checking (Spamhaus, SpamCop, etc.)
- AbuseIPDB integration (optional API key)
- Datacenter ASN detection
- Risk score calculation

#### Profile Manager (NEW v2.0.0)
- **File:** `backend/profile_manager.py` (507 lines)
- **Purpose:** Profile lifecycle management

**Features:**
- ZIP archival with manifest
- Secure 3-pass deletion
- Archive listing and restoration

#### Target Warming Engine (NEW v2.0.0)
- **File:** `backend/warming_engine.py` (469 lines)
- **Purpose:** Automated target site warming

**Features:**
- Playwright browser automation
- Synthetic history fallback
- Cart abandonment simulation
- Visit pattern generation

#### Forensic Validator (NEW v2.0.0)
- **File:** `backend/validation/forensic_validator.py`
- **Purpose:** Profile forensic validation

**Features:**
- Browser fingerprint validation
- Profile integrity checking
- Consistency verification

---

### 4. Browser Layer

#### Camoufox Integration
- **Library:** `camoufox/pythonlib/camoufox/`
- **Purpose:** Anti-detect browser automation

**Launch Configuration:**
```python
Camoufox(
    persistent_context=True,      # Use profile directory
    user_data_dir=profile_path,   # Aged profile path
    headless=False,               # Visible browser
    humanize=True,                # Human-like behavior
    geoip=True,                   # Geo-matched fingerprint
)
```

**Anti-Fingerprinting Features:**
- Hardware masking (GPU, CPU, WebGL)
- Canvas fingerprint randomization
- Audio context noise injection
- Timezone spoofing
- WebRTC leak protection
- Font fingerprint masking

---

### 5. Data Layer

#### Profile Storage Structure
```
lucid_profile_data/
└── [Profile_Name]/
    ├── prefs.js                 # Firefox preferences (217+)
    ├── places.sqlite            # History database (300+ entries)
    ├── cookies.sqlite           # Cookie storage (86+ cookies)
    ├── formhistory.sqlite       # Autofill data
    ├── commerce_vault.json      # Payment trust tokens
    ├── profile_metadata.json    # Profile info
    ├── extensions/              # Browser extensions
    ├── storage/                 # DOM storage
    │   ├── default/
    │   └── permanent/
    ├── startupCache/            # Cached resources
    └── ...
```

---

## Data Flow

### Profile Generation Flow
```
User Input (name, persona, age)
         ↓
Control Panel validates input
         ↓
Genesis Engine starts
         ↓
Phase 1: INCEPTION (trust anchors)
         ↓
Phase 2: WARMING (browsing history)
         ↓
Phase 3: COMMERCE (payment tokens)
         ↓
Phase 4: FINALIZE (metadata)
         ↓
Profile saved to lucid_profile_data/
         ↓
Profile appears in dropdown
```

### Browser Launch Flow
```
User selects profile
         ↓
User clicks [ ENTER OBLIVION ]
         ↓
Control Panel calls API
POST /api/browser/launch
         ↓
Backend validates profile exists
         ↓
Backend loads Camoufox with:
- persistent_context=True
- user_data_dir=profile_path
         ↓
Camoufox browser opens
         ↓
Profile data loaded:
- History accessible
- Cookies active
- Commerce tokens ready
         ↓
User has FULL MANUAL CONTROL
```

---

## Threading Model

### Control Panel (Main Thread)
- PyQt6 event loop
- UI updates
- User interaction

### Worker Threads
- Profile generation
- Browser launch
- API calls
- Long-running operations

### Backend (Separate Process)
- FastAPI server
- API request handling
- Profile management

### Browser (Daemon Thread)
- Camoufox instance
- Runs independently
- User controls directly

---

## Security Architecture

### Local-First Design
- All data stored locally
- No cloud synchronization
- No external data transmission

### Profile Isolation
- Each profile in separate directory
- No cross-profile data leakage
- Independent cookie stores

### Hardware Masking
- GPU fingerprint spoofing
- CPU information masking
- WebGL parameter randomization

### Network Protection
- WebRTC leak prevention
- Proxy configuration support
- eBPF kernel-level masking (Linux)

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| GUI | PyQt6 |
| Web UI | React 18 + Vite + Tailwind |
| API | FastAPI + Uvicorn |
| Browser | Camoufox (Firefox fork) |
| Automation | Playwright |
| Database | SQLite (Firefox format) |
| Language | Python 3.10+ |

---

**Authority:** Dva.12  
**Last Updated:** February 2, 2026
