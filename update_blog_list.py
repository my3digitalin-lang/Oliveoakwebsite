import os
import re

with open(r'c:\tmp\Oliveoakk\blog.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the blog grid
html = re.sub(r'(<div class="(?:blog-grid|grid-blog)[^"]*")', r'\1 id="dyn-blog-grid"', html, count=1)
html = re.sub(r'(<div class="(?:blog-grid|grid-blog)[^"]*" id="dyn-blog-grid">)(.*?)(</div><!-- END GRID -->|</div>\s*</section>)', r'\1\n  <div style="color:var(--gold);padding:40px;text-align:center;">Loading articles...</div>\n\3', html, flags=re.DOTALL)

script = """
<script>
document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('dyn-blog-grid') || document.querySelector('.blog-grid');
  if (!grid) return;

  try {
    const res = await fetch('/data/blogs.json');
    const blogs = await res.json();
    
    const published = blogs.filter(b => b.status === 'published').sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt));
    
    grid.innerHTML = published.map((b) => {
      const img = b.featuredImage || '';
      return `
        <a href="blog-post.html?id=${b.slug}" class="blog-card reveal" style="display:block;border:1px solid rgba(200,169,126,0.15);border-radius:12px;overflow:hidden;background:rgba(255,255,255,0.02);transition:transform 0.3s;margin-bottom:24px;">
          ${img ? `<img src="${img}" alt="${b.title}" style="width:100%;height:240px;object-fit:cover;">` : ''}
          <div style="padding:24px;">
            <div style="font-size:10px;text-transform:uppercase;color:var(--gold);letter-spacing:2px;margin-bottom:12px;">${b.category} &bull; ${new Date(b.createdAt).toLocaleDateString()}</div>
            <h3 style="font-family:var(--f-display);font-size:22px;color:var(--white);margin-bottom:12px;">${b.title}</h3>
            <p style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.6;margin-bottom:20px;">${b.excerpt}</p>
            <div style="font-size:11px;color:var(--gold);text-transform:uppercase;letter-spacing:1px;font-weight:600;">Read Article &rarr;</div>
          </div>
        </a>
      `;
    }).join('');

    setTimeout(() => {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    }, 100);
  } catch (e) {
    grid.innerHTML = '<div style="color:red;padding:40px;">Failed to load articles.</div>';
  }
});
</script>
"""

if "<script>" not in script in html:
    html = html.replace('</body>', script + '\n</body>')

with open(r'c:\tmp\Oliveoakk\blog.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated blog.html")
