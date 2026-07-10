from __future__ import annotations

import sys

from concrete_motivation.membership_program import build_membership_program, save_membership_program
from scripts import create_membership_program


def test_membership_program_writes_requested_assets(tmp_path):
    program = build_membership_program(
        offer="Concrete Builders Membership",
        monthly_price=40,
        annual_price=400,
        premium_annual_price=444,
        audience="students and fathers",
    )
    result = save_membership_program(program, output_dir=tmp_path)

    assert len(result.created_paths) == 10
    names = {path.name for path in result.created_paths}
    assert "00_membership_sales_page.md" in names
    assert "09_weekly_challenge_template.md" in names
    assert "Join Concrete Builders Membership" in result.created_paths[0].read_text(encoding="utf-8")


def test_membership_program_script_runs(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "create_membership_program.py",
            "--monthly-price",
            "40",
            "--annual-price",
            "400",
            "--premium-annual-price",
            "444",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert create_membership_program.main() == 0
    output = capsys.readouterr().out
    assert "Membership Program Complete" in output
