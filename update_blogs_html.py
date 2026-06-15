import re
import os

blog_list_path = r'c:\tmp\Oliveoakk\blog.html'
blog_post_path = r'c:\tmp\Oliveoakk\blog-post.html'

if os.path.exists(blog_list_path):
    with open(blog_list_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if we need to sort blogs
    if "const blogs = await res.json();" in html and "blogs.sort(" not in html:
        html = html.replace(
            "const blogs = await res.json();",
            "const blogs = await res.json();\n      blogs.sort((a,b) => (a.order||0) - (b.order||0));"
        )
        with open(blog_list_path, 'w', encoding='utf-8') as f:
            f.write(html)
            print("blog.html updated with sorting.")

if os.path.exists(blog_post_path):
    with open(blog_post_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Inject SEO details
    if "document.title =" in html and "document.querySelector('meta[name=\"description\"]')" not in html:
        seo_js = r"""
      // SEO
      if (post.metaTitle) {
        document.title = post.metaTitle;
      } else {
        document.title = `${post.title} | OliveOak Blog`;
      }
      if (post.metaDescription) {
        let metaDesc = document.querySelector('meta[name="description"]');
        if (!metaDesc) {
          metaDesc = document.createElement('meta');
          metaDesc.name = "description";
          document.head.appendChild(metaDesc);
        }
        metaDesc.content = post.metaDescription;
      }
"""
        html = html.replace("document.title = `${post.title} | OliveOak Blog`;", seo_js)
        with open(blog_post_path, 'w', encoding='utf-8') as f:
            f.write(html)
            print("blog-post.html updated with SEO.")
