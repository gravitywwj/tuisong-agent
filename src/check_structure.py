import re
import sys
from pathlib import Path


FORBIDDEN_HEADINGS = {"环境意义", "精读结论", "精度结论"}
REQUIRED_HEADING = "结论"
MAX_CHINESE_SECTION_CHARS = 18
MAX_CORE_FINDING_SECTIONS = 4


def visible_heading_text(line):
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
    if not match:
        return None, None
    level = len(match.group(1))
    text = re.sub(r"[*_`]+", "", match.group(2)).strip()
    return level, text


def cjk_char_count(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def check_structure(md_file):
    md_file = Path(md_file)
    if not md_file.exists():
        print(f"ERROR: Markdown file not found: {md_file}")
        return 1

    content = md_file.read_text(encoding="utf-8")
    errors = 0
    has_conclusion = False
    in_core_findings = False
    core_finding_sections = 0

    print("Checking output structure and heading length...")
    for line_number, line in enumerate(content.splitlines(), start=1):
        level, text = visible_heading_text(line)
        if level is None:
            continue

        normalized = re.sub(r"^\d+[\.\s、-]+", "", text).strip()
        if level == 2:
            in_core_findings = normalized.startswith("主要内容")
        elif in_core_findings and level <= 2:
            in_core_findings = False
        elif in_core_findings and level == 3:
            core_finding_sections += 1

        if normalized in FORBIDDEN_HEADINGS:
            print(f"  ERROR: Line {line_number}: forbidden heading '{text}'")
            errors += 1
        if normalized == REQUIRED_HEADING:
            has_conclusion = True

        if cjk_char_count(text) == 0:
            continue
        if level >= 2 and cjk_char_count(text) > MAX_CHINESE_SECTION_CHARS:
            print(
                f"  ERROR: Line {line_number}: section heading is too long "
                f"({cjk_char_count(text)} > {MAX_CHINESE_SECTION_CHARS} Chinese chars): '{text}'"
            )
            errors += 1

    if not has_conclusion:
        print("  ERROR: Missing required final heading '结论'.")
        errors += 1
    if core_finding_sections > MAX_CORE_FINDING_SECTIONS:
        print(
            f"  ERROR: Too many core finding sections "
            f"({core_finding_sections} > {MAX_CORE_FINDING_SECTIONS})."
        )
        errors += 1

    if errors:
        print(f"ERROR: Found {errors} structure issue(s).")
        return 1

    print("OK: Structure and headings match the concise workflow.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/check_structure.py <path_to_output_md>")
        sys.exit(1)

    exit_code = 0
    for md_path in sys.argv[1:]:
        exit_code |= check_structure(md_path)
    sys.exit(exit_code)
