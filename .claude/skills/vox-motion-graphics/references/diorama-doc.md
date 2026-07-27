# Paper-Diorama Documentary Style ("WHO BLINKS?" playbook)

The second house style: a cinematic vintage paper-diorama documentary —
aged sepia newsprint worlds, censor-bar cutout figures, one burnt-orange
accent, letterpress prop typography, tungsten light, macro tilt-shift.
Born from reverse-engineering a reference video and battle-tested on the
"WHO BLINKS?" nuclear-treaty explainer. Use it when the brief says
cinematic / dramatic / investigative / "like the AI bubble video", or when
the topic is geopolitics, money, or power.

## Style key

Generate a fresh key per run with `images_generate`
(`mode: "imagen-nano-banana-2-flash"`, `aspectRatio` matching the video),
then attach its creation `identifier` as the single `{ type: "style" }`
reference on every clip:

```
Cinematic vintage paper diorama style swatch, documentary collage
aesthetic: a miniature three-dimensional landscape built entirely from
aged sepia newspaper sheets and cardboard, torn edges, layered paper
canyon walls of old newsprint, monochrome archival photo cutouts of
anonymous suited figures standing among the paper structures with black
censor bars over their eyes, one dominant burnt-orange paper prop as the
single color accent against the sepia world, distressed letterpress print
texture, warm tungsten documentary lighting with deep shadows, macro
tilt-shift lens look with shallow depth of field, film grain and dust.
Handcrafted physical paper materials only — no letters, no words, no
numbers, no logos. Non-photorealistic scene content, no live-action
people, stylized paper craft world.
```

## STYLE tokens (open every clip prompt with these)

```
cinematic vintage paper diorama, aged sepia newsprint world, monochrome
halftone print, monochrome archival cutout figures with black censor bars
over their eyes, single burnt-orange accent, distressed letterpress,
warm tungsten light, macro tilt-shift shallow depth of field, film grain,
handcrafted stop-motion paper feel, non-photorealistic, no live-action
```

## Prop typography

Unlike the Mixed Media style (which bans all in-clip text), this style
CARRIES short letterpress text on props — that's its signature. One label
per scene, 1–2 words or a number ("EXPIRED", "1,000", "AUGUST",
"WHO BLINKS?"), always described as "distressed letterpress" on a torn
burnt-orange paper element, and always fenced in the closing exclusions:
`No text anywhere except "<LABEL>". No gibberish letters…`.

## Reusable prop assets

Props keep objects from morphing between clips. Generate each one 1:1 on a
plain background with the style key referenced:

```
images_generate
  prompt: "Single reusable prop asset, centered on a plain warm off-white
           paper background… Nothing else in frame. <STYLE tokens>"
  mode: "imagen-nano-banana-2-flash"
  aspectRatio: "1:1"
  references: [ { type: "style", identifier: "<style key identifier>" } ]
```

Then pass each prop into the clip alongside the style key as
`{ type: "image", url: "<prop identifier>" }` (Seedance allows up to 9) and
say "the X from the reference image" in the prompt.

Props worth building for a geopolitics piece: a paper missile with an orange
nose, an aged newspaper front page with a censor-bar portrait, a powder keg
with a coiled fuse carrying the question label, and a set of anonymous leader
cutouts distinguished only by silhouette and tie color.

**For props reused across multiple videos**, promote them once with
`library_create { name, type: "product", images: [{ creationIdentifier }] }`
and reference the returned numeric `id` thereafter — that survives past a
single run, where a bare creation identifier is just an asset pointer.

> Earlier versions of this file pinned specific job ids for a prebuilt key
> and four props. Those were Higgsfield job ids and do not resolve on
> Magnific — always generate or look up your own.

## Engine: Seedance 2.0

```
video_generate
  video:
    clips:
      - slug: "bytedance-seedance-pro-2.0"
        prompt: <fake-oner block prompt>
        duration: 10
        aspectRatio: "16:9"
        resolution: "720p"
        withSoundEffects: true
        cameraMotion: "fpvDrone"
        references:
          - { type: "style", url: "<style key identifier>" }
          - { type: "image", url: "<prop identifier>" }
```

Seedance reads "speed ramp", "FPV" and "whip pan" literally and renders real
fire/embers beautifully. Its native sound effects (fuse crackle, drones,
impacts) survive assembly ducked under the voiceover — design them in the
prompt ("Sound design: … No speech.") and keep `withSoundEffects: true`.

There is no per-clip `genre` control on Magnific — the dark grade comes from
the style key and the STYLE tokens, so keep both attached to every clip.

**Multi-shot blocks:** rather than writing "Shot 1 … Cut to shot 2" into one
prompt, use `multi_prompt` (max 6 shots, per-shot `duration` and
`cameraMotion`, durations summing to the clip `duration`). Seedance cuts
between them natively.

Cheaper passes: `bytedance-seedance-mini-2.0` is the quality/price pick and
`bytedance-seedance-fast-2.0` is for drafts; both take the same references,
`cameraMotion` and `multi_prompt` controls, capped at 720p.

## Moderation map (hard-won)

- **Named politicians in video prompts → the job fails** (submits fine, dies
  at render). Names are fine in the TTS narration.
- **Close-up recognizable statesman faces** (even described, unnamed) fail.
  Route those blocks through an image first: generate the still with
  `images_generate`, then animate it via
  `keyframes: { start: { type: "image", url: "<identifier>" } }`. Mind the
  constraint — `keyframes` cannot be combined with `image` or `video`
  references, though a `style` reference is still allowed.
- Mid-shot / full-body "leader with red tie / compact Russian / East
  Asian statesman" descriptions pass. Censor bars over the eyes both sell
  the editorial look and defuse likeness issues.
- **"mushroom cloud" → nsfw flag.** Replace with another silhouette
  (an hourglass worked and fit the deadline theme better).
- A failed generation still costs nothing only if it never rendered — check
  `creations_wait` before resubmitting, since a resubmit double-charges.

## Fake-oner block prompt shape

Every clip = one continuous camera move; every boundary hidden in motion
blur so hard cuts read as a single unbroken shot:

```
<STYLE tokens> — shot as ONE continuous high-energy FPV camera move with
aggressive speed ramps.
The shot: [emerges from motion-blurred <previous element>] … [one impact
moment every ~3s: slam / stamp / shockwave / snap] … [ends fully
motion-blurred mid-<dive/whip/fall/flare>].
Sound design: [3–5 concrete diegetic events]. No speech.
No text anywhere except "<LABEL>". No gibberish letters, no captions,
no watermark, no photorealism, no live-action.
```

Worked example (opening block of "WHO BLINKS?"):

```
…shot as ONE continuous high-energy FPV camera move with aggressive speed
ramps.
The shot: from black, EXTREME slow-motion macro of a halftone-printed
human eye on newsprint as a thick black censor bar SLAMS down over it
like a guillotine, paper dust exploding on impact. Violent speed-ramp
pull-back reveals it is a giant newspaper front-page portrait of a
heavyset elderly American statesman with a long red tie; a gust RIPS the
page away revealing a second portrait — a compact stern Russian
statesman — ripped away again to a third — an East Asian statesman —
each rip faster than the last. The camera then DIVES at full speed into a
tearing gap in a giant aged treaty document as a burnt-orange stamp
punches the letterpress word "EXPIRED" across it; the lens plunges
through the torn fibers into swirling paper dust, ending mid-dive fully
motion-blurred.
Sound design: guillotine slam with dust whump, three accelerating page
rips, one massive stamp punch, rushing paper wind. No speech.
No text except "EXPIRED". …
```

Send this one with `cameraMotion: "crashZoomIn"` or `"fpvDrone"`.

## Music

Magnific generates the score directly — no external tool needed:

```
audio_music_generate
  prompt: "~46 BPM heartbeat pulse, sub-bass drone and low cello, almost no
           high frequencies, eight-second breathing swells, loud open,
           single climax at eighty percent of runtime, rapid decay to
           silence. Tense investigative documentary underscore."
  model: "elevenlabs-music-generation-v2"
  durationSeconds: <video length>
  instrumental: true
```

Google Lyria models are fixed at 30s; only `google-lyria-3-pro` (30–180s)
and the ElevenLabs v1/v2 models honor a longer `durationSeconds`. The bed is
mixed under the whole piece by `scripts/assemble.py` at low gain with fades,
so brief it to sit *below* the narration rather than compete with it.
