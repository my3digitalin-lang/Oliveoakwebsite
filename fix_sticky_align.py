import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove align-items:start from .svc-wrap
pattern_wrap = r'gap:120px;align-items:start;'
fix_wrap = r'gap:120px; /* align-items: stretch by default to allow sticky */'

html = re.sub(pattern_wrap, fix_wrap, html)

# Just to make absolutely sure the sticky works, let's add align-self: start to .svc-img-wrap
# Actually, if align-items is stretch, then the item stretches. Since we want it to be sticky,
# its margin box should be 640px. align-self: start forces its margin box to be exactly 640px,
# and it sticks within its grid cell.
pattern_img = r'\.svc-img-wrap\{\s*position:sticky;top:100px;'
fix_img = r'.svc-img-wrap{\n    position:sticky;top:100px; align-self: start;'

html = re.sub(pattern_img, fix_img, html)


with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed align-items in index.html")
