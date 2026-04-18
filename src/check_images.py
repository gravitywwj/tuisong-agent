import sys
import re
import os
from pathlib import Path

def check_images(images_dir, md_file):
    """
    Check if all images referenced in the minimal markdown output actually exist.
    """
    images_dir = Path(images_dir)
    md_file = Path(md_file)
    
    if not md_file.exists():
        print(f"❌ Markdown file not found: {md_file}")
        return
        
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract image links ![...](images/...)
    img_refs = re.findall(r'!\[.*?\]\((images/[^)]+)\)', content)
    
    if not img_refs:
        print("ℹ️ No image references found in the markdown.")
        return
        
    errors = 0
    print(f"🔍 Checking {len(img_refs)} image references...")
    for ref in img_refs:
        # Remove 'images/' part to check the actual file in the provided images_dir
        filename = ref.split("images/")[-1]
        actual_path = images_dir / filename
        
        if not actual_path.exists():
            print(f"  ❌ Broken Link: '{ref}' does not exist.")
            errors += 1
            
    if errors == 0:
        print("✅ All image links are valid.")
    else:
        print(f"⚠️ Found {errors} broken image links!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_images.py <path_to_images_dir> <path_to_output_md>")
        sys.exit(1)
    
    check_images(sys.argv[1], sys.argv[2])
