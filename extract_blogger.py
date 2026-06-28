import os
import re
import copy
from bs4 import BeautifulSoup

def clean_html(text):
    # Helper to clean text
    return text.strip()

def process_all_blogs():
    blog_dir = r"e:\Mokshshara\blog posts"
    export_dir = os.path.join(blog_dir, "blogger_export")
    os.makedirs(export_dir, exist_ok=True)
    
    print(f"Scanning for blogs in {blog_dir}...")
    files = [f for f in os.listdir(blog_dir) if f.startswith("mokshara-blog-") and f.endswith(".html")]
    
    for filename in files:
        file_path = os.path.join(blog_dir, filename)
        name_without_ext = os.path.splitext(filename)[0]
        
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        
        # 1. Extract Title (strip brand name at the end)
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else ""
        title = re.sub(r"\s*\|\s*Mókshara\s*$", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s*\|\s*Mokshara\s*$", "", title, flags=re.IGNORECASE)
        title = title.strip()
        
        # 2. Extract Search Description (meta description)
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag else ""
        
        # 3. Extract Keywords as Labels
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        labels = keywords_tag["content"].strip() if keywords_tag else ""
        
        # 4. Extract Custom Permalink
        canonical_tag = soup.find("link", rel="canonical")
        permalink = ""
        if canonical_tag and "href" in canonical_tag.attrs:
            href = canonical_tag["href"]
            match = re.search(r"/([^/]+)\.html$", href)
            if match:
                permalink = match.group(1)
        if not permalink:
            permalink = name_without_ext
            
        # 5. Extract Style Block & Add Blogger Overrides
        style_tag = soup.find("style")
        style_content = style_tag.string if style_tag else ""
        
        # Prevent Blogger's HTML escape bug on CSS pseudo-element content quotes
        # Replace raw quotes with safe CSS unicode escape sequences
        style_content = re.sub(r"content:\s*['\"]“['\"];", "content: '\\\\201C';", style_content)
        style_content = re.sub(r"content:\s*['\"]”['\"];", "content: '\\\\201D';", style_content)
        style_content = re.sub(r"content:\s*['\"]\"['\"];", "content: '\\\\201C';", style_content)
        style_content = re.sub(r"content:\s*['\"]'['\"];", "content: '\\\\2018';", style_content)
        
        # Replace heart symbols to prevent &#9825; and &#9829; text output
        style_content = re.sub(r"content:\s*['\"](?:♡|â™¡)['\"];", "content: '\\\\2661';", style_content)
        style_content = re.sub(r"content:\s*['\"](?:♥|â™¥)['\"];", "content: '\\\\2665';", style_content)
        
        # Replace star icons to prevent &#10022; text output
        style_content = re.sub(r"content:\s*['\"](?:✦|âœ¦)['\"];", "content: '\\\\2726';", style_content)
        
        # Replace microscope emojis to prevent &#128300; text output
        style_content = re.sub(r"content:\s*['\"]🔬['\"];", "content: '\\\\1F52C';", style_content)
        
        extra_css = """
/* === BLOGGER.COM POST CONTAINER OVERRIDES === */
.sidebar, aside {
  display: none !important;
}
body {
  background: var(--cream) !important;
}

/* Fix main post column sizing */
.layout-container {
  grid-template-columns: 1fr !important;
  max-width: 800px !important;
  margin: 0 auto !important;
  padding: 2rem 1.5rem !important;
}

/* Disable scroll-reveal opacity-hide by default inside Blogger post editor/previews */
/* This prevents empty white spaces and ensures 100% visibility even if JS is blocked */
.reveal, .reveal-left, .reveal-right, .reveal-scale {
  opacity: 1 !important;
  transform: none !important;
  transition: none !important;
}

/* Fix Hero section layout to match actual desktop design (two columns side-by-side) */
.hero {
  min-height: auto !important;
  padding: 5rem 2rem !important;
  background: linear-gradient(135deg, var(--navy-bg) 0%, #050d24 60%, #002222 100%) !important;
}
.hero-container {
  grid-template-columns: 1.2fr 0.8fr !important;
  gap: 2.5rem !important;
  text-align: left !important;
  display: grid !important;
  align-items: center !important;
}
.hero-left {
  text-align: left !important;
}
.hero-tag, .hero-pill, .hero-badge {
  margin-left: 0 !important;
  margin-right: auto !important;
  display: inline-flex !important;
}
.hero-meta, .hero-meta-row {
  display: flex !important;
  justify-content: flex-start !important;
  flex-wrap: wrap !important;
  gap: 1.5rem !important;
}
.hero-meta span {
  display: inline-flex !important;
  align-items: center !important;
}
/* Style any image in hero-right (original or uploaded in Blogger) to have the premium gradient frame */
.hero-right img {
  display: block !important;
  width: 100% !important;
  max-width: 440px !important;
  border-radius: 16px !important;
  padding: 6px !important;
  background: linear-gradient(135deg, var(--gold), var(--teal)) !important;
  box-shadow: 0 20px 50px rgba(0,0,0,0.4) !important;
  aspect-ratio: 4/3 !important;
  margin: 0 auto !important;
  object-fit: cover !important;
}

/* Mobile responsive stacked layout for the Hero section */
@media (max-width: 768px) {
  .hero {
    padding: 3rem 1rem !important;
  }
  .hero-container {
    grid-template-columns: 1fr !important;
    gap: 2rem !important;
    text-align: center !important;
  }
  .hero-left {
    text-align: center !important;
  }
  .hero-tag, .hero-pill, .hero-badge {
    margin-left: auto !important;
    margin-right: auto !important;
  }
  .hero-meta, .hero-meta-row {
    justify-content: center !important;
  }
  .hero-right {
    order: -1 !important; /* Image on top on mobile */
  }
}

/* Ensure no empty hero-frame containers render as a green card if left behind */
.hero-frame {
  background: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  aspect-ratio: auto !important;
  width: auto !important;
  height: auto !important;
  border-radius: 0 !important;
}

/* Fix other layout elements for a single column view */
.stat-grid {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)) !important;
  gap: 1.5rem !important;
}
.dashboard-grid, .verdict-grid, .efficacy-bars {
  grid-template-columns: 1fr !important;
  gap: 2rem !important;
}
.cta-banner {
  grid-template-columns: 1fr !important;
  text-align: center !important;
  padding: 2.5rem 2rem !important;
}
.cta-right {
  display: none !important; /* Hide eBook 3D mockup on mobile/narrow layouts */
}
.wide-pullquote {
  margin: 2rem 0 !important;
  width: 100% !important;
  padding: 2.5rem 2rem !important;
}
.article-visual {
  margin: 2rem 0 !important;
  width: 100% !important;
}
.visual-stat {
  flex-direction: column !important;
  text-align: center !important;
  gap: 1rem !important;
}
.use-step {
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
}
.use-step-num {
  margin-bottom: 0.5rem !important;
}

@media (max-width: 768px) {
  .layout-container {
    padding: 2rem 1rem !important;
  }
}
"""
        style_content_full = style_content.strip() + "\n" + extra_css
        styled_block = f"<style type=\"text/css\">\n/*<![CDATA[*/\n{style_content_full}\n/*]]>*/\n</style>"
        
        # 5.5. Extract Nav (or new custom article header)
        nav_tag = soup.find("nav")
        header_tag = soup.find(class_="article-top-header")
        nav_html = ""
        if header_tag:
            nav_html = str(header_tag)
        elif nav_tag:
            nav_html = str(nav_tag)
        
        # 6. Extract Hero Section
        hero_section = soup.find("section", class_="hero")
        if hero_section:
            # Unwrap the hero-frame container to prevent Blogger editor duplicate/empty cards
            hero_frame = hero_section.find(class_="hero-frame")
            if hero_frame:
                hero_frame.unwrap()
        hero_html = str(hero_section) if hero_section else ""
        
        # 7. Extract Stat Strip
        stat_strip = soup.find("div", class_="stat-strip")
        stat_html = str(stat_strip) if stat_strip else ""
        
        # 8. Extract Layout Container (without sidebar)
        layout_container = soup.find("div", class_="layout-container")
        layout_html = ""
        if layout_container:
            layout_copy = copy.copy(layout_container)
            sidebar = layout_copy.find("aside", class_="sidebar")
            if sidebar:
                sidebar.decompose()
            layout_html = str(layout_copy)
        else:
            main_section = soup.find("main")
            if main_section:
                layout_html = str(main_section)
            else:
                article_section = soup.find("article")
                layout_html = str(article_section) if article_section else ""
                
        # 8.5. Extract Footer (or new custom article bottom section)
        footer_tag = soup.find("footer")
        footer_sec = soup.find("section", class_="article-bottom-footer")
        footer_html = ""
        if footer_sec:
            footer_html = str(footer_sec)
        elif footer_tag:
            footer_html = str(footer_tag)
                
        # 9. Extract script elements (including ld+json for SEO schema)
        scripts = soup.find_all("script")
        scripts_html_list = []
        for s in scripts:
            script_code = s.string if s.string else s.text
            if s.get("type") == "application/ld+json":
                # Keep JSON-LD exactly as is, without CDATA comments (which break JSON)
                scripts_html_list.append(f'<script type="application/ld+json">\n{script_code}\n</script>')
            else:
                # Wrap script contents in CDATA comments to satisfy Blogger XML validator
                scripts_html_list.append(f"<script type=\"text/javascript\">\n//<![CDATA[\n{script_code}\n//]]>\n</script>")
        scripts_html = "\n".join(scripts_html_list)
        
        # Rebuild Post Body HTML
        post_body_html = f"{styled_block}\n\n{hero_html}\n\n{stat_html}\n\n{layout_html}\n\n{scripts_html}"
        
        # Create Export Directory for this blog post
        blog_export_dir = os.path.join(export_dir, name_without_ext)
        os.makedirs(blog_export_dir, exist_ok=True)
        
        # Write metadata.txt
        metadata_content = f"=== BLOGGER POST METADATA ===\n" \
                           f"TITLE: {title}\n" \
                           f"DESCRIPTION: {description}\n" \
                           f"LABELS: {labels}\n" \
                           f"PERMALINK: {permalink}\n"
                           
        with open(os.path.join(blog_export_dir, "metadata.txt"), "w", encoding="utf-8") as meta_file:
            meta_file.write(metadata_content)
            
        # Write post_body.html
        with open(os.path.join(blog_export_dir, "post_body.html"), "w", encoding="utf-8") as body_file:
            body_file.write(post_body_html)
            
        print(f"Processed: {filename} -> Exported to blogger_export/{name_without_ext}/")

if __name__ == "__main__":
    process_all_blogs()
