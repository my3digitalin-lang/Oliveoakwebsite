import os
import re

with open(r'c:\tmp\Oliveoakk\project-1.html', 'r', encoding='utf-8') as f:
    project_html = f.read()

# Make it dynamic! We replace the hardcoded content with empty spans/divs with IDs
# and add a script to load data from /data/projects.json based on URL search params (?id=slug)

# First, strip out all the hardcoded content inside the body except nav/footer
# It's safer to just construct the dynamic JS script and append it to the end.

# Replace title
project_html = re.sub(r'<title>.*?</title>', '<title>Project | OliveOak Interiors</title>', project_html)

# Add IDs to elements that need dynamic data
project_html = re.sub(r'<h1 class="proj-hero-h1">The Linden Court</h1>', '<h1 class="proj-hero-h1" id="dyn-title">Loading...</h1>', project_html)
project_html = re.sub(r'<span class="hero-cat">Residential</span>', '<span class="hero-cat" id="dyn-cat"></span>', project_html)
project_html = re.sub(r'<img src="images/projects/proj1_1\.webp" alt="The Linden Court Hero" class="proj-hero-bg">', '<img src="" id="dyn-hero-img" class="proj-hero-bg" style="display:none;">', project_html)

project_html = re.sub(r'<div class="ov-val">OliveOak Residences</div>', '<div class="ov-val" id="dyn-client">OliveOak Residences</div>', project_html)
project_html = re.sub(r'<div class="ov-val">2026</div>', '<div class="ov-val" id="dyn-year"></div>', project_html)
project_html = re.sub(r'<div class="ov-val">Hyderabad, India</div>', '<div class="ov-val" id="dyn-location">Hyderabad, India</div>', project_html)
project_html = re.sub(r'<div class="ov-val">Wood, Marble, Brass</div>', '<div class="ov-val" id="dyn-tech"></div>', project_html)

project_html = re.sub(r'<h2 class="story-h2">.*?</h2\s*>', '<h2 class="story-h2" id="dyn-story-h2"></h2>', project_html, flags=re.DOTALL)
project_html = re.sub(r'<div class="story-body">.*?</div>', '<div class="story-body" id="dyn-desc"></div>', project_html, flags=re.DOTALL)

project_html = re.sub(r'<div class="gallery-grid">.*?</div>', '<div class="gallery-grid" id="dyn-gallery-1"></div>', project_html, flags=re.DOTALL)
project_html = re.sub(r'<div class="gallery-grid-row2">.*?</div>', '<div class="gallery-grid-row2" id="dyn-gallery-2"></div>', project_html, flags=re.DOTALL)

dynamic_script = """
<script>
  async function loadProject() {
    const urlParams = new URLSearchParams(window.location.search);
    const slug = urlParams.get('id');
    if (!slug) {
      window.location.href = 'projects.html';
      return;
    }

    try {
      const res = await fetch('/data/projects.json');
      const projects = await res.json();
      const proj = projects.find(p => p.slug === slug && p.status === 'published');

      if (!proj) {
        document.getElementById('dyn-title').textContent = 'Project Not Found';
        return;
      }

      document.title = `${proj.title} | OliveOak Interiors`;
      document.getElementById('dyn-title').textContent = proj.title;
      document.getElementById('dyn-cat').textContent = proj.category;
      
      const heroImg = document.getElementById('dyn-hero-img');
      heroImg.src = proj.featuredImage || proj.images[0] || '';
      heroImg.style.display = 'block';

      document.getElementById('dyn-year').textContent = new Date(proj.updatedAt).getFullYear();
      document.getElementById('dyn-tech').textContent = (proj.technologies || []).join(', ');
      
      document.getElementById('dyn-story-h2').innerHTML = `The <em>${proj.title}</em>`;
      
      // Basic formatting for description
      const descHtml = (proj.description || '').split('\\n').map(p => `<p>${p}</p>`).join('<div class="divider"></div>');
      document.getElementById('dyn-desc').innerHTML = descHtml;

      // Gallery up to 7 images
      const imgs = proj.images || [];
      const g1 = document.getElementById('dyn-gallery-1');
      const g2 = document.getElementById('dyn-gallery-2');
      g1.innerHTML = ''; g2.innerHTML = '';

      // First 3 images go to grid 1
      for (let i = 0; i < Math.min(3, imgs.length); i++) {
        g1.innerHTML += `<div class="g-item reveal"><img src="${imgs[i]}" loading="lazy"></div>`;
      }
      // Next 4 images go to grid 2
      for (let i = 3; i < Math.min(7, imgs.length); i++) {
        g2.innerHTML += `<div class="g-item reveal"><img src="${imgs[i]}" loading="lazy"></div>`;
      }

      // Re-trigger reveal animation logic if any
      setTimeout(() => {
        document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
      }, 100);

    } catch (e) {
      console.error('Error loading project', e);
      document.getElementById('dyn-title').textContent = 'Error Loading Project';
    }
  }

  window.addEventListener('DOMContentLoaded', loadProject);
</script>
"""

project_html = project_html.replace('</body>', dynamic_script + '\n</body>')

with open(r'c:\tmp\Oliveoakk\project.html', 'w', encoding='utf-8') as f:
    f.write(project_html)

print("Created dynamic project.html")
