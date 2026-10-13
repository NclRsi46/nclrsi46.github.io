# Design spec (C4)

Read this before changing anything visual. `assets/css/style.css` implements it; if the two disagree, fix one of them in the same commit.

C4 is a spec sheet with an editorial voice: ruled cells, mono uppercase labels, a serif for anything a person reads, and one ink-green accent on warm paper.

## Tokens

All colors are custom properties on `:root`, redefined for dark mode under `@media (prefers-color-scheme: dark)` (guarded by `:root:not([data-theme="light"])`) and again under `:root[data-theme="dark"]`. Never hard-code a color outside these blocks.

| Token | Light | Dark | Role |
|---|---|---|---|
| `--bg` | `#F4EFE0` | `#181612` | Page |
| `--surface` | `#FBF8EE` | `#211E18` | Header strip, photo backdrop |
| `--ink` | `#1E1D1A` | `#E9E4D3` | Text, heavy rules |
| `--muted` | `#5F5B50` | `#A39D8A` | Labels, secondary text |
| `--rule` | `#BDB6A0` | `#3C382D` | Hairlines. Decorative only: below 3:1, never the sole carrier of meaning |
| `--accent` | `#1F5F46` | `#7FC4A0` | See the emphasis budget |

Contrast on `--bg` (WCAG 2.2): ink 14.66 / 14.20, muted 5.90 / 6.67, accent 6.56 / 8.87 (light / dark). Recompute after any token change; every text pair must reach 4.5:1.

## Type

| Role | Family | Size / line-height | Notes |
|---|---|---|---|
| Body (UI text, lists, `dd`) | IBM Plex Sans | 1.0625rem / 1.6; small UI 0.9375rem / 1.5 | |
| Prose (paragraphs a person reads) | Newsreader | 1.125rem / 1.55 | Max 40rem measure |
| Home intro | Newsreader | 1.375rem / 1.45 | Max 36rem |
| Name (home sidebar) | Newsreader 400 | 2.25rem / 1.1, −0.02em | |
| Page title (`.title h1`) | Newsreader 400 | clamp(2.5rem, 6vw, 4rem) / 1.02, −0.02em | |
| Section heading | Newsreader 500 | 1.25rem | Table item heading 1.1875rem |
| Label | IBM Plex Mono 400 | 0.75rem, +0.06em, uppercase | Site code, buttons, footer, `th`, `dt`, keys, codes |
| Nav links | IBM Plex Sans 400 | body size | Muted; current page in ink with an accent ▸ |

Faces actually used: Plex Sans 400, Plex Mono 400, Newsreader 400 and 500 (roman only). Don't ship other weights or italics until a page uses them.

Fonts are self-hosted WOFF2 under `assets/fonts/` with their OFL licenses. Nothing loads from a third-party origin.

## Layout

- `.sheet`: max 68rem, centered. Gutter 1rem on phones, 2rem from 48rem up.
- Header strip: a bordered surface bar with the site code, nav, and theme button. It sits directly on the page's first bordered box.
- Home: the profile sidebar (17rem, sticky) beside the content from 56rem up, stacked below that.
- Inner pages (`_layouts/page.html`): a header block of ruled cells (photo, title, then key/value cells from `kv:` front matter), then numbered sections. With no `kv:` cells the block drops to two columns (`.block-short`).
- Key/value rows (`dl.rows`, Contact): a mono label column of 9.5rem beside the value from 40rem up, stacked below that, with hairline rules between rows.
- A section head is a mono accent number (`01`) plus a serif heading over a 2px ink rule.
- Tables are ruled with hairlines. Under 40rem each row becomes a stacked block and the header row is visually hidden.

## Emphasis budget

The accent is the only color. It is allowed in exactly these places:

1. Link underline (2px) and link hover color
2. Section numbers
3. The current-page marker (▸) in the nav
4. The status dot, once, in the profile sidebar
5. The outer ring around the home headshot
6. Focus outline
7. The "Copied" status text

Intensity ladder, quietest first: muted label → ink text → serif heading → 2px ink rule → accent mark. The loudest marks (photo ring, status dot) appear once per site, both on Home. No bold inside prose. No callout boxes, badges, pills, icons, or skill bars.

## Motion budget

All motion sits inside `@media (prefers-reduced-motion: no-preference)`; with reduced motion nothing moves.

- `main` rises in once per page load: 0.4s, 4px, opacity.
- Links and buttons: color and border transitions, 0.15s.
- Theme change: 0.3s crossfade on background, color, and border, only while the toggle is switching.
- "Copied" text shows for 2s.

Nothing else: no scroll-triggered animation, parallax, typing effects, or hover lifts.

## Photo

- Always a circle, background removed, never a square ID photo. `object-position: 50% 20%` on the `--surface` backdrop.
- Home: 6rem on phones, 11rem from 56rem up. Ring = 1px `--rule`, a 6px `--bg` gap, then 1px `--accent`.
- Inner page header: 7.5rem (5.5rem under 52rem) with a 1px `--rule` ring only.
- Alt text "Nicolas Rossi". Strip all metadata except the sRGB ICC profile.

## JavaScript

`assets/js/site.js` is progressive enhancement only. The theme and copy-email buttons ship `hidden`, and JS reveals them; with JS off the page is complete and has no dead controls. Theme cycles system → light → dark. The copy button reports "Copied" or "Copy failed": browsers can deny clipboard writes, and a silent failure looks like a broken button. CSS and JS URLs carry `?v=<build time>` so returning visitors never pair new HTML with cached old assets. It is stored in `localStorage`, and every read and write is wrapped in try/catch. No tracking and no third-party requests.

## Content

Copy lives in page Markdown files and `_data/*.yml`. Layouts and includes hold structure and labels only. Every fact traces to the resume PDF, the phishing repo's README and results, or a line Nick approved (`_prototypes/copy.md`, kept outside the repo).
