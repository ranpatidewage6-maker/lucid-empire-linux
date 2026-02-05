#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKDIR="$SCRIPT_DIR/../iso"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_cmd lb
require_cmd debootstrap
require_cmd mksquashfs
require_cmd xorriso

if [[ $EUID -ne 0 ]]; then
  echo "Please run as root (use sudo)." >&2
  exit 1
fi

mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [[ "${CLEAN:-0}" == "1" ]]; then
  lb clean --purge
fi

lb config \
  --distribution noble \
  --archive-areas "main restricted universe multiverse" \
  --binary-images iso-hybrid \
  --linux-packages linux-generic \
  --debootstrap-options "--variant=minbase" \
  --bootappend-live "boot=live components quiet splash"

lb build

echo "Build complete. Look for an ISO in $WORKDIR (e.g. live-image-amd64.hybrid.iso)."
