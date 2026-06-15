import glob
import re

html_files = glob.glob(r'c:\tmp\Oliveoakk\*.html')

phone = "+91 8187094428"
email = "contact@oliveoak.in"

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        enc = 'utf-8'
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as f:
            html = f.read()
        enc = 'utf-16'
    
    html = re.sub(r'mailto:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', f'mailto:{email}', html)
    html = re.sub(r'>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+<', f'>{email}<', html)
    
    html = re.sub(r'\+91 \d{5}\s?\d{5}', phone, html)
    html = re.sub(r'\+91\d{10}', phone, html)
    html = re.sub(r'tel:\+91\d+', f'tel:{phone.replace(" ", "")}', html)
    
    with open(filepath, 'w', encoding=enc) as f:
        f.write(html)

print("Footers updated globally.")
