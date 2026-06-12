import sys

with open('projects.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make card sizes same in mobile view by ensuring fixed height for .bento-item.hero
# And remove content under titles (hide .bento-room, show only .bento-project).
css_to_add = """
  /* Mobile adjustments per user request */
  .bento-room { display: none !important; }
  .bento-item.hero { height: 320px !important; min-height: unset !important; }
"""
if css_to_add not in content:
    content = content.replace("  .bento-item:not(.hero){\n    display:none !important;\n  }", "  .bento-item:not(.hero){\n    display:none !important;\n  }\n" + css_to_add)

# Change object-fit for bento images
content = content.replace(".bento-inner img{\n  width:100%;height:100%;object-fit:cover;", ".bento-inner img{\n  width:100%;height:100%;object-fit:contain;background:#130f0a;")

with open('projects.html', 'w', encoding='utf-8') as f:
    f.write(content)

# We also need to fix services.html images not to be cropped if they are grids. 
# And blog.html uses .mc img and .strip-card-img img { object-fit: cover; }
# Let's change those to object-fit: contain to be safe.
def apply_contain(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('object-fit:cover;', 'object-fit:contain;background:#130f0a;')
    html = html.replace('object-fit: cover;', 'object-fit: contain;background:#130f0a;')
    # Don't change hero-bg though
    html = html.replace('.hero-bg{\n  position:absolute;inset:0;\n  background:url(\'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1800&q=85\') center/contain;background:#130f0a; no-repeat;', '.hero-bg{\n  position:absolute;inset:0;\n  background:url(\'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1800&q=85\') center/cover no-repeat;')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

apply_contain('services.html')
apply_contain('blog.html')

print("Applied object-fit: contain to grids.")
