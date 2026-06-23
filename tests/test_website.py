from html.parser import HTMLParser
from pathlib import Path


WEBSITE_DIR = Path(__file__).resolve().parent.parent / "website"


class WebsiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.labels_for: set[str] = set()
        self.inputs: set[str] = set()
        self.links: list[str] = []
        self.images: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if tag == "label" and "for" in attrs_dict:
            self.labels_for.add(attrs_dict["for"])
        if tag in {"input", "select", "textarea"} and "id" in attrs_dict:
            self.inputs.add(attrs_dict["id"])
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])
        if tag == "img" and "src" in attrs_dict:
            self.images.append(attrs_dict["src"])

    def handle_data(self, data):
        text = " ".join(data.split())
        if text:
            self.text_parts.append(text)

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)


def parse_site() -> WebsiteParser:
    parser = WebsiteParser()
    parser.feed((WEBSITE_DIR / "index.html").read_text(encoding="utf-8"))
    return parser


def test_required_website_files_exist():
    assert (WEBSITE_DIR / "index.html").is_file()
    assert (WEBSITE_DIR / "styles.css").is_file()
    assert (WEBSITE_DIR / "script.js").is_file()
    assert (WEBSITE_DIR / "assets" / ".gitkeep").is_file()
    assert (WEBSITE_DIR / "assets" / "concrete-hero.png").is_file()


def test_homepage_contains_required_sections_and_ctas():
    parser = parse_site()

    assert {"top", "story", "speaking", "podcast", "programs", "booking"}.issubset(parser.ids)
    assert "Concrete Motivation" in parser.text
    assert "Build from pressure. Lead with purpose. Move with discipline." in parser.text
    assert "Book Jaytee to Speak" in parser.text
    assert "Watch Concrete Conversations" in parser.text


def test_speaking_topics_programs_and_podcast_placeholders_exist():
    text = parse_site().text

    for phrase in (
        "Discipline Under Pressure",
        "Pain Into Purpose",
        "Fatherhood and Legacy",
        "Athlete Mindset and Leadership",
        "Building After Setbacks",
        "Concrete Conversations Live",
        "Team Talk",
        "Youth Leadership Workshop",
        "Concrete Builder Session",
        "Podcast Guest / Live Conversation",
        "Business and Leadership Keynote",
        "YouTube coming soon",
        "Podcast links coming soon",
    ):
        assert phrase in text


def test_booking_form_placeholder_is_accessible_and_honest():
    parser = parse_site()

    assert {"name", "email", "organization", "event-type", "message"}.issubset(parser.inputs)
    assert parser.inputs.issubset(parser.labels_for)
    assert "Placeholder only. No message is sent until a form service is connected." in parser.text


def test_styles_include_responsive_rules_and_hero_asset():
    css = (WEBSITE_DIR / "styles.css").read_text(encoding="utf-8")

    assert "@media (max-width: 820px)" in css
    assert "@media (max-width: 520px)" in css
    assert "assets/concrete-hero.png" in css
