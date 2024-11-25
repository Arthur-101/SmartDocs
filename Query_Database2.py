import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import config
import json

# Set up the API connection (Sambanova)
SAMBANOVA_API_URL = config.SAMBANOVA_API_URL
SAMBANOVA_API_KEY = config.SAMBANOVA_API_KEY
client = OpenAI(base_url=SAMBANOVA_API_URL, api_key=SAMBANOVA_API_KEY)

# A simple in-memory history to track conversation
conversation_history = []

# Function to add user input and model response to history
def add_to_history(user_input, model_response):
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": model_response})

# Function to query FAISS index and generate response using SAMBANOVA API with history
def query_faiss_snova(question, top_k=5,
                       chunk_folder=config.TEXT_CHUNKS_FOLDER,
                       index_path=config.FAISS_INDEX_PATH):
    
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
    model = SentenceTransformer(config.SENTENCE_TRANSFORMER_MODEL)

    # Generate embedding for the question
    query_embedding = model.encode([question])

    # Search the FAISS index to find the top_k most relevant chunks
    distances, indices = index.search(np.array(query_embedding), top_k)

    # Retrieve the text chunks corresponding to the top_k indices
    results = [chunks[i] for i in indices[0]]
    context = " ".join(results)  # Combine the results into a single context

    # Prepare the system prompt (you can tweak this depending on your setup)
    sys_prompt = config.SYSTEM_PROMPT

    # Build up the user message with context, history, and the new question
    user_message = f"Context: {context}\n\nQuestion: {question}\nAnswer:"

    # Include conversation history in the prompt for context
    if conversation_history:
        # Add history to the prompt, limiting the number of exchanges if necessary
        history_str = ""
        for message in conversation_history[-5:]:  # Limit history to last 5 exchanges
            history_str += f"{message['role'].capitalize()}: {message['content']}\n"

        user_message = history_str + user_message

    
    # Getting the model name
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    model_name = config_data['model']

    # Query the SAMBANOVA model using the OpenAI API
    completion = client.chat.completions.create(
        model= model_name,
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": user_message}],
        stream=True,
    )

    # Collect the response from the streamed API output
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""  # Append each chunk of the response

    # Add the user input and model response to the conversation history
    add_to_history(question, response)

    return response  # Return the final response
