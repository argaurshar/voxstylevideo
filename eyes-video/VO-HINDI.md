# Hindi voiceover — give-claude-eyes-9x16

Hinglish, not pure Hindi: technical terms (transcript, frames, API) stay in
English because that is how the audience actually speaks. The video itself is
silent, so this is recorded over it.

**Runs ~21 s** against the English script's 18 s — Hindi needs roughly 15% more
time for the same content, and "739" spoken properly is *saat sau untaalis*.
To hit 18 s, drop the `पूरा local` line: it is the weakest claim in the script
and the visual already carries it.

| Time | Hindi | Roman | On screen |
|---|---|---|---|
| 0:00 | Claude सिर्फ transcript पढ़ता है। | Claude sirf transcript padhta hai. | Claude reads the transcript. |
| 0:02 | Screen पर जो है — वो नहीं दिखता। | Screen par jo hai — woh nahin dikhta. | struck through |
| 0:04 | मतलब आधी video गायब। | Matlab aadhi video gaayab. | Half the video is missing. |
| 0:06 | तो इसे आँखें दे दो। | To ise aankhein de do. | So give it eyes. |
| 0:08 | yt-dlp file लाता है, FFmpeg उसे frames में काट देता है। | yt-dlp file laata hai, FFmpeg use frames mein kaat deta hai. | the card splits into 24 frames |
| 0:11 | अब Claude frames और words — दोनों साथ पढ़ता है। | Ab Claude frames aur words — donon saath padhta hai. | scan bar stamping timestamps |
| 0:14 | 739 frames, एक ही pass में। | 739 frames, ek hi pass mein. | 739 locks |
| 0:16 | पूरा local। कोई API cost नहीं। | Poora local. Koi API cost nahin. | All local. Zero API cost. |
| 0:18 | अब उसे पूरी video दिखती है। | Ab use poori video dikhti hai. | It sees the whole video. |

## Notes

- Protect the beat at 0:08–0:11. The card splitting into its own frames is the
  only moment that *shows* the idea instead of asserting it — give it the full
  1.5 s even if the counter has to lose time.
- `कोई API cost नहीं` reads better in Hindi than a literal `zero API cost`.
- On-screen text stays English. Hindi VO over English type is standard for
  Indian reels and keeps the video usable for an English audience too. Burning
  Devanagari on screen would mean vendoring Noto Sans Devanagari — Inter has no
  Devanagari glyphs — and re-spacing the type, since Devanagari sits taller and
  needs more line-height than Latin at the same size.
