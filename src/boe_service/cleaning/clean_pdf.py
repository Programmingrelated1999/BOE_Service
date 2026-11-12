import re
from pathlib import Path

from boe_service.cleaning.date_extraction import extract_date
from boe_service.cleaning.helpers import check_doc_type, save_to_json
from boe_service.cleaning.patterns import (
    MPS_HEADER_PATTERNS,
    MPS_START_PATTERNS,
    MPS_SUMMARY_PATTERNS,
)

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
CLEANED_PATH = ROOT_PATH / "data/cleaned"


# Read Text From Address And Return List Of Seperated Text By Pages
def split_pages(addr: str) -> list[str]:
    txt = Path.read_text(addr)
    return txt.lstrip().split("\f")


# Remove Footer In Pages
def remove_footer(text: str) -> str:
    replaced = False
    for pattern in MPS_HEADER_PATTERNS:
        text, n = pattern.subn("", text)
        if n:
            replaced = True
    return text, replaced


# Cut Text Start
def cut_text_start(whole_text: str) -> str | None:
    for pattern in MPS_START_PATTERNS:
        match = pattern.search(whole_text)
        if match:
            return whole_text[match.start() :]
    return None


# Get Summary Text
def get_summary(whole_text: str) -> str:
    for pattern in MPS_SUMMARY_PATTERNS:
        match = pattern.search(whole_text)
        if match:
            summary = whole_text[: match.start()]
            minutes = whole_text[match.end() :].strip()
            return summary, minutes
    return None


# Find The Label For Paragraph In MPS Text
def find_number(text: str, n: int, pos: int = 0) -> re.Match[str] | None:
    pattern = re.compile(rf"^[ \t]*{n}\.\s+", re.MULTILINE)
    return pattern.search(text, pos)


# Split One Large Text Into Paragraphs Numbered
def split_into_paragraphs(text: str) -> list[str]:
    counter = 1
    chunks = []
    current = find_number(text, counter)
    # Get Next Number Start Index, If Not Set The End Of Text
    while current:
        nxt = find_number(text, counter + 1, current.end())
        end = nxt.start() if nxt else len(text)
        chunks.append((counter, text[current.end() : end].strip()))
        counter += 1
        current = nxt
    return chunks


# Create Meta Field
def create_meta_field(filename, meeting_date, published_date, part, text, index):
    return {
        "filename": f"{filename}.pdf",
        "meeting_date": meeting_date,
        "published_date": published_date,
        "part": part or None,
        "text": text,
        "index": index or None,
    }


# Extract Text From All Reports And Save Them As JSON File
def clean_data_in_text_files():
    # Create Folder Destination
    CLEANED_PATH.mkdir(parents=True, exist_ok=True)
    all_data = []
    for i in EXTRACT_PATH.iterdir():
        # Work Only With MPS - Which Start From May 2022
        if check_doc_type(i.stem) != "mps":
            continue
        # Split Into Pages, Use First Page To Extract Dates, Join The Pages Into One Single Text
        pages = split_pages(i)
        dates = extract_date(pages[0], doc_type=check_doc_type(i.stem))
        whole_text = "".join([text for text, _ in (remove_footer(p) for p in pages)])
        whole_text = cut_text_start(whole_text)
        # Splitting Text Into Summary And Indexed Chuncks.
        summary, minutes = get_summary(whole_text)
        data = create_meta_field(
            i.stem,
            dates["meeting_date"],
            dates["published_date"],
            "summary",
            summary,
            None,
        )
        if data:
            all_data.append(data)
        chuncks = split_into_paragraphs(minutes)
        if len(chuncks) > 0:
            for c in chuncks:
                data = create_meta_field(
                    i.stem,
                    dates["meeting_date"],
                    dates["published_date"],
                    "minutes",
                    c[1],
                    c[0],
                )
                if data:
                    all_data.append(data)
    save_to_json(all_data, CLEANED_PATH / "test.json")


# Main Function
def main():
    clean_data_in_text_files()


if __name__ == "__main__":
    main()
