# Did You Know — channel design spec (frame.md)

Shared by every `videos/dyk-*` template. Copy changes here, then into each project's `frame.md`.

## Concept
"Case file." Every episode is an investigation: a question is opened, evidence (clues) is stamped in,
the case is closed with the answer. Dark, cinematic, quiet tension — never cartoonish, never neon.

## Palette (CSS custom properties, no inline hex elsewhere)
| Token      | Hex       | Use                                   |
| ---------- | --------- | ------------------------------------- |
| `--ink`    | `#06080d` | background base                       |
| `--deep`   | `#0d1422` | background gradient centre, panels    |
| `--fog`    | `#1b2638` | hairlines, grid, subtle shapes        |
| `--paper`  | `#ece6d8` | primary text (warm off-white)         |
| `--muted`  | `#7d8799` | secondary text, labels                |
| `--amber`  | `#f2b33d` | glow, the "?", emphasis, answer       |
| `--red`    | `#d6453d` | stamps ("CLUE", "CASE CLOSED")        |

## Type
- Display: **League Gothic** 400, uppercase, tight leading (0.95), letter-spacing 0.01em. Questions, clues, answers.
- Labels: **IBM Plex Mono** 400/700, uppercase, letter-spacing 0.18em. Kickers, counters, stamps.
- Both are HyperFrames-bundled (offline, deterministic). No other families.
- Sizes at 1920×1080: display 96–150px (auto-fit to text length), labels 26–34px. Title-safe padding ≥ 120px.

## Texture (every template)
Radial `--deep` → `--ink` background, slow-drifting vignette, light film grain, faint `--fog` grid lines.
Amber glow = `text-shadow`/`filter: drop-shadow` in `--amber` at low alpha, pulsing — not a blur bloom.

## Motion
- Mood: slow build, sharp hits. Eases: `power2.out` / `expo.out` for entrances, `back.out(1.6)` only for stamps.
- Camera: one slow push-in (scale 1.00 → 1.06) over the whole piece.
- Hits land on a single beat with a short (≤ 3 frame) deterministic shake; no random values.
- Every template ends on a ≥ 1s readable hold, so editors can trim to the voiceover.

## Variables
Per-episode text is a composition variable (`data-composition-variables`); text auto-fits by length at init.
Render with: `npx hyperframes render --variables-file episode.json`.
