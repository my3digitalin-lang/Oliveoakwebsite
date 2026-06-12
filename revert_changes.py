import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"

# 1. Revert projects.html
projects_file = os.path.join(HTML_DIR, 'projects.html')
with open(projects_file, 'r', encoding='utf-8') as f:
    p_html = f.read()

p_html = re.sub(r'margin-top:\s*20px;', 'margin-top: 60px;', p_html)
p_html = re.sub(r'padding-top:\s*10px;', 'padding-top: 40px;', p_html)

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(p_html)


# 2. Revert index.html
index_file = os.path.join(HTML_DIR, 'index.html')
with open(index_file, 'r', encoding='utf-8') as f:
    i_html = f.read()

original_rows = '''        <!-- Top two equal cards -->
        <div class="proj-top-row">
          <div class="proj-card proj-card-top rx from-left">
            <img src="https://images.unsplash.com/photo-1631679706909-1844bbd07221?auto=format&fit=crop&w=1600&q=80" alt="The Emerald">
            <div class="proj-card-inner">
              <div class="proj-number">01 / Residential</div>
              <h3 class="proj-title">The Emerald<br>in Narsingi</h3>
              <p class="proj-location">Narsingi, Hyderabad</p>
              <a href="projects.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>
          <div class="proj-card proj-card-top rx from-right">
            <img src="https://images.unsplash.com/photo-1497366858526-0766cadbe8fa?auto=format&fit=crop&w=1200&q=80" alt="The Onyx">
            <div class="proj-card-inner">
              <div class="proj-number">02 / Commercial</div>
              <h3 class="proj-title">The Onyx,<br>Financial District</h3>
              <p class="proj-location">Financial District, Hyderabad</p>
              <a href="projects.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>
        </div>

        <!-- Bottom section: two uneven cards -->
        <div class="proj-bottom-row">
          <div class="proj-card proj-card-bot rx from-left">
            <img src="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80" alt="The Aurelia">
            <div class="proj-card-inner">
              <div class="proj-number">03 / Residential</div>
              <h3 class="proj-title">The Aurelia</h3>
              <p class="proj-location">Banjara Hills, Hyderabad</p>
              <a href="projects.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>
          <div class="proj-card proj-card-bot rx from-right">
            <img src="https://images.unsplash.com/photo-1503174971373-b1f69850bded?auto=format&fit=crop&w=1200&q=80" alt="Studio 27">
            <div class="proj-card-inner">
              <div class="proj-number">04 / Commercial</div>
              <h3 class="proj-title">Studio 27</h3>
              <p class="proj-location">Gachibowli, Hyderabad</p>
              <a href="projects.html" class="proj-link">
                View Project
                <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </a>
            </div>
          </div>
        </div>'''

# Replace whatever is in <div class="proj-top-row"> ... </div> and <div class="proj-bottom-row"> ... </div>
pattern_all = r'(<!-- Top two equal cards -->\s*<div class="proj-top-row">).*?(</div>\s*</div>\s*<!-- /proj-wrap -->)'
i_html = re.sub(pattern_all, original_rows + r'\n      \2', i_html, flags=re.DOTALL)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(i_html)

print("Reverted successfully")
