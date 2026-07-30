---
name: eyes
description: Use when the user gives a video URL or local video file (YouTube, Instagram, TikTok, Loom, direct link) and wants Claude to actually SEE it — a scene-by-scene / frame-by-frame breakdown, on-screen text, cuts, visual hook — not just the transcript. Triggers on "/eyes URL", "give claude eyes", "watch this video", "break this reel down", "what happens on screen in this video".
---

# eyes — see the video, not just the transcript

Claude has no native video model, so this skill splits a video into the two things Claude does
understand — **images + text** — and reads both with the timestamps lined up. Everything runs
locally; there is no API cost.

Run every step. Never skip the dense-hook sampling — that is what makes the read accurate.

## Step 0 — Check the toolchain (first run only)

```bash
for c in yt-dlp ffmpeg ffprobe whisper-cli; do command -v $c >/dev/null || echo "missing: $c"; done
```

If anything is missing, install it and stop to tell the user what was installed:

```bash
# macOS (Homebrew)
brew install yt-dlp ffmpeg whisper-cpp

# small, fast local transcription model (~150 MB, one time)
mkdir -p ~/.claude/models
curl -L -o ~/.claude/models/ggml-base.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

Linux: `pipx install yt-dlp`, `apt install ffmpeg`, and build `whisper.cpp` from its repo.
Windows: `winget install yt-dlp.yt-dlp`, `winget install Gyan.FFmpeg`, plus whisper.cpp from its repo.
Same three tools everywhere. On some whisper.cpp builds the binary is `main` or `whisper-cpp`
instead of `whisper-cli` — use whichever exists.

## Step 1 — Get the video

```bash
mkdir -p /tmp/eyes && cd /tmp/eyes
yt-dlp -o video.mp4 -f "mp4" "<URL>"          # skip if the user gave a local file
ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4   # duration in seconds
```

If `yt-dlp` fails on a login-walled URL, say so and ask the user for a file or a public link —
do not try to work around the wall.

## Step 2 — Two-stage frame sampling (the important part)

The hook carries the most motion and decides retention, so sample it densely and the body sparsely.
One frame every few seconds only catches end-states — it misses word-by-word reveals, fast cuts and
count-up animations.

```bash
# HOOK: first 15s at 15 fps -> tiled contact sheets (5 cols x 9 rows = 45 frames = 3s per sheet)
mkdir -p hook && ffmpeg -y -t 15 -i video.mp4 \
  -vf "fps=15,scale=200:-1,tile=5x9:margin=6:padding=4:color=white" -an hook/sheet_%02d.jpg

# BODY: 1 frame / 3.5s across the whole video
mkdir -p body && ffmpeg -y -i video.mp4 -vf "fps=1/3.5,scale=360:-1" body/f_%03d.jpg
```

Read the sheets in order. Frame N of the hook is at `t = N / 15` seconds, where sheet k, cell i
(row-major) is frame `(k-1)*45 + i`. Body frame `f_NNN.jpg` is at `t ≈ (NNN - 0.5) * 3.5` seconds.

For a video longer than ~10 minutes, raise the body interval (`fps=1/8`) so the frame count stays
readable, and say in the output that you sampled more sparsely.

## Step 3 — Transcribe the audio (free, local)

```bash
ffmpeg -y -i video.mp4 -ar 16000 -ac 1 audio.wav
whisper-cli -m ~/.claude/models/ggml-base.en.bin -f audio.wav -otxt -of transcript
```

If the source has real captions, prefer those — free and exact:
`yt-dlp --write-auto-subs --sub-format vtt --skip-download -o captions "<URL>"`.

Always sanity-check the transcript against the frames. Local models mishear names and jargon
(they'll hear "Claude" as "plot"); the on-screen text is usually the ground truth.

## Step 4 — Read frames + transcript together, then output

Look at the hook sheets and the body frames, line them up with the transcript timing, and produce:

1. **Transcript** — corrected against what is on screen.
2. **Scene-by-scene breakdown** — per chapter: timecode, what's on screen, the on-screen text, the cut.
3. **Why it works** — 2–3 concrete mechanisms (hook structure, cut cadence, the one visual payoff, the CTA).
4. **Steal-the-structure notes** — what to lift into your own video (change the content, keep the structure).

Describe only what is actually visible in the frames. If something is ambiguous between two frames,
say so rather than inventing the in-between.

## Step 5 — Clean up

```bash
rm -rf /tmp/eyes
```

Keep the files only if the user asked for the frames or the transcript as artifacts, and tell them
where they are.

---

Adapted from "Give Claude Eyes" by Conrad (@buildwith.conrad),
<https://gist.github.com/conradcaffier03/ef914685fc9d7da91b6591947fa1ddb2>.
