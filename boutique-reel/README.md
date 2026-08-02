# boutique-reel — Delhi boutique, site → sketch → render

A 10-second 9:16 reel showing an interior project in three stages: the raw
construction shell, a hand-drawn concept overlay on that same photo, and the
finished space. Built entirely on Magnific — unlike the other videos in this
repo, no local rendering was involved.

Final video: `Delhi boutique — site to sketch to render` in the Magnific
gallery, 10 s, 1080p, 9:16, silent (Kling 2.5 emits no audio track).

## The three plates

| File | Stage |
|---|---|
| `assets/1-site.jpg` | Raw shell — exposed brick, block wall, copper pipes, rubble, hard window light |
| `assets/2-sketch.jpg` | The *same photograph* with white continuous-line concept overlay |
| `assets/3-render.jpg` | Finished warm Indian boutique interior |

Generated with Seedream 5 Pro at 9:16. Stages 2 and 3 were produced as
**reference-guided edits of stage 1**, not as fresh prompts — that is what keeps
the camera still across the sequence.

Design direction: hand-troweled lime plaster in terracotta and clay, a curved
Kota stone counter with a brass edge, a carved red sandstone jaali screen
throwing patterned light, backlit brass niches, cane webbing with indigo and
madder block-print, terrazzo and red sandstone floor, dried palm and marigold.

## Verifying a set before animating

The whole effect depends on the plates sharing one camera. Test it by
compositing the left half of one against the right half of another — walls,
window and floor edges should run straight through the seam:

    ffmpeg -i 1-site.jpg -i 2-sketch.jpg -filter_complex \
      "[0:v]crop=iw/2:ih:0:0[l];[1:v]crop=iw/2:ih:iw/2:0[r];[l][r]hstack=2" chk.png

On this set, **1 → 2 is pixel-identical** (stage 2 really is the site photo with
lines drawn on it) but **1 → 3 is a different, wider viewpoint**. The second
transition is therefore a morph across a camera move rather than a seamless
materialise. Accepted deliberately; regenerating stage 3 pinned harder to
stage 1 is the fix if a true match is wanted.

## The animation

Kling 2.5, two clips, 5 s each, **1080p** — the resolution matters: at 720p
Kling requires a start frame and *prohibits* an end frame, and without both ends
pinned the model invents its own interior and the approved design is lost.

| Clip | Start frame | End frame |
|---|---|---|
| 1 | `1-site` | `2-sketch` |
| 2 | `2-sketch` | `3-render` |

Clip 1: slow forward push, dust drifting through the window shaft, white
concept lines drawing themselves into the air over the untouched shell.
Clip 2: the lines dissolve as brick blooms into plaster, the jaali screen
materialises and casts patterned light, brass pendants descend and light up.

Assembled with `video_concatenate`.

## Why this one is not rendered locally

This session's container only permits outbound traffic to an allowlist.
`pikaso.cdnpk.net` (asset delivery) and `ak-data.magnific.com` (upload) are both
blocked, so generated media cannot be pulled down and local files cannot be
pushed up. Everything therefore had to stay server-side, and Kling had to be
pointed at creation identifiers rather than uploaded files.

Consequence: no burned-in CTA. Overlaying type needs the video on local disk.
To add one, download the MP4, place it here, and run an ffmpeg `drawtext` pass —
or reuse the caption approach in `../taj-morph-video/index.html`.
