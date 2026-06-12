import os
import re

with open(r'c:\tmp\Oliveoakk\blog-post.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove firebase scripts
html = re.sub(r'<script src="https://www.gstatic.com/firebasejs/.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script src="firebase-config.js"></script>', '', html)

new_script = """<script>
(async function() {
  const params = new URLSearchParams(window.location.search);
  const slug = params.get('id');

  if (!slug) {
    showError('No blog post specified.');
    return;
  }

  try {
    const res = await fetch('/data/blogs.json');
    const blogs = await res.json();
    const post = blogs.find(b => b.slug === slug && b.status === 'published');

    if (!post) {
      showError('Blog post not found.');
      return;
    }

    renderPost(post);

  } catch(e) {
    console.error(e);
    showError('Could not load blog post. Error fetching data.');
  }

  function renderPost(post) {
    document.title = (post.title) + ' | OliveOak Interiors';
    const metaDesc = document.createElement('meta');
    metaDesc.name = 'description';
    metaDesc.content = post.excerpt || '';
    document.head.appendChild(metaDesc);

    document.getElementById('postContent').innerHTML = `
      <!-- HERO -->
      <div class="post-hero">
        ${post.featuredImage ? `<img class="post-hero-img" src="${post.featuredImage}" alt="${post.title}">` : ''}
        <div class="post-hero-overlay"></div>
        <div class="post-hero-content">
          <span class="post-cat-tag">${post.category || 'Blog'}</span>
          <h1 class="post-h1">${post.title}</h1>
          <div class="post-meta">${new Date(post.createdAt).toLocaleDateString()}</div>
        </div>
      </div>

      <!-- BODY -->
      <article class="post-body">
        <div class="post-intro">${post.excerpt || ''}</div>
        ${post.content || ''}
      </article>
    `;
  }

  function showError(msg) {
    document.getElementById('postContent').innerHTML = `
      <div class="error-box" style="margin-top:72px">
        <h2>Oops!</h2>
        <p>${msg}</p>
        <a href="blog.html" class="back-link">← Back to Blog</a>
      </div>`;
  }
})();
</script>"""

html = re.sub(r'<script>\s*\(async function\(\).*?\}\)\(\);\s*</script>', new_script, html, flags=re.DOTALL)

with open(r'c:\tmp\Oliveoakk\blog-post.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated blog-post.html")
