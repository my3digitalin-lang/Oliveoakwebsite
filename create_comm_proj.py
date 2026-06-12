# -*- coding: utf-8 -*-
import re

# 1. Create commercial-project-1.html based on project-1.html
with open(r'c:\tmp\Oliveoakk\project-1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update meta & title
html = html.replace('Linden Court | OliveOak Interiors', 'PSV PRECAST Corporate Office | OliveOak Interiors')
html = html.replace('The Linden Court — a quiet masterpiece', 'PSV PRECAST Corporate Office — Designed to reflect commitment to strength, precision, and progress.')
html = html.replace('project-linden-court.html', 'commercial-project-1.html')

# Update hero
html = re.sub(r'src="images/projects/proj1_3\.webp"', 'src="images/commercial/commercial-1.webp"', html)
html = html.replace('The Linden Court — Living Room by OliveOak Interiors', 'PSV PRECAST Corporate Office by OliveOak Interiors')

html = html.replace('OliveOak Residences', 'OliveOak Commercial')
html = html.replace('<h1 class="hero-h1">Linden Court</h1>', '<h1 class="hero-h1" style="font-size:clamp(32px,4vw,60px);">PSV PRECAST<br><em>Corporate Office</em></h1>')

hero_sub = 'Designed to reflect PSV Precast’s commitment to strength, precision, and progress, this workspace blends functionality with refined elegance.'
html = re.sub(r'<p class="hero-sub reveal"[^>]*>.*?</p>', f'<p class="hero-sub reveal" style="transition-delay:0.3s;">{hero_sub}</p>', html, count=1, flags=re.DOTALL)

# Update Story section
html = html.replace('<h2 class="story-h2">Linden Court</h2>', '<h2 class="story-h2">PSV PRECAST</h2>')
html = re.sub(r'<blockquote class="story-quote".*?</blockquote>', 
              '<blockquote class="story-quote" style="margin-top: 32px;">"A workplace designed not just for work, but for the people shaping the future of PSV Precast."</blockquote>', 
              html, flags=re.DOTALL)

story_p = '<p>Designed to reflect PSV Precast’s commitment to strength, precision, and progress, this workspace blends functionality with refined elegance.</p><p>Thoughtfully planned work zones, warm material palettes, and biophilic elements come together to create an environment that fosters collaboration, focus, and growth. A workplace designed not just for work, but for the people shaping the future of PSV Precast.</p>'

html = re.sub(r'<div class="story-body">.*?</div>', f'<div class="story-body">{story_p}</div>', html, flags=re.DOTALL)
html = re.sub(r'</div>\s*<p>Nothing within the home asks for attention.*?</p>', '</div>', html, flags=re.DOTALL) # remove extra p

# Replace gallery grid
gallery_items = ""
for i in range(1, 11):
    gallery_items += f'''    <div class="masonry-item">
      <img src="images/commercial/commercial-{i}.webp" alt="PSV PRECAST Corporate Office" loading="lazy">
    </div>\n'''

html = re.sub(r'<div class="masonry-grid reveal">.*?</div>\s*</div>\s*<!-- ✦✦✦ CTA ✦✦✦ -->', 
              f'<div class="masonry-grid reveal">\n{gallery_items}  </div>\n</div>\n\n  <!-- ✦✦✦ CTA ✦✦✦ -->', html, flags=re.DOTALL)

with open(r'c:\tmp\Oliveoakk\commercial-project-1.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update projects.html
with open(r'c:\tmp\Oliveoakk\projects.html', 'r', encoding='utf-8') as f:
    p_html = f.read()

# Replace the bulky header with standard one
old_header = r'<div class="project-header" id="label-comm1" style="align-items: flex-start;">.*?</div>\s*</div>'
new_header = '''    <div class="project-header" id="label-comm1">
      <div class="proj-info-left">
        <span class="p-no">01</span>
        <h3 class="p-name">PSV PRECAST</h3>
        <span class="p-type">OliveOak Commercial</span>
      </div>
      <a href="commercial-project-1.html" class="btn-ghost">View Full Project</a>
    </div>'''
p_html = re.sub(old_header, new_header, p_html, flags=re.DOTALL)

# Add hrefs to the commercial masonry items
p_html = p_html.replace('<div class="masonry-item portal">', '<a class="masonry-item portal" href="commercial-project-1.html">')
p_html = re.sub(r'(<img src="images/commercial/commercial-\d+\.webp".*?>\s*)</div>', r'\1</a>', p_html)

with open(r'c:\tmp\Oliveoakk\projects.html', 'w', encoding='utf-8') as f:
    f.write(p_html)


# 3. Update index.html
with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    i_html = f.read()

i_html = i_html.replace('<a href="projects.html" class="proj-link">\n              View Project', '<a href="commercial-project-1.html" class="proj-link">\n              View Project')

with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
    f.write(i_html)

print("Created commercial-project-1.html and updated links in index.html & projects.html")
