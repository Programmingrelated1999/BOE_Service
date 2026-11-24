from typing import Literal

import typer
from sentence_transformers import SentenceTransformer

from boe_service.config import CLEANED_FOLDER_PATH, INDEXED_JSON_PATH
from boe_service.qdrant_db import connect_to_local, create_collection, upload_in_batches
from boe_service.rag.indexing.helpers import chunk_paragraphs, encode_chunked_text
from boe_service.utils.json_utils import load_json, save_to_json


# Main Function
def main(encoder_model: Literal["small", "large"] = "small", use_header: bool = True):
    # Load Data
    if encoder_model == "small":
        model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        vector_size = 384
    else:
        model = SentenceTransformer("BAAI/bge-base-en-v1.5")
        vector_size = 768

    if use_header:
        exp_name = f"{encoder_model}_with_headers"
    else:
        exp_name = f"{encoder_model}_baseline"
    encoded_path = CLEANED_FOLDER_PATH / f"{exp_name}-encoded.json"

    data = load_json(INDEXED_JSON_PATH)
    chunck_data = []
    for i in data:
        chunks = chunk_paragraphs(i["text"], 300)
        new_data = encode_chunked_text(chunks, i, model, use_header)
        chunck_data.extend(new_data)
    save_to_json(chunck_data, encoded_path)

    # Create Client Instance And Create Documents Collections If Not-Exists
    client = connect_to_local()
    if not client:
        return
    create_collection(client, f"{exp_name}_documents", vector_size)

    # Upload In Batches
    records = load_json(encoded_path)
    upload_in_batches(client, records, f"{exp_name}_documents", 256)


if __name__ == "__main__":
    typer.run(main)
