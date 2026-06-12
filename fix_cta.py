import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_cta = """        <div style="margin-top: 50px;">
          <a href="#footer" class="btn-outline" style="display:inline-flex; align-items:center; gap:8px;">
            Book Consultation
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
          </a>
        </div>"""

good_cta = """        <div style="margin-top: 40px; padding-bottom: 50px;">
          <a href="#footer" class="btn btn-ghost" style="display:inline-flex; align-items:center; gap:8px;">
            Book Consultation
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
          </a>
        </div>"""

count = html.count(bad_cta)
print(f"Found {count} instances of bad_cta")

if count > 0:
    # replace first instance (services section)
    html = html.replace(bad_cta, good_cta, 1)

    # replace any remaining instances with empty string (projects section mistake)
    if count > 1:
        html = html.replace(bad_cta, '')

    with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed CTA")
else:
    print("Could not find exact bad_cta")
