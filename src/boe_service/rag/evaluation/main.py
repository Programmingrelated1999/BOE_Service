from typing import Any

import pandas as pd
import typer
from sentence_transformers import SentenceTransformer

from boe_service.config import EVAL_TEST_SET_PATH, RESULTS_PATH
from boe_service.qdrant_db import connect_to_local, filter_by_filename_and_index, search
from boe_service.utils.json_utils import load_json, save_to_json


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


def save_run(
    name: str,
    config: dict[str, Any],
    metrics: dict[str, Any],
    results_df: pd.DataFrame,
):
    details_path = RESULTS_PATH / f"{name}-details.csv"
    summary_path = RESULTS_PATH / f"{name}-summary.json"
    # Save Summary Data - Experiment Name, Config, Metrics
    summary_data = {"name": name, "config": config, "metrics": metrics}
    results_df.to_csv(details_path, index=False)
    save_to_json(summary_data, summary_path)


def get_curr_results_pd(question: str, search_results, c_fname, c_index):
    data = []
    for r in search_results:
        data.append(
            [
                question,
                r.payload["text"],
                r.score,
                r.payload["filename"],
                r.payload["index"],
                c_fname,
                c_index,
            ]
        )
    data = pd.DataFrame(
        data,
        columns=[
            "Question",
            "Answer",
            "Score",
            "Filename",
            "Index",
            "Correct_Filename",
            "Correct_Index",
        ],
    )
    return data


# Main
def main(collection_name: str, encoder_model: str):
    if encoder_model == "small":
        model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    else:
        model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    client = connect_to_local()
    data = load_json(EVAL_TEST_SET_PATH)
    results_df = pd.DataFrame(
        columns=[
            "Question",
            "Answer",
            "Score",
            "Filename",
            "Index",
            "Correct_Filename",
            "Correct_Index",
        ]
    )
    p_scores = []
    for i in data:
        search_results = search(client, collection_name, model, i["question"], 5, True)
        results_df = pd.concat(
            [
                results_df,
                get_curr_results_pd(
                    i["question"], search_results, i["filename"], i["index"]
                ),
            ],
            ignore_index=True,
        )
        chunks_in_section = filter_by_filename_and_index(
            client, collection_name, i["filename"], i["index"]
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

    save_run(
        name=collection_name,
        config={
            "collection_name": collection_name,
            "model": encoder_model,
            "chunk_words": 300,
            "overlap": 0.1,
            "k": 5,
        },
        metrics={"cap_recall": p_avg, "hit_rate": hit_rate},
        results_df=results_df,
    )

    q = data[0]["question"]
    for flag in (False, True):
        res = search(client, collection_name, model, q, limit=5, use_q_prefix=flag)
        print(flag, [round(r.score, 4) for r in res])


if __name__ == "__main__":
    typer.run(main)
