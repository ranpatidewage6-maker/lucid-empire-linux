#!/usr/bin/env bash
set -euo pipefail
WORKDIR="/workspaces/lucid-empire-linux"
LOG="$WORKDIR/iso/monitor.log"
BUILDLOG="$WORKDIR/iso/build_full.log"
WATCHLOG="$WORKDIR/iso/auto_boot_vnc.out"
INTERVAL=10

echo "[MONITOR] started at $(date)" | tee -a "$LOG"
while true; do
  echo "\n===== STATUS @ $(date) =====" | tee -a "$LOG"
  echo "-- ISO files --" | tee -a "$LOG"
  find "$WORKDIR/iso" -maxdepth 2 -type f -name '*.iso' -ls | tee -a "$LOG" || true

  echo "\n-- Last build log lines --" | tee -a "$LOG"
  if [ -f "$BUILDLOG" ]; then
    tail -n 40 "$BUILDLOG" | sed -n '1,200p' | tee -a "$LOG"
  else
    echo "(no build log yet)" | tee -a "$LOG"
  fi

  echo "\n-- Last auto-boot watcher lines --" | tee -a "$LOG"
  if [ -f "$WATCHLOG" ]; then
    tail -n 40 "$WATCHLOG" | sed -n '1,200p' | tee -a "$LOG"
  else
    echo "(no watcher log yet)" | tee -a "$LOG"
  fi

  echo "\n-- QEMU processes --" | tee -a "$LOG"
  ps aux | egrep 'qemu-system-x86_64|qemu-kvm' | egrep -v 'egrep' | tee -a "$LOG" || true

  echo "\n-- Network listeners (VNC) --" | tee -a "$LOG"
  ss -ltnp 2>/dev/null | egrep ':590|:5901' | tee -a "$LOG" || true

  echo "\n-- End status --\n" | tee -a "$LOG"
  sleep "$INTERVAL"
done
