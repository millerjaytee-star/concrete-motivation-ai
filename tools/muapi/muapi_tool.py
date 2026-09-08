from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_PATH = Path(__file__).with_name("config.json")

@dataclass(frozen=True)
class MuAPIConfig:
    api_base_url: str
    rest_api_base: str
    hosted_mcp_url: str
    official_cli_repository: str
    official_cli_commit: str
    official_cli_version: str
    auth_env: str

def load_config(path: Path = CONFIG_PATH) -> MuAPIConfig:
    data = json.loads(path.read_text())
    return MuAPIConfig(
        api_base_url=data["api_base_url"],
        rest_api_base=data["rest_api_base"],
        hosted_mcp_url=data["hosted_mcp_url"],
        official_cli_repository=data["official_cli_repository"],
        official_cli_commit=data["official_cli_commit"],
        official_cli_version=data["official_cli_version"],
        auth_env=data["auth_env"],
    )

def api_key_present(env: Optional[Dict[str, str]] = None) -> bool:
    env = env if env is not None else os.environ
    return bool(env.get(load_config().auth_env))

def auth_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    cfg = load_config()
    key = api_key or os.environ.get(cfg.auth_env)
    if not key:
        raise RuntimeError(f"{cfg.auth_env} is not set")
    return {"x-api-key": key, "Content-Type": "application/json"}

def bearer_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    cfg = load_config()
    key = api_key or os.environ.get(cfg.auth_env)
    if not key:
        raise RuntimeError(f"{cfg.auth_env} is not set")
    return {"Authorization": f"Bearer {key}"}

def submit_url(model: str) -> str:
    if not model or "/" in model or model.startswith("."):
        raise ValueError("model must be a non-empty MuAPI endpoint name")
    return f"{load_config().rest_api_base}/{model}"

def result_url(request_id: str) -> str:
    if not request_id:
        raise ValueError("request_id is required")
    return f"{load_config().rest_api_base}/predictions/{request_id}/result"

def cli_install_command() -> str:
    cfg = load_config()
    return f"npm install -g muapi-cli@{cfg.official_cli_version}"

def cli_mcp_command() -> str:
    return "muapi mcp serve"

def hosted_mcp_config(api_key_placeholder: str = "${MUAPI_API_KEY}") -> Dict[str, Any]:
    return {
        "mcpServers": {
            "muapi": {
                "url": load_config().hosted_mcp_url,
                "headers": {
                    "Authorization": f"Bearer {api_key_placeholder}"
                },
            }
        }
    }

def status() -> Dict[str, Any]:
    cfg = load_config()
    return {
        "tool": "MuAPI",
        "api_key_configured": api_key_present(),
        "rest_api_base": cfg.rest_api_base,
        "hosted_mcp_url": cfg.hosted_mcp_url,
        "official_cli_repository": cfg.official_cli_repository,
        "official_cli_commit": cfg.official_cli_commit,
        "official_cli_version": cfg.official_cli_version,
        "execution_ready": api_key_present(),
        "note": (
            "Use a Sandbox key for integration testing. Production generations consume MuAPI credits."
            if not api_key_present()
            else "Credentials detected; choose Sandbox for mock testing or Production for real generations."
        ),
    }

if __name__ == "__main__":
    print(json.dumps(status(), indent=2))
