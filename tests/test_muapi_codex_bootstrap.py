from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_codex_config_uses_local_muapi_stdio():
    text = (ROOT / ".codex" / "config.toml").read_text()
    assert "[mcp_servers.muapi]" in text
    assert 'command = "muapi"' in text
    assert 'args = ["mcp", "serve"]' in text
    assert "MUAPI_API_KEY" not in text
    assert "Bearer " not in text


def test_bootstrap_pins_cli_and_does_not_embed_secret():
    text = (ROOT / "tools" / "muapi" / "bootstrap_codex.sh").read_text()
    assert 'MUAPI_VERSION="0.2.7"' in text
    assert 'npm install -g "muapi-cli@$MUAPI_VERSION"' in text
    assert "muapi auth configure" in text
    assert "YOUR_MUAPI_KEY" not in text
    assert "Bearer " not in text


def test_verifier_is_read_only_for_media_generation():
    text = (ROOT / "tools" / "muapi" / "verify_codex.sh").read_text()
    assert "muapi auth whoami" in text
    assert "muapi account balance" in text
    assert "muapi models list --category video" in text
    assert "muapi image generate" not in text
    assert "muapi video generate" not in text
    assert "muapi audio create" not in text


def test_readme_documents_single_key_step():
    text = (ROOT / "tools" / "muapi" / "README.md").read_text()
    assert "bash tools/muapi/bootstrap_codex.sh" in text
    assert "muapi auth configure" in text
    assert "bash tools/muapi/verify_codex.sh" in text
