import { chromium } from 'playwright';
import path from 'node:path'; import { fileURLToPath } from 'node:url'; import fs from 'node:fs';
const here = path.dirname(fileURLToPath(import.meta.url));
const times = process.argv.slice(2).map(Number);
const outDir = process.env.PREV_DIR || '/tmp/claude-0/-home-user-voxstylevideo/c37f90cd-3de9-52cd-a4fd-5cdbf317b4f5/scratchpad/tpreview';
fs.mkdirSync(outDir, { recursive: true });
const b = await chromium.launch({args:['--force-color-profile=srgb','--font-render-hinting=none','--hide-scrollbars']});
const p = await b.newPage({ viewport:{width:1080,height:1920}, deviceScaleFactor:1 });
await p.goto('file://'+path.join(here,'index.html'),{waitUntil:'load'});
await p.evaluate(()=>window.prepare());
for (const t of times){ await p.evaluate(tt=>window.renderFrame(tt), t); await p.screenshot({path:path.join(outDir,`t${String(t).replace('.','_')}.png`)}); }
await b.close(); console.log('previews in', outDir);
