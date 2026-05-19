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
- Auto-saves to `localStorage` continuously as the user types (debounced 500ms)
- Restores the last session on page load
- Writing mode only — there is no "read back" mode
- Spellcheck disabled (`spellcheck="false"`)
- Optimised to handle very long documents (10,000+ words) without performance degradation

### 3.2 Visible Word Limit

- The user sets **N**, the number of words visible at any time (range: **1 – 100 words**)
- Default on first visit: **10 words**
- Only the last N words are shown; everything before them is affected by the chosen visibility mode
- When the user deletes words (backspace), the visible window **shifts back** — earlier text becomes visible again as it re-enters the last N words
- N is configurable via the settings panel (direct number input)

### 3.3 Visibility Modes

Two modes control what happens to words beyond the visible limit:

| Mode | UI Label | Behavior |
|------|----------|----------|
| `narrowwrite` | **Haze** | Older words remain on screen but are heavily blurred — unreadable, but color remains visible |
| `blankpast` | **Blank Past** | Older words disappear entirely; two typing styles available (see below) |

- Default mode: **Haze**
- The user selects their preferred mode via a two-button toggle in the settings panel

#### Haze mode — Enter key

Pressing Enter creates a new line as normal. Line breaks are treated as word boundaries.

#### Haze mode — Performance

All hidden tokens are wrapped in a single `<span id="haze-group">` element. The CSS `filter: blur()` is applied to the group, not to individual spans — a single GPU composite operation regardless of how many hidden words exist.

#### Blank Past — Typing Styles

When **Blank Past** is active, a secondary toggle in the settings panel lets the user choose how text behaves as words vanish:

| Style | Behavior |
|-------|----------|
| **Classic** | Cursor moves normally left-to-right. Words disappear once the word count limit (N) is reached. |
| **Typewriter** | Cursor is locked to the horizontal and vertical center of the left half of the screen. Typed words shift left and disappear off the left edge. The word count limit still applies. |

- Default style: **Classic**

#### Blank Past — Typewriter Style — Cursor Position

In Typewriter style:
- The writing container occupies the **left half of the screen** (`right: 50%`)
- Text is **right-aligned** inside that container, so new characters always appear at the right edge — which is the horizontal center of the full screen
- The container is **vertically centered** (`align-items: center`)
- The effect: the cursor never moves; the existing text streams to the left
- `overflow: hidden` and `min-width: 0` on the editor prevent the container from expanding when text is wide, keeping the cursor position stable

#### Blank Past — Typewriter Style — Backspace

Backspace **deletes normally** — it removes the last character from the document. There is no strikethrough behavior.

#### Blank Past — Enter key

Pressing Enter is recorded in the full document text (line break preserved), but **nothing is shown on screen** — the frontend does not render the line break visually in Blank Past mode.

### 3.4 Settings Panel

Accessible via a **sliders icon in the top-right corner** of the screen. Clicking it opens a **floating popover** anchored below the icon. Clicking anywhere outside the popover closes it.

| Setting | Control | Default | Description |
|---------|---------|---------|-------------|
| **Mode** | Two-button toggle | Haze | Haze or Blank Past |
| **Blank Past style** | Two-button toggle | Classic | Classic or Typewriter (only shown when Blank Past is active) |
| **Visible words (N)** | Direct number input | 10 | Number of words shown at once; range 1–100 |
| **Font family** | Dropdown select + custom toggle | Merriweather | Curated list of 6 fonts; pencil icon switches to free-text input for any font name |
| **Font size** | Direct number input | 18 | Size of the writing text in px |
| **Line spacing** | Direct number input | 1.8 | Leading multiplier |
| **Theme** | Dropdown select + cycle button | Dark | System / Dark / Light / HC Light / HC Dark |
| **Copy all** | Button | — | Copies entire document to clipboard |
| **Clear document** | Button → inline confirm | — | Wipes the document after a confirm step |

Settings are persisted to `localStorage`.

Settings order: **Mode → Blank Past style → Visible words → Font → Font size → Line spacing → Theme → Copy → Clear**

### 3.5 Theme System

Five themes are available:

| Theme | Background | Text | Notes |
|-------|-----------|------|-------|
| **Dark** | `#1a1a1a` | `#e8e4dc` | Default |
| **Light** | `#faf8f5` | `#1a1a1a` | Warm off-white |
| **System** | Follows OS preference | — | `prefers-color-scheme` |
| **HC Light** | `#ffffff` | `#000000` | High contrast; blur replaced with full hide; no transitions |
| **HC Dark** | `#000000` | `#ffffff` | High contrast; blur replaced with full hide; no transitions |

A **theme cycle button** (`↻`) is always visible at the **top-left** of the canvas — outside the settings panel — for quick switching even when the settings icon is not visible. The cycle order is: System → Dark → Light → HC Light → HC Dark.

A second cycle button also exists inside the settings panel, next to the theme dropdown.

In HC themes, the haze blur is replaced with `opacity: 0` (complete hide) to avoid blur artifacts on high-contrast displays.

### 3.6 Custom Font

The **Font** setting row has a pencil icon button. Clicking it switches from the curated dropdown to a free-text input where the user can type any font name (e.g. `Georgia`, `Courier New`). Clicking the pencil again returns to the dropdown. The custom font name is persisted as `customFont` in settings.

### 3.7 Word Count Display

- Total word count is shown **always visible in the bottom-right corner** of the screen
- Rendered in a **low-contrast color** (`--muted`) so it does not compete with the writing area
- Updates in real time as the user types

### 3.8 Clear Document

- Available as a button inside the settings panel
- Triggers an **inline confirm step** — the button is replaced by a confirmation prompt directly in the panel
- On confirm: clears `localStorage` content and resets the writing area to blank; closes settings

### 3.9 Copy All

- Available as a button inside the settings panel
- Copies the **full document text** (including hidden/blurred words and line breaks) to the system clipboard
- Button label briefly changes to "Copied!" for 1.5 seconds as confirmation

---

## 4. User Experience

### Flow

1. User opens Narrow Write in a browser
2. Previous session text is restored (if any); blank canvas if first visit
3. User begins typing immediately — no onboarding, no sign-in, no placeholder
4. Older words beyond N are blurred (Haze) or hidden (Blank Past)
5. In Blank Past + Typewriter style, the cursor stays at screen center; words flow left and vanish
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
| Dark background | `#1a1a1a` |
| Light background | `#faf8f5` (warm off-white) |
| Writing area width | Full window width |
| Writing text alignment | Left-aligned (right-aligned in Typewriter) |
| Writing area padding | `3rem` all sides (mobile: `2rem 1.25rem`) |
| Haze blur amount | `14px` |
| Haze opacity | `0.75` |
| Word disappear animation | CSS transition (`opacity`, `filter`) — 180ms ease |
| Cursor (caret) style | Slow pulsing |
| Word count position | Bottom-right corner |
| Word count format | Number only (e.g. `342`) |
| Settings icon | Sliders icon, top-right, subtle |
| Theme cycle button | Top-left, subtle (cycle-arrows icon) |
| Settings panel style | Narrow floating popover (~260px), fades in, closes on outside click |
| Spellcheck | Disabled |

### Font Library

| Category | Fonts |
|----------|-------|
| Serif | Merriweather, Lora, Playfair Display |
| Sans-serif | Inter, DM Sans |
| Monospace | JetBrains Mono |
| Custom | Any font name the user types (loaded from system or Google Fonts if available) |

Default font: **Merriweather**.

### Mobile

- Mobile is a **first-class target**
- Layout adapted for small screens via responsive CSS — adjusted padding and font size
- Settings icon remains in the top-right corner on mobile
- Typewriter style fully supported on mobile

---

## 5. Technical Specification

### Stack

| Layer | Choice |
|-------|--------|
| Language | Vanilla JavaScript (no framework) |
| Styling | Pico.css (classless) + minimal custom CSS |
| Fonts | Google Fonts (6 curated) |
| Icons | Inline SVG — no icon library |
| Storage | Browser `localStorage` |
| Backend | None — fully client-side |
| Build tool | None — single `index.html` file |
| Deployment | GitHub Pages via GitHub Actions |

### Storage Schema (localStorage)

```json
{
  "narrowwrite_content": "<full plain text>",
  "narrowwrite_settings": {
    "visibleWords": 10,
    "mode": "narrowwrite",
    "blankPastStyle": "classic",
    "fontFamily": "Merriweather",
    "customFont": "",
    "fontSize": 18,
    "lineSpacing": 1.8,
    "theme": "dark"
  }
}
```

### Word Tokenisation & Rendering

- Content is split into alternating `[word, whitespace, word, …]` tokens via `text.split(/(\s+)/)`
- Each token is wrapped in a `<span class="word" data-state="visible|hidden">`
- CSS targets `[data-state="hidden"]` to apply blur or `display: none` depending on mode
- In Haze mode, all hidden spans are grouped inside `<span id="haze-group">` — a single `filter: blur()` is applied to the group (one GPU operation)
- `trimOverflow()` hides spans from the top until content fits the viewport — batch reads then batch writes to avoid layout thrashing
- Total word count is derived from the same token pass

### Incremental Render Fast Path

On each keystroke, if:
- token count is unchanged (user typed within the current word)
- `visibleFrom` index is unchanged (window didn't shift)
- the current word span reference is valid

…only `_currentWordSpan.textContent` is updated — no DOM rebuild. This fires on the vast majority of keystrokes.

The cache is invalidated (`invalidateRenderCache()`) on mode or style change, and after any full re-render.

### Input Handling (Firefox/Safari compatibility)

`handleInput` uses the `InputEvent` API (`e.inputType`, `e.data`) to update `state.content` **without reading `editor.textContent`**. Reading the DOM inside an input handler caused Firefox and Safari to re-apply queued events on the rebuilt DOM, producing exponential character duplication.

| `inputType` | Action |
|-------------|--------|
| `insertText` | `state.content += e.data` |
| `insertParagraph` / `insertLineBreak` | `state.content += '\n'` |
| `deleteContentBackward` | `state.content = state.content.slice(0, -1)` |
| `deleteWordBackward` | strip last word + trailing whitespace via regex |
| `deleteSoftLineBackward` / `deleteHardLineBackward` | truncate at last `\n` |
| `insertCompositionText` | skip (IME mid-composition) |
| default | DOM fallback — `editor.textContent` (undo, redo, drag, IME commit) |

### Typewriter Layout

- `#editor-container` is positioned `left: 0; right: 50%` — occupies the left half of the screen
- `text-align: right` on `#editor` keeps the cursor at the container's right edge (= screen center)
- `min-width: 0` on `#editor` prevents the flex child from expanding beyond the container when text is wide (default `min-width: auto` + `white-space: nowrap` would allow this, causing the cursor to jump when long words disappear)
- `overflow: hidden` on `#editor` clips text scrolling off the left edge

### Cursor Placement

`placeCursorAtEnd()` collapses a Range into `editor.lastElementChild` (the last visible span), not after it. Collapsing after the span would cause Firefox/Safari to insert the next character as a stray text node directly in `#editor`, creating duplicate characters.

### Startup Sequence

1. Inline `<script>` in `<head>` reads theme from `localStorage` and sets `data-theme` on `<html>` before render — prevents flash of wrong theme
2. `loadState()` populates `state` from `localStorage`
3. `renderWords()` paints the restored content
4. `editor.focus()` — user can type immediately
5. Event listeners are wired

### localStorage Writes

- All writes debounced at 500ms — fast typing does not hammer storage
- `saveState()` writes both `narrowwrite_content` and `narrowwrite_settings`

### Render Buffer

A maximum of **800 tokens before the visible window** are rendered to the DOM. This caps DOM size for very long documents while keeping enough context for smooth backspace behavior.

---

## 6. Implementation Guidelines

### File Structure

The entire app lives in a **single `index.html`** file — HTML, CSS (in a `<style>` tag), and JS (in a `<script>` tag). No build step, no bundler, no separate files.

### JavaScript Style

- **Plain functions only** — no classes, no modules, no frameworks
- **One state object** — a single `state` object holds all runtime app state
- **Verb-first naming** — `renderWords()`, `saveState()`, `applyTheme()`, `openSettings()`
- **Early returns** — functions exit as soon as their work is done
- Code reads top-to-bottom: setup → event wiring → handlers

### State Object

```js
const state = {
  content: '',
  settings: {
    visibleWords: 10,
    mode: 'narrowwrite',       // 'narrowwrite' | 'blankpast'
    blankPastStyle: 'classic', // 'classic' | 'typewriter'
    fontFamily: 'Merriweather',
    customFont: '',
    fontSize: 18,
    lineSpacing: 1.8,
    theme: 'dark',             // 'dark' | 'light' | 'system' | 'hc-light' | 'hc-dark'
  }
};
```

### CSS Conventions

- All custom properties in `:root` as CSS variables — theme switching is a `data-theme` attribute on `<html>`
- Theme applied before render (flash prevention)
- `[data-state="hidden"]` drives blur and hide behavior
- Transitions on `opacity` and `filter` handle the fade-out animation
- HC themes override `--fade: 0ms` to suppress all transitions

---

## 7. Non-Goals (V1)

- User accounts or authentication
- Cloud storage or sync
- Multiple documents
- Rich text formatting
- Read/review mode
- Collaboration or sharing
- Offline PWA support
- Export to any format
- Keyboard shortcuts
- Typing sounds
