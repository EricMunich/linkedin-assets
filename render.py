#!/usr/bin/env python3
"""Rendert LinkedIn-Post-Bilder aus HTML-Vorlagen.

Konvention je Post-Ordner posts/<slug>/:
  image.html     -> <slug>.png            (Einzelbild, 1080x1350 @2x = 2160x2700)
  carousel.html  -> <slug>.pdf            (Karussell, print_background=True)
                    <slug>-cover.png      (erste Seite als Vorschaubild)
Es wird nur gerendert, wenn die Ausgabe fehlt oder aelter als die Vorlage ist.
"""
import os, subprocess, sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
POSTS = ROOT / "posts"

def git_ts(path):
    try:
        out = subprocess.check_output(["git", "log", "-1", "--format=%ct", "--", str(path)], cwd=ROOT, text=True).strip()
        return int(out) if out else 0
    except Exception:
        return 0

def needs(src, out):
    if not out.exists():
        return True
    return git_ts(src) > git_ts(out)

def main():
    force = "--force" in sys.argv
    jobs = []
    for d in sorted(POSTS.iterdir()) if POSTS.exists() else []:
        if not d.is_dir():
            continue
        slug = d.name
        img = d / "image.html"
        car = d / "carousel.html"
        if img.exists() and (force or needs(img, d / f"{slug}.png")):
            jobs.append(("png", img, d / f"{slug}.png"))
        if car.exists() and (force or needs(car, d / f"{slug}.pdf")):
            jobs.append(("pdf", car, d / f"{slug}.pdf"))
    if not jobs:
        print("Nichts zu rendern.")
        return
    with sync_playwright() as p:
        b = p.chromium.launch()
        for kind, src, out in jobs:
            pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
            pg.goto(src.resolve().as_uri())
            pg.wait_for_timeout(600)
            if kind == "png":
                pg.screenshot(path=str(out), full_page=False)
                print("PNG", out.relative_to(ROOT), out.stat().st_size, "Bytes")
            else:
                pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
                print("PDF", out.relative_to(ROOT), out.stat().st_size, "Bytes")
                cover = out.with_name(out.stem + "-cover.png")
                pg.screenshot(path=str(cover), full_page=False)
                print("PNG", cover.relative_to(ROOT), cover.stat().st_size, "Bytes")
            pg.close()
        b.close()

if __name__ == "__main__":
    main()
