#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

MUAPI_VERSION="0.2.7"

echo "== MuAPI + Codex bootstrap =="
echo "Repo: $ROOT_DIR"

if ! command -v npm >/dev/null 2>&1; then
  echo "ERROR: npm is not available. Install Node.js/npm, then rerun this script." >&2
  exit 2
fi

if ! command -v muapi >/dev/null 2>&1; then
  echo "Installing muapi-cli@$MUAPI_VERSION..."
  npm install -g "muapi-cli@$MUAPI_VERSION"
else
  echo "MuAPI CLI already installed: $(command -v muapi)"
fi

if ! command -v muapi >/dev/null 2>&1; then
  echo "ERROR: muapi command is still unavailable after installation." >&2
  exit 3
fi

printf 'MuAPI CLI: '
muapi --version || true

echo
if command -v codex >/dev/null 2>&1; then
  echo "Codex CLI detected: $(command -v codex)"
  echo "Checking project MCP registration..."
  if codex mcp get muapi --json >/tmp/muapi-codex-mcp.json 2>/tmp/muapi-codex-mcp.err; then
    cat /tmp/muapi-codex-mcp.json
  else
    echo "Codex did not return the project MCP entry through the CLI yet."
    echo "The repo-level .codex/config.toml is already present and will be loaded by Codex when this project is opened/trusted."
    cat /tmp/muapi-codex-mcp.err 2>/dev/null || true
  fi
else
  echo "Codex CLI is not on PATH. That does not block the Codex desktop app from using this repo's .codex/config.toml."
fi

echo
if muapi auth whoami >/tmp/muapi-whoami.txt 2>/tmp/muapi-whoami.err; then
  echo "MuAPI authentication is already configured:"
  cat /tmp/muapi-whoami.txt
  echo
  echo "Checking account balance (read-only)..."
  muapi account balance || true
  echo
  echo "Checking model discovery (read-only)..."
  muapi models list --category video || true
  echo
  echo "READY: MuAPI CLI + Codex MCP are configured."
else
  echo "READY FOR YOUR KEY: CLI and Codex MCP configuration are installed."
  echo "Add the key once with:"
  echo "  muapi auth configure"
  echo
  echo "Then rerun:"
  echo "  bash tools/muapi/verify_codex.sh"
fi
