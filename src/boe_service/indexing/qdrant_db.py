import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

load_dotenv()


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


def search(client: QdrantClient, model: SentenceTransformer, query: str):
    query_vector = model.encode(query).tolist()
    results = client.query_points(
        collection_name="documents", query=query_vector, limit=5
    )
    for point in results.points:
        print("Score: ", point.score)
        print("Filename: ", point.payload["filename"])
        print("Published Date: ", point.payload["published_date"])


def main():
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    client = connect_to_local()
    search(client, model, "What was the interest rate in May of 2023?")


if __name__ == "__main__":
    main()
