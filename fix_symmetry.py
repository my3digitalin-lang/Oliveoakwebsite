import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix grid-template-columns in .svc-wrap to prevent right column from expanding due to content
pattern_wrap = r'display:grid;grid-template-columns:1fr 1fr;'
fix_wrap = r'display:grid;grid-template-columns:minmax(0, 1fr) minmax(0, 1fr);'
html = re.sub(pattern_wrap, fix_wrap, html)

# 2. Let's also slightly reduce the font size of the heading just to be safe, 
# and ensure it can wrap if needed, although minmax(0, 1fr) will force it to wrap.
# Let's reduce the max font size from 56px to 48px to look more balanced with the image.
pattern_heading = r'font-size:clamp\(36px,4vw,56px\);'
fix_heading = r'font-size:clamp(32px, 3.5vw, 48px);'
html = re.sub(pattern_heading, fix_heading, html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed grid column symmetry and heading size in index.html")
