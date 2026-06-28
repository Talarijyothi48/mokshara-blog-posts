import os
from bs4 import BeautifulSoup

index_path = r"e:\Mokshshara\index.html"
output_path = r"e:\Mokshshara\blogger_homepage_theme_snippet.txt"

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Extract styles
style_tag = soup.find("style")
index_css = style_tag.string if style_tag else ""

# Extract body contents
body = soup.find("body")
body_contents = ""
if body:
    from bs4 import Comment
    # Get all body children as strings, wrapping Comment nodes in <!-- --> tags
    children = []
    for child in body.children:
        if isinstance(child, Comment):
            children.append(f"<!--{child}-->")
        else:
            children.append(str(child))
    body_contents = "".join(children)

snippet_text = f"""===================================================================
MÓKSHARA BLOGGER CUSTOM HOMEPAGE INTEGRATION GUIDE
===================================================================
Follow these 3 simple steps to make your Blogger blog homepage (https://moksharawellness.blogspot.com/)
look exactly like your beautiful custom landing page preview, while keeping your article pages clean!

-------------------------------------------------------------------
STEP 1: CHANGE THE <body> TAG IN BLOGGER
-------------------------------------------------------------------
1. Go to Blogger Dashboard -> Theme -> click arrow next to "Customize" -> "Edit HTML".
2. Search (Ctrl+F) for the <body> tag. It usually looks like:
   <body>   or   <body class='...' ...>
3. Replace the entire <body> tag with this dynamic code:

<body expr:class='data:view.isHomepage ? "is-homepage" : "is-item-page"'>


-------------------------------------------------------------------
STEP 2: ADD THE CSS STYLES BEFORE THE </head> TAG
-------------------------------------------------------------------
1. Search (Ctrl+F) for </head> in the Blogger Theme editor.
2. Paste the following block of code directly on the line above </head>:

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&amp;family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&amp;family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&amp;family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet" />

<style type="text/css">
/* --- Visibility control wrapper classes --- */
.custom-homepage-wrapper {{
  display: none;
}}

/* --- Homepage specific overrides --- */
.is-homepage .custom-homepage-wrapper {{
  display: block !important;
}}
/* Hide Blogger's default post feed and widgets on the main homepage */
.is-homepage .main-outer,
.is-homepage .content-outer,
.is-homepage #main,
.is-homepage .blog-posts,
.is-homepage .post-outer,
.is-homepage .sidebar-container,
.is-homepage .sidebar,
.is-homepage #header,
.is-homepage .header-outer,
.is-homepage .Header-container {{
  display: none !important;
}}

/* --- Article/Item page specific overrides --- */
.is-item-page .custom-homepage-wrapper {{
  display: none !important;
}}
.is-item-page .main-outer,
.is-item-page .content-outer,
.is-item-page #main,
.is-item-page .post-outer {{
  display: block !important;
}}

/* --- Your Custom Landing Page CSS Styles --- */
{index_css}
</style>


-------------------------------------------------------------------
STEP 3: PASTE THE HOMEPAGE HTML RIGHT BELOW <body>
-------------------------------------------------------------------
1. Go to the <body expr:class='...'> tag you modified in Step 1.
2. Directly below that line, paste the following custom homepage block:

<div class='custom-homepage-wrapper'>
{body_contents}
</div>


-------------------------------------------------------------------
3. Save your theme by clicking the floppy disk icon in the top right.
Done! Now your homepage will load the beautiful landing page preview,
and your articles will open as clean Blogger posts when clicked!
===================================================================
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(snippet_text)

print(f"Generated Blogger Theme Snippet Guide at: {output_path}")
