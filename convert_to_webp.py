from PIL import Image
import os, glob, time

ROOT = r"c:\Oliveoakk"
QUALITY = 82   # good balance: quality vs size
DIRS = [
    ROOT,
    os.path.join(ROOT, "images"),
    os.path.join(ROOT, "Frames"),
    os.path.join(ROOT, "framesformobile"),
]

converted = 0
skipped   = 0
saved_kb  = 0
errors    = []

def convert(src):
    global converted, skipped, saved_kb
    dst = os.path.splitext(src)[0] + ".webp"
    if os.path.exists(dst):
        skipped += 1
        return
    try:
        orig_kb = os.path.getsize(src) / 1024
        img = Image.open(src)
        # Preserve transparency for PNG
        if img.mode in ("RGBA", "LA", "PA"):
            img.save(dst, "WEBP", quality=QUALITY, method=6)
        else:
            img = img.convert("RGB")
            img.save(dst, "WEBP", quality=QUALITY, method=6)
        new_kb  = os.path.getsize(dst) / 1024
        saved_kb += (orig_kb - new_kb)
        converted += 1
        if converted % 50 == 0:
            print(f"  [{converted}] converted so far... saved {saved_kb/1024:.1f} MB")
    except Exception as e:
        errors.append((src, str(e)))

t0 = time.time()
for d in DIRS:
    if not os.path.isdir(d):
        continue
    # Only search top-level of each dir (not recursive, dirs already listed)
    for ext in ("*.jpg","*.jpeg","*.PNG","*.png","*.gif"):
        for f in glob.glob(os.path.join(d, ext)):
            convert(f)

elapsed = time.time() - t0
print(f"\n=== DONE in {elapsed:.1f}s ===")
print(f"Converted : {converted}")
print(f"Skipped   : {skipped} (already .webp exists)")
print(f"Saved     : {saved_kb/1024:.2f} MB")
print(f"Errors    : {len(errors)}")
for src, err in errors[:10]:
    print(f"  ERROR {os.path.basename(src)}: {err}")
