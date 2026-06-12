import os
import glob
import re

HTML_DIR = r"C:\tmp\Oliveoakk"

# 1. Replace "Balcony / Kitchen" with "Kitchen" in all project-*.html files
project_files = glob.glob(os.path.join(HTML_DIR, "project-*.html"))
for pfile in project_files:
    with open(pfile, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace("Balcony / Kitchen", "Kitchen")
    if new_content != content:
        with open(pfile, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(pfile)}")

# 2. Add tabs to projects.html
projects_file = os.path.join(HTML_DIR, 'projects.html')
with open(projects_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for tabs
tabs_css = """
  <style>
  .projects-tabs {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 40px auto;
    padding: 0 24px;
  }
  .tab-btn {
    font-family: var(--f-body);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    background: transparent;
    border: 1px solid rgba(200,169,126,0.3);
    color: rgba(255,255,255,0.6);
    padding: 12px 32px;
    border-radius: 40px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  .tab-btn:hover {
    border-color: var(--gold);
    color: var(--gold);
  }
  .tab-btn.active {
    background: var(--gold);
    color: var(--bg);
    border-color: var(--gold);
  }
  </style>
</head>"""

if ".projects-tabs {" not in html:
    html = html.replace("</head>", tabs_css)

# Find the gallery section and wrap its contents
# The gallery section starts with <section class="gallery-section" id="gallerySection">
# and ends with </section><!-- /gallery-section -->

gallery_match = re.search(r'<section class="gallery-section" id="gallerySection">(.*?)</section><!-- /gallery-section -->', html, flags=re.DOTALL)
if gallery_match:
    inner = gallery_match.group(1)
    
    # We need to split inner into residential and commercial parts
    res_match = re.search(r'<h2 class="section-title">Residential Projects</h2>(.*?)<h2 class="section-title" style="margin-top: 80px;">Commercial Projects</h2>', inner, flags=re.DOTALL)
    if res_match:
        res_content = res_match.group(1)
        com_content = inner.split('<h2 class="section-title" style="margin-top: 80px;">Commercial Projects</h2>')[1]
        
        # Build the new tabbed layout
        tabbed_html = f'''
  <div class="projects-tabs">
    <button class="tab-btn active" onclick="showTab('residential')">Residential</button>
    <button class="tab-btn" onclick="showTab('commercial')">Commercial</button>
  </div>

  <div id="tab-residential">
    {res_content}
  </div>

  <div id="tab-commercial" style="display: none;">
    <div style="padding: 40px 60px 120px; color: rgba(200,169,126,0.6); font-family: var(--f-serif); font-size: 18px; font-style: italic; text-align: center;">
      Commercial projects coming soon.
    </div>
  </div>

  <script>
  function showTab(tab) {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.tab-btn[onclick="showTab(\\'' + tab + '\\')"]').classList.add('active');
    document.getElementById('tab-residential').style.display = tab === 'residential' ? 'block' : 'none';
    document.getElementById('tab-commercial').style.display = tab === 'commercial' ? 'block' : 'none';
  }}
  </script>
'''
        # Replace the entire section content
        html = html[:gallery_match.start(1)] + tabbed_html + html[gallery_match.end(1):]

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(html)
print("Tabs added to projects.html")
