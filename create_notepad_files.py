import os
import shutil

src_export_dir = r"e:\Mokshshara\blog posts\blogger_export"
dest_txt_dir = r"e:\Mokshshara\blogger_notepad_files"

if not os.path.exists(dest_txt_dir):
    os.makedirs(dest_txt_dir)

# Mapping of folder names to user-friendly text filenames
blog_mapping = {
    "mokshara-blog-1-caregiver-burnout": "blog-1-caregiver-burnout.txt",
    "mokshara-blog-2-ai-mental-health": "blog-2-ai-mental-health.txt",
    "mokshara-blog-3-cognitive-resilience": "blog-3-cognitive-resilience.txt",
    "mokshara-blog-4-preventive-care-planning": "blog-4-preventive-care-planning.txt",
    "mokshara-blog-5-mokshara-mission": "blog-5-mokshara-mission.txt"
}

for folderName, textName in blog_mapping.items():
    src_file = os.path.join(src_export_dir, folderName, "post_body_clean.html")
    dest_file = os.path.join(dest_txt_dir, textName)
    
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied clean HTML to text file: {dest_file}")
    else:
        print(f"Source file not found: {src_file}")

print("All notepad-compatible text files generated successfully!")
