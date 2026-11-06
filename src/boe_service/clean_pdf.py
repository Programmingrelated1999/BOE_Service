import re
from datetime import datetime
from pathlib import Path

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
CLEANED_PATH = ROOT_PATH / "data/cleaned"

MEETING_DATE_PATTERN = re.compile(r"meeting ending on\s+(\d{1,2} [A-Za-z]+ \d{4})")
PUBLISHED_DATE_PATTERNS = [
    re.compile(r"Publication date:\s+(\d{1,2} [A-Za-z]+ \d{4})"),
    re.compile(
        r"meeting ending on\s+\d{1,2} [A-Za-z]+ \d{4}\s+(\d{1,2} [A-Za-z]+ \d{4})"
    ),
]


# Extract Date Using Regex
def extract_date(text: str) -> list[datetime] | None:
    meeting_date = MEETING_DATE_PATTERN.search(text)
    for pattern in PUBLISHED_DATE_PATTERNS:
        published_date = pattern.search(text)
        if published_date:
            break
    if meeting_date and published_date:
        meeting_date = datetime.strptime(meeting_date.group(1), "%d %B %Y").date()
        published_date = datetime.strptime(published_date.group(1), "%d %B %Y").date()
        return [meeting_date.isoformat(), published_date.isoformat()]
    return None


# Extract Text From All Reports And Save Them In Extracted Folder As Txt Files
def clean_data_in_text_files():
    CLEANED_PATH.mkdir(parents=True, exist_ok=True)
    count = 0
    names = []
    for i in EXTRACT_PATH.iterdir():
        txt = Path.read_text(i)
        pages = txt.lstrip().split("\f")
        if extract_date(pages[0]) is not None:
            count += 1
            names.append(i.name)


# Main Function
def main():
    clean_data_in_text_files()


if __name__ == "__main__":
    main()
