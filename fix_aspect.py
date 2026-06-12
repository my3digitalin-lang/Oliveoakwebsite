import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace height:640px with aspect-ratio: 1 / 1; height: auto;
pattern_img = r'\.svc-img-wrap\{\s*position:sticky;top:100px;\s*align-self:\s*start;\s*height:640px;'
fix_img = r'.svc-img-wrap{\n    position:sticky;top:100px; align-self: start;\n    aspect-ratio: 1 / 1; height: auto;'
html = re.sub(pattern_img, fix_img, html)

# Just in case the previous script's align-self wasn't formatted exactly like that:
# Let's use a more robust regex that catches it regardless of align-self
pattern_img2 = r'\.svc-img-wrap\{([^}]*?)height:\s*640px;'
fix_img2 = r'.svc-img-wrap{\g<1>aspect-ratio: 1 / 1; height: auto;'
html = re.sub(pattern_img2, fix_img2, html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed image aspect ratio in index.html")
