# Narrow Write

A distraction-free writing tool that limits how many words are visible on screen at any time. The less you see, the more you focus on what you're actually writing.

**[Try it →](https://icyavocado.github.io/narrow-write)**

---

## What it does

When you write with a full page of text visible, your eye wanders. You start editing instead of drafting. Momentum breaks.

Narrow Write fixes this by showing only the last **N words** you've typed. Everything before that is either blurred or gone. Your words exist — you just can't see them.

---

## Modes

### Haze
Past words stay on screen but are blurred beyond reading. You can sense them; you can't dwell on them.

### Blank Past
Past words vanish entirely. Two styles:

- **Classic** — cursor moves left-to-right normally; words disappear as they exit the visible window
- **Typewriter** — cursor is locked at the horizontal center of the screen; text streams left and disappears

---

## Settings

Open with the sliders icon (top-right). All settings are saved automatically.

| Setting | Default | Range |
|---------|---------|-------|
| Visible words | 10 | 1 – 100 |
| Mode | Haze | Haze / Blank Past |
| Blank Past style | Classic | Classic / Typewriter |
| Font | Merriweather | 6 curated + any custom font |
| Font size | 18px | any |
| Line spacing | 1.8 | any |
| Theme | Dark | Dark / Light / System / HC Light / HC Dark |

---

## Themes

- **Dark** — off-black background, warm off-white text (default)
- **Light** — warm off-white background, dark text
- **System** — follows OS preference
- **HC Light / HC Dark** — pure black-on-white or white-on-black; blur replaced with full hide; no transitions

The `↻` button in the top-left corner cycles through themes instantly, even when the settings panel is closed.

---

## Your text is safe

- Everything is saved to your browser's `localStorage` as you type
- Nothing is sent anywhere — no server, no account, no tracking
- Clearing the document requires a confirmation step

---

## Technical notes

- Single `index.html` file — no build step, no dependencies beyond Google Fonts and Pico.css
- Vanilla JS, no framework
- Spellcheck disabled
- Input handling uses the `InputEvent` API (`e.inputType` / `e.data`) to avoid a Firefox/Safari duplicate-character bug caused by reading `contenteditable` DOM inside an input handler

---

## Local development

```sh
git clone https://github.com/icyavocado/narrow-write.git
cd narrow-write
open index.html   # or just drag it into a browser
```

No install step. No build. Edit `index.html` and refresh.

Deployed automatically to GitHub Pages on every push to `main` via `.github/workflows/deploy.yml`.
