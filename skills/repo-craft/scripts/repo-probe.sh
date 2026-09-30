#!/usr/bin/env bash
# Portable compatibility entrypoint. Python resolves all bundled paths itself.
set -eu
if ! command -v python3 >/dev/null 2>&1; then
  printf 'repo-probe: Python 3.9 or newer is required; install Python and retry.\n' >&2
  exit 1
fi
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 -B "$SCRIPT_DIR/repo_probe.py" "$@"
