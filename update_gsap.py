import re

file_path = r'c:\tmp\Oliveoakk\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the CSS for .svc-img-wrap
old_css = r'''\.svc-img-wrap\{[^}]*aspect-ratio: 4/5; height: auto; overflow:hidden;\s*border-radius:16px;'''
new_css = r'''.svc-img-wrap{
    position:sticky; top:140px; width: 100%; height: calc(100vh - 180px); overflow:hidden;
    border-radius:16px;'''
html = re.sub(old_css, new_css, html, count=1, flags=re.DOTALL)

# 2. Update the Javascript for Desktop Click -> GSAP
old_js = r'''\} else \{\s*/\*\s*Desktop: click to switch sticky image\s*\*/\s*svcItemEls\.forEach\(item => \{\s*item\.addEventListener\('click', \(\) => \{\s*const i = \+item\.dataset\.i;\s*svcItemEls\.forEach\(x => x\.classList\.remove\('on'\)\);\s*document\.querySelectorAll\('\.svc-img'\)\.forEach\(x => x\.classList\.remove\('on'\)\);\s*item\.classList\.add\('on'\);\s*document\.querySelectorAll\('\.svc-img'\)\[i\]\.classList\.add\('on'\);\s*\}\);\s*\}\);\s*\}'''

new_js = r'''} else {
  /* Desktop: GSAP ScrollTrigger for sticky image */
  if (typeof gsap !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
    
    svcItemEls.forEach((item, i) => {
      ScrollTrigger.create({
        trigger: item,
        start: "top center",
        end: "bottom center",
        onToggle: self => {
          if (self.isActive) {
            svcItemEls.forEach(x => x.classList.remove('on'));
            document.querySelectorAll('.svc-img').forEach(x => x.classList.remove('on'));
            item.classList.add('on');
            const targetImg = document.querySelectorAll('.svc-img')[i];
            if (targetImg) targetImg.classList.add('on');
          }
        }
      });
    });
  }
}'''

html = re.sub(old_js, new_js, html, count=1, flags=re.DOTALL)

# 3. Add GSAP & ScrollTrigger scripts before </body>
if 'gsap.min.js' not in html:
    gsap_scripts = '''
<!-- GSAP & ScrollTrigger -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</body>'''
    html = html.replace('</body>', gsap_scripts)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html GSAP update complete.")
