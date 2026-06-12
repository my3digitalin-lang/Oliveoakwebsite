import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix missing closing tags for Villa Serenita (and Studio 27 overlap)
pattern_villa = r'(<h3 class="proj-title">Villa Serenita</h3>\s*<p class="proj-location">Jubilee Hills, Hyderabad</p>)\s*(<div class="proj-card proj-card-bot rx from-bottom" style="transition-delay:\.24s">)'

fix_villa = r'''\1
              <a href="projects.html" class="proj-link">
                View Project<svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>
          \2'''

html = re.sub(pattern_villa, fix_villa, html)

# 2. Fix the extra </div> before Book Consultation
pattern_btn = r'</div>\s*</div>\s*<a href="#footer" class="btn btn-gold" style="margin-top:48px">'
fix_btn = r'</div>\n          <a href="#footer" class="btn btn-gold" style="margin-top:48px">'

html = re.sub(pattern_btn, fix_btn, html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed alignment issues in index.html")
