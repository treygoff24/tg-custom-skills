#!/usr/bin/env bash
# run_blender.sh — Convenience wrapper for headless Blender
# Usage: bash run_blender.sh <script.py> [-- extra args for script]
set -euo pipefail

# Auto-detect Blender binary
if [ -n "${BLENDER_BIN:-}" ]; then
  BLENDER="$BLENDER_BIN"
elif [ -x "/Applications/Blender.app/Contents/MacOS/Blender" ]; then
  BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
elif command -v blender &>/dev/null; then
  BLENDER="$(command -v blender)"
else
  echo "ERROR: Blender not found. Install it or set BLENDER_BIN." >&2
  exit 1
fi

SCRIPT="$1"
shift

if [ ! -f "$SCRIPT" ]; then
  echo "ERROR: Script not found: $SCRIPT" >&2
  exit 1
fi

exec "$BLENDER" --background --factory-startup --python "$SCRIPT" "$@"
