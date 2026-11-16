import os
from typing import Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)
from sentence_transformers import SentenceTransformer

load_dotenv()


# Connect To Local Qdrant
def connect_to_local():
    try:
        db_path = os.getenv("QDRANT_CLIENT")
        if not db_path:
            raise ValueError("QDRANT_CLIENT environment variable is missing")
        client = QdrantClient(path=db_path)
        return client
    except Exception as e:
        print(f"Cannot connect to Qdrant DB: {e}")
        return None


# Search For Vector And Points
def search(client: QdrantClient, model: SentenceTransformer, query: str):
    query_vector = model.encode(query).tolist()
    results = client.query_points(
        collection_name="documents", query=query_vector, limit=5
    )
    return results.points


def filter_by_filename_and_index(client: QdrantClient, filename: str, index: int):
    points, _ = client.scroll(
        collection_name="documents",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="filename",
                    match=MatchValue(value=filename),
                ),
                FieldCondition(
                    key="index",
                    match=MatchValue(value=index),
                ),
            ]
        ),
        limit=100,
    )
    return [p.payload for p in points]


# Create Collection If Not Exists
def create_collection(client: QdrantClient, collection_name: str, v_size: int):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=v_size, distance=Distance.COSINE),
        )


# Upload Data In Batches To Qdrant
def upload_in_batches(
    client: QdrantClient,
    records: list[dict[str, Any]],
    collection_name: str = "documents",
    batch_size: int = 256,
):
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
        client.upsert(
            collection_name=collection_name,
            points=points,
        )


def main():
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    client = connect_to_local()
    search(client, model, "What was the interest rate in May of 2023?")


if __name__ == "__main__":
    main()
