import pymupdf

from boe_service.config import EXTRACTED_FOLDER_PATH, REPORTS_FOLDER_PATH


# Extract Text From All Reports And Save Them In Extracted Folder As Txt Files
def extract_txt_from_reports():
    EXTRACTED_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    # For Each File - Transform Into Text Format
    for i in REPORTS_FOLDER_PATH.iterdir():
        if i.suffix.lower() == ".pdf":
            with pymupdf.open(i) as doc:
                txt = chr(12).join([page.get_text() for page in doc])
            output_path = EXTRACTED_FOLDER_PATH / f"{i.stem}.txt"
            output_path.write_bytes(txt.encode())


# Main
def main():
    extract_txt_from_reports()


if __name__ == "__main__":
    main()
