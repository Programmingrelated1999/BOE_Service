from pathlib import Path

import pymupdf

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
REPORT_PATH = ROOT_PATH / "data/reports"


# Extract Text From All Reports And Save Them In Extracted Folder As Txt Files
def extract_txt_from_reports():
    EXTRACT_PATH.mkdir(parents=True, exist_ok=True)
    for i in REPORT_PATH.iterdir():
        if i.suffix.lower() == ".pdf":
            with pymupdf.open(i) as doc:
                txt = chr(12).join([page.get_text() for page in doc])
            (EXTRACT_PATH / f"{i.stem}.txt").write_bytes(txt.encode())


# Main
def main():
    extract_txt_from_reports()


if __name__ == "__main__":
    main()
