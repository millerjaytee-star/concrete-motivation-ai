from __future__ import annotations

import sys

from concrete_motivation.content_batch_runner import create_30_day_content_batch, create_reels_batch
from scripts import create_30_day_content_batch as create_30_day_script
from scripts import create_content_package as create_content_package_script
from scripts import create_reels_batch as create_reels_script


def test_reels_batch_creates_requested_count(tmp_path):
    result = create_reels_batch("one brick at a time", 3, audience="high school athletes", output_dir=tmp_path)

    assert len(result.packages) == 3
    assert len(result.exports) == 3
    assert all(export.folder.is_dir() for export in result.exports)
    assert result.packages[0].topic.startswith("one brick at a time:")


def test_thirty_day_batch_creates_thirty_assets(tmp_path):
    result = create_30_day_content_batch(
        "Pressure Has a Purpose",
        audience="students and fathers",
        output_dir=tmp_path,
    )

    assert len(result.packages) == 30
    assert len(result.exports) == 30
    assert result.packages[-1].topic == "Day 30: Pressure Has a Purpose"


def test_scripts_import_from_scripts_directory(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(sys, "argv", [
        "create_content_package.py",
        "discipline after pressure",
        "--audience",
        "high school athletes",
        "--output-dir",
        str(tmp_path),
    ])
    assert create_content_package_script.main() == 0

    monkeypatch.setattr(sys, "argv", [
        "create_reels_batch.py",
        "--theme",
        "one brick at a time",
        "--count",
        "2",
        "--output-dir",
        str(tmp_path),
    ])
    assert create_reels_script.main() == 0

    monkeypatch.setattr(sys, "argv", [
        "create_30_day_content_batch.py",
        "--theme",
        "Pressure Has a Purpose",
        "--audience",
        "students and fathers",
        "--output-dir",
        str(tmp_path),
    ])
    assert create_30_day_script.main() == 0

    output = capsys.readouterr().out
    assert "Saved markdown:" in output
    assert "Saved package:" in output
