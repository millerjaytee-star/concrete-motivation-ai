from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "trellis2" / "trellis2_tool.py"
spec = importlib.util.spec_from_file_location("trellis2_tool", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_config_points_to_official_sources_and_full_commit_sha():
    cfg = module.load_config(ROOT / "tools" / "trellis2" / "config.json")
    assert cfg["upstream"]["github_repository"] == "https://github.com/microsoft/TRELLIS.2"
    assert cfg["upstream"]["github_commit"] == "75fbf0183001ed9876c8dbb35de6b68552ee08bd"
    assert cfg["hugging_face"]["model_id"] == "microsoft/TRELLIS.2-4B"
    assert cfg["hugging_face"]["space_id"] == "microsoft/TRELLIS.2"
    assert len(cfg["upstream"]["github_commit"]) == 40


def test_local_runtime_flags_macos_as_not_officially_supported():
    status = module.local_runtime_status(system="Darwin")
    assert status["os_supported"] is False
    assert status["official_local_os"] == "Linux"
    assert "24 GB" in status["gpu_requirement"]


def test_validate_image_accepts_supported_file(tmp_path: Path):
    image = tmp_path / "asset.PNG"
    image.write_bytes(b"not-real-image-but-path-validation-only")
    assert module.validate_image(image) == image.resolve()


def test_validate_image_rejects_unknown_extension(tmp_path: Path):
    bad = tmp_path / "asset.txt"
    bad.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        module.validate_image(bad)


def test_clone_command_is_pinned_not_floating_main():
    command = module.clone_command()
    assert "microsoft/TRELLIS.2" in command
    assert "75fbf0183001ed9876c8dbb35de6b68552ee08bd" in command
    assert "git checkout" in command


def test_config_json_is_valid_json():
    path = ROOT / "tools" / "trellis2" / "config.json"
    json.loads(path.read_text(encoding="utf-8"))


def test_registry_has_unique_approved_trellis2_entry():
    registry = json.loads((ROOT / "tools" / "registry.json").read_text(encoding="utf-8"))
    ids = [tool["id"] for tool in registry["tools"]]
    assert len(ids) == len(set(ids))
    entry = next(tool for tool in registry["tools"] if tool["id"] == "microsoft-trellis2")
    assert entry["status"] == "approved"
    assert entry["integration_path"] == "tools/trellis2/"
    assert entry["hugging_face_model"] == "microsoft/TRELLIS.2-4B"
    assert entry["version_pin"] == "75fbf0183001ed9876c8dbb35de6b68552ee08bd"
