import os
import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the masonry grid inside projects section
html = re.sub(r'(<div class="masonry-grid"[^>]*>)(.*?)(</div><!-- END GRID -->|</div>\s*</section>)', r'\1\n  <div id="dyn-index-projects" style="width:100%;text-align:center;color:var(--gold);padding:40px;">Loading projects...</div>\n\3', html, flags=re.DOTALL)

# Inject script
script = """
<script>
document.addEventListener('DOMContentLoaded', async () => {
  // Load recent projects
  const projGrid = document.getElementById('dyn-index-projects');
  if (projGrid) {
    try {
      const res = await fetch('/data/projects.json');
      const projects = await res.json();
      const published = projects.filter(p => p.status === 'published').sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt)).slice(0, 3);
      
      projGrid.innerHTML = published.map((p, i) => {
        const img = p.featuredImage || (p.images && p.images[0]) || '';
        const cl = i === 0 ? 'p-card-large' : 'p-card-small'; // based on their masonry style
        return `
          <a href="project.html?id=${p.slug}" class="p-card ${cl} reveal" style="display:block;border-radius:12px;overflow:hidden;position:relative;margin-bottom:24px;background:#111;">
            <img src="${img}" alt="${p.title}" style="width:100%;height:${i===0?'500px':'300px'};object-fit:cover;transition:transform 0.5s;">
            <div style="position:absolute;bottom:0;left:0;right:0;padding:24px;background:linear-gradient(to top, rgba(0,0,0,0.9), transparent);">
              <div style="font-size:10px;text-transform:uppercase;color:var(--gold);letter-spacing:2px;margin-bottom:8px;">${p.category}</div>
              <h3 style="font-family:var(--f-display);font-size:24px;color:var(--white);">${p.title}</h3>
            </div>
          </a>
        `;
      }).join('');
    } catch(e) {
      projGrid.innerHTML = '';
    }
  }

  // Load recent blogs if there's a blog section
  // Assuming there's a blog grid, but if not it's safe
  const blogGrid = document.getElementById('dyn-index-blogs');
  if (blogGrid) {
    try {
      const res = await fetch('/data/blogs.json');
      const blogs = await res.json();
      const published = blogs.filter(b => b.status === 'published').sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt)).slice(0, 3);
      
      blogGrid.innerHTML = published.map(b => {
        const img = b.featuredImage || '';
        return `
          <a href="blog-post.html?id=${b.slug}" class="blog-card reveal" style="display:block;border:1px solid rgba(200,169,126,0.15);border-radius:12px;overflow:hidden;background:rgba(255,255,255,0.02);margin-bottom:24px;">
            ${img ? `<img src="${img}" alt="${b.title}" style="width:100%;height:200px;object-fit:cover;">` : ''}
            <div style="padding:24px;">
              <h3 style="font-family:var(--f-display);font-size:20px;color:var(--white);margin-bottom:12px;">${b.title}</h3>
              <p style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.6;margin-bottom:16px;">${b.excerpt}</p>
              <div style="font-size:10px;color:var(--gold);text-transform:uppercase;letter-spacing:1px;font-weight:600;">Read &rarr;</div>
            </div>
          </a>
        `;
      }).join('');
    } catch(e) {
      blogGrid.innerHTML = '';
    }
  }

  setTimeout(() => {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
  }, 200);
});
</script>
"""

if "dyn-index-projects" in script and "<script>" not in html[-2000:]:
    html = html.replace('</body>', script + '\n</body>')

with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html")
