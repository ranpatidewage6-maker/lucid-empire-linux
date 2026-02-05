#!/bin/bash
# =============================================================================
# LUCID EMPIRE TITAN - Main Launcher (No-Fork Edition)
# =============================================================================
# ARCHITECTURE: Naked Browser Protocol
# - Standard Firefox ESR / Chromium with Hardware Shield
# - No forked browsers - true sovereignty
# =============================================================================

set -e

TITAN_HOME="/opt/lucid-empire"
TITAN_DATA="${HOME}/.lucid-empire"
HARDWARE_SHIELD="${TITAN_HOME}/lib/libhardwareshield.so"
LOG_DIR="${TITAN_DATA}/logs"
VENV_PATH="${TITAN_HOME}/venv"

# Create data directories
mkdir -p "${TITAN_DATA}"/{profiles,logs,cache,commerce_vault}

# Initialize logging
LOG_FILE="${LOG_DIR}/titan-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "=============================================="
echo "  LUCID EMPIRE v5.0-TITAN (No-Fork Edition)"
echo "  Architecture: Naked Browser Protocol"
echo "  Starting Console..."
echo "=============================================="
echo ""
echo "[$(date)] TITAN Console starting..."
echo "[$(date)] Data directory: ${TITAN_DATA}"
echo "[$(date)] Log file: ${LOG_FILE}"

# Check for Hardware Shield
if [[ -f "${HARDWARE_SHIELD}" ]]; then
    echo "[$(date)] Hardware Shield: COMPILED"
else
    echo "[$(date)] WARNING: Hardware Shield not compiled"
    echo "[$(date)] Run: make -C ${TITAN_HOME}/lib"
fi

# Check for eBPF capabilities
if [[ -f /sys/kernel/btf/vmlinux ]]; then
    echo "[$(date)] BTF available - eBPF features enabled"
else
    echo "[$(date)] WARNING: BTF not available, eBPF features may be limited"
fi

# Set environment variables
export TITAN_HOME
export TITAN_DATA
export PYTHONDONTWRITEBYTECODE=1
export QT_AUTO_SCREEN_SCALE_FACTOR=1

# libfaketime setup (activated per-profile)
export FAKETIME_DONT_FAKE_MONOTONIC=1
export FAKETIME_NO_CACHE=1

# Determine Python path
if [[ -d "${VENV_PATH}" ]] && [[ -f "${VENV_PATH}/bin/python3" ]]; then
    PYTHON="${VENV_PATH}/bin/python3"
    echo "[$(date)] Using venv Python: ${PYTHON}"
else
    PYTHON="python3"
    echo "[$(date)] Using system Python: ${PYTHON}"
fi

# Launch TITAN Console
cd "${TITAN_HOME}"
echo "[$(date)] Launching TITAN Console GUI..."
exec "${PYTHON}" TITAN_CONSOLE.py "$@"
