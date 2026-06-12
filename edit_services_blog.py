import sys
import re

# 1. FIX SERVICES.HTML
with open('services.html', 'r', encoding='utf-8') as f:
    services = f.read()

# I had replaced `object-fit:cover;` with `object-fit:contain;background:#130f0a;`
# Revert it for the services bento cards.
services = services.replace('object-fit:contain;background:#130f0a;', 'object-fit:cover;')
with open('services.html', 'w', encoding='utf-8') as f:
    f.write(services)


# 2. FIX BLOG.HTML
with open('blog.html', 'r', encoding='utf-8') as f:
    blog = f.read()

# Hide badges and numbers via CSS
css = """
  .mc-cat, .mc-featured-badge, .mc-num { display: none !important; }
"""
if ".mc-cat, .mc-featured-badge, .mc-num {" not in blog:
    blog = blog.replace("</style>", css + "</style>")

# The user wants "one line content under it" (excerpt) for every mosaic card.
# The original hero card has:
# <div class="mc-excerpt">From compact Gachibowli apartments to spacious Jubilee Hills villas a blend of modern lifestyles and cultural elegance.</div>
# Let's add an excerpt to cards 2, 3, 4, 5.
# Let's look for:
#         <div class="mc-title">3BHK Interior Design in Hyderabad for Modern Homes</div>
#         <div class="mc-read">Read Article  </div>

# I will just inject a dummy excerpt for the ones missing it based on their title, or I can use a generic one.
# "From compact Gachibowli apartments to spacious Jubilee Hills villas a blend of modern lifestyles and cultural elegance."
# Wait, maybe they just meant "keep the excerpt for every card, and make sure it displays on mobile".
# Let's check mobile CSS for .mc-excerpt. 

mob_css = """
  @media(max-width:768px){
    .mc-excerpt { display: block !important; -webkit-line-clamp: 2; display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; font-size: 13px !important; margin-bottom: 12px; }
  }
"""
if "@media(max-width:768px){\n    .mc-excerpt" not in blog:
    blog = blog.replace("</style>", mob_css + "</style>")

# Let's ensure every card has an excerpt.
def add_excerpt(match):
    title = match.group(1)
    if '3BHK' in title:
        excerpt = "A 3BHK home offers the perfect space for comfortable living, blending style and functionality."
    elif '2BHK' in title:
        excerpt = "2BHK interior design in Hyderabad is the perfect choice for small families and working professionals."
    elif 'Bedroom' in title:
        excerpt = "Create a serene escape with the top bedroom design trends tailored for ultimate relaxation."
    elif 'Dining' in title:
        excerpt = "Elevate your dining experience with the latest interior design ideas for modern dining rooms."
    else:
        excerpt = "Discover the latest tips and trends in interior design for your home."
    
    return f'<div class="mc-title">{title}</div>\n        <div class="mc-excerpt" style="font-family:var(--f-body);font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:12px;">{excerpt}</div>'

blog = re.sub(r'<div class="mc-title">(.*?)</div>\s*<div class="mc-read">', lambda m: add_excerpt(m) + '\n        <div class="mc-read">', blog)

# Make sure all .mc cards have an excerpt visible.
# And also the mobile CSS will ensure it's shown.

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(blog)

print("Updated services and blog pages.")
