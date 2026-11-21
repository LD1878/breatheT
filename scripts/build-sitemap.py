#!/usr/bin/env python3
"""Build sitemap.xml and llms.txt from live canonical pages.

Includes an index.html page only when its canonical matches its path and
the page is not noindex. lastmod comes from journal front matter, then git.

Run from the repo root: python3 scripts/build-sitemap.py
The journal builder calls this after it writes /guides/.
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.breathetherm.co.uk"
SKIP_DIRS = {".git", ".amp", ".agents", "node_modules"}

CANON_RE = re.compile(
    r"""rel=["']canonical["']\s+href=(["'])(.*?)\1""", re.I
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
META_RE = re.compile(
    r"""<meta\s+name=(["'])(.*?)\1\s+content=(["'])(.*?)\3""", re.I
)

LLMS_SECTIONS: list[tuple[str, list[str]]] = [
    ("Start here", ["/", "/will-it-work/", "/contact/"]),
    (
        "Solutions",
        [
            "/solutions/",
            "/solutions/internal-walls/",
            "/solutions/external-walls/",
            "/solutions/floors/",
            "/display/",
        ],
    ),
    (
        "Products",
        [
            "/products/",
            "/products/perlitherm/",
            "/products/gelpanel/",
            "/products/perliscatch/",
            "/products/perlimessh/",
            "/products/aerobond/",
            "/products/perlifinish/",
            "/products/perlibase/",
            "/products/perlistruct/",
            "/products/perlilay/",
            "/products/perlimat/",
        ],
    ),
    ("Journal", ["/guides/"]),
    (
        "Projects",
        [
            "/projects/",
            "/projects/kerry-cottage/",
            "/projects/kerry-cottage-perthshire/",
            "/projects/bristol-mansion-block/",
        ],
    ),
    (
        "Who it is for",
        ["/for-homeowners/", "/for-architects/", "/for-installers/"],
    ),
    ("Company", ["/about/", "/glossary/"]),
]


def flatten(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def expected_url(html_path: Path) -> str:
    rel = html_path.parent.relative_to(ROOT)
    if rel == Path("."):
        return SITE + "/"
    return f"{SITE}/{rel.as_posix()}/"


def page_path(url: str) -> str:
    if url == SITE or url == SITE + "/":
        return "/"
    if url.startswith(SITE):
        return url[len(SITE) :] or "/"
    return url


def meta_content(html: str, name: str) -> str | None:
    for match in META_RE.finditer(html):
        if match.group(2).lower() == name.lower():
            return match.group(4)
    return None


def is_noindex(html: str) -> bool:
    robots = meta_content(html, "robots")
    return bool(robots and "noindex" in robots.lower())


def journal_meta() -> dict[str, dict]:
    posts: dict[str, dict] = {}
    src = ROOT / "content" / "journal"
    if not src.is_dir():
        return posts
    for path in sorted(src.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text()
        slug = re.search(r"^slug:\s*(.+)$", text, re.M)
        date = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
        updated = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
        order = re.search(r"^order:\s*(\d+)", text, re.M)
        if not slug or not date:
            continue
        key = slug.group(1).strip()
        posts[key] = {
            "lastmod": updated.group(1) if updated else date.group(1),
            "order": int(order.group(1)) if order else 99,
        }
    return posts


def git_lastmod(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", rel],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    date = result.stdout.strip()
    return date or None


def collect_pages() -> list[dict]:
    journal = journal_meta()
    journal_latest = (
        max(p["lastmod"] for p in journal.values()) if journal else None
    )
    pages: list[dict] = []
    for html_path in sorted(ROOT.rglob("index.html")):
        if any(part in SKIP_DIRS for part in html_path.parts):
            continue
        html = html_path.read_text(errors="ignore")
        if is_noindex(html):
            continue
        canon_match = CANON_RE.search(html)
        if not canon_match:
            continue
        canonical = canon_match.group(2).strip()
        if canonical != expected_url(html_path):
            continue
        title_match = TITLE_RE.search(html)
        desc = meta_content(html, "description")
        path = page_path(canonical)
        lastmod = None
        if path.startswith("/guides/") and path != "/guides/":
            slug = path.strip("/").split("/")[-1]
            lastmod = (journal.get(slug) or {}).get("lastmod")
        elif path == "/guides/":
            lastmod = journal_latest
        if not lastmod:
            lastmod = git_lastmod(html_path)
        slug = path.strip("/").split("/")[-1] if path.startswith("/guides/") else ""
        pages.append(
            {
                "url": canonical,
                "path": path,
                "title": flatten(title_match.group(1)) if title_match else path,
                "description": flatten(desc) if desc else "",
                "lastmod": lastmod,
                "order": (journal.get(slug) or {}).get("order", 99),
            }
        )
    pages.sort(key=lambda p: (p["path"] != "/", p["path"]))
    return pages


def write_sitemap(pages: list[dict]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!-- Generated by scripts/build-sitemap.py. Do not edit. -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        loc = escape(page["url"])
        if page["lastmod"]:
            lines.append(
                f"  <url><loc>{loc}</loc><lastmod>{page['lastmod']}</lastmod></url>"
            )
        else:
            lines.append(f"  <url><loc>{loc}</loc></url>")
    lines.append("</urlset>")
    lines.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(lines))


def md_link(page: dict) -> str:
    note = page["description"] or page["title"]
    return f"- [{page['title']}]({page['url']}): {note}"


def write_llms_txt(pages: list[dict]) -> None:
    by_path = {p["path"]: p for p in pages}
    used: set[str] = set()
    chunks = [
        "# BreatheTherm",
        "",
        "> Breathable mineral insulation for pre-1919 and listed buildings in the UK. Vapour-open lime, perlite and aerogel systems that keep solid walls drying while the home stays warm.",
        "",
        "BreatheTherm specifies and installs vapour-open wall and floor build-ups for solid masonry. Materials are mineral and designed for listed and conservation work, including WTA 6-4 internal insulation. Contact: hello@breathetherm.co.uk, 01285 407088. The Old Forge, Todenham, Gloucestershire GL56 9PF.",
        "",
        f"Canonical pages: {SITE}/sitemap.xml",
        "",
    ]
    for heading, paths in LLMS_SECTIONS:
        rows = []
        for path in paths:
            page = by_path.get(path)
            if not page:
                continue
            rows.append(md_link(page))
            used.add(path)
        if heading == "Journal":
            journal_pages = [
                p
                for p in pages
                if p["path"].startswith("/guides/") and p["path"] != "/guides/"
            ]
            journal_pages.sort(key=lambda p: (p["order"], p["path"]))
            rows.extend(md_link(p) for p in journal_pages)
            used.update(p["path"] for p in journal_pages)
        if rows:
            chunks.append(f"## {heading}")
            chunks.append("")
            chunks.extend(rows)
            chunks.append("")
    leftover = [p for p in pages if p["path"] not in used]
    if leftover:
        chunks.append("## Optional")
        chunks.append("")
        chunks.extend(md_link(p) for p in leftover)
        chunks.append("")
    (ROOT / "llms.txt").write_text("\n".join(chunks))


def main() -> None:
    pages = collect_pages()
    if not pages:
        sys.exit("No canonical indexable pages found")
    write_sitemap(pages)
    write_llms_txt(pages)
    print(f"wrote sitemap.xml ({len(pages)} URLs)")
    print("wrote llms.txt")


if __name__ == "__main__":
    main()
