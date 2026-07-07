import os
import re
from bs4 import BeautifulSoup

blog_dir = r"e:\Mokshshara\blog posts"
files = [f for f in os.listdir(blog_dir) if f.startswith("mokshara-blog-") and f.endswith(".html")]

modal_html = """
<!-- Dynamic Footer Modal Overlay -->
<div id="footerModal" class="footer-modal-overlay" style="display:none;">
  <div class="footer-modal-card">
    <button class="footer-modal-close" id="closeModalBtn" aria-label="Close modal">&times;</button>
    <div class="footer-modal-body" id="modalContentBody">
      <!-- Content injected dynamically -->
    </div>
  </div>
</div>

<!-- Full Screen Menu Overlay -->
<div id="navMenuOverlay" class="nav-menu-overlay" style="display:none;">
  <div class="overlay-header">
    <button class="overlay-back-btn" id="overlayCloseBtn" aria-label="Go Back">←</button>
    <span class="overlay-brand">Mókshara</span>
    <button class="overlay-close-btn" id="overlayCloseBtnX" aria-label="Close menu">&times;</button>
  </div>
  
  <div class="overlay-content">
    <div class="overlay-links-section">
      <h3>Navigation</h3>
      <ul class="overlay-menu-links">
        <li><a href="https://moksharawellness.blogspot.com/">Home</a></li>
        <li><a href="https://moksharawellness.blogspot.com/search/label/caregiver%20burnout">Mental Wellness</a></li>
        <li><a href="https://moksharawellness.blogspot.com/search/label/elderly%20care">Elderly Care</a></li>
        <li><a href="https://moksharawellness.blogspot.com/store/caregiver-recovery-blueprint">eBooks</a></li>
        <li><a href="https://moksharawellness.blogspot.com/search/label/mokshara-mission">About Our Mission</a></li>
        <li><a href="https://moksharawellness.blogspot.com/store/caregiver-recovery-blueprint" class="overlay-cta">Get eBook</a></li>
      </ul>
    </div>
    
    <div class="overlay-founders-section">
      <h3>About the Founders</h3>
      <div class="overlay-founder-profiles">
        <div class="overlay-founder-card">
          <div class="overlay-avatar-container">
            <img src="https://mokshara.indevs.in/assets/jyothi.jpeg" alt="Jyothi Talari" class="overlay-avatar">
          </div>
          <h4>Jyothi Talari</h4>
          <span class="overlay-role">Founder & Wellness Practitioner</span>
          <p>Jyothi combines neuroscience research with practical caregiving insights to help families navigate mental wellness, elderly care, and burnout recovery.</p>
        </div>
        
        <div class="overlay-founder-card">
          <div class="overlay-avatar-container">
            <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnj9d2kgKerb6KuTzVwdTl4BNgPoN-wh2Y0c1DuFby4fEEqwZ_-pzkmVMW1ucpz1VEWFnnUn4TfuaEGnMIYXuFw-KB0sFurMgvXi8UuFnZn9Z7L7KWpG77JZPh19XwrkRGgKwcLosCYOsFguCbNikmmnV7WkppvtLMMR4iH9zUajJtBzKx0SBNmtoEl_A/s1600/devi.jpeg" alt="Devi" class="overlay-avatar">
          </div>
          <h4>Devi</h4>
          <span class="overlay-role">Founder & Somatic Specialist</span>
          <p>Devi specializes in somatic healing practices, emotional nervous system regulation, and holistic wellness protocols for caregivers and seniors.</p>
        </div>
      </div>
      
      <div style="margin-top: 2rem; text-align: center;">
        <a href="https://www.linkedin.com/in/jyothi-talari" target="_blank" class="overlay-linkedin-btn">Connect on LinkedIn</a>
      </div>
    </div>
  </div>
</div>
"""

modal_css = """
/* CSS for Footer Modals */
.footer-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 34, 0.75);
  backdrop-filter: blur(8px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  padding: 1.5rem;
}
.footer-modal-overlay.active {
  opacity: 1;
}
.footer-modal-card {
  background: #FAF8F2;
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  padding: 2.5rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  position: relative;
  transform: scale(0.9);
  transition: transform 0.3s ease;
  font-family: 'Source Serif 4', Georgia, serif;
  color: #1A1A2E;
  max-height: 85vh;
  overflow-y: auto;
}
.footer-modal-overlay.active .footer-modal-card {
  transform: scale(1);
}
.footer-modal-close {
  position: absolute;
  top: 1rem;
  right: 1.5rem;
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #5a5a75;
  transition: color 0.3s ease;
  line-height: 1;
}
.footer-modal-close:hover {
  color: #D4AF37;
}
.footer-modal-body h3 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.8rem;
  color: #000022;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 128, 128, 0.15);
  padding-bottom: 0.8rem;
}
.footer-modal-body p {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 1.05rem;
  line-height: 1.65;
  color: #5a5a75;
  margin-bottom: 1rem;
}
.footer-modal-body ul {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
  color: #5a5a75;
}
.footer-modal-body li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* Nav Logo Image */
.nav-logo-img {
  height: 35px;
  width: auto;
  margin-right: 12px;
  vertical-align: middle;
  border-radius: 4px;
}

/* Liked Button red/pink override */
.like-btn.liked {
  background: rgba(224, 36, 94, 0.08) !important;
  border-color: #e0245e !important;
  color: #e0245e !important;
  box-shadow: 0 6px 18px rgba(224, 36, 94, 0.15) !important;
}
.like-btn.liked .heart-icon {
  color: #e0245e !important;
}

/* Navigation Header Adjustments */
.nav-back-arrow {
  color: #D4AF37 !important;
  font-size: 1.8rem !important;
  text-decoration: none !important;
  margin-right: 15px !important;
  display: none !important; /* hidden by default, shown dynamically via JS */
  align-items: center !important;
  justify-content: center !important;
  font-weight: bold !important;
  line-height: 1 !important;
  cursor: pointer !important;
  outline: none !important;
}

.nav-menu-toggle {
  background: none !important;
  border: none !important;
  color: #D4AF37 !important;
  font-size: 1.8rem !important;
  cursor: pointer !important;
  padding: 0 !important;
  margin-right: 18px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
  outline: none !important;
  transition: transform 0.2s ease !important;
}
.nav-menu-toggle:hover {
  transform: scale(1.1) !important;
}

.nav-links {
  margin-left: auto !important;
}

/* Full Screen Menu Overlay Styles */
.nav-menu-overlay {
  position: fixed !important;
  inset: 0 !important;
  background: #000022 !important;
  color: #ffffff !important;
  z-index: 15000 !important;
  display: flex !important;
  flex-direction: column !important;
  opacity: 0 !important;
  pointer-events: none !important;
  transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
  padding: 2rem 3rem !important;
  overflow-y: auto !important;
}
.nav-menu-overlay.active {
  opacity: 1 !important;
  pointer-events: auto !important;
}
.overlay-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  border-bottom: 1px solid rgba(212, 175, 55, 0.15) !important;
  padding-bottom: 1.2rem !important;
  margin-bottom: 2.5rem !important;
  width: 100% !important;
}
.overlay-brand {
  font-family: 'Playfair Display', Georgia, serif !important;
  font-size: 1.8rem !important;
  color: #D4AF37 !important;
  font-weight: bold !important;
  letter-spacing: 0.05em !important;
}
.overlay-back-btn, .overlay-close-btn {
  background: none !important;
  border: none !important;
  color: #D4AF37 !important;
  font-size: 2rem !important;
  cursor: pointer !important;
  line-height: 1 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0.5rem !important;
  transition: color 0.3s ease, transform 0.2s ease !important;
}
.overlay-back-btn:hover, .overlay-close-btn:hover {
  color: #ffffff !important;
  transform: scale(1.1) !important;
}

.overlay-content {
  display: grid !important;
  grid-template-columns: 1fr 1.8fr !important;
  gap: 4rem !important;
  max-width: 1200px !important;
  width: 100% !important;
  margin: 0 auto !important;
  flex-grow: 1 !important;
}

.overlay-links-section h3, .overlay-founders-section h3 {
  font-family: 'Playfair Display', Georgia, serif !important;
  font-size: 1.35rem !important;
  color: #D4AF37 !important;
  margin-bottom: 1.8rem !important;
  border-bottom: 1px solid rgba(0, 128, 128, 0.2) !important;
  padding-bottom: 0.6rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}

.overlay-menu-links {
  list-style: none !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 1.5rem !important;
}
.overlay-menu-links a {
  color: rgba(255, 255, 255, 0.9) !important;
  text-decoration: none !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 1.25rem !important;
  font-weight: 600 !important;
  transition: color 0.3s ease, padding-left 0.3s ease !important;
  display: block !important;
}
.overlay-menu-links a:hover {
  color: #D4AF37 !important;
  padding-left: 8px !important;
}
.overlay-cta {
  background: linear-gradient(135deg, #008080, #004d4d) !important;
  color: #ffffff !important;
  text-align: center !important;
  padding: 0.8rem !important;
  border-radius: 6px !important;
  border: 1px solid #009999 !important;
  margin-top: 1rem !important;
}
.overlay-cta:hover {
  padding-left: 0 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 15px rgba(0, 128, 128, 0.3) !important;
}

.overlay-founder-profiles {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 2rem !important;
}
.overlay-founder-card {
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(212, 175, 55, 0.1) !important;
  border-radius: 12px !important;
  padding: 1.8rem 1.5rem !important;
  text-align: center !important;
}
.overlay-avatar-container {
  width: 90px !important;
  height: 90px !important;
  margin: 0 auto 0.8rem !important;
  border-radius: 50% !important;
  border: 3px solid #D4AF37 !important;
  overflow: hidden !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
}
.overlay-avatar {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: center 20% !important;
}
.overlay-founder-card h4 {
  font-family: 'Libre Baskerville', Georgia, serif !important;
  font-size: 1.15rem !important;
  color: #ffffff !important;
  margin: 0.4rem 0 0.2rem !important;
}
.overlay-role {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  color: #008080 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  display: block !important;
  margin-bottom: 0.8rem !important;
}
.overlay-founder-card p {
  font-family: 'Source Serif 4', Georgia, serif !important;
  font-size: 0.85rem !important;
  line-height: 1.55 !important;
  color: rgba(255, 255, 255, 0.7) !important;
  text-align: left !important;
  margin: 0 !important;
}
.overlay-linkedin-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: #0077b5 !important;
  color: #ffffff !important;
  text-decoration: none !important;
  padding: 0.6rem 2.2rem !important;
  border-radius: 4px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  transition: background 0.3s ease !important;
  margin-top: 1.5rem !important;
}
.overlay-linkedin-btn:hover {
  background: #005a87 !important;
}

@media (max-width: 992px) {
  .overlay-content {
    grid-template-columns: 1fr !important;
    gap: 3rem !important;
  }
}
@media (max-width: 768px) {
  .nav-links {
    display: none !important; /* Hide old dropdown */
  }
  .nav-menu-toggle {
    margin-right: 10px !important;
  }
}
@media (max-width: 576px) {
  .overlay-founder-profiles {
    grid-template-columns: 1fr !important;
  }
  .nav-menu-overlay {
    padding: 1.5rem 1.5rem !important;
  }
}

"""

modal_js = """
// Dynamic Footer Links Modal Content
const modalData = {
  about: `
    <h3>About the Founders</h3>
    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; margin-top: 1.5rem;">
      <div style="flex: 1; min-width: 240px; text-align: center; background: rgba(0,128,128,0.03); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0,128,128,0.1);">
        <img src="https://mokshara.indevs.in/assets/jyothi.jpeg" alt="Jyothi Talari" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #D4AF37; object-fit: cover; object-position: center 20% !important; margin-bottom: 0.8rem; display: inline-block;">
        <h4 style="margin: 0.2rem 0; font-size: 1.2rem; font-weight: 700; color: #000022;">Jyothi Talari</h4>
        <span style="font-size: 0.72rem; font-weight: 700; color: #008080; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 0.8rem;">Founder & Wellness Practitioner</span>
        <p style="font-size: 0.85rem; line-height: 1.5; color: #5a5a75; text-align: left; margin: 0;">Jyothi combines neuroscience research with practical caregiving insights to help families navigate mental wellness, elderly care, and burnout recovery.</p>
      </div>
      <div style="flex: 1; min-width: 240px; text-align: center; background: rgba(0,128,128,0.03); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(0,128,128,0.1);">
        <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnj9d2kgKerb6KuTzVwdTl4BNgPoN-wh2Y0c1DuFby4fEEqwZ_-pzkmVMW1ucpz1VEWFnnUn4TfuaEGnMIYXuFw-KB0sFurMgvXi8UuFnZn9Z7L7KWpG77JZPh19XwrkRGgKwcLosCYOsFguCbNikmmnV7WkppvtLMMR4iH9zUajJtBzKx0SBNmtoEl_A/s1600/devi.jpeg" alt="Devi" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #D4AF37; object-fit: cover; object-position: center 20% !important; margin-bottom: 0.8rem; display: inline-block;">
        <h4 style="margin: 0.2rem 0; font-size: 1.2rem; font-weight: 700; color: #000022;">Devi</h4>
        <span style="font-size: 0.72rem; font-weight: 700; color: #008080; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 0.8rem;">Founder & Somatic Specialist</span>
        <p style="font-size: 0.85rem; line-height: 1.5; color: #5a5a75; text-align: left; margin: 0;">Devi specializes in somatic healing practices, emotional nervous system regulation, and holistic wellness protocols for caregivers and seniors.</p>
      </div>
    </div>
  `,
  editorial: `
    <h3>Editorial Standards</h3>
    <p>Mókshara upholds absolute scientific and clinical integrity. Every guide, metric, and recovery pathway is cross-checked against peer-reviewed clinical publications from leading institutions like Harvard Health, PubMed, the World Health Organization (WHO), and the AARP Caregiving Alliance.</p>
    <p>Our core content review board includes mental health advocates and care professionals to ensure every piece of advice is safe, proactive, and actionable.</p>
  `,
  brand: `
    <h3>Brand Guidelines</h3>
    <p>The Mókshara aesthetic is built around three core pillars: Calm, Trust, and Authority.</p>
    <ul>
      <li><strong>Teal (#008080)</strong> represents healing, clarity, and mental wellness.</li>
      <li><strong>Gold (#D4AF37)</strong> represents light, restoration, and the premium quality of our resources.</li>
      <li><strong>Cream (#FAF8F2)</strong> provides a warm, non-clinical background to reduce reader stress.</li>
    </ul>
    <p>All content and tools must maintain a calm, authoritative, and non-judgmental tone.</p>
  `,
  privacy: `
    <h3>Privacy Policy</h3>
    <p>Your trust is paramount. Mókshara maintains a strict privacy posture:</p>
    <ul>
      <li><strong>No data tracking:</strong> Any information you click or input on our interactive stress-testing dashboards or checklists is processed locally in your browser. We never collect, transmit, or store your private wellness inputs.</li>
      <li><strong>Local Storage:</strong> Interactive preferences (like your article likes) are saved directly on your device so they persist across visits, but they never leave your browser.</li>
    </ul>
  `,
  contact: `
    <h3>Contact Support</h3>
    <p>We are here to support your wellness and caregiving journey. If you have questions about our guidelines, eBooks, or resource tools, feel free to reach out:</p>
    <ul>
      <li>📧 Email: <a href="mailto:support@mokshara.com" style="color:#008080;">support@mokshara.com</a></li>
      <li>💼 Creator LinkedIn: <a href="https://www.linkedin.com/in/jyothi-talari" target="_blank" style="color:#008080;">Jyothi Talari</a></li>
    </ul>
  `
};

document.addEventListener('DOMContentLoaded', () => {
  const footerLinks = document.querySelectorAll('.footer-links a');
  const navLinks = document.querySelectorAll('.nav-links a');
  const modalOverlay = document.getElementById('footerModal');
  const modalBody = document.getElementById('modalContentBody');
  const closeModalBtn = document.getElementById('closeModalBtn');
  
  // Navigation Menu Toggle (Full Screen Overlay)
  const toggleBtn = document.querySelector('.nav-menu-toggle');
  const navMenuOverlay = document.getElementById('navMenuOverlay');
  const overlayCloseBtn = document.getElementById('overlayCloseBtn');
  const overlayCloseBtnX = document.getElementById('overlayCloseBtnX');

  const openOverlay = () => {
    if (navMenuOverlay) {
      navMenuOverlay.style.display = 'flex';
      setTimeout(() => navMenuOverlay.classList.add('active'), 10);
      document.body.style.overflow = 'hidden'; // prevent scrolling behind overlay
    }
  };

  const closeOverlay = () => {
    if (navMenuOverlay) {
      navMenuOverlay.classList.remove('active');
      setTimeout(() => {
        navMenuOverlay.style.display = 'none';
        document.body.style.overflow = ''; // restore scroll
      }, 350);
    }
  };

  if (toggleBtn && navMenuOverlay) {
    toggleBtn.addEventListener('click', openOverlay);
  }

  if (overlayCloseBtn) overlayCloseBtn.addEventListener('click', closeOverlay);
  if (overlayCloseBtnX) overlayCloseBtnX.addEventListener('click', closeOverlay);

  // Close overlay on link clicks
  const overlayLinks = document.querySelectorAll('.overlay-menu-links a');
  overlayLinks.forEach(link => {
    link.addEventListener('click', closeOverlay);
  });

  if (modalOverlay && modalBody) {
    // Intercept footer link clicks
    if (footerLinks) {
      footerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
          const text = link.textContent.trim().toLowerCase();
          if (text.includes('about')) {
            e.preventDefault();
            openOverlay();
          } else {
            let key = '';
            if (text.includes('editorial')) key = 'editorial';
            else if (text.includes('brand') || text.includes('guidelines')) key = 'brand';
            else if (text.includes('privacy')) key = 'privacy';
            else if (text.includes('contact')) key = 'contact';
            
            if (key && modalData[key]) {
              e.preventDefault();
              modalBody.innerHTML = modalData[key];
              modalOverlay.style.display = 'flex';
              setTimeout(() => modalOverlay.classList.add('active'), 10);
            }
          }
        });
      });
    }
    
    // Intercept top nav ABOUT link click to open the full screen overlay
    const aboutLinks = document.querySelectorAll('.nav-about-link, a[href="#about"], a[href*="mokshara-mission"]');
    aboutLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        openOverlay();
      });
    });
    
    const closeModal = () => {
      modalOverlay.classList.remove('active');
      setTimeout(() => modalOverlay.style.display = 'none', 300);
    };
    
    if (closeModalBtn) {
      closeModalBtn.addEventListener('click', closeModal);
    }
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
  }

  // Handle back arrow visibility dynamically (shows on article pages, hides on homepage)
  const backArrow = document.getElementById('navBackArrow');
  if (backArrow) {
    if (window.location.pathname !== '/' && window.location.pathname !== '/index.html' && !window.location.pathname.endsWith('.blogspot.com/')) {
      backArrow.style.setProperty('display', 'inline-flex', 'important');
    } else {
      backArrow.style.setProperty('display', 'none', 'important');
    }
  }
});
"""

for filename in files:
    file_path = os.path.join(blog_dir, filename)
    print(f"Updating links and footer modal in: {filename}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    
    # 0. Wrap all scripts in an IIFE and readyState checker to prevent variable collisions and execution timing issues on Blogger
    scripts_tags = soup.find_all("script")
    for script_tag in scripts_tags:
        # Skip json-ld and script templates without content
        if script_tag.get("type") == "application/ld+json" or not script_tag.string:
            continue
        script_code = script_tag.string.strip()
        # Avoid double-wrapping if already wrapped
        if not script_code.startswith("(function()"):
            wrapped_code = f"(function() {{\n  function initPost() {{\n{script_code}\n  }}\n  if (document.readyState === 'loading') {{\n    document.addEventListener('DOMContentLoaded', initPost);\n  }} else {{\n    initPost();\n  }}\n}})();"
            script_tag.string = wrapped_code
    
    # 1. Update Navigation Links
    nav = soup.find("nav")
    if nav:
        brand = nav.find("a", class_="nav-brand")
        if brand:
            brand["href"] = "https://moksharawellness.blogspot.com/"
            # Insert logo image if it does not exist
            img = brand.find("img")
            if not img:
                logo_tag = soup.new_tag("img", src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhgruE9nwPItaS4avpn9h61DqqyrRmO-RKZfG4IbVk5EDivLXx03AOYpHuAcGjksfvg_Eb2PHJ-8cq-fPMouMUEkbhPRQ9XG5UVPRx5OTNc5LXj7esKjm0IFQ1mfDMYEnD-WQahbmle9Fg50GF_boOfvA8mzXPZ3FSl38yQtVAjDzWsdamohyKNvwX6Zao/s1600/logo.jpeg", alt="Mókshara Logo")
                logo_tag["class"] = "nav-logo-img"
                brand.insert(0, logo_tag)
            
            # Decompose duplicates (handling both class and class_ syntax)
            for old_toggle in nav.find_all("button", class_="nav-menu-toggle"):
                old_toggle.decompose()
            for old_toggle_bug in nav.find_all("button", attrs={"class_": "nav-menu-toggle"}):
                old_toggle_bug.decompose()
                
            for old_back in nav.find_all("a", class_="nav-back-arrow"):
                old_back.decompose()
            for old_back_bug in nav.find_all("a", attrs={"class_": "nav-back-arrow"}):
                old_back_bug.decompose()
            
            # Insert back arrow with correct attrs class
            back_arrow_tag = soup.new_tag("a", href="https://moksharawellness.blogspot.com/", id="navBackArrow", attrs={"class": "nav-back-arrow"})
            back_arrow_tag.string = "←"
            brand.insert_before(back_arrow_tag)
            
            # Insert menu toggle button with correct attrs class
            toggle_tag = soup.new_tag("button", attrs={"class": "nav-menu-toggle", "aria-label": "Toggle Navigation"})
            toggle_tag.string = "☰"
            brand.insert_before(toggle_tag)
        
        links = nav.find_all("a")
        for link in links:
            text = link.text.strip().lower()
            if text == "home":
                link["href"] = "https://moksharawellness.blogspot.com/"
            elif text == "mental wellness":
                link["href"] = "https://moksharawellness.blogspot.com/search/label/caregiver%20burnout"
            elif text == "elderly care":
                link["href"] = "https://moksharawellness.blogspot.com/search/label/elderly%20care"
            elif text == "ebooks":
                link["href"] = "https://moksharawellness.blogspot.com/store/caregiver-recovery-blueprint"
            elif text == "about":
                link["href"] = "#about"
                link["class"] = "nav-about-link"
            elif text == "get ebook":
                link["href"] = "https://moksharawellness.blogspot.com/store/caregiver-recovery-blueprint"
                
    # 2. Update Footer Links
    footer = soup.find("footer")
    if footer:
        links = footer.find_all("a")
        for link in links:
            link["href"] = "#"
            
    # Remove any existing injected css/html/js modal content if we are re-running
    existing_css = soup.find("style", string=re.compile("CSS for Footer Modals"))
    if existing_css:
        existing_css.decompose()
        
    existing_modal = soup.find("div", id="footerModal")
    if existing_modal:
        existing_modal.decompose()
        
    existing_js = soup.find("script", string=re.compile("Dynamic Footer Links Modal Content"))
    if existing_js:
        existing_js.decompose()
        
    # 3. Add CSS block
    head = soup.find("head")
    if head:
        style_tag = soup.new_tag("style", type="text/css")
        style_tag.string = modal_css
        head.append(style_tag)
        
    # 4. Add HTML modal block
    body = soup.find("body")
    if body:
        modal_soup = BeautifulSoup(modal_html, "html.parser")
        body.append(modal_soup)
        
        # 5. Add JS script block
        js_tag = soup.new_tag("script", type="text/javascript")
        js_tag.string = modal_js
        body.append(js_tag)
        
    # Write back the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
        
print("All source files updated successfully!")
