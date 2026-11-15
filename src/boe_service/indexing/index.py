import json
import math
from pathlib import Path

from sentence_transformers import SentenceTransformer

from boe_service.cleaning.helpers import save_to_json

json_path = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "data"
    / "cleaned"
    / "test.json"
)

chunck_path = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "data"
    / "cleaned"
    / "chunck.json"
)


# Load Json
def load_json():
    with open(json_path) as file:
        data = json.load(file)
        return data


# Chunking Into Paragraphs
def chunk_paragraphs(text: str, max_words: int = 300) -> list[str]:
    words = text.split()
    overlap = min(math.ceil(0.1 * max_words), max_words - 1)
    chunks, i = [], 0
    while i < len(words):
        subtext = words[i : i + max_words]
        chunks.append(" ".join(subtext))
        if i + max_words >= len(words):
            break
        i += max_words - overlap
    return chunks


# Main Function
def main():
    # Create a local Qdrant database
    # client = connect_to_local()
    # if not client:
    #     return

    # load data
    data = load_json()
    chunck_data = []
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    for i in data:
        chunks = chunk_paragraphs(i["text"], 300)
        for c in chunks:
            vector = model.encode(
                c,
                normalize_embeddings=True,
            ).tolist()
            new_data = {**i, "text": c, "vector": vector}
            chunck_data.append(new_data)

    save_to_json(chunck_data, chunck_path)


if __name__ == "__main__":
    main()
