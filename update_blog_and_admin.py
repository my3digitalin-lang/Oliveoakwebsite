import re

blog_path = r'c:\tmp\Oliveoakk\blog.html'
admin_path = r'c:\tmp\Oliveoakk\admin.html'

# 1. Update blog.html
with open(blog_path, 'r', encoding='utf-8') as f:
    blog_html = f.read()

# Remove firebase scripts
blog_html = re.sub(r'<script src="https://www\.gstatic\.com/firebasejs[^>]*></script>', '', blog_html)
blog_html = re.sub(r'<script src="firebase-config\.js"></script>', '', blog_html)

# Replace the loadFirebaseBlog function with a fetch to /data/blogs.json
new_blog_script = r"""<script>
/* ══════════════════════════════════════════════════════════════
   CMS — Load dynamic blog posts from JSON CMS
   New posts are prepended to the "More Articles" scroll strip.
══════════════════════════════════════════════════════════════ */
(async function loadCMSBlog() {
  try {
    const res = await fetch('/data/blogs.json');
    const blogs = await res.json();
    if (!blogs || !blogs.length) return;

    const publishedBlogs = blogs.filter(b => b.status === 'published');
    publishedBlogs.sort((a,b) => (a.order||0) - (b.order||0));

    if (!publishedBlogs.length) return;

    const strip = document.getElementById('scrollStrip');
    if (!strip) return;

    /* Build a document fragment so we insert all at once */
    const frag = document.createDocumentFragment();

    publishedBlogs.forEach(d => {
      if (!d.title) return;
      const postUrl = `blog-post.html?id=${d.slug || d.id}`;
      const a = document.createElement('a');
      a.href = postUrl;
      a.className = 'strip-card';
      a.dataset.cat = d.category || 'Blog';
      a.innerHTML = `
        <div class="strip-card-img">
          <img src="${d.featuredImage || d.coverImage || 'images/kitchen-vastu.webp'}" alt="${d.title}" loading="lazy" decoding="async">
        </div>
        <div class="strip-card-body">
          <div class="strip-card-cat">${d.category || 'Blog'}</div>
          <div class="strip-card-title">${d.title}</div>
          <div class="strip-card-footer">
            <div class="strip-card-date">${new Date(d.createdAt || d.updatedAt).toLocaleDateString()}</div>
            <div class="strip-card-read">Read &rarr;</div>
          </div>
        </div>`;
      frag.appendChild(a);
    });

    /* Prepend CMS cards before existing hardcoded cards */
    strip.insertBefore(frag, strip.firstChild);

    /* Trigger the visible animation for new cards */
    strip.querySelectorAll('.strip-card:not(.visible)').forEach((c, i) => {
      setTimeout(() => c.classList.add('visible'), i * 60 + 100);
    });

  } catch(e) {
    console.warn('CMS blog not loaded:', e.message);
  }
})();
</script>"""

blog_html = re.sub(r'<script>\s*/\* ══════════════════════════════════════════════════════════════\s*FIREBASE — Load dynamic blog posts from admin CMS.*?</script>', new_blog_script, blog_html, flags=re.DOTALL)

with open(blog_path, 'w', encoding='utf-8') as f:
    f.write(blog_html)

# 2. Update admin.html
with open(admin_path, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Replace the password input
old_input = '<input class="login-input" type="password" id="adminPwd" placeholder="Enter password" onkeydown="if(event.key===\'Enter\')doLogin()">'
new_input = """<div style="position:relative;">
      <input class="login-input" type="password" id="adminPwd" placeholder="Enter password" onkeydown="if(event.key==='Enter')doLogin()" style="padding-right:40px;">
      <button type="button" onclick="const p=document.getElementById('adminPwd'); p.type=p.type==='password'?'text':'password'; this.textContent=p.type==='password'?'👁️':'🙈';" style="position:absolute;right:12px;top:14px;background:none;border:none;cursor:pointer;font-size:16px;">👁️</button>
    </div>"""

admin_html = admin_html.replace(old_input, new_input)

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Updates completed.")
