import sys
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS
css = """
  .svc-mob-img { display: none; width: 100%; height: 220px; object-fit: cover; border-radius: 8px; margin-bottom: 16px; margin-top: -16px; }
  @media(max-width:768px){
    .svc-mob-img { display: block; }
    .svc-body { position: relative; z-index: 2; padding-top: 16px; }
  }
"""
if ".svc-mob-img {" not in content:
    content = content.replace("</style>", css + "\n</style>", 1)

images = [
    "https://images.unsplash.com/photo-1503174971373-b1f69850bded?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1600121848594-d8644e57abab?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1600210492493-0946911123ea?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1000&q=80"
]

for i in range(8):
    search_str = f'<div class="svc-item'
    
    # We find all svc-items. Wait, doing a simple replace is risky if it's the same string.
    pass

# Let's use regex to find each svc-item and insert the img inside it.
def repl(match):
    idx = int(match.group(2))
    img_tag = f'<img src="{images[idx]}" class="svc-mob-img" loading="lazy" alt="Service Image">'
    return match.group(1) + match.group(2) + '">\n            ' + img_tag + '\n' + match.group(3)

content = re.sub(r'(<div class="svc-item(?: on)?" data-i=")(\d)(">)\n(\s*)<div class="svc-body">', repl, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added mobile images to index.html.")
