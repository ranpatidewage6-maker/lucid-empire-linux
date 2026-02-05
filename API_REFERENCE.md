# 📡 LUCID EMPIRE - API REFERENCE

**Version:** 2.0.0 | **Status:** ✅ 100% OPERATIONAL

## Base URL
```
http://localhost:8000/api
```

## New Endpoints (v2.0.0)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/preflight` | POST | Run 5 pre-flight checks |
| `/api/blacklist-check` | POST | Check IP against blacklists |
| `/api/archive` | POST | Archive profile to ZIP |
| `/api/incinerate` | POST | Secure delete profile |
| `/api/archives` | GET | List archived profiles |
| `/api/warm` | POST | Warm target site |
| `/api/inject` | POST | Inject cookies/history |

---

## Endpoints

### Health Check

#### GET /api/health
Check if the API server is running.

**Request:**
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "operational",
  "version": "5.0.0-TITAN"
}
```

---

### Profile Management

#### GET /api/aged-profiles
List all available aged profiles ready for browser launch.

**Request:**
```bash
curl http://localhost:8000/api/aged-profiles
```

**Response:**
```json
{
  "status": "success",
  "total": 12,
  "profiles": [
    {
      "name": "Titan_SoftwareEng_USA_001",
      "path": "C:/path/to/lucid_profile_data/Titan_SoftwareEng_USA_001",
      "age_days": 90,
      "has_history": true,
      "has_cookies": true,
      "has_commerce": true,
      "has_proxy": true
    },
    {
      "name": "Phantom_Student_130",
      "path": "C:/path/to/lucid_profile_data/Phantom_Student_130",
      "age_days": 90,
      "has_history": true,
      "has_cookies": true,
      "has_commerce": false,
      "has_proxy": true
    }
  ]
}
```

---

#### GET /api/profiles
List all profiles (including non-aged).

**Request:**
```bash
curl http://localhost:8000/api/profiles
```

**Response:**
```json
{
  "status": "success",
  "profiles": [
    {
      "id": "Titan_SoftwareEng_USA_001",
      "name": "Titan_SoftwareEng_USA_001",
      "created_at": "2025-11-05T10:30:00Z"
    }
  ],
  "total": 12
}
```

---

#### GET /api/profiles/{profile_id}
Get details for a specific profile.

**Request:**
```bash
curl http://localhost:8000/api/profiles/Titan_SoftwareEng_USA_001
```

**Response (Success):**
```json
{
  "status": "success",
  "profile": {
    "id": "Titan_SoftwareEng_USA_001",
    "name": "Titan_SoftwareEng_USA_001",
    "path": "C:/path/to/profile",
    "age_days": 90,
    "persona": "worker",
    "created_at": "2025-11-05T10:30:00Z"
  }
}
```

**Response (Not Found):**
```json
{
  "status": "error",
  "message": "Profile not found"
}
```

---

#### POST /api/profiles
Create a new profile.

**Request:**
```bash
curl -X POST http://localhost:8000/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"name": "New_Profile_001", "persona": "student"}'
```

**Response:**
```json
{
  "status": "success",
  "message": "Profile created",
  "profile": {
    "id": "New_Profile_001",
    "name": "New_Profile_001",
    "persona": "student"
  }
}
```

---

#### DELETE /api/profiles/{profile_id}
Delete a profile.

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/profiles/Old_Profile_001
```

**Response:**
```json
{
  "status": "success",
  "message": "Profile deleted"
}
```

---

### Browser Launch

#### POST /api/browser/launch
Launch Camoufox browser with an aged profile.

**Request:**
```bash
curl -X POST http://localhost:8000/api/browser/launch \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "Titan_SoftwareEng_USA_001"}'
```

**Request Body:**
```json
{
  "profile_id": "Titan_SoftwareEng_USA_001",
  "profile_name": "Titan_SoftwareEng_USA_001"  // Optional
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Camoufox browser launched with aged profile: Titan_SoftwareEng_USA_001",
  "url": "https://www.google.com",
  "profile": {
    "id": "Titan_SoftwareEng_USA_001",
    "path": "C:/path/to/lucid_profile_data/Titan_SoftwareEng_USA_001",
    "age_days": 90
  }
}
```

**Response (Profile Not Found):**
```json
{
  "status": "error",
  "message": "Profile not found: invalid_profile_id"
}
```

**Response (Launch Failed):**
```json
{
  "status": "error",
  "message": "Failed to launch browser: [error details]"
}
```

---

## Request/Response Models

### BrowserLaunchRequest
```python
class BrowserLaunchRequest(BaseModel):
    profile_id: str = "Titan_SoftwareEng_USA_001"
    profile_name: Optional[str] = None
```

### ProfileResponse
```python
class ProfileResponse(BaseModel):
    status: str                      # "success" or "error"
    message: Optional[str] = None
    profile: Optional[Dict] = None
    profiles: Optional[List[Dict]] = None
    total: Optional[int] = None
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 404 | Profile not found |
| 500 | Server error |

---

## CORS Configuration

The API allows requests from all origins (development mode):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Starting the API Server

### From Control Panel
Click **START BACKEND API** button.

### From Command Line
```bash
cd "e:\camoufox\New folder\lucid-empire-new"
python -m uvicorn backend.lucid_api:app --reload --port 8000
```

### API Documentation (Swagger)
Once running, access interactive docs at:
```
http://localhost:8000/docs
```

---

**Authority:** Dva.12  
**Last Updated:** February 2, 2026
