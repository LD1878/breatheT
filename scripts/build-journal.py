#!/usr/bin/env python3
"""Build journal HTML from content/journal/*.md.

Post format: content/journal/_format.md
Run from the repo root: python3 scripts/build-journal.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "journal"
GUIDES = ROOT / "guides"
SITE = "https://www.breathetherm.co.uk"
CSS_VER = "journal4"


NAV_LINKS = """\
                <a href="{p}solutions/#problem">The Problem</a>
                <a href="{p}solutions/#approach">The System</a>
                <a href="{p}products/">Products</a>
                <a href="{p}projects/">Projects</a>
                <a href="{p}will-it-work/">Will it work?</a>
                <a href="{p}guides/#faq">FAQs</a>
                <a href="{p}guides/#journal">Journal</a>
                <a href="{p}contact/" class="btn btn-primary btn-nav">Book assessment</a>"""

MOBILE_NAV = """\
        <span class="mobile-label">Paths</span>
        <a href="{p}for-homeowners/">Homeowners</a>
        <a href="{p}for-architects/">Architects</a>
        <a href="{p}for-installers/">Installers</a>
        <a href="{p}about/">About</a>
        <a href="{p}will-it-work/">Will it work?</a>
        <a href="{p}contact/">Book assessment</a>
        <span class="mobile-label">Applications</span>
        <a href="{p}solutions/">The Problem</a>
        <a href="{p}solutions/">The System</a>
        <a href="{p}solutions/internal-walls/">Internal walls</a>
        <a href="{p}solutions/external-walls/">External walls</a>
        <a href="{p}solutions/floors/">Floors</a>
        <a href="{p}display/">Demo house</a>
        <span class="mobile-label">Products</span>
        <a href="{p}products/">Products</a>
        <a href="{p}products/perlitherm/">PerliTherm</a>
        <a href="{p}products/gelpanel/">AeroGel</a>
        <a href="{p}products/perliscatch/">PerliScratch</a>
        <a href="{p}products/perlimessh/">PerliMesh</a>
        <a href="{p}products/aerobond/">AeroBond</a>
        <a href="{p}products/perlifinish/">PerliFinish</a>
        <a href="{p}products/perlibase/">PerliBase</a>
        <a href="{p}products/perlistruct/">PerliStruct</a>
        <a href="{p}products/perlilay/">PerliScreed</a>
        <a href="{p}products/perlimat/">PerliMat</a>
        <span class="mobile-label">Projects and journal</span>
        <a href="{p}projects/">Projects</a>
        <a href="{p}projects/kerry-cottage-perthshire/">Kerry Cottage, Perthshire</a>
        <a href="{p}projects/kerry-cottage/">17th-century Cotswold farmhouse</a>
        <a href="{p}projects/bristol-mansion-block/">Victorian mansion block, Bristol</a>
        <a href="{p}guides/">Journal</a>
        <a href="{p}privacy/">Privacy</a>
        <a href="tel:01285407088">01285 407088</a>"""

FOOTER = """\
    <footer class="site-footer grain">
        <div class="container footer-main">
            <div class="footer-brand">
                <a class="footer-logo" href="{p}">
                    <img src="{a}assets/images/breathetherm-logo.png" alt="BreatheTherm">
                </a>
                <p>Breathable mineral insulation for the UK’s pre-1919 and listed buildings. Walls and floors that can breathe while the home stays warm.</p>
                <p><a href="tel:01285407088">01285 407088</a><br>
                    <a href="mailto:hello@breathetherm.co.uk">hello@breathetherm.co.uk</a></p>
                <p class="footer-audiences">
                    <a href="{p}for-homeowners/" data-role="owner">Homeowners</a>
                    <a href="{p}for-architects/" data-role="architect">Architects</a>
                    <a href="{p}for-installers/" data-role="installer">Installers</a>
                </p>
                <p>Company no: 16491516 &nbsp;·&nbsp; VAT: 505 972 871</p>
            </div>
            <div class="footer-col">
                <h5>Navigate</h5>
                <a href="{p}solutions/#problem">The Problem</a>
                <a href="{p}solutions/#approach">The System</a>
                <a href="{p}solutions/internal-walls/">Layer Guide</a>
                <a href="{p}solutions/external-walls/">External walls</a>
                <a href="{p}solutions/floors/">Floors</a>
                <a href="{p}projects/">Projects</a>
                <a href="{p}guides/">Journal</a>
                <a href="{p}glossary/">Glossary</a>
            </div>
            <div class="footer-col">
                <h5>For you</h5>
                <a href="{p}for-homeowners/">Homeowners</a>
                <a href="{p}for-architects/">Architects</a>
                <a href="{p}for-installers/">Installers</a>
                <a href="{p}about/">About</a>
                <a href="{p}will-it-work/">Will it work?</a>
                <a href="{p}contact/">Book assessment</a>
                <a href="{p}display/">Demo house</a>
                <a href="{p}privacy/">Privacy</a>
            </div>
            <div class="footer-col">
                <h5>Products</h5>
                <a href="{p}products/">Products</a>
                <a href="{p}products/perlitherm/">PerliTherm</a>
                <a href="{p}products/gelpanel/">AeroGel</a>
                <a href="{p}products/perliscatch/">PerliScratch</a>
                <a href="{p}products/perlimessh/">PerliMesh</a>
                <a href="{p}products/aerobond/">AeroBond</a>
                <a href="{p}products/perlifinish/">PerliFinish</a>
                <a href="{p}products/perlibase/">PerliBase</a>
                <a href="{p}products/perlistruct/">PerliStruct</a>
                <a href="{p}products/perlilay/">PerliScreed</a>
                <a href="{p}products/perlimat/">PerliMat</a>
            </div>
        </div>
        <div class="footer-base">
            <div class="container footer-base-inner">
                <span>© 2026 Breathe Therm Ltd. All rights reserved. · <a href="{p}privacy/">Privacy</a></span>
                <span>The Old Forge, Todenham, Gloucestershire GL56 9PF</span>
            </div>
        </div>
    </footer>"""

HEAD_FONTS = """\
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Serif:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">"""


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ValueError("Missing YAML front matter")
    _, rest = text.split("---", 1)
    yaml_block, body = rest.split("---", 1)
    data: dict = {}
    key = None
    stack: list = []
    for raw in yaml_block.splitlines():
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0 and line.endswith(":") and not line.startswith("- "):
            key = line[:-1]
            data[key] = []
            continue
        if indent == 0 and ":" in line and not line.startswith("- "):
            k, v = line.split(":", 1)
            val = v.strip()
            data[k] = None if val in ("", "~", "null") else val
            key = k
            continue
        if line.startswith("- ") and indent == 0:
            data.setdefault(key, [])
            item = line[2:].strip()
            if ":" in item and not item.startswith("http"):
                ik, iv = item.split(":", 1)
                data[key].append({ik.strip(): iv.strip() or None})
                stack = [data[key][-1]]
            else:
                data[key].append(item)
                stack = []
            continue
        if line.startswith("- ") and indent > 0:
            parent = data[key]
            item = line[2:].strip()
            if ":" in item:
                ik, iv = item.split(":", 1)
                obj = {ik.strip(): _scalar(iv.strip())}
                parent.append(obj)
                stack = [obj]
            else:
                parent.append(item)
                stack = []
            continue
        if indent > 0 and ":" in line and stack:
            ik, iv = line.split(":", 1)
            stack[-1][ik.strip()] = _scalar(iv.strip())
    return data, body.strip() + "\n"


def _scalar(v: str):
    if v == "":
        return ""
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def inline(text: str) -> str:
    parts = []
    last = 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(inline_no_link(text[last:m.start()]))
        label, url = m.group(1), m.group(2)
        parts.append(
            f'<a href="{html.escape(url, quote=True)}">{inline_no_link(label)}</a>'
        )
        last = m.end()
    parts.append(inline_no_link(text[last:]))
    return "".join(parts)


def inline_no_link(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render_markdown(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Return HTML and a list of (id, heading) for H2s."""
    lines = body.splitlines()
    out: list[str] = []
    headings: list[tuple[str, str]] = []
    i = 0
    para: list[str] = []
    list_kind = None
    list_items: list[str] = []

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []

    def flush_list():
        nonlocal list_kind, list_items
        if list_kind:
            tag = "ol" if list_kind == "ol" else "ul"
            items = "".join(f"<li>{inline(x)}</li>" for x in list_items)
            out.append(f"<{tag}>{items}</{tag}>")
            list_kind = None
            list_items = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("> "):
            flush_para()
            flush_list()
            quote = [line[2:]]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                quote.append(lines[i][2:])
                i += 1
            out.append(
                '<aside class="journal-callout"><p>'
                + inline(" ".join(quote))
                + "</p></aside>"
            )
            continue
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if m:
            flush_para()
            flush_list()
            level = len(m.group(1))
            title = m.group(2).strip()
            hid = slugify(title)
            if level == 2:
                headings.append((hid, title))
            out.append(f'<h{level} id="{html.escape(hid, quote=True)}">{inline(title)}</h{level}>')
            i += 1
            continue
        ol = re.match(r"^\d+\.\s+(.+)$", line)
        if ol:
            flush_para()
            if list_kind != "ol":
                flush_list()
                list_kind = "ol"
            list_items.append(ol.group(1))
            i += 1
            continue
        ul = re.match(r"^[-*]\s+(.+)$", line)
        if ul:
            flush_para()
            if list_kind != "ul":
                flush_list()
                list_kind = "ul"
            list_items.append(ul.group(1))
            i += 1
            continue
        if not line.strip():
            flush_para()
            flush_list()
            i += 1
            continue
        flush_list()
        para.append(line.strip())
        i += 1
    flush_para()
    flush_list()
    return "\n".join(out), headings


def asset_src(path: str, prefix: str) -> str:
    if path.startswith("/"):
        return prefix.rstrip("/") + path
    return path


def json_ld(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


def chrome(prefix: str) -> tuple[str, str, str]:
    """prefix is relative to site root from this page, e.g. '../' or '../../'."""
    nav = NAV_LINKS.format(p=prefix)
    mobile = MOBILE_NAV.format(p=prefix)
    footer = FOOTER.format(p=prefix, a=prefix)
    return nav, mobile, footer


def format_date(iso: str) -> str:
    y, m, d = iso.split("-")
    months = "January February March April May June July August September October November December".split()
    return f"{int(d)} {months[int(m) - 1]} {y}"


def load_posts() -> list[dict]:
    posts = []
    for path in sorted(SRC.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = parse_front_matter(path.read_text())
        html_body, headings = render_markdown(body)
        meta["body_html"] = html_body
        meta["headings"] = headings
        meta["source"] = path.name
        meta.setdefault("author", "BreatheTherm")
        meta.setdefault("updated", meta["date"])
        meta["keywords"] = [k for k in meta.get("keywords", []) if isinstance(k, str)]
        posts.append(meta)
    posts.sort(key=lambda p: (int(p.get("order") or 99), p["date"], p["slug"]))
    return posts


def page_shell(
    *,
    title: str,
    description: str,
    canonical: str,
    og_type: str,
    og_image: str,
    prefix: str,
    extra_head: str,
    body_class: str,
    main: str,
) -> str:
    nav, mobile, footer = chrome(prefix)
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description, quote=True)}">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/png" href="{prefix}favicon.png">
    <meta property="og:title" content="{html.escape(title, quote=True)}">
    <meta property="og:description" content="{html.escape(description, quote=True)}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:locale" content="en_GB">
    <meta property="og:site_name" content="BreatheTherm">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title, quote=True)}">
    <meta name="twitter:description" content="{html.escape(description, quote=True)}">
    <meta name="twitter:image" content="{og_image}">
{HEAD_FONTS}
    <link rel="stylesheet" href="{prefix}styles.css?v={CSS_VER}">
{extra_head}
</head>
<body class="{body_class}">
    <a class="skip-link" href="#main">Skip to main content</a>
    <header id="main-nav">
        <div class="container nav-content">
            <a class="nav-logo" href="{prefix}">
                <img src="{prefix}assets/images/breathetherm-logo.png" alt="BreatheTherm">
            </a>
            <nav class="nav-links" aria-label="Main navigation">
{nav}
            </nav>
            <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
        </div>
    </header>
    <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation">
{mobile}
    </nav>
    <main id="main">
{main}
    </main>
{footer}
    <script src="{prefix}main.js"></script>
</body>
</html>
"""


def render_post(post: dict, posts: list[dict]) -> str:
    prefix = "../../"
    url = f"{SITE}/guides/{post['slug']}/"
    og_image = SITE + post["hero"]
    keywords = ", ".join(post["keywords"])
    faq = post.get("faq") or []
    products = post.get("products") or []
    related = post.get("related") or []
    idx = next(i for i, p in enumerate(posts) if p["slug"] == post["slug"])
    prev_post = posts[idx - 1] if idx else None
    next_post = posts[idx + 1] if idx + 1 < len(posts) else None

    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"],
        "dateModified": post["updated"],
        "author": {"@type": "Organization", "name": post["author"], "url": SITE + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "BreatheTherm",
            "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/assets/images/breathetherm-logo.png"},
        },
        "image": og_image,
        "mainEntityOfPage": url,
        "keywords": keywords,
        "inLanguage": "en-GB",
        "about": [{"@type": "Thing", "name": k} for k in post["keywords"][:4]],
        "mentions": [
            {"@type": "Product", "name": item["name"], "url": SITE + item["href"]}
            for item in products
        ],
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".journal-dek", ".journal-prose h2", ".faq-item summary"],
        },
        "isPartOf": {"@type": "Blog", "name": "BreatheTherm Journal", "url": SITE + "/guides/"},
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Journal", "item": SITE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": post["title"], "item": url},
        ],
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
            for item in faq
        ],
    }
    nav_head = [f'    <link rel="index" href="{SITE}/guides/">']
    if prev_post:
        nav_head.append(f'    <link rel="prev" href="{SITE}/guides/{prev_post["slug"]}/">')
    if next_post:
        nav_head.append(f'    <link rel="next" href="{SITE}/guides/{next_post["slug"]}/">')
    extra = f"""    <meta name="author" content="{html.escape(post['author'], quote=True)}">
    <meta name="keywords" content="{html.escape(keywords, quote=True)}">
    <meta property="article:published_time" content="{post['date']}">
    <meta property="article:modified_time" content="{post['updated']}">
    <meta property="article:section" content="Journal">
{chr(10).join(nav_head)}
    <script type="application/ld+json">
    {json_ld(article_ld)}
    </script>
    <script type="application/ld+json">
    {json_ld(breadcrumb_ld)}
    </script>
    <script type="application/ld+json">
    {json_ld(faq_ld)}
    </script>"""

    toc = "".join(
        f'<li><a href="#{html.escape(hid, quote=True)}">{html.escape(title)}</a></li>'
        for hid, title in post["headings"]
    )
    product_html = "".join(
        f'<a href="{prefix.rstrip("/")}{item["href"]}"><span class="jp-name">{html.escape(item["name"])}</span>'
        f'<p class="jp-note">{html.escape(item["note"])}</p></a>'
        for item in products
    )
    by_slug = {p["slug"]: p for p in posts}
    related_html = "".join(
        (
            f'<a href="../{html.escape(item["slug"], quote=True)}/">'
            f"<h3>{html.escape(item['title'])}</h3>"
            f"<p>{html.escape(by_slug[item['slug']]['dek'] if item['slug'] in by_slug else '')}</p>"
            f"</a>"
        )
        for item in related
    )
    seq_links = []
    if prev_post:
        seq_links.append(
            f'<a class="text-link" href="../{html.escape(prev_post["slug"], quote=True)}/">Previous: {html.escape(prev_post["title"])}</a>'
        )
    seq_links.append('<a class="text-link" href="../">All journal notes</a>')
    if next_post:
        seq_links.append(
            f'<a class="text-link" href="../{html.escape(next_post["slug"], quote=True)}/">Next: {html.escape(next_post["title"])}</a>'
        )
    faq_items = []
    for i, item in enumerate(faq):
        open_attr = " open" if i == 0 else ""
        faq_items.append(
            f'''                    <details class="faq-item"{open_attr}>
                        <summary>{html.escape(item["q"])}</summary>
                        <div class="faq-body">{html.escape(item["a"])}</div>
                    </details>'''
        )

    hero_src = asset_src(post["hero"], prefix)
    published = format_date(post["date"])

    main = f"""        <header class="journal-hero grain">
            <div class="container">
                <nav class="journal-crumbs" aria-label="Breadcrumb">
                    <a href="{prefix}">Home</a>
                    <span class="crumb-sep" aria-hidden="true">●</span>
                    <a href="../">Journal</a>
                    <span class="crumb-sep" aria-hidden="true">●</span>
                    <span aria-current="page">{html.escape(post["title"])}</span>
                </nav>
                <p class="eyebrow">Journal</p>
                <h1>{html.escape(post["title"])}</h1>
                <p class="journal-dek">{html.escape(post["dek"])}</p>
                <p class="journal-meta">
                    <time datetime="{post["date"]}">{published}</time>
                    <span class="meta-dot" aria-hidden="true">●</span>
                    <span>{post["reading_minutes"]} min read</span>
                    <span class="meta-dot" aria-hidden="true">●</span>
                    <span>{html.escape(post["author"])}</span>
                </p>
            </div>
        </header>
        <article class="band band-paper journal-post" aria-labelledby="main">
            <div class="container journal-layout">
                <div>
                    <figure class="journal-figure">
                        <img src="{hero_src}" alt="{html.escape(post["hero_alt"], quote=True)}" width="1200" height="750">
                        <figcaption>{html.escape(post["hero_alt"])}</figcaption>
                    </figure>
                    <div class="journal-prose">
{chr(10).join(("                        " + line if line else line) for line in post["body_html"].splitlines())}
                    </div>
                </div>
                <aside class="journal-aside" aria-label="On this page">
                    <nav class="journal-toc" aria-label="Article sections">
                        <p>On this page</p>
                        <ol>{toc}</ol>
                    </nav>
                    <div class="journal-aside-card">
                        <p>In the system</p>
                        <div class="journal-products">
{product_html}
                        </div>
                    </div>
                    <div class="journal-aside-card">
                        <p>Need a thickness?</p>
                        <p class="aside-note">A free assessment reads the wall before anyone specifies millimetres.</p>
                        <a href="{prefix}contact/">Book assessment</a>
                    </div>
                </aside>
            </div>
        </article>
        <section id="faq" class="band band-stone grain" aria-labelledby="faq-title">
            <div class="container faq-layout">
                <div class="faq-intro">
                    <p class="eyebrow">Questions this note answers</p>
                    <h2 id="faq-title">FAQ</h2>
                    <p>Short answers you can take to a conservation officer, an architect, or a first site visit.</p>
                    <a href="{prefix}contact/" class="btn btn-primary">Book an assessment</a>
                </div>
                <div class="faq-list">
{chr(10).join(faq_items)}
                </div>
            </div>
        </section>
        <section class="band band-paper" aria-labelledby="related-title">
            <div class="container">
                <p class="eyebrow">Keep reading</p>
                <h2 id="related-title">Related journal notes</h2>
                <div class="journal-related">
{related_html}
                </div>
            </div>
        </section>
        <section class="band band-paper">
            <div class="container">
                <div class="journal-cta">
                    <div>
                        <h2>Read the wall before you insulate it.</h2>
                        <p>A free assessment is how thickness, consent and moisture get decided together.</p>
                    </div>
                    <div class="journal-cta-actions">
                        <a class="btn btn-primary" href="{prefix}contact/">Book a free assessment</a>
                    </div>
                </div>
                <nav class="next-steps" aria-label="Next steps">
                    {"".join(seq_links)}
                    <a class="text-link" href="{prefix}solutions/internal-walls/">See the wall build-up</a>
                    <a class="text-link" href="{prefix}products/">See the products</a>
                </nav>
            </div>
        </section>"""

    # Fix article aria-labelledby: there is no id=main on h1. Use a dedicated id.
    main = main.replace(
        '<article class="band band-paper journal-post" aria-labelledby="main">',
        '<article class="band band-paper journal-post">',
    )

    return page_shell(
        title=post["title"],
        description=post["description"],
        canonical=url,
        og_type="article",
        og_image=og_image,
        prefix=prefix,
        extra_head=extra,
        body_class="inner-page journal-post-page",
        main=main,
    )


INDEX_FAQ_LD = """    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is BreatheTherm?",
          "acceptedAnswer": { "@type": "Answer", "text": "BreatheTherm is a breathable, fabric-first retrofit system developed specifically for solid-wall and heritage buildings. Rather than offering a single product, we look at how the building behaves as a whole (moisture, condensation, comfort and energy performance) and then design an appropriate wall, floor or junction build-up around that." }
        },
        {
          "@type": "Question",
          "name": "Is this suitable for listed and heritage buildings?",
          "acceptedAnswer": { "@type": "Answer", "text": "Yes. All materials are mineral, vapour-open and designed to work with traditional construction. The approach supports drying and long-term fabric health, which generally aligns well with conservation principles." }
        },
        {
          "@type": "Question",
          "name": "Why can't standard modern insulation be used in pre-1919 homes?",
          "acceptedAnswer": { "@type": "Answer", "text": "Pre-1919 buildings were built using breathable lime mortar and solid masonry designed to absorb and release moisture naturally. Modern PIR foam boards and mineral wool are vapour-resistant: when installed in old walls, they trap moisture inside the structure. BreatheTherm uses vapour-permeable mineral materials that work with the natural moisture cycle rather than against it." }
        },
        {
          "@type": "Question",
          "name": "What U-value can I achieve with BreatheTherm?",
          "acceptedAnswer": { "@type": "Answer", "text": "Depending on the thickness available and existing wall construction, BreatheTherm systems can achieve U-values between 0.17 and 0.45 W/m²K. A typical 50mm PerliTherm build-up on a 215mm solid brick wall achieves approximately 0.35 W/m²K. Combining PerliTherm with our 10mm Aerogel Booster in constrained reveals can reach 0.17 W/m²K. A site-specific hygrothermal calculation is produced for every project." }
        },
        {
          "@type": "Question",
          "name": "Does installing internal wall insulation require planning permission?",
          "acceptedAnswer": { "@type": "Answer", "text": "Internal insulation does not typically require planning permission as it doesn't alter the building's external appearance. However, if your property is Listed, you will need Listed Building Consent before carrying out works that affect its character. BreatheTherm can provide supporting hygrothermal modelling reports and documentation to assist consent applications." }
        },
        {
          "@type": "Question",
          "name": "What is WTA certification and why does it matter?",
          "acceptedAnswer": { "@type": "Answer", "text": "The WTA is the German scientific association for building maintenance and monument preservation. WTA Merkblatt 6-4 defines the internationally recognised technical standard for internal insulation of historic buildings. A WTA-compliant system has been tested to manage moisture correctly in heritage wall constructions." }
        }
      ]
    }
    </script>"""

INDEX_FAQ_HTML = """        <section id="faq" class="band band-stone grain" aria-labelledby="faq-title">
            <div class="container faq-layout">
                <div class="faq-intro">
                    <p class="eyebrow">Common questions</p>
                    <h2 id="faq-title">Questions?</h2>
                    <p>Everything you need to know before your free assessment.</p>
                    <p>Still unsure? Call us on <a href="tel:01285407088">01285 407088</a>. We’re always delighted to talk through the specifics of your project.</p>
                    <a href="../contact/" class="btn btn-primary">Book an assessment</a>
                </div>
                <div class="faq-list">
                    <details class="faq-item" open>
                        <summary>What is BreatheTherm?</summary>
                        <div class="faq-body">BreatheTherm is a breathable, fabric-first retrofit system developed specifically for solid-wall and heritage buildings. Rather than offering a single product, we look at how the building behaves as a whole (moisture, condensation, comfort and energy performance) and then design an appropriate wall, floor or junction build-up around that.</div>
                    </details>
                    <details class="faq-item">
                        <summary>Is this suitable for listed and heritage buildings?</summary>
                        <div class="faq-body">Yes. All materials are mineral, vapour-open and designed to work with traditional construction. The approach supports drying and long-term fabric health, which generally aligns well with conservation principles.</div>
                    </details>
                    <details class="faq-item">
                        <summary>Why can’t standard modern insulation be used in pre-1919 homes?</summary>
                        <div class="faq-body">Pre-1919 buildings were built using breathable lime mortar and solid masonry designed to absorb and release moisture naturally. Modern PIR foam boards and mineral wool are vapour-resistant: when installed in old walls, they trap moisture inside the structure. This causes interstitial condensation, accelerated decay of historic fabric, and serious structural damp. BreatheTherm uses vapour-permeable mineral materials that work <em>with</em> the natural moisture cycle rather than against it.</div>
                    </details>
                    <details class="faq-item">
                        <summary>What U-value can I achieve with BreatheTherm?</summary>
                        <div class="faq-body">Depending on the thickness available and existing wall construction, BreatheTherm systems can achieve U-values between 0.17 and 0.45 W/m²K. A typical 50mm PerliTherm build-up on a 215mm solid brick wall achieves approximately 0.35 W/m²K. Combining PerliTherm with our 10mm Aerogel Booster in constrained reveals can reach 0.17 W/m²K. A site-specific hygrothermal calculation is produced for every project.</div>
                    </details>
                    <details class="faq-item">
                        <summary>Does installing internal wall insulation require planning permission?</summary>
                        <div class="faq-body">Internal insulation does not typically require planning permission as it doesn’t alter the building’s external appearance. However, if your property is Listed, you will need Listed Building Consent before carrying out works that affect its character. BreatheTherm can provide supporting hygrothermal modelling reports and documentation to assist consent applications.</div>
                    </details>
                    <details class="faq-item">
                        <summary>How long does BreatheTherm installation take?</summary>
                        <div class="faq-body">For a typical Victorian or Georgian home, internal wall insulation takes 2–5 days per room, or 1–3 weeks for a whole house depending on scope and preparation required. The system uses dry-application materials (lime plaster requires 3–7 days curing before decoration).</div>
                    </details>

                    <div class="faq-more" id="faq-more" hidden>
                        <details class="faq-item">
                            <summary>What problems does it address first?</summary>
                            <div class="faq-body">Cold internal surfaces, condensation and comfort issues, while avoiding the moisture-trapping risks that can arise with more conventional retrofit approaches.</div>
                        </details>
                        <details class="faq-item">
                            <summary>What is perlite?</summary>
                            <div class="faq-body">Perlite is a natural volcanic mineral. When heated it expands and traps air, which makes our lime-based renders lightweight, insulating and vapour-open. Within the system it helps walls manage moisture safely by absorbing excess humidity and releasing it again as conditions dry.</div>
                        </details>
                        <details class="faq-item">
                            <summary>What is aerogel made from?</summary>
                            <div class="faq-body">Aerogel is a mineral material based on silica (the same basic constituent as sand and glass). During manufacture the liquid component is replaced with air, creating an extremely lightweight, non-combustible and highly insulating solid.</div>
                        </details>
                        <details class="faq-item">
                            <summary>How do perlite and aerogel work together?</summary>
                            <div class="faq-body">They are the component parts. Perlite forms the breathable, moisture-regulating backbone of the system. Aerogel is introduced selectively, typically in thin layers of around 5–30 mm, to enhance thermal performance where space, detailing or heritage constraints limit build-up thickness. They can be used together or independently, depending on the building and the priorities of the project.</div>
                        </details>
                        <details class="faq-item">
                            <summary>Is BreatheTherm just insulation?</summary>
                            <div class="faq-body">Not really. It’s a joined-up approach to the building fabric, considering floors, walls, junctions and finishes so that improvements work together safely rather than in isolation.</div>
                        </details>
                        <details class="faq-item">
                            <summary>What is vapour-permeable (breathable) insulation?</summary>
                            <div class="faq-body">Vapour-permeable insulation allows moisture vapour to pass through the wall assembly, preventing it accumulating within the structure. Materials like expanded perlite and silica aerogel are hygroscopic: they can absorb small amounts of moisture and release it as conditions dry. This capillary activity keeps walls dry without impermeable barriers, making them ideal for solid masonry and timber-framed heritage buildings.</div>
                        </details>
                        <details class="faq-item" id="faq-wta" open>
                            <summary>What is WTA certification and why does it matter?</summary>
                            <div class="faq-body">The WTA (Wissenschaftlich-Technische Arbeitsgemeinschaft) is the German scientific association for building maintenance and monument preservation. WTA Merkblatt 6-4 defines the internationally recognised technical standard for internal insulation of historic buildings. A WTA-compliant system has been tested to manage moisture correctly in heritage wall constructions, giving architects, conservation officers and homeowners confidence that the insulation will protect, not harm, the historic fabric.</div>
                        </details>
                        <details class="faq-item">
                            <summary>Can BreatheTherm be used on timber-framed or cob buildings?</summary>
                            <div class="faq-body">Yes. The vapour-permeable nature of BreatheTherm materials makes them particularly suitable for timber-frame, wattle-and-daub, cob, and flint construction, all of which need to breathe freely. We adapt the specification for each substrate. Our technical team will advise on the most appropriate system for your specific construction type on the free assessment visit.</div>
                        </details>
                    </div>
                    <button type="button" class="text-link faq-toggle" id="faqToggle" aria-expanded="false" aria-controls="faq-more">More questions</button>
                </div>
            </div>
        </section>"""


def render_index(posts: list[dict]) -> str:
    prefix = "../"
    url = f"{SITE}/guides/"
    feature = posts[0]
    rest = posts[1:]
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "BreatheTherm Journal",
        "description": "Notes on breathable insulation, listed building consent, U-values and WTA 6-4 for pre-1919 solid walls.",
        "url": url,
        "publisher": {"@type": "Organization", "name": "BreatheTherm", "url": SITE + "/"},
        "blogPost": [
            {
                "@type": "BlogPosting",
                "headline": p["title"],
                "description": p["description"],
                "url": f"{SITE}/guides/{p['slug']}/",
                "datePublished": p["date"],
                "image": SITE + p["hero"],
            }
            for p in posts
        ],
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "url": f"{SITE}/guides/{p['slug']}/",
                    "name": p["title"],
                }
                for i, p in enumerate(posts)
            ],
        },
    }
    extra = f"""    <meta name="keywords" content="breathable insulation, listed building consent, WTA 6-4, solid wall insulation, internal wall insulation, hygrothermal modelling">
    <script type="application/ld+json">
    {json_ld(blog_ld)}
    </script>
{INDEX_FAQ_LD}"""

    rest_html = "".join(
        f'''                    <li>
                        <a href="./{html.escape(p["slug"], quote=True)}/">
                            <time datetime="{p["date"]}">{format_date(p["date"])}</time>
                            <h2>{html.escape(p["title"])}</h2>
                            <p>{html.escape(p["dek"])}</p>
                        </a>
                    </li>'''
        for p in rest
    )
    feature_img = asset_src(feature["hero"], prefix)
    main = f"""        <section id="journal" class="band journal-hero journal-index-hero grain" aria-labelledby="journal-title">
            <div class="container">
                <p class="eyebrow">Journal</p>
                <h1 id="journal-title">Notes on walls that still have to dry</h1>
                <p class="journal-index-lead">Breathable insulation, listed building consent, U-values and WTA 6-4, written for the first serious conversation about a pre-1919 wall.</p>
                <article class="journal-feature-card">
                    <a class="feature-copy" href="./{html.escape(feature["slug"], quote=True)}/">
                        <time datetime="{feature["date"]}">{format_date(feature["date"])}</time>
                        <h2>{html.escape(feature["title"])}</h2>
                        <p>{html.escape(feature["dek"])}</p>
                        <span class="text-link text-link-light">Read the note</span>
                    </a>
                    <a href="./{html.escape(feature["slug"], quote=True)}/">
                        <img src="{feature_img}" alt="{html.escape(feature["hero_alt"], quote=True)}" width="800" height="600">
                    </a>
                </article>
                <ul class="journal-index-list">
{rest_html}
                </ul>
            </div>
        </section>
{INDEX_FAQ_HTML}
        <section class="band band-paper">
            <div class="container">
                <nav class="next-steps" aria-label="Next steps">
                    <a class="text-link" href="../solutions/">See the system</a>
                    <a class="text-link" href="../products/">See the products</a>
                    <a class="text-link" href="../projects/kerry-cottage/">See the Cotswold farmhouse</a>
                </nav>
            </div>
        </section>"""
    return page_shell(
        title="Breathable insulation journal",
        description="Why vapour-open build-ups matter in solid masonry, and what breathable actually means on a pre-1919 wall.",
        canonical=url,
        og_type="website",
        og_image=SITE + "/assets/images/london-stock-brick-terrace.jpg",
        prefix=prefix,
        extra_head=extra,
        body_class="inner-page",
        main=main,
    )


def update_sitemap(posts: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text()
    text = re.sub(
        r"  <url><loc>https://www\.breathetherm\.co\.uk/guides/[^<]*</loc>(?:<lastmod>[^<]+</lastmod>)?</url>\n",
        "",
        text,
    )
    latest = max(p["updated"] for p in posts)
    block = (
        f"  <url><loc>{SITE}/guides/</loc><lastmod>{latest}</lastmod></url>\n"
        + "".join(
            f"  <url><loc>{SITE}/guides/{p['slug']}/</loc>"
            f"<lastmod>{p['updated']}</lastmod></url>\n"
            for p in posts
        )
    )
    marker = "  <url><loc>https://www.breathetherm.co.uk/display/</loc></url>\n"
    if marker not in text:
        raise SystemExit("sitemap is missing the /display/ URL used as an insert marker")
    path.write_text(text.replace(marker, marker + block, 1))


def check_em_dashes(posts: list[dict]) -> None:
    bad = []
    for p in posts:
        blob = p["title"] + p["description"] + p["dek"] + p["body_html"]
        for item in p.get("faq") or []:
            blob += item["q"] + item["a"]
        if "—" in blob or "–" in blob:
            bad.append(p["slug"])
    if bad:
        raise SystemExit(f"Em or en dashes in: {', '.join(bad)}")


def main() -> None:
    posts = load_posts()
    if not posts:
        raise SystemExit("No journal posts found")
    check_em_dashes(posts)
    for post in posts:
        dest = GUIDES / post["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render_post(post, posts))
        print(f"wrote {dest.relative_to(ROOT)}")
    (GUIDES / "index.html").write_text(render_index(posts))
    print("wrote guides/index.html")
    update_sitemap(posts)
    print("updated sitemap.xml")


if __name__ == "__main__":
    main()
