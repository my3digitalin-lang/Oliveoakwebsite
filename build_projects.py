import os
import shutil
import re
import docx

SOURCE_DIR = r"C:\Users\DELL\Downloads\oliveoak_projects"
DEST_DIR = r"C:\tmp\Oliveoakk\images\projects"
HTML_DIR = r"C:\tmp\Oliveoakk"

if not os.path.exists(DEST_DIR):
    os.makedirs(DEST_DIR)

# 1. Read descriptions
doc_path = os.path.join(SOURCE_DIR, 'DESCRIPTION.docx')
doc = docx.Document(doc_path)
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
# paragraphs are like: "PROJECT 01", "Some homes are built to be lived in...", "Designed with warmth...", etc.
# Let's extract descriptions for each project
descriptions = {}
current_proj = 0
current_text = []
for p in paragraphs:
    if p.startswith("PROJECT 0"):
        if current_proj > 0:
            descriptions[current_proj] = " ".join(current_text)
        current_proj = int(p.split()[1])
        current_text = []
    else:
        current_text.append(p)
if current_proj > 0:
    descriptions[current_proj] = " ".join(current_text)

# 2. Process folders
folders = [d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))]
folders.sort() # Should be 1. linden court, 2. Olivara, etc.

projects_data = []

for idx, folder in enumerate(folders):
    proj_id = idx + 1
    # Extract project name from folder name e.g. "1. linden court" -> "Linden Court"
    proj_name = re.sub(r'^\d+[\.\,\s]+', '', folder).title().strip()
    if proj_name.lower() == "Linden Court":
        proj_name = "The Linden Court"
    
    src_folder = os.path.join(SOURCE_DIR, folder)
    images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    images.sort()
    
    dest_images = []
    for img_idx, img in enumerate(images):
        ext = os.path.splitext(img)[1].lower()
        new_name = f"proj{proj_id}_{img_idx+1}{ext}"
        shutil.copy(os.path.join(src_folder, img), os.path.join(DEST_DIR, new_name))
        dest_images.append(f"images/projects/{new_name}")
    
    projects_data.append({
        'id': proj_id,
        'name': proj_name,
        'desc': descriptions.get(proj_id, "A beautiful residential project by OliveOak Interiors."),
        'images': dest_images
    })

# 3. Generate individual project pages
with open(os.path.join(HTML_DIR, 'project-linden-court.html'), 'r', encoding='utf-8') as f:
    template_html = f.read()

# We'll replace the hero, title, desc, and gallery.
for p in projects_data:
    page_html = template_html
    
    # Replace title
    page_html = re.sub(r'<title>.*?</title>', f'<title>{p["name"]} | OliveOak Interiors</title>', page_html)
    page_html = re.sub(r'<h1 class="hero-h1[^>]*>.*?</h1>', f'<h1 class="hero-h1">{p["name"]}</h1>', page_html, flags=re.DOTALL)
    page_html = re.sub(r'<span class="hero-eyebrow[^>]*>.*?</span>', f'<span class="hero-eyebrow">Project 0{p["id"]}</span>', page_html, flags=re.DOTALL)
    
    # Replace hero img
    if p['images']:
        page_html = re.sub(r'<img src="images/projects/[^"]*"[^>]*class="proj-hero-img"[^>]*>', f'<img src="{p["images"][0]}" class="proj-hero-img" alt="{p["name"]}">', page_html)
        # There's another img tag in proj-hero-img? Wait, the template has:
        page_html = re.sub(r'class="proj-hero-img"\s*src="images/projects/[^"]*"', f'class="proj-hero-img" src="{p["images"][0]}"', page_html)
    
    # Replace description in story
    story_h2 = f'<h2 class="story-h2">{p["name"]}</h2>'
    page_html = re.sub(r'<h2 class="story-h2">.*?</h2>', story_h2, page_html, flags=re.DOTALL)
    
    # Story body p
    story_body = f'<div class="story-body">\n        <p>{p["desc"]}</p>\n      </div>'
    page_html = re.sub(r'<div class="story-body">.*?</div>', story_body, page_html, flags=re.DOTALL)
    
    # Gallery grid replacement using Masonry CSS
    gallery_html = '<div class="masonry-grid">\n'
    for img in p['images']:
        gallery_html += f'''      <div class="masonry-item">
        <img src="{img}" alt="{p['name']} Image" loading="lazy">
      </div>\n'''
    gallery_html += '    </div>'
    
    page_html = re.sub(r'<div class="gallery-grid">.*?</div>\s*<!-- Bottom row.*?</div>', gallery_html, page_html, flags=re.DOTALL)
    page_html = re.sub(r'<div class="gallery-grid">.*?</div>', gallery_html, page_html, flags=re.DOTALL)
    
    # Add masonry CSS to the head
    masonry_css = """
  <style>
  .masonry-grid {
    column-count: 3;
    column-gap: 16px;
  }
  .masonry-item {
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
  }
  @media (max-width: 900px) { .masonry-grid { column-count: 2; } }
  @media (max-width: 480px) { .masonry-grid { column-count: 1; } }
  </style>
</head>"""
    if ".masonry-grid {" not in page_html:
        page_html = page_html.replace('</head>', masonry_css)
        
    with open(os.path.join(HTML_DIR, f'project-{p["id"]}.html'), 'w', encoding='utf-8') as f:
        f.write(page_html)

# 4. Generate new projects.html
with open(os.path.join(HTML_DIR, 'projects.html'), 'r', encoding='utf-8') as f:
    projects_page = f.read()

# Add Masonry CSS for projects.html
proj_masonry_css = """
  <style>
  .section-title {
    font-family: var(--f-display);
    font-size: clamp(32px, 4vw, 56px);
    color: var(--white);
    padding: 0 60px;
    margin: 60px 0 20px;
  }
  @media(max-width: 900px) { .section-title { padding: 0 24px; } }
  
  .masonry-grid {
    column-count: 3;
    column-gap: 16px;
    padding: 0 60px 40px;
  }
  @media(max-width: 900px) { .masonry-grid { column-count: 2; padding: 0 24px 24px; } }
  @media(max-width: 480px) { .masonry-grid { column-count: 1; padding: 0 16px 24px; } }
  
  .masonry-item {
    break-inside: avoid;
    margin-bottom: 16px;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    background: var(--bg2);
    display: block;
  }
  .masonry-item img {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 12px;
    transition: transform 1s ease, filter 0.5s;
  }
  .masonry-item:hover img {
    transform: scale(1.04);
    filter: brightness(0.8);
  }
  .masonry-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 24px;
    background: linear-gradient(to top, rgba(8,7,6,0.9), transparent);
    color: white;
    font-family: var(--f-body);
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.4s;
    border-radius: 0 0 12px 12px;
  }
  .masonry-item:hover .masonry-overlay {
    opacity: 1;
  }
  .cta-cell {
    background: var(--bg2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
    text-align: center;
    border-radius: 12px;
    border: 1px solid rgba(200,169,126,.1);
    color: var(--gold);
    text-decoration: none;
    transition: background 0.3s;
    height: 100%;
    min-height: 200px;
  }
  .cta-cell:hover {
    background: rgba(200,169,126,.05);
  }
  .cta-cell-name { font-family: var(--f-display); font-size: 24px; color: var(--white); margin: 12px 0; }
  .cta-cell-link { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; display: flex; align-items: center; gap: 8px; }
  </style>
</head>"""

if ".masonry-grid {" not in projects_page:
    projects_page = projects_page.replace('</head>', proj_masonry_css)

# Generate Residential Section HTML
residential_html = '<h2 class="section-title">Residential Projects</h2>\n'
for p in projects_data:
    residential_html += f'''
  <div class="project-label" id="label-proj{p['id']}">
    <span class="project-label-no">0{p['id']}</span>
    <span class="project-label-name">{p['name']}</span>
    <span class="project-label-type">OliveOak Residences — Hyderabad</span>
  </div>
  <div class="masonry-grid">
'''
    # Show first 4 images + 1 CTA card
    display_images = p['images'][:4]
    for img in display_images:
        residential_html += f'''
    <a class="masonry-item portal" href="project-{p['id']}.html">
      <img src="{img}" alt="{p['name']}" loading="lazy">
      <div class="masonry-overlay">View {p['name']}</div>
    </a>
'''
    residential_html += f'''
    <div class="masonry-item" style="display:flex;height:100%;min-height:200px;">
      <a class="cta-cell portal" href="project-{p['id']}.html" style="flex:1;">
        <span class="cta-cell-name">{p['name']}</span>
        <span class="cta-cell-link">
          View Full Project
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        </span>
      </a>
    </div>
  </div>
'''

commercial_html = '''
  <h2 class="section-title">Commercial Projects</h2>
  <div style="padding: 0 60px 100px; color: rgba(255,255,255,0.5); font-family: var(--f-body); font-size: 14px;">
    Coming Soon.
  </div>
'''

# Replace gallery section
gallery_section_pattern = re.compile(r'<section class="gallery-section"[^>]*>.*?</section><!-- /gallery-section -->', re.DOTALL)
projects_page = gallery_section_pattern.sub(f'<section class="gallery-section" id="gallerySection">\n{residential_html}\n{commercial_html}\n</section><!-- /gallery-section -->', projects_page)

with open(os.path.join(HTML_DIR, 'projects.html'), 'w', encoding='utf-8') as f:
    f.write(projects_page)

print("Build complete.")
