#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"

# Codex-launched MCP processes on macOS may not be able to resolve the
# Python keyring entry even though interactive MuAPI CLI commands can.
# Bridge the official MuAPI Keychain entry into this child process only.
# Nothing is written to disk or project configuration.
if [[ -z "${MUAPI_API_KEY:-}" && "$(uname -s)" == "Darwin" && -x /usr/bin/security ]]; then
  if MUAPI_KEYCHAIN_VALUE="$(/usr/bin/security find-generic-password -s "muapi-cli" -a "api-key" -w 2>/dev/null)"; then
    if [[ -n "$MUAPI_KEYCHAIN_VALUE" ]]; then
      export MUAPI_API_KEY="$MUAPI_KEYCHAIN_VALUE"
    fi
  fi
  unset MUAPI_KEYCHAIN_VALUE
fi

exec bash "$CLI" mcp serve
