import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/quran_hadith_faiss.index")
chunks = pickle.load(open("data/chunks_metadata.pkl", "rb"))

def embed_query(text: str):
    vec = embedder.encode([text])[0].astype("float32")
    return np.expand_dims(vec, axis=0)

def retrieve_chunks(query, k=5):
    D, I = index.search(embed_query(query), k)
    return [chunks[i] for i in I[0]]
 
