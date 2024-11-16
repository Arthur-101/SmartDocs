import os
import config

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks

def save_chunks(chunks, output_dir=config.TEXT_CHUNKS_FOLDER):
    os.makedirs(output_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        with open(f"{output_dir}/chunk_{i+1}.txt", 'w', encoding='utf-8') as file:
            file.write(chunk)

def chunk_and_save(input_file=config.EXTRACTED_TEXT_PATH, chunk_size=2000, overlap=200, output_dir=config.TEXT_CHUNKS_FOLDER):
    text = read_text_file(input_file)
    chunks = chunk_text(text, chunk_size, overlap)
    print(f"Text divided into {len(chunks)} chunks.")
    save_chunks(chunks, output_dir)
    print(f"Chunks saved in the '{output_dir}' directory.")
