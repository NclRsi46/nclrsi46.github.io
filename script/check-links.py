#!/usr/bin/env python3
"""Check every internal link in the built site. Standard library only.

Walks _site/**/*.html, collects href/src/srcset values, meta refresh targets,
and og:/canonical URLs on this site's own origin, then checks that each target
file exists and that each #fragment names an id in the target page. External
links are listed, not fetched. Exits 1 if anything internal is broken.

Usage: script/check-links.py [site_dir] [--origin https://nclrsi46.github.io]
"""
import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []  # (attr, value)
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for key in ("href", "src"):
            if a.get(key) is not None:
                self.links.append((f"{tag}[{key}]", a[key]))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                self.links.append((f"{tag}[srcset]", part.strip().split(" ")[0]))
        if tag == "meta":
            if (a.get("http-equiv") or "").lower() == "refresh" and "url=" in (a.get("content") or "").lower():
                content = a["content"]
                self.links.append(("meta[refresh]", content[content.lower().index("url=") + 4:].strip()))
            prop = a.get("property") or a.get("name") or ""
            if prop in ("og:url", "og:image", "twitter:image"):
                self.links.append((f"meta[{prop}]", a.get("content") or ""))


def target_file(site, path):
    """Map a URL path to the file GitHub Pages would serve, or None."""
    rel = unquote(path).lstrip("/")
    candidate = site / rel
    if path.endswith("/") or candidate.is_dir():
        candidate = candidate / "index.html"
    if candidate.is_file():
        return candidate
    if not Path(rel).suffix and (site / (rel + ".html")).is_file():
        return site / (rel + ".html")  # Pages serves /foo from foo.html
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site", nargs="?", default="_site")
    ap.add_argument("--origin", default="https://nclrsi46.github.io")
    args = ap.parse_args()
    site = Path(args.site).resolve()
    if not site.is_dir():
        sys.exit(f"no such directory: {site}")

    pages = {}
    for f in sorted(site.rglob("*.html")):
        c = Collector()
        c.feed(f.read_text(encoding="utf-8"))
        pages[f] = c

    broken, external, checked = [], set(), 0
    for f, c in pages.items():
        page_url = "/" + f.relative_to(site).as_posix()
        for attr, raw in c.links:
            if not raw or raw.startswith(("mailto:", "tel:", "data:", "javascript:")):
                continue
            url = urljoin(args.origin + page_url, raw)
            parts = urlsplit(url)
            if f"{parts.scheme}://{parts.netloc}" != args.origin:
                external.add(url)
                continue
            checked += 1
            dest = target_file(site, parts.path or "/")
            where = f"{f.relative_to(site)} {attr}={raw}"
            if dest is None:
                broken.append(f"{where}: no file for {parts.path}")
                continue
            if parts.fragment:
                ids = pages[dest].ids if dest in pages else set()
                if unquote(parts.fragment) not in ids:
                    broken.append(f"{where}: no id '{parts.fragment}' in {dest.relative_to(site)}")

    print(f"{len(pages)} pages, {checked} internal links checked, {len(broken)} broken")
    for b in broken:
        print(f"BROKEN  {b}")
    print(f"{len(external)} external links (not fetched):")
    for e in sorted(external):
        print(f"  {e}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
