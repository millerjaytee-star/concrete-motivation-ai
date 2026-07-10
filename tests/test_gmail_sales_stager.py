from __future__ import annotations

import sys

from concrete_motivation.gmail_sales_stager import build_gmail_sales_sequence, save_gmail_sales_sequence
from scripts import stage_membership_gmail_sequence


def test_gmail_sales_sequence_stages_drafts(tmp_path):
    sequence = build_gmail_sales_sequence("Concrete Builders Membership", audience="students and fathers")
    result = save_gmail_sales_sequence(sequence, output_dir=tmp_path)

    assert len(result.created_paths) == 7
    assert result.created_paths[0].name == "01_launch-email.md"
    launch = result.created_paths[0].read_text(encoding="utf-8")
    assert "Suggested Gmail Label" in launch
    assert "CRM Stage" in launch


def test_gmail_sales_sequence_script_runs(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "stage_membership_gmail_sequence.py",
            "--offer",
            "Concrete Builders Membership",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert stage_membership_gmail_sequence.main() == 0
    output = capsys.readouterr().out
    assert "Gmail Membership Sequence Complete" in output
