# -*- coding: utf-8 -*-
import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Background elements
html = html.replace('background:radial-gradient(circle,rgba(92,61,30,.04) 0%,transparent 70%);',
                    'background:radial-gradient(circle,rgba(92,61,30,.015) 0%,transparent 70%);')

# 2. Grid Layout
html = html.replace('.svc-wrap{display:grid;grid-template-columns:1fr 1.1fr;gap:100px;align-items:stretch;}',
                    '.svc-wrap{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:stretch;}')

# 3. Image Wrapper
old_img_css = '''.svc-img-wrap{
    position:sticky; top:120px; align-self: stretch; height:calc(100vh - 160px); min-height: 600px; overflow:hidden;
    border-radius:16px;
    border: 1px solid rgba(200,169,126,0.15);
    background: rgba(0,0,0,0.5);
  }'''
new_img_css = '''.svc-img-wrap{
    position:sticky; top:140px; width: 100%; aspect-ratio: 4/5; height: auto; overflow:hidden;
    border-radius:16px;
    border: 1px solid rgba(200,169,126,0.25);
    background: rgba(0,0,0,0.5);
    box-shadow: 0 24px 48px rgba(0,0,0,0.4);
  }'''
html = html.replace(old_img_css, new_img_css)

# 4. Right side container
html = html.replace('.svc-right{padding-top:8px; max-width: 100%;}', '.svc-right{padding-top:0; max-width: 100%; display: flex; flex-direction: column; justify-content: center;}')
html = html.replace('.svc-header{margin-bottom:60px}', '.svc-header{margin-bottom:50px}')
html = html.replace('.svc-heading{\n\n  font-family:var(--f-display);\n\n  font-size:clamp(32px, 3.5vw, 48px);', '.svc-heading{\n\n  font-family:var(--f-display);\n\n  font-size:clamp(36px, 4vw, 52px);')

# 5. List items spacing and hover effects
old_item_css = '''.svc-item{
    display:flex;align-items:flex-start;gap:28px;
    padding:32px 24px;
    margin: 0 -24px;
    border-bottom:1px solid rgba(255,255,255,.05);
    border-left: 2px solid transparent;
    cursor:pointer;
    position:relative;
    transition: all .4s var(--ease);
  }'''
new_item_css = '''.svc-item{
    display:flex;align-items:flex-start;gap:28px;
    padding:36px 24px;
    margin: 0 -24px;
    border-bottom:1px solid rgba(255,255,255,.05);
    border-left: 2px solid transparent;
    cursor:pointer;
    position:relative;
    transition: all .5s cubic-bezier(0.22, 1, 0.36, 1);
  }'''
html = html.replace(old_item_css, new_item_css)

old_hover_css = '''.svc-item:hover, .svc-item.on {
    padding-left: 36px;
    border-left: 2px solid var(--gold);
    background: linear-gradient(90deg, rgba(200,169,126,0.04) 0%, transparent 100%);
  }'''
new_hover_css = '''.svc-item:hover, .svc-item.on {
    padding-left: 40px;
    border-left: 2px solid var(--gold);
    background: linear-gradient(90deg, rgba(200,169,126,0.07) 0%, transparent 100%);
    box-shadow: inset 0 -1px 0 rgba(200,169,126,0.15);
  }'''
html = html.replace(old_hover_css, new_hover_css)

# Font sizes
html = html.replace('.svc-name{\n\n    font-family:var(--f-display);\n\n    font-size:20px;font-weight:300;', '.svc-name{\n\n    font-family:var(--f-display);\n\n    font-size:18px;font-weight:300;')

# 6. Remove old inline CTA
html = re.sub(r'<br><a href="#footer" class="svc-mini-cta".*?</a>', '', html)

# 7. Add new CTA placement at bottom of the list
new_cta = '''
        <div style="margin-top: 50px;">
          <a href="#footer" class="btn-outline" style="display:inline-flex; align-items:center; gap:8px;">
            Book Consultation
            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
          </a>
        </div>
'''
html = re.sub(r'          </div>\s+</div>\s+</div>\s+</div>\s+</section>', 
              r'          </div>\n        </div>\n' + new_cta + '\n      </div>\n    </div>\n  </section>', html)

with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Updated services section layout and styling")
