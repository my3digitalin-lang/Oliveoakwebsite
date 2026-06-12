import os

def fix_object_fit():
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Revert the global replacement
            if 'object-fit: contain;background:#130f0a;' in content:
                content = content.replace('object-fit: contain;background:#130f0a;', 'object-fit: cover;')
            if 'object-fit:contain;background:#130f0a;' in content:
                content = content.replace('object-fit:contain;background:#130f0a;', 'object-fit:cover;')
            
            # For blog.html line 30, it might be explicitly written as 'img { display: block; max-width: 100%; object-fit: cover; }' now
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f"Fixed {filename}")

fix_object_fit()
