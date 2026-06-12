import sys

with open('contact.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Your Vision
vision_str = """      <div class="form-group">
        <label for="fmsg">Your Vision</label>
        <textarea id="fmsg" name="message" class="form-input" placeholder="Describe your space, style preferences, or any specific requirements…"></textarea>
      </div>"""
content = content.replace(vision_str, "")

# 2. Update Address in info side
address_old_1 = """        <div class="info-label">Studio</div>
        <div class="info-val">Road No. 1, Shantinagar Colony,<br>Hyderabad</div>"""
address_new_1 = """        <div class="info-label">Studio</div>
        <div class="info-val">Rd No. 33, Kondapur,<br>Raghavendra Colony, Gachibowli,<br>Hyderabad, Telangana 500084</div>"""
content = content.replace(address_old_1, address_new_1)

# 3. Update Address in map footer
address_old_2 = "<span>Road No. 1, Shantinagar Colony, Hyderabad, Telangana</span>"
address_new_2 = "<span>Rd No. 33, Kondapur, Raghavendra Colony, Gachibowli, Hyderabad, Telangana 500084</span>"
content = content.replace(address_old_2, address_new_2)

with open('contact.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Contact page updated.")
