from pathlib import Path

from sentence_transformers import SentenceTransformer

from boe_service.qdrant_db import connect_to_local, filter_by_filename_and_index, search
from boe_service.utils.json_utils import load_json

QA_JSON_PATH = Path(__file__).resolve().parent / "q_and_a.json"


# Calculate Cap-Recall
def capped_recall(search_results, correct_filename, correct_index, chunks_in_section):
    correct_count = 0
    for result in search_results:
        if (
            result.payload["filename"] == correct_filename
            and result.payload["index"] == correct_index
        ):
            correct_count += 1
    possible = min(len(search_results), chunks_in_section)
    return correct_count / possible if possible else 0


# Calculate Hit Rate
def calculate_hit_rate(p_scores):
    total = sum(score > 0 for score in p_scores)
    return total / len(p_scores) if len(p_scores) else 0.0


# Main
def main():
    client = connect_to_local()
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    data = load_json(QA_JSON_PATH)
    p_scores = []
    for i in data:
        search_results = search(client, model, i["question"])
        chunks_in_section = filter_by_filename_and_index(
            client, i["filename"], i["index"]
        )
        p_scores.append(
            capped_recall(
                search_results, i["filename"], i["index"], len(chunks_in_section)
            )
        )
    p_avg = sum(p_scores) / len(p_scores)
    print(f"Capp Recall Scores Average: {p_avg:.3f}")
    hit_rate = calculate_hit_rate(p_scores)
    print(f"Hit Rate: {hit_rate:.3f}")


if __name__ == "__main__":
    main()
