#!/bin/bash
# ==============================================================================
# LUCID EMPIRE TITAN V5 - FINAL ISO BUILDER
# AUTHORITY: Dva.12 | TARGET: DEBIAN 12 BOOKWORM
# ==============================================================================

set -e

# Configuration
ISO_NAME="lucid-titan-v5-final.iso"
WORK_DIR="./build_work"
ISO_DIR="./iso_source"
TITAN_CORE="./titan"

echo "[*] INITIATING TITAN V5 BUILD PROTOCOL..."
echo "[*] TARGET: Manual High-Trust Sovereign Workstation"

# 1. Dependency Check
echo "[*] Verifying build environment..."
apt-get update && apt-get install -y \
    live-build \
    debootstrap \
    squashfs-tools \
    xorriso \
    linux-headers-$(uname -r) \
    clang \
    llvm \
    libbpf-dev \
    python3-dev

# 2. Compile Network Shield (eBPF)
echo "[*] Compiling Network Shield (eBPF)..."
if [ -f "$TITAN_CORE/ebpf/network_shield.c" ]; then
    clang -O2 -target bpf -c "$TITAN_CORE/ebpf/network_shield.c" -o "$ISO_DIR/opt/lucid-empire/ebpf/network_shield.o"
    echo "[+] eBPF Object Generated."
else
    echo "[!] CRITICAL: Network Shield source missing!"
    exit 1
fi

# 3. Compile Hardware Shield (Kernel Module)
echo "[*] Compiling Hardware Shield (Kernel Module)..."
# We need to compile this inside the chroot during the actual build, 
# or pre-compile if the kernel matches. For this script, we setup the source for DKMS.
mkdir -p "$ISO_DIR/usr/src/titan-hw-5.0.1"
cp "$TITAN_CORE/hardware_shield/titan_hw.c" "$ISO_DIR/usr/src/titan-hw-5.0.1/"
cp "$TITAN_CORE/hardware_shield/Makefile" "$ISO_DIR/usr/src/titan-hw-5.0.1/"

# Create DKMS config
cat <<EOF > "$ISO_DIR/usr/src/titan-hw-5.0.1/dkms.conf"
PACKAGE_NAME="titan-hw"
PACKAGE_VERSION="5.0.1"
BUILT_MODULE_NAME[0]="titan_hw"
DEST_MODULE_LOCATION[0]="/kernel/drivers/misc"
AUTOINSTALL="yes"
EOF

# 4. Automation Purge (The "Not Automation" Directive)
echo "[*] PURGING AUTOMATION VECTORS..."
# We explicitly ensure no selenium drivers are present
rm -f "$ISO_DIR/usr/bin/chromedriver"
rm -f "$ISO_DIR/usr/bin/geckodriver"
# Remove any botting libraries from python requirements if they exist
sed -i '/selenium/d' "$ISO_DIR/opt/lucid-empire/requirements.txt"
sed -i '/puppeteer/d' "$ISO_DIR/opt/lucid-empire/requirements.txt"
sed -i '/playwright/d' "$ISO_DIR/opt/lucid-empire/requirements.txt"
echo "[+] System Purified. Manual Control Only."

# 5. Live-Build Configuration
echo "[*] Configuring Debian Live..."
lb config \
    --distribution bookworm \
    --archive-areas "main contrib non-free-firmware" \
    --architectures amd64 \
    --linux-packages "linux-image linux-headers" \
    --bootappend-live "boot=live components quiet splash persistence"

# 6. Build
echo "[*] Building ISO Image (This may take time)..."
# lb build  <-- Commented out to prevent accidental execution in non-build envs
echo "[!] COMMAND READY: 'sudo lb build'"

echo "[*] TITAN V5 CONFIGURATION COMPLETE."
echo "[*] ARTIFACTS READY FOR INJECTION."
