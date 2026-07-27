#!/usr/bin/env python3
"""
Assemble a narrated motion-graphics explainer from Magnific creations.

Magnific has no server-side assembler: `video_concatenate` joins clips but
keeps only each clip's own audio ("no external audio bed"), so narration,
music and burned subtitles have to be muxed locally. This script is that
step — Phase 6 of the vox-motion-graphics skill.

Usage:
    python3 assemble.py manifest.json

Manifest (see MANIFEST_EXAMPLE at the bottom for a filled-in copy):
{
  "out": "final.mp4",
  "width": 720,
  "height": 1280,
  "subtitles": true,
  "font": "Anton",                 # falls back to a condensed bold if absent
  "sfx_gain": 0.25,                # clip's native Seedance audio, ducked
  "music": {"url": "...", "gain": 0.10},
  "blocks": [
    {"clip": "<url|path>", "voice": "<url|path>", "text": "narration line"}
  ]
}

Only "blocks" is required; every block needs "clip". A block with no "voice"
runs as a pure visual beat. Pass creation `url` values from `creations_get`
(the full-res asset URL) — never `webUrl`.

Exit code 0 on success. Prints a JSON report to stdout describing per-block
timing and any narration that had to be time-compressed, so the caller can
decide whether to re-voice a block.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

# ---------------------------------------------------------------- constants

# Narration is nudged this far in from the top of a block so it doesn't
# collide with the clip's opening impact.
LEAD_IN = 0.30
# Tail room left after narration before the block cuts.
TAIL_PAD = 0.25
# Most we will speed up a long take before flagging it for a re-voice.
# Beyond ~1.12 the narrator audibly rushes.
MAX_ATEMPO = 1.12
# Words per caption chunk.
CHUNK_WORDS = 6

FONT_CANDIDATES = [
    # (family name as libass sees it, ScaleX to fake condensed)
    ("Anton", 100),
    ("Oswald", 100),
    ("Liberation Sans Narrow", 100),
    ("DejaVu Sans Condensed", 100),
    ("Liberation Sans", 88),
    ("DejaVu Sans", 88),
]


# ------------------------------------------------------------------ helpers

def die(msg):
    print(f"assemble: error: {msg}", file=sys.stderr)
    sys.exit(1)


def ffmpeg_bin():
    """Prefer a system ffmpeg; fall back to the imageio-ffmpeg wheel."""
    system = shutil.which("ffmpeg")
    if system:
        return system
    try:
        import imageio_ffmpeg
    except ImportError:
        die("no ffmpeg found. Install one with: pip install imageio-ffmpeg")
    return imageio_ffmpeg.get_ffmpeg_exe()


FF = None  # populated in main()


def run(args, check=True):
    p = subprocess.run(args, capture_output=True, text=True)
    if check and p.returncode != 0:
        die(f"ffmpeg failed:\n{' '.join(args[:6])} ...\n{p.stderr[-1500:]}")
    return p


def duration_of(path):
    """Read a media duration without depending on ffprobe being present."""
    p = subprocess.run([FF, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", p.stderr)
    if not m:
        die(f"could not read duration of {path}")
    h, mnt, s = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(s)


def has_audio(path):
    p = subprocess.run([FF, "-hide_banner", "-i", path],
                       capture_output=True, text=True)
    return bool(re.search(r"Stream #\d+:\d+.*: Audio:", p.stderr))


def fetch(src, dest):
    """Accept a local path or an http(s) URL; return a local path."""
    if not src:
        return None
    if not str(src).startswith(("http://", "https://")):
        if not os.path.exists(src):
            die(f"input not found: {src}")
        return src
    req = urllib.request.Request(src, headers={"User-Agent": "vox-assemble/1"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r, \
                open(dest, "wb") as f:
            shutil.copyfileobj(r, f)
    except Exception as e:  # noqa: BLE001 - surface the real cause
        die(f"download failed for {src}: {e}")
    if os.path.getsize(dest) == 0:
        die(f"downloaded 0 bytes from {src}")
    return dest


def pick_font(requested):
    """Resolve a subtitle font to (family, scale_x) that libass can find."""
    installed = set()
    if shutil.which("fc-list"):
        out = subprocess.run(["fc-list", ":", "family"],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            for fam in line.split(","):
                installed.add(fam.strip())
    candidates = list(FONT_CANDIDATES)
    if requested:
        candidates.insert(0, (requested, 100))
    for fam, scale in candidates:
        if fam in installed:
            return fam, scale
    # libass will substitute something legible; condense it a little.
    return (requested or "sans-serif"), 92


def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def chunk_words(text, per):
    words = text.split()
    return [" ".join(words[i:i + per]) for i in range(0, len(words), per)] or []


def build_ass(text, start, end, path, width, height, font, scale_x):
    """One caption track for a single block, chunked for readability."""
    chunks = chunk_words(text, CHUNK_WORDS)
    if not chunks:
        return False
    span = max(0.4, end - start)
    total_words = sum(len(c.split()) for c in chunks)
    # Font size tracks the short edge so 9:16 and 16:9 both read correctly.
    short_edge = min(width, height)
    fontsize = max(18, int(short_edge * 0.062))
    margin_v = int(height * 0.10)
    margin_h = int(width * 0.07)

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Vox,{font},{fontsize},&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,{scale_x},100,0,0,1,{max(2, fontsize // 9)},0,2,{margin_h},{margin_h},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    cursor = start
    for c in chunks:
        share = len(c.split()) / total_words
        c_end = cursor + span * share
        safe = c.replace("\n", " ").replace("{", "(").replace("}", ")")
        lines.append(
            f"Dialogue: 0,{ass_time(cursor)},{ass_time(c_end)},Vox,,0,0,0,,{safe}"
        )
        cursor = c_end
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")
    return True


def atempo_chain(rate):
    """ffmpeg's atempo accepts 0.5-2.0 per stage; chain if outside."""
    stages = []
    r = rate
    while r > 2.0:
        stages.append(2.0)
        r /= 2.0
    while r < 0.5:
        stages.append(0.5)
        r /= 0.5
    stages.append(r)
    return ",".join(f"atempo={s:.6f}" for s in stages)


# --------------------------------------------------------------------- main

def main():
    global FF
    if len(sys.argv) != 2:
        die("usage: assemble.py manifest.json")
    with open(sys.argv[1], encoding="utf-8") as f:
        man = json.load(f)

    FF = ffmpeg_bin()

    blocks = man.get("blocks") or []
    if not blocks:
        die("manifest has no blocks")

    out = man.get("out", "final.mp4")
    width = int(man.get("width", 720))
    height = int(man.get("height", 1280))
    want_subs = bool(man.get("subtitles", True))
    sfx_gain = float(man.get("sfx_gain", 0.25))
    music = man.get("music") or {}

    work = os.path.abspath(man.get("workdir", "vox_build"))
    os.makedirs(work, exist_ok=True)

    font, scale_x = pick_font(man.get("font"))
    report = {"font": font, "scale_x": scale_x, "blocks": [], "warnings": []}

    seg_paths = []
    for i, b in enumerate(blocks, start=1):
        tag = f"b{i:02d}"
        clip = fetch(b.get("clip"), os.path.join(work, f"{tag}_clip.mp4"))
        if not clip:
            die(f"block {i} has no clip")
        voice = fetch(b.get("voice"), os.path.join(work, f"{tag}_vo.mp3"))

        clip_d = duration_of(clip)
        vo_d = duration_of(voice) if voice else 0.0
        clip_has_audio = has_audio(clip)

        # Fit narration inside the clip window where possible; only stretch
        # the block if the take genuinely cannot be compressed enough.
        tempo = 1.0
        block_d = clip_d
        note = None
        if vo_d:
            budget = clip_d - LEAD_IN - TAIL_PAD
            if vo_d > budget:
                needed = vo_d / max(0.1, budget)
                if needed <= MAX_ATEMPO:
                    tempo = needed
                    note = f"narration sped {needed:.3f}x to fit"
                else:
                    tempo = MAX_ATEMPO
                    block_d = LEAD_IN + (vo_d / MAX_ATEMPO) + TAIL_PAD
                    note = (f"take {vo_d:.1f}s exceeds clip {clip_d:.1f}s; "
                            f"capped at {MAX_ATEMPO}x and block extended to "
                            f"{block_d:.1f}s — consider re-voicing shorter")
                    report["warnings"].append(f"block {i}: {note}")
        eff_vo = (vo_d / tempo) if vo_d else 0.0
        vo_start = LEAD_IN
        vo_end = vo_start + eff_vo

        # ---- filtergraph
        inputs = ["-i", clip]
        if voice:
            inputs += ["-i", voice]

        # Always start from a filter label so every branch below can be
        # mapped uniformly as [label] regardless of which chains ran.
        chains = ["[0:v]null[v0]"]
        vlabel = "v0"
        if block_d > clip_d + 0.05:
            # Hold the last frame rather than stretching motion.
            chains.append(f"[{vlabel}]tpad=stop_mode=clone:stop_duration="
                          f"{block_d - clip_d:.3f}[vp]")
            vlabel = "vp"

        sub_path = os.path.join(work, f"{tag}.ass")
        if want_subs and b.get("text") and voice:
            if build_ass(b["text"], vo_start, vo_end, sub_path,
                         width, height, font, scale_x):
                esc = sub_path.replace("\\", "/").replace(":", r"\:")
                chains.append(f"[{vlabel}]subtitles='{esc}'[vs]")
                vlabel = "vs"

        # audio: ducked clip SFX + narration
        alabel = None
        if clip_has_audio and sfx_gain > 0:
            chains.append(f"[0:a]volume={sfx_gain},"
                          f"apad,atrim=0:{block_d:.3f},asetpts=N/SR/TB[bed]")
            alabel = "bed"
        if voice:
            vo_chain = f"[1:a]{atempo_chain(tempo)}," if tempo != 1.0 else "[1:a]"
            if tempo == 1.0:
                vo_chain = "[1:a]"
            chains.append(
                f"{vo_chain}adelay={int(vo_start * 1000)}|{int(vo_start * 1000)},"
                f"apad,atrim=0:{block_d:.3f},asetpts=N/SR/TB[vo]")
            if alabel:
                chains.append(f"[{alabel}][vo]amix=inputs=2:duration=first:"
                              f"normalize=0[aout]")
                alabel = "aout"
            else:
                alabel = "vo"
        if alabel is None:
            chains.append(f"anullsrc=r=44100:cl=stereo,atrim=0:{block_d:.3f}[aout]")
            alabel = "aout"

        seg = os.path.join(work, f"{tag}_seg.mp4")
        args = [FF, "-hide_banner", "-loglevel", "error", *inputs,
                "-filter_complex", ";".join(chains),
                "-map", f"[{vlabel}]", "-map", f"[{alabel}]",
                "-t", f"{block_d:.3f}",
                "-r", "24",
                "-c:v", "libx264",
                "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-ar", "44100", "-ac", "2",
                "-video_track_timescale", "24000",
                seg, "-y"]
        run(args)
        seg_paths.append(seg)
        report["blocks"].append({
            "block": i, "clip_s": round(clip_d, 2), "voice_s": round(vo_d, 2),
            "block_s": round(block_d, 2), "tempo": round(tempo, 3),
            "note": note,
        })

    # ---- concat
    list_path = os.path.join(work, "concat.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for s in seg_paths:
            f.write(f"file '{s}'\n")

    joined = os.path.join(work, "joined.mp4")
    run([FF, "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", list_path, "-c", "copy", joined, "-y"])

    total = duration_of(joined)

    # ---- optional music bed under the whole piece
    if music.get("url"):
        mpath = fetch(music["url"], os.path.join(work, "music.mp3"))
        gain = float(music.get("gain", 0.10))
        run([FF, "-hide_banner", "-loglevel", "error",
             "-i", joined, "-stream_loop", "-1", "-i", mpath,
             "-filter_complex",
             f"[1:a]volume={gain},afade=t=in:st=0:d=1.5,"
             f"afade=t=out:st={max(0.0, total - 2.5):.3f}:d=2.5[mus];"
             f"[0:a][mus]amix=inputs=2:duration=first:normalize=0[aout]",
             "-map", "0:v", "-map", "[aout]",
             "-c:v", "copy", "-c:a", "aac", "-ar", "44100",
             "-t", f"{total:.3f}", out, "-y"])
    else:
        shutil.copyfile(joined, out)

    report["out"] = os.path.abspath(out)
    report["duration_s"] = round(duration_of(out), 2)
    report["size_bytes"] = os.path.getsize(out)
    print(json.dumps(report, indent=2))


MANIFEST_EXAMPLE = {
    "out": "why-food-waste.mp4",
    "width": 720, "height": 1280,
    "subtitles": True, "font": "Anton",
    "sfx_gain": 0.25,
    "music": {"url": "https://…/score.mp3", "gain": 0.10},
    "blocks": [
        {"clip": "https://…/clip1.mp4", "voice": "https://…/vo1.mp3",
         "text": "Every day humans throw away enough food to feed two billion people."},
    ],
}

if __name__ == "__main__":
    main()
