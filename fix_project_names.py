import json
import re

html_file = r'c:\tmp\Oliveoakk\project.html'
json_file = r'c:\tmp\Oliveoakk\data\projects.json'

# 1. Fix project.html \n literal
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r'\n', '')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update projects.json
with open(json_file, 'r', encoding='utf-8') as f:
    projects = json.load(f)

for p in projects:
    if p['id'] == 'proj-linden-court':
        p['title'] = 'Linden Court'
    elif p['id'] == 'proj-residence-01':
        p['title'] = 'Olivara'
    elif p['id'] == 'proj-residence-02':
        p['title'] = 'The Duskwood'
    elif p['id'] == 'proj-residence-03':
        p['title'] = 'The Walnut Crest'
    elif p['id'] == 'proj-residence-04':
        p['title'] = 'The Quiet Canopy'
    
    # Also clear out technologies if it exists, or ensure it's empty so we don't get random text
    if 'technologies' in p:
        p['technologies'] = []

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(projects, f, indent=2)

print("Fixed project.html and updated projects.json")
