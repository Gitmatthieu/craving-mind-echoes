
"""
RAM-based vector store for quick similarity search.
No persistence yet – entire index lives in memory.
"""
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_EMBEDDING_DIM = 384
_model = SentenceTransformer("all-MiniLM-L6-v2")  # 80 MB, CPU OK
_index = faiss.IndexFlatL2(_EMBEDDING_DIM)
_texts: list[str] = []            # keeps parallel list of raw texts

def add(text: str) -> None:
    """Embed and add `text` to the FAISS index."""
    vec = _model.encode([text]).astype("float32")
    _index.add(vec)
    _texts.append(text)

def most_similar(query: str, k: int = 3) -> list[str]:
    """Return up to k stored texts most similar to `query`."""
    if len(_texts) == 0:
        return []
    vec = _model.encode([query]).astype("float32")
    _, idx = _index.search(vec, min(k, len(_texts)))
    return [_texts[i] for i in idx[0] if i < len(_texts)]
