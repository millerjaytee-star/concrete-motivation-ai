#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"

echo "== Verify MuAPI + Codex =="

if ! bash "$CLI" --version >/dev/null 2>&1; then
  echo "FAIL: MuAPI CLI not installed. Run bash tools/muapi/bootstrap_codex.sh" >&2
  exit 2
fi

echo "PASS: MuAPI CLI available through tools/muapi/run_cli.sh"
bash "$CLI" --version || true

echo
if bash "$CLI" auth whoami; then
  echo "PASS: MuAPI authentication configured"
else
  echo "FAIL: MuAPI key not configured. Run: bash tools/muapi/run_cli.sh auth configure" >&2
  exit 3
fi

if [[ "$(uname -s)" == "Darwin" && -x /bin/launchctl ]]; then
  MUAPI_LAUNCHD_CHECK="$(/bin/launchctl getenv MUAPI_API_KEY 2>/dev/null || true)"
  if [[ -n "$MUAPI_LAUNCHD_CHECK" ]]; then
    echo "PASS: macOS GUI credential bridge is populated for this login session"
  else
    echo "WARN: macOS GUI credential bridge is empty. Run bash tools/muapi/bootstrap_codex.sh, then restart Codex/VS Code." >&2
  fi
  unset MUAPI_LAUNCHD_CHECK
fi

echo
bash "$CLI" account balance || true

echo
bash "$CLI" models list --category video || true

echo
if command -v codex >/dev/null 2>&1; then
  if codex mcp get muapi --json; then
    echo "PASS: Codex can see the MuAPI MCP entry"
  else
    echo "WARN: Codex CLI could not resolve the project MCP entry. Reopen/trust this repo in Codex and retry." >&2
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
