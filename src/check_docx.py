import re
import sys
import hashlib
import zipfile
from pathlib import Path
from urllib.parse import unquote

from docx import Document


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
DOI_URL_RE = re.compile(r"https?://(?:dx\.)?doi\.org/[^\s\]\)\"'，。；;]+", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)

TEMPLATE_TITLE = "Deep representation learning enables cross-basin water quality prediction under data-scarce conditions"
TEMPLATE_DOI = "10.1038/s41545-025-00466-2"
DEFAULT_TEMPLATE_DIRS = [
    Path("data/example format"),
    Path("data/示例模板"),
    Path("data/示例模板文件夹"),
]


def parse_image_target(raw_target):
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        match = re.match(r"(.+?)(?:\s+[\"'][^\"']+[\"'])?$", target)
        if match:
            target = match.group(1)
    return unquote(target.strip())


def markdown_image_refs(md_text):
    refs = []
    for raw_target in IMAGE_RE.findall(md_text):
        target = parse_image_target(raw_target)
        if target.startswith("images/"):
            refs.append(target)
    return refs


def extract_title_lines(md_text):
    titles = []
    for line in md_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line.strip())
        if match:
            titles.append(match.group(1).strip())
        if len(titles) >= 2:
            break
    return titles


def extract_doi_text(paths):
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = DOI_URL_RE.search(text)
        if match:
            return match.group(0).rstrip(".,;:，。；：)")
        match = DOI_RE.search(text)
        if match:
            return match.group(0).rstrip(".,;:，。；：)")
    return ""


def media_hashes(docx_path):
    hashes = set()
    try:
        with zipfile.ZipFile(docx_path) as package:
            for name in package.namelist():
                if name.startswith("word/media/"):
                    hashes.add(hashlib.sha256(package.read(name)).hexdigest())
    except Exception:
        return hashes
    return hashes


def template_media_hashes():
    hashes = set()
    for template_dir in DEFAULT_TEMPLATE_DIRS:
        if not template_dir.exists():
            continue
        for template in template_dir.glob("*.docx"):
            hashes.update(media_hashes(template))
    return hashes


def check_docx(paper_id):
    input_dir = Path("data/input") / paper_id
    md_file = Path("data/output") / f"{paper_id}_summary.md"
    docx_file = Path("data/output") / f"{paper_id}_summary.docx"
    images_dir = input_dir / "images"

    errors = 0
    if not md_file.exists():
        print(f"ERROR: Markdown file not found: {md_file}")
        return 1
    if not docx_file.exists():
        print(f"ERROR: DOCX file not found: {docx_file}")
        return 1

    md_text = md_file.read_text(encoding="utf-8")
    doc = Document(docx_file)
    doc_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    for title in extract_title_lines(md_text):
        if title and title not in doc_text:
            print(f"ERROR: Title missing from DOCX: {title}")
            errors += 1

    image_refs = markdown_image_refs(md_text)
    for ref in image_refs:
        filename = ref.split("images/", 1)[1]
        if not (images_dir / filename).exists():
            print(f"ERROR: Markdown image does not exist: {ref}")
            errors += 1

    if len(doc.inline_shapes) < len(image_refs):
        print(
            f"ERROR: DOCX has {len(doc.inline_shapes)} inline images, "
            f"but markdown references {len(image_refs)} images."
        )
        errors += 1

    doi = extract_doi_text([md_file, input_dir / "full.md", *sorted(input_dir.glob("*.json"))])
    if doi:
        doi_key = doi.replace("https://doi.org/", "")
        if doi_key not in doc_text:
            print(f"ERROR: DOI missing from DOCX: {doi}")
            errors += 1

    title_lines = extract_title_lines(md_text)
    current_title = title_lines[0] if title_lines else ""
    if TEMPLATE_TITLE in doc_text and TEMPLATE_TITLE != current_title:
        print("ERROR: Template title is still present in generated DOCX.")
        errors += 1
    if TEMPLATE_DOI in doc_text and (not doi or TEMPLATE_DOI not in doi):
        print("ERROR: Template DOI is still present in generated DOCX.")
        errors += 1

    leftover_template_media = media_hashes(docx_file) & template_media_hashes()
    if leftover_template_media:
        print(
            "ERROR: Generated DOCX still contains media copied from the reference template."
        )
        errors += 1

    if errors:
        print(f"ERROR: Found {errors} DOCX validation issue(s).")
        return 1

    print(
        f"OK: DOCX validation passed for {paper_id} "
        f"({len(image_refs)} markdown image reference(s), {len(doc.inline_shapes)} inline image(s))."
    )
    return 0


if __name__ == "__main__":
    paper_ids = sys.argv[1:]
    if not paper_ids:
        print("Usage: python src/check_docx.py <paper_id> [paper_id ...]")
        sys.exit(1)

    exit_code = 0
    for paper_id in paper_ids:
        exit_code |= check_docx(paper_id)
    sys.exit(exit_code)
