import sys

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace blog links in about.html to redirect to projects
content = content.replace('href="best-interior-design-ideas.html"', 'href="projects.html"')
content = content.replace('href="3bhk-interior-design-hyderabad.html"', 'href="projects.html"')
content = content.replace('href="2bhk-interior-design-hyderabad.html"', 'href="projects.html"')

# Just in case there are others
content = content.replace('class="blog-more"', 'class="blog-more" title="View Project"')

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated about.html blog cards to redirect to projects.")
