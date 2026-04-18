import sys
import re
from pathlib import Path

# Common first-person academic phrases to avoid
FORBIDDEN_PHRASES = [
    r'我们(发现|提出|展示|开发|建立|认为|观察到)',
    r'本研究',
    r'本文',
    r'我们的(方法|研究|方案|模型)',
    r'\bwe\s+(found|show|propose|present|develop|introduce)',
    r'\bour\s+(study|research|approach|method|model)'
]

def check_phrases(md_file):
    """
    Scan markdown output for first-person/author-perspective phrases.
    """
    md_file = Path(md_file)
    if not md_file.exists():
        print(f"❌ Markdown file not found: {md_file}")
        return
        
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    errors = 0
    print("🔍 Scanning for forbidden first-person phrases...")
    
    for pattern in FORBIDDEN_PHRASES:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            print(f"  ❌ Line {line_num}: found forbidden phrase '{match.group()}'")
            errors += 1
            
    if errors == 0:
        print("✅ No first-person phrasing detected. Academic tone is preserved.")
    else:
        print(f"⚠️ Found {errors} instances of inappropriate phrasing that need rewriting!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_phrases.py <path_to_output_md>")
        sys.exit(1)
        
    check_phrases(sys.argv[1])
