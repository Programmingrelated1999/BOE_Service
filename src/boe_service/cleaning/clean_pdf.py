import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from boe_service.cleaning.helpers import check_doc_type, doc_type_counter
from boe_service.cleaning.patterns import (
    MINUTES_MEETING_DATE_PATTERNS,
    MINUTES_PUBLISHED_DATE_PATTERNS,
    MPC_PUBLISHED_DATE_PATTERNS,
    MPS_FOOTER_PATTERNS,
    MPS_MEETING_DATE_PATTERNS,
    MPS_PUBLISHED_DATE_PATTERNS,
)

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
CLEANED_PATH = ROOT_PATH / "data/cleaned"


# Read Text From Address And Return List Of Seperated Text By Pages
def split_pages(addr: str) -> list[str]:
    txt = Path.read_text(addr)
    return txt.lstrip().split("\f")


# Search And Return Any Matching Dates From Given Patterns
def search_date(text: str, patterns: list[re.Pattern[str]]) -> str | None:
    for pattern in patterns:
        date = pattern.search(text)
        if date:
            return date
    return None


# Determine Regex Pattern For Meeting Date And Call Search Date
def search_meeting_date(text: str, doc_type: str) -> str | None:
    if doc_type in ["month-year", "mps"]:
        return search_date(text, MPS_MEETING_DATE_PATTERNS)
    if doc_type == "minutes":
        return search_date(text, MINUTES_MEETING_DATE_PATTERNS)
    return None


# Determine Regex Pattern For Published Date And Call Search Date
def search_published_date(text: str, doc_type: str) -> str | None:
    if doc_type in ["month-year", "mps"]:
        return search_date(text, MPS_PUBLISHED_DATE_PATTERNS)
    if doc_type == "mpc-month-year":
        return search_date(text, MPC_PUBLISHED_DATE_PATTERNS)
    if doc_type == "minutes":
        return search_date(text, MINUTES_PUBLISHED_DATE_PATTERNS)
    return None


# Extract Date Using Regex
def extract_date(text: str, doc_type: str) -> dict[str, str]:
    meeting_date = search_meeting_date(text, doc_type)
    published_date = search_published_date(text, doc_type)

    if published_date:
        published_date = datetime.strptime(published_date.group(1), "%d %B %Y").date()
    if meeting_date:
        meeting_date = datetime.strptime(meeting_date.group(1), "%d %B %Y").date()
        if doc_type in ["month-year", "mps"] and not published_date:
            published_date = meeting_date + timedelta(1)

    if meeting_date:
        meeting_date = meeting_date.isoformat()
        # print(meeting_date) if doc_type == "minutes" else None
    if published_date:
        published_date = published_date.isoformat()

    if doc_type == "minutes":
        print(meeting_date)

    return {
        "meeting_date": meeting_date,
        "published_date": published_date,
    }


# Remove Footer In Pages
def remove_footer(text: str) -> str:
    replaced = False
    for pattern in MPS_FOOTER_PATTERNS:
        text, n = pattern.subn("", text)
        if n:
            replaced = True
    return text, replaced


# Split One Large Text Into Paragraphs Numbered
def split_into_paragraphs():
    return


# Filter Noise
def preprocess_text(pages: list[str]) -> str:
    pass


# Extract Text From All Reports And Save Them In Extracted Folder As Txt Files
def clean_data_in_text_files():
    CLEANED_PATH.mkdir(parents=True, exist_ok=True)
    data = []
    for i in EXTRACT_PATH.iterdir():
        pages = split_pages(i)
        if check_doc_type(i.stem) == "other":
            continue
        dates = extract_date(pages[0], doc_type=check_doc_type(i.stem))
        if dates:
            data.append(
                {
                    "name": i.name,
                    "meeting_date": dates["meeting_date"],
                    "published_date": dates["published_date"],
                }
            )
    print([i["published_date"] for i in data])
    data.sort(key=lambda d: d["published_date"])
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Main Function
def main():
    clean_data_in_text_files()
    doc_type_counter()


if __name__ == "__main__":
    main()
