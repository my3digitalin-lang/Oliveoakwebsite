import os
from PIL import Image
import glob
import re

IMG_DIR = r"C:\tmp\Oliveoakk\images\projects"
HTML_DIR = r"C:\tmp\Oliveoakk"

def convert_to_webp():
    # Find all project images we just copied (proj1_*, proj2_*, etc.)
    images = glob.glob(os.path.join(IMG_DIR, "proj*.*"))
    converted_map = {} # original_name -> new_name
    
    for img_path in images:
        filename = os.path.basename(img_path)
        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # If it's already webp, skip
        if ext == '.webp':
            continue
            
        new_filename = f"{name}.webp"
        new_path = os.path.join(IMG_DIR, new_filename)
        
        try:
            with Image.open(img_path) as im:
                # Convert to RGB if it has alpha and we're saving to webp? 
                # Actually WebP supports alpha, but if image is RGBA we just save it as webp.
                im.save(new_path, "WEBP", quality=80)
            print(f"Converted {filename} -> {new_filename}")
            
            # Store mapping for HTML replacement
            converted_map[filename] = new_filename
            
            # Delete original to save space
            os.remove(img_path)
            
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
            
    # Now update HTML files
    if not converted_map:
        print("No images needed conversion.")
        return
        
    html_files = glob.glob(os.path.join(HTML_DIR, "project*.html"))
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        for old_name, new_name in converted_map.items():
            content = content.replace(f"images/projects/{old_name}", f"images/projects/{new_name}")
            
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated references in {os.path.basename(html_file)}")

if __name__ == "__main__":
    convert_to_webp()
