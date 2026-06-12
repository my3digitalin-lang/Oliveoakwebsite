import sys

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I previously blindly replaced the hrefs in about.html to projects.html. Let me restore them.
# The original titles were:
# 1. Best Interior Design Ideas for Homes in Hyderabad -> best-interior-design-ideas.html
# 2. 3BHK Interior Design in Hyderabad for Modern Homes -> 3bhk-interior-design-hyderabad.html
# 3. 2BHK Interior Design in Hyderabad -> 2bhk-interior-design-hyderabad.html

import re

# Since I replaced them all with 'projects.html', I need to put them back based on the title next to them.
content = re.sub(
    r'<a href="projects.html" class="blog-more" title="View Project">Read More(.*?)</a>\s*</div>\s*</article>\s*<article class="blog-card" style="transition-delay:\.14s">',
    r'<a href="best-interior-design-ideas.html" class="blog-more">Read More\1</a>\n      </div>\n    </article>\n    <article class="blog-card" style="transition-delay:.14s">',
    content, flags=re.DOTALL
)

content = re.sub(
    r'<a href="projects.html" class="blog-more" title="View Project">Read More(.*?)</a>\s*</div>\s*</article>\s*<article class="blog-card" style="transition-delay:\.28s">',
    r'<a href="3bhk-interior-design-hyderabad.html" class="blog-more">Read More\1</a>\n      </div>\n    </article>\n    <article class="blog-card" style="transition-delay:.28s">',
    content, flags=re.DOTALL
)

content = re.sub(
    r'<a href="projects.html" class="blog-more" title="View Project">Read More(.*?)</a>\s*</div>\s*</article>\s*</div>\s*</section>',
    r'<a href="2bhk-interior-design-hyderabad.html" class="blog-more">Read More\1</a>\n      </div>\n    </article>\n  </div>\n</section>',
    content, flags=re.DOTALL
)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored about.html blog card links.")
