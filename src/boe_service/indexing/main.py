from pathlib import Path

from sentence_transformers import SentenceTransformer

from boe_service.indexing.helpers import chunk_paragraphs, encode_chunked_text
from boe_service.qdrant_db import connect_to_local, create_collection, upload_in_batches
from boe_service.utils.json_utils import load_json, save_to_json

json_path = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "data"
    / "cleaned"
    / "data.json"
)

chunck_path = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "data"
    / "cleaned"
    / "chunck.json"
)


# Main Function
def main():
    # Load Data
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    if not chunck_path.exists():
        data = load_json(json_path)
        chunck_data = []
        for i in data:
            chunks = chunk_paragraphs(i["text"], 300)
            new_data = encode_chunked_text(chunks, i, model, True)
            chunck_data.extend(new_data)
        save_to_json(chunck_data, chunck_path)

    # Create Client Instance And Create Documents Collections If Not-Exists
    client = connect_to_local()
    if not client:
        return
    create_collection(client, "documents", 384)

    # Upload In Batches
    records = load_json(chunck_path)
    upload_in_batches(client, records, "documents", 256)


if __name__ == "__main__":
    main()
