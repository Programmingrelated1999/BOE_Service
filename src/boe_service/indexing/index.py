import math
from pathlib import Path

from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from boe_service.indexing.qdrant_db import connect_to_local
from boe_service.utils.json_utils import load_json, save_to_json

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
    # Load Data
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    if not chunck_path.exists():
        data = load_json(json_path)
        chunck_data = []
        # Chuck Data
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

    # Create To A Local QDrant Database
    client = connect_to_local()
    if not client:
        return

    # Store In Database
    if not client.collection_exists("documents"):
        client.create_collection(
            collection_name="documents",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    # Upload In Batches
    records = load_json(chunck_path)
    batch_size = 256
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        points = [
            PointStruct(
                id=i + j,
                vector=r["vector"],
                payload={k: v for k, v in r.items() if k != "vector"},
            )
            for j, r in enumerate(batch)
        ]
        client.upsert(collection_name="documents", points=points)


if __name__ == "__main__":
    main()
