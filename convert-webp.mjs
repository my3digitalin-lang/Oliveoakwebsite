import sharp from 'sharp';
import https from 'https';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── LOCAL files to convert ──────────────────────────────────────
const LOCAL = [
  { src: 'logo.PNG',         out: 'logo.webp',         quality: 90, lossless: false },
  { src: 'imag1.jpeg',       out: 'imag1.webp',         quality: 82 },
  { src: 'imag2.jpeg',       out: 'imag2.webp',         quality: 82 },
  { src: 'imag3.jpeg',       out: 'imag3.webp',         quality: 82 },
  { src: 'imag4.jpeg',       out: 'imag4.webp',         quality: 80 },
  { src: 'bg-texture.jpg',   out: 'bg-texture.webp',    quality: 78 },
];

// ── REMOTE images still not localised ──────────────────────────
const REMOTE = [
  {
    url: 'https://oliveoak.in/wp-content/uploads/2026/01/living-room.png',
    out: 'images/living-room.webp',
    quality: 82
  },
  {
    url: 'https://oliveoak.in/wp-content/uploads/2026/01/pexels-matreding-9669483-683x1024.jpg',
    out: 'images/pexels-matreding-portrait.webp',
    quality: 82
  },
  {
    url: 'https://oliveoak.in/wp-content/uploads/2026/01/l-shaped-modular-kitchen-design-handleless-cabinets-black-glass-appliances-marble-countertops.webp',
    out: 'images/modular-kitchen-l-shaped.webp',
    quality: 82
  },
];

fs.mkdirSync(path.join(__dirname, 'images'), { recursive: true });

function download(url, redirectCount = 0) {
  return new Promise((resolve, reject) => {
    if (redirectCount > 5) return reject(new Error('Too many redirects'));
    const client = url.startsWith('https') ? https : http;
    const chunks = [];
    client.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      if ([301, 302, 307, 308].includes(res.statusCode)) {
        return download(res.headers.location, redirectCount + 1).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks)));
    }).on('error', reject);
  });
}

async function convertLocal(item) {
  const srcPath = path.join(__dirname, item.src);
  const outPath = path.join(__dirname, item.out);
  if (!fs.existsSync(srcPath)) {
    console.log(`  ⚠️  SKIP (not found): ${item.src}`);
    return null;
  }
  if (fs.existsSync(outPath)) {
    const stat = fs.statSync(outPath);
    console.log(`  SKIP (exists ${Math.round(stat.size/1024)}KB): ${item.out}`);
    return { old: item.src, new: item.out };
  }
  try {
    const srcBuf = fs.readFileSync(srcPath);
    const originalKB = Math.round(srcBuf.length / 1024);
    await sharp(srcBuf)
      .webp({ quality: item.quality || 82, effort: 5, lossless: item.lossless || false })
      .toFile(outPath);
    const newKB = Math.round(fs.statSync(outPath).size / 1024);
    const pct = Math.round((1 - newKB / originalKB) * 100);
    console.log(`  ✅ ${item.src} → ${item.out}: ${originalKB}KB → ${newKB}KB (${pct}% smaller)`);
    return { old: item.src, new: item.out };
  } catch (e) {
    console.log(`  ❌ FAILED: ${item.src} — ${e.message}`);
    return null;
  }
}

async function convertRemote(item) {
  const outPath = path.join(__dirname, item.out);
  if (fs.existsSync(outPath)) {
    const stat = fs.statSync(outPath);
    console.log(`  SKIP (exists ${Math.round(stat.size/1024)}KB): ${item.out}`);
    return { old: item.url, new: item.out };
  }
  try {
    console.log(`  ⬇️  Downloading: ${item.url.split('/').pop()}`);
    const buf = await download(item.url);
    const originalKB = Math.round(buf.length / 1024);
    await sharp(buf)
      .webp({ quality: item.quality || 82, effort: 5 })
      .toFile(outPath);
    const newKB = Math.round(fs.statSync(outPath).size / 1024);
    const pct = Math.round((1 - newKB / originalKB) * 100);
    console.log(`  ✅ ${path.basename(item.out)}: ${originalKB}KB → ${newKB}KB (${pct}% smaller)`);
    return { old: item.url, new: item.out };
  } catch (e) {
    console.log(`  ❌ FAILED: ${path.basename(item.out)} — ${e.message}`);
    return null;
  }
}

console.log('\n🖼️  Converting ALL images to WebP...\n');
console.log('── Local files ──────────────────────');
const localResults = [];
for (const item of LOCAL) { localResults.push(await convertLocal(item)); }

console.log('\n── Remote images ────────────────────');
const remoteResults = [];
for (const item of REMOTE) { remoteResults.push(await convertRemote(item)); }

// Build replacement map
const replacements = [...localResults, ...remoteResults].filter(Boolean);

console.log('\n── Updating HTML files ──────────────');
const htmlFiles = fs.readdirSync(__dirname).filter(f => f.endsWith('.html'));

for (const f of htmlFiles) {
  const filePath = path.join(__dirname, f);
  let html = fs.readFileSync(filePath, 'utf8');
  let changes = 0;
  for (const r of replacements) {
    if (html.includes(r.old)) {
      html = html.split(r.old).join(r.new);
      changes++;
    }
  }
  if (changes > 0) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`  Updated: ${f} (${changes} replacements)`);
  }
}

const ok = replacements.length;
const fail = [...localResults, ...remoteResults].filter(r => !r).length;
console.log(`\n✅ Complete! ${ok} converted, ${fail} failed.`);
console.log('📁 All images in: c:\\Oliveoakk\\images\\ and root folder');
