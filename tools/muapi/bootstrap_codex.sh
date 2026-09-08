#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

MUAPI_VERSION="0.2.7"
VENV_DIR="${MUAPI_VENV_DIR:-$HOME/.local/share/muapi-cli-$MUAPI_VERSION}"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"

echo "== MuAPI + Codex bootstrap =="
echo "Repo: $ROOT_DIR"
echo "Install target: $VENV_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required for the cross-platform MuAPI install." >&2
  exit 2
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 9):
    raise SystemExit("ERROR: MuAPI requires Python 3.9+")
print(f"Python: {sys.version.split()[0]}")
PY

if ! bash "$CLI" --version >/dev/null 2>&1; then
  echo "Installing official muapi-cli==$MUAPI_VERSION from PyPI into a private virtual environment..."
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/python" -m pip install --disable-pip-version-check "muapi-cli==$MUAPI_VERSION"
fi

if ! bash "$CLI" --version >/dev/null 2>&1; then
  echo "ERROR: MuAPI CLI is still unavailable after the PyPI install." >&2
  exit 3
fi

printf 'MuAPI CLI: '
bash "$CLI" --version || true

echo
if command -v codex >/dev/null 2>&1; then
  echo "Codex CLI detected: $(command -v codex)"
  echo "Checking project MCP registration..."
  if codex mcp get muapi --json >/tmp/muapi-codex-mcp.json 2>/tmp/muapi-codex-mcp.err; then
    cat /tmp/muapi-codex-mcp.json
  else
    echo "Codex did not return the project MCP entry through the CLI yet."
    echo "The repo-level .codex/config.toml is present and will be loaded when this project is opened/trusted."
    cat /tmp/muapi-codex-mcp.err 2>/dev/null || true
  fi
else
  echo "Codex CLI is not on PATH. The desktop app can still use this repo's .codex/config.toml."
fi

echo
if bash "$CLI" auth whoami >/tmp/muapi-whoami.txt 2>/tmp/muapi-whoami.err; then
  echo "MuAPI authentication is already configured:"
  cat /tmp/muapi-whoami.txt
  echo
  echo "Checking account balance (read-only)..."
  bash "$CLI" account balance || true
  echo
  echo "Checking model discovery (read-only)..."
  bash "$CLI" models list --category video || true
  echo
  echo "READY: MuAPI CLI + Codex MCP are configured."
else
  echo "READY FOR YOUR KEY: CLI and Codex MCP configuration are installed."
  echo "Add the key once with:"
  echo "  bash tools/muapi/run_cli.sh auth configure"
  echo
  echo "Then rerun:"
  echo "  bash tools/muapi/verify_codex.sh"
fi
