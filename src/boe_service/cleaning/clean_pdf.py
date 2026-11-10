import re
from datetime import datetime, timedelta
from pathlib import Path

from boe_service.cleaning.patterns import (
    MINUTES_PATTERN,
    MONTH_YEAR_PATTERN,
    MPC_YEAR_MONTH_PATTERN,
    MPS_FOOTER_PATTERNS,
    MPS_MEETING_DATE_PATTERNS,
    MPS_PATTERN,
    MPS_PUBLISHED_DATE_PATTERNS,
)

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
CLEANED_PATH = ROOT_PATH / "data/cleaned"


# Scan Through Text Files. Print A Counter Of Each Type By Identifying Naming Convention Through Regex.
def doc_type_counter():
    counter = {}
    for i in EXTRACT_PATH.iterdir():
        doc_type = check_doc_type(i.stem)
        counter[doc_type] = counter.get(doc_type, 0) + 1
    print(counter)


# Stem of Text
def check_doc_type(stem: str) -> str:
    if re.fullmatch(MONTH_YEAR_PATTERN, stem):
        return "month-year"
    if re.fullmatch(MPC_YEAR_MONTH_PATTERN, stem):
        return "mpc-month-year"
    if re.fullmatch(MPS_PATTERN, stem):
        return "mps"
    if re.fullmatch(MINUTES_PATTERN, stem):
        return "minutes"
    return "other"


# Search Meeting Date With Regex
def search_meeting_date(text: str, doc_type: str) -> datetime | None:
    if doc_type in ["month-year", "mps"]:
        for pattern in MPS_MEETING_DATE_PATTERNS:
            meeting_date = pattern.search(text)
            if meeting_date:
                return meeting_date
    return None


# Search Published Date With Regex
def search_published_date(text: str, doc_type: str) -> datetime | None:
    if doc_type in ["month-year", "mps"]:
        for pattern in MPS_PUBLISHED_DATE_PATTERNS:
            meeting_date = pattern.search(text)
            if meeting_date:
                return meeting_date
    return None


# Remove Footer In Pages
def remove_boe_footer(text: str) -> str:
    replaced = False
    for pattern in MPS_FOOTER_PATTERNS:
        text, n = pattern.subn("", text)
        if n:
            replaced = True
    return text, replaced


# Read Text From Address And Return List Of Seperated Text By Page
def read_text_split_pages(addr: str) -> list[str]:
    txt = Path.read_text(addr)
    return txt.lstrip().split("\f")


# Split One Large Text Into Paragraphs Numbered
def split_into_paragraphs():
    return


# Extract Date Using Regex
def extract_date(text: str, doc_type: str) -> dict[str, str] | None:
    meeting_date = search_meeting_date(text, doc_type)
    published_date = search_published_date(text, doc_type)
    if meeting_date:
        meeting_date = datetime.strptime(meeting_date.group(1), "%d %B %Y").date()
        published_date = (
            datetime.strptime(published_date.group(1), "%d %B %Y").date()
            if published_date
            else meeting_date + timedelta(1)
        )  # Publish Date Pattern Search Missing - Set To One Day After Meeting Date
        return {
            "meeting_date": meeting_date.isoformat(),
            "published_date": published_date.isoformat(),
        }
    return None


# Extract Text From All Reports And Save Them In Extracted Folder As Txt Files
def clean_data_in_text_files():
    CLEANED_PATH.mkdir(parents=True, exist_ok=True)
    count = 0
    meta_data = {}
    for i in EXTRACT_PATH.iterdir():
        doc_type = check_doc_type(i.stem)
        pages = read_text_split_pages(i)
        dates = extract_date(pages[0], doc_type)
        if dates:
            meta_data["published_date"] = dates["published_date"]
            print(meta_data)
    print("Count: ", count)


# Main Function
def main():
    clean_data_in_text_files()
    doc_type_counter()


if __name__ == "__main__":
    main()
