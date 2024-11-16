import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import config  # Import the config file

SAMBANOVA_API_URL = config.SAMBANOVA_API_URL
SAMBANOVA_API_KEY = config.SAMBANOVA_API_KEY

client = OpenAI(base_url=SAMBANOVA_API_URL, api_key=SAMBANOVA_API_KEY)

def query_faiss_snova(question, top_k=5, chunk_folder=config.TEXT_CHUNKS_FOLDER, index_path=config.FAISS_INDEX_PATH):
    index = faiss.read_index(index_path)

    chunks = []
    file_names = sorted([f for f in os.listdir(chunk_folder) if f.startswith("chunk_")])

    for file_name in file_names:
        file_path = os.path.join(chunk_folder, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            chunks.append(file.read())

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    query_embedding = model.encode([question])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = [chunks[i] for i in indices[0]]
    context = " ".join(results)

    sys_prompt = """You are a the personification of the provided document.
    Your task is to provide the best responses you can to the user's questions.
    You can also ask the user for clarifications if you think it's necessary.
    When asked, respond that 'I am the document' or something like that."""

    user_message = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    completion = client.chat.completions.create(
        model="Meta-Llama-3.1-405B-Instruct",
        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_message}],
        stream=True,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response
