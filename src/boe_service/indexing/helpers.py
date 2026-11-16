import math
from typing import Any

from sentence_transformers import SentenceTransformer


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


# Create Vectors For The Chunked Paragraphs Of A Payload, And Multiple Dict Of Payload With Different Chunked Paragraphs
def encode_chunked_text(
    chunked_paras: list[str], payload: dict[str, Any], model: SentenceTransformer
) -> list[dict[str, Any]]:
    r_data = []
    for c in chunked_paras:
        vector = model.encode(
            c,
            normalize_embeddings=True,
        ).tolist()
        new_data = {**payload, "text": c, "vector": vector}
        r_data.append(new_data)
    return r_data
