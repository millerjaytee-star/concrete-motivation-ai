"""Launch readiness checks and safety policy for the championship build."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent

PRIVATE_ONLY_VISIBILITY = "private"
FORBIDDEN_DEFAULT_ACTIONS = (
    "send_gmail",
    "publish_public_youtube_video",
    "create_live_stripe_charge",
    "commit_secret",
)

SYSTEMS = (
    "CEO Bot",
    "YouTube",
    "Gmail",
    "Website",
    "Stripe",
    "ElevenLabs",
    "FFmpeg",
    "CRM",
    "Dashboard",
    "Social Handoff",
)


@dataclass(frozen=True, slots=True)
class IntegrationCheck:
    """One launch-system verification result."""

    name: str
    status: str
    detail: str
    next_action: str

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "next_action": self.next_action,
        }


@dataclass(frozen=True, slots=True)
class LaunchVerificationReport:
    """A full launch readiness report."""

    checks: tuple[IntegrationCheck, ...]

    @property
    def upload_policy(self) -> dict[str, str | tuple[str, ...]]:
        return {
            "youtube_visibility": PRIVATE_ONLY_VISIBILITY,
            "blocked_actions": FORBIDDEN_DEFAULT_ACTIONS,
            "upload_limit": "one video per explicit verification run",
        }

    @property
    def overall_status(self) -> str:
        if any(check.status == "blocked" for check in self.checks):
            return "blocked"
        if any(check.status == "manual_action_required" for check in self.checks):
            return "manual_action_required"
        return "ready"

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "upload_policy": self.upload_policy,
            "checks": [check.as_dict() for check in self.checks],
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2, sort_keys=True)

    def as_markdown(self) -> str:
        lines = [
            "# Championship Launch Verification",
            "",
            f"Overall status: **{self.overall_status}**",
            "",
            "## Safety Policy",
            "",
            f"- YouTube visibility: `{PRIVATE_ONLY_VISIBILITY}`",
            "- Upload limit: one video per explicit verification run",
            "- Gmail sends, public video publishing, live Stripe charges, and secrets commits are blocked by default.",
            "",
            "## System Checks",
            "",
        ]
        for check in self.checks:
            lines.extend(
                (
                    f"### {check.name}",
                    f"- Status: `{check.status}`",
                    f"- Detail: {check.detail}",
                    f"- Next action: {check.next_action}",
                    "",
                )
            )
        return "\n".join(lines).strip() + "\n"


def command_available(name: str) -> bool:
    """Return whether an executable exists on PATH."""
    return shutil.which(name) is not None


def command_version(command: tuple[str, ...]) -> str:
    """Run a local version command without raising into the caller."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}"
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else f"exit code {result.returncode}"


def verify_launch_system(root: Path = ROOT) -> LaunchVerificationReport:
    """Verify local launch readiness without sending, charging, or publishing."""
    checks = [
        _check_ceo_bot(root),
        _check_youtube(root),
        _check_gmail(),
        _check_website(root),
        _check_stripe(),
        _check_elevenlabs(),
        _check_ffmpeg(),
        _check_crm(root),
        _check_dashboard(root),
        _check_social_handoff(root),
    ]
    return LaunchVerificationReport(tuple(checks))


def _check_ceo_bot(root: Path) -> IntegrationCheck:
    prompt = root / "prompts" / "ceo_bot.md"
    if prompt.is_file() and "Do not publish public videos" in prompt.read_text(encoding="utf-8"):
        return IntegrationCheck("CEO Bot", "ready", "CEO Bot prompt and safety controls are present.", "Use bot 9 for launch orchestration.")
    return IntegrationCheck("CEO Bot", "blocked", "CEO Bot prompt is missing or incomplete.", "Restore prompts/ceo_bot.md.")


def _check_youtube(root: Path) -> IntegrationCheck:
    script = root / "scripts" / "test_youtube_upload.py"
    docs = root / "docs" / "YOUTUBE_PUBLISHING_VERIFICATION.md"
    if script.is_file() and docs.is_file():
        return IntegrationCheck(
            "YouTube",
            "manual_action_required",
            "Private-only verification harness is installed; OAuth/upload requires an explicit operator run.",
            "Run scripts/test_youtube_upload.py first in dry-run mode, then use --execute only after reviewing metadata.",
        )
    return IntegrationCheck("YouTube", "blocked", "YouTube verification script or docs are missing.", "Add the private-only upload harness.")


def _check_gmail() -> IntegrationCheck:
    return IntegrationCheck(
        "Gmail",
        "manual_action_required",
        "Launch system is allowed to prepare outreach copy only; no email send command is automated.",
        "Keep Gmail work in draft/review until explicit send approval is given.",
    )


def _check_website(root: Path) -> IntegrationCheck:
    required = (root / "website" / "index.html", root / "website" / "styles.css", root / "website" / "script.js")
    if all(path.is_file() for path in required):
        return IntegrationCheck("Website", "ready", "Static website files exist and tests cover the booking form.", "Preview website/index.html before external launch.")
    return IntegrationCheck("Website", "blocked", "One or more static website files are missing.", "Restore website files and rerun tests.")


def _check_stripe() -> IntegrationCheck:
    return IntegrationCheck(
        "Stripe",
        "manual_action_required",
        "Revenue path is documented, but no live payment links or charges are created by this repo.",
        "Add Stripe links manually after offer/pricing approval; keep secrets out of Git.",
    )


def _check_elevenlabs() -> IntegrationCheck:
    return IntegrationCheck(
        "ElevenLabs",
        "manual_action_required",
        "Voice production is treated as an external manual step; no API key or generated voice file is committed.",
        "Generate approved narration outside Git and store only final non-secret assets.",
    )


def _check_ffmpeg() -> IntegrationCheck:
    if command_available("ffmpeg"):
        return IntegrationCheck("FFmpeg", "ready", f"FFmpeg is available: {command_version(('ffmpeg', '-version'))}", "Use FFmpeg for local render checks before uploads.")
    return IntegrationCheck("FFmpeg", "manual_action_required", "ffmpeg is not on PATH for this shell.", "Install or add FFmpeg to PATH before video production.")


def _check_crm(root: Path) -> IntegrationCheck:
    template = root / "crm" / "lead_pipeline_template.csv"
    if template.is_file():
        return IntegrationCheck("CRM", "ready", "CRM lead pipeline template is present.", "Copy the template for live leads; do not commit private lead data.")
    return IntegrationCheck("CRM", "blocked", "CRM template is missing.", "Restore crm/lead_pipeline_template.csv.")


def _check_dashboard(root: Path) -> IntegrationCheck:
    dashboard = root / "dashboard" / "launch_dashboard.html"
    if dashboard.is_file():
        return IntegrationCheck("Dashboard", "ready", "Local launch dashboard is present.", "Open dashboard/launch_dashboard.html during launch review.")
    return IntegrationCheck("Dashboard", "blocked", "Launch dashboard is missing.", "Restore dashboard/launch_dashboard.html.")


def _check_social_handoff(root: Path) -> IntegrationCheck:
    handoff = root / "social_handoff" / "launch_handoff.md"
    if handoff.is_file():
        return IntegrationCheck("Social Handoff", "ready", "Social handoff checklist is present.", "Use the checklist to review assets before posting manually.")
    return IntegrationCheck("Social Handoff", "blocked", "Social handoff document is missing.", "Restore social_handoff/launch_handoff.md.")

