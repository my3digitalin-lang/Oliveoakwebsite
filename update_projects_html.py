import re

filepath = r'c:\tmp\Oliveoakk\projects.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Change background to pure black
# There is likely an element with `background: var(--bg3)` or similar. Or `#080706`.
html = html.replace('background:var(--bg3)', 'background:#000')
html = html.replace('background: var(--bg3)', 'background: #000')
html = re.sub(r'body\s*\{.*?(background:\s*var\(--bg.*?;|background:\s*#[a-f0-9]+;).*?\}', lambda m: m.group(0).replace(m.group(1), 'background:#000;'), html)

# Let's also check inline styles or specific IDs like `<body style="background: ...">` or `#projects { background: ... }`
html = html.replace('background:var(--bg)', 'background:#000')

# 2. Sort projects by order
# In projects.html JS fetch:
sort_by_order = r"""
      residential.sort((a,b) => (a.order||0) - (b.order||0));
      commercial.sort((a,b) => (a.order||0) - (b.order||0));
      architecture.sort((a,b) => (a.order||0) - (b.order||0));
"""

if "residential.sort" not in html:
    # Find where residential is assigned
    html = re.sub(r"(const commercial = projects\.filter\(p => p\.category === 'Commercial'\);)", 
                  r"\1" + "\n" + sort_by_order, html)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

print("projects.html updated.")
