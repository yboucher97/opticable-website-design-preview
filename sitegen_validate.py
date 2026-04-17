"""Build validation helpers for the site generator."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

from sitegen_data import DEPLOY_ROOT, FORCE_NOINDEX, SITE_URL

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
SKIPPED_PATH_PREFIXES = (
    "/api/",
)

ARTICLE_STYLE_MARKERS = (
    "blog-grid",
    "blog-card",
    "blog-article-card",
    "blog-related-articles-section",
    "blog-related-services-section",
    "blog-summary-section",
    "blog-article-shell",
)
ARTICLE_STYLE_HREF_FRAGMENT = "styles-articles.css"


def absolute_url_for_path(path):
    if path == "/":
        return SITE_URL + "/"
    return f"{SITE_URL}{path}"


def deploy_path_for_path(path):
    if path == "/":
        return DEPLOY_ROOT / "index.html"
    stripped = path.strip("/")
    if not stripped:
        return DEPLOY_ROOT / "index.html"
    candidate = DEPLOY_ROOT / stripped
    if candidate.suffix:
        return candidate
    return candidate / "index.html"


def _normalized_internal_path(reference):
    if not reference:
        return None
    parsed = urlparse(reference)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None
    if parsed.scheme in {"http", "https"} and parsed.netloc and parsed.netloc != urlparse(SITE_URL).netloc:
        return None
    path = parsed.path or "/"
    if not path.startswith("/"):
        return None
    if any(path.startswith(prefix) for prefix in SKIPPED_PATH_PREFIXES):
        return None
    return path


def _parse_srcset(value):
    candidates = []
    for entry in (value or "").split(","):
        part = entry.strip()
        if not part:
            continue
        candidates.append(part.split()[0])
    return candidates


class BuildHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.in_h1 = False
        self.title_parts = []
        self.h1_parts = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.references = []
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        lowered_tag = tag.lower()
        if lowered_tag == "title":
            self.in_title = True
        elif lowered_tag == "h1":
            self.in_h1 = True
        elif lowered_tag == "meta":
            name = attrs.get("name", "").lower()
            prop = attrs.get("property", "").lower()
            content = attrs.get("content", "").strip()
            if name == "description" and content:
                self.description = content
            elif name == "robots" and content:
                self.robots = content
            elif prop in {"og:image", "twitter:image"} and content:
                self.references.append(content)
        elif lowered_tag == "link":
            rel_values = {part.lower() for part in attrs.get("rel", "").split()}
            href = attrs.get("href", "").strip()
            if "canonical" in rel_values and href:
                self.canonical = href
            if "stylesheet" in rel_values and href:
                self.stylesheets.append(href)
            if href:
                self.references.append(href)
        elif lowered_tag in {"a", "script", "img", "iframe", "source"}:
            attr_name = "href" if lowered_tag == "a" else "src"
            attr_value = attrs.get(attr_name, "").strip()
            if attr_value:
                self.references.append(attr_value)
            if "srcset" in attrs:
                self.references.extend(_parse_srcset(attrs.get("srcset", "")))
        elif lowered_tag == "video":
            poster = attrs.get("poster", "").strip()
            if poster:
                self.references.append(poster)

    def handle_endtag(self, tag):
        lowered_tag = tag.lower()
        if lowered_tag == "title":
            self.in_title = False
        elif lowered_tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h1:
            self.h1_parts.append(data)

    @property
    def title(self):
        return "".join(self.title_parts).strip()

    @property
    def h1(self):
        return " ".join(part.strip() for part in self.h1_parts if part.strip()).strip()


def parse_html(path):
    parser = BuildHtmlParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def sitemap_paths():
    sitemap_path = DEPLOY_ROOT / "sitemap.xml"
    root = ET.fromstring(sitemap_path.read_text(encoding="utf-8"))
    paths = []
    for loc in root.findall("sm:url/sm:loc", SITEMAP_NS):
        path = _normalized_internal_path((loc.text or "").strip())
        if path:
            paths.append(path)
    return paths


def _validate_references(page_path, parser, issues):
    for reference in parser.references:
        internal_path = _normalized_internal_path(reference)
        if not internal_path:
            continue
        target = deploy_path_for_path(internal_path)
        if not target.exists():
            issues.append(f"{page_path}: broken internal reference {reference}")


def _validate_page(path, issues):
    file_path = deploy_path_for_path(path)
    if not file_path.exists():
        issues.append(f"{path}: generated file is missing")
        return
    html = file_path.read_text(encoding="utf-8")
    parser = parse_html(file_path)
    if not parser.title:
        issues.append(f"{path}: missing <title>")
    if not parser.description:
        issues.append(f"{path}: missing meta description")
    if not parser.h1:
        issues.append(f"{path}: missing <h1>")
    expected_canonical = absolute_url_for_path(path)
    if not parser.canonical:
        issues.append(f"{path}: missing canonical link")
    elif parser.canonical != expected_canonical:
        issues.append(f"{path}: canonical mismatch ({parser.canonical} != {expected_canonical})")
    if FORCE_NOINDEX and "noindex" not in parser.robots.lower():
        issues.append(f"{path}: preview build is missing noindex robots")
    if not FORCE_NOINDEX and "noindex" in parser.robots.lower():
        issues.append(f"{path}: indexable build unexpectedly contains noindex")
    if any(marker in html for marker in ARTICLE_STYLE_MARKERS) and not any(
        ARTICLE_STYLE_HREF_FRAGMENT in stylesheet for stylesheet in parser.stylesheets
    ):
        issues.append(f"{path}: article-style markup is present but styles-articles.css is missing")
    _validate_references(path, parser, issues)


def validate_build():
    issues = []
    paths = sitemap_paths()
    if not paths:
        issues.append("sitemap.xml does not contain any local URLs")
    for path in paths:
        _validate_page(path, issues)
    _validate_page("/404.html", issues)
    if issues:
        joined = "\n - ".join(issues[:50])
        if len(issues) > 50:
            joined += f"\n - ...and {len(issues) - 50} more"
        raise RuntimeError(f"Build validation failed ({len(issues)} issues):\n - {joined}")
    print(f"Build validation passed: {len(paths)} sitemap pages checked plus /404.html.")
