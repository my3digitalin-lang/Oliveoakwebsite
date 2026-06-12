const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const INPUT_DIR  = './Frames';
const OUTPUT_DIR = './Frames-webp';
const QUALITY    = 72;          // WebP quality (72 is visually near-lossless for these)
const MAX_WIDTH  = 1920;        // cap resolution — anything wider is wasteful

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

const files = fs.readdirSync(INPUT_DIR)
  .filter(f => f.endsWith('.png'))
  .sort();

console.log(`Converting ${files.length} frames PNG → WebP (quality ${QUALITY}) …`);

let done = 0;
const BATCH = 20; // parallel workers

async function convertFile(file) {
  const src  = path.join(INPUT_DIR, file);
  const dest = path.join(OUTPUT_DIR, file.replace('.png', '.webp'));

  await sharp(src)
    .resize({ width: MAX_WIDTH, withoutEnlargement: true })
    .webp({ quality: QUALITY, effort: 4 })
    .toFile(dest);

  done++;
  if (done % 20 === 0 || done === files.length) {
    process.stdout.write(`\r  ${done}/${files.length} done`);
  }
}

// Run in batches of BATCH concurrently
(async () => {
  const t0 = Date.now();
  for (let i = 0; i < files.length; i += BATCH) {
    const batch = files.slice(i, i + BATCH).map(f => convertFile(f));
    await Promise.all(batch);
  }

  // Report size comparison
  const pngBytes  = files.reduce((s,f) => s + fs.statSync(path.join(INPUT_DIR,f)).size, 0);
  const webpFiles = fs.readdirSync(OUTPUT_DIR).filter(f => f.endsWith('.webp'));
  const webpBytes = webpFiles.reduce((s,f) => s + fs.statSync(path.join(OUTPUT_DIR,f)).size, 0);
  const saved     = (1 - webpBytes/pngBytes) * 100;

  console.log(`\n\n✅ Done in ${((Date.now()-t0)/1000).toFixed(1)}s`);
  console.log(`   PNG total : ${(pngBytes /1e6).toFixed(1)} MB`);
  console.log(`   WebP total: ${(webpBytes/1e6).toFixed(1)} MB`);
  console.log(`   Saved     : ${saved.toFixed(1)}%`);
})();
