#!/bin/bash
# LUCID EMPIRE: TITAN V5 DEPLOYMENT BRIDGE
# ----------------------------------------
# This script moves the "Source" code (Titan V5, eBPF, Kernel Modules)
# into the "ISO Build" structure (includes.chroot) to ensure the
# final ISO contains the latest Anti-Detect features.

set -euo pipefail

echo "[*] LUCID TITAN V5 :: DEPLOYMENT SEQUENCE STARTED"

# 1. Define Paths
SOURCE_ROOT="./titan"
ISO_DEST="./iso/config/includes.chroot/opt/lucid-empire"
SYSTEMD_DIR="./iso/config/includes.chroot/etc/systemd/system"

# 2. Ensure destinations
mkdir -p "$ISO_DEST"
mkdir -p "$ISO_DEST/ebpf"
mkdir -p "$ISO_DEST/hardware_shield"
mkdir -p "$SYSTEMD_DIR"

# 3. Deploy Titan Core V5
if [ -f "$SOURCE_ROOT/TITAN_CORE_v5.py" ]; then
    echo "[*] Migrating Titan Core V5 Logic..."
    cp "$SOURCE_ROOT/TITAN_CORE_v5.py" "$ISO_DEST/titan_core.py"
    chmod +x "$ISO_DEST/titan_core.py"
else
    echo "[!] Warning: $SOURCE_ROOT/TITAN_CORE_v5.py not found; skipping core copy"
fi

# 4. Deploy eBPF Network Shield
if [ -d "$SOURCE_ROOT/ebpf" ]; then
    echo "[*] Migrating eBPF Network Shield..."
    cp -r "$SOURCE_ROOT/ebpf/"* "$ISO_DEST/ebpf/" || true
else
    echo "[!] Warning: $SOURCE_ROOT/ebpf not found; skipping eBPF copy"
fi

# 5. Deploy Hardware Kernel Module Source
if [ -d "$SOURCE_ROOT/hardware_shield" ]; then
    echo "[*] Migrating Hardware Shield Source..."
    cp -r "$SOURCE_ROOT/hardware_shield/"* "$ISO_DEST/hardware_shield/" || true
else
    echo "[!] Warning: $SOURCE_ROOT/hardware_shield not found; skipping hardware_shield copy"
fi

# 6. Backup existing service and update systemd unit to run titan_core.py (if present)
SERVICE_FILE="$SYSTEMD_DIR/lucid-titan.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "[*] Backing up existing $SERVICE_FILE -> ${SERVICE_FILE}.bak"
    cp "$SERVICE_FILE" "${SERVICE_FILE}.bak"
fi

if [ -f "$ISO_DEST/titan_core.py" ]; then
    echo "[*] Updating systemd service to launch titan_core.py"
    cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Lucid Titan V5 Identity Daemon
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/lucid-empire
ExecStart=/usr/bin/python3 /opt/lucid-empire/titan_core.py
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
else
    echo "[!] titan_core.py not deployed; skipping systemd service update"
fi

echo "[+] DEPLOYMENT COMPLETE."
echo "    Next Step: Run './scripts/build-lucid-iso.sh' to compile the new ISO."
