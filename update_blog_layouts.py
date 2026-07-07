import os
from bs4 import BeautifulSoup

blog_dir = r"e:\Mokshshara\blog posts"
files = [f for f in os.listdir(blog_dir) if f.startswith("mokshara-blog-") and f.endswith(".html")]

header_html = """
<header class="article-top-header">
  <div class="header-content-left">
    <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjUz8ImkkbVpWI9ehy5ZBeyuNg4BIPO3G860c0Kl8wNeS9n7ArZp5Uy0XXX3vlxF59SploE5wksRVnX0fCw9AGOvOFcRzJU90wfDhZA2sVW_oID9dt-3p5HV36CMeSGPImkdNKG10onxczWEtKRc8F-WHrZecv4nS48WneYxn4KecO6wT-OkM2i79wnvAg/s1600/logo_11zon.jpeg" alt="Mókshara Logo" class="article-header-logo" onerror="this.style.display='none'"/>
    <span class="article-header-brand">Mókshara</span>
  </div>
  <div class="header-content-right">
    <a href="https://mokshara.in/store/" class="btn-visit-store" target="_blank">Visit My Store</a>
  </div>
</header>
"""

footer_html = """
<section class="article-bottom-footer">
  <div class="footer-founders-section">
    <h3>About the Founders &amp; Authors</h3>
    <div class="footer-founder-profiles">
      <div class="footer-founder-card">
        <div class="footer-avatar-container">
          <img src="https://mokshara.indevs.in/assets/jyothi.jpeg" alt="Jyothi Talari" class="footer-avatar" onerror="this.style.display='none'"/>
        </div>
        <h4>Jyothi Talari</h4>
        <span class="footer-role">Founder &amp; Wellness Practitioner</span>
        <p>Jyothi combines neuroscience research with practical caregiving insights to help families navigate mental wellness, elderly care, and burnout recovery.</p>
      </div>
      <div class="footer-founder-card">
        <div class="footer-avatar-container">
          <img src="https://mokshara.indevs.in/assets/devi.jpeg" alt="Devi" class="footer-avatar" onerror="this.style.display='none'"/>
        </div>
        <h4>Devi</h4>
        <span class="footer-role">Founder &amp; Somatic Specialist</span>
        <p>Devi specializes in somatic healing practices, emotional nervous system regulation, and holistic wellness protocols for caregivers and seniors.</p>
      </div>
    </div>
  </div>
  
  <div class="footer-info-section">
    <div class="footer-contact-details">
      <h4>Contact Info</h4>
      <p style="display: flex; align-items: center; justify-content: center; gap: 8px;">
        <svg class="email-icon" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" style="color: #008080;"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        Email: <a href="mailto:support@mokshara.com">support@mokshara.com</a>
      </p>
    </div>
    
    <div class="footer-social-subscribe">
      <h4>Connect &amp; Subscribe</h4>
      <p>Follow us on our channels for daily guides &amp; videos:</p>
      <div class="social-btn-group">
        <a href="https://www.linkedin.com/in/mokshara--wellness" target="_blank" class="btn-social btn-linkedin" style="display: inline-flex; align-items: center; gap: 6px;">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.779-1.75-1.75s.784-1.75 1.75-1.75 1.75.779 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
          LinkedIn
        </a>
        <a href="https://www.youtube.com/@Mokshara7M" target="_blank" class="btn-social btn-youtube" style="display: inline-flex; align-items: center; gap: 6px;">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M23.498 6.163c-.272-1.022-1.074-1.826-2.097-2.099C19.56 3.54 12 3.54 12 3.54s-7.56 0-9.402.524c-1.022.273-1.825 1.077-2.097 2.099C0 8.007 0 12 0 12s0 3.993.501 5.837c.272 1.022 1.075 1.826 2.097 2.099C4.44 20.46 12 20.46 12 20.46s7.56 0 9.402-.524c1.022-.273 1.825-1.077 2.097-2.099C24 15.993 24 12 24 12s0-3.993-.502-5.837zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          YouTube
        </a>
      </div>
    </div>
  </div>

  <div class="footer-copyright">
    &#169; 2026 Mókshara. All Rights Reserved. For educational and caregiver support purposes only. Not a substitute for medical or clinical therapy advice.
  </div>
</section>
"""

custom_styles = """
  /* Article Top Header Styles */
  .article-top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 2rem;
    background: #000022;
    border-bottom: 2px solid #D4AF37;
    font-family: 'Inter', sans-serif;
  }
  .header-content-left {
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }
  .article-header-logo {
    height: 40px;
    width: auto;
    border-radius: 4px;
    border: 1px solid #D4AF37;
  }
  .article-header-brand {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #D4AF37;
    letter-spacing: 0.05em;
  }
  .btn-visit-store {
    display: inline-block;
    background: linear-gradient(135deg, #008080, #004d4d);
    color: #ffffff !important;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-decoration: none;
    padding: 0.5rem 1.2rem;
    border-radius: 4px;
    border: 1px solid #009999;
    box-shadow: 0 4px 10px rgba(0, 128, 128, 0.2);
    transition: all 0.3s ease;
  }
  .btn-visit-store:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0, 128, 128, 0.4);
  }

  /* Article Bottom Footer Styles */
  .article-bottom-footer {
    background: #000022;
    color: rgba(255, 255, 255, 0.7);
    padding: 4rem 2rem 2.5rem;
    border-top: 3px solid #D4AF37;
    font-family: 'Inter', sans-serif;
  }
  .footer-founders-section {
    max-width: 1000px;
    margin: 0 auto 3rem;
  }
  .footer-founders-section h3 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.6rem;
    color: #D4AF37;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 0.05em;
  }
  .footer-founder-profiles {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
  .footer-founder-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(212, 175, 55, 0.1);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
  }
  .footer-avatar-container {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 3px solid #D4AF37;
    overflow: hidden;
    margin: 0 auto 1rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  }
  .footer-avatar {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 8% !important;
  }
  .footer-founder-card h4 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.2rem;
    color: #ffffff;
    margin-bottom: 0.2rem;
  }
  .footer-role {
    font-size: 0.7rem;
    font-weight: 700;
    color: #008080;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: block;
    margin-bottom: 0.8rem;
  }
  .footer-founder-card p {
    font-size: 0.85rem;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.65);
    text-align: left;
    margin: 0;
  }
  .footer-info-section {
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 2rem;
    padding-bottom: 2rem;
  }
  .footer-contact-details h4, .footer-social-subscribe h4 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.25rem;
    color: #ffffff;
    margin-bottom: 0.8rem;
  }
  .footer-contact-details p, .footer-social-subscribe p {
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0;
  }
  .footer-contact-details a {
    color: #008080;
    text-decoration: none;
    font-weight: 600;
  }
  .footer-contact-details a:hover {
    text-decoration: underline;
  }
  .social-btn-group {
    display: flex;
    gap: 1rem;
    margin-top: 0.8rem;
  }
  .btn-social {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #ffffff;
    padding: 0.5rem 1.2rem;
    border-radius: 4px;
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 700;
    transition: all 0.3s ease;
    letter-spacing: 0.05em;
  }
  .btn-linkedin:hover {
    background: #0077b5;
    border-color: #0077b5;
    transform: translateY(-2px);
  }
  .btn-youtube:hover {
    background: #ff0000;
    border-color: #ff0000;
    transform: translateY(-2px);
  }
  .footer-copyright {
    text-align: center;
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.35);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 1.5rem;
    max-width: 1000px;
    margin: 0 auto;
  }
  @media (max-width: 768px) {
    .footer-founder-profiles, .footer-info-section {
      grid-template-columns: 1fr;
    }
  }
"""

for filename in files:
    file_path = os.path.join(blog_dir, filename)
    print(f"Modifying layout for: {filename}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Remove navigation bar
    nav = soup.find("nav")
    if nav:
        nav.decompose()
        
    # Remove toggle button and overlay elements if they exist independently
    for old_toggle in soup.find_all("button", class_="nav-menu-toggle"):
        old_toggle.decompose()
    for old_overlay in soup.find_all("div", id="navMenuOverlay"):
        old_overlay.decompose()
        
    # Remove any existing top header we added previously
    old_header = soup.find(class_="article-top-header")
    if old_header:
        old_header.decompose()
        
    # Remove existing footer (check both old footer tag and section tag)
    old_footer_tag = soup.find("footer")
    if old_footer_tag:
        old_footer_tag.decompose()
        
    old_footer_sec = soup.find("section", class_="article-bottom-footer")
    if old_footer_sec:
        old_footer_sec.decompose()
        
    # Remove custom styles from the style tag
    style_tag = soup.find("style")
    if style_tag and style_tag.string:
        if "/* Article Top Header Styles */" in style_tag.string:
            parts = style_tag.string.split("/* Article Top Header Styles */")
            style_tag.string = parts[0].strip()
            
    # Save the updated source file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
        
print("All source blog layouts cleaned of injected elements successfully!")
