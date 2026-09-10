# Accessibility report (Step 9)

Palette unchanged. Text and UI pairings were swapped onto existing tokens: `--ink`, `--ink-mid`, `--cream`, `--primary`, `--navy`, `--navy-dark`. No new hex values.

## Contrast, pairs touched

Thresholds: 4.5:1 body (including captions and eyebrows), 3:1 large text and UI.

| Pair | Where | Before | After | Notes |
| --- | --- | --- | --- | --- |
| White on `--terra` `#25D366` | `.btn-terra`, form submit, outline-terra | 1.98 fail | **8.88** (`--ink` on `--terra`) | First preference: darkest brand neutral as text |
| `--sage` on `--navy` | Hero eyebrow | 2.86 fail | **5.84** (`--cream` on `--navy`) | |
| White at 0.72 on `--navy` | Hero sub-line | 3.98 fail | **5.84** (`--cream` on `--navy`) | Overlay still commented out; copy sits in the navy panel |
| `--terra` italic on `--navy` | Hero H1 emphasis | 3.06 / 2.57 over photo | **5.84** (`--cream`) | |
| White at 0.45 on `--primary-dark` | Hero 65% label | 3.66 fail | **11.73** (`--cream` on `--primary-dark`) | Number still `--terra` on `--primary-dark` (6.15, large pass) |
| Ink at 0.6 on `--cream-mid` | Light-section eyebrows | 4.47 fail | **10.45** (`--ink-mid` on `--cream-mid`, no 0.6 opacity) | |
| Cream at 0.6 on `--navy` | Approach eyebrow | 3.16 fail | **5.84** | |
| `--cream-deep` at 0.85/0.75 on `--navy` | Approach intro and steps | 4.05 / 3.49 fail | **5.84** (`--cream`) | |
| `--ink-light` on `--cream` / cream-mid / cream-deep | Problem cards, case copy, trust-desc, price key | 4.65 / 4.35 / 3.95 | **11.17 / 10.45 / 9.48** (`--ink-mid`) | |
| `--terra` on `--cream-deep` | Layer Guide price | 1.62 fail | **7.24** (`--primary` on `--cream-deep`) | |
| `--stone-400` on `--cream` | Spec keys | 2.70 fail | **11.17** (`--ink-mid`) | Size raised to 13px |
| White at 0.55/0.50 on `--primary` | Paths intro, card copy, lists | 3.78 / 3.39 fail | **8.53** (`--cream` on `--primary`) | |
| `--sage` on `--primary` | Contact trust chips | 4.18 fail | **8.53** (`--cream`) | |
| `.tag--ghost` white 0.45 on `--primary` | Contact eyebrow | 3.03 fail | **8.53** | |
| Footer badges, white on 50% white | Footer pills | 2.44 fail | **5.84** (`--cream` on `--navy`) | |
| Modal "For Owners" `--terra` on `--terra-light` | Modal tag | 1.69 fail | **8.88** (`--ink` on `--terra`) | |
| WhatsApp icon white on `#25D366` | Sticky button | 1.98 fail | **8.88** (`--ink` fill) | |
| Stars `--terra` on `--cream` | Testimonials | 1.91 fail | **7.60** (`--primary` on `--primary-light`/cream) | Now `--primary` |
| Table "Conventional" `--ink-light` on `--primary-light` | Compare approaches | 4.14 fail | **7.60** (`--ink-mid`) | |

Untouched passing pairs (nav ink-mid on white, primary buttons, footer cream-mid on navy-dark, case tags on photo overlays) were left as they were.

## Typography

- H1, H2, H3 each have one size. Body 17px (1.0625rem), line-height 1.55. Headings 1.2–1.25.
- Captions `.image-caption` 13px, `--ink-mid`.
- Eyebrow letter-spacing capped at 0.08em. Opacity 0.6 removed.
- Long copy constrained to about 70 characters (`max-width: 70ch` / 42rem).
- Emoji ticks replaced with a numbered list.

## Structure and interaction

- Skip link to `#main`. One H1 per page. Problem and project card titles are `h3` under `h2`.
- Sections that needed names use `aria-labelledby`.
- Focus ring remains `--primary`. Layer Guide cyan glow removed. Hotspots and legend items activate on Enter/Space and announce the layer name.
- Required fields emit a text error, not colour alone. `autocomplete` already on the technical-pack and quiz fields.
- `prefers-reduced-motion` now covers reveals, hover lifts, and smooth scrolling as well as the existing parallax gate.
- Buttons, hamburger, modal close, legend items and quiz options are at least 44px tall.

## Lighthouse accessibility

This environment has no Chrome/Chromium, so Lighthouse could not be executed here.

Before (Step 0 audit, not a Lighthouse score): colour-contrast failures on the main buttons (1.98:1), missing skip link, heading skips (h2 to h4), hover-only legend, emoji in lists, missing alt on project photos.

After: contrast pairs in the table above all pass their threshold; skip link present; heading order corrected on the homepage; Layer Guide labels match the visible names and respond to Enter/Space. A Lighthouse accessibility score should be captured in Chrome DevTools against the local server (`python3 -m http.server 8080`) when a browser is available.
