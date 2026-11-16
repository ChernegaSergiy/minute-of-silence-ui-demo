# minute-of-silence-ui-demo

Інтерактивна демо-сторінка налаштувань застосунку
[«Хвилина мовчання»](https://github.com/ChernegaSergiy/minute-of-silence)
(гілка `feature/test-ceremony-stop`) із кнопкою «ТЕСТ» / «СТОП».

Це **справжній фронтенд** застосунку (React 19 + Fluent UI), зібраний у браузері.
Бекенд Tauri замінено моком, тому нічого не грає й нічого не зберігається.

## Перегляд

Відкрийте `index.html` у Chrome/Edge або ввімкніть GitHub Pages (Settings → Pages → `main` / root).

- Кнопка «ТЕСТ» запускає імітацію тестової церемонії (60 с) і перемикається на «СТОП».
- Візуальний оверлей за замовчуванням вимкнено. Щоб побачити свічку з кільцем, увімкніть
  перемикач оверлея в налаштуваннях і натисніть «ТЕСТ».
- Кільце в оверлеї — APNG, який застосунок розкладає на кадри Rust-командою
  `decode_apng_frames`. У моку її замінено на `ImageDecoder`, тому потрібен Chromium-браузер.

## Структура

| Шлях | Призначення |
| --- | --- |
| `index.html` | зібрана самодостатня сторінка (JS, CSS, мок і PNG вбудовані) |
| `tools/mock-tauri.js` | мок `window.__TAURI_INTERNALS__` (команди, події, `decode_apng_frames`) |
| `tools/index.mock.html`, `tools/vite.mock.config.ts` | вхід і конфіг Vite для демо-збірки |
| `tools/build.py` | збирає `index.html` із клону застосунку |
| `tools/screenshot.py` | робить скриншоти через Playwright |
| `patch/test-button-pending-state.patch` | зміни до `App.tsx` і локалей, показані на демо |
| `screenshots/` | готові знімки (світла/темна тема, ТЕСТ/СТОП, оверлей) |

## Як перебудувати

```bash
git clone --branch feature/test-ceremony-stop https://github.com/ChernegaSergiy/minute-of-silence.git
cd minute-of-silence && git apply ../minute-of-silence-ui-demo/patch/test-button-pending-state.patch && cd ..
python3 minute-of-silence-ui-demo/tools/build.py minute-of-silence      # потрібні Node 20+ і npm
pip install playwright && playwright install chromium
python3 minute-of-silence-ui-demo/tools/screenshot.py                   # необов'язково
```

Без застосування патча збереться стан гілки як є.

## Про патч

Патч **не входить** до гілки застосунку. Він додає:

- `testPending`: захист від повторного кліку, поки тест ще не стартував
  (`trigger_ceremony_now` завершується лише після церемонії, тож `await` на нього не можна);
- `bundleIcon` для іконок Play/Stop та `Tooltip` з новими ключами `buttons.test_hint` і
  `buttons.stop_hint` у `uk.json` та `en.json`.

## Обмеження

Це не знімок реального вікна Tauri: шрифти (Segoe UI Variable), рамка вікна й поведінка
системи можуть відрізнятися. Ліцензія застосунку: див. основний репозиторій.
