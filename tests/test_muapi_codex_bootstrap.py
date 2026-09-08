from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_codex_config_uses_wrapper_stdio():
    text = (ROOT / ".codex" / "config.toml").read_text()
    assert "[mcp_servers.muapi]" in text
    assert 'command = "bash"' in text
    assert 'args = ["tools/muapi/run_mcp.sh"]' in text
    assert "MUAPI_API_KEY" not in text
    assert "Bearer " not in text


def test_bootstrap_pins_cli_and_uses_pypi_venv():
    text = (ROOT / "tools" / "muapi" / "bootstrap_codex.sh").read_text()
    assert 'MUAPI_VERSION="0.2.7"' in text
    assert 'muapi-cli==$MUAPI_VERSION' in text
    assert "python3 -m venv" in text
    assert "npm install -g" not in text
    assert "bash tools/muapi/run_cli.sh auth configure" in text
    assert "YOUR_MUAPI_KEY" not in text
    assert "Bearer " not in text


def test_cli_wrapper_has_private_venv_fallback():
    text = (ROOT / "tools" / "muapi" / "run_cli.sh").read_text()
    assert 'MUAPI_VERSION="0.2.7"' in text
    assert ".local/share/muapi-cli-$MUAPI_VERSION" in text
    assert 'exec "$VENV_DIR/bin/muapi" "$@"' in text


def test_mcp_wrapper_uses_cli_wrapper():
    text = (ROOT / "tools" / "muapi" / "run_mcp.sh").read_text()
    assert 'run_cli.sh" mcp serve' in text


def test_verifier_is_read_only_for_media_generation():
    text = (ROOT / "tools" / "muapi" / "verify_codex.sh").read_text()
    assert "auth whoami" in text
    assert "account balance" in text
    assert "models list --category video" in text
    assert "image generate" not in text
    assert "video generate" not in text
    assert "audio create" not in text


def test_readme_documents_single_key_step():
    text = (ROOT / "tools" / "muapi" / "README.md").read_text()
    assert "bash tools/muapi/bootstrap_codex.sh" in text
    assert "auth configure" in text
    assert "bash tools/muapi/verify_codex.sh" in text
