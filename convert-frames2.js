const sharp = require('sharp');
const fs    = require('fs');
const path  = require('path');

const OUTPUT_DIR = './Frames-webp';
const QUALITY    = 72;
const MAX_WIDTH  = 1920;
const BATCH      = 20;

// ── Two source folders ──────────────────────────────────────────
const SOURCES = [
  { dir: 'C:\\website\\frames1', offset: 0   }, // 001 – 270
  { dir: 'C:\\website\\frames2', offset: 270 }, // 271 – 360
];

// ── Output name helper ──────────────────────────────────────────
const outName = n => `ezgif-frame-${String(n).padStart(3,'0')}.webp`;

// ── Gather all jobs ─────────────────────────────────────────────
const jobs = [];
for (const { dir, offset } of SOURCES) {
  const files = fs.readdirSync(dir)
    .filter(f => /\.(png|jpe?g)$/i.test(f))
    .sort();

  files.forEach((file, idx) => {
    const frameNum = offset + idx + 1;          // 1-based
    jobs.push({
      src:  path.join(dir, file),
      dest: path.join(OUTPUT_DIR, outName(frameNum)),
      n:    frameNum,
    });
  });
}

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

console.log(`\nConverting ${jobs.length} frames → WebP (quality ${QUALITY})`);
console.log(`  frames1 : 001 – ${String(SOURCES[0].offset + fs.readdirSync(SOURCES[0].dir).filter(f=>/\.(png|jpe?g)$/i.test(f)).length).padStart(3,'0')}`);
console.log(`  frames2 : ${String(SOURCES[1].offset+1).padStart(3,'0')} – ${String(SOURCES[1].offset + fs.readdirSync(SOURCES[1].dir).filter(f=>/\.(png|jpe?g)$/i.test(f)).length).padStart(3,'0')}`);
console.log(`  output  : ${OUTPUT_DIR}\n`);

let done = 0;
const t0 = Date.now();

async function convert({ src, dest }) {
  await sharp(src)
    .resize({ width: MAX_WIDTH, withoutEnlargement: true })
    .webp({ quality: QUALITY, effort: 4 })
    .toFile(dest);
  done++;
  if (done % 20 === 0 || done === jobs.length)
    process.stdout.write(`\r  ${done}/${jobs.length} converted`);
}

(async () => {
  for (let i = 0; i < jobs.length; i += BATCH) {
    await Promise.all(jobs.slice(i, i + BATCH).map(convert));
  }

  // Size report
  const pngBytes  = jobs.reduce((s,j) => s + fs.statSync(j.src).size, 0);
  const webpBytes = jobs.reduce((s,j) => s + fs.statSync(j.dest).size, 0);
  const saved     = (1 - webpBytes / pngBytes) * 100;

  console.log(`\n\n✅ Done in ${((Date.now()-t0)/1000).toFixed(1)}s`);
  console.log(`   PNG total  : ${(pngBytes /1e6).toFixed(1)} MB`);
  console.log(`   WebP total : ${(webpBytes/1e6).toFixed(1)} MB`);
  console.log(`   Saved      : ${saved.toFixed(1)}%`);
  console.log(`\n   TOTAL = ${jobs.length}  ← update index.html`);
})();
