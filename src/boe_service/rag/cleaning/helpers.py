import re
from pathlib import Path

from boe_service.config import EXTRACTED_FOLDER_PATH
from boe_service.rag.cleaning.patterns import (
    MINUTES_PATTERN,
    MONTH_YEAR_PATTERN,
    MPC_YEAR_MONTH_PATTERN,
    MPS_HEADER_PATTERNS,
    MPS_PATTERN,
    MPS_START_PATTERNS,
    MPS_SUMMARY_PATTERNS,
)


# Scan Through Text Files. Print A Counter Of Each Type By Identifying Naming Convention Through Regex.
def doc_type_counter():
    counter = {}
    for i in EXTRACTED_FOLDER_PATH.iterdir():
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
    pattern = re.compile(rf"(?<![\d.,£$])\b{n}[.:]\s+(?=[A-Z])")
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
        "index": index,
    }
