# Journal post format

Every new journal entry is one Markdown file in this folder. Required front matter first, then the article in a fixed heading order. Run `python3 scripts/build-journal.py` from the repo root. It writes `/guides/<slug>/index.html`, rebuilds `/guides/index.html`, and adds the new URLs to `sitemap.xml`.

Do not use em dashes or en dashes. Use a comma, a colon, a period, or "to".

## Front matter

```yaml
title:              # H1. Include the primary search phrase. Title case, no trailing period.
slug:               # kebab-case, matches the live URL /guides/<slug>/
description:        # 140 to 160 characters. Completes the search intent. No quotes.
dek:                # One-line standfirst under the H1. Completes "why this page exists".
date:               # YYYY-MM-DD, first published
order:              # Integer. Lower numbers appear first on the journal index.
updated:            # YYYY-MM-DD, last factual edit (optional; defaults to date)
author:             # Display name. Default BreatheTherm.
reading_minutes:    # Integer, honest reading time
hero:               # Site-root path, /assets/images/...
hero_alt:           # Describe the masonry or room, not the brand.
primary_keyword:    # The phrase the H1 and first paragraph must contain
keywords:           # 5 to 9 related phrases, used in meta and naturally in copy
products:           # 2 to 4 products this article should sell through, not mention in passing
  - name:
    href:           # /products/perlitherm/
    note:           # One clause on why it belongs here
related:            # 2 or 3 other journal slugs
  - slug:
    title:
faq:                # 4 to 6 questions a searcher or model would ask after the article
  - q:
    a:              # Standalone answer, 40 to 60 words, cite a product or page where it helps
```

## Body order

1. Opening paragraph. Answer the H1 in two or three sentences. Name the primary keyword once. No preamble.
2. `##` headings, in reading order, each a complete search phrase. Six is the default. Do not skip levels. Do not use `####`.
3. One `>` callout. The sentence a conservation officer or homeowner could quote.
4. Product names as Markdown links to `/products/<slug>/`. Glossary terms to `/glossary/#anchor`. Solutions, projects and audience pages the same way.
5. Close on what to do next, then the FAQ heading (the builder renders FAQ from front matter, so do not duplicate it in the body).

## Linking rules

- Each product in `products:` must appear as a link in the body.
- Link related posts by slug (`/guides/<slug>/`), not by homepage.
- Link `/solutions/internal-walls/`, `/solutions/floors/` or `/solutions/external-walls/` when the build-up is the point.
- Link `/for-architects/` when consent, WTA or specification is the point.
- Link `/contact/` once, near the end, as the action.
- Do not link the same URL twice in one section.

## SEO and GEO checklist

- H1, title tag and `og:title` are the same string.
- Description is unique, includes the primary keyword, and reads as an answer.
- First 100 words could stand as a featured snippet.
- FAQ answers are self-contained so a model can cite them without the article.
- Facts that can go stale (U-values, thicknesses, prices) match the product pages.
- Canonical is `https://www.breathetherm.co.uk/guides/<slug>/`.
