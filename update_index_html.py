import re

filepath = r'c:\tmp\Oliveoakk\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Desktop Services: object-fit contain
# .svc-img { width:100%;height:100%;object-fit:cover; ... }
html = re.sub(r'(\.svc-img\{[^\}]*?object-fit:)cover(;[^\}]*\})', r'\1contain\2', html)
html = html.replace('.svc-img{\n\n  position:absolute;inset:0;\n\n  width:100%;height:100%;object-fit:cover;', 
                    '.svc-img{\n\n  position:absolute;inset:0;\n\n  width:100%;height:100%;object-fit:contain;padding:24px;')

# 2. Desktop Projects: show only title and TEV logo
# Instead of doing complex regex, I will match the inner wrapper of proj-card
# <div class="proj-card-inner">
#   <div class="proj-number">01</div>
#   <div class="proj-title">The Linden Court</div>
#   <div class="proj-location">Banjara Hills, Hyderabad</div>
#   <div class="proj-link">View Project →</div>
# </div>
# I will use re.sub to replace everything inside .proj-card-inner with logo + title.
def replace_card_inner(match):
    inner = match.group(1)
    title_match = re.search(r'<div class="proj-title">(.*?)</div>', inner)
    if title_match:
        title = title_match.group(1)
        # Check if the title is PSV PRECAST, replace it
        if 'PSV PRECAST' in title:
            title = 'PSVA Precast workspace'
        
        # Build new inner HTML
        new_inner = f'\n  <img src="logo.webp" alt="TEV" style="height:32px; width:auto; margin-bottom:12px; object-fit:contain; object-position:left;">\n  <div class="proj-title">{title}</div>\n'
        return f'<div class="proj-card-inner">{new_inner}</div>'
    return match.group(0)

html = re.sub(r'<div class="proj-card-inner">(.*?)</div>', replace_card_inner, html, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated.")
