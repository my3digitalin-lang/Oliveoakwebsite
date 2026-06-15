import re

filepath = r'c:\tmp\Oliveoakk\project.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove hardcoded "The <em>"
html = html.replace('`The <em>${proj.title}</em>`;', 'proj.title;')

# 2. Render "Quotation" below title
# Currently: document.getElementById('dyn-cat').textContent = proj.category;
# In HTML, there is hero-left: 
# <div class="hero-left">
#   <div class="hero-eyebrow reveal" id="dyn-cat"...></div>
#   <h1 class="hero-h1" id="dyn-title">...</h1>
# </div>
# I will add `<div class="hero-quotation reveal" id="dyn-quotation" style="..."></div>` under `dyn-title`.
quotation_html = r'<h1 class="hero-h1" id="dyn-title">Linden Court</h1>\n        <div class="hero-quotation reveal" id="dyn-quotation" style="font-family:var(--f-body);font-size:14px;color:rgba(200,169,126,.9);letter-spacing:1px;margin-top:16px;"></div>'
html = html.replace('<h1 class="hero-h1" id="dyn-title">Linden Court</h1>', quotation_html)

quotation_js = r"document.getElementById('dyn-cat').textContent = proj.category;\n      document.getElementById('dyn-quotation').textContent = (proj.technologies || []).join(', ');"
html = html.replace("document.getElementById('dyn-cat').textContent = proj.category;", quotation_js)

# 3. Lighten hero overlay
# .proj-hero-overlay in project.html: Wait, let's see if it's defined in style tag or external.
# The style tag has .proj-hero-overlay.
overlay_css_old = r"background: linear-gradient(to top, var(--black) 0%, rgba(8,8,8,0.7) 40%, rgba(8,8,8,0.3) 100%);"
overlay_css_new = r"background: linear-gradient(to top, var(--black) 0%, rgba(8,8,8,0.4) 40%, rgba(8,8,8,0.1) 100%);"
html = html.replace(overlay_css_old, overlay_css_new)
# Let me also just do a regex replace in case the opacity is different.
html = re.sub(r'background:\s*linear-gradient\(to top,\s*var\(--black\)\s*0%,\s*rgba\(8,8,8,0\.[0-9]+\)\s*40%,\s*rgba\(8,8,8,0\.[0-9]+\)\s*100%\);', 
              'background: linear-gradient(to top, var(--black) 0%, rgba(8,8,8,0.3) 40%, rgba(8,8,8,0.05) 100%);', html)

# 4. Remove hardcoded paragraph text
html = re.sub(r'<p>Nothing within the home asks for attention.*?<\/p>', '', html, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

print("project.html updated.")
