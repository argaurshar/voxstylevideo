---
name: vox-motion-graphics
description: >
  Produce a complete narrated motion-graphics explainer video end-to-end with
  Magnific MCP: trend/topic research, fact-checked script, a locked style
  key, animated clips, documentary voiceover, optional score, and one final
  assembled MP4. Two house styles: Vox-style Mixed Media collage (flat
  editorial, burned subtitles) and cinematic paper-diorama documentary (sepia
  newsprint worlds, censor-bar cutouts, letterpress props, fake-oner FPV
  energy). Use this skill whenever the user asks for a "Vox-style video",
  "motion graphics explainer", "animated explainer", "data-driven video",
  "cinematic paper / newspaper collage documentary", "make a video about X",
  "make a video about something trending/viral", a video "like the AI bubble
  reference", or just "run the vox pipeline" — even when no topic is given
  (the skill finds a trending topic itself). Also use it for faceless
  narrated shorts/YouTube videos on geopolitics, money, or power via Magnific.
---

# Vox-Style Motion Graphics Explainer (Magnific MCP)

Turn one request — a topic, or nothing at all — into a finished Vox-style
explainer video: bold editorial collage visuals, a documentary narrator, tight
fact-driven writing, one final MP4. The pipeline runs on the Magnific MCP
using **Seedance 2.0** for clips, **ElevenLabs** for narration, and a local
ffmpeg assembly step.

**The Vox look, in one line:** archival photo cutouts with paper edges drifting
over flat color fields and textured paper, halftone accents, hand-drawn circles
and underlines, abstract growing charts and maps, snappy camera pushes — a
motion-designed magazine spread, never a filmed scene.

**Two house styles** — pick per brief, each with its own reference file:

- **Mixed Media collage** (default; `references/vox-prompts.md`) — flat, bright,
  playful-editorial; no text in clips, subtitles burned at assembly. Best for
  data stories, "why X" explainers, shorts.
- **Paper-diorama documentary** (`references/diorama-doc.md`) — cinematic sepia
  newsprint dioramas, censor-bar cutout figures, one burnt-orange accent,
  letterpress text ON props, fake-oner FPV camera. Best for geopolitics,
  money, power, anything the user wants "cinematic" or high-energy.

## Operating mode

This skill is built to run **hands-off**. The user delegates everything:
topic discovery, script, voice, assets, assembly. That means:

- If the user gave a topic, angle, duration, or voice preference — honor it.
  Everything they didn't specify, decide yourself using the defaults below.
- Right before submitting the first **paid** generation, post one short plan
  message (topic, angle, block count, voice, estimated credits from
  `simulate_cost`) so the user can interrupt — then **proceed immediately
  without waiting for approval**, unless the user asked to be consulted.
- Never stop mid-pipeline to ask a question you can answer with a default.
  Delivering loose clips instead of an assembled MP4 is a failure.

Magnific's `video_generate` asks external clients to call `video_plan` first.
That step exists to draft a brief you don't have — this skill authors its own
prompts, so **skip `video_plan` for block clips** and pass an explicit `slug`.
Calling it once on the overall concept is fine; calling it per block will
fight the script you already wrote.

## Defaults

| Setting    | Default                                | Override when… |
|------------|----------------------------------------|----------------|
| Video model| `bytedance-seedance-pro-2.0` (sota). Cost-sensitive or long runs → `bytedance-seedance-mini-2.0`; drafts → `bytedance-seedance-fast-2.0` | user names a model, or `video_models_list` shows a newer sota |
| Image model| `imagen-nano-banana-2-flash` (Nano Banana 2). **Naming trap:** `imagen-nano-banana-2` is Nano Banana *Pro* — use it only for a final hero asset | user asks for max fidelity |
| Aspect     | 9:16 vertical (shorts/TikTok/Reels). `aspectRatio` is a **required input** on every clip — always set it | user says YouTube/landscape → 16:9 |
| Resolution | `720p` | user asks for 1080p/4K (pro-2.0 only) |
| Duration   | 1 minute → N = 6 blocks (N = minutes × 6, each block = one 10s clip). Seedance accepts 4–15s, so vary block length to fit the beat | user gives a length (1–10 min) |
| Character  | Faceless (no mascot)                   | user asks for a host/mascot |
| Language   | English narration                      | user asks otherwise (prompts stay English regardless) |
| Voice      | `voiceId: 350` (Henry Beckett — British documentary narrator). Alternatives: `366` Ethan Parker (deep US), `519` Basil Thornecroft (dry, wry) | user wants to choose → `audio_voices_show` and wait |
| TTS model  | `eleven_v3` | user wants another provider |
| Subtitles  | ON, burned locally at assembly | user says no subtitles |
| Music      | ON — one instrumental bed via `audio_music_generate`, mixed low | user says no music |

## Story engine (what separates a banger from postcards)

A sequence of pretty, disconnected scenes reads as a museum slideshow. What
makes the reference-grade videos hit:

- **One through-line object.** A single physical metaphor travels through
  EVERY block and escalates (a burning fuse crossing all scenes, a balloon
  being pumped toward a needle). The viewer holds it the whole runtime; the
  finale pays it off. Design this object before writing any block.
- **A question hook, answered last.** Put the question ON a prop
  ("WHO PAYS?", "WHO BLINKS?") in block 1 or the finale; the narration
  withholds the answer until the kicker.
- **Fake-oner.** Write every clip as one continuous FPV camera move that
  begins and ends in full motion blur (dive, whip, flare, fall) — hard cuts
  between blocks then read as one unbroken shot. Parallel generation, no
  frame-matching needed.
- **An impact every ~3 seconds** (slam, stamp, shockwave, snap) and at least
  one speed ramp per block (slow-mo beat → whip). Alternate extreme macro
  and wide diorama; whiplash the scale (giant face → ant-sized figures →
  colossal prop).
- **One reveal shot** the whole video is remembered by (crowd arranged into
  a meaningful silhouette, a reveal only visible when the camera cranes up).

## Pipeline

| Phase | What happens | Tools |
|---|---|---|
| T Topic | use the given topic, or research what's trending and pick one | WebSearch / WebFetch |
| R Research | gather verified facts, numbers, names; keep a Sources list | WebSearch / WebFetch |
| 1 Style key | generate one style swatch; its creation identifier is the key | `images_generate` |
| 2 Script | N narration blocks, Vox formula, ~20–24 words each | reasoning (free) |
| 3 Block prompts | N labeled video prompts in the Vox visual language | reasoning (free) — templates in `references/vox-prompts.md` |
| 4 Clips | N × 10s clips, style key referenced on every one | `video_generate` |
| 5 Voice | one narrator, N takes, same `voiceId` on every block | `audio_voices_list` + `audio_tts` |
| 5b Music | one instrumental bed the length of the video | `audio_music_generate` |
| 6 Assemble | mux narration + music, burn subtitles, concat → one MP4 | `scripts/assemble.py` |

Read `references/vox-prompts.md` before Phase 1 — it holds the style
descriptor, the block-prompt template with worked examples, and the negative
list. Phases T, R, 2, 3 are free; 1, 4, 5, 5b cost credits.

**Job model:** every generation returns a creation `identifier` and queues
async. Long-poll with `creations_wait { identifiers: [...], timeoutSeconds:
25 }` (1–8 at a time; in-progress entries come back with
`poll_after_seconds`). Fetch final asset URLs with `creations_get` — use
`url` (full-res), **never `webUrl`**. An identifier can be passed directly as
a `references[].url` on later generations, so you rarely need raw URLs until
Phase 6. Price any step with `simulate_cost { tool, arguments }` before
running it — it is read-only and never charges.

## Phase T — Topic

**Topic given** → use it, go to Phase R.

**No topic** → find one that's popular *right now*:

1. WebSearch 2–3 angles: `trending topics this week <current month year>`,
   `most searched questions this week`, plus one vertical the user cares
   about if known (tech, money, science, sports…).
2. A good Vox-able topic has: a **"why/how" question** at its core, at least
   one **surprising number or reversal**, strong **visual potential** (maps,
   charts, objects, archival imagery), and broad appeal. "Why X is suddenly
   everywhere", "The real reason X costs so much", "How X quietly changed Y"
   are the shape you want.
3. Avoid: breaking tragedies and active disasters, raw celebrity gossip with
   no data angle, anything you can't verify with two independent sources.
4. Pick the strongest candidate yourself and state it in the plan message
   (with one runner-up in case the user swaps).

## Phase R — Research

Never script from memory. WebSearch the chosen topic, fetch the 2–3 best
sources, and collect: the hook stat, 3–5 concrete facts/numbers/dates, the
counterintuitive turn, and who/what/where specifics that make blocks vivid.
Cross-check every number against a second source. Keep a short **Sources**
list and include it in the final delivery message. No fabricated quotes, no
invented numbers — a vague true line beats a specific false one.

## Phase 1 — Style key

Generate one style swatch at the **same aspect ratio as the video**, using
the STYLE KEY prompt from the chosen style's reference file:

```
images_generate
  prompt: <STYLE KEY prompt from the reference file>
  mode: "imagen-nano-banana-2-flash"
  aspectRatio: "9:16"        # or "16:9" — match the target
  count: 1
```

Wait for it, then keep its creation `identifier`. That identifier IS the
style key: attach it to **every** clip in Phase 4 as

```
references: [ { type: "style", url: "<style key identifier>" } ]
```

Seedance allows exactly **one** `style` reference; additional prop assets go
in as `type: "image"` (limit 9). Generate 2–3 candidates and pick the
strongest if the first swatch is weak — it sets the look of the whole video.

## Phase 2 — Script (Vox formula)

Write N blocks, labeled `Block 1 … Block N`, one per clip. Each block is
**~20–24 words** (~8–9s spoken; hard ceiling ≈9.5s for a 10s clip). Plain
spoken text only: no stage directions, no parentheticals, numbers spelled
out ("seventy percent", "twenty twenty-four").

Structure the N blocks like a Vox piece:

- **Block 1 — cold open.** The most surprising fact or question, stated
  flat. No greeting, no "in this video".
- **Block 2 — stakes.** Why this is weird or why it matters to the viewer.
- **Middle blocks — evidence.** One idea per block, each anchored to a
  concrete number, date, place, or comparison from Phase R. Escalate.
- **Block N−1 — the turn.** The counterintuitive reveal, the "but here's
  the thing".
- **Block N — resolution + kicker.** Land the answer, end on a line that
  reframes the opening fact.

Tone: curious, precise, a little wry. Short declarative sentences. The
narrator explains, never hypes.

## Phase 3 — Block prompts

Write N video prompts, one per block, each visually translating its
narration line into the Vox collage language. Use the exact labeled template
and the scene vocabulary in `references/vox-prompts.md`. Three rules that are
easy to forget:

- **Seedance has no `negativePrompt` field.** The catalog does not list it,
  so exclusions must be written **inline in the prompt text** as a closing
  sentence. Do not pass `negativePrompt` — it will be ignored or rejected.
- **No readable text anywhere in the clips** (Mixed Media). AI-generated
  lettering garbles; typography beats are expressed as abstract highlight
  bars, redaction blocks, circles and underlines instead. Real captions are
  burned locally in Phase 6. The diorama style is the deliberate exception —
  see its reference file.
- **No one speaks on screen.** The sound-design line is ambient/SFX only;
  narration is mixed in at assembly.

## Phase 4 — Clips

Submit N `video_generate` calls — style key on every single one:

```
video_generate
  video:
    clips:
      - slug: "bytedance-seedance-pro-2.0"
        prompt: <Block N video prompt>       # max 10000 chars
        duration: 10                          # 4-15 allowed
        aspectRatio: "9:16"                   # required
        resolution: "720p"
        withSoundEffects: true                # native SFX bed
        cameraMotion: "fpvDrone"              # optional, see below
        references:
          - { type: "style", url: "<style key identifier>" }
          - { type: "image", url: "<prop identifier>" }   # optional, max 9
```

**Use the `cameraMotion` enum instead of hoping the prose lands.** Seedance
exposes 52 named moves; the ones that serve this style are `fpvDrone`,
`whipPan`, `crashZoomIn`, `superDollyIn`, `superDollyOut`, `craneUp`,
`craneDown`, `360Orbit`, `orbitLeft`, `dutchAngle`, `pushIn`, `pullOut`,
`lensFlare`, `focusChange`, `handheld`, `overhead`. Set it per block to match
the written move; keep the prose description too.

**In-block cuts are native.** For a block that needs 2–3 shots, use
`multi_prompt` (max 6 entries, each with `prompt`, `index`, per-shot
`duration`, optional `cameraMotion`) instead of `prompt`. Shot durations must
sum to the clip `duration`. This replaces writing "Shot 1 … Cut to shot 2"
into a single prompt.

Submit in batches, record every identifier against its block number, and
re-submit only failed blocks. If a clip renders photoreal/live-action,
strengthen the style sentence and the inline exclusions and re-run that block
— two identical failures means the prompt is wrong, not the seed. If a slug
is rejected, re-check `video_models_list`; never silently switch to a
photoreal model.

**Face-forward blocks.** Seedance refuses close-up recognizable likenesses
(see the moderation map in `references/diorama-doc.md`). Route those through
an image first: generate the still with `images_generate`, then pass it as
`keyframes: { start: { type: "image", url: "<identifier>" } }`. Note the
constraint — `keyframes` is **prohibited with** `references` of type `image`
or `video`, though a `style` reference is still allowed alongside it.

## Phase 5 — Voiceover

1. Default to `voiceId: 350` (Henry Beckett). To pick differently, call
   `audio_voices_list { search: "documentary" }` and choose a deep, measured
   narrator — calm authority, not ad-read energy. Only show
   `audio_voices_show` and wait if the user asked to choose.
2. One `audio_tts` call per block, same voice every time:

```
audio_tts
  text: "<Block N line, plain text>"
  model: "eleven_v3"
  voiceId: 350
  speed: 1.0          # 0.7-1.2
  stability: 0.5
```

**Verify every take's real duration before assembling.** Fetch each take with
`creations_get` and target **8.0–9.5s** for a 10s block. TTS pacing is
unpredictable: narrator voices pause ~0.7s at every period, so choppy
name-heavy lines read ~1.8 words/s while one flowing comma-joined sentence
reads ~2.5 words/s — the same word count can differ by 4+ seconds. Prefer
single flowing sentences; expect 1–2 re-voice rounds and keep the best take
per block. The assembler compresses a slight overrun automatically and tells
you when a take was too long to fix (see Phase 6).

## Phase 5b — Music

Magnific can score the piece — a capability the pipeline previously lacked.
One instrumental bed for the whole video:

```
audio_music_generate
  prompt: <mood brief — genre, instruments, tempo, arc>
  model: "elevenlabs-music-generation-v2"   # 10-300s, honors durationSeconds
  durationSeconds: <video length, rounded up>
  instrumental: true
```

A brief that matched the reference grade: *"~46 BPM heartbeat pulse,
sub-bass drone and low cello, almost no high frequencies, eight-second
breathing swells, loud open, single climax at eighty percent of runtime,
rapid decay to silence."* Google Lyria models are fixed 30s — use ElevenLabs
v2 for anything longer. Skip this phase if the user said no music.

## Phase 6 — Assemble (automatic, mandatory)

**Magnific has no server-side assembler.** `video_concatenate` joins 2–10
clips but keeps only each clip's own audio ("no external audio bed"), so it
cannot mux narration or burn subtitles. Use it only for a silent/SFX-only
cut. The narrated deliverable is assembled locally by `scripts/assemble.py`.

The moment all clips and takes are done, assemble — in the same run, without
being asked:

1. `creations_get` every clip, take, and the music track; collect the
   full-res `url` of each (never `webUrl`).
2. Read the clips' real `width`/`height` — if they rendered in a different
   aspect than planned, the assembly must match the clips, not the plan.
3. Write a manifest and run it:

```bash
pip install imageio-ffmpeg      # only if no system ffmpeg
python3 scripts/assemble.py manifest.json
```

```json
{
  "out": "topic-slug.mp4",
  "width": 720, "height": 1280,
  "subtitles": true, "font": "Anton",
  "sfx_gain": 0.25,
  "music": {"url": "<music url>", "gain": 0.10},
  "blocks": [
    {"clip": "<clip 1 url>", "voice": "<take 1 url>", "text": "<Block 1 line>"},
    {"clip": "<clip N url>", "voice": "<take N url>", "text": "<Block N line>"}
  ]
}
```

The script downloads everything, ducks each clip's native Seedance audio
under the narration, burns chunked captions, holds the last frame if a take
genuinely overruns, concatenates, and lays the music bed underneath with
fade in/out. It prints a JSON report: per-block clip/voice/block durations,
any tempo compression applied, and a `warnings` list. **Read the warnings** —
a block flagged "consider re-voicing shorter" should be re-voiced and
reassembled rather than shipped.

Font note: `Anton` is the intended caption face but is rarely installed. The
script falls back through Oswald → Liberation Sans Narrow → a condensed
Liberation/DejaVu Sans (ScaleX 88), which reads correctly. Dropping
`Anton-Regular.ttf` into a system font dir upgrades it automatically.

Finally, present the MP4 to the user. Use `creations_show` for any Magnific
creations worth previewing inline; send the assembled local file directly.

## Delivery

Final message: the video, the topic + angle in one sentence, the full script
(so the user can reuse it), and the Sources list. Then offer — don't run
unasked — a titles/description/tags pass if the video is headed to YouTube.

## Failure handling

- Clip drifts off-style → re-attach the style key, strengthen the style
  sentence and inline exclusions, rerun that block only.
- Voice take too long → shorten the line or lower `speed`, re-voice that
  block only. The assembler's warnings tell you exactly which blocks.
- `video_generate` rejects `negativePrompt` → Seedance doesn't support it;
  move exclusions inline into the prompt text.
- `references` rejected alongside `keyframes` → `image`/`video` references
  are prohibited with keyframes; drop to a `style` reference only.
- Creation stuck non-terminal → `creations_wait` returns `poll_after_seconds`;
  respect it and poll again rather than resubmitting (resubmitting double-charges).
- Video job fails with no error text → moderation, not bad luck. Check the
  moderation map in `references/diorama-doc.md`: named politicians and
  close-up recognizable faces fail (route those blocks through a
  `keyframes.start` still or drop to mid-shot descriptions); "mushroom cloud"
  and similar flag nsfw — swap the image, keep the idea.
- User wants isolated deliverables (SFX-only track, single clips, stills):
  raw clips have no narration — it exists only in the local assembly — so the
  downloaded clips are already clean voiceless assets, and
  `video_concatenate` gives a quick SFX-only cut.
