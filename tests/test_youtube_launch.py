from pathlib import Path


YOUTUBE_DIR = Path(__file__).resolve().parent.parent / "youtube_launch"

REQUIRED_FILES = (
    "CHANNEL_SETUP.md",
    "CHANNEL_COPY.md",
    "VIDEO_TEMPLATES.md",
    "FIRST_10_VIDEOS.md",
    "SHORTS_SYSTEM.md",
    "THUMBNAIL_GUIDE.md",
    "UPLOAD_CHECKLIST.md",
)

FIRST_10_TITLES = (
    "Pressure Has a Purpose",
    "Fatherhood Made Me Build Different",
    "Discipline When Nobody Claps",
    "From Pain to Platform",
    "The Brick-by-Brick Mindset",
    "Stop Waiting to Feel Ready",
    "How to Lead When Life Is Heavy",
    "Athlete Mindset Beyond the Scoreboard",
    "What Legacy Requires From You",
    "Concrete Conversations: Why We Build",
)


def read(name: str) -> str:
    return (YOUTUBE_DIR / name).read_text(encoding="utf-8")


def test_youtube_launch_required_files_exist():
    assert YOUTUBE_DIR.is_dir()
    for filename in REQUIRED_FILES:
        path = YOUTUBE_DIR / filename
        assert path.is_file(), filename
        assert path.read_text(encoding="utf-8").strip()


def test_channel_copy_has_required_copy_blocks():
    text = read("CHANNEL_COPY.md")
    for heading in (
        "## Channel Description",
        "## Short Channel Bio",
        "## Long Channel Bio",
        "## About Section",
        "## Links Section Copy",
        "## Pinned Comment Template",
        "## Community Post Templates",
        "## Sponsor / Booking Inquiry Blurb",
    ):
        assert heading in text


def test_first_10_videos_are_fully_outlined():
    text = read("FIRST_10_VIDEOS.md")
    assert text.count("**Title:**") == 10
    assert text.count("**Hook:**") == 10
    assert text.count("**Description:**") == 10
    assert text.count("**Outline:**") == 10
    assert text.count("**CTA:**") == 10
    for title in FIRST_10_TITLES:
        assert title in text


def test_shorts_system_has_required_formats_and_banks():
    text = read("SHORTS_SYSTEM.md")
    for phrase in (
        "## 15-Second Format",
        "## 30-Second Format",
        "## 60-Second Format",
        "## Hook Bank",
        "## CTA Bank",
        "## Caption Templates",
        "## Repurposing From Podcast Clips",
    ):
        assert phrase in text


def test_thumbnail_guide_has_style_rules_and_first_10_examples():
    text = read("THUMBNAIL_GUIDE.md")
    for phrase in (
        "Black, concrete gray, white, and gold accents",
        "2-4 word thumbnail text",
        "## First 10 Thumbnail Examples",
        "PRESSURE BUILDS",
        "WHY WE BUILD",
    ):
        assert phrase in text


def test_upload_checklist_has_required_upload_steps():
    text = read("UPLOAD_CHECKLIST.md")
    for phrase in (
        "Title",
        "Description",
        "Thumbnail",
        "Tags/keywords",
        "Chapters",
        "Pinned comment",
        "Shorts cutdown",
        "Community post",
        "Website link",
        "Booking CTA",
    ):
        assert phrase in text
