from __future__ import annotations

import sys

from concrete_motivation.revenue_website_pages import build_revenue_website_pages, save_revenue_website_pages
from scripts import update_revenue_website_pages


def test_revenue_website_pages_include_required_sections(monkeypatch, tmp_path):
    monkeypatch.setenv("CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK", "https://pay.concretemotivation.test/monthly")
    monkeypatch.setenv("CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK", "https://pay.concretemotivation.test/annual")
    monkeypatch.setenv("CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK", "https://pay.concretemotivation.test/booking")
    monkeypatch.setenv("CONCRETE_MOTIVATION_SPONSOR_PAYMENT_LINK", "https://pay.concretemotivation.test/sponsor")

    pages = build_revenue_website_pages()
    result = save_revenue_website_pages(tmp_path)

    assert set(pages) == {"membership.md", "speaking.md", "sponsors.md", "book_jaytee.md", "payment_links.md"}
    assert len(result.created_paths) == 5
    membership = (tmp_path / "membership.md").read_text(encoding="utf-8")
    assert "CTA Button Text" in membership
    assert "payment link" in (tmp_path / "payment_links.md").read_text(encoding="utf-8").lower()


def test_update_revenue_website_pages_script_runs(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_revenue_website_pages.py",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert update_revenue_website_pages.main() == 0
    output = capsys.readouterr().out
    assert "Revenue Website Pages Complete" in output
