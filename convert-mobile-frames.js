const sharp = require('sharp');
const fs    = require('fs');
const path  = require('path');

const SOURCE_DIR = './framesformobile';
const OUTPUT_DIR = './Frames-webp-mobile';
const QUALITY    = 72;
const MAX_WIDTH  = 768;   // mobile — narrower than desktop 1920
const BATCH      = 20;

const outName = n => `ezgif-frame-${String(n).padStart(3,'0')}.webp`;

const files = fs.readdirSync(SOURCE_DIR)
  .filter(f => /\.(png|jpe?g)$/i.test(f))
  .sort();

const jobs = files.map((file, idx) => ({
  src:  path.join(SOURCE_DIR, file),
  dest: path.join(OUTPUT_DIR, outName(idx + 1)),
  n:    idx + 1,
}));

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

console.log(`\nConverting ${jobs.length} mobile frames → WebP (quality ${QUALITY}, max ${MAX_WIDTH}px wide)`);
console.log(`  source : ${SOURCE_DIR}`);
console.log(`  output : ${OUTPUT_DIR}\n`);

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

  const pngBytes  = jobs.reduce((s,j) => s + fs.statSync(j.src).size, 0);
  const webpBytes = jobs.reduce((s,j) => s + fs.statSync(j.dest).size, 0);
  const saved     = (1 - webpBytes / pngBytes) * 100;

  console.log(`\n\n✅ Done in ${((Date.now()-t0)/1000).toFixed(1)}s`);
  console.log(`   PNG total  : ${(pngBytes /1e6).toFixed(1)} MB`);
  console.log(`   WebP total : ${(webpBytes/1e6).toFixed(1)} MB`);
  console.log(`   Saved      : ${saved.toFixed(1)}%`);
  console.log(`\n   TOTAL = ${jobs.length} mobile frames ready`);
})();
