import re
import glob
import os
import json

HTML_DIR = r"C:\tmp\Oliveoakk"
IMG_DIR = os.path.join(HTML_DIR, "images", "projects")

# The JSON from the subagent
classifications = {
  "proj1_1.webp": "WASHROOM",
  "proj1_2.webp": "BEDROOMS",
  "proj1_3.webp": "DININGROOM",
  "proj1_4.webp": "BEDROOMS",
  "proj1_5.webp": "HALL",
  "proj1_6.webp": "BALCONY/KITCHEN",
  "proj2-bathroom-1.webp": "WASHROOM",
  "proj2-bathroom-2.webp": "WASHROOM",
  "proj2-bedroom.webp": "BEDROOMS",
  "proj2-foyer.webp": "HALL",
  "proj2-kitchen.webp": "BALCONY/KITCHEN",
  "proj2_1.webp": "WASHROOM",
  "proj2_2.webp": "BEDROOMS",
  "proj2_3.webp": "BALCONY/KITCHEN",
  "proj2_4.webp": "DININGROOM",
  "proj2_5.webp": "BEDROOMS",
  "proj2_6.webp": "BALCONY/KITCHEN",
  "proj2_7.webp": "HALL",
  "proj3_1.webp": "HALL",
  "proj3_2.webp": "HALL",
  "proj3_3.webp": "BEDROOMS",
  "proj3_4.webp": "BALCONY/KITCHEN",
  "proj3_5.webp": "BEDROOMS",
  "proj3_6.webp": "DININGROOM",
  "proj3_7.webp": "BEDROOMS",
  "proj3_8.webp": "WASHROOM",
  "proj3_9.webp": "WASHROOM",
  "proj4_1.webp": "WASHROOM",
  "proj4_10.webp": "HALL",
  "proj4_2.webp": "DININGROOM",
  "proj4_3.webp": "HALL",
  "proj4_4.webp": "BALCONY/KITCHEN",
  "proj4_5.webp": "WASHROOM",
  "proj4_6.webp": "WASHROOM",
  "proj4_7.webp": "HALL",
  "proj4_8.webp": "BEDROOMS",
  "proj4_9.webp": "BEDROOMS",
  "proj5_1.webp": "BEDROOMS",
  "proj5_10.webp": "DININGROOM",
  "proj5_11.webp": "DININGROOM",
  "proj5_12.webp": "HALL",
  "proj5_2.webp": "WASHROOM",
  "proj5_3.webp": "BEDROOMS",
  "proj5_4.webp": "WASHROOM",
  "proj5_5.webp": "HALL",
  "proj5_6.webp": "BEDROOMS",
  "proj5_7.webp": "HALL",
  "proj5_8.webp": "BEDROOMS",
  "proj5_9.webp": "BALCONY/KITCHEN"
}

ORDER = ["HALL", "DININGROOM", "BEDROOMS", "BALCONY/KITCHEN", "WASHROOM"]

def sort_images_by_category(image_filenames):
    # Group images
    groups = {cat: [] for cat in ORDER}
    for img in image_filenames:
        cat = classifications.get(img)
        if cat in groups:
            groups[cat].append(img)
    
    # Flatten based on order
    sorted_imgs = []
    for cat in ORDER:
        sorted_imgs.extend(sorted(groups[cat]))
    
    # Add any unclassified ones just in case
    for img in image_filenames:
        if img not in sorted_imgs:
            sorted_imgs.append(img)
            
    return sorted_imgs

# 1. Update individual project pages
for i in range(1, 6):
    file_path = os.path.join(HTML_DIR, f'project-{i}.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    images = glob.glob(os.path.join(IMG_DIR, f"proj{i}_*.webp"))
    image_names = [os.path.basename(img) for img in images]
    
    # Special fix: For project 2, some images were uploaded with original names
    if i == 2:
        # Check if they exist in the folder and add them
        other_proj2_imgs = ['proj2-bathroom-1.webp', 'proj2-bathroom-2.webp', 'proj2-bedroom.webp', 'proj2-foyer.webp', 'proj2-kitchen.webp']
        for o in other_proj2_imgs:
            if os.path.exists(os.path.join(IMG_DIR, o)):
                image_names.append(o)

    sorted_image_names = sort_images_by_category(image_names)
    
    # Build masonry gallery
    gallery_html = '<!-- ✦✦✦ GALLERY ✦✦✦ -->\n<div class="gallery-section">\n  <div class="gallery-eyebrow reveal">Complete Project Gallery</div>\n  <div class="masonry-grid reveal">\n'
    for img_name in sorted_image_names:
        gallery_html += f'''    <div class="masonry-item">
      <img src="images/projects/{img_name}" alt="Project Image" loading="lazy">
    </div>\n'''
    gallery_html += '  </div>\n</div>\n\n  <!-- ✦✦✦ CTA ✦✦✦ -->'

    # Replace gallery section block
    pattern = r'<!--[^>]*GALLERY[^>]*-->.*?<!--[^>]*CTA[^>]*-->'
    html = re.sub(pattern, gallery_html, html, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated project-{i}.html")

# 2. Update projects.html
projects_file = os.path.join(HTML_DIR, 'projects.html')
with open(projects_file, 'r', encoding='utf-8') as f:
    html = f.read()

for i in range(1, 6):
    images = glob.glob(os.path.join(IMG_DIR, f"proj{i}_*.webp"))
    image_names = [os.path.basename(img) for img in images]
    sorted_image_names = sort_images_by_category(image_names)
    
    # Grab the first 3
    top_3 = sorted_image_names[:3]
    
    # The masonry-grid block for this project in projects.html contains 3 <a> tags
    # We need to replace the src attribute of these 3 images.
    # The safest way is to find the block for project i and replace it
    # <div class="project-header" id="label-proj{i}">...</div><div class="masonry-grid">...</div>
    
    block_pattern = fr'(<div class="project-header" id="label-proj{i}">.*?</div\s*>\s*<div class="masonry-grid">)(.*?)(</div>)'
    match = re.search(block_pattern, html, flags=re.DOTALL)
    if match:
        inner = match.group(2)
        # Find all src="images/projects/..."
        # Replace them sequentially with the top 3 images
        for j, img_name in enumerate(top_3):
            inner = re.sub(r'src="images/projects/[^"]*"', f'src="images/projects/{img_name}"', inner, count=1)
        
        new_block = match.group(1) + inner + match.group(3)
        html = html[:match.start()] + new_block + html[match.end():]

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated projects.html")
