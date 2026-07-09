"""Generate simple placeholder vertical video assets for the first 3 Concrete Motivation reels.

This script creates text-based MP4 files locally. Use them as drafts/placeholders,
then replace with real recorded video when ready.

Run:
    python3 scripts/make_first_3_reels.py

Outputs:
    generated_videos/01_built_under_pressure.mp4
    generated_videos/02_discipline_after_motivation_leaves.mp4
    generated_videos/03_the_leadership_standard.mp4

Requires:
    pip install moviepy pillow
"""
from __future__ import annotations

from pathlib import Path
import textwrap

from moviepy.editor import ColorClip, CompositeVideoClip, TextClip

WIDTH, HEIGHT = 1080, 1920
DURATION = 18
BG = (7, 7, 7)
GOLD = "#c49a45"
WHITE = "#f7f4ed"

VIDEOS = [
    {
        "filename": "01_built_under_pressure.mp4",
        "title": "BUILT UNDER PRESSURE",
        "hook": "You are not weak.\nYou are under construction.",
        "body": "Concrete does not become strong without pressure. Today, do one disciplined thing your future self will thank you for.",
    },
    {
        "filename": "02_discipline_after_motivation_leaves.mp4",
        "title": "DISCIPLINE AFTER MOTIVATION LEAVES",
        "hook": "Motivation starts the fire.\nDiscipline keeps the lights on.",
        "body": "Discipline is keeping the promise after the emotion disappears. Pick one promise today. Keep it.",
    },
    {
        "filename": "03_the_leadership_standard.mp4",
        "title": "THE LEADERSHIP STANDARD",
        "hook": "The people depending on you need consistency more than excuses.",
        "body": "Leadership starts with the promises nobody sees you keep. Be present. Be accountable. Be disciplined.",
    },
]


def text_clip(text: str, fontsize: int, color: str, y: int, max_width: int = 28) -> TextClip:
    wrapped = "\n".join(textwrap.wrap(text, width=max_width))
    return (
        TextClip(wrapped, fontsize=fontsize, color=color, font="Arial-Bold", method="caption", size=(940, None), align="center")
        .set_position((70, y))
        .set_duration(DURATION)
    )


def make_video(item: dict[str, str], output_dir: Path) -> Path:
    bg = ColorClip((WIDTH, HEIGHT), color=BG, duration=DURATION)
    title = text_clip(item["title"], 74, GOLD, 220, 22)
    hook = text_clip(item["hook"], 88, WHITE, 560, 20)
    body = text_clip(item["body"], 54, WHITE, 1060, 30)
    brand = text_clip("CONCRETE MOTIVATION", 42, GOLD, 1640, 24)
    cta = text_clip("Built under pressure. Proven through purpose.", 36, WHITE, 1710, 34)
    video = CompositeVideoClip([bg, title, hook, body, brand, cta])
    output = output_dir / item["filename"]
    video.write_videofile(str(output), fps=24, codec="libx264", audio=False)
    return output


def main() -> None:
    output_dir = Path("generated_videos")
    output_dir.mkdir(exist_ok=True)
    for item in VIDEOS:
        path = make_video(item, output_dir)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
