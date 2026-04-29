import sys
import re
from pathlib import Path
from urllib.parse import unquote

def check_images(images_dir, md_file):
    """
    Check if all images referenced in the minimal markdown output actually exist.
    Returns 0 when valid, 1 when errors are found.
    """
    images_dir = Path(images_dir)
    md_file = Path(md_file)
    
    if not md_file.exists():
        print(f"ERROR: Markdown file not found: {md_file}")
        return 1
        
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    img_refs = []
    for raw_target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', content):
        target = raw_target.strip()
        if target.startswith("<") and ">" in target:
            target = target[1:target.index(">")]
        elif target.startswith("images/"):
            # Drop an optional Markdown title: ![alt](images/a.png "title")
            title_match = re.match(r'(images/.*?)(?:\s+["\'][^"\']*["\'])?$', target)
            if title_match:
                target = title_match.group(1)
        if target.startswith("images/"):
            img_refs.append(target)
    
    if not img_refs:
        print("INFO: No image references found in the markdown.")
        return 0

    if not images_dir.exists():
        print(f"ERROR: Images directory not found: {images_dir}")
        return 1
        
    errors = 0
    print(f"Checking {len(img_refs)} image references...")
    for ref in img_refs:
        # Remove 'images/' part to check the actual file in the provided images_dir
        filename = unquote(ref.split("images/", 1)[-1])
        actual_path = images_dir / filename
        
        if not actual_path.exists():
            print(f"  ERROR: Broken link: '{ref}' does not exist.")
            errors += 1
            
    if errors == 0:
        print("OK: All image links are valid.")
    else:
        print(f"ERROR: Found {errors} broken image links!")
    return 1 if errors else 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_images.py <path_to_images_dir> <path_to_output_md>")
        sys.exit(1)
    
    sys.exit(check_images(sys.argv[1], sys.argv[2]))
