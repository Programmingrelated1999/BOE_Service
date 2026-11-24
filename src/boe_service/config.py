from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORTS_FOLDER_PATH = PROJECT_ROOT / "data" / "reports"
EXTRACTED_FOLDER_PATH = PROJECT_ROOT / "data" / "extracted"
CLEANED_FOLDER_PATH = PROJECT_ROOT / "data" / "cleaned"

INDEXED_JSON_PATH = CLEANED_FOLDER_PATH / "indexed.json"

EVAL_FOLDER = PROJECT_ROOT / "src" / "boe_service" / "rag" / "evaluation"
EVAL_TEST_SET_PATH = EVAL_FOLDER / "q_and_a.json"
RESULTS_PATH = EVAL_FOLDER / "results"
