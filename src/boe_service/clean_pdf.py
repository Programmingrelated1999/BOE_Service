import re
from datetime import datetime, timedelta
from pathlib import Path

# Define paths
ROOT_PATH = Path(__file__).parent.parent.parent
EXTRACT_PATH = ROOT_PATH / "data/extracted"
CLEANED_PATH = ROOT_PATH / "data/cleaned"

# Regex Patterns
MEETING_DATE_PATTERNS = [
    re.compile(r"meeting ending on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})"),
    re.compile(r"COMMITTEE MEETING\s+\d{1,2} and (\d{1,2}\s+[A-Za-z]+\s+\d{4})"),
]
PUBLISHED_DATE_PATTERNS = [
    re.compile(r"Publication date:\s+(\d{1,2} [A-Za-z]+ \d{4})"),
    re.compile(
        r"meeting ending on\s+\d{1,2}\s+[A-Za-z]+\s+\d{4}\s+(\d{1,2} [A-Za-z]+ \d{4})"
    ),
    re.compile(r"Publication date:\s+\d{1,2} [A-Za-z]+ \d{4}"),
]
YEAR_PATTERN = re.compile(r"[A-Za-z]+-\d{4}")


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
    count = 0
    for i in EXTRACT_PATH.iterdir():
        txt = Path.read_text(i)
        pages = txt.lstrip().split("\f")
        if extract_date(pages[0]) is not None:
            [meeting_date, published_date] = extract_date(pages[0])
            count += 1
    print(count)


# Main Function
def main():
    clean_data_in_text_files()


if __name__ == "__main__":
    main()
