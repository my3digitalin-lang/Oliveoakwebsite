import glob
import re

html_files = glob.glob(r'c:\tmp\Oliveoakk\*.html')

phone = "+91 8187094428"
email = "contact@oliveoak.in"

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Simple regex to replace phone numbers
    # Look for href="tel:..." and >...< text. 
    # Or just replace the specific text blocks we know exist in footer.
    # In OliveOak footers usually it's `contact@oliveoak.in` or similar.
    # Let's replace any email href: `mailto:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+`
    html = re.sub(r'mailto:[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', f'mailto:{email}', html)
    html = re.sub(r'>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+<', f'>{email}<', html)
    
    # Replace phone numbers. The old one might be `+91 9999999999` or similar.
    # Let's just blindly replace `+91 99496 95166` or similar.
    html = re.sub(r'\+91 \d{5}\s?\d{5}', phone, html)
    html = re.sub(r'\+91\d{10}', phone, html)
    html = re.sub(r'tel:\+91\d+', f'tel:{phone.replace(" ", "")}', html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Footers updated globally.")
