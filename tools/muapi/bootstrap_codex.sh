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

  # GUI apps launched by macOS may not inherit shell credentials and Codex may
  # run MCP servers with a restricted environment. Seed the current user's
  # launchd environment from the existing MuAPI Keychain entry so a restarted
  # Codex app can make the credential available to the MCP launcher. Nothing is
  # written to project files, .env files, or Codex config.
  if [[ "$(uname -s)" == "Darwin" && -x /bin/launchctl ]]; then
    MUAPI_GUI_KEY=""

    if [[ -x /usr/bin/security ]]; then
      MUAPI_GUI_KEY="$(/usr/bin/security find-generic-password -s "muapi-cli" -a "api-key" -w 2>/dev/null || true)"
    fi

    # If the direct security command cannot read the entry in this Terminal,
    # ask the installed MuAPI package to resolve its normal credential chain.
    if [[ -z "$MUAPI_GUI_KEY" && -x "$VENV_DIR/bin/python" ]]; then
      MUAPI_GUI_KEY="$("$VENV_DIR/bin/python" - <<'PY'
from muapi.config import get_api_key
key = get_api_key()
if key:
    print(key, end="")
PY
)"
    fi

    if [[ -n "$MUAPI_GUI_KEY" ]]; then
      /bin/launchctl setenv MUAPI_API_KEY "$MUAPI_GUI_KEY"
      unset MUAPI_GUI_KEY

      MUAPI_LAUNCHD_CHECK="$(/bin/launchctl getenv MUAPI_API_KEY 2>/dev/null || true)"
      if [[ -n "$MUAPI_LAUNCHD_CHECK" ]]; then
        echo "macOS GUI credential bridge: configured for this login session."
        echo "Restart Codex/VS Code after this bootstrap so the new GUI session environment is used."
      else
        echo "WARN: launchd did not retain the MuAPI credential bridge." >&2
      fi
      unset MUAPI_LAUNCHD_CHECK
    else
      echo "WARN: could not seed the macOS GUI credential bridge from the configured MuAPI credential." >&2
    fi
  fi

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
  echo "  bash tools/muapi/bootstrap_codex.sh"
  echo "  bash tools/muapi/verify_codex.sh"
fi
