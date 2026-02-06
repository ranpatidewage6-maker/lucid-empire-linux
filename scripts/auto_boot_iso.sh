#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/workspaces/lucid-empire-linux"
LOG="$WORKDIR/iso/auto_boot.log"
ISO_OUT="$WORKDIR/iso"

echo "[AUTO-BOOT] watcher started at $(date)" | tee -a "$LOG"

find_iso() {
  # prefer iso/ then /tmp
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

# Poll until ISO appears
while true; do
  iso_path=$(find_iso)
  if [ -n "$iso_path" ]; then
    echo "[AUTO-BOOT] Found ISO: $iso_path" | tee -a "$LOG"
    break
  fi
  echo "[AUTO-BOOT] ISO not found yet, sleeping 10s..." | tee -a "$LOG"
  sleep 10
done

# Verify checksum and metadata
sha256sum "$iso_path" | tee "$WORKDIR/iso/last_iso.sha256" | tee -a "$LOG"
ls -lh "$iso_path" | tee -a "$LOG"

# Boot with QEMU in serial (no GUI) so console appears in this terminal.
# Use modest resources to fit CI/container env.
QEMU_BIN=$(command -v qemu-system-x86_64 || true)
if [ -z "$QEMU_BIN" ]; then
  echo "[AUTO-BOOT] qemu-system-x86_64 not found in PATH" | tee -a "$LOG"
  exit 2
fi

echo "[AUTO-BOOT] Launching QEMU (serial console). To exit: Ctrl-a x or send quit to monitor." | tee -a "$LOG"
"$QEMU_BIN" -m 2048 -smp 2 -cdrom "$iso_path" -boot d -nographic -serial mon:stdio -monitor none 2>&1 | tee -a "$LOG"

echo "[AUTO-BOOT] QEMU exited at $(date)" | tee -a "$LOG"
