from __future__ import annotations

import json
import os
import platform
import shlex
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config.json"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def validate_config(config: dict[str, Any]) -> None:
    required = {
        "upstream_repository",
        "upstream_commit",
        "hugging_face_model",
        "hugging_face_space",
        "distilled_transformer",
        "text_encoder",
        "video_vae",
        "audio_vae",
        "spatial_upscaler",
    }
    missing = sorted(required.difference(config))
    if missing:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing)}")
    if len(config["upstream_commit"]) != 40:
        raise ValueError("upstream_commit must be a full 40-character Git SHA")
    if not config["distilled_transformer"].endswith(".safetensors"):
        raise ValueError("distilled_transformer must point to a safetensors checkpoint")


def local_runtime_status() -> dict[str, Any]:
    system = platform.system()
    machine = platform.machine()
    is_darwin = system == "Darwin"
    is_intel_mac = is_darwin and machine in {"x86_64", "i386"}
    return {
        "system": system,
        "machine": machine,
        "supported_for_heavy_local_install": not is_intel_mac,
        "recommended_execution": (
            "Hugging Face Space or Linux/NVIDIA cloud GPU"
            if is_intel_mac
            else "Hugging Face Space first; validate GPU before local install"
        ),
    }


def require_model_terms_acknowledged() -> None:
    if os.getenv("LTX25_TERMS_ACCEPTED", "").lower() not in {"1", "true", "yes"}:
        raise RuntimeError(
            "LTX-2.5 is a gated Hugging Face model. Accept the model terms on "
            "Hugging Face before attempting checkpoint download."
        )


def build_clone_command(destination: str = "vendor/LTX-2") -> list[str]:
    cfg = load_config()
    validate_config(cfg)
    return [
        "git", "clone", cfg["upstream_repository"], destination,
        "--no-checkout",
    ]


def build_checkout_command(destination: str = "vendor/LTX-2") -> list[str]:
    cfg = load_config()
    return ["git", "-C", destination, "checkout", cfg["upstream_commit"]]


def build_hf_download_command(local_dir: str = "models/ltx-2.5") -> list[str]:
    cfg = load_config()
    validate_config(cfg)
    return [
        "hf", "download", cfg["hugging_face_model"],
        cfg["distilled_transformer"],
        cfg["text_encoder"],
        cfg["video_vae"],
        cfg["audio_vae"],
        cfg["spatial_upscaler"],
        "--local-dir", local_dir,
    ]


def build_distilled_command(
    prompt: str,
    output_path: str = "output.mp4",
    models_dir: str = "models/ltx-2.5",
    num_frames: int = 121,
    seed: int = 42,
) -> list[str]:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if num_frames < 1:
        raise ValueError("num_frames must be >= 1")
    cfg = load_config()
    return [
        "uv", "run", "python", "-m", "ltx_pipelines.distilled",
        "--transformer-path", f"{models_dir}/{cfg['distilled_transformer']}",
        "--text-encoder-path", f"{models_dir}/{cfg['text_encoder']}",
        "--video-vae-path", f"{models_dir}/{cfg['video_vae']}",
        "--audio-vae-path", f"{models_dir}/{cfg['audio_vae']}",
        "--spatial-upsampler-path", f"{models_dir}/{cfg['spatial_upscaler']}",
        "--num-frames", str(num_frames),
        "--seed", str(seed),
        "--output-path", output_path,
        "--prompt", prompt,
    ]


def shell(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def status_report() -> dict[str, Any]:
    cfg = load_config()
    validate_config(cfg)
    return {
        "tool": cfg["name"],
        "upstream_commit": cfg["upstream_commit"],
        "hugging_face_model": cfg["hugging_face_model"],
        "hugging_face_space": cfg["hugging_face_space"],
        "checkpoint": cfg["distilled_transformer"],
        "model_access": cfg["model_access"],
        "runtime": local_runtime_status(),
    }


if __name__ == "__main__":
    print(json.dumps(status_report(), indent=2))
