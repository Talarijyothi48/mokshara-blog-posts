import os
import re
import shutil
from PIL import Image

image_dir = r"e:\Mokshshara\blog posts\images"
backup_dir = r"e:\Mokshshara\blog posts\images_backup"
os.makedirs(backup_dir, exist_ok=True)

blog_dir = r"e:\Mokshshara\blog posts"
html_files = [f for f in os.listdir(blog_dir) if f.startswith("mokshara-blog-") and f.endswith(".html")]

files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

print(f"Starting image optimization in {image_dir}...")
conversions = {} # Keep track of renamed files to update HTML

for filename in files:
    src_path = os.path.join(image_dir, filename)
    backup_path = os.path.join(backup_dir, filename)
    
    # Back up the original image
    if not os.path.exists(backup_path):
        shutil.copy(src_path, backup_path)
        
    print(f"Optimizing {filename}...")
    img = Image.open(src_path)
    
    # Resize to a maximum width of 1000px for blog posts (fits mobile and desktop perfectly)
    max_width = 1000
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * float(ratio))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
    # Check if PNG needs transparency. If not, convert to JPEG (saves 90% space)
    is_png = filename.lower().endswith('.png')
    if is_png:
        if img.mode in ('RGBA', 'LA'):
            alpha = img.split()[-1]
            min_alpha = alpha.getextrema()[0]
            if min_alpha == 255:
                # Fully opaque, safe to convert to JPEG
                img = img.convert('RGB')
                is_png = False
            else:
                # Actual transparency exists, keep as PNG but compress it
                img.save(src_path, 'PNG', optimize=True)
                print(f"  Optimized transparent PNG: {os.path.getsize(src_path) // 1024} KB")
                continue
        else:
            # Non-transparent PNG, convert to JPEG
            img = img.convert('RGB')
            is_png = False
            
    if not is_png and filename.lower().endswith('.png'):
        # Converted PNG to JPEG, rename
        base_name = os.path.splitext(filename)[0]
        dest_filename = base_name + '.jpeg'
        dest_path = os.path.join(image_dir, dest_filename)
        img.save(dest_path, 'JPEG', quality=80, optimize=True)
        os.remove(src_path)
        conversions[filename] = dest_filename
        print(f"  Converted PNG to JPEG: {dest_filename} ({os.path.getsize(dest_path) // 1024} KB)")
    else:
        # Already a JPEG, optimize in place
        img.save(src_path, 'JPEG', quality=80, optimize=True)
        print(f"  Optimized JPEG in place: {filename} ({os.path.getsize(src_path) // 1024} KB)")

# If we renamed PNGs to JPEGs, update the image URLs inside the HTML files
if conversions:
    print("\nUpdating image filenames inside HTML source files...")
    for html_file in html_files:
        html_path = os.path.join(blog_dir, html_file)
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        modified = False
        for old_png, new_jpeg in conversions.items():
            # Search for the old image filename in HTML and replace with new
            old_str = f"images/{old_png}"
            new_str = f"images/{new_jpeg}"
            if old_str in html_content:
                html_content = html_content.replace(old_str, new_str)
                modified = True
                print(f"  Updated reference in {html_file}: {old_png} -> {new_jpeg}")
                
        if modified:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

print("\nImage optimization complete!")
