"""System checks for the Concrete Motivation command center."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path

from concrete_motivation.bot_registry import list_bots
from concrete_motivation.bot_runner import BotRunner
from concrete_motivation.output_vault import BOT_OUTPUT_FOLDERS


@dataclass(frozen=True, slots=True)
class SystemCheckResult:
    """Structured result from a local system check."""

    passed: tuple[str, ...]
    failed: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.failed

    def as_markdown(self) -> str:
        status = "PASS" if self.ok else "FAIL"
        lines = [f"# Concrete Motivation System Check: {status}"]
        if self.passed:
            lines.append("\n## Passed")
            lines.extend(f"- {item}" for item in self.passed)
        if self.failed:
            lines.append("\n## Failed")
            lines.extend(f"- {item}" for item in self.failed)
        if self.warnings:
            lines.append("\n## Warnings")
            lines.extend(f"- {item}" for item in self.warnings)
        return "\n".join(lines)


def run_system_check() -> SystemCheckResult:
    """Validate imports, prompts, vault mappings, and offline bot execution."""
    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []
    root = Path(__file__).resolve().parent.parent

    for module_name in (
        "main",
        "concrete_motivation.app",
        "concrete_motivation.bot_registry",
        "concrete_motivation.bot_runner",
        "concrete_motivation.providers.offline_provider",
        "concrete_motivation.output_vault",
    ):
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            failed.append(f"Import failed: {module_name} ({exc})")
        else:
            passed.append(f"Import ok: {module_name}")

    bots = list_bots()
    if bots:
        passed.append(f"Registered bots: {len(bots)}")
    else:
        failed.append("No bots registered.")

    bot_slugs = {bot.slug for bot in bots}
    folder_slugs = set(BOT_OUTPUT_FOLDERS)
    missing_folders = sorted(bot_slugs - folder_slugs)
    extra_folders = sorted(folder_slugs - bot_slugs)
    if missing_folders:
        failed.append(f"Missing output folders for: {', '.join(missing_folders)}")
    else:
        passed.append("Every bot has an output vault mapping.")
    if extra_folders:
        failed.append(f"Output vault mappings without registered bots: {', '.join(extra_folders)}")

    runner = BotRunner()
    for bot in bots:
        if not bot.prompt_file.is_file():
            failed.append(f"Prompt missing: {bot.slug} -> {bot.prompt_file}")
            continue
        if not bot.prompt_file.read_text(encoding="utf-8").strip().startswith("# "):
            failed.append(f"Prompt invalid or empty: {bot.prompt_file}")
            continue
        try:
            response = runner.run(bot, "system check")
        except Exception as exc:
            failed.append(f"Offline run failed: {bot.slug} ({exc})")
        else:
            headings = {heading for heading, _body in response.sections}
            missing_sections = [section for section in bot.sections if section not in headings]
            if missing_sections:
                failed.append(f"Response missing sections for {bot.slug}: {', '.join(missing_sections)}")
            else:
                passed.append(f"Offline run ok: {bot.slug}")

    for folder_name in sorted(set(BOT_OUTPUT_FOLDERS.values())):
        folder = root / "outputs" / folder_name
        if folder.is_dir():
            passed.append(f"Output folder ok: outputs/{folder_name}")
        else:
            failed.append(f"Output folder missing: outputs/{folder_name}")

    housekeeping_paths = (
        root / ".DS_Store",
        root / "code concrete_motivation" / "bot_registry.py",
    )
    for path in housekeeping_paths:
        if path.exists():
            warnings.append(f"Housekeeping issue present: {path.relative_to(root)}")

    generated_video_dir = root / "generated_videos"
    if generated_video_dir.exists() and any(generated_video_dir.glob("*.mp4")):
        warnings.append("Generated MP4 files are present; keep an eye on repository size before future commits.")

    markdown_prompt_dirs = [path for path in (root / "prompts").glob("*.md") if path.is_dir()]
    if markdown_prompt_dirs:
        formatted = ", ".join(str(path.relative_to(root)) for path in sorted(markdown_prompt_dirs))
        warnings.append(f"Prompt paths shaped like Markdown files but stored as directories: {formatted}")

    return SystemCheckResult(tuple(passed), tuple(failed), tuple(warnings))
