# BreatheTherm homepage audit (Step 0)

Date: 10 September 2026
Scope: live homepage at repo root (`index.html`, `styles.css`, `main.js`). No files were edited.
Method: source inspection plus WCAG 2.2 relative-luminance contrast maths (sRGB). Ratios are for the computed token colours, including alpha composites onto the actual section backgrounds.

---

## 1. Stack, tooling, tokens, fonts

### Stack

Static HTML, CSS and vanilla JavaScript. No bundler, no `package.json`, no README, no `.gitignore`. Hosted as GitHub Pages (`CNAME` is `www.breathetherm.co.uk`). Live site returns 200 at `https://www.breathetherm.co.uk/`.

Google Analytics (`G-N7S93FQQKV`) is in the document head. Phosphor icons load from `https://unpkg.com/@phosphor-icons/web`. A Google Calendar appointment widget is injected inside the homeowner modal.

`main.js` looks for `#leadForm` and posts nowhere. The form is not on the homepage. The handler comments a Formspree or Netlify Forms TODO, then shows a success state immediately. That success node (`#formSuccess`) is present but unreachable.

### How to run locally

From the repo root, any static server:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`. Opening `index.html` as a file also works for layout, but relative asset paths and later multi-page routes (`/will-it-work`, `/privacy`) need a server.

### Where CSS lives

| File | Role |
| --- | --- |
| `styles.css` | Live design system and all homepage styles. Tokens in `:root`. |
| `v3/styles.css`, `v4/styles.css`, `v5/stylesOLD.css` | Previous visual versions. Not linked from the live page. |
| `interactive/styles.css`, `3D/style.css` | Prototype tools. Not linked from the live page. |

Leftover rule blocks in live `styles.css` that nothing on the homepage uses: `.stats-band`, `.system-section`, `.grants-section`, `.process-section`, `.lead-form` (the form markup was removed; the CSS remains).

There is a stray extra `}` after `.price-callout h4` (around line 1006). The following `.price-callout p` rule still parses.

### Design tokens

All brand colours are CSS custom properties in `styles.css` `:root`. Important mismatch: `--terra` has been remapped to WhatsApp green `#25D366` (comment still shows the old terracotta `#F1513B`), while `--terra-dark` (`#c9402b`) and `--terra-light` (`rgba(241, 81, 59, 0.13)`) still describe terracotta. Green buttons therefore hover to a red-brown. `--sh-terra` still uses the old terracotta shadow.

`--whatsapp` is the same hex as `--terra` (`#25D366`).

`--terr` is referenced on `.path-icon i` and is not defined.

Hotspot focus and hover use `#00aaff`, which is not a token.

| Token | Hex or value | Notes |
| --- | --- | --- |
| `--primary` | `#00479A` | Brand blue |
| `--primary-dark` | `#003373` | |
| `--primary-mid` | `#005CBF` | |
| `--primary-light` | `rgba(0, 71, 154, 0.09)` | Composites to about `#e8eef6` on white |
| `--sage` | `#3CC6B0` | |
| `--terra` | `#25D366` | Now WhatsApp green, not terracotta |
| `--terra-dark` | `#c9402b` | Still terracotta |
| `--terra-light` | `rgba(241, 81, 59, 0.13)` | Still terracotta |
| `--navy` | `#1664AD` | |
| `--navy-dark` | `#0E467D` | Footer |
| `--success` | `#3A7D44` | Table RAG |
| `--error` | `#C0392B` | Table RAG |
| `--whatsapp` | `#25D366` | Sticky button |
| `--bg` | `#ffffff` | |
| `--cream` | `#f8fbfc` | |
| `--cream-mid` | `#edf4f7` | |
| `--cream-deep` | `#dfeaee` | |
| `--stone-100` | `#d2dee4` | |
| `--stone-200` | `#b5c8d1` | |
| `--stone-400` | `#869ea9` | |
| `--ink` | `#0a192f` | |
| `--ink-mid` | `#23395b` | Default body |
| `--ink-light` | `#5c748e` | Muted body: fails on cream-mid and cream-deep |
| `--ink-xlight` | `#95aec7` | Placeholders, unused hint text |
| `--white` | `#ffffff` | |
| `--font-sans` | `'DM Sans', sans-serif` | |
| `--font-serif` | `'Playfair Display', Georgia, serif` | Headings |
| Radii | `--r-sm` 6px through `--r-pill` | |
| Shadows | `--sh-sm` through `--sh-xl`, plus brand `--sh-primary` and `--sh-terra` | |

Non-token colour in use: comparison RAG amber `#fbbf24`.

### Fonts

Loaded from Google Fonts in `index.html`:

- Playfair Display (400, 500, 700, italic) for `h1`–`h3` and a few display numbers
- DM Sans (300, 400, 500, 600, italic, optical size 9–40) for body, UI, `h4`

No other families. Phosphor is an icon font, not a text face.

Type scale is not consistent. Global `h1`/`h2`/`h3` exist, then `#approach h2` overrides to a different clamp, plus one-off sizes down to `0.62rem` (~10px) on modal tags and `0.67rem` on spec keys. Body is `1rem` / 1.65–1.78. Captions and chips regularly fall below 13px.

---

## 2. Homepage sections in scroll order

| Order | Section | Anchor id | Notes |
| --- | --- | --- | --- |
| 0 | Fixed header | `#main-nav` | Not in document flow. Logo is not a home link. |
| 1 | Mobile drawer | `#mobile-nav` | Off-canvas, same targets as desktop. |
| 2 | Hero | `#hero` | Full-viewport photo, navy copy panel, 65% stat chip. Overlay and grain markup are commented out. |
| 3 | Why insulation fails | `#problem` | Three problem cards. CTA points at `#solution`, which does not exist. |
| 4 | Our approach | `#approach` | How-it-works list plus six benefit tiles. This is the nearest thing to "The System", but the nav does not point here. |
| 5 | Interactive Layer Guide | `#explorer` | Cross-section, legend, spec panel. |
| 6 | Conventional vs BreatheTherm | `#price` | Nine-row comparison table plus dark callout. |
| 7 | Select your profile (first set) | `#paths` | Owners / Architects / Installers cards, open modals. |
| 8 | Past projects | `#proof` | Three case cards. None are links. |
| 9 | Testimonials | `#testimonials` | Nick, Christopher, Patricia. |
| 10 | Team | `#team` | Josh Tetley, Greg Podolak. |
| 11 | FAQ | `#faq` | 14 `<details>` items. No grants item. |
| 12 | Contact | `#contact` | Phone, email, WhatsApp, then a **second** set of the three profile cards. `#formSuccess` is hidden and unused. |
| 13 | Trust band | none | WTA, RIBA CPD, Green Register, Historic England. Not a `<section>`. |
| 14 | Footer | none | Navigate / For You / Contact. |

Off-flow: `#modal-homeowner`, `#modal-architect`, `#modal-installer`, sticky WhatsApp.

**Missing ids that other links expect:** `#solution`, `#grants`. There is no `#privacy`.

**Ids present but unused by nav:** `#approach`, `#price`, `#paths`, `#testimonials`, `#team`, `#hero`.

---

## 3. Dead, empty, or broken links

Checked every `href` on the live homepage.

| Link text / location | Target | Status |
| --- | --- | --- |
| Nav, mobile nav, footer: "The System" | `#solution` | **Dead.** No `id="solution"`. Closest content is `#approach`. |
| Problem CTA: "See the BreatheTherm solution" | `#solution` | **Dead.** Same. |
| Footer: "Grants & Funding" | `#grants` | **Dead.** No grants section. CSS for `.grants-section` is leftover. JSON-LD contains a grants FAQ that is **not rendered** on the page. Visible mentions: Owners card "Grant funding guidance"; homeowner modal "Grant and finance eligibility check". |
| Footer: "Privacy Policy" | `#` | **Empty hash.** No privacy page. |
| Instagram | `https://www.instagram.com/breathetherm_/` | URL is well-formed. A HEAD request hit Instagram's login wall (HTTP 429), so the profile was not confirmed from this environment. Not treated as a site 404. |
| WhatsApp (several) | `https://wa.me/+447887591971` | Well-formed. Not fetched. |
| Tel / mailto | `01285 407088`, `hello@breathetherm.co.uk` | Well-formed. |
| Google Calendar widget (homeowner modal) | Google appointments URL | Third-party. Not fetched. |
| Logo in header and footer | no `href` | Not a link. |

Working in-page anchors: `#problem`, `#explorer`, `#proof`, `#faq`, `#contact`, `#paths`.

`#leadForm` is referenced in JS and does not exist.

No other `href="#"` on the live homepage. Older trees (`v3`, `v4`, `v5`) repeat the Privacy Policy `#` and add a "Learn More About Our System" `#` in the architect modal: those files are not the live page.

---

## 4. Images: alt text and filenames

### Used on the live homepage (including modals and CSS backgrounds)

| File | Where | Alt / accessible name | Issue |
| --- | --- | --- | --- |
| `Breathatherm-logo-22-3-1.png` | Header, footer | `BreatheTherm Logo` | Generic. Filename misspells the brand and carries a version suffix. |
| `BT-hero-bkg.jpg` | Hero CSS background | none (CSS) | Content image with no text alternative. Overlay that would darken it is commented out. |
| `TF-icon-efiiciency_edited.png` | Approach tile 1 | `alt=""` + `aria-hidden="true"` | Decorative, acceptable. Filename: typo "efiiciency", `_edited` suffix. |
| `TF-icon-breathability_edited.png` | Approach tile 2 | empty / hidden | Same pattern. |
| `TF-icon-heritage_edited.png` | Approach tile 3 | empty / hidden | Same. |
| `TF-icon-sustainability_edited.png` | Approach tile 4 | empty / hidden | Same. |
| `TF-icon-easy_edited.png` | Approach tile 5 | empty / hidden | Same. |
| `TF-icon-health_edited.png` | Approach tile 6 | empty / hidden | Same. |
| `BT cutaway.webp` | Layer Guide SVG `<image>` | Parent SVG `aria-label="BreatheTherm wall build-up cross-section"` | Space in filename. Label names the brand, not what the drawing shows. No visible caption. |
| `Marcus.jpg` | Cheltenham project card | **missing** | First name as a filename. Photo is a stripped brick bedroom with lath ceiling, Upper Park Street. Nested `.case-img` twice. |
| `VicMan.webp` | Bristol project card | **missing** | Cryptic contraction. Photo is a red-brick mansion-block street frontage, not a terrace. |
| `C17CotsFarm.jpeg` | Gloucestershire project card | **missing** | Cryptic. Aerial of a Cotswold stone farmhouse and outbuilding. |
| `josh-bio-picture.jpg` | Team | `Josh Tetley, Co-Founder of BreatheTherm` | Acceptable person alt. Filename is intern-style. |
| `greg-bio-picture.png` | Team | `Greg Podolak, Co-Founder of BreatheTherm` | Same. |
| `BT bad wall.png` | Homeowner modal | **missing** | Spaces. Mould and peeling plaster on a solid wall, brick exposed. |
| `surveyor in action.webp` | Architect modal | **missing** | Spaces. Stock-style photo of a man in hard hat using a theodolite. Not obviously a BreatheTherm survey. |
| `Installer interior.jpg` | Installer modal | **missing** | Spaces. Period interior with ladders, stripped plaster, arched opening. |

No `<figcaption>` or caption class exists anywhere.

### Unused in `/assets/images/` (unprofessional or generic names still on disk)

`68b17c23e4d44.webp`, `Approach.jpg`, `BREATHABILITY.jpg`, `BT cutthrough.jpg`, `BT hero image from Josh.jpg`, `BT-S100-hero.jpg`, `COMFORT.png`, `COMPATIBILITY.png`, `EnEff.png`, `ENERGY.jpg`, `HERITAGE.jpg`, `PrettyHouses.jpg`, `rob-bio-picture.png`, `stone-wall.jpg`, `stone-wall.png`, `stone-wall.webp`, `SUSTAINABILITY.jpg`, `wall2d.jpg`.

`assets/BT_demohouse.png` and `interactive/BT_demohouse.png` belong to the 3D / interactive prototypes.

---

## 5. Colour contrast report

Thresholds used: 4.5:1 body text (including small eyebrows, captions, chips, table headers), 3:1 large text (18pt+ or 14pt+ bold) and UI components (buttons, icons, focus).

`--terra` (`#25D366`) and `--sage` (`#3CC6B0`) are too light to be text or to carry white text. `--ink-light` (`#5c748e`) only clears 4.5:1 on pure white or `--cream`. `.eyebrow` adds `opacity: 0.6`, which knocks otherwise-passing ink below 4.5:1.

### Passes

| Pair | Where | Ratio | Threshold |
| --- | --- | --- | --- |
| `--ink-mid` on white | Nav, FAQ, explorer body | 11.62 | 4.5 |
| `--ink` on `--cream-mid` | Problem, projects headings | 15.83 | 4.5 |
| `--ink-mid` on `--cream-mid` | Problem body | 10.45 | 4.5 |
| `--ink-light` on white | Case-card body, team bio | 4.83 | 4.5 |
| `--ink-light` on `--cream` | Problem-card body, testimonial role | 4.65 | 4.5 |
| `--primary` on `--cream-mid` | `.tag` | 7.98 | 4.5 |
| `--primary` on `--primary-light` (~`#e8eef6`) | Metric pills, avatars | 7.60 | 4.5 / 3 |
| White on `--primary` | Paths and contact headings, primary buttons | 8.87 | 3 / 4.5 |
| White on `--navy` | Hero H1 (solid navy, large) | 6.07 | 3 |
| White on `--primary-mid` | Table "BreatheTherm" header, hotspot labels | 6.40 | 4.5 / 3 |
| `--terra` on `--primary-dark` | Hero 65% figure, price-callout h3 (large) | 6.15 | 3 |
| `--cream` on `--navy-dark` | Footer copy and links | 8.62 | 4.5 |
| White on `--terra-dark` | Green button in hover state only | 4.94 | 3 |
| White on `--navy` | Navy buttons | 6.07 | 3 |
| Case-tag white on 45% black over the three project photos | Sampled brick, red facade, stone, grass | 5.91–9.80 | 4.5 |
| Focus ring `--primary` on white | Global `:focus-visible` | 8.87 | 3 |

### Fails: body text (below 4.5:1)

| Pair | Where | Ratio | Notes |
| --- | --- | --- | --- |
| `--sage` on `--navy` | Hero eyebrow | 2.86 | Worse (~2.40–2.64) once the 90% navy panel is composited over the pale facade. |
| White at 0.72 on `--navy` | Hero sub-line | 3.98 | 3.46–3.75 over the photo. |
| White at 0.45 on `--primary-dark` | Hero "Average Reduction in heat loss" | 3.66 | The 65% number itself passes as large. |
| Ink at 0.6 on `--cream-mid` | "WHY INSULATION FAILS" and other light-section eyebrows | 4.47 | `.eyebrow { opacity: 0.6 }`. |
| Cream at 0.6 on `--navy` | "OUR APPROACH" | 3.16 | |
| `--cream-deep` at 0.85 on `--navy` | Approach intro | 4.05 | |
| `--cream-deep` at 0.75 on `--navy` | How-it-works body copy | 3.49 | |
| `--ink-light` on `--cream-deep` | Benefit tile descriptions, price-key, trust-band descriptions | 3.95 | |
| `--ink-light` on `--cream-mid` | Price-section intro (inline style) | 4.35 | |
| `--ink-light` on `--primary-light` | "Conventional Insulation" table header | 4.14 | |
| `--terra` on `--cream-deep` | Layer Guide guide price | 1.62 | Almost invisible. |
| `--stone-400` on `--cream` | Spec keys Thickness / λ / Sd | 2.70 | 0.67rem type. |
| White at 0.55 on `--primary` | Paths intro and card intros | 3.78 | |
| White at 0.60 on `--primary` | Paths "ABOUT YOU" eyebrow | 4.20 | |
| White at 0.50 on `--primary` | Paths feature lists | 3.39 | |
| `--sage` on `--primary` | Contact trust chips ("Free assessment") | 4.18 | |
| White at 0.45 on `--primary` | Contact "Get Started" `.tag--ghost` | 3.03 | |
| `--terra` on `--terra-light` | Modal "For Owners" tag | 1.69 | |
| `--ink-xlight` on white | Form privacy line (CSS only, form missing) | 2.29 | |
| `--ink-xlight` on `--cream` | Input placeholders | 2.21 | |
| White at 0.9 on 50% white over `--navy-dark` | Footer WTA / RIBA / Green Register pills | 2.44 | |

### Fails: large text or UI (below 3:1)

| Pair | Where | Ratio | Notes |
| --- | --- | --- | --- |
| White on `--terra` | **Every `.btn-terra`**: hero Contact Us, path CTAs, form submit, outline-terra | 1.98 | Highest-traffic buttons on the page. |
| `--terra` on white | Outline terra buttons | 1.98 | |
| `--terra` on `--cream` | Testimonial stars | 1.91 | Decorative, still a UI graphic. |
| White on `--whatsapp` | Sticky WhatsApp icon | 1.98 | |
| `--terra` italic on `--navy` | Hero H1 emphasis, approach H2 emphasis | 3.06 solid / **2.57–2.82** over the photo | Large-text borderline on a solid fill, fail once the panel is 90% opaque over yellow brick or white stucco. |
| White at 0.75 on `--terra` | Homeowner modal tagline if it sits on the green end of the gradient | 1.64 | Modal hero photos sit in the tagline with no dark overlay. |
| White at 0.4 on `--terra` | Modal "average bill reduction" small print | 1.28 | |
| `#00aaff` glow | Layer Guide hotspot focus | not a brand colour | `:focus` and `:focus-visible` both set `outline: none`. |

### Hero-on-photo, specifically

The gradient overlay (`.hero-overlay`) and grain are **commented out in HTML**. Copy sits in `.hero-content` at `background: var(--navy); opacity: 0.9` over `BT-hero-bkg.jpg` (pale London-stock terrace, white stucco, bright sky). The 65% chip sits on the photograph in `--primary-dark`.

| Sample | Result |
| --- | --- |
| White H1 on navy@0.9 over yellow brick | 5.59, pass as large |
| White H1 on navy@0.9 over white stucco | 5.10, pass as large |
| Green italic H1 over those same samples | 2.82 and 2.57, **fail even as large** |
| Sage eyebrow over those samples | 2.64 and 2.40, fail |
| 0.72 white sub-line over those samples | 3.75 and 3.46, fail as body |

---

## 6. Templated or AI-looking patterns

### Confirmed on the live page

- **Emoji ticks:** four `✅` characters in "How breathable insulation works" (`index.html` around the approach list). CSS comments also use `✅`. Modal lists use a `✓` in `::before`.
- **Six identical benefit tiles:** ENERGY EFFICIENCY, BREATHABILITY, HERITAGE FRIENDLY, SUSTAINABILITY, COMPATIBILITY, COMFORT & WELL-BEING. Same 80px icon + uppercase label + generic sentence. This is the block Step 8 archives.
- **Two identical rows of three profile cards** (`#paths` and `#contact`), same component, same hover lift and 48px icon circles.
- **Three testimonial cards** cloned: five `★`, letter avatar (N / C / P), name, town. Stars fail contrast.
- **Four trust-band items** with the same 36px icon-in-rounded-square treatment.
- **Card hover formula everywhere:** `translateY(-4px)` plus a larger shadow on case cards, team cards, path cards, problem cards, FAQ items, grant cards (unused). Sticky WhatsApp scales and glows `rgba(37,211,102,0.4)`.
- **Cyan hover/focus glow** on Layer Guide hotspots: `drop-shadow(0 0 6px #00aaff)`. Not a brand colour. Looks like a default interactive-demo effect.
- **Modal hero gradients** (`linear-gradient(145deg, …)`) behind, and sometimes under, the photos.
- **Hero overlay and film-grain** still in CSS (commented in HTML): generic template leftovers.
- **Boilerplate superlatives and interchangeable sentences:**
  - Meta: "The UK's leading breathable insulation system"
  - Footer: "Premium breathable insulation systems… Protecting historic fabric. Improving lives. Reducing emissions."
  - Paths intro: "each path is different but every outcome is the same"
  - Projects intro: "Every project is different. Every outcome is the same: a warmer, drier, healthier building…"
  - Owners: "Future-proof your heritage building"
  - Approach: "efficiency genuinely improves"
  - Installer modal: "Join the Network." / "Own the Market."
  - Architect modal: "Specification-ready. Conservation-compliant."
  - Homeowner modal: "Your Heritage Home, protected for generations"
  - Price eyebrow: "RETROFIT WITHOUT REGRET" / "Invest in BreatheTherm. Enjoy the savings for years"
- **Letter-spacing on eyebrows** is 0.12–0.16em (hero 0.16em, `.tag` 0.14em), above the 0.08em cap in Step 9.
- **No image captions.** The site has no caption motif yet.

`genuinely` appears once on the live page. `seamlessly`, `cutting-edge`, `unlock`, `elevate` do not appear on the live homepage. They do appear in archived `v3`/`v4`/`v5` copy.

### Structural tells (not visual chrome, still template)

- Heading skips: problem cards and project cards use `h4` under `h2`. Footer uses `h5`.
- No `<main>`, no skip link, sections do not use `aria-labelledby`.
- One H1, which is correct.
- Layer Guide hotspot `aria-label`s do not match the visible layer names (W1 announced as PerliTherm, W2 as Aerogel Boost, W3–W5 all as Perlifinish).
- Legend items are `tabindex="0"` but only handle `click`, not Enter or Space.
- Comparison RAG dots are colour alone (green / amber / red) with no text equivalent.
- `html { scroll-behavior: smooth }` and card/reveal motion ignore `prefers-reduced-motion` except the hero parallax.
- Touch targets under 44px: modal close 32px, hamburger (~28px tall), legend items (~31px), metric pills, footer badge pills, `.tag` at 0.68rem.

---

## 7. Content and trust issues already in the brief (confirmed)

| Issue | Evidence |
| --- | --- |
| 65% claim is inconsistent | Hero: "65% Average Reduction in heat loss". Owners card: "Energy savings up to 65%". Homeowner modal: "65% average bill reduction". |
| Bristol card tag vs title | Tag: "Victorian Terrace · Bristol". Title: "Victorian Mansion Block, 12 Units". Photo is a mansion-block facade. |
| `#grants` | Footer only. No target. Grants FAQ exists in JSON-LD only, not as a visible `<details>`. |
| Privacy Policy `#` | Footer. No page. |
| "succesful" | Patricia, Fairford testimonial. |
| `Marcus.jpg` and other filenames | See section 4. |
| Missing alts on project and modal photos | See section 4. |
| Profile cards appear twice | `#paths` and `#contact`. |
| `#solution` dead | Nav label "The System" has no destination. |

### Other copy defects (not in the brief, logged for later steps)

- Em dashes in live copy: Josh bio, Greg bio, timber-frame FAQ, homeowner modal ("No hard sell — just clear, honest advice."), architect modal. Also en dashes in ranges (`2–5 days`, `£8,000–£20,000`) and placeholder em dashes (`—`) in the layer card.
- "FYI lime plaster" in the installation-time FAQ (visible and JSON-LD).
- Footer legal line: "Breathe Therm Ltd" (space in the name).
- JSON-LD FAQs do not match the visible list (JSON-LD includes cost and grants, omits several visible questions, and uses different listed-building wording).
- Visible FAQ has no grants question, so Step 1 cannot point `#grants` at an existing FAQ node without first adding one (copy already exists in JSON-LD).
- Layer data in `main.js` still contains editorial artefacts: double spaces, "[1, 2]" citations, `thick: '[75mm - 200mm'`.
- Company number `16491516` and VAT `505 972 871` are in the footer; not verified here.

### Facts already on the page (usable later, not to invent beyond)

Cheltenham: Upper Park Street bedroom, bare brick, retained lath ceiling, PerliScratch / AeroBond / mesh / PerliTherm 25mm, walls −46%, ceiling −38%.

Bristol: 12 flats, internal wall insulation, hygrothermal monitoring, U-value 0.19, bills −71%, zero moisture failures at 36 months.

Gloucestershire: Grade I, 17th-century Cotswold farmhouse, solid stone, cob, original lime plaster, U-value 0.22, bills −52%, Historic England.

Testimonials: Nick (Cirencester), Christopher (barn conversion, Bristol), Patricia (Fairford).

Team: Josh Tetley (HF Limited 2003), Greg Podolak (joined 2007, HF Building 2016), BreatheTherm 2024, "combined 45 years".

System names: PerliScratch, PerliTherm, AeroBond, AeroGel, PerliFinish, PerliMat, Perlibase, Perlistruct, PerliScreed.

Architect offer (on the card and in the modal): WTA-compliant system, hygrothermal modelling, BIM/CAD, conservation area approval record, RIBA CPD, NBS clauses.

5.9 million pre-1919 buildings: used in problem copy and installer card.

Address, phone, email, WhatsApp, Instagram handle: as in the footer.

---

## 8. Accessibility and IA extras (for Steps 2 and 9)

- Global `:focus-visible` is a 2px `--primary` ring, then several components undo it (`outline: none` on hotspots and focused inputs, replaced by a cyan glow or a box-shadow).
- `prefers-reduced-motion` only wraps hero parallax. Reveals, hover lifts, modal scale, WhatsApp pulse-scale, and `scroll-behavior: smooth` still run.
- No skip link. No `<main>`.
- Contact "form" is not a form. Labels, errors, and `autocomplete` therefore do not exist on the live page, though `.lead-form` CSS assumes they will.
- Layer Guide hotspots are keyboard-reachable (`tabindex="0"`, Enter/Space). Legend items are not fully operable from the keyboard.
- One H1. Skipped heading levels as in section 6.

---

## 9. Out of scope trees (do not ship, do not delete in later steps unless asked)

`v3/`, `v4/`, `v5/`, `3D/`, `interactive/`, `BreatheTherm_Executive_Summary.html`. These are earlier versions and tools. They repeat many of the same dead links and are not in the live navigation.

---

## 10. Suggested commit order (no work done)

Step 0 is this file only. Waiting for go-ahead before Step 1.

Known Step 1 dependencies from this audit:

1. Align 65% wording and add the confirm comment in three places (hero, owners card, homeowner modal).
2. Relabel the Bristol tag.
3. `#grants`: the grants answer is only in JSON-LD. To point the nav/footer at "the FAQ answer that mentions grant guidance", a visible FAQ item must be added from that existing JSON-LD copy, or the footer item removed.
4. Privacy placeholder page.
5. Fix "succesful".
6. Rename images to kebab-case and write real alts. Spaces in current filenames (`BT cutaway.webp`, `BT bad wall.png`, `surveyor in action.webp`, `Installer interior.jpg`) will break if renamed without updating every reference, including the SVG `href` and the CSS `background-image`.
