import os
from bs4 import BeautifulSoup

blog_dir = r"e:\Mokshshara\blog posts"
html_files = [f for f in os.listdir(blog_dir) if f.startswith("mokshara-blog-") and f.endswith(".html")]

about_founders_html = """
    <div class="sidebar-widget author-widget">
      <h4 class="widget-title">About the Founders</h4>
      
      <!-- Founder 1 -->
      <div style="margin-bottom: 1.5rem; text-align: center;">
        <div style="width: 80px; height: 80px; margin: 0 auto 0.6rem; border-radius: 50%; border: 3px solid var(--gold); overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
          <img src="https://mokshara.indevs.in/assets/jyothi.jpeg?v=1.3" alt="Jyothi Talari" style="width: 100%; height: 100%; object-fit: cover; object-position: center 20%;">
        </div>
        <h4 class="author-name" style="margin: 0.2rem 0; font-family: var(--font-heading); font-size: 1.15rem; color: var(--navy-bg); font-weight: 700;">Jyothi Talari</h4>
        <span class="author-title" style="margin-bottom: 0.5rem; font-family: var(--font-ui); font-size: 0.7rem; font-weight: 700; color: var(--teal); text-transform: uppercase; letter-spacing: 0.08em; display: block;">Founder & Wellness Practitioner</span>
        <p class="author-bio" style="text-align: left; font-size: 0.82rem; line-height: 1.5; color: var(--text-muted);">Jyothi combines neuroscience research with practical caregiving insights to help families navigate mental wellness, elderly care, and burnout recovery.</p>
      </div>
      
      <div style="height: 1px; background: rgba(0, 128, 128, 0.1); margin: 1.2rem 0;"></div>
      
      <!-- Founder 2 -->
      <div style="text-align: center;">
        <div style="width: 80px; height: 80px; margin: 0 auto 0.6rem; border-radius: 50%; border: 3px solid var(--gold); overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
          <img src="https://mokshara.indevs.in/assets/devi.jpeg?v=1.3" alt="Devi" style="width: 100%; height: 100%; object-fit: cover; object-position: center 20%;">
        </div>
        <h4 class="author-name" style="margin: 0.2rem 0; font-family: var(--font-heading); font-size: 1.15rem; color: var(--navy-bg); font-weight: 700;">Devi</h4>
        <span class="author-title" style="margin-bottom: 0.5rem; font-family: var(--font-ui); font-size: 0.7rem; font-weight: 700; color: var(--teal); text-transform: uppercase; letter-spacing: 0.08em; display: block;">Founder & Somatic Specialist</span>
        <p class="author-bio" style="text-align: left; font-size: 0.82rem; line-height: 1.5; color: var(--text-muted);">Devi specializes in somatic healing practices, emotional nervous system regulation, and holistic wellness protocols for caregivers and seniors.</p>
      </div>
    </div>
"""

print("Updating original HTML files with the new About the Founders section...")

for html_file in html_files:
    html_path = os.path.join(blog_dir, html_file)
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # Find the author-widget sidebar div
    author_widget = soup.find("div", class_="author-widget")
    if author_widget:
        # Create a new element from about_founders_html
        new_widget_soup = BeautifulSoup(about_founders_html, "html.parser").find("div")
        author_widget.replace_with(new_widget_soup)
        print(f"  Updated About section in {html_file}")
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
            
print("About section update complete!")
