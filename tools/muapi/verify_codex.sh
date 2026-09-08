#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"
MCP_WRAPPER="$ROOT_DIR/tools/muapi/run_mcp.sh"
CONFIG_FILE="$HOME/.muapi/config.json"

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

echo
python3 - "$CONFIG_FILE" <<'PY'
import json
import stat
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit("FAIL: ~/.muapi/config.json is missing; rerun bootstrap_codex.sh")

try:
    data = json.loads(path.read_text())
except Exception as exc:
    raise SystemExit(f"FAIL: ~/.muapi/config.json is unreadable JSON: {exc}")

if not isinstance(data, dict) or not data.get("api_key"):
    raise SystemExit("FAIL: ~/.muapi/config.json does not contain an API key")

mode = stat.S_IMODE(path.stat().st_mode)
if mode & 0o077:
    raise SystemExit(f"FAIL: ~/.muapi/config.json permissions are too broad: {oct(mode)}")

print(f"PASS: MuAPI native config fallback exists with restricted permissions ({oct(mode)})")
PY

echo
python3 - "$MCP_WRAPPER" <<'PY'
import subprocess
import sys

wrapper = sys.argv[1]
proc = subprocess.Popen(
    ["bash", wrapper],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
try:
    stdout, stderr = proc.communicate(input="", timeout=5)
except subprocess.TimeoutExpired:
    proc.terminate()
    stdout, stderr = proc.communicate(timeout=2)

combined = (stdout or "") + "\n" + (stderr or "")
if "No MUAPI_API_KEY configured" in combined:
    raise SystemExit("FAIL: MuAPI MCP startup still cannot resolve a credential")
if "muapi MCP server ready" not in combined:
    raise SystemExit("FAIL: MuAPI MCP startup did not report ready")

print("PASS: MuAPI MCP server resolves authentication and reaches ready state")
PY

echo
bash "$CLI" account balance || true

echo
bash "$CLI" models list --category video || true

echo
if command -v codex >/dev/null 2>&1; then
  if codex mcp get muapi --json; then
    echo "PASS: Codex can see the MuAPI MCP entry"
  else
    echo "WARN: Codex CLI could not resolve the MuAPI MCP entry. Reopen/trust this repo in Codex and retry." >&2
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
