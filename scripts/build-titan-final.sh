#!/bin/bash
# ==============================================================================
# LUCID EMPIRE TITAN V5 - FINAL ISO BUILDER
# AUTHORITY: Dva.12 | TARGET: DEBIAN 12 BOOKWORM
# ==============================================================================

set -e

# Configuration
ISO_NAME="lucid-titan-v5-final.iso"
WORK_DIR="./build_work"
ISO_CHROOT="./iso/config/includes.chroot"
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
    gcc \
    make \
    python3-dev

# 2. Compile Network Shield (eBPF)
echo "[*] Compiling Network Shield (eBPF)..."
if [ -f "$TITAN_CORE/ebpf/network_shield.c" ]; then
    mkdir -p "$ISO_CHROOT/opt/lucid-empire/ebpf"
    clang -O2 -target bpf -D__TARGET_ARCH_x86 -I/usr/include/x86_64-linux-gnu \
        -c "$TITAN_CORE/ebpf/network_shield.c" \
        -o "$ISO_CHROOT/opt/lucid-empire/ebpf/network_shield.o"
    echo "[+] eBPF Object Generated."
    llvm-objdump -h "$ISO_CHROOT/opt/lucid-empire/ebpf/network_shield.o" | grep -E "(xdp|tc)" || true
else
    echo "[!] CRITICAL: Network Shield source missing!"
    exit 1
fi

# 3. Setup Hardware Shield (Kernel Module) for DKMS build
echo "[*] Setting up Hardware Shield (Kernel Module)..."
mkdir -p "$ISO_CHROOT/usr/src/titan-hw-5.0.1"
cp "$TITAN_CORE/hardware_shield/titan_hw.c" "$ISO_CHROOT/usr/src/titan-hw-5.0.1/"
cp "$TITAN_CORE/hardware_shield/Makefile" "$ISO_CHROOT/usr/src/titan-hw-5.0.1/"

# Create DKMS config
cat <<EOF > "$ISO_CHROOT/usr/src/titan-hw-5.0.1/dkms.conf"
PACKAGE_NAME="titan-hw"
PACKAGE_VERSION="5.0.1"
BUILT_MODULE_NAME[0]="titan_hw"
DEST_MODULE_LOCATION[0]="/kernel/drivers/misc"
AUTOINSTALL="yes"
EOF
echo "[+] Kernel module source staged for ISO."

# 4. Automation Purge (The "Not Automation" Directive)
echo "[*] PURGING AUTOMATION VECTORS..."
# We explicitly ensure no selenium drivers are present
rm -f "$ISO_CHROOT/usr/bin/chromedriver"
rm -f "$ISO_CHROOT/usr/bin/geckodriver"
# Remove any botting libraries from python requirements if they exist
if [ -f "$ISO_CHROOT/opt/lucid-empire/requirements.txt" ]; then
    sed -i '/selenium/d' "$ISO_CHROOT/opt/lucid-empire/requirements.txt"
    sed -i '/puppeteer/d' "$ISO_CHROOT/opt/lucid-empire/requirements.txt"
    sed -i '/playwright/d' "$ISO_CHROOT/opt/lucid-empire/requirements.txt"
fi
echo "[+] System Purified. Manual Control Only."

# 5. Live-Build Configuration
echo "[*] Configuring Debian Live..."
cd iso
lb clean --purge || true
lb config \
    --distribution bookworm \
    --archive-areas "main contrib non-free-firmware" \
    --architectures amd64 \
    --linux-packages "linux-image linux-headers" \
    --bootappend-live "boot=live components quiet splash persistence"

# 6. Build
echo "[*] Building ISO Image (This may take significant time)..."
lb build

# 7. Move ISO to root directory
if [ -f "live-image-amd64.hybrid.iso" ]; then
    mv live-image-amd64.hybrid.iso "../${ISO_NAME}"
    echo "[+] ISO Built Successfully: ${ISO_NAME}"
else
    echo "[!] ERROR: ISO build did not produce expected output"
    exit 1
fi

cd ..

echo "[*] TITAN V5 BUILD COMPLETE."
echo "[*] ISO Location: ./${ISO_NAME}"
