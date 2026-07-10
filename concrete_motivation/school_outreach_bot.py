"""School outreach workflow for Concrete Motivation."""

from __future__ import annotations

import json
import csv
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


@dataclass(frozen=True, slots=True)
class SchoolOutreachResult:
    theme: str
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# School Outreach Complete\n\n"
            f"**Theme:** {self.theme}\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


class SchoolOutreachBot:
    """Create school outreach assets for speaking and partnerships."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parent.parent / "outputs" / "outreach_messages" / "school_outreach"

    def run(self, theme: str, audience: str = "high school athletes", region: str = "") -> SchoolOutreachResult:
        clean_theme = theme.strip() or "Built Under Pressure"
        clean_audience = audience.strip() or "high school athletes"
        clean_region = region.strip()
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder_name = f"{stamp}-{slugify(clean_theme)}"
        if clean_region:
            folder_name = f"{folder_name}-{slugify(clean_region)}"
        folder = self.root / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        files = {
            "00_school_outreach_package.md": self._readme(clean_theme, clean_audience, clean_region),
            "00_school_outreach_package.json": json.dumps(self._package_dict(clean_theme, clean_audience, clean_region), indent=2),
            "01_lead_template.csv": self._lead_csv(clean_theme, clean_audience, clean_region),
            "02_initial_message.md": self._initial_message(clean_theme, clean_audience, clean_region),
            "03_follow_up_1.md": self._follow_up_one(clean_theme, clean_audience, clean_region),
            "04_follow_up_2.md": self._follow_up_two(clean_theme, clean_audience, clean_region),
            "05_call_script.md": self._call_script(clean_theme, clean_audience, clean_region),
            "06_crm_import_row.csv": self._crm_import_row(clean_theme, clean_audience, clean_region),
            "README.md": self._readme(clean_theme, clean_audience, clean_region),
        }
        paths: list[Path] = []
        for filename, body in files.items():
            path = folder / filename
            if filename.endswith(".json"):
                path.write_text(body + "\n", encoding="utf-8")
            else:
                path.write_text(body.strip() + "\n", encoding="utf-8")
            paths.append(path)
        return SchoolOutreachResult(clean_theme, clean_audience, tuple(paths))

    def _package_dict(self, theme: str, audience: str, region: str) -> dict[str, str]:
        return {
            "theme": theme,
            "audience": audience,
            "region": region,
            "initial_message": self._initial_message(theme, audience, region),
            "follow_up_1": self._follow_up_one(theme, audience, region),
            "follow_up_2": self._follow_up_two(theme, audience, region),
            "call_script": self._call_script(theme, audience, region),
        }

    def _readme(self, theme: str, audience: str, region: str = "") -> str:
        return f"""# School Outreach Package

## Theme
{theme}

## Audience
{audience}

## Region
{region or "n/a"}

## Purpose
Open doors with schools, athletic directors, coaches, counselors, and youth leaders.

## Files
- Markdown package
- JSON package
- Lead CSV template
- Initial message
- Follow-up 1
- Follow-up 2
- Call script
- CRM import row format
"""

    def _lead_csv(self, theme: str, audience: str, region: str = "") -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "school_name",
                "contact_name",
                "role",
                "email",
                "phone",
                "city",
                "state",
                "fit_score",
                "status",
                "next_action",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "school_name": f"{region or 'Local'} School",
                "contact_name": "Athletic Director",
                "role": "athletic_director",
                "fit_score": "5",
                "status": "new",
                "next_action": "send intro email",
                "notes": f"{theme} for {audience} {region}".strip(),
            }
        )
        writer.writerow(
            {
                "school_name": f"{region or 'Local'} School",
                "role": "principal",
                "fit_score": "4",
                "status": "new",
                "next_action": "research school priorities",
            }
        )
        writer.writerow(
            {
                "school_name": f"{region or 'Local'} School",
                "role": "coach",
                "fit_score": "4",
                "status": "new",
                "next_action": "call office",
            }
        )
        return buffer.getvalue()

    def _initial_message(self, theme: str, audience: str, region: str = "") -> str:
        return f"""# School Outreach Email

Subject: Speaking opportunity for {audience}{f" in {region}" if region else ""}

Hello,

My name is Jaytee Miller, founder of Concrete Motivation. I am reaching out to share a speaking experience built around {theme}, discipline, consistency, faith, and refusing to quit when life gets hard.

Concrete Motivation is designed to connect with students and leaders who need a message that is practical, direct, and grounded in real life.

I would love to connect about bringing this message to your school, program, or team.

Respectfully,
Jaytee Miller
Concrete Motivation
"""

    def _follow_up_one(self, theme: str, audience: str, region: str = "") -> str:
        return f"""# Follow-Up Sequence

## Follow-Up 1
Following up in case this got buried.

I can send a one-page outline for a short session built around {theme} for {audience}{f" in {region}" if region else ""}.

Would next week be a good time for a quick conversation?
"""

    def _follow_up_two(self, theme: str, audience: str, region: str = "") -> str:
        return f"""# Follow-Up 2

If now is not the right time, should I reconnect before your next assembly, leadership event, sports season, or student program?

I appreciate your time either way.
"""

    def _call_script(self, theme: str, audience: str, region: str = "") -> str:
        return f"""# Call Script

Hello, my name is Jaytee Miller with Concrete Motivation.

I am calling because I want to share a speaking message built around {theme} for {audience}{f" in {region}" if region else ""}.
The message is direct, practical, and focused on discipline, faith, consistency, and real action.

If you are the right person to speak with, I would love to ask about the best next step for bringing this to your school.

Thank you for your time.
"""

    def _crm_import_row(self, theme: str, audience: str, region: str = "") -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "school_name",
                "contact_name",
                "role",
                "email",
                "phone",
                "stage",
                "next_follow_up_date",
                "source",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "school_name": f"{region or 'Local'} School",
                "contact_name": "Athletic Director",
                "role": "athletic_director",
                "stage": "New Lead",
                "source": "School Outreach Campaign",
                "notes": f"{theme} for {audience} {region}".strip(),
            }
        )
        return buffer.getvalue()
