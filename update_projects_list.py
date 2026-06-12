import os
import re

with open(r'c:\tmp\Oliveoakk\projects.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to find where the grid items are and replace them with a dynamic loader.
# The user's projects are displayed via .grid-projects or something similar.
# Let's just find the first .masonry-grid or .proj-grid and clear its innerHTML.

# Find the masonry grid wrapper
grid_match = re.search(r'<div class="(?:masonry-grid|projects-grid|p-grid)[^"]*"(?: id="[^"]*")?>.*?(</section>|</main>)', html, re.DOTALL)
if grid_match:
    # Actually, the simplest way is to inject a script before </body> that targets the container
    pass

# We will inject the script and assign an id to the container if we can find it.
html = re.sub(r'(<div class="(?:masonry-grid|projects-grid|p-grid)[^"]*")', r'\1 id="dyn-projects-grid"', html, count=1)

# Remove the static items
html = re.sub(r'(<div class="(?:masonry-grid|projects-grid|p-grid)[^"]*" id="dyn-projects-grid">)(.*?)(</div><!-- END GRID -->|</div>\s*</section>)', r'\1\n  <div style="color:var(--gold);padding:40px;text-align:center;">Loading projects...</div>\n\3', html, flags=re.DOTALL)


script = """
<script>
document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('dyn-projects-grid') || document.querySelector('.masonry-grid, .projects-grid, .bento-grid, .p-grid');
  if (!grid) return;

  try {
    const res = await fetch('/data/projects.json');
    const projects = await res.json();
    
    // Filter published and sort by date
    const published = projects.filter(p => p.status === 'published').sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt));
    
    grid.innerHTML = published.map((p, i) => {
      // Create a bento card or masonry item depending on what OliveOak uses
      // They use a masonry layout like: <a href="project-1.html" class="p-card masonry-item ...">
      const img = p.featuredImage || (p.images && p.images[0]) || '';
      return `
        <a href="project.html?id=${p.slug}" class="p-card reveal" style="display:block;margin-bottom:24px;border-radius:12px;overflow:hidden;position:relative;background:#111;">
          <img src="${img}" alt="${p.title}" style="width:100%;height:350px;object-fit:cover;transition:transform 0.5s;">
          <div style="position:absolute;bottom:0;left:0;right:0;padding:24px;background:linear-gradient(to top, rgba(0,0,0,0.9), transparent);">
            <div style="font-size:10px;text-transform:uppercase;color:var(--gold);letter-spacing:2px;margin-bottom:8px;">${p.category}</div>
            <h3 style="font-family:var(--f-display);font-size:24px;color:var(--white);">${p.title}</h3>
          </div>
        </a>
      `;
    }).join('');

    // Trigger reveal if any
    setTimeout(() => {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
    }, 100);
  } catch (e) {
    grid.innerHTML = '<div style="color:red;padding:40px;">Failed to load projects.</div>';
  }
});
</script>
"""

if "<script>" not in script in html:
    html = html.replace('</body>', script + '\n</body>')

with open(r'c:\tmp\Oliveoakk\projects.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated projects.html")
