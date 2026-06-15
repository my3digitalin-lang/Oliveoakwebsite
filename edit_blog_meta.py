import re

file_path = r'c:\tmp\Oliveoakk\blog.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add .mc-meta to CSS if not present
if '.mc-meta {' not in content:
    content = content.replace('.mc-excerpt {', '.mc-meta {\n  font-family: var(--f-body);\n  font-size: 10px;\n  letter-spacing: 1.5px;\n  text-transform: uppercase;\n  color: rgba(200,169,126,.8);\n  margin-top: 10px;\n  margin-bottom: 12px;\n}\n.mc-excerpt {')

# Replacements mapping excerpt to new meta data
replacements = [
    (
        '<div class="mc-excerpt">From compact Gachibowli apartments to spacious Jubilee Hills villas   a blend of modern lifestyles and cultural elegance.</div>',
        '<div class="mc-meta">Interior Design • February 5, 2026</div>'
    ),
    (
        '<div class="mc-excerpt" style="font-family:var(--f-body);font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:12px;">A 3BHK home offers the perfect space for comfortable living, blending style and functionality.</div>',
        '<div class="mc-meta">Living Room • January 30, 2026</div>'
    ),
    (
        '<div class="mc-excerpt" style="font-family:var(--f-body);font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:12px;">2BHK interior design in Hyderabad is the perfect choice for small families and working professionals.</div>',
        '<div class="mc-meta">2BHK • January 30, 2026</div>'
    ),
    (
        '<div class="mc-excerpt" style="font-family:var(--f-body);font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:12px;">Create a serene escape with the top bedroom design trends tailored for ultimate relaxation.</div>',
        '<div class="mc-meta">Bedroom • January 30, 2026</div>'
    ),
    (
        '<div class="mc-excerpt" style="font-family:var(--f-body);font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:12px;">Elevate your dining experience with the latest interior design ideas for modern dining rooms.</div>',
        '<div class="mc-meta">Dining Room • January 30, 2026</div>'
    ),
    (
        '<div class="mc-excerpt" style="font-family:var(--f-body);font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:12px;">Discover the best home interior decoration ideas to elevate your living space beautifully.</div>',
        '<div class="mc-meta">Decoration • January 30, 2026</div>'
    )
]

for old, new in replacements:
    content = content.replace(old, new)

# Also remove display:none from mc-date if the user wants it? No, we combined date into mc-meta, so we can leave mc-date hidden or remove it.
# Let's remove mc-date to keep DOM clean.
content = re.sub(r'<div class="mc-date"[^>]*>.*?</div>\s*', '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Blog cards updated successfully!")
