# design-prompts-video — "15 design prompts", 9:16, silent

A 54-second Instagram reel: a hook, 15 prompt topics at 3.0 s each, and a
keyword CTA. The reel carries the short punchy line per topic; the full prompts
live in `CAPTION.md` for the caption or the DM auto-reply.

    ./build.sh                 # -> out/15-design-prompts-9x16.mp4
    ./build.sh --fps 60        # smoother, 2x the frames
    ./build.sh --scale 2       # 2160x3840 supersample

Output: 1080×1920, 30 fps, 54.00 s, H.264 (yuv420p), **no audio stream at all**.

| File | |
|---|---|
| `index.html` | The design, the content, and the whole animation timeline |
| `CAPTION.md` | The 15 full prompts + a beat-matched voiceover script |
| `render.mjs` | Frame-exact renderer (Chromium → ffmpeg) |
| `preview.mjs` | Dumps single frames as PNGs for layout checks |
| `build.sh` | Wrapper |
| `fonts/` | Vendored TTFs (Inter, JetBrains Mono) |

## Timing

    0:00 – 0:04   hook
    0:04 – 0:49   15 topics × 3.0 s
    0:49 – 0:54   CTA

`HOOK`, `PER` and `CTA` at the top of the script drive all of it, so changing
`PER` to 2.5 reflows the whole reel and `VIDEO_DURATION` with it.

## How it renders

The page never animates on its own. It exposes `window.renderFrame(t)`, and
`render.mjs` calls it once per frame in headless Chromium, screenshots the
result and pipes the PNG straight into ffmpeg with `-an`. Deterministic — no
`Math.random()`, no `Date.now()`, no CSS transitions — so the same input always
yields the same file.

## The design

Claude's palette: warm ivory ground (`#F0EEE6`), near-black ink, terracotta
accent (`#D97757`). Inter for the type, JetBrains Mono for labels and the prompt
body, so the prompt reads as something you'd actually paste into a terminal or
a chat box.

Per topic, in order:

1. The index rolls in (`01 / 15`) and the segment meter advances.
2. A **line glyph draws itself on** — every one of the 15 is drawn stroke by
   stroke in canvas, not faded in. Each is specific to its stage: a document, a
   rule set with one item checked, three overlapping concept circles, a row of
   finish swatches, a floor plan with a door swing, a sheet stack, a consultant
   hub, a vendor table, a code shield, an RFI bubble, a punch-list clipboard, a
   superseded sheet being archived, a revision delta, a guardrail, a closed loop.
3. The **title types out** behind a terracotta caret.
4. The short line rises in word by word.
5. The prompt card opens and the **prompt types itself out** — the substance,
   readable in the 3 seconds it's on screen.

Running underneath the whole reel: a marquee of all 15 topic names, the Claude
spark turning slowly in the top-left, and a very slow push-in so no frame is
completely static.

The spark is drawn procedurally in `spark()` — 11 tapered petals with per-petal
length, so it can be scaled, recoloured or re-timed from code rather than being
a pasted asset.

## A note on the mark

The spark and the palette are Claude's, used to signal what the prompts are for.
That's referential use, not a claim of endorsement — the reel carries no
Anthropic wordmark and no "official" framing. If you'd rather avoid the
association entirely, change the `spark()` call sites or swap `--clay` in
`:root`; nothing else depends on either.

## Safe area

Everything load-bearing sits above y=1650, so Instagram's caption and action
buttons don't cover the CTA, the prompt card or the marquee. The top bar starts
at y=118 for the same reason at the top.
