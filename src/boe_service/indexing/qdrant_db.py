import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

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
