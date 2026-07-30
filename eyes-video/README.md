# eyes-video — "Give Claude eyes", 9:16, silent

A 24-second vertical explainer for the `eyes` skill: Claude only reads the
transcript, so it misses everything that is only on screen — until you cut the
video into frames and hand it both.

    ./build.sh                 # -> out/give-claude-eyes-9x16.mp4
    ./build.sh --fps 60        # smoother, 2x the frames
    ./build.sh --scale 2       # 2160x3840 supersample

Output: 1080×1920, 30 fps, 24.00 s, H.264 (yuv420p), **no audio stream at all**.

| File | |
|---|---|
| `index.html` | The design and the whole animation timeline |
| `render.mjs` | Frame-exact renderer (Chromium → ffmpeg) |
| `preview.mjs` | Dumps single frames as PNGs for layout checks |
| `build.sh` | Wrapper |
| `fonts/` | Vendored TTFs (Inter, JetBrains Mono) |

## How it renders

The page never animates on its own. It exposes `window.renderFrame(t)`, and
`render.mjs` calls it once per frame in headless Chromium, screenshots the
result and pipes the PNG straight into ffmpeg with `-an`. The render is
deterministic — no `Math.random()`, no `Date.now()`, no CSS transitions — so
the same input always yields the same file, and no intermediate frames touch
the disk.

## The piece

Bone paper, ink type, one cobalt accent. The hero object is a **contact
sheet**: 24 landscape cells that are the same synthetic clip sampled at 24
different moments, which is the thing the skill actually does.

1. **01 · THE GAP** — a transcript fills the sheet area: timestamps and lines
   of words, and nothing else. "It never sees the picture." is written, then
   struck through in cobalt.
2. The words wipe out and 24 **empty frame cells** outline in where the
   pictures should have been — "Half the video is missing."
3. **02 · THE FIX** — "So give it eyes." A cobalt outline travels the empty
   cells, looking at each one.
4. **03 · YT-DLP** — the source lands as a single card with a play glyph.
5. **04 · FFMPEG** — that card **splits into its 24 frames**, each tile flying
   from its slice of the card out to its place in the grid.
6. **05 · WHISPER.CPP** — the transcript returns as three timestamped lines
   under the sheet, so both halves are now on screen.
7. **06 · CLAUDE** — a cobalt scan bar walks down the sheet and stamps every
   frame with its timestamp.
8. **07 · THE RESULT** — a 30:00 source chip, then the counter races to
   **739**, and it closes on "It sees the whole video."

Timing lives in the `BEATS` array (headline, caption, command line, chapter)
and the `S` object (the sheet choreography); the two are deliberately separate
so pacing and staging can be tuned apart.

## Why 739

That is what the `eyes` skill's own sampling produces for a 30-minute source,
not a round number picked for the edit:

    hook   15s @ 15fps            -> 225 frames
    body   1800s @ 1 frame/3.5s   -> 514 frames
                                     ---
                                     739

Verified against `ffmpeg -f lavfi -i color=...:d=1800 -vf fps=1/3.5`. The
per-cell timestamps walk the full half hour (00:00 → 28:45) for the same
reason.

## Captions, not narration

The piece is silent by design, so every line that would have been spoken is
burned in at the bottom instead. Nothing is carried by audio — it reads the
same muted, which is how vertical video is watched anyway.
