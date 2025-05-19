import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import gdown

# File IDs from Google Drive shareable links
INDEX_FILE_ID = "16aHgnJCQOXU0R6pin_yYcS8DFlimw11F"
CHUNKS_FILE_ID = "1c2TsLzj10NEYcgHME7fMtDs3aTie46Df"

# Local filenames
INDEX_FILE = "quran_hadith_faiss.index"
CHUNKS_FILE = "chunks_metadata.pkl"

# Download if not already present
if not os.path.exists(INDEX_FILE):
    gdown.download(f"https://drive.google.com/uc?id={INDEX_FILE_ID}", INDEX_FILE, quiet=False)

if not os.path.exists(CHUNKS_FILE):
    gdown.download(f"https://drive.google.com/uc?id={CHUNKS_FILE_ID}", CHUNKS_FILE, quiet=False)

# Load model and data
embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_FILE)

with open(CHUNKS_FILE, "rb") as f:
    chunks = pickle.load(f)

# Embed query
def embed_query(text: str):
    vec = embedder.encode([text])[0].astype("float32")
    return np.expand_dims(vec, axis=0)

# Retrieve top-k similar chunks
def retrieve_chunks(query, k=5):
    D, I = index.search(embed_query(query), k)
    return [chunks[i] for i in I[0]]
