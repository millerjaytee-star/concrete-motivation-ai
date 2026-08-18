from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WEBSITE_DIR = ROOT / "website"
WEB_APP = ROOT / "apps" / "web"


class WebsiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "href" in attrs_dict:
            self.links.append(attrs_dict["href"])

    def handle_data(self, data):
        text = " ".join(data.split())
        if text:
            self.text_parts.append(text)

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)


def parse_legacy_site() -> WebsiteParser:
    parser = WebsiteParser()
    parser.feed((WEBSITE_DIR / "index.html").read_text(encoding="utf-8"))
    return parser


def test_legacy_website_assets_are_preserved():
    assert (WEBSITE_DIR / "index.html").is_file()
    assert (WEBSITE_DIR / "styles.css").is_file()
    assert (WEBSITE_DIR / "script.js").is_file()
    assert (WEBSITE_DIR / "assets" / "concrete-hero.png").is_file()


def test_production_next_application_is_the_deployed_public_site():
    netlify = (ROOT / "netlify.toml").read_text(encoding="utf-8")
    package = (WEB_APP / "package.json").read_text(encoding="utf-8")
    assert 'base = "apps/web"' in netlify
    assert 'publish = ".next"' in netlify
    assert '"build": "next build"' in package
    assert not (WEB_APP / "vite.config.ts").exists()


def test_legacy_site_retains_approved_brand_and_public_navigation():
    parser = parse_legacy_site()
    assert "Concrete Motivation" in parser.text
    assert "Build from pressure. Lead with purpose. Move with discipline." in parser.text
    for page in ("story.html", "who-we-serve.html", "conversations.html", "nation.html", "join.html"):
        assert page in parser.links


def test_production_assets_are_real_decodable_image_formats():
    signatures = {
        b"\xff\xd8\xff",  # JPEG
        b"\x89PNG\r\n\x1a\n",  # PNG
        b"RIFF",  # WebP container
    }
    assets = list((WEB_APP / "public" / "brand").glob("*"))
    assert len(assets) >= 9
    for asset in assets:
        header = asset.read_bytes()[:12]
        assert any(header.startswith(signature) for signature in signatures), asset


def test_static_export_is_not_enabled():
    next_config = (WEB_APP / "next.config.ts").read_text(encoding="utf-8")
    assert 'output: "export"' not in next_config
