import os

os.makedirs(r'c:\tmp\Oliveoakk\data', exist_ok=True)
os.makedirs(r'c:\tmp\Oliveoakk\api', exist_ok=True)

with open(r'c:\tmp\Oliveoakk\data\projects.json', 'w', encoding='utf-8') as f:
    f.write('[]')

with open(r'c:\tmp\Oliveoakk\data\blogs.json', 'w', encoding='utf-8') as f:
    f.write('[]')

with open(r'c:\tmp\Oliveoakk\vercel.json', 'w', encoding='utf-8') as f:
    f.write('{\n  "version": 2\n}')

print("Created data directories and updated vercel.json")
