# minute-of-silence-ui-demo

An interactive demo of the settings screen of
[Minute of Silence](https://github.com/ChernegaSergiy/minute-of-silence)
(branch `feature/test-ceremony-stop`) with the TEST / STOP button.

This is the app's **real frontend** (React 19 + Fluent UI) built to run in a browser.
The Tauri backend is replaced with a mock, so nothing plays and nothing is saved.

## Viewing

Open `index.html` in Chrome or Edge, or enable GitHub Pages (Settings → Pages → `main` / root).

- The TEST button starts a simulated test ceremony (60 s) and switches to STOP.
- The visual overlay is off by default. To see the candle with the progress ring, turn on
  the overlay switch in the settings and press TEST.
- The ring in the overlay is an APNG that the app splits into frames with the Rust command
  `decode_apng_frames`. The mock replaces it with `ImageDecoder`, so a Chromium-based
  browser is required.
- The UI is in Ukrainian, so the buttons read «ТЕСТ» / «СТОП». The app picks the language
  from the browser locale.

## Structure

| Path | Purpose |
| --- | --- |
| `index.html` | the built self-contained page (JS, CSS, mock and PNGs inlined) |
| `tools/mock-tauri.js` | mock of `window.__TAURI_INTERNALS__` (commands, events, `decode_apng_frames`) |
| `tools/index.mock.html`, `tools/vite.mock.config.ts` | entry point and Vite config for the demo build |
| `tools/build.py` | builds `index.html` from a clone of the app |
| `tools/screenshot.py` | takes screenshots with Playwright |
| `screenshots/` | ready-made screenshots (light/dark theme, TEST/STOP, overlay) |

## Rebuilding

```bash
git clone --branch feature/test-ceremony-stop https://github.com/ChernegaSergiy/minute-of-silence.git
python3 minute-of-silence-ui-demo/tools/build.py minute-of-silence      # needs Node 20+ and npm
pip install playwright && playwright install chromium
python3 minute-of-silence-ui-demo/tools/screenshot.py                   # optional
```

## Limitations

This is not a screenshot of the real Tauri window: fonts (Segoe UI Variable), the window frame
and system behavior may differ. For the app's license, see the main repository.
