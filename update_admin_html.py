import re

filepath = r'c:\tmp\Oliveoakk\admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Change sorting from updatedAt to order
html = html.replace('.sort((a,b)=>new Date(b.updatedAt)-new Date(a.updatedAt))', '.sort((a,b)=>(a.order||0)-(b.order||0))')

# 2. Add drag and drop attributes to renderProjects
# Original: tb.innerHTML = dataCache.projects.sort(...).map(p => `
#             <tr>
html = re.sub(
    r'(tb\.innerHTML = dataCache\.projects.*?\.map\()p => `\s*<tr>',
    r'\1(p, i) => `\n    <tr draggable="true" ondragstart="dragStart(event, \'project\', i)" ondragover="dragOver(event)" ondrop="drop(event, \'project\', i)" style="cursor:grab">',
    html
)

# 3. Add drag and drop attributes to renderBlogs
html = re.sub(
    r'(tb\.innerHTML = dataCache\.blogs.*?\.map\()b => `\s*<tr>',
    r'\1(b, i) => `\n    <tr draggable="true" ondragstart="dragStart(event, \'blog\', i)" ondragover="dragOver(event)" ondrop="drop(event, \'blog\', i)" style="cursor:grab">',
    html
)

# 4. Change "Technologies" to "Quotation"
html = html.replace('Technologies (Comma separated)', 'Quotation (Sub-title)')

# 5. Add SEO fields to blogs
blog_excerpt_html = r"""<div class="form-row">
        <div class="form-group">
          <label class="form-label">SEO Meta Title</label>
          <input type="text" class="form-input" id="blog-meta-title" placeholder="Optional">
        </div>
        <div class="form-group">
          <label class="form-label">SEO Meta Description</label>
          <input type="text" class="form-input" id="blog-meta-desc" placeholder="Optional">
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Excerpt (Short summary)</label>"""
html = html.replace('<div class="form-group">\n        <label class="form-label">Excerpt (Short summary)</label>', blog_excerpt_html)

# 6. Update resetBlogForm
reset_blog_js = r"""document.getElementById('blog-excerpt').value = '';
  document.getElementById('blog-meta-title').value = '';
  document.getElementById('blog-meta-desc').value = '';"""
html = html.replace("document.getElementById('blog-excerpt').value = '';", reset_blog_js)

# 7. Update editBlog
edit_blog_js = r"""document.getElementById('blog-excerpt').value = b.excerpt || '';
  document.getElementById('blog-meta-title').value = b.metaTitle || '';
  document.getElementById('blog-meta-desc').value = b.metaDescription || '';"""
html = html.replace("document.getElementById('blog-excerpt').value = b.excerpt || '';", edit_blog_js)

# 8. Update saveBlog
save_blog_js = r"""excerpt: document.getElementById('blog-excerpt').value,
    metaTitle: document.getElementById('blog-meta-title').value,
    metaDescription: document.getElementById('blog-meta-desc').value,"""
html = html.replace("excerpt: document.getElementById('blog-excerpt').value,", save_blog_js)

# 9. Add drag and drop JS functions
dnd_js = r"""
// ===== DRAG AND DROP =====
let draggedItem = null;
function dragStart(e, type, index) {
  draggedItem = { type, index };
  e.dataTransfer.effectAllowed = "move";
}
function dragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = "move";
}
async function drop(e, type, index) {
  e.preventDefault();
  if (!draggedItem || draggedItem.type !== type || draggedItem.index === index) return;
  
  const arr = type === 'project' ? dataCache.projects : dataCache.blogs;
  
  // Need to ensure array is currently sorted by order to match visual index
  arr.sort((a,b)=>(a.order||0)-(b.order||0));
  
  const item = arr.splice(draggedItem.index, 1)[0];
  arr.splice(index, 0, item);
  
  arr.forEach((x, i) => x.order = i + 1);
  
  if (type === 'project') renderProjects(); else renderBlogs();
  
  try {
    showToast('Saving new order...', 'info');
    await apiCall(type === 'project' ? 'projects' : 'blogs', 'PUT', arr);
    showToast('Order saved successfully!', 'success');
  } catch(err) {
    showToast('Failed to save order: ' + err.message, 'error');
  }
}

// ===== PROJECT CRUD =====
"""
html = html.replace('// ===== PROJECT CRUD =====', dnd_js)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

print("Admin HTML updated successfully!")
