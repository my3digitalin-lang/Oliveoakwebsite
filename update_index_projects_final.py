import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

project_data = [
    {
        "id": 1,
        "name": "The Linden Court",
        "type": "RESIDENTIAL",
        "location": "OliveOak Residences, Hyderabad",
        "img": "images/projects/proj1_5.webp"
    },
    {
        "id": 2,
        "name": "Olivara",
        "type": "RESIDENTIAL",
        "location": "OliveOak Residences, Hyderabad",
        "img": "images/projects/proj2_7.webp"
    },
    {
        "id": 3,
        "name": "The Duskwood",
        "type": "RESIDENTIAL",
        "location": "OliveOak Residences, Hyderabad",
        "img": "images/projects/proj3_1.webp"
    },
    {
        "id": 4,
        "name": "The Walnut Crest",
        "type": "RESIDENTIAL",
        "location": "OliveOak Residences, Hyderabad",
        "img": "images/projects/proj4_10.webp"
    },
    {
        "id": 5,
        "name": "The Quiet Canopy",
        "type": "RESIDENTIAL",
        "location": "OliveOak Residences, Hyderabad",
        "img": "images/projects/proj5_12.webp"
    }
]

top_row = ""
for i, p in enumerate(project_data[:2]):
    cl = "from-left" if i==0 else "from-right"
    top_row += f'''
          <div class="proj-card proj-card-top rx {cl}">
            <img src="{p['img']}" alt="{p['name']}" loading="lazy" decoding="async">
            <div class="proj-card-inner">
              <div class="proj-number">0{p['id']} / {p['type']}</div>
              <h3 class="proj-title">{p['name']}</h3>
              <p class="proj-location">{p['location']}</p>
              <a href="project-{p['id']}.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>'''

bottom_row = ""
for i, p in enumerate(project_data[2:]):
    bottom_row += f'''
          <div class="proj-card proj-card-bot rx from-bottom" style="transition-delay:{i*0.15}s">
            <img src="{p['img']}" alt="{p['name']}" loading="lazy" decoding="async">
            <div class="proj-card-inner">
              <div class="proj-number">0{p['id']} / {p['type']}</div>
              <h3 class="proj-title">{p['name']}</h3>
              <p class="proj-location">{p['location']}</p>
              <a href="project-{p['id']}.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>'''

# Replace the inner contents of <div class="proj-top-row"> ... </div>
pattern_top = r'(<div class="proj-top-row">).*?(</div>\s*<!-- Bottom section:)'
html = re.sub(pattern_top, r'\1' + top_row + r'\n        \2', html, flags=re.DOTALL)

pattern_bot = r'(<div class="proj-bottom-row">).*?(</div>\s*</div>\s*<!-- /proj-wrap -->)'
html = re.sub(pattern_bot, r'\1' + bottom_row + r'\n        \2', html, flags=re.DOTALL)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html projects again")
