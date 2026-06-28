import os
import re
from bs4 import BeautifulSoup

blog_dir = r"e:\Mokshshara\blog posts"
export_dir = os.path.join(blog_dir, "blogger_export")

for folderName in os.listdir(export_dir):
    folder_path = os.path.join(export_dir, folderName)
    if not os.path.isdir(folder_path):
        continue
    
    post_body_path = os.path.join(folder_path, "post_body.html")
    if not os.path.exists(post_body_path):
        continue
        
    print(f"Cleaning exported file: {post_body_path}")
    
    with open(post_body_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Remove navigation bar
    nav = soup.find("nav")
    if nav:
        nav.decompose()
    old_header = soup.find(class_="article-top-header")
    if old_header:
        old_header.decompose()
        
    # 2. Remove footer
    footer = soup.find("footer")
    if footer:
        footer.decompose()
    old_footer_sec = soup.find("section", class_="article-bottom-footer")
    if old_footer_sec:
        old_footer_sec.decompose()
        
    # 3. Clean up the CSS styles inside <style>
    style_tags = soup.find_all("style")
    for style_tag in style_tags:
        if not style_tag.string:
            continue
            
        css = style_tag.string
        
        # Remove CDATA wrapper if it exists (Blogger CDATA might be added)
        css = css.replace("/*<![CDATA[*/", "").replace("/*]]>*/", "")
        
        # Replace global body settings with a container class `.mokshara-post-container`
        css = re.sub(r'body\s*\{', '.mokshara-post-container {', css)
        
        # Remove global reset * { margin: 0; padding: 0; ... } and scope box-sizing
        css = re.sub(r'\*\s*\{\s*margin:\s*0;\s*padding:\s*0;\s*box-sizing:\s*border-box;\s*\}', '.mokshara-post-container * { box-sizing: border-box; }', css)
        
        # Remove fixed navigation styles
        css = re.sub(r'nav\s*\{[^}]*\}', '', css)
        css = re.sub(r'\.nav-[^}]*\{[^}]*\}', '', css)
        css = re.sub(r'\.overlay-[^}]*\{[^}]*\}', '', css)
        css = re.sub(r'\.footer-modal-[^}]*\{[^}]*\}', '', css)
        
        # Remove footer styles
        css = re.sub(r'footer\s*\{[^}]*\}', '', css)
        css = re.sub(r'footer\s+[^}]*\{[^}]*\}', '', css)
        
        style_tag.string = css
        
    # 4. Extract only the main body content and wrap in a clean container
    # We want everything that's inside the body, excluding nav and footer (which are already decomposed)
    body = soup.find("body")
    if body:
        # Get all child elements of body
        body_children = []
        for child in body.children:
            body_children.append(str(child))
            
        inner_content = "".join(body_children)
    else:
        # Fallback if no body tag (already partial HTML)
        inner_content = str(soup)
        
    # Wrap in our scoped container div
    cleaned_html = f'<div class="mokshara-post-container">\n{inner_content}\n</div>'
    
    # Save the cleaned file
    clean_post_body_path = os.path.join(folder_path, "post_body_clean.html")
    with open(clean_post_body_path, "w", encoding="utf-8") as f:
        f.write(cleaned_html)
        
    print(f"Successfully saved clean version to: {clean_post_body_path}")

print("All exports cleaned successfully!")
