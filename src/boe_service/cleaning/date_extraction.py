from datetime import datetime, timedelta

from boe_service.cleaning.patterns import (
    MINUTES_MEETING_DATE_PATTERNS,
    MINUTES_PUBLISHED_DATE_PATTERNS,
    MPC_PUBLISHED_DATE_PATTERNS,
    MPS_MEETING_DATE_PATTERNS,
    MPS_PUBLISHED_DATE_PATTERNS,
)


# Determine Regex Pattern For Meeting Date And Call Search Date
def search_meeting_date(text: str, doc_type: str) -> str | None:
    if doc_type in ["month-year", "mps"]:
        return search_date(text, MPS_MEETING_DATE_PATTERNS)
    if doc_type == "minutes":
        return search_date(text, MINUTES_MEETING_DATE_PATTERNS)
    return None


# Search And Return Any Matching Dates From Given Patterns
def search_date(text: str, patterns: list[re.Pattern[str]]) -> str | None:
    for pattern in patterns:
        date = pattern.search(text)
        if date:
            return date
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
        published_date = (
            datetime.strptime(published_date.group(1), "%d %B %Y").date().isoformat()
        )
    if meeting_date:
        meeting_date = datetime.strptime(meeting_date.group(1), "%d %B %Y").date()
        if doc_type in ["month-year", "mps"] and not published_date:
            published_date = (meeting_date + timedelta(1)).isoformat()
        meeting_date = meeting_date.isoformat()

    return {
        "meeting_date": meeting_date,
        "published_date": published_date,
    }
