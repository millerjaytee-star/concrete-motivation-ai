#!/usr/bin/env bash
set -euo pipefail

MUAPI_VERSION="0.2.7"
VENV_DIR="${MUAPI_VENV_DIR:-$HOME/.local/share/muapi-cli-$MUAPI_VERSION}"

if command -v muapi >/dev/null 2>&1; then
  exec muapi "$@"
fi

if [[ -x "$VENV_DIR/bin/muapi" ]]; then
  exec "$VENV_DIR/bin/muapi" "$@"
fi

echo "ERROR: MuAPI CLI is not installed. Run: bash tools/muapi/bootstrap_codex.sh" >&2
exit 127
