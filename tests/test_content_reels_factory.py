from __future__ import annotations

import csv
import json
import socket
from pathlib import Path

from concrete_motivation.content_reels_factory import create_content_package, save_content_package
from concrete_motivation.reels_script_writer import build_content_package


def test_content_package_generates_all_required_fields():
    package = build_content_package("discipline after pressure", "high school athletes")

    rendered = package.as_markdown()
    assert package.topic == "discipline after pressure"
    assert package.audience == "high school athletes"
    assert "YouTube Concept" in rendered
    assert "60-Second Reel Script" in rendered
    assert "30-Second Short Script" in rendered
    assert "Podcast Segment" in rendered
    assert package.youtube_tags
    assert package.repurpose_plan


def test_save_content_package_writes_markdown_json_and_csv(tmp_path):
    package = build_content_package("pressure builds discipline", "students and fathers")
    export = save_content_package(package, output_dir=tmp_path, label="test-package")

    assert export.folder.is_dir()
    assert export.markdown_path.read_text(encoding="utf-8").startswith("# Concrete Motivation Content Package")
    payload = json.loads(export.json_path.read_text(encoding="utf-8"))
    assert payload["topic"] == "pressure builds discipline"
    assert payload["audience"] == "students and fathers"

    rows = list(csv.DictReader(export.csv_path.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 1
    assert rows[0]["topic"] == "pressure builds discipline"
    assert rows[0]["call_to_action"]


def test_create_content_package_saves_package_without_network(tmp_path, monkeypatch):
    def fail(*_args, **_kwargs):
        raise AssertionError("network access is not expected")

    monkeypatch.setattr(socket, "create_connection", fail)

    package, export = create_content_package(
        "one brick at a time",
        audience="high school athletes",
        output_dir=tmp_path,
    )

    assert export.folder.exists()
    assert package.long_form_youtube_title.startswith("Pressure Has a Purpose:")
    assert not list(Path(tmp_path).glob("**/*.mp4"))
