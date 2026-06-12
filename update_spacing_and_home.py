import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"

# 1. Fix spacing in projects.html
projects_file = os.path.join(HTML_DIR, 'projects.html')
with open(projects_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace project-header margins
html = re.sub(r'margin-top:\s*60px;', 'margin-top: 20px;', html)
html = re.sub(r'padding-top:\s*40px;', 'padding-top: 10px;', html)

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Replace projects in index.html
index_file = os.path.join(HTML_DIR, 'index.html')
with open(index_file, 'r', encoding='utf-8') as f:
    idx_html = f.read()

# The projects section in index.html has a .proj-track that contains .proj-card items
# Let's completely replace the inner HTML of .proj-track

project_data = [
    {
        "id": 1,
        "name": "The Linden Court",
        "location": "OliveOak Residences — Hyderabad",
        "img": "images/projects/proj1_5.webp"
    },
    {
        "id": 2,
        "name": "Olivara",
        "location": "OliveOak Residences — Hyderabad",
        "img": "images/projects/proj2_7.webp"
    },
    {
        "id": 3,
        "name": "The Duskwood",
        "location": "OliveOak Residences — Hyderabad",
        "img": "images/projects/proj3_1.webp"
    },
    {
        "id": 4,
        "name": "The Walnut Crest",
        "location": "OliveOak Residences — Hyderabad",
        "img": "images/projects/proj4_10.webp"
    },
    {
        "id": 5,
        "name": "The Quiet Canopy",
        "location": "OliveOak Residences — Hyderabad",
        "img": "images/projects/proj5_12.webp"
    }
]

new_cards_html = ""
for i, p in enumerate(project_data):
    delay = i * 0.15
    new_cards_html += f'''
          <div class="proj-card rx from-bottom" style="transition-delay:{delay}s">
            <div class="proj-img-wrap">
              <img src="{p['img']}" alt="{p['name']}" loading="lazy" decoding="async">
            </div>
            <div class="proj-info">
              <h3 class="proj-title">{p['name']}</h3>
              <p class="proj-location">{p['location']}</p>
              <a href="project-{p['id']}.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>'''

# Replace the inner contents of <div class="proj-track" id="projTrack">
# Using regex to find the proj-track div and its closing tag
track_pattern = r'(<div class="proj-track"[^>]*>).*?(</div>\s*<!-- /proj-track -->)'
# Wait, index.html might not have <!-- /proj-track -->
# Let's check how the proj-track is closed.
