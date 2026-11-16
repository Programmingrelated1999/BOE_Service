from pathlib import Path

from sentence_transformers import SentenceTransformer

from boe_service.indexing.qdrant_db import connect_to_local, search
from boe_service.utils.json_utils import load_json

json_path = Path(__file__).resolve().parent.parent.parent.parent / "q_and_a.json"


def main():
    data = load_json(json_path)
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    client = connect_to_local()
    count = 0
    for i in data:
        question = i["question"]
        result = search(client, model, question)
        for r in result:
            if r.payload["filename"] == i["filename"] and (
                r.payload["index"] == i["index"]
                or (i["index"] == 0 and r.payload["index"] is None)
            ):
                count += 1
                break
    print(count)


if __name__ == "__main__":
    main()
