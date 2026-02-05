#!/bin/bash
# =============================================================================
# LUCID EMPIRE TITAN - Main Launcher (No-Fork Edition)
# =============================================================================
# ARCHITECTURE: Naked Browser Protocol
# - Standard Firefox ESR / Chromium with Kernel-Level Hardware Masking
# - No forked browsers - true sovereignty
# - NO LD_PRELOAD - Hardware masking via kernel module (Ring-0)
# =============================================================================

set -e

TITAN_HOME="/opt/lucid-empire"
TITAN_DATA="${HOME}/.lucid-empire"
KERNEL_MODULE="/opt/lucid-empire/kernel-modules/titan_hw.ko"
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
echo "  Hardware Masking: Kernel Module (Ring-0)"
echo "  Starting Console..."
echo "=============================================="
echo ""
echo "[$(date)] TITAN Console starting..."
echo "[$(date)] Data directory: ${TITAN_DATA}"
echo "[$(date)] Log file: ${LOG_FILE}"

# Check for Kernel Module (Hardware Shield v2)
if lsmod | grep -q titan_hw; then
    echo "[$(date)] ✓ Kernel Hardware Masking: ACTIVE"
    echo "[$(date)] ✓ Zero-Detect Protocol: OPERATIONAL"
elif [[ -f "${KERNEL_MODULE}" ]]; then
    echo "[$(date)] ⚠ Kernel Module exists but not loaded"
    echo "[$(date)] Run: sudo systemctl start lucid-titan.service"
else
    echo "[$(date)] ⚠ Kernel Module not found: ${KERNEL_MODULE}"
    echo "[$(date)] Hardware masking may not be active"
fi

# Verify NO LD_PRELOAD (security check)
if [[ -n "${LD_PRELOAD}" ]]; then
    echo "[$(date)] ⚠ WARNING: LD_PRELOAD detected: ${LD_PRELOAD}"
    echo "[$(date)] This may indicate userspace interception (detectable)"
    echo "[$(date)] Kernel module should handle all masking"
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
