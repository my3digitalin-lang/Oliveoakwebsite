import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update grid-template-columns to 5fr 6fr for a more balanced, elegant look
# (Image takes ~45%, text takes ~55%)
pattern_grid = r'grid-template-columns:\s*minmax\(0,\s*1fr\)\s*minmax\(0,\s*1fr\);'
fix_grid = r'grid-template-columns: 5fr 6fr;'
html = re.sub(pattern_grid, fix_grid, html)

# Just in case it's still 1fr 1fr
pattern_grid_alt = r'display:grid;grid-template-columns:1fr 1fr;'
fix_grid_alt = r'display:grid;grid-template-columns: 5fr 6fr;'
html = re.sub(pattern_grid_alt, fix_grid_alt, html)

# 2. Change the aspect-ratio to 4/5 for a more premium portrait look, instead of a squat 1:1 square
pattern_aspect = r'aspect-ratio:\s*1\s*/\s*1;'
fix_aspect = r'aspect-ratio: 4 / 5;'
html = re.sub(pattern_aspect, fix_aspect, html)

# If aspect-ratio isn't there but height:640px is:
pattern_height = r'top:100px;\s*align-self:\s*start;\s*height:640px;'
fix_height = r'top:100px; align-self: start; aspect-ratio: 4 / 5; height: auto;'
html = re.sub(pattern_height, fix_height, html)

# 3. Add max-width to the text column so the heading gracefully wraps without stretching the grid
# I will just ensure .svc-right has a max width so the text doesn't flow infinitely
pattern_right = r'\.svc-right\{padding-top:8px\}'
fix_right = r'.svc-right{padding-top:8px; max-width: 100%;}'
html = re.sub(pattern_right, fix_right, html)


with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated grid columns and image aspect ratio")
