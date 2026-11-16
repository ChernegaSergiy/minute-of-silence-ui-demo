#!/usr/bin/env python3
"""Збирає самодостатню демо-сторінку з клону minute-of-silence.

Використання:
    python3 tools/build.py /шлях/до/minute-of-silence [-o index.html]

Що робить:
  1. копіює мок Tauri та конфіг Vite у клон застосунку;
  2. збирає справжній фронтенд (React + Fluent UI) через `vite build`;
  3. вбудовує JS, CSS, мок і PNG (як data: URI) в один index.html.
"""
import argparse, base64, glob, re, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = ("index.mock.html", "vite.mock.config.ts", "mock-tauri.js")
PNGS = {
    "/logo.png": "public/logo.png",
    "/img/candle_circle.png": "public/img/candle_circle.png",
    "/img/progress_ring.png": "public/img/progress_ring.png",
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("app", type=Path, help="шлях до клону minute-of-silence")
    ap.add_argument("-o", "--out", type=Path, default=ROOT.parent / "index.html")
    args = ap.parse_args()
    app = args.app.resolve()

    if not (app / "node_modules").exists():
        subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=app, check=True)
    for name in FILES:
        shutil.copy(ROOT / name, app / name)
    subprocess.run(["npx", "vite", "build", "-c", "vite.mock.config.ts"], cwd=app, check=True)

    dist = app / "dist-mock"
    html = (dist / "index.mock.html").read_text(encoding="utf-8")
    js = Path(glob.glob(str(dist / "assets/*.js"))[0]).read_text(encoding="utf-8")
    # </script усередині рядка закрив би тег; U+FFFD не приймає публікація артефактів
    js = js.replace("</script", "<\\/script").replace("\ufffd", "\\uFFFD")
    css = Path(glob.glob(str(dist / "assets/*.css"))[0]).read_text(encoding="utf-8")
    mock = (app / "mock-tauri.js").read_text(encoding="utf-8")

    html = re.sub(r"<script[^>]*mock-tauri\.js[^>]*></script>", "", html)
    html = re.sub(r'<script type="module"[^>]*></script>', "", html)
    html = re.sub(r'<link rel="stylesheet"[^>]*>', "", html)
    html = html.replace("</head>", f"<style>{css}</style><script>{mock}</script></head>")
    html = html.replace("</body>", f'<script type="module">{js}</script></body>')

    for url, rel in PNGS.items():
        uri = "data:image/png;base64," + base64.b64encode((app / rel).read_bytes()).decode()
        html = re.sub(r"([\"'`])" + re.escape(url) + r"\1", lambda m: m.group(1) + uri + m.group(1), html)

    args.out.write_text(html, encoding="utf-8")
    print(f"OK: {args.out} ({args.out.stat().st_size / 1e6:.2f} МБ)")


if __name__ == "__main__":
    main()
