import os
import config

# Read the contents of a text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Split text into chunks with optional overlap
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):  # Create chunks with overlap
        chunks.append(text[i:i+chunk_size])  # Append each chunk to the list
    return chunks

# Save the chunks as separate text files in the specified directory
def save_chunks(chunks, output_dir=config.TEXT_CHUNKS_FOLDER):
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
    for i, chunk in enumerate(chunks):  # Iterate over each chunk
        with open(f"{output_dir}/chunk_{i+1}.txt", 'w', encoding='utf-8') as file:
            file.write(chunk)  # Write the chunk to a file

# Read, chunk, and save the text from the input file
def chunk_and_save(input_file=config.EXTRACTED_TEXT_PATH, chunk_size=2000, overlap=200, output_dir=config.TEXT_CHUNKS_FOLDER):
    text = read_text_file(input_file)  # Read the extracted text from the input file
    chunks = chunk_text(text, chunk_size, overlap)  # Chunk the text into smaller parts
    # print(f"Text divided into {len(chunks)} chunks.")
    save_chunks(chunks, output_dir)  # Save the chunks to the specified directory
    # print(f"Chunks saved in the '{output_dir}' directory.")
    chunk_length = len(chunks)

    return chunk_length
