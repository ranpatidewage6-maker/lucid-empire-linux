#!/usr/bin/env bash
#===============================================================================
#  LUCID EMPIRE TITAN - Custom Linux ISO Builder
#  Version: 5.0-TITAN
#  
#  Builds a customized Ubuntu-based live ISO with:
#    - TITAN Anti-Detection Console
#    - eBPF/XDP network stack manipulation
#    - Camoufox browser integration
#    - Pre-configured privacy and security hardening
#===============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT="$SCRIPT_DIR/.."
WORKDIR="$PROJECT_ROOT/iso"
BUILD_LOG="$PROJECT_ROOT/build-$(date +%Y%m%d-%H%M%S).log"

# TITAN Build Configuration
TITAN_VERSION="5.0-TITAN"
ISO_NAME="lucid-empire-titan"
ISO_PUBLISHER="LUCID EMPIRE"
ISO_VOLUME="LUCID_TITAN"

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║   ██╗     ██╗   ██╗ ██████╗██╗██████╗                       ║"
    echo "║   ██║     ██║   ██║██╔════╝██║██╔══██╗                      ║"
    echo "║   ██║     ██║   ██║██║     ██║██║  ██║                      ║"
    echo "║   ██║     ██║   ██║██║     ██║██║  ██║                      ║"
    echo "║   ███████╗╚██████╔╝╚██████╗██║██████╔╝                      ║"
    echo "║   ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═════╝                       ║"
    echo "║                                                              ║"
    echo "║   ███████╗███╗   ███╗██████╗ ██╗██████╗ ███████╗            ║"
    echo "║   ██╔════╝████╗ ████║██╔══██╗██║██╔══██╗██╔════╝            ║"
    echo "║   █████╗  ██╔████╔██║██████╔╝██║██████╔╝█████╗              ║"
    echo "║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║██╔══██╗██╔══╝              ║"
    echo "║   ███████╗██║ ╚═╝ ██║██║     ██║██║  ██║███████╗            ║"
    echo "║   ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝            ║"
    echo "║                                                              ║"
    echo "║                    T I T A N   v${TITAN_VERSION}                        ║"
    echo "║                  Custom Linux ISO Builder                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$BUILD_LOG"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[WARNING] $1" >> "$BUILD_LOG"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    echo "[ERROR] $1" >> "$BUILD_LOG"
}

require_cmd() {
    if ! command -v "$1" >/dev/null 2>&1; then
        error "Missing required command: $1"
        exit 1
    fi
}

check_dependencies() {
    log "Checking build dependencies..."
    local deps=(lb debootstrap mksquashfs xorriso)
    local missing=()
    
    for cmd in "${deps[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing+=("$cmd")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing dependencies: ${missing[*]}"
        echo "Install with: sudo apt install live-build squashfs-tools xorriso debootstrap"
        exit 1
    fi
    
    log "All dependencies satisfied"
}

prepare_titan_files() {
    log "Preparing TITAN components..."
    
    local titan_dir="$WORKDIR/config/includes.chroot/opt/lucid-empire"
    
    # Set executable permissions on scripts
    if [[ -f "$titan_dir/launch-titan.sh" ]]; then
        chmod +x "$titan_dir/launch-titan.sh"
        log "  - Set executable: launch-titan.sh"
    fi
    
    if [[ -f "$titan_dir/install-camoufox.sh" ]]; then
        chmod +x "$titan_dir/install-camoufox.sh"
        log "  - Set executable: install-camoufox.sh"
    fi
    
    # Set executable permissions on hooks
    local hooks_dir="$WORKDIR/config/hooks/live"
    if [[ -d "$hooks_dir" ]]; then
        find "$hooks_dir" -type f -name "*.hook.chroot" -exec chmod +x {} \;
        log "  - Set executable on all hooks"
    fi
    
    # Verify core files exist
    local required_files=(
        "$titan_dir/TITAN_CONSOLE.py"
        "$titan_dir/backend/__init__.py"
        "$titan_dir/backend/zero_detect.py"
        "$titan_dir/backend/genesis_engine.py"
        "$titan_dir/backend/firefox_injector_v2.py"
        "$titan_dir/requirements.txt"
    )
    
    for f in "${required_files[@]}"; do
        if [[ ! -f "$f" ]]; then
            warn "Missing expected file: $f"
        fi
    done
    
    log "TITAN components prepared"
}

create_titan_hook() {
    log "Creating TITAN setup hook..."
    
    local hook_file="$WORKDIR/config/hooks/live/099-titan-finalize.hook.chroot"
    
    cat > "$hook_file" << 'HOOKEOF'
#!/bin/bash
# LUCID EMPIRE TITAN - Final Setup Hook
# This runs inside the chroot during ISO build

set -e

echo "[TITAN] Running final setup..."

TITAN_HOME="/opt/lucid-empire"

# Install Python dependencies
if [[ -f "${TITAN_HOME}/requirements.txt" ]]; then
    echo "[TITAN] Installing Python dependencies..."
    pip3 install --no-cache-dir -r "${TITAN_HOME}/requirements.txt" || {
        echo "[TITAN] Warning: Some Python packages failed to install"
    }
fi

# Set permissions
chmod +x "${TITAN_HOME}/launch-titan.sh" 2>/dev/null || true
chmod +x "${TITAN_HOME}/install-camoufox.sh" 2>/dev/null || true

# Create user data directory structure
mkdir -p /etc/skel/.lucid-empire/{profiles,logs,cache,commerce_vault}

# Update desktop database
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database /usr/share/applications/ 2>/dev/null || true
fi

# Enable BPF JIT (already in sysctl, but ensure it's loaded)
echo "kernel.unprivileged_bpf_disabled=0" >> /etc/sysctl.d/99-titan-bpf.conf
echo "net.core.bpf_jit_enable=1" >> /etc/sysctl.d/99-titan-bpf.conf

# Create TITAN version file
echo "TITAN_VERSION=5.0-TITAN" > "${TITAN_HOME}/VERSION"
echo "BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "${TITAN_HOME}/VERSION"

echo "[TITAN] Setup complete"
HOOKEOF

    chmod +x "$hook_file"
    log "Created finalization hook"
}

print_banner

if [[ $EUID -ne 0 ]]; then
    error "Please run as root (use sudo)."
    exit 1
fi

check_dependencies

log "Starting TITAN ISO build..."
log "Build log: $BUILD_LOG"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [[ "${CLEAN:-0}" == "1" ]]; then
    log "Cleaning previous build..."
    lb clean --purge
fi

prepare_titan_files
create_titan_hook

log "Configuring live-build..."

lb config \
    --distribution noble \
    --archive-areas "main restricted universe multiverse" \
    --binary-images iso-hybrid \
    --linux-packages linux-generic \
    --debootstrap-options "--variant=minbase" \
    --bootappend-live "boot=live components quiet splash" \
    --iso-application "LUCID EMPIRE TITAN" \
    --iso-publisher "${ISO_PUBLISHER}" \
    --iso-volume "${ISO_VOLUME}" \
    --image-name "${ISO_NAME}"

log "Building ISO (this may take 30-60 minutes)..."
log "You can monitor progress in: $BUILD_LOG"

lb build 2>&1 | tee -a "$BUILD_LOG"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    BUILD COMPLETE                            ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
log "ISO Location: $WORKDIR/${ISO_NAME}-amd64.hybrid.iso"
log "Build log: $BUILD_LOG"
echo ""
echo -e "${CYAN}To test the ISO:${NC}"
echo "  qemu-system-x86_64 -m 4096 -cdrom ${ISO_NAME}-amd64.hybrid.iso -boot d"
echo ""
echo -e "${CYAN}To write to USB:${NC}"
echo "  sudo dd if=${ISO_NAME}-amd64.hybrid.iso of=/dev/sdX bs=4M status=progress"
echo ""
