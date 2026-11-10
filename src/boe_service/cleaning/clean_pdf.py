import re
from datetime import datetime, timedelta
from pathlib import Path

from boe_service.cleaning.patterns import (
    BOE_FOOTER_PATTERNS,
    MEETING_DATE_PATTERNS,
    MINUTES_PATTERN,
    MONTH_YEAR_PATTERN,
    MPC_YEAR_MONTH_PATTERN,
    MPS_PATTERN,
    PUBLISHED_DATE_PATTERNS,
)

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
CLEANED_PATH = ROOT_PATH / "data/cleaned"


def doc_analysis():
    doc_type_counter = {}
    for i in EXTRACT_PATH.iterdir():
        if re.fullmatch(MONTH_YEAR_PATTERN, i.stem):
            doc_type_counter["month-year"] = doc_type_counter.get("month-year", 0) + 1
        elif re.fullmatch(MPC_YEAR_MONTH_PATTERN, i.stem):
            doc_type_counter["mpc-month-year"] = (
                doc_type_counter.get("mpc-month-year", 0) + 1
            )
        elif re.fullmatch(MPS_PATTERN, i.stem):
            doc_type_counter["mps"] = doc_type_counter.get("mps", 0) + 1
        elif re.fullmatch(MINUTES_PATTERN, i.stem):
            doc_type_counter["minutes"] = doc_type_counter.get("minutes", 0) + 1
        else:
            doc_type_counter["others"] = doc_type_counter.get("others", 0) + 1
    print(doc_type_counter)


# Search Meeting Date With Regex
def search_meeting_date(text: str):
    for pattern in MEETING_DATE_PATTERNS:
        meeting_date = pattern.search(text)
        if meeting_date:
            return meeting_date


# Search Published Date With Regex
def search_published_date(text: str):
    for pattern in PUBLISHED_DATE_PATTERNS:
        meeting_date = pattern.search(text)
        if meeting_date:
            return meeting_date


def remove_boe_footer(text: str) -> str:
    replaced = False
    for pattern in BOE_FOOTER_PATTERNS:
        text, n = pattern.subn("", text)
        if n > 1:
            print("Greater Than One")
        if n:
            replaced = True
    return text, replaced


# Read Text From Address And Return List Of Seperated Text By Page
def read_txt(addr: str) -> list[str]:
    txt = Path.read_text(addr)
    return txt.lstrip().split("\f")


# Split One Large Text Into Paragraphs Numbered
def split_into_paragraphs():
    return


# Extract Date Using Regex
def extract_date(text: str) -> list[datetime] | None:
    meeting_date = search_meeting_date(text)
    published_date = search_published_date(text)
    if meeting_date:
        meeting_date = datetime.strptime(meeting_date.group(1), "%d %B %Y").date()
        published_date = (
            datetime.strptime(published_date.group(1), "%d %B %Y").date()
            if published_date
            else meeting_date + timedelta(1)
        )  # Publish Date Pattern Search Missing - Set To One Day After Meeting Date
        return [meeting_date.isoformat(), published_date.isoformat()]
    return None


# Extract Text From All Reports And Save Them In Extracted Folder As Txt Files
def clean_data_in_text_files():
    CLEANED_PATH.mkdir(parents=True, exist_ok=True)
    meta_data = {}
    count = 0
    count_list = []
    publish_list = []

    for i in EXTRACT_PATH.iterdir():
        pages = read_txt(i)
        if extract_date(pages[0]) is not None:
            [meeting_date, published_date] = extract_date(pages[0])
            meta_data["published_date"] = published_date
            publish_list.append(i.name)
        for j in pages:
            footer, replaced = remove_boe_footer(j)
            if replaced:
                count += 1
        count_list.append({"name": i.name, "count": count})
        count = 0
    empty_list_str = "\n".join([i["name"] for i in count_list if i["count"] == 0])
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(empty_list_str)
    with open("p_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(publish_list))


# Main Function
def main():
    # clean_data_in_text_files()
    doc_analysis()


if __name__ == "__main__":
    main()
