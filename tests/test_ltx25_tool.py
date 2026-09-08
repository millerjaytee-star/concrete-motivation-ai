import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "ltx25" / "ltx25_tool.py"
CONFIG = ROOT / "tools" / "ltx25" / "config.json"

spec = importlib.util.spec_from_file_location("ltx25_tool", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


def test_config_points_to_official_sources():
    cfg = json.loads(CONFIG.read_text())
    assert cfg["upstream_repository"] == "https://github.com/Lightricks/LTX-2"
    assert cfg["hugging_face_model"] == "Lightricks/LTX-2.5"
    assert cfg["hugging_face_space"] == "Lightricks/LTX-2.5"


def test_upstream_commit_is_full_sha():
    cfg = mod.load_config()
    mod.validate_config(cfg)
    assert len(cfg["upstream_commit"]) == 40


def test_distilled_checkpoint_is_exact_official_component():
    cfg = mod.load_config()
    assert cfg["distilled_transformer"].endswith(
        "ltx-2.5-22b-distilled-transformer-bf16.safetensors"
    )


def test_download_command_uses_gated_official_repo():
    cmd = mod.build_hf_download_command()
    assert cmd[:3] == ["hf", "download", "Lightricks/LTX-2.5"]
    assert "--local-dir" in cmd


def test_distilled_command_builds_audio_video_pipeline():
    cmd = mod.build_distilled_command("Build from pressure.", output_path="test.mp4")
    joined = " ".join(cmd)
    assert "ltx_pipelines.distilled" in joined
    assert "--audio-vae-path" in cmd
    assert "--video-vae-path" in cmd
    assert cmd[-2:] == ["--prompt", "Build from pressure."]


def test_empty_prompt_is_rejected():
    try:
        mod.build_distilled_command("   ")
    except ValueError as exc:
        assert "prompt" in str(exc)
    else:
        raise AssertionError("empty prompt should fail")


def test_clone_and_checkout_are_pinned():
    cfg = mod.load_config()
    clone = mod.build_clone_command()
    checkout = mod.build_checkout_command()
    assert cfg["upstream_repository"] in clone
    assert checkout[-1] == cfg["upstream_commit"]


def test_status_report_has_runtime_guardrail():
    report = mod.status_report()
    assert report["model_access"] == "gated"
    assert "recommended_execution" in report["runtime"]
