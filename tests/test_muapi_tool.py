import importlib.util
from pathlib import Path
import pytest
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "muapi" / "muapi_tool.py"
spec = importlib.util.spec_from_file_location("muapi_tool", MODULE_PATH)
muapi = importlib.util.module_from_spec(spec)
sys.modules["muapi_tool"] = muapi
spec.loader.exec_module(muapi)

def test_official_source_pin():
    cfg = muapi.load_config()
    assert cfg.official_cli_repository == "https://github.com/SamurAIGPT/muapi-cli"
    assert cfg.official_cli_commit == "59c9b9f7c0432f89f048ba3db8e04d4d94b12cd8"
    assert cfg.official_cli_version == "0.2.7"

def test_official_endpoints():
    cfg = muapi.load_config()
    assert cfg.rest_api_base == "https://api.muapi.ai/api/v1"
    assert cfg.hosted_mcp_url == "https://api.muapi.ai/mcp"

def test_submit_url_validation():
    assert muapi.submit_url("flux-dev-image").endswith("/flux-dev-image")
    with pytest.raises(ValueError):
        muapi.submit_url("")
    with pytest.raises(ValueError):
        muapi.submit_url("../bad")

def test_result_url():
    assert muapi.result_url("abc123").endswith("/predictions/abc123/result")

def test_api_key_guardrail():
    assert muapi.api_key_present({}) is False
    assert muapi.api_key_present({"MUAPI_API_KEY": "sandbox-test"}) is True
    with pytest.raises(RuntimeError):
        muapi.auth_headers(api_key=None)

def test_auth_header_shapes():
    assert muapi.auth_headers("k")["x-api-key"] == "k"
    assert muapi.bearer_headers("k")["Authorization"] == "Bearer k"

def test_pinned_cli_command():
    assert muapi.cli_install_command() == "npm install -g muapi-cli@0.2.7"
    assert muapi.cli_mcp_command() == "muapi mcp serve"

def test_hosted_mcp_config():
    conf = muapi.hosted_mcp_config("TEST")
    assert conf["mcpServers"]["muapi"]["url"] == "https://api.muapi.ai/mcp"
    assert conf["mcpServers"]["muapi"]["headers"]["Authorization"] == "Bearer TEST"

def test_env_template_has_no_secret():
    text = (ROOT / "tools" / "muapi" / ".env.example").read_text()
    assert "MUAPI_API_KEY=" in text
    assert "sk-" not in text
