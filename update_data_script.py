import json
import os

projects_path = r'c:\tmp\Oliveoakk\data\projects.json'
blogs_path = r'c:\tmp\Oliveoakk\data\blogs.json'

if os.path.exists(projects_path):
    with open(projects_path, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    for i, p in enumerate(projects):
        if 'PSV PRECAST' in p.get('title', ''):
            p['title'] = 'PSVA Precast workspace'
        # Set order
        if 'order' not in p:
            p['order'] = i + 1
    with open(projects_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2)

if os.path.exists(blogs_path):
    with open(blogs_path, 'r', encoding='utf-8') as f:
        try:
            blogs = json.load(f)
        except:
            blogs = []
    for i, b in enumerate(blogs):
        if 'order' not in b:
            b['order'] = i + 1
    with open(blogs_path, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=2)

print("Data JSON files updated.")
