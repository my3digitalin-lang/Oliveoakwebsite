import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace overflow:hidden with overflow:visible in #services
# The original CSS:
# #services{
#     background:transparent;
#     position:relative;overflow:hidden
#   }
pattern_services = r'#services\s*\{\s*background:transparent;\s*position:relative;\s*overflow:hidden\s*\}'
fix_services = r'''#services{
    background:transparent;
    position:relative;overflow:visible
  }'''

html = re.sub(pattern_services, fix_services, html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed #services overflow in index.html")
