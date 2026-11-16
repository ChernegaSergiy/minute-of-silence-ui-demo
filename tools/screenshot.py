#!/usr/bin/env python3
"""Takes screenshots of the demo page (requires `pip install playwright` + `playwright install chromium`).

    python3 tools/screenshot.py [index.html] [output_dir]

Shots: TEST / STOP in light and dark themes, and the overlay with the ring (~18 s after start).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
page_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "index.html"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "screenshots"
out.mkdir(parents=True, exist_ok=True)
url = page_path.resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()

    def new_page(scheme: str):
        # uk-UA is required so the labels are in Ukrainian (ТЕСТ / СТОП)
        ctx = browser.new_context(viewport={"width": 900, "height": 720}, color_scheme=scheme, locale="uk-UA")
        pg = ctx.new_page()
        pg.goto(url)
        pg.get_by_role("button", name="ТЕСТ").wait_for()
        pg.wait_for_timeout(400)
        return pg

    for scheme in ("light", "dark"):
        pg = new_page(scheme)
        pg.screenshot(path=out / f"test-{scheme}.png")
        pg.get_by_role("button", name="ТЕСТ").click()
        pg.get_by_role("button", name="СТОП").wait_for()
        pg.mouse.move(0, 0)
        pg.wait_for_timeout(300)
        pg.screenshot(path=out / f"stop-{scheme}.png")

    pg = new_page("light")
    pg.locator("#overlayToggle").check()  # the overlay is off by default in the mock
    pg.get_by_role("button", name="ТЕСТ").click()
    pg.wait_for_timeout(18000)
    pg.screenshot(path=out / "overlay.png")
    browser.close()
print("OK:", out)
