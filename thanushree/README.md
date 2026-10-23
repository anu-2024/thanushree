# Chapter 20 — A Little Universe Made Just For You

A dreamy, interactive birthday surprise built with **Streamlit**, Python, HTML and CSS. It is a digital scrapbook, a tiny film premiere, a Kannada birthday anthem, a 20-reason card deck, a memory timeline, a sibling letter, a wish wall and a full-screen finale — all in one deployable app.

The project is intentionally **content-driven**: almost every name, caption, date, lyric and message lives in `content.json` or `assets/lyrics.json`, not in the code.

---

## What is inside

| # | Section | What it does |
|---|---------|--------------|
| 1 | Secret welcome | Envelope illustration, "Open Your Surprise" button, CSS confetti and a cinematic hero reveal |
| 2 | Her photo universe | Spotlight photo + scrapbook gallery, automatic image optimisation, editable captions, graceful empty frames |
| 3 | Her birthday music video | Poster stage, play button, local MP4 playback, optional audio player, attractive fallback when the video is missing |
| 4 | The birthday anthem | Kannada lyrics + English transliteration tabs, highlighted chorus, gentle motion, editable lyrics file |
| 5 | 20 reasons we love you | Twenty tap-to-open cards, fully keyboard accessible |
| 6 | Memory lane | Alternating chronological timeline plus a "One more memory" card |
| 7 | A letter from your sibling | Sealed letter with a gentle open animation and editable paragraphs |
| 8 | Birthday wish wall | Static wishes from family and friends — no forms, database or tracking |
| 9 | Grand finale | Full-screen starry send-off with sunflowers, gold confetti and a replay button |

Everything is responsive and works on desktop and mobile. Animations automatically calm down when the visitor's device asks for **reduced motion**. There are no API keys, external services, databases or personal data collection.

---

## Project structure

```text
thanushree/
├── app.py                     # The whole experience (layout, styling, sections)
├── content.json               # Names, captions, timeline, letter, reasons, wishes...
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml            # Soft pink/lavender Streamlit theme
└── assets/
    ├── photos/                # Put her real photos here (the folder is kept by .gitkeep)
    │   └── .gitkeep
    ├── lyrics.json            # Kannada + transliteration lyrics (editable)
    ├── birthday_video.mp4     # ADD THIS: the birthday music video
    ├── video_poster.jpg       # OPTIONAL: cinematic poster image
    └── birthday_audio.mp3     # OPTIONAL: standalone audio track
```

You only need to add the media files. Missing photos, poster, video or audio are handled gracefully with designed placeholder/fallback cards — the app never crashes.

---

## Quick start (local)

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Personalisation checklist

Open `content.json` and replace every bracketed placeholder:

- `[SISTER'S NAME]` — the birthday girl's name
- `[NICKNAME]` — the name your family actually calls her
- `[YOUR NAME]` — the sibling signing the letter
- `[BIRTHDAY DATE]` — the date shown in the hero chip
- `[BIRTHDAY MESSAGE]` — one personal paragraph inside the letter
- `[YEAR]` and `[ADD YOUR FAVOURITE MEMORY HERE]` — timeline details
- `[SONG TITLE]`, `[ARTIST / MOVIE]` — in `assets/lyrics.json`

Then make it sound like your family:

1. **Birthday details** — `birthday` object: name, nickname, subtitle, welcome line, date, Libra note.
2. **Photos** — two supplied photos are already in `assets/photos/`; add or replace files there, then name them in `photos.captions`. Set `photos.spotlight` to the filename you want featured. Captions are optional; fallback captions are used for unnamed photos.
3. **Video** — place the edited video at `assets/birthday_video.mp4`. Optionally add `assets/video_poster.jpg` and `assets/birthday_audio.mp3`.
4. **Lyrics** — edit `assets/lyrics.json` (schema below). **Do not invent or reproduce lyrics you do not have permission to use.** Only add the selected lines you want to share.
5. **Reasons** — replace the 20 sample messages in `reasons` (funny, sweet, specific).
6. **Timeline** — edit `timeline` dates, titles and text; edit `one_more_memory`.
7. **Letter** — personalise `letter.salutation`, `paragraphs`, `signoff` and `signature`.
8. **Wishes** — edit `wishes` (static, no form, no database).
9. **Finale + footer** — adjust the closing lines and footer credit.

All section headings and subtitles can also be changed under `sections` in `content.json`.

### Photo naming tips

- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`.
- Use lowercase filenames without spaces if possible, e.g. `photo1.jpg`, `school-days.jpg`.
- Both portrait and landscape photos are supported. Landscape photos automatically get a wider scrapbook frame on desktop.
- Photos are automatically rotated correctly (EXIF), resized and converted to optimised WebP thumbnails in memory. Very large originals are fine locally, but keep repository images reasonable (roughly 2000 px on the long edge).
- The app displays **only supplied photographs** — it never generates fake images of her.

### Video notes

- Use an **H.264 MP4** for the broadest browser support (Chrome, Edge, Safari, mobile).
- Keep the file comfortably under 100 MB because GitHub rejects files above that limit. 20–40 MB is ideal for Streamlit Community Cloud.
- Do not upload a video you do not have rights to share.
- Playback always requires the visitor to click — sound never autoplays.

### Lyrics file schema

`assets/lyrics.json` looks like this:

```json
{
  "title": "Song title",
  "artist": "Artist / film",
  "kannada": [
    { "type": "verse",  "lines": ["Line one", "Line two"] },
    { "type": "chorus", "lines": ["Chorus line one", "Chorus line two"] }
  ],
  "transliteration": [
    { "type": "verse",  "lines": ["Line one in transliteration"] },
    { "type": "chorus", "lines": ["Chorus line in transliteration"] }
  ]
}
```

- Any stanza with `"type": "chorus"` gets the gold highlighted chorus treatment.
- Both arrays can contain as many stanzas as you need.
- If either array is empty, the tab shows a gentle "add your lyrics" note instead of breaking.
- Kannada text is rendered with **Noto Sans Kannada** (loaded from Google Fonts with system-font fallbacks).

---

## Testing locally

The project has no test framework, but these checks are enough before deploying:

```powershell
python -m py_compile app.py
streamlit run app.py
```

Then verify manually:

- The envelope welcome appears and "Open Your Surprise" reveals the hero with confetti.
- Navigation links jump to each section.
- Photos appear in the spotlight and scrapbook; hover/tap captions are readable on mobile.
- The video plays only after clicking the play button, or the fallback card appears when the file is missing.
- Both anthem tabs render Kannada and transliteration.
- All 20 reason cards open with mouse, touch and keyboard.
- The letter opens and folds back.
- The replay button at the very bottom returns to the envelope welcome screen.
- Test at a narrow mobile width (~375 px) and with reduced motion enabled.

Optional automated smoke test:

```powershell
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py'); at.run(timeout=30); print('EXCEPTIONS:', list(at.exception))"
```

To test the reveal flow in the same harness:

```powershell
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(); at.button[0].click().run(); print('EXCEPTIONS:', list(at.exception))"
```

---

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository and push this folder (including `assets/photos`, `assets/lyrics.json`, `content.json`, `requirements.txt`).
2. Go to <https://share.streamlit.io> and sign in with GitHub.
3. Choose **New app** → select the repository and branch.
4. Set **Main file path** to `app.py`.
5. In **Advanced settings**, choose Python 3.11 or 3.12 and click **Deploy**.
6. Wait for the build; every future push to the branch redeploys automatically.

GitHub/Streamlit tips:

- Keep individual files under 100 MB (GitHub hard limit). Compress the video if necessary.
- Avoid Git LFS unless you know the deployment path handles it; a compressed MP4 is simpler.
- The Google Fonts import is the only external request. If the venue has no internet, the app falls back to elegant system serif/sans fonts automatically.
- No secrets or environment variables are needed.

---

## Accessibility and privacy

- High-contrast body text on cream/glass surfaces; the finale uses cream text on deep plum.
- Semantic headings, alt text for photos, labelled sections and visible keyboard focus rings.
- Reason cards use native `<details>` / `<summary>`, so they work with keyboard and screen readers.
- `prefers-reduced-motion` turns continuous animation into a near-static experience.
- No analytics, no cookies, no forms, no database, no API keys. Wishes are static text in `content.json`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Photos do not appear | Check the files are inside `assets/photos/` with a supported extension. Refresh the browser tab. |
| Captions show the wrong text | Match the caption key in `content.json` exactly to the filename (case-sensitive). |
| Video area shows the fallback card | Confirm `assets/birthday_video.mp4` exists, is not empty, and is an H.264 MP4. |
| Video will not play on Safari/iOS | Re-export as H.264 + AAC MP4 (not HEVC/WebM). |
| Kannada looks like boxes | Enable a Kannada font on the device; the web font normally covers it. |
| Content changes do not show | Save `content.json` and refresh the browser. |
| App warns about Cloud file size | Compress the video/photo assets below GitHub's 100 MB file limit. |
| Replay button seems to do nothing | The replay button clears the saved section state and reruns the app back to the envelope. Make sure the page has finished rerunning. |

---

## A note on the placeholders

The repository currently includes two photos and a birthday video, while names, messages and lyrics remain editable placeholders. Replace every bracketed value before sharing the link, and swap the media files for the ones you want to keep. Missing photos, poster or audio still fall back to the designed "waiting for your memory" cards without crashing.

Happy Chapter 20. 🌻
