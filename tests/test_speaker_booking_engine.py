from __future__ import annotations

import csv
import sys

from concrete_motivation.speaker_booking_engine import build_speaker_booking_package, save_speaker_booking_package
from scripts import create_speaker_booking_package


def test_speaker_booking_package_builds_segment_assets(tmp_path):
    package = build_speaker_booking_package(segment="schools", theme="Pressure Has a Purpose")
    result = save_speaker_booking_package(package, output_dir=tmp_path)

    assert len(result.created_paths) == 10
    names = {path.name for path in result.created_paths}
    assert "00_speaker_booking_package.md" in names
    assert "08_crm_import_row.csv" in names
    rows = list(csv.DictReader(result.created_paths[8].read_text(encoding="utf-8").splitlines()))
    assert rows[0]["stage"] == "New Lead"


def test_speaker_booking_package_script_runs(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_speaker_booking_package.py",
            "--segment",
            "schools",
            "--theme",
            "Pressure Has a Purpose",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert create_speaker_booking_package.main() == 0
    output = capsys.readouterr().out
    assert "Speaker Booking Package Complete" in output
