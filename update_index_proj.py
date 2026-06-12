import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = """        <div class="proj-card proj-card-top rx from-left">
          <img src="images/commercial/commercial-1.webp" alt="PSV PRECAST Corporate Office" loading="lazy" decoding="async">
          <div class="proj-card-inner">
            <div class="proj-number">01 / COMMERCIAL</div>
            <h3 class="proj-title">PSV PRECAST Corporate Office</h3>
            <p class="proj-location">Designed by OliveOak Interiors</p>
            <a href="projects.html" class="proj-link">
              View Project
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
            </a>
          </div>
        </div>"""

pattern = re.compile(r'<div class="proj-card proj-card-top rx from-left">.*?<img src="images/projects/proj1_5\.webp".*?</div>\s*</div>', re.DOTALL)

if pattern.search(html):
    html = pattern.sub(replacement, html, count=1)
    with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully updated index.html")
else:
    print("Pattern not found")
