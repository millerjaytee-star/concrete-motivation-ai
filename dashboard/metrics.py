"""Aggregate metrics for the Concrete Motivation executive dashboard."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .content_metrics import ContentMetrics, build_content_metrics
from .crm_metrics import CRMMetrics, build_crm_metrics
from .revenue_metrics import RevenueMetrics, build_revenue_metrics


@dataclass(frozen=True, slots=True)
class DashboardMetrics:
    content: ContentMetrics
    crm: CRMMetrics
    revenue: RevenueMetrics

    def as_rows(self) -> tuple[tuple[str, str], ...]:
        return self.content.as_rows() + self.crm.as_rows() + self.revenue.as_rows()

    def weekly_scoreboard_rows(self) -> tuple[tuple[str, str], ...]:
        return self.content.weekly_scoreboard_rows() + self.crm.as_rows() + self.revenue.as_rows()

    def as_markdown(self) -> str:
        rows = "\n".join(f"| {label} | {value} |" for label, value in self.as_rows())
        scoreboard = "\n".join(f"- {label}: {value}" for label, value in self.weekly_scoreboard_rows())
        return f"""# Concrete Motivation Executive Dashboard

| Metric | Value |
|---|---:|
{rows}

## Weekly Scoreboard
{scoreboard}
"""


def build_dashboard_metrics(root: Path | str | None = None) -> DashboardMetrics:
    return DashboardMetrics(
        content=build_content_metrics(root),
        crm=build_crm_metrics(root),
        revenue=build_revenue_metrics(root),
    )
