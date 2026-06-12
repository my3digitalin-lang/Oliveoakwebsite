import re
import glob
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
IMG_DIR = os.path.join(HTML_DIR, "images", "projects")

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
    groups = {cat: [] for cat in ORDER}
    for img in image_filenames:
        cat = classifications.get(img)
        if cat in groups:
            groups[cat].append(img)
    
    sorted_imgs = []
    for cat in ORDER:
        sorted_imgs.extend(sorted(groups[cat]))
    
    for img in image_filenames:
        if img not in sorted_imgs:
            sorted_imgs.append(img)
            
    return sorted_imgs

# 1. Fix duplicates in projects.html
projects_file = os.path.join(HTML_DIR, 'projects.html')
with open(projects_file, 'r', encoding='utf-8') as f:
    html = f.read()

project_names = {
    1: "The Linden Court",
    2: "Olivara",
    3: "The Duskwood",
    4: "The Walnut Crest",
    5: "The Quiet Canopy"
}

for i in range(1, 6):
    images = glob.glob(os.path.join(IMG_DIR, f"proj{i}_*.webp"))
    image_names = [os.path.basename(img) for img in images]
    if i == 2:
        other_proj2_imgs = ['proj2-bathroom-1.webp', 'proj2-bathroom-2.webp', 'proj2-bedroom.webp', 'proj2-foyer.webp', 'proj2-kitchen.webp']
        for o in other_proj2_imgs:
            if os.path.exists(os.path.join(IMG_DIR, o)):
                image_names.append(o)
                
    sorted_image_names = sort_images_by_category(image_names)
    top_3 = sorted_image_names[:3]
    
    block_pattern = fr'(<div class="project-header" id="label-proj{i}">.*?</div\s*>\s*<div class="masonry-grid">)(.*?)(</div>)'
    match = re.search(block_pattern, html, flags=re.DOTALL)
    if match:
        new_inner = ""
        for img_name in top_3:
            new_inner += f'''
    <a class="masonry-item portal" href="project-{i}.html">
      <img src="images/projects/{img_name}" alt="{project_names[i]}" loading="lazy">
      <div class="masonry-overlay">Explore {project_names[i]}</div>
    </a>
'''
        new_block = match.group(1) + new_inner + "  " + match.group(3)
        html = html[:match.start()] + new_block + html[match.end():]

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(html)
print("projects.html fixed.")

# 2. Add animation CSS to project pages
for i in range(1, 6):
    file_path = os.path.join(HTML_DIR, f'project-{i}.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        p_html = f.read()

    # Find masonry CSS and update it
    old_css = """.masonry-item {
      break-inside: avoid;
      margin-bottom: 16px;
      border-radius: 12px;
      overflow: hidden;
    }
    .masonry-item img {
      width: 100%;
      height: auto;
      display: block;
      border-radius: 12px;
    }"""
    
    new_css = """.masonry-item {
      break-inside: avoid;
      margin-bottom: 16px;
      border-radius: 12px;
      overflow: hidden;
      position: relative;
    }
    .masonry-item img {
      width: 100%;
      height: auto;
      display: block;
      border-radius: 12px;
      transition: transform 1.2s cubic-bezier(0.19, 1, 0.22, 1), filter 0.8s;
    }
    .masonry-item:hover img {
      transform: scale(1.05);
      filter: brightness(0.85);
    }"""
    
    if "transition: transform" not in p_html:
        p_html = p_html.replace(old_css, new_css)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(p_html)
        print(f"Added animation to project-{i}.html")
