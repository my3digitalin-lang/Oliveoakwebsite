import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
PROJECTS_FILE = os.path.join(HTML_DIR, 'projects.html')

with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the masonry CSS to make it ultra-premium
premium_css = """
  <style>
  .section-title {
    font-family: var(--f-display);
    font-size: clamp(32px, 4vw, 56px);
    color: var(--white);
    padding: 0 60px;
    margin: 80px 0 20px;
  }
  @media(max-width: 900px) { .section-title { padding: 0 24px; } }
  
  .project-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0 60px;
    margin-top: 60px;
    margin-bottom: 32px;
    border-top: 1px solid rgba(200,169,126,0.15);
    padding-top: 40px;
  }
  @media(max-width: 900px) { 
    .project-header { 
      flex-direction: column; 
      align-items: flex-start; 
      padding: 0 24px; 
      gap: 20px;
    } 
  }

  .proj-info-left { display: flex; flex-direction: column; gap: 8px; }
  .p-no { font-family: var(--f-body); font-size: 11px; letter-spacing: 4px; color: var(--gold); }
  .p-name { font-family: var(--f-display); font-size: clamp(28px, 4vw, 42px); color: var(--white); line-height: 1.1; margin: 0; }
  .p-type { font-family: var(--f-body); font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: rgba(248,243,234,.4); }

  .masonry-grid {
    column-count: 3;
    column-gap: 24px;
    padding: 0 60px 40px;
  }
  @media(max-width: 900px) { .masonry-grid { column-count: 2; column-gap: 16px; padding: 0 24px 24px; } }
  @media(max-width: 480px) { .masonry-grid { column-count: 1; padding: 0 16px 24px; } }
  
  .masonry-item {
    break-inside: avoid;
    margin-bottom: 24px;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    background: var(--bg2);
    display: block;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  }
  @media(max-width: 900px) { .masonry-item { margin-bottom: 16px; } }

  .masonry-item img {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 4px;
    transition: transform 1.2s cubic-bezier(0.19, 1, 0.22, 1), filter 0.8s;
  }
  .masonry-item:hover img {
    transform: scale(1.05);
    filter: brightness(0.85);
  }
  .masonry-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 30px;
    background: linear-gradient(to top, rgba(8,7,6,0.95), transparent);
    color: white;
    font-family: var(--f-serif);
    font-style: italic;
    font-size: 16px;
    opacity: 0;
    transition: opacity 0.5s;
    border-radius: 0 0 4px 4px;
  }
  .masonry-item:hover .masonry-overlay {
    opacity: 1;
  }
  </style>
</head>"""

# Replace old CSS
html = re.sub(r'<style>\s*\.section-title \{.*?</style>\s*</head>', premium_css, html, flags=re.DOTALL)

# Rebuild gallery section
projects_data = [
    {"id": 1, "name": "The Linden Court"},
    {"id": 2, "name": "Olivara"},
    {"id": 3, "name": "The Duskwood"},
    {"id": 4, "name": "The Walnut Crest"},
    {"id": 5, "name": "The Quiet Canopy"},
]

new_gallery = '<section class="gallery-section" id="gallerySection">\n<h2 class="section-title">Residential Projects</h2>\n'

for p in projects_data:
    new_gallery += f'''
  <div class="project-header" id="label-proj{p['id']}">
    <div class="proj-info-left">
      <span class="p-no">0{p['id']}</span>
      <h3 class="p-name">{p['name']}</h3>
      <span class="p-type">OliveOak Residences — Hyderabad</span>
    </div>
    <a href="project-{p['id']}.html" class="btn-ghost">View Full Project</a>
  </div>
  <div class="masonry-grid">
'''
    # We use exactly 3 images so it perfectly distributes 1 per column!
    for i in range(1, 4):
        new_gallery += f'''
    <a class="masonry-item portal" href="project-{p['id']}.html">
      <img src="images/projects/proj{p['id']}_{i}.webp" alt="{p['name']}" loading="lazy">
      <div class="masonry-overlay">Explore {p['name']}</div>
    </a>
'''
    new_gallery += '  </div>\n'

new_gallery += '''
  <h2 class="section-title" style="margin-top: 80px;">Commercial Projects</h2>
  <div style="padding: 0 60px 120px; color: rgba(200,169,126,0.6); font-family: var(--f-serif); font-size: 18px; font-style: italic;">
    Coming Soon...
  </div>
</section><!-- /gallery-section -->'''

html = re.sub(r'<section class="gallery-section"[^>]*>.*?</section><!-- /gallery-section -->', new_gallery, html, flags=re.DOTALL)

with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print("Premium masonry applied.")
