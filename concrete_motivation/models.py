"""Core data models for bots and their responses."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Bot:
    """Metadata for one specialist on the Concrete Motivation bot team."""

    id: int
    slug: str
    name: str
    purpose: str
    prompt_file: Path
    sections: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BotResponse:
    """A bot's ordered, structured response."""

    bot_name: str
    goal: str
    sections: tuple[tuple[str, str], ...]

    def as_markdown(self) -> str:
        """Render the response for the terminal or a future export."""
        blocks = [f"# {self.bot_name}", f"**Goal:** {self.goal}"]
        blocks.extend(f"## {heading}\n{body}" for heading, body in self.sections)
        return "\n\n".join(blocks)
