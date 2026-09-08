from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_codex_config_uses_wrapper_stdio():
    text = (ROOT / ".codex" / "config.toml").read_text()
    assert "[mcp_servers.muapi]" in text
    assert 'command = "bash"' in text
    assert 'args = ["tools/muapi/run_mcp.sh"]' in text
    assert "MUAPI_API_KEY" not in text
    assert "Bearer " not in text


def test_bootstrap_pins_cli_registers_codex_and_seeds_native_config():
    text = (ROOT / "tools" / "muapi" / "bootstrap_codex.sh").read_text()
    assert 'MUAPI_VERSION="0.2.7"' in text
    assert 'muapi-cli==$MUAPI_VERSION' in text
    assert "python3 -m venv" in text
    assert "npm install -g" not in text
    assert 'codex mcp add muapi -- bash "$MCP_WRAPPER"' in text
    assert "codex mcp get muapi --json" in text
    assert "bash tools/muapi/run_cli.sh auth configure" in text
    assert 'config_file = config_dir / "config.json"' in text
    assert 'existing["api_key"] = key' in text
    assert "os.chmod(config_file, 0o600)" in text
    assert "/bin/launchctl unsetenv MUAPI_API_KEY" in text
    assert "/bin/launchctl setenv MUAPI_API_KEY" not in text
    assert "YOUR_MUAPI_KEY" not in text
    assert "Bearer " not in text


def test_cli_wrapper_has_private_venv_fallback():
    text = (ROOT / "tools" / "muapi" / "run_cli.sh").read_text()
    assert 'MUAPI_VERSION="0.2.7"' in text
    assert ".local/share/muapi-cli-$MUAPI_VERSION" in text
    assert 'exec "$VENV_DIR/bin/muapi" "$@"' in text


def test_mcp_wrapper_uses_muapi_native_resolver_without_secret_injection():
    text = (ROOT / "tools" / "muapi" / "run_mcp.sh").read_text()
    assert 'run_cli.sh" mcp serve' in text
    assert "~/.muapi/config.json" in text
    assert "/usr/bin/security find-generic-password" not in text
    assert "/bin/launchctl getenv MUAPI_API_KEY" not in text
    assert "export MUAPI_API_KEY" not in text
    assert 'echo "$MUAPI_API_KEY"' not in text
    assert 'printf "$MUAPI_API_KEY"' not in text


def test_verifier_is_read_only_and_smoke_tests_mcp_auth():
    text = (ROOT / "tools" / "muapi" / "verify_codex.sh").read_text()
    assert "auth whoami" in text
    assert "account balance" in text
    assert "models list --category video" in text
    assert "config.json" in text
    assert "muapi MCP server ready" in text
    assert "No MUAPI_API_KEY configured" in text
    assert "image generate" not in text
    assert "video generate" not in text
    assert "audio create" not in text


def test_readme_documents_single_key_step_and_native_fallback():
    text = (ROOT / "tools" / "muapi" / "README.md").read_text()
    assert "bash tools/muapi/bootstrap_codex.sh" in text
    assert "auth configure" in text
    assert "bash tools/muapi/verify_codex.sh" in text
    assert "~/.muapi/config.json" in text
    assert "0600" in text or "mode `600`" in text
