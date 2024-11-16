import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import config

def generate_embeddings_and_index(chunk_folder=config.TEXT_CHUNKS_FOLDER, index_path=config.FAISS_INDEX_PATH):
    chunks = []
    file_names = sorted([f for f in os.listdir(chunk_folder) if f.startswith("chunk_")])

    for file_name in file_names:
        file_path = os.path.join(chunk_folder, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            chunks.append(file.read())

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)

    dimension = len(embeddings[0])  # Embedding size
    index = faiss.IndexFlatL2(dimension)  # L2 distance

    embeddings_array = np.array(embeddings)
    index.add(embeddings_array)

    print(f"FAISS index created with {index.ntotal} entries!")

    faiss.write_index(index, index_path)
    print(f"FAISS index saved to {index_path}")
