import re

# Regex For Text Files
MONTH_YEAR_PATTERN = re.compile(r"[A-Za-z]+-\d{4}")
MPC_YEAR_MONTH_PATTERN = re.compile(r"mpc-[A-Za-z]+-\d{4}")
MPS_PATTERN = re.compile(r"monetary-policy-summary-and-minutes-[A-Za-z]+-\d{4}")
MINUTES_PATTERN = re.compile(r"minutes-[A-Za-z]+-\d{4}")

# Regex Patterns - Dates Extraction
MPS_MEETING_DATE_PATTERNS = [
    re.compile(r"meeting ending on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})"),
    re.compile(
        r"COMMITTEE MEETING\s+\d{1,2}(?:\s+[A-Za-z]+)?\s+and\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})"
    ),
]

# Regex Patterns - Published Date
MPS_PUBLISHED_DATE_PATTERNS = [
    re.compile(r"Publication date:\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})"),
    re.compile(
        r"meeting ending on\s+\d{1,2}\s+[A-Za-z]+\s+\d{4}\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})"
    ),
]

# MPC - Published Date
MPC_PUBLISHED_DATE_PATTERNS = [
    re.compile(r"(\d{1,2}\s+[A-Za-z]+\s+\d{4})"),
]

# Minutes Published Date
MINUTES_PUBLISHED_DATE_PATTERNS = [
    re.compile(r"Publication date:\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})")
]

MINUTES_MEETING_DATE_PATTERNS = [
    re.compile(
        r"committee\s+meeting\s+(?:\d{1,2}(?:\s+[A-Za-z]+)?\s+and\s+)?(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        re.IGNORECASE,
    ),
    re.compile(r"meeting ending on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})", re.IGNORECASE),
    re.compile(r"meeting ending\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})", re.IGNORECASE),
]

# Regex Patterns - Headers
MPS_FOOTER_PATTERNS = [
    re.compile(
        r"Bank of England\s+Minutes of the Monetary Policy Committee Meeting ending on\s+"
        r"(?:\d{1,2}(?:\s+[A-Za-z]+)?\s+and\s+)?\d{1,2}\s+[A-Z]+\s+\d{4}"
        r"\s+\d{1,2}",
        re.IGNORECASE,
    ),
]
