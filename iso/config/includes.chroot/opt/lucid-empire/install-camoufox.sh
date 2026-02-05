#!/bin/bash
# =============================================================================
# LUCID EMPIRE TITAN - Camoufox Browser Installer
# =============================================================================
# Downloads and configures Camoufox with TITAN integration
# =============================================================================

set -e

TITAN_HOME="/opt/lucid-empire"
CAMOUFOX_DIR="${TITAN_HOME}/camoufox"
CAMOUFOX_VERSION="132.0.2-beta.20"
ARCH=$(uname -m)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   LUCID EMPIRE TITAN                                         ║"
echo "║   Camoufox Browser Installer                                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Determine architecture
case "${ARCH}" in
    x86_64|amd64)
        PLATFORM="linux-x86_64"
        ;;
    aarch64|arm64)
        PLATFORM="linux-aarch64"
        ;;
    *)
        echo -e "${RED}[ERROR] Unsupported architecture: ${ARCH}${NC}"
        exit 1
        ;;
esac

echo -e "${CYAN}[*]${NC} Architecture: ${ARCH} (${PLATFORM})"
echo -e "${CYAN}[*]${NC} Target version: ${CAMOUFOX_VERSION}"
echo ""

# Check if already installed
if [[ -d "${CAMOUFOX_DIR}" ]] && [[ -f "${CAMOUFOX_DIR}/camoufox" || -f "${CAMOUFOX_DIR}/firefox" ]]; then
    echo -e "${YELLOW}[*] Camoufox already installed at ${CAMOUFOX_DIR}${NC}"
    read -p "Reinstall? (y/N): " REINSTALL
    if [[ "${REINSTALL,,}" != "y" ]]; then
        echo "[*] Keeping existing installation."
        exit 0
    fi
    echo "[*] Removing existing installation..."
    rm -rf "${CAMOUFOX_DIR}"
fi

# Create directory
mkdir -p "${CAMOUFOX_DIR}"
cd /tmp

# Try to download Camoufox
CAMOUFOX_TAR="camoufox-${CAMOUFOX_VERSION}-${PLATFORM}.tar.gz"
DOWNLOAD_URL="https://github.com/nicgpt/camoufox-portable/releases/download/v${CAMOUFOX_VERSION}/${CAMOUFOX_TAR}"

echo -e "${CYAN}[*]${NC} Attempting to download Camoufox..."
echo "    URL: ${DOWNLOAD_URL}"

if command -v wget &>/dev/null; then
    wget -q --show-progress -O "${CAMOUFOX_TAR}" "${DOWNLOAD_URL}" 2>/dev/null || DOWNLOAD_FAILED=1
elif command -v curl &>/dev/null; then
    curl -L --progress-bar -o "${CAMOUFOX_TAR}" "${DOWNLOAD_URL}" 2>/dev/null || DOWNLOAD_FAILED=1
else
    echo -e "${RED}[ERROR] Neither wget nor curl available${NC}"
    exit 1
fi

# If Camoufox download failed, use Firefox as fallback
if [[ "${DOWNLOAD_FAILED}" == "1" ]] || [[ ! -f "${CAMOUFOX_TAR}" ]] || [[ ! -s "${CAMOUFOX_TAR}" ]]; then
    echo ""
    echo -e "${YELLOW}[*] Camoufox download failed, using Firefox fallback...${NC}"
    
    FIREFOX_VERSION="132.0"
    FIREFOX_URL="https://archive.mozilla.org/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2"
    
    echo -e "${CYAN}[*]${NC} Downloading Firefox ${FIREFOX_VERSION}..."
    
    if command -v wget &>/dev/null; then
        wget -q --show-progress -O firefox.tar.bz2 "${FIREFOX_URL}"
    else
        curl -L --progress-bar -o firefox.tar.bz2 "${FIREFOX_URL}"
    fi
    
    echo -e "${CYAN}[*]${NC} Extracting Firefox..."
    tar -xjf firefox.tar.bz2
    mv firefox/* "${CAMOUFOX_DIR}/"
    rm -rf firefox firefox.tar.bz2
    
    # Create camoufox symlink
    ln -sf "${CAMOUFOX_DIR}/firefox" "${CAMOUFOX_DIR}/camoufox"
else
    echo -e "${CYAN}[*]${NC} Extracting Camoufox..."
    tar -xzf "${CAMOUFOX_TAR}" -C "${CAMOUFOX_DIR}" --strip-components=1 2>/dev/null || \
    tar -xf "${CAMOUFOX_TAR}" -C "${CAMOUFOX_DIR}" --strip-components=1
    rm -f "${CAMOUFOX_TAR}"
fi

# Verify installation
if [[ ! -f "${CAMOUFOX_DIR}/camoufox" ]] && [[ ! -f "${CAMOUFOX_DIR}/firefox" ]]; then
    echo -e "${RED}[ERROR] Installation verification failed${NC}"
    exit 1
fi

# Set permissions
chmod +x "${CAMOUFOX_DIR}/camoufox" 2>/dev/null || true
chmod +x "${CAMOUFOX_DIR}/firefox" 2>/dev/null || true

echo ""
echo -e "${CYAN}[*]${NC} Configuring TITAN browser policies..."

# Create distribution directory
mkdir -p "${CAMOUFOX_DIR}/distribution"

# Create policies.json for anti-fingerprinting defaults
cat > "${CAMOUFOX_DIR}/distribution/policies.json" << 'POLICIES'
{
  "policies": {
    "DisableTelemetry": true,
    "DisableFirefoxStudies": true,
    "DisablePocket": true,
    "DisableFirefoxAccounts": true,
    "DisableFormHistory": false,
    "EnableTrackingProtection": {
      "Value": true,
      "Locked": true,
      "Cryptomining": true,
      "Fingerprinting": false
    },
    "Cookies": {
      "Behavior": "reject-tracker-and-partition-foreign",
      "BehaviorPrivateBrowsing": "reject-tracker-and-partition-foreign"
    },
    "DNSOverHTTPS": {
      "Enabled": false,
      "Locked": true
    },
    "Preferences": {
      "privacy.resistFingerprinting": {
        "Value": false,
        "Status": "locked"
      },
      "dom.webaudio.enabled": {
        "Value": true,
        "Status": "default"
      },
      "webgl.disabled": {
        "Value": false,
        "Status": "default"
      },
      "media.peerconnection.enabled": {
        "Value": true,
        "Status": "default"
      }
    }
  }
}
POLICIES

# Create autoconfig
mkdir -p "${CAMOUFOX_DIR}/defaults/pref"

cat > "${CAMOUFOX_DIR}/defaults/pref/autoconfig.js" << 'AUTOCONFIG'
pref("general.config.filename", "titan-autoconfig.cfg");
pref("general.config.obscure_value", 0);
AUTOCONFIG

cat > "${CAMOUFOX_DIR}/titan-autoconfig.cfg" << 'TITANCONFIG'
// LUCID EMPIRE TITAN Browser Configuration

// Disable automatic updates
lockPref("app.update.enabled", false);
lockPref("browser.search.update", false);

// Performance
pref("network.http.max-connections", 256);
pref("network.http.max-persistent-connections-per-server", 8);

// Disable telemetry
lockPref("toolkit.telemetry.enabled", false);
lockPref("toolkit.telemetry.unified", false);
lockPref("toolkit.telemetry.server", "");
lockPref("datareporting.healthreport.uploadEnabled", false);
lockPref("datareporting.policy.dataSubmissionEnabled", false);

// Disable safe browsing
pref("browser.safebrowsing.malware.enabled", false);
pref("browser.safebrowsing.phishing.enabled", false);
pref("browser.safebrowsing.downloads.enabled", false);

// WebRTC leak prevention defaults
pref("media.peerconnection.ice.default_address_only", true);
pref("media.peerconnection.ice.no_host", true);

// Enable debugging for fingerprint injection
pref("webgl.enable-debug-renderer-info", true);
TITANCONFIG

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            Camoufox Installation Complete                    ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${CYAN}Location:${NC} ${CAMOUFOX_DIR}"
echo -e "  ${CYAN}Binary:${NC}   ${CAMOUFOX_DIR}/camoufox"
echo ""
echo "  Launch via TITAN Console for full anti-detection features."
echo ""
