import os
import shutil
from PIL import Image

src_dir = r"C:\Users\DELL\Downloads\COMMERCIAL"
dest_dir = r"C:\tmp\Oliveoakk\images\commercial"

os.makedirs(dest_dir, exist_ok=True)

# List all files
files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Sort files to ensure specific file is first
target_first = "WhatsApp Image 2026-06-11 at 11.16.38 PM.jpeg"

if target_first in files:
    files.remove(target_first)
    files.insert(0, target_first)

# Convert and save
converted_files = []
for idx, filename in enumerate(files):
    src_path = os.path.join(src_dir, filename)
    dest_filename = f"commercial-{idx+1}.webp"
    dest_path = os.path.join(dest_dir, dest_filename)
    
    try:
        with Image.open(src_path) as img:
            # Convert to RGB to avoid issues with transparent PNGs to JPEG/WebP
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Save as WebP
            img.save(dest_path, "WEBP", quality=85)
        converted_files.append(dest_filename)
        print(f"Converted {filename} -> {dest_filename}")
    except Exception as e:
        print(f"Failed to convert {filename}: {e}")

print("Done converting.", len(converted_files), "files created.")
