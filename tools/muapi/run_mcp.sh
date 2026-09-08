#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"

# Codex-launched MCP processes on macOS may run with a cleared environment
# and may not be able to resolve Python's Keychain backend directly.
# Resolve the credential at runtime without persisting it in Git or config.
if [[ -z "${MUAPI_API_KEY:-}" && "$(uname -s)" == "Darwin" ]]; then
  # First choice: read the official MuAPI Keychain entry directly.
  if [[ -x /usr/bin/security ]]; then
    if MUAPI_KEYCHAIN_VALUE="$(/usr/bin/security find-generic-password -s "muapi-cli" -a "api-key" -w 2>/dev/null)"; then
      if [[ -n "$MUAPI_KEYCHAIN_VALUE" ]]; then
        export MUAPI_API_KEY="$MUAPI_KEYCHAIN_VALUE"
      fi
    fi
    unset MUAPI_KEYCHAIN_VALUE
  fi

  # Fallback for sandboxed GUI launches: read the user's launchd session env.
  # bootstrap_codex.sh seeds this value from Keychain without writing it to disk.
  if [[ -z "${MUAPI_API_KEY:-}" && -x /bin/launchctl ]]; then
    MUAPI_LAUNCHD_VALUE="$(/bin/launchctl getenv MUAPI_API_KEY 2>/dev/null || true)"
    if [[ -n "$MUAPI_LAUNCHD_VALUE" ]]; then
      export MUAPI_API_KEY="$MUAPI_LAUNCHD_VALUE"
    fi
    unset MUAPI_LAUNCHD_VALUE
  fi
fi

exec bash "$CLI" mcp serve
