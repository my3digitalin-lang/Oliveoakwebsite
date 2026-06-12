import re
import glob
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
IMG_DIR = os.path.join(HTML_DIR, "images", "projects")

descriptions = {
    1: "Some homes are built to be lived in. Others are built to be remembered. Designed with warmth, character, and a deep sense of belonging, this residence creates an atmosphere that feels familiar from the very first moment. Thoughtfully crafted spaces encourage connection, comfort, and togetherness, transforming everyday experiences into cherished memories that last for generations.",
    2: "In a world that rarely slows down, home should feel like a pause. This residence is designed to bring balance, calm, and quiet sophistication into everyday life. Through thoughtful planning, refined materials, and effortless flow, each space offers a sense of ease, allowing its residents to slow down, reconnect, and truly feel at home.",
    3: "A home should enrich not only the way you live, but the way you feel. Filled with warmth, natural light, and timeless design, this residence creates an environment that feels peaceful and uplifting. Every detail has been carefully considered to foster connection, comfort, and a deeper appreciation for the simple moments that make life meaningful.",
    4: "True luxury is not about excess—it is about intention. Crafted with meticulous attention to detail, this residence combines elegance, depth, and sophistication in every corner. Rich materials, layered textures, and refined craftsmanship create an immersive living experience that feels both distinctive and deeply personal.",
    5: "The most beautiful homes are those that live in harmony with their surroundings. Designed to embrace light, openness, and nature, this residence offers a sense of tranquility that flows throughout every space. Blurring the boundaries between indoors and outdoors, it creates an atmosphere where comfort, beauty, and everyday living come together effortlessly."
}

for i in range(1, 6):
    file_path = os.path.join(HTML_DIR, f'project-{i}.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update description
    story_body_pattern = r'<div class="story-body">.*?</div>'
    new_story_body = f'<div class="story-body">\n        <p>{descriptions[i]}</p>\n      </div>'
    html = re.sub(story_body_pattern, new_story_body, html, flags=re.DOTALL)

    # Get images
    images = glob.glob(os.path.join(IMG_DIR, f"proj{i}_*.webp"))
    # Sort them nicely (proj1_1, proj1_2, etc)
    images.sort(key=lambda x: int(re.search(r'_(\d+)\.webp', x).group(1)))
    
    # Build masonry gallery
    gallery_html = '<!-- ✦✦✦ GALLERY ✦✦✦ -->\n<div class="gallery-section">\n  <div class="gallery-eyebrow reveal">Complete Project Gallery</div>\n  <div class="masonry-grid reveal">\n'
    for img_path in images:
        img_name = os.path.basename(img_path)
        gallery_html += f'''    <div class="masonry-item">
      <img src="images/projects/{img_name}" alt="Project Image" loading="lazy">
    </div>\n'''
    gallery_html += '  </div>\n</div>\n\n  <!-- ✦✦✦ CTA ✦✦✦ -->'

    # Replace gallery section block
    pattern = r'<!--[^>]*GALLERY[^>]*-->.*?<!--[^>]*CTA[^>]*-->'
    html = re.sub(pattern, gallery_html, html, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated project-{i}.html")
