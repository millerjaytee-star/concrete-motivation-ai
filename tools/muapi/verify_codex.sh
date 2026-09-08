#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "== Verify MuAPI + Codex =="

command -v muapi >/dev/null 2>&1 || {
  echo "FAIL: muapi CLI not installed. Run bash tools/muapi/bootstrap_codex.sh" >&2
  exit 2
}

echo "PASS: muapi CLI found at $(command -v muapi)"
muapi --version || true

echo
if muapi auth whoami; then
  echo "PASS: MuAPI authentication configured"
else
  echo "FAIL: MuAPI key not configured. Run: muapi auth configure" >&2
  exit 3
fi

echo
muapi account balance || true

echo
muapi models list --category video || true

echo
if command -v codex >/dev/null 2>&1; then
  if codex mcp get muapi --json; then
    echo "PASS: Codex can see the MuAPI MCP entry"
  else
    echo "WARN: Codex CLI could not resolve the project MCP entry. Open/trust this repo in Codex and retry." >&2
  fi
else
  echo "INFO: Codex CLI is not on PATH; verify the MCP in the Codex desktop app after reopening this project."
fi

echo
cat <<'EOF'
MuAPI is ready for agent use.
No generation was submitted by this verification script.
Production generation can consume MuAPI credits; keep Sandbox credentials for testing until you intentionally switch.
EOF
