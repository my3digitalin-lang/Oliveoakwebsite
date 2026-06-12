import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix missing closing tags for Villa Serenita (and Studio 27)
# Right now it looks like:
#               <h3 class="proj-title">Villa Serenita</h3>
#               <p class="proj-location">Jubilee Hills, Hyderabad</p>
#           <div class="proj-card proj-card-bot rx from-bottom" style="transition-delay:.24s">
#             <img src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=900&q=80" alt="Studio 27">

fix_villa = r'''              <h3 class="proj-title">Villa Serenita</h3>
              <p class="proj-location">Jubilee Hills, Hyderabad</p>
              <a href="projects.html" class="proj-link">
                View Project<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>
          <div class="proj-card proj-card-bot rx from-bottom" style="transition-delay:.24s">'''

# Search for the broken version and replace it
broken_villa_pattern = r'              <h3 class="proj-title">Villa Serenita</h3>\s*<p class="proj-location">Jubilee Hills, Hyderabad</p>\s*<div class="proj-card proj-card-bot rx from-bottom" style="transition-delay:\.24s">'
html = re.sub(broken_villa_pattern, fix_villa, html)

# 2. Fix the stray `  ">` and missing `<div class="svc-body">` in the services section
# Pattern: `  ">\s*<div class="svc-name">` -> replace with `              <div class="svc-body">\n                <div class="svc-name">`
broken_svc_pattern = r'\s*">\s*<div class="svc-name">'
fix_svc = r'''
              <div class="svc-body">
                <div class="svc-name">'''

html = re.sub(broken_svc_pattern, fix_svc, html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed alignment issues in index.html")
