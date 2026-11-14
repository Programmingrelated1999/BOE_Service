import json
import re
from pathlib import Path

from boe_service.cleaning.patterns import (
    MINUTES_PATTERN,
    MONTH_YEAR_PATTERN,
    MPC_YEAR_MONTH_PATTERN,
    MPS_PATTERN,
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


# Save Cleaned Data For Pre Processing
def save_to_json(data: dict, output_file: str) -> None:
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii="False")
