"""Checks the built site in _site/ against the study hub spec.

Run after a Jekyll build (tools/build-site.ps1 does both):
    python tools/check_site.py
Exits non-zero and lists every problem found.
"""
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
COLLECTIONS = ("projects", "experience", "tech")

# Repo-only files that must never be published
MUST_BE_ABSENT = [
    "CLAUDE.md", "CLAUDE.html", "README.md", "README.html", "resume.tex",
    "build-resume.ps1", "docs", "tools", "Gemfile", "Gemfile.lock", ".githooks",
]
MUST_BE_PRESENT = [
    "index.html", "style.css", "script.js", "resume.pdf", "CNAME", "robots.txt",
    "sitemap.xml", "images/prashant.jpg", "study/index.html", "study.css",
]

# Hub must link every study page (switched on once the hub exists)
CHECK_HUB = True

# (page under _site, href that must appear on it)
REQUIRED_LINKS = [
    ("study/projects/qwr-voice-bot/index.html", "/study/tech/django-channels/"),
    ("study/projects/qwr-voice-bot/index.html", "/study/experience/qwr/"),
    ("study/experience/qwr/index.html", "/study/projects/qwr-voice-bot/"),
    ("study/experience/qwr/index.html", "/study/tech/django-channels/"),
    ("study/tech/django-channels/index.html", "/study/projects/qwr-voice-bot/"),
    ("study/tech/django-channels/index.html", "/study/experience/qwr/"),
    ("study/tech/django-channels/index.html", "/study/"),
    ("study/tech/django/index.html", "/study/experience/jaxl/"),
    ("study/tech/django/index.html", "/study/experience/jaxl-intern/"),
    ("study/tech/gemini-live-api/index.html", "/study/projects/qwr-voice-bot/"),
    ("study/projects/qwr-voice-bot/index.html", "/study/tech/gemini-live-api/"),
]
# (page under _site, href that must not appear on it)
FORBIDDEN_LINKS = [
    # exotel has no tech page: it must render as plain text, not a dead link
    ("study/projects/qwr-voice-bot/index.html", "/study/tech/exotel/"),
    # the hub is unlisted: only reachable by typing the URL
    ("index.html", "study/"),
]
# (page under _site, text that must appear in its HTML)
REQUIRED_TEXT = [
    ("study/projects/qwr-voice-bot/index.html", '<li class="tag-missing">exotel</li>'),
    ("study/projects/qwr-voice-bot/index.html", "Built during"),
    # mobile menu markup that script.js depends on
    ("study/tech/django-channels/index.html", 'class="nav-toggle"'),
    ("study/tech/django-channels/index.html", "<title>Django Channels · Study | Prashant Singh</title>"),
    # redis is on the skills list but no page is tagged with it yet
    ("study/tech/redis/index.html", "Nothing is tagged with this yet."),
]
# (page under _site, text that must not appear in its HTML)
FORBIDDEN_TEXT = [
    # vargi-bot was a competition project, not built during a role
    ("study/projects/vargi-bot/index.html", "Built during"),
]

EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", re.I)


class RefCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.refs.append(value)


def refs(page):
    collector = RefCollector()
    collector.feed(page.read_text(encoding="utf-8"))
    return collector.refs


def html(rel):
    page = SITE / rel
    return page.read_text(encoding="utf-8") if page.exists() else None


def resolve(page, ref):
    """Map an internal href/src to the file it points at under _site, or None if external."""
    if EXTERNAL.match(ref):
        return None
    path = ref.split("#")[0].split("?")[0]
    target = SITE / path.lstrip("/") if path.startswith("/") else page.parent / path
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


FRONT_MATTER = re.compile(r"\A---[ \t]*\n(.*?)^---[ \t]*$", re.S | re.M)
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def front_matter(source):
    match = FRONT_MATTER.match(source.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def question_count(source):
    return len(re.findall(r"^\s*- q:", front_matter(source), re.M))


def tech_errors(source):
    """`tech:` must be an inline list of slugs: a bare string makes `contains` match substrings."""
    match = re.search(r"^tech:[ \t]*(.*)$", front_matter(source), re.M)
    if not match:
        return []
    value = match.group(1).strip()
    if not (value.startswith("[") and value.endswith("]")):
        return [f"tech must be an inline list, e.g. tech: [{value.strip('[]') or 'django'}]"]
    slugs = [t.strip().strip("\"'") for t in value[1:-1].split(",") if t.strip()]
    return [f"tech slug must be lowercase-with-dashes: {slug}" for slug in slugs if not SLUG.match(slug)]


def main():
    if not SITE.is_dir():
        print("No _site/ found: build the site first (tools/build-site.ps1).")
        return 1
    errors = []

    for rel in MUST_BE_ABSENT:
        if (SITE / rel).exists():
            errors.append(f"published but must not be: {rel}")
    for rel in MUST_BE_PRESENT:
        if not (SITE / rel).exists():
            errors.append(f"missing from build: {rel}")
    built_index = SITE / "index.html"
    if built_index.exists() and built_index.read_bytes() != (ROOT / "index.html").read_bytes():
        errors.append("index.html was changed by the build (it must pass through untouched)")

    hub = SITE / "study" / "index.html"
    hub_refs = refs(hub) if CHECK_HUB and hub.exists() else []
    sitemap = html("sitemap.xml") or ""
    for coll in COLLECTIONS:
        for source in sorted((ROOT / f"_{coll}").glob("*.md")):
            url = f"/study/{coll}/{source.stem}/"
            page = SITE / url.strip("/") / "index.html"
            if not page.exists():
                errors.append(f"no page built for _{coll}/{source.name}")
                continue
            for problem in tech_errors(source):
                errors.append(f"_{coll}/{source.name}: {problem}")
            # Jekyll only warns on a YAML error and builds the page with no front matter at all
            if '<h1 class="study-title"></h1>' in page.read_text(encoding="utf-8"):
                errors.append(f"{url}: empty title (front matter missing or not valid YAML?)")
            want = question_count(source)
            got = page.read_text(encoding="utf-8").count('<details class="qa"')
            if got != want:
                errors.append(f"{url}: {got} questions rendered, front matter has {want}")
            # the hub is unlisted: keep it out of search engines
            if '<meta name="robots" content="noindex">' not in page.read_text(encoding="utf-8"):
                errors.append(f"{url}: missing noindex")
            if CHECK_HUB and url not in hub_refs:
                errors.append(f"hub does not link to {url}")

    for page in sorted(SITE.rglob("*.html")):
        for ref in refs(page):
            target = resolve(page, ref)
            if target is not None and not target.exists():
                errors.append(f"{page.relative_to(SITE).as_posix()}: broken link {ref}")

    if "/study" in sitemap:
        errors.append("sitemap.xml lists study pages (the hub is unlisted)")
    if '<meta name="robots" content="noindex">' not in (html("study/index.html") or ""):
        errors.append("study/index.html: missing noindex")

    try:
        ET.parse(SITE / "sitemap.xml")
    except (ET.ParseError, FileNotFoundError) as e:
        errors.append(f"sitemap.xml is not valid XML: {e}")

    for rel, href in REQUIRED_LINKS:
        if html(rel) is None or href not in refs(SITE / rel):
            errors.append(f"{rel}: missing link {href}")
    for rel, href in FORBIDDEN_LINKS:
        if html(rel) is not None and href in refs(SITE / rel):
            errors.append(f"{rel}: must not link {href}")
    for rel, text in REQUIRED_TEXT:
        if text not in (html(rel) or ""):
            errors.append(f"{rel}: missing text {text!r}")
    for rel, text in FORBIDDEN_TEXT:
        if text in (html(rel) or ""):
            errors.append(f"{rel}: must not contain {text!r}")

    for error in errors:
        print("FAIL", error)
    print(f"{len(errors)} problem(s)" if errors else "OK: site matches the study hub spec")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
