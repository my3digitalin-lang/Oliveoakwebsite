import json
import re

def update_descriptions():
    with open(r'c:\tmp\Oliveoakk\DESCRIPTION.md', 'r', encoding='utf-8') as f:
        desc_text = f.read()

    # Parse descriptions
    blocks = re.split(r'(PROJECT 0[1-5]|COMMERCIAL\s*)', desc_text)
    
    desc_map = {}
    current_key = None
    for part in blocks:
        if part.startswith('PROJECT') or part.startswith('COMMERCIAL'):
            current_key = part.strip()
        elif current_key:
            # clean up the text
            text = part.strip()
            # If it's commercial, it has markdown bolding for the title and author, we can strip that or keep it.
            # The user provided:
            # **PSV PRECAST Corporate Office**
            # *Designed by OliveOak Interiors*
            # We can leave it as is, or strip it. Let's just keep the text clean, or let the markdown be since we render html.
            # Wait, our description renderer splits by \n and wraps in <p>. So Markdown won't be parsed, it will just show **.
            # Let's remove the ** and * for clean text.
            text = text.replace('**', '').replace('*', '')
            desc_map[current_key] = text
            current_key = None

    # Load projects.json
    json_file = r'c:\tmp\Oliveoakk\data\projects.json'
    with open(json_file, 'r', encoding='utf-8') as f:
        projects = json.load(f)

    # Map keys to project ids
    mapping = {
        'PROJECT 01': 'proj-linden-court',
        'PROJECT 02': 'proj-residence-01',
        'PROJECT 03': 'proj-residence-02',
        'PROJECT 04': 'proj-residence-03',
        'PROJECT 05': 'proj-residence-04',
        'COMMERCIAL': 'proj-psv-precast'
    }

    for p in projects:
        for k, v in mapping.items():
            if p['id'] == v and k in desc_map:
                p['description'] = desc_map[k]
                break

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

    print("Updated projects.json descriptions.")

    # Update project.html
    html_file = r'c:\tmp\Oliveoakk\project.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove the hero-sub block
    # <p class="hero-sub reveal" style="transition-delay:0.3s;">Bathed in soft natural light and wrapped in warm oak and textured stone, this home is inspired by the understated refinement of luxury residences.</p>
    html = re.sub(
        r'<p class="hero-sub reveal"[^>]*>.*?</p>',
        '',
        html,
        flags=re.DOTALL
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Removed hero-sub from project.html.")

if __name__ == '__main__':
    update_descriptions()
