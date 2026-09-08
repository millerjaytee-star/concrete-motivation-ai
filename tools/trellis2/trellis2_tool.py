"""Small, dependency-light registry/health wrapper for Microsoft TRELLIS.2.

This module intentionally does not vendor or import TRELLIS.2 itself. The official
implementation is GPU-heavy and remains pinned upstream. ChatGPT/Hugging Face is
the preferred remote execution route; supported Linux/NVIDIA hosts can use the
pinned upstream source directly.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).with_name("config.json")
SUPPORTED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema_version", "tool_id", "name", "upstream", "hugging_face", "execution"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"TRELLIS.2 config missing required keys: {sorted(missing)}")

    upstream = data["upstream"]
    hf = data["hugging_face"]
    if upstream.get("github_repository") != "https://github.com/microsoft/TRELLIS.2":
        raise ValueError("TRELLIS.2 must point to Microsoft's official GitHub repository")
    if not SHA40.fullmatch(str(upstream.get("github_commit", ""))):
        raise ValueError("TRELLIS.2 github_commit must be a full 40-character SHA")
    if hf.get("model_id") != "microsoft/TRELLIS.2-4B":
        raise ValueError("Unexpected TRELLIS.2 Hugging Face model id")
    if hf.get("space_id") != "microsoft/TRELLIS.2":
        raise ValueError("Unexpected TRELLIS.2 Hugging Face Space id")
    return data


def validate_image(path: str | Path) -> Path:
    image = Path(path).expanduser().resolve()
    if not image.is_file():
        raise FileNotFoundError(f"Input image does not exist: {image}")
    if image.suffix.lower() not in SUPPORTED_IMAGE_SUFFIXES:
        raise ValueError(
            f"Unsupported input image type {image.suffix!r}; "
            f"use one of {sorted(SUPPORTED_IMAGE_SUFFIXES)}"
        )
    return image


def local_runtime_status(system: str | None = None) -> dict[str, Any]:
    cfg = load_config()
    detected = system or platform.system()
    supported_os = cfg["execution"]["official_local_os"]
    return {
        "detected_os": detected,
        "official_local_os": supported_os,
        "os_supported": detected == supported_os,
        "gpu_requirement": f"NVIDIA GPU with >= {cfg['execution']['minimum_vram_gb']} GB VRAM",
        "recommended_cuda": cfg["execution"]["recommended_cuda"],
    }


def tool_status() -> dict[str, Any]:
    cfg = load_config()
    return {
        "tool_id": cfg["tool_id"],
        "name": cfg["name"],
        "source": cfg["upstream"]["github_repository"],
        "pinned_commit": cfg["upstream"]["github_commit"],
        "hf_model": cfg["hugging_face"]["model_id"],
        "hf_space": cfg["hugging_face"]["space_id"],
        "default_route": cfg["execution"]["default_route"],
        "hf_token_present": bool(os.getenv("HF_TOKEN")),
        "local_runtime": local_runtime_status(),
    }


def clone_command() -> str:
    cfg = load_config()
    repo = cfg["upstream"]["github_repository"]
    sha = cfg["upstream"]["github_commit"]
    return (
        f"git clone --recursive {repo}.git TRELLIS.2 && "
        f"cd TRELLIS.2 && git checkout {sha} && git submodule update --init --recursive"
    )


def probe_hf_space() -> Any:
    """Return the official Space API description using an optional HF_TOKEN.

    gradio_client is kept as a tool-local optional dependency so the core Concrete
    Motivation application remains lightweight.
    """
    try:
        from gradio_client import Client  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "gradio_client is not installed. Install tools/trellis2/requirements.txt first."
        ) from exc

    cfg = load_config()
    token = os.getenv("HF_TOKEN") or None
    client = Client(cfg["hugging_face"]["space_id"], token=token)
    return client.view_api(print_info=False, return_format="dict")


def main() -> int:
    parser = argparse.ArgumentParser(description="TRELLIS.2 integration helper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Show pinned source/model/runtime status")
    sub.add_parser("clone-command", help="Print the reproducible upstream clone command")
    check = sub.add_parser("check-image", help="Validate an image input")
    check.add_argument("image")
    sub.add_parser("probe-space", help="Inspect the official Hugging Face Space API")
    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps(tool_status(), indent=2))
    elif args.command == "clone-command":
        print(clone_command())
    elif args.command == "check-image":
        print(validate_image(args.image))
    elif args.command == "probe-space":
        print(json.dumps(probe_hf_space(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
