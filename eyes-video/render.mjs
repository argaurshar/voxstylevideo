/**
 * Deterministic frame renderer.
 *
 * Drives eyes-video/index.html one frame at a time (the page never animates
 * on its own — it exposes renderFrame(t)), screenshots each frame and pipes the
 * PNG straight into ffmpeg. No intermediate frames touch the disk.
 *
 *   node render.mjs [--fps 30] [--out ../out/name.mp4] [--scale 1]
 */
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const here = path.dirname(fileURLToPath(import.meta.url));

const arg = (k, d) => {
  const i = process.argv.indexOf('--' + k);
  return i > -1 ? process.argv[i + 1] : d;
};

const FPS = Number(arg('fps', 30));
const SCALE = Number(arg('scale', 1));
const OUT = path.resolve(here, arg('out', '../out/give-claude-eyes-9x16.mp4'));
const FFMPEG = arg('ffmpeg', 'ffmpeg');

fs.mkdirSync(path.dirname(OUT), { recursive: true });

const browser = await chromium.launch({
  args: [
    '--force-color-profile=srgb',
    '--font-render-hinting=none',
    '--disable-font-subpixel-positioning',
    '--hide-scrollbars',
    '--disable-lcd-text'
  ]
});
const page = await browser.newPage({
  viewport: { width: 1080, height: 1920 },
  deviceScaleFactor: SCALE
});

await page.goto('file://' + path.join(here, 'index.html'), { waitUntil: 'load' });
await page.evaluate(() => window.prepare());

const DURATION = await page.evaluate(() => window.VIDEO_DURATION);
const TOTAL = Math.round(DURATION * FPS);
console.log(`rendering ${TOTAL} frames @ ${FPS}fps (${DURATION}s) -> ${OUT}`);

const ff = spawn(FFMPEG, [
  '-y',
  '-f', 'image2pipe', '-framerate', String(FPS), '-i', 'pipe:0',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
  '-an',                                  // silent by design — no audio stream at all
  '-pix_fmt', 'yuv420p',
  '-profile:v', 'high', '-level', '4.2',
  '-movflags', '+faststart',
  '-r', String(FPS),
  OUT
], { stdio: ['pipe', 'inherit', 'pipe'] });

let ffErr = '';
ff.stderr.on('data', d => { ffErr += d.toString(); if (ffErr.length > 40000) ffErr = ffErr.slice(-20000); });

const done = new Promise((res, rej) => {
  ff.on('close', code => code === 0 ? res() : rej(new Error('ffmpeg exited ' + code + '\n' + ffErr.slice(-3000))));
});

const write = buf => new Promise(res => ff.stdin.write(buf) ? res() : ff.stdin.once('drain', res));

const t0 = Date.now();
for (let f = 0; f < TOTAL; f++) {
  const t = f / FPS;
  await page.evaluate(tt => window.renderFrame(tt), t);
  await write(await page.screenshot({ type: 'png', animations: 'disabled' }));
  if (f % 60 === 0 || f === TOTAL - 1) {
    const el = (Date.now() - t0) / 1000;
    process.stdout.write(`  frame ${f + 1}/${TOTAL}  ${(el).toFixed(0)}s elapsed, ~${(el / (f + 1) * (TOTAL - f - 1)).toFixed(0)}s left\n`);
  }
}

ff.stdin.end();
await done;
await browser.close();
console.log('done ->', OUT, (fs.statSync(OUT).size / 1e6).toFixed(2) + ' MB');
