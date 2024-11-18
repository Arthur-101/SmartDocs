import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import config

# Generate embeddings for text chunks and create a FAISS index
def generate_embeddings_and_index(chunk_folder=config.TEXT_CHUNKS_FOLDER, index_path=config.FAISS_INDEX_PATH):
    # Read text chunks from files in the specified folder
    chunks = []
    file_names = sorted([f for f in os.listdir(chunk_folder) if f.startswith("chunk_")])

    for file_name in file_names:
        file_path = os.path.join(chunk_folder, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            chunks.append(file.read())  # Append each chunk to the list

    # Initialize the SentenceTransformer model to generate embeddings
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)  # Generate embeddings for each chunk

    dimension = len(embeddings[0])  # Embedding size (dimensionality of the vector)
    index = faiss.IndexFlatL2(dimension)  # Create a FAISS index using L2 distance

    embeddings_array = np.array(embeddings)  # Convert embeddings to a numpy array
    index.add(embeddings_array)  # Add embeddings to the FAISS index

    # print(f"FAISS index created with {index.ntotal} entries!")  # Notify the number of indexed entries

    # Save the FAISS index to a file
    faiss.write_index(index, index_path)
    # print(f"FAISS index saved to {index_path}")
