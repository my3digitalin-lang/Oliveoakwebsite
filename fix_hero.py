import re
import os

HTML_DIR = r"C:\tmp\Oliveoakk"

for i in range(1, 6):
    file_path = os.path.join(HTML_DIR, f'project-{i}.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the hero image src
    # Pattern looks for id="heroImg" followed by optional whitespace/newlines, then src="images/projects/..."
    html = re.sub(
        r'(id="heroImg"\s*src=")images/projects/[^"]*(")',
        f'\\g<1>images/projects/proj{i}_1.webp\\g<2>',
        html
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed hero image for project-{i}.html")
