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

    assert "main" in parser.ids
    assert "Concrete Motivation" in parser.text
    assert "Build from pressure. Lead with purpose. Move with discipline." in parser.text
    assert "Become a Founding Member" in parser.text
    assert "Join Concrete Nation" in parser.text


def test_brand_engines_audiences_and_member_journey_exist():
    text = parse_site().text

    for phrase in (
        "Concrete Motivation",
        "Concrete Conversations",
        "Concrete Nation",
        "Parents & Providers",
        "Students & Athletes",
        "Workers & Leaders",
        "Builders & Entrepreneurs",
        "Connect",
        "Clarify",
        "Commit",
        "Contribute",
        "Compound",
    ):
        assert phrase in text


def test_navigation_and_calls_to_action_use_real_local_routes():
    parser = parse_site()

    expected = {
        "index.html",
        "story.html",
        "who-we-serve.html",
        "conversations.html",
        "nation.html",
        "join.html",
    }
    assert expected.issubset(set(parser.links))
    for href in expected:
        assert (WEBSITE_DIR / href).is_file()


def test_styles_include_responsive_rules_and_hero_asset():
    css = (WEBSITE_DIR / "styles.css").read_text(encoding="utf-8")

    assert "@media(max-width:900px)" in css
    assert "@media(max-width:620px)" in css
    assert "--gold:" in css
    assert "prefers-reduced-motion:reduce" in css
