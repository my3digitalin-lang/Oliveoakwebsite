from PIL import Image, ImageFilter
import os, glob

SRC_DIR = 'Laptop'
OUT_DIR = 'Frames-webp-pc'
OUT_W   = 1920
OUT_H   = 1080
QUALITY = 90
METHOD  = 6

# Unsharp mask settings — enhances edges/textures without visible artifacts
USM_RADIUS    = 1.2   # blur radius (lower = tighter sharpening)
USM_PERCENT   = 120   # strength (100 = subtle, 150 = strong)
USM_THRESHOLD = 3     # only sharpen pixels that differ by this much (avoids noise)

old = glob.glob(os.path.join(OUT_DIR, '*.webp'))
for f in old:
    os.remove(f)
print(f'Removed {len(old)} old files.')

os.makedirs(OUT_DIR, exist_ok=True)
total_out = 0

for i in range(1, 169):
    src = os.path.join(SRC_DIR, f'ezgif-frame-{i:03d}.png')
    out = os.path.join(OUT_DIR, f'frame_{i:04d}.webp')
    if not os.path.exists(src):
        print(f'  MISSING: {src}')
        continue

    with Image.open(src) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Step 1: 4K -> 1080p LANCZOS supersampling
        img = img.resize((OUT_W, OUT_H), Image.LANCZOS)
        # Step 2: Unsharp mask — sharpens edges, lighting, textures
        img = img.filter(ImageFilter.UnsharpMask(
            radius=USM_RADIUS,
            percent=USM_PERCENT,
            threshold=USM_THRESHOLD
        ))
        # Step 3: Save high-quality WebP
        img.save(out, 'WEBP', quality=QUALITY, method=METHOD, lossless=False)
        total_out += os.path.getsize(out)

    if i % 20 == 0:
        print(f'  {i}/168 done...', flush=True)

print(f'Done! Total: {total_out/1024/1024:.1f} MB  Avg: {total_out/168/1024:.1f} KB/frame')
