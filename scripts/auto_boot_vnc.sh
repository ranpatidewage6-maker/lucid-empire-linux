#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/workspaces/lucid-empire-linux"
LOG="$WORKDIR/iso/auto_boot_vnc.log"
ISO_OUT="$WORKDIR/iso"
VM_DISK="$WORKDIR/iso/lucid-vm.qcow2"
VNC_DISPLAY=1

echo "[AUTO-BOOT-VNC] watcher started at $(date)" | tee -a "$LOG"

find_iso() {
  local f
  f=$(find "$WORKDIR/iso" -maxdepth 3 -type f -name '*.iso' -print -quit 2>/dev/null || true)
  if [ -n "$f" ]; then
    echo "$f"
    return
  fi
  f=$(find /tmp -maxdepth 2 -type f -name '*.iso' -print -quit 2>/dev/null || true)
  if [ -n "$f" ]; then
    echo "$f"
    return
  fi
  echo ""
}

# Ensure VM disk exists
if [ ! -f "$VM_DISK" ]; then
  echo "[AUTO-BOOT-VNC] Creating VM disk $VM_DISK (20G)" | tee -a "$LOG"
  qemu-img create -f qcow2 "$VM_DISK" 20G | tee -a "$LOG"
fi

# Poll until ISO appears
while true; do
  iso_path=$(find_iso)
  if [ -n "$iso_path" ]; then
    echo "[AUTO-BOOT-VNC] Found ISO: $iso_path" | tee -a "$LOG"
    break
  fi
  echo "[AUTO-BOOT-VNC] ISO not found yet, sleeping 10s..." | tee -a "$LOG"
  sleep 10
done

# Verify checksum and metadata
sha256sum "$iso_path" | tee "$WORKDIR/iso/last_iso.sha256" | tee -a "$LOG"
ls -lh "$iso_path" | tee -a "$LOG"

QEMU_BIN=$(command -v qemu-system-x86_64 || true)
if [ -z "$QEMU_BIN" ]; then
  echo "[AUTO-BOOT-VNC] qemu-system-x86_64 not found in PATH" | tee -a "$LOG"
  exit 2
fi

# Launch QEMU with VNC display :1
echo "[AUTO-BOOT-VNC] Launching QEMU (VNC :$VNC_DISPLAY)." | tee -a "$LOG"
"$QEMU_BIN" -m 4096 -smp 2 -cdrom "$iso_path" -hda "$VM_DISK" -boot d -vnc :${VNC_DISPLAY} -nographic -serial none -monitor none 2>&1 | tee -a "$LOG"

echo "[AUTO-BOOT-VNC] QEMU exited at $(date)" | tee -a "$LOG"
