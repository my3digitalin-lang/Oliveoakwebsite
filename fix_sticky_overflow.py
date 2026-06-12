import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
index_file = os.path.join(HTML_DIR, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace overflow-x:hidden with overflow-x:clip on html and body
# This hides horizontal overflow (caused by animations) WITHOUT breaking position:sticky!

html = re.sub(r'html\s*\{([^}]*)overflow-x:\s*hidden;([^}]*)\}', r'html{\1overflow-x:clip;\2}', html)
html = re.sub(r'body\s*\{([^}]*)overflow-x:\s*hidden;([^}]*)\}', r'body{\1overflow-x:clip;\2}', html)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Changed overflow-x:hidden to clip in index.html")
