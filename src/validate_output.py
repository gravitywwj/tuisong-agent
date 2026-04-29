import sys
from pathlib import Path

from check_images import check_images
from check_phrases import check_phrases
from check_structure import check_structure


def validate_paper(paper_id):
    input_dir = Path("data/input") / paper_id
    images_dir = input_dir / "images"
    output_file = Path("data/output") / f"{paper_id}_summary.md"

    print(f"Validating paper: {paper_id}")
    image_status = check_images(images_dir, output_file)
    phrase_status = check_phrases(output_file)
    structure_status = check_structure(output_file)

    return 1 if image_status or phrase_status or structure_status else 0


def find_output_papers():
    output_dir = Path("data/output")
    if not output_dir.exists():
        return []
    return sorted(
        path.name[: -len("_summary.md")]
        for path in output_dir.glob("*_summary.md")
    )


if __name__ == "__main__":
    paper_ids = sys.argv[1:] or find_output_papers()
    if not paper_ids:
        print("Usage: python src/validate_output.py <paper_id> [paper_id ...]")
        print("No output files found under data/output/.")
        sys.exit(1)

    exit_code = 0
    for paper_id in paper_ids:
        exit_code |= validate_paper(paper_id)

    sys.exit(exit_code)
