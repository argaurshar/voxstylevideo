# taj-morph-video — satellite → photoreal aerial, 9:16, silent

A 10-second vertical clip: a flat satellite basemap of the Taj Mahal complex
wipes left-to-right into a cinematic photorealistic aerial of the same place,
under a continuous push-in, closing on a keyword CTA.

    ./build.sh                 # -> out/taj-aerial-morph-9x16.mp4

Output: 1080×1920, 30 fps, 10.00 s, H.264 (yuv420p), **no audio stream at all**.

## Required assets

Two images must sit in `assets/`, and they must share the **same composition** —
same camera position, same framing, everything in the same place. The whole
effect depends on it: if the plates don't line up, the wipe reads as a cut
between two different pictures instead of one place transforming.

| File | What it is |
|---|---|
| `assets/sat.jpg` | Flat satellite basemap look — even overcast light, desaturated, no long shadows |
| `assets/real.jpg` | The same framing as a golden-hour photoreal aerial drone shot |

Both are generated with Magnific (Seedream 5 Pro), 9:16, 2k. `real.jpg` is
produced as a **reference-guided edit of `sat.jpg`**, not a fresh prompt, which
is what keeps the two aligned.

Neither plate is real satellite imagery, so there is no mapping-service licence
attached to the output, and the clip carries no third-party branding.

## Timing

    0.00 – 8.20   wipe sweeps left to right, satellite -> photoreal
    8.40 – 10.00  caption: COMMENT "AI" FOR THE PROMPT
    0.00 – 10.00  push-in, 1.00 -> 1.22

`WIPE_END`, `CTA_IN` and `ZOOM_TO` at the top of the script drive all of it.

The reference clip put its caption at 9.2 s, leaving it on screen for 0.9 s.
This one lands at 8.4 s for 1.6 s — the caption is the only thing in the piece
asking the viewer to act, and under a second is not long enough to read three
lines and decide.

## How it renders

The page never animates on its own. It exposes `window.renderFrame(t)`, and
`render.mjs` calls it once per frame in headless Chromium, screenshots the
result and pipes the PNG straight into ffmpeg with `-an`. Deterministic — no
`Math.random()`, no `Date.now()`, no CSS transitions.

`prepare()` waits for both plates to decode before the first screenshot;
without that, frame 0 renders empty because CSS background images load lazily.

## Why the Taj Mahal

It is the most globally recognisable landmark in India, and — unlike most —
it *gains* legibility from directly overhead rather than losing it: the charbagh
quadrants, the central reflecting-pool axis, four corner minarets, and the
matched red sandstone mosque and jawab are unmistakable in a nadir view.

To swap the location, regenerate both plates with the same two-stage prompt
pattern and drop them into `assets/`. Nothing in the page is Taj-specific.
