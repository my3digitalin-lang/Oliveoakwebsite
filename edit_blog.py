import sys

with open('blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make mosaic cards equal size
content = content.replace(
    "grid-template-columns: 2fr 1fr 1fr;",
    "grid-template-columns: repeat(3, 1fr);"
)
content = content.replace(
    "grid-template-rows: 260px 220px;",
    "grid-template-rows: 240px 240px;"
)
content = content.replace(
    "grid-template-columns: 1fr 1fr;\n    grid-template-rows: 280px 220px 220px;",
    "grid-template-columns: 1fr 1fr;\n    grid-auto-rows: 240px;"
)

# Remove .mc-featured overrides
content = content.replace(".mc-featured { grid-column: 1; grid-row: 1 / span 2; }", "/* .mc-featured grid removed */")
content = content.replace(".mc-featured .mc-title { font-size: 21px; }", "/* .mc-featured title size removed */")
content = content.replace(".mc-featured { grid-column: 1 / span 2; grid-row: 1; }", "/* .mc-featured grid removed */")
content = content.replace(".mc-featured .mc-title { font-size: 18px; }", "/* .mc-featured title size removed */")
content = content.replace(".mc-featured { min-height: 260px; }", ".mc-featured { min-height: 220px; }")
content = content.replace(".mc-featured .mc-title { font-size: 16px; }", "/* .mc-featured title size removed */")
content = content.replace(".mc-featured { min-height: 230px; }", ".mc-featured { min-height: 200px; }")
content = content.replace(".mc-featured .mc-title { font-size: 15px; }", "/* .mc-featured title size removed */")

# Remove category and date from strip cards in blog.html
content = content.replace('<div class="strip-card-cat">Decoration</div>', '')
content = content.replace('<div class="strip-card-date">January 29, 2026</div>', '')
content = content.replace('<div class="strip-card-cat">Kitchen</div>', '')
content = content.replace('<div class="strip-card-cat">Renovation</div>', '')
# Dynamic generation part in blog.html
content = content.replace('<div class="strip-card-cat">${d.category || \'Blog\'}</div>', '')
content = content.replace('<div class="strip-card-date">${d.date || \'\'}</div>', '')

# Remove date and cat from mosaic cards if they exist
content = content.replace('<div class="mc-cat">', '<div class="mc-cat" style="display:none">')
content = content.replace('<div class="mc-date">', '<div class="mc-date" style="display:none">')
content = content.replace('<div class="mc-featured-badge">', '<div class="mc-featured-badge" style="display:none">')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('admin.html', 'r', encoding='utf-8') as f:
    admin_content = f.read()

admin_content = admin_content.replace('<div class="strip-card-cat">${blog.category}</div>', '')
admin_content = admin_content.replace('<div class="strip-card-date">${blog.date}</div>', '')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_content)

print("Updates applied successfully.")
