import re

with open(r'c:\tmp\Oliveoakk\projects.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Firebase scripts
html = re.sub(r'<!-- Firebase SDK -->.*?</script>\s*</body>', '</body>', html, flags=re.DOTALL)

# Ensure the new JSON fetch script is present
script = """
<script>
document.addEventListener('DOMContentLoaded', async () => {
  const container = document.getElementById('firebase-grids') || document.querySelector('.container') || document.body;
  
  // Clear container if it has "firebase-grids" to start fresh
  if(container.id === 'firebase-grids') container.innerHTML = '';

  try {
    const res = await fetch('/data/projects.json');
    const projects = await res.json();
    const published = projects.filter(p => p.status === 'published').sort((a,b)=>new Date(b.createdAt)-new Date(a.createdAt));
    
    let htmlStr = '';
    let projNum = 1;
    
    published.forEach((d) => {
      const images = (d.images && d.images.length) ? d.images.filter(i=>i) : [d.featuredImage];
      const noStr = String(projNum).padStart(2,'0');
      const gridId = `gh-grid-${d.id}`;
      const layoutClasses = ['hero','left','right','sm','sm','sm cta-cell'];
      
      let labelHTML = `
        <div class="project-label" style="margin-top:80px;margin-bottom:16px;">
          <span class="project-label-no" style="font-size:12px;color:var(--gold);margin-right:12px;">${noStr}</span>
          <span class="project-label-name" style="font-size:24px;font-family:var(--f-display);">${d.title}</span>
          <span class="project-label-type" style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,0.5);margin-left:16px;">${d.category}</span>
        </div>`;

      let itemsHTML = '';
      images.slice(0,5).forEach((img,i)=>{
        const cls = layoutClasses[i]||'sm';
        itemsHTML += `
          <a class="bento-item ${cls} portal" href="project.html?id=${d.slug}">
            <div class="bento-inner">
              <img src="${img}" alt="${d.title}" loading="lazy">
            </div>
            <div class="bento-overlay">
              <span class="bento-project">${d.title}</span>
            </div>
          </a>`;
      });

      if(images.length < 6){
        itemsHTML += `
          <a class="bento-item sm cta-cell portal" href="project.html?id=${d.slug}">
            <span class="cta-cell-no">${noStr}</span>
            <span class="cta-cell-name">${d.title}</span>
            <span class="cta-cell-link">View Full Project &rarr;</span>
          </a>`;
      }

      htmlStr += labelHTML + `<div class="bento-grid" id="${gridId}">${itemsHTML}</div>`;
      projNum++;
    });
    
    // Inject at the bottom before footer or append to container
    container.innerHTML += htmlStr;
    
  } catch(e) {
    console.error(e);
  }
});
</script>
"""

# Append the new script
if 'fetch(\'/data/projects.json\')' not in html:
    html = html.replace('</body>', script + '\n</body>')

with open(r'c:\tmp\Oliveoakk\projects.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed projects.html")
