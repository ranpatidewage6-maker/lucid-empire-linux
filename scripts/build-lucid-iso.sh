#!/bin/bash
#
# Lucid Empire v5.0-TITAN - ISO Build System
#
# This script orchestrates the creation of a customized Debian-based live ISO
# integrated with the TITAN architecture components for kernel-level sovereignty.
# It leverages 'live-build' to construct the image and injects custom
# configurations, packages, and kernel-level hooks.
#
# Source: Unified Agent [cite: 1, 26, 27]

set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error.
set -o pipefail # Return the exit status of the last command in the pipe that failed.

# --- Configuration ---
ISO_DIR="$(pwd)/iso"
CONFIG_DIR="${ISO_DIR}/config"
BUILD_DIR="${ISO_DIR}/live-build-tmp"
TITAN_DIR="$(pwd)/titan"
ISO_FILENAME="lucid-empire-titan-v5.0.iso"
DISTRIBUTION="bookworm" # Debian 12
ARCHITECTURE="amd64"

# --- Helper Functions ---

# Log a message to the console with a timestamp.
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [BUILD] :: $1"
}

# Check if the script is running with root privileges.
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        log "This script requires root privileges. Please run with sudo."
        exit 1
    fi
}

# Install necessary build dependencies.
install_dependencies() {
    log "Installing build dependencies..."
    apt-get update
    apt-get install -y live-build debootstrap cdebootstrap
    log "Dependencies installed."
}

# Clean up previous build artifacts.
cleanup() {
    log "Cleaning up previous build artifacts..."
    if [ -d "${BUILD_DIR}" ]; then
        rm -rf "${BUILD_DIR}"
    fi
    # Clean any leftover live-build cache
    lb clean --purge
    log "Cleanup complete."
}

# Configure the live-build environment.
configure_build() {
    log "Configuring live-build environment in ${BUILD_DIR}..."
    mkdir -p "${BUILD_DIR}"
    cd "${BUILD_DIR}"

    lb config noauto \
        --architecture "${ARCHITECTURE}" \
        --distribution "${DISTRIBUTION}" \
        --archive-areas "main contrib non-free non-free-firmware" \
        --debian-installer live \
        --bootappend-live "boot=live components quiet splash" \
        --iso-publisher "Lucid Empire Project" \
        --iso-volume "Lucid Empire v5.0" \
        --memtest none \
        --apt-recommends false \
        --apt-secure true \
        --linux-flavours "amd64" \
        --linux-packages "linux-image" \
        --binary-images iso-hybrid

    log "Live-build configured."
}

# Copy custom configurations into the build directory.
copy_custom_config() {
    log "Copying custom configurations into the build..."

    # Copy package lists
    log "Adding custom package lists..."
    mkdir -p "${BUILD_DIR}/config/package-lists"
    cp "${CONFIG_DIR}/package-lists/custom.list.chroot" "${BUILD_DIR}/config/package-lists/"

    # Copy chroot includes (files to be placed in the ISO's root filesystem)
    log "Adding chroot filesystem includes..."
    mkdir -p "${BUILD_DIR}/config/includes.chroot"
    cp -r "${CONFIG_DIR}/includes.chroot/"* "${BUILD_DIR}/config/includes.chroot/"

    # Copy TITAN framework to /opt/titan in the chroot
    log "Adding TITAN framework components..."
    mkdir -p "${BUILD_DIR}/config/includes.chroot/opt/titan"
    cp -r "${TITAN_DIR}/"* "${BUILD_DIR}/config/includes.chroot/opt/titan/"
    
    # Set executable permissions on Python scripts
    find "${BUILD_DIR}/config/includes.chroot/opt/titan" -name "*.py" -exec chmod +x {} \;

    # Copy live hooks (scripts to be run during the build process)
    log "Adding live build hooks..."
    mkdir -p "${BUILD_DIR}/config/hooks/live"
    cp "${CONFIG_DIR}/hooks/live/"*.hook.chroot "${BUILD_DIR}/config/hooks/live/"
    
    # Ensure hooks are executable
    chmod +x "${BUILD_DIR}/config/hooks/live/"*.hook.chroot

    log "Custom configurations copied."
}

# --- Main Execution ---
main() {
    log "--- Lucid Empire v5.0-TITAN ISO Build System Initialized ---"
    
    check_root
    install_dependencies
    cleanup
    
    # Navigate to the ISO directory to keep build artifacts contained.
    cd "$(dirname "${ISO_DIR}")"

    configure_build
    copy_custom_config

    log "Starting the live-build process... This may take a long time."
    lb build

    log "Build process finished."
    log "Moving generated ISO to the root directory..."
    mv "${BUILD_DIR}/live-image-${ARCHITECTURE}.iso" "${ISO_DIR}/${ISO_FILENAME}"

    log "--- Build Complete ---"
    log "ISO available at: ${ISO_DIR}/${ISO_FILENAME}"
    
    # Final cleanup of the build directory
    cd ..
    rm -rf "${BUILD_DIR}"
}

# --- Script Entry Point ---
main "$@"
