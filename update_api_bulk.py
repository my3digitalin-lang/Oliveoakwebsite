import re
import os

projects_api = r'c:\tmp\Oliveoakk\api\projects.js'
blogs_api = r'c:\tmp\Oliveoakk\api\blogs.js'

def update_api(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if bulk array update is already supported
    if 'Array.isArray(updatedProject)' in content or 'Array.isArray(req.body)' in content:
        return

    # In the PUT block, add array bulk support
    put_regex = r"(if\s*\(req\.method\s*===\s*'PUT'\)\s*\{)(.*?)(const\s+updatedProject\s*=\s*req\.body;)"
    
    bulk_code = r"""\1\n    if (Array.isArray(req.body)) {
      const { sha } = await getFileContent(filePath);
      await updateFileContent(filePath, JSON.stringify(req.body, null, 2), `CMS: Bulk reorder`, sha);
      return res.status(200).json(req.body);
    }\n    \3"""
    
    content = re.sub(put_regex, bulk_code, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_api(projects_api)
update_api(blogs_api)

print("APIs updated to support bulk array saving.")
