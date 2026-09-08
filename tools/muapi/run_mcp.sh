#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLI="$ROOT_DIR/tools/muapi/run_cli.sh"

# Do not inject credentials here. MuAPI's own resolver checks, in order:
# MUAPI_API_KEY, the OS Keychain/keyring, then ~/.muapi/config.json.
# bootstrap_codex.sh seeds the official config-file fallback with mode 600 when
# Codex cannot access the interactive Keychain backend.
exec bash "$CLI" mcp serve
