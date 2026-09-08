#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

MUAPI_VERSION="0.2.7"
VENV_DIR="${MUAPI_VENV_DIR:-$HOME/.local/share/muapi-cli-$MUAPI_VERSION}"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"
MCP_WRAPPER="$ROOT_DIR/tools/muapi/run_mcp.sh"

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

# Keep a pinned private PyPI install available even if another global MuAPI CLI
# happens to be on PATH. This gives the bootstrap a known Python package for
# credential resolution and avoids the broken Intel macOS npm artifact path.
if [[ ! -x "$VENV_DIR/bin/muapi" || ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Installing official muapi-cli==$MUAPI_VERSION from PyPI into a private virtual environment..."
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/python" -m pip install --disable-pip-version-check "muapi-cli==$MUAPI_VERSION"
fi

if ! bash "$CLI" --version >/dev/null 2>&1; then
  echo "ERROR: MuAPI CLI is unavailable after the PyPI install." >&2
  exit 3
fi

printf 'MuAPI CLI: '
bash "$CLI" --version || true

echo
if command -v codex >/dev/null 2>&1; then
  echo "Codex CLI detected: $(command -v codex)"
  echo "Checking MuAPI MCP registration..."
  if codex mcp get muapi --json >/tmp/muapi-codex-mcp.json 2>/tmp/muapi-codex-mcp.err; then
    cat /tmp/muapi-codex-mcp.json
  else
    echo "MuAPI MCP is not registered globally in Codex yet. Registering it now..."
    codex mcp add muapi -- bash "$MCP_WRAPPER"
    echo "Verifying Codex MCP registration..."
    codex mcp get muapi --json
  fi
else
  echo "Codex CLI is not on PATH. The desktop app can still use this repo's .codex/config.toml."
fi

echo
if bash "$CLI" auth whoami >/tmp/muapi-whoami.txt 2>/tmp/muapi-whoami.err; then
  echo "MuAPI authentication is already configured:"
  cat /tmp/muapi-whoami.txt

  echo
  echo "Preparing MuAPI's native MCP credential fallback..."
  "$VENV_DIR/bin/python" - <<'PY'
import json
import os
from pathlib import Path

from muapi.config import get_api_key

key = get_api_key()
if not key:
    raise SystemExit("ERROR: MuAPI credential resolver returned no API key")

config_dir = Path.home() / ".muapi"
config_file = config_dir / "config.json"
config_dir.mkdir(parents=True, exist_ok=True)
os.chmod(config_dir, 0o700)

existing = {}
if config_file.exists():
    try:
        parsed = json.loads(config_file.read_text())
        if isinstance(parsed, dict):
            existing = parsed
    except Exception:
        existing = {}

existing["api_key"] = key

tmp_file = config_dir / "config.json.tmp"
with tmp_file.open("w") as handle:
    json.dump(existing, handle, indent=2)
    handle.write("\n")
os.chmod(tmp_file, 0o600)
os.replace(tmp_file, config_file)
os.chmod(config_file, 0o600)

print("MuAPI native fallback: ~/.muapi/config.json (mode 600)")
PY

  # Remove the older launchd bridge if it was created by a previous bootstrap.
  # The MCP server now uses MuAPI's own documented config-file fallback instead.
  if [[ "$(uname -s)" == "Darwin" && -x /bin/launchctl ]]; then
    /bin/launchctl unsetenv MUAPI_API_KEY >/dev/null 2>&1 || true
  fi

  echo
  echo "Checking account balance (read-only)..."
  bash "$CLI" account balance || true
  echo
  echo "Checking model discovery (read-only)..."
  bash "$CLI" models list --category video || true
  echo
  echo "READY: MuAPI CLI + native credential fallback + Codex MCP are configured."
else
  echo "READY FOR YOUR KEY: CLI and Codex MCP configuration are installed."
  echo "Add the key once with:"
  echo "  bash tools/muapi/run_cli.sh auth configure"
  echo
  echo "Then rerun:"
  echo "  bash tools/muapi/bootstrap_codex.sh"
  echo "  bash tools/muapi/verify_codex.sh"
fi
