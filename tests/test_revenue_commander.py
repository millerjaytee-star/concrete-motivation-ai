from __future__ import annotations

import json
import sys

from concrete_motivation.payment_link_manager import PaymentLinkManager
from concrete_motivation.revenue_commander import RevenueCommander
from scripts import run_revenue_commander


def test_revenue_commander_generates_full_package(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    local = config_dir / "payment_links.local.json"
    local.write_text(
        json.dumps(
            {
                "monthly_payment_link": "https://pay.concretemotivation.test/monthly",
                "annual_payment_link": "https://pay.concretemotivation.test/annual",
                "booking_payment_link": "https://pay.concretemotivation.test/booking",
                "sponsor_payment_link": "https://pay.concretemotivation.test/sponsor",
            }
        ),
        encoding="utf-8",
    )
    manager = PaymentLinkManager(config_path=local, example_path=config_dir / "payment_links.example.json")
    result = RevenueCommander(root=tmp_path, payment_manager=manager).run("Concrete Builders Membership")

    assert len(result.created_paths) == 9
    names = {path.name for path in result.created_paths}
    assert "00_revenue_decision.md" in names
    assert "03_payment_link_map.json" in names
    payment_map = json.loads(result.created_paths[3].read_text(encoding="utf-8"))
    assert payment_map["links"][0]["configured"] is True


def test_revenue_commander_script_runs(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK", "https://pay.concretemotivation.test/monthly")
    monkeypatch.setenv("CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK", "https://pay.concretemotivation.test/annual")
    monkeypatch.setenv("CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK", "https://pay.concretemotivation.test/booking")
    monkeypatch.setenv("CONCRETE_MOTIVATION_SPONSOR_PAYMENT_LINK", "https://pay.concretemotivation.test/sponsor")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_revenue_commander.py",
            "--theme",
            "Concrete Builders Membership",
            "--monthly-price",
            "40",
            "--annual-price",
            "400",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert run_revenue_commander.main() == 0
    output = capsys.readouterr().out
    assert "Revenue Commander Complete" in output
