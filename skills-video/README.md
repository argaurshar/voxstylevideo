# 15 Free Claude Skills — 9:16 animated sheet

A vertical (1080×1920) 30-second animated version of the "15 Free Claude Skills"
spec sheet. The original 4:5 still is re-laid out for 9:16 and every element is
animated: the title pops in, the counter spins up to 15, and all fifteen skill
names are revealed one at a time.

| | |
|---|---|
| Output | `../out/15-free-claude-skills-9x16.mp4` |
| Format | 1080×1920, 30 fps, 30.0 s, H.264 (yuv420p), silent |
| Built from | `index.html` (design + timeline) rendered by `render.mjs` |

## How it works

The design is plain HTML/CSS. Nothing animates on its own — the page exposes a
single function:

```js
window.renderFrame(t)   // t in seconds, 0 .. 30
```

`render.mjs` opens the page in headless Chromium, calls `renderFrame(t)` for
every frame, screenshots it and pipes the PNG straight into ffmpeg. Rendering is
therefore **deterministic and frame-exact** — no dropped frames, no timing
jitter, and the same input always produces the same file. No intermediate
frames are written to disk.

```
./build.sh                 # default: 30 fps
./build.sh --fps 60        # smoother
./build.sh --scale 2       # 2160x3840 supersample
node preview.mjs 12 22.9   # single frames as PNGs, for checking layout
```

Requires node + playwright (chromium) and ffmpeg with libx264.

## Animation timeline

| t (s) | Beat |
|---|---|
| 0.0 – 0.9 | Blueprint grid fades up; panel border draws out from the centre; corner registration marks spin in |
| 0.7 – 1.7 | `AI + INTERIORS + ARCHITECTURE` types in behind a blinking caret |
| 1.3 – 2.3 | The big **15** spins up as an odometer (01 → 15), then pops with an overshoot and defocus |
| 2.0 – 2.9 | **FREE / CLAUDE / SKILLS** pop in one word at a time — scale overshoot, rotation, blur-in |
| 2.9 – 5.2 | Rules wipe left→right; headline reveals line by line behind a mask; sub-line fades up |
| 5.6 – 6.3 | Column headers slide in; the orange swatch pops and starts a slow heartbeat |
| 5.9 – 6.6 | The 15-row **skeleton** draws in — hairlines and dimmed index numbers, so the sheet reads as a schedule waiting to be filled |
| 6.3 – 23.2 | The fifteen skill names land in order, ~1.15 s apart. Each one: an orange wash sweeps the row, the name wipes open behind a travelling caret, its index brightens, and a marker snaps to the active row |
| 6.1 → 23.2 | Bottom progress bar and `NN / 15 REVEALED` readout track the reveal |
| 23.3 – 24.0 | A bracket draws down the right edge of items 12–15 with `NO INSTALL NEEDED` — the ones already in your Claude account |
| 24.0 – 25.2 | Closing rule wipes; the three footer fields rise in |
| 25.5 – 26.5 | `ALL FREE · MIT` stamp lands with rotation and settles into a slow pulse |
| 26.9 – 30.0 | A light sweep passes across the sheet, the slow push-in settles, and the frame holds |

A very slow push-in (1.0 → 1.012) runs under the whole piece so no frame is
completely static.

## Editing

- **Skill names / order** — the `SKILLS` array in `index.html`. The fourth
  element marks a row as orange (already installed).
- **Pacing** — the `T` object holds every cue time in seconds; `rowStag` is the
  gap between skill reveals. Change `DURATION` if you re-time the tail.
- **Colours** — the `:root` custom properties, sampled from the original sheet.
- **Type** — Playfair Display 900 (the numeral), Inter (headline / title),
  JetBrains Mono (labels, skill names); TTFs are vendored in `fonts/`.
