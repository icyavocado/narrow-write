# Narrow Write — Product Specification

## 1. Overview

**Narrow Write** is a distraction-free writing tool that combats mind-wandering by limiting how many words are visible on screen at any one time. The less you see, the more you focus on what you're actually writing.

There is no formatting. No toolbar. No sidebar. Just words.

**Browser tab title:** `Narrow Write — write without looking back`

### Problem

When writing, having a full page of text visible creates cognitive noise — the eye wanders, the writer edits instead of drafts, momentum breaks. Narrow Write solves this by hiding or blurring everything except the most recent N words.

### Target Users

- Writers and authors working on long-form drafts
- Students writing essays or notes
- Anyone who types and gets distracted by their own output

---

## 2. Core Concept

The user types into a single full-screen writing area. Only the **last N words** they have typed are visible. Everything before that is either blurred or hidden entirely, depending on the chosen mode. The total text is preserved — just not shown.

---

## 3. Features

### 3.1 Writing Area

- Full-screen, full-width writing surface — text spans the full window width
- Single document — no tabs, no file list
- Plain text only — no bold, italic, headings, or any rich text formatting
- Blank on first visit — no placeholder, no welcome message; cursor is ready immediately
- Auto-saves to `localStorage` continuously as the user types
- Restores the last session on page load
- Writing mode only — there is no "read back" mode
- Optimised to handle very long documents (10,000+ words) without performance degradation

### 3.2 Visible Word Limit

- The user sets **N**, the number of words visible at any time (range: **1 – 100 words**)
- Default on first visit: **10 words**
- Only the last N words are shown; everything before them is affected by the chosen visibility mode
- When the user deletes words (backspace), the visible window **shifts back** — earlier text becomes visible again as it re-enters the last N words
- N is configurable via the settings panel

### 3.3 Visibility Modes

Two modes control what happens to words beyond the visible limit:

| Mode | Behavior |
|------|----------|
| **narrow-write** | Older words remain on screen but are heavily blurred — the color should remain visible (not fade to near-black), just unreadable |
| **Blank Past** | Older words disappear entirely; two typing styles available (see below) |

- Default mode: **narrow-write**
- The user selects their preferred mode from the settings panel

#### narrow-write mode — Enter key

Pressing Enter creates a new line as normal. Line breaks are counted as word boundaries.

#### Blank Past — Typing Styles

When **Blank Past** is active, a secondary toggle in the config panel lets the user choose how text behaves as words vanish:

| Style | Behavior |
|-------|----------|
| **Typewriter** | Cursor is locked to **dead center** of the screen; typed words shift left and disappear off the left edge. The word count limit still applies — words beyond N also vanish. Going off-screen naturally is acceptable. |
| **Classic** | Cursor moves normally left-to-right. Words disappear once the word count limit (N) is reached, matching the standard flow. |

- The style names **Typewriter** and **Classic** are shown explicitly in the config panel
- Default style: **Classic**

#### Blank Past — Typewriter Style — Cursor Position

In Typewriter style, the cursor is anchored at **dead center horizontally and vertically** on screen. As the user types, each new letter appears at the cursor (screen center) and the existing text shifts left — the cursor itself never moves. Words that go beyond the word count limit, or that drift off the left edge of the screen, disappear. The effect is that the user always types at the same fixed point while their writing streams away to the left.

#### Blank Past — Typewriter Style — Backspace behavior

In Typewriter style, **backspace does not delete**. Instead:

- Each backspace press adds a **strikethrough** to the most recent non-struck, non-whitespace character
- The cursor stays fixed at screen center — nothing is removed, nothing shifts
- Struck characters remain in the content — they are part of the document
- Struck characters are **preserved when copying** — the copy output uses the Unicode combining strikethrough character (`U+0336`) so the strikethrough is visible in any app that supports it
- Only non-whitespace characters can be struck — spaces and line breaks are skipped

#### Blank Past — Enter key

Pressing Enter is recorded in the full document text (line break preserved), but **nothing is shown on screen** — the frontend does not render the line break visually in Blank Past mode.

### 3.4 Settings Panel

Accessible via a **sliders icon in the top-right corner** of the screen, always visible. Clicking it opens a **floating popover** anchored below the icon. Clicking anywhere outside the popover closes it.

| Setting | Default | Description |
|---------|---------|-------------|
| **Visible word count (N)** | 10 | Number of words shown at once; range 1–100 |
| **Visibility mode** | narrow-write | Narrow Write or Blank Past |
| **Blank Past style** | Classic | Typewriter or Classic (only shown when Blank Past is active) |
| **Font family** | — | Curated list of 6–9 fonts (see §4 Visual Design) |
| **Font size** | 18px | Controls the size of the writing text |
| **Line spacing** | 1.8 | Controls leading for readability |
| **Theme** | Dark | Light or Dark |
| **Typing sounds** | Off | Toggle optional single-click sound per keypress |
| **Copy all** | — | Button — copies entire document text to clipboard |
| **Clear document** | — | Button — wipes the document after a confirm dialog |

Settings are persisted to `localStorage`.

### 3.5 Word Count Display

- Total word count is shown **always visible in the bottom-right corner** of the screen
- Rendered in a **low-contrast color** so it does not compete with the writing area
- Updates in real time as the user types

### 3.6 Clear Document

- Available as a button inside the settings panel
- Triggers a **confirm dialog** before wiping ("Are you sure? This cannot be undone.")
- On confirm: clears `localStorage` content and resets the writing area to blank

### 3.7 Copy All

- Available as a button inside the settings panel
- Copies the **full document text** (including hidden/blurred words and line breaks) to the system clipboard
- No partial copy UI — standard browser text selection + Ctrl+C still works for manual selection

---

## 4. User Experience

### Flow

1. User opens Narrow Write in a browser
2. Previous session text is restored (if any); blank canvas if first visit
3. User begins typing immediately — no onboarding, no sign-in, no placeholder
4. Older words beyond N fade out and are blurred (narrow-write mode) or hidden (Blank Past mode)
5. In Blank Past + Typewriter style, the cursor stays at dead center (horizontally and vertically); words flow left and vanish
6. Backspacing shifts the window back — previously hidden/blurred text becomes visible again
7. User clicks the sliders icon (top-right) to open the floating settings popover
8. After a Clear, the screen instantly returns to a blank writing area — ready to type
9. Total word count is quietly visible in the bottom-right corner at all times

### Design Principles

- **Nothing competes for attention** — the interface disappears; only the current words exist
- **No friction** — no accounts, no login, no setup, no placeholder copy
- **Forgiveness** — text is never lost; auto-save runs silently in the background
- **One thing at a time** — one document, one mode, one focus
- **Quiet feedback** — word count is present but visually subordinate

### Visual Design

| Property | Value |
|----------|-------|
| Default theme | Dark |
| Dark background | Off-black (~`#111` or `#1a1a1a`) |
| Light background | Warm off-white (~`#faf8f5`) |
| Writing area width | Full window width |
| Writing text alignment | Left-aligned |
| Writing area padding | Generous on all sides |
| Blur intensity | Heavy blur — text is unreadable but color remains visible (not dark/faded) |
| Word disappear animation | Fade out (CSS transition) |
| Mode switch animation | Smooth fade between modes |
| Cursor (caret) style | Slow pulsing |
| Word count position | Bottom-right corner |
| Word count format | Number only (e.g. `342`) |
| Word count opacity | Subtle but readable (~40–60% opacity) |
| Settings icon | Sliders icon, top-right, small and subtle |
| Settings panel style | Narrow floating popover (~260px), fades in, closes on outside click |
| Keyboard shortcuts | None |
| Browser tab title | `Narrow Write — write without looking back` |

### Font Library

A curated list of **6–9 fonts** covering a balanced mix of styles. Loaded via Google Fonts or system fonts where possible.

| Category | Examples |
|----------|---------|
| Serif | Merriweather, Lora, Playfair Display |
| Sans-serif | Inter, DM Sans |
| Monospace | JetBrains Mono |

Default font: **Merriweather** (serif).

### Typing Sounds

- Optional feature, **off by default**
- When enabled: a single mechanical click sound plays on every keypress
- Toggled from the settings panel
- Sound file should be lightweight (short WAV or MP3)

### Mobile

- Mobile is a **first-class target**, not an afterthought
- Layout is **slightly adapted** for small screens — adjusted margins and font size
- Settings icon remains in the **top-right corner** on mobile
- The floating settings popover adapts to fit smaller viewports
- **Typewriter style is fully supported on mobile** — cursor centered horizontally
- No separate mobile-only UI; responsive CSS handles the adaptation

---

## 5. Technical Specification

### Stack

| Layer | Choice |
|-------|--------|
| Language | Vanilla JavaScript (no framework) |
| Styling | Pico.css + minimal custom CSS |
| Fonts | Google Fonts (6–9 curated) |
| Storage | Browser `localStorage` |
| Backend | None — fully client-side |
| Build tool | None — single `index.html` file |

### Storage Schema (localStorage)

```json
{
  "narrowwrite_content": "<full plain text>",
  "narrowwrite_settings": {
    "visibleWords": 10,
    "mode": "narrow-write",
    "blankPastStyle": "classic",
    "fontFamily": "Merriweather",
    "fontSize": 18,
    "lineSpacing": 1.8,
    "theme": "dark",
    "typingSounds": false
  }
}
```

### Word Counting & Rendering

- Words are counted by splitting on whitespace
- On every keystroke, the full text is split into words
- Each word is wrapped in a `<span>` with a `data-state` attribute (`visible` or `hidden`)
- CSS targets `[data-state="hidden"]` to apply blur or display:none depending on mode
- Words beyond the visible limit **fade out** via CSS transition when they leave the window
- Backspace recalculates the word array — the visible window shifts back naturally
- Total word count (all words) is derived from the same split and displayed in the UI
- Rendering is optimised for long documents — only visible DOM nodes are actively styled; older content is inert

---

## 6. Implementation Guidelines

### File Structure

The entire app lives in a **single `index.html`** file — HTML, CSS (in a `<style>` tag), and JS (in a `<script>` tag). No build step, no bundler, no separate files.

### JavaScript Style

- **Plain functions only** — no classes, no modules, no frameworks
- **One state object** — a single `state` object holds all runtime app state
- **Verb-first naming** — `renderWords()`, `saveState()`, `applyTheme()`, `openSettings()`
- **Early returns** — functions exit as soon as their work is done; no wrapping everything in a top-level `if`
- **No defensive guard clauses** — trust the flow; don't add redundant checks that obscure intent
- Code should read top-to-bottom like a story — setup, then event wiring, then handlers

```js
// Good — early return, clear flow
function handleKeydown(e) {
  if (e.key === 'Escape') return closeSettings();
  renderWords();
  scheduleSave();
}

// Avoid — unnecessary nesting
function handleKeydown(e) {
  if (e.key !== 'Escape') {
    renderWords();
    scheduleSave();
  } else {
    closeSettings();
  }
}
```

### State Object

```js
const state = {
  content: '',
  settings: {
    visibleWords: 10,
    mode: 'narrow-write',       // 'narrow-write' | 'blankpast'
    blankPastStyle: 'classic', // 'classic' | 'typewriter'
    fontFamily: 'Merriweather',
    fontSize: 18,
    lineSpacing: 1.8,
    theme: 'dark',
    typingSounds: false,
  }
};
```

### Rendering Pipeline

On every keystroke:

1. `getContent()` — read raw text from the `contenteditable` div
2. `splitWords(content)` — split into word array
3. `renderWords(words, visibleWords)` — rebuild `<span>` elements with correct `data-state`
4. `updateWordCount(words.length)` — update the bottom-right counter
5. `scheduleSave()` — debounce a `localStorage` write (500ms)

### Typewriter Mode

- The `contenteditable` div is positioned with `transform: translateX(...)` calculated so the caret stays at the horizontal center
- Vertical center is achieved with `top: 50%; transform: translateY(-50%)`
- On each keystroke, the X offset is recalculated based on the width of the visible text

### localStorage Writes

- All writes are **debounced at 500ms** — typing quickly does not hammer storage
- `saveState()` writes both `narrow-write_content` and `narrow-write_settings`
- `loadState()` is called once on startup and populates `state`

### Typing Sounds

- A single `Audio` element is created at startup with the click sound preloaded
- On each keypress (when sounds are enabled): set `.currentTime = 0`, then call `.play()`
- No pooling needed — resetting `currentTime` is sufficient for fast typing

### CSS Conventions

- Pico.css provides the base reset and form element styles
- All custom properties live in `:root` as CSS variables — theme switching is a single class swap on `<body>`
- Theme CSS variables are written inline in a `<script>` block in `<head>` before the page renders — prevents flash of wrong theme on load
- `[data-state="hidden"]` drives blur and hide behaviour
- Transitions on `opacity` and `filter` handle the fade-out animation

### Icons

All icons are **inline SVG** — no icon library dependency, no CDN request.

### Settings Popover — Layout & Controls

| Setting | Control type |
|---------|-------------|
| Visible word count (N) | Range slider + number display |
| Visibility mode | Dropdown select |
| Blank Past style | Dropdown select (hidden when mode is narrow-write) |
| Font family | Dropdown select |
| Font size | Range slider + number display |
| Line spacing | Range slider + number display |
| Theme | Toggle (Light / Dark) |
| Typing sounds | Toggle (On / Off) |
| Copy all | Button |
| Clear document | Button → inline confirm replaces button text |

Settings appear in this order: **Word count → Mode → Blank Past style → Font → Size → Spacing → Theme → Sounds → Copy → Clear**

### Clear Confirm Flow

When the user clicks Clear, the button transforms inline (within the popover) into a confirm prompt — no modal, no browser dialog. On confirm, content is wiped and the writing area resets to blank instantly.

### Startup Sequence

1. Read theme from `localStorage` and apply it to `<body>` immediately (before render — no flash)
2. Load full `state` from `localStorage`
3. Render the writing area with restored content
4. Auto-focus the writing area — user can type immediately
5. Wire all event listeners

---

## 6. Non-Goals (V1)

The following are explicitly out of scope for the first version:

- User accounts or authentication
- Cloud storage or sync
- Multiple documents
- Rich text formatting (bold, italic, headings, etc.)
- Read/review mode
- Collaboration or sharing
- Offline PWA support
- Export to any format
- Keyboard shortcuts
