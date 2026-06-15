import os, glob

d = r'c:\tmp\Oliveoakk'
fs = glob.glob(os.path.join(d, '*.html'))

for f in fs:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        enc = 'utf-8'
    except UnicodeDecodeError:
        try:
            with open(f, 'r', encoding='utf-16') as file:
                c = file.read()
            enc = 'utf-16'
        except:
            continue

    changed = False
    
    # Replace navbar logo
    if '>OliveOak</a>' in c:
        c = c.replace('>OliveOak</a>', '><img src="logo.webp" alt="Tet Contractors" style="height:30px; width:auto; object-fit:contain; filter: brightness(0) invert(1);"></a>')
        changed = True
        
    # Replace footer logo
    if 'class="foot-logo">OliveOak</div>' in c:
        c = c.replace('class="foot-logo">OliveOak</div>', 'class="foot-logo"><img src="logo.webp" alt="Tet Contractors" style="height:50px; width:auto; object-fit:contain; filter: brightness(0) invert(1);"></div>')
        changed = True
        
    # We already did the phone/email earlier but we'll ensure they are replaced if anything was missed
    if '+91 77801 96804' in c:
        c = c.replace('+91 77801 96804', '+91 8187094428')
        changed = True
    if 'tel:+917780196804' in c:
        c = c.replace('tel:+917780196804', 'tel:+918187094428')
        changed = True
    if 'hello@oliveoak.in' in c or 'info@oliveoak.in' in c:
        c = c.replace('hello@oliveoak.in', 'contact@oliveoak.in')
        c = c.replace('info@oliveoak.in', 'contact@oliveoak.in')
        changed = True

    if changed:
        with open(f, 'w', encoding=enc) as file:
            file.write(c)

print('Replacements Done!')
