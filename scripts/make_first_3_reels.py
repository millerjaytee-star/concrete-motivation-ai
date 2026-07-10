"""Generate simple vertical MP4 assets for the first 3 Concrete Motivation reels.

Run from the project root:
    python scripts/make_first_3_reels.py

Outputs:
    generated_videos/01_built_under_pressure.mp4
    generated_videos/02_discipline_after_motivation_leaves.mp4
    generated_videos/03_the_leadership_standard.mp4

Requires:
    python -m pip install pillow imageio imageio-ffmpeg

This version intentionally avoids MoviePy because newer MoviePy releases changed
import paths on some Macs. Pillow + imageio is simpler and more reliable here.
"""
from __future__ import annotations

import argparse
import os
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import imageio.v2 as imageio
    import imageio_ffmpeg
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
except ImportError as exc:  # pragma: no cover - depends on optional local media packages.
    raise SystemExit(
        "Missing video dependencies. Run: python3 -m pip install pillow imageio imageio-ffmpeg"
    ) from exc

from concrete_motivation.ffmpeg_tools import configure_imageio_ffmpeg, ffmpeg_status
from concrete_motivation.ffmpeg_tools import bundled_imageio_ffmpeg_binary, ffmpeg_supports_encoder

WIDTH, HEIGHT = 1080, 1920
DURATION_SECONDS = 12
FPS = 24
BG = (7, 7, 7)
GOLD = (196, 154, 69)
WHITE = (247, 244, 237)
MUTED = (190, 184, 174)

VIDEOS = [
    {
        "filename": "01_built_under_pressure.mp4",
        "title": "BUILT UNDER PRESSURE",
        "hook": "You are not weak. You are under construction.",
        "body": "Concrete does not become strong without pressure. Today, do one disciplined thing your future self will thank you for.",
    },
    {
        "filename": "02_discipline_after_motivation_leaves.mp4",
        "title": "DISCIPLINE AFTER MOTIVATION LEAVES",
        "hook": "Motivation starts the fire. Discipline keeps the lights on.",
        "body": "Discipline is keeping the promise after the emotion disappears. Pick one promise today. Keep it.",
    },
    {
        "filename": "03_the_leadership_standard.mp4",
        "title": "THE LEADERSHIP STANDARD",
        "hook": "The people depending on you need consistency more than excuses.",
        "body": "Leadership starts with the promises nobody sees you keep. Be present. Be accountable. Be disciplined.",
    },
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font: ImageFont.ImageFont,
    color: tuple[int, int, int],
    line_width: int,
    spacing: int = 14,
) -> None:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=line_width) or [""])

    current_y = y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        draw.text((x, current_y), line, font=font, fill=color)
        current_y += (bbox[3] - bbox[1]) + spacing


def make_frame(item: dict[str, str]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    # Border and brand blocks
    draw.rectangle((54, 54, WIDTH - 54, HEIGHT - 54), outline=GOLD, width=6)
    draw.rectangle((80, 80, WIDTH - 80, 210), fill=(18, 18, 18), outline=GOLD, width=2)

    title_font = load_font(66)
    hook_font = load_font(82)
    body_font = load_font(48)
    small_font = load_font(40)
    footer_font = load_font(34)

    draw_centered_text(draw, item["title"], 112, title_font, GOLD, 24, spacing=10)
    draw_centered_text(draw, item["hook"], 520, hook_font, WHITE, 23, spacing=20)
    draw_centered_text(draw, item["body"], 1030, body_font, MUTED, 34, spacing=16)
    draw_centered_text(draw, "CONCRETE MOTIVATION", 1580, small_font, GOLD, 26, spacing=10)
    draw_centered_text(draw, "Built under pressure. Proven through purpose.", 1660, footer_font, WHITE, 40, spacing=8)

    return image


def _write_video(item: dict[str, str], output: Path) -> Path:
    frame = make_frame(item)
    with imageio.get_writer(
        output,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=1,
    ) as writer:
        for _ in range(DURATION_SECONDS * FPS):
            writer.append_data(np.asarray(frame))
    return output
def main() -> None:
    parser = argparse.ArgumentParser(description="Create the first 3 Concrete Motivation reels.")
    parser.add_argument(
        "--ffmpeg-bin",
        default=os.getenv("CONCRETE_MOTIVATION_FFMPEG_BIN", ""),
        help="Preferred ffmpeg binary path or directory",
    )
    args = parser.parse_args()

    resolved = configure_imageio_ffmpeg(args.ffmpeg_bin or None)
    bundled = bundled_imageio_ffmpeg_binary() or Path(imageio_ffmpeg.get_ffmpeg_exe())
    if args.ffmpeg_bin and not ffmpeg_supports_encoder(resolved, "libx264"):
        print(f"Preferred ffmpeg does not support libx264: {resolved}")
        print(f"Falling back to bundled ffmpeg: {bundled}")
        resolved = configure_imageio_ffmpeg(bundled)
    status = ffmpeg_status(args.ffmpeg_bin or None)
    print(status.as_markdown())
    print(f"Using ffmpeg binary: {resolved}")

    output_dir = ROOT / "generated_videos"
    output_dir.mkdir(exist_ok=True)
    for item in VIDEOS:
        path = _write_video(item, output_dir / item["filename"])
        print(f"Created {path}")


if __name__ == "__main__":
    main()
