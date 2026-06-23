/* Recompress existing hero WebP frames smaller, WITHOUT changing frame count
   or resolution. Outputs to *-opt folders so originals stay intact for A/B. */
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

sharp.concurrency(0); // use all cores

const JOBS = [
  { in: 'Frames-webp-pc',     out: 'Frames-webp-pc-opt',     quality: 64 },
  { in: 'Frames-webp-mobile', out: 'Frames-webp-mobile-opt', quality: 62 },
];

async function run(job) {
  if (!fs.existsSync(job.out)) fs.mkdirSync(job.out);
  const files = fs.readdirSync(job.in).filter(f => f.endsWith('.webp')).sort();

  let inBytes = 0, outBytes = 0, done = 0;
  const BATCH = 24;
  for (let i = 0; i < files.length; i += BATCH) {
    await Promise.all(files.slice(i, i + BATCH).map(async f => {
      const src = path.join(job.in, f), dst = path.join(job.out, f);
      inBytes += fs.statSync(src).size;
      // smartSubsample + effort 6 = better compression at same perceived quality
      await sharp(src).webp({ quality: job.quality, effort: 6, smartSubsample: true }).toFile(dst);
      outBytes += fs.statSync(dst).size;
      done++;
      if (done % 20 === 0 || done === files.length) process.stdout.write(`\r  ${job.in}: ${done}/${files.length}`);
    }));
  }
  const saved = (1 - outBytes / inBytes) * 100;
  console.log(`\n  ${job.in}  ${(inBytes/1e6).toFixed(1)}MB -> ${(outBytes/1e6).toFixed(1)}MB  (saved ${saved.toFixed(0)}%)\n`);
}

(async () => {
  const t0 = Date.now();
  for (const job of JOBS) await run(job);
  console.log(`Done in ${((Date.now()-t0)/1000).toFixed(0)}s`);
})();
