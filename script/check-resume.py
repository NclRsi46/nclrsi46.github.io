#!/usr/bin/env python3
"""Diff the resume PDF's facts against the built Experience page. Stdlib + pdftotext.

1. Every fact unit on _site/resume.html (bullet, heading, org line, date cell,
   skill group and list) must appear in the PDF text.
2. Every bullet in the PDF must appear on the page.
3. Every number on every page must appear in the PDF or in one of the --source
   files (the phishing README, for the case study).

Both sides are normalized first: curly quotes, en dashes, commas, and whitespace.
Usage: script/check-resume.py [--source path ...]
"""
import argparse
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ").replace(",", "")
    return re.sub(r"\s+", " ", s).strip()


class Units(HTMLParser):
    """Text of fact-bearing elements inside <main>, plus all of <main>'s text."""
    UNIT = {"li", "h3", "dt", "dd"}
    UNIT_CLASSES = {"code", "org"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = 0
        self.stack = []  # (tag, is_unit, buffer)
        self.units, self.text = [], []
        self.in_label = 0  # depth inside .lbl (section numbers, eyebrows): structure, not facts

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main += 1
        if not self.in_main or tag in ("br", "img", "meta", "link"):
            return
        cls = set((dict(attrs).get("class") or "").split())
        if "lbl" in cls:
            self.in_label += 1
        unit = tag in self.UNIT or (tag == "p" and cls & self.UNIT_CLASSES)
        self.stack.append((tag, bool(unit), [], "lbl" in cls))

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main -= 1
        if not self.stack or self.stack[-1][0] != tag:
            return
        _, unit, buf, label = self.stack.pop()
        if label:
            self.in_label -= 1
        if unit:
            self.units.append("".join(buf))
        for _, _, outer, _ in self.stack:
            outer.extend(buf)

    def handle_data(self, data):
        if self.in_main and not self.in_label:
            self.text.append(data)
            if self.stack:
                self.stack[-1][2].append(data)


def pdf_text(pdf):
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    return out


def pdf_bullets(raw):
    bullets, cur = [], None
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("•"):
            if cur:
                bullets.append(cur)
            cur = s.lstrip("•").strip()
        elif cur is not None and s and line.startswith(" " * 6):
            cur += " " + s  # wrapped continuation of the bullet
        else:
            if cur:
                bullets.append(cur)
            cur = None
    if cur:
        bullets.append(cur)
    return bullets


URLISH = re.compile(r"\S+\.[a-z]{2,}/\S*")
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?%?")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=str(ROOT / "Nicolas_Rossi_Resume.pdf"))
    ap.add_argument("--site", default=str(ROOT / "_site"))
    ap.add_argument("--source", action="append", default=[], help="extra text source for numbers")
    args = ap.parse_args()

    raw = pdf_text(args.pdf)
    pdf = norm(raw)
    failures = 0

    page = Units()
    page.feed(Path(args.site, "resume.html").read_text(encoding="utf-8"))
    page_text = norm(" ".join(page.text))
    units = [norm(u) for u in page.units if norm(u)]
    missing = [u for u in units if u not in pdf]
    print(f"[1] Experience -> PDF: {len(units)} units, {len(missing)} not in the PDF")
    for u in missing:
        print(f"    NOT IN PDF: {u}")
    failures += len(missing)

    bullets = [norm(b) for b in pdf_bullets(raw)]
    absent = [b for b in bullets if b not in page_text]
    print(f"[2] PDF -> Experience: {len(bullets)} bullets, {len(absent)} not on the page")
    for b in absent:
        print(f"    NOT ON PAGE: {b}")
    failures += len(absent)

    sources = pdf + " " + " ".join(norm(Path(s).read_text(encoding="utf-8")) for s in args.source)
    source_nums = set(NUM.findall(sources))
    bad = []
    total = 0
    for f in sorted(Path(args.site).rglob("*.html")):
        u = Units()
        u.feed(f.read_text(encoding="utf-8"))
        for n in sorted(set(NUM.findall(URLISH.sub(" ", norm(" ".join(u.text)))))):
            total += 1
            if n not in source_nums:
                bad.append(f"{f.relative_to(args.site)}: {n}")
    print(f"[3] Numbers on all pages: {total} distinct per page, {len(bad)} with no source")
    for b in bad:
        print(f"    NO SOURCE: {b}")
    failures += len(bad)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
