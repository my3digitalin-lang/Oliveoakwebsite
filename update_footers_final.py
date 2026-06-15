import re
import glob

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the <footer id="footer">...</footer> from index.html
footer_match = re.search(r'(<footer id="footer">.*?</footer>)', html, re.DOTALL)
if not footer_match:
    footer_match = re.search(r'(<footer.*?>.*?</footer>)', html, re.DOTALL)

if not footer_match:
    print("Could not find footer in index.html")
    exit()

footer_html = footer_match.group(1)

# Now go through all html files and replace their footer with this footer_html
for fpath in glob.glob('*.html'):
    if fpath == 'index.html': continue
    
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            cont = f.read()
        enc = 'utf-8'
    except UnicodeDecodeError:
        with open(fpath, 'r', encoding='utf-16') as f:
            cont = f.read()
        enc = 'utf-16'
        
    new_cont = re.sub(r'<footer.*?>.*?</footer>', footer_html, cont, flags=re.DOTALL)
    
    with open(fpath, 'w', encoding=enc) as f:
        f.write(new_cont)

print('Done replaced footers.')
