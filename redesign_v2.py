import re

with open(r'c:\tmp\Oliveoakk\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Instead of replacing all `.svc-img-wrap { ... }`, we locate the <style> section and do direct replacements on exact blocks.

# 1. Update Layout Balance (45/55 -> 1fr 1fr or roughly 45/55)
# Original: .svc-wrap{display:grid;grid-template-columns:5fr 7fr;gap:80px;align-items:flex-start}
html = re.sub(
    r'\.svc-wrap\s*\{[^}]*\}', 
    r'.svc-wrap{display:grid;grid-template-columns:1fr 1.1fr;gap:100px;align-items:stretch;}', 
    html, count=1
)

# 2. Update .svc-img-wrap in main CSS
# Original main: .svc-img-wrap{position:sticky;top:120px;border-radius:16px;overflow:hidden;...}
html = re.sub(
    r'/\*\s*Left:\s*sticky\s*image\s*\*/\s*\.svc-img-wrap\s*\{[^}]*\}',
    r'/* Left: sticky image */\n  .svc-img-wrap{\n    position:sticky; top:120px; align-self: stretch; height:calc(100vh - 160px); min-height: 600px; overflow:hidden;\n    border-radius:16px;\n    border: 1px solid rgba(200,169,126,0.15);\n    background: rgba(0,0,0,0.5);\n  }',
    html
)

# 3. Add Image Borders / Gold Accents right after .svc-img-wrap
accents = r'''
  .svc-img-wrap::before, .svc-img-wrap::after {
    content:''; position:absolute; z-index:2;
    width:40px; height:40px; pointer-events: none;
  }
  .svc-img-wrap::before {
    top:16px; left:16px;
    border-top:1px solid rgba(200,169,126,.4);
    border-left:1px solid rgba(200,169,126,.4);
  }
  .svc-img-wrap::after {
    bottom:16px; right:16px;
    border-bottom:1px solid rgba(200,169,126,.4);
    border-right:1px solid rgba(200,169,126,.4);
  }
'''
html = html.replace('/* Right: accordion */', accents + '  /* Right: accordion */')

# 4. Update .svc-item
html = re.sub(
    r'\.svc-item\s*\{[^}]*padding:28px 0;[^}]*\}',
    r'''.svc-item{
    display:flex;align-items:flex-start;gap:28px;
    padding:32px 24px;
    margin: 0 -24px;
    border-bottom:1px solid rgba(255,255,255,.05);
    border-left: 2px solid transparent;
    cursor:pointer;
    position:relative;
    transition: all .4s var(--ease);
  }''',
    html
)

html = re.sub(
    r'\.svc-item:hover,\.svc-item\.on\s*\{padding-left:16px\}',
    r'''.svc-item:hover, .svc-item.on {
    padding-left: 36px;
    border-left: 2px solid var(--gold);
    background: linear-gradient(90deg, rgba(200,169,126,0.04) 0%, transparent 100%);
  }''',
    html
)

# 5. Update Typography Hierarchy
html = re.sub(
    r'\.svc-name\s*\{[^}]*font-size:22px;[^}]*\}',
    r'''.svc-name{
    font-family:var(--f-display);
    font-size:20px;font-weight:300;
    letter-spacing: 0.5px;
    color:rgba(255,255,255,.5);
    margin-bottom:0;
    transition:color .3s;
  }''',
    html
)

html = re.sub(
    r'\.svc-desc\s*\{[^}]*max-height:0;overflow:hidden;[^}]*\}',
    r'''.svc-desc{
    font-family:var(--f-body);font-size:14px;
    color:rgba(255,255,255,.45);line-height:1.75;
    max-height:0;overflow:hidden;
    transition:max-height .5s,opacity .5s,margin-top .5s;
    opacity:0;margin-top:0;
  }''',
    html
)

html = re.sub(
    r'\.svc-item\.on\s*\.svc-desc\s*\{max-height:80px;opacity:1;margin-top:10px\}',
    r'''.svc-item.on .svc-desc{max-height:160px;opacity:1;margin-top:12px}''',
    html
)

# 6. Reduce floating glow
html = re.sub(r'rgba\(92,61,30,\.15\)', r'rgba(92,61,30,.04)', html)

# 7. Add mini CTA
cta_style = '''
  .svc-mini-cta {
    display: inline-flex; align-items: center; gap: 8px;
    margin-top: 20px;
    color: var(--gold);
    font-size: 11px; text-transform: uppercase; letter-spacing: 1px;
    font-weight: 500; text-decoration: none;
    border-bottom: 1px solid rgba(200,169,126,0.3);
    padding-bottom: 2px;
    transition: all .3s;
  }
  .svc-mini-cta:hover { border-bottom-color: var(--gold); transform: translateX(4px); }
  .svc-mini-cta svg { width: 12px; height: 12px; }
  '''
html = html.replace('</style>', cta_style + '\n  </style>', 1)

# Remove the old isolated CTA
html = re.sub(r'<a href="#footer" class="btn btn-gold" style="margin-top:48px">\s*Book Consultation\s*<span class="arr">.*?</span>\s*</a>', '', html, flags=re.DOTALL)

# Inject mini CTA
mini_cta_html = r'<br><a href="#footer" class="svc-mini-cta">Book Consultation <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></a>'
html = re.sub(r'(<div class="svc-desc">.*?)(</div>)', r'\1' + mini_cta_html + r'\2', html, flags=re.DOTALL)

# Save
with open(r'c:\tmp\Oliveoakk\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied safe services redesign")
