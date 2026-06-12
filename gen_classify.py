import glob
import os

HTML_DIR = r"C:\tmp\Oliveoakk"
IMG_DIR = os.path.join(HTML_DIR, "images", "projects")

images = glob.glob(os.path.join(IMG_DIR, "proj*.webp"))
images.sort()

html_content = """
<html>
<head>
<style>
  body { font-family: sans-serif; background: #fff; }
  .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 20px; }
  .item { border: 1px solid #ccc; padding: 10px; text-align: center; }
  .item img { max-width: 100%; height: auto; max-height: 200px; }
  .filename { font-weight: bold; margin-top: 10px; font-size: 18px; color: red; }
</style>
</head>
<body>
  <h1>Image Classification Task</h1>
  <p>For each image below, classify it into EXACTLY ONE of these categories: <strong>HALL, DININGROOM, BEDROOMS, BALCONY/KITCHEN, WASHROOM</strong></p>
  <div class="grid">
"""

for img_path in images:
    filename = os.path.basename(img_path)
    # Use relative path so it loads correctly when opening the HTML locally
    rel_path = f"images/projects/{filename}"
    html_content += f'''
    <div class="item">
      <img src="{rel_path}">
      <div class="filename">{filename}</div>
    </div>
    '''

html_content += """
  </div>
</body>
</html>
"""

with open(os.path.join(HTML_DIR, "classify.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated classify.html with {len(images)} images.")
