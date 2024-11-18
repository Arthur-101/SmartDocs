import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import config

SAMBANOVA_API_URL = config.SAMBANOVA_API_URL
SAMBANOVA_API_KEY = config.SAMBANOVA_API_KEY

client = OpenAI(base_url=SAMBANOVA_API_URL, api_key=SAMBANOVA_API_KEY)

# Function to query FAISS index and generate response using SAMBANOVA API
def query_faiss_snova(question, top_k=5, llm_model=config.MODEL,
                chunk_folder=config.TEXT_CHUNKS_FOLDER, index_path=config.FAISS_INDEX_PATH):
    # Read the FAISS index from the file
    index = faiss.read_index(index_path)

    # Load text chunks from the chunk folder
    chunks = []
    file_names = sorted([f for f in os.listdir(chunk_folder) if f.startswith("chunk_")])

    for file_name in file_names:
        file_path = os.path.join(chunk_folder, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            chunks.append(file.read())  # Append each chunk's content

    # Initialize SentenceTransformer model to generate query embeddings
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Generate embedding for the question
    query_embedding = model.encode([question])

    # Search the FAISS index to find the top_k most relevant chunks
    distances, indices = index.search(np.array(query_embedding), top_k)

    # Retrieve the text chunks corresponding to the top_k indices
    results = [chunks[i] for i in indices[0]]
    context = " ".join(results)  # Combine the results into a single context

    # Prepare the system and user prompt for the chat completion API
    sys_prompt = config.SYSTEM_PROMPT
    user_message = f"Context: {context}\n\nQuestion: {question}\nAnswer:"

    # Query the SAMBANOVA model using the OpenAI API
    completion = client.chat.completions.create(
        model = llm_model,
        messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_message}],
        stream = True,
    )

    # Collect the response from the streamed API output
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""  # Append each chunk of the response

    return response  # Return the final response
