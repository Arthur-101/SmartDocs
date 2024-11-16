import tkinter as tk
from tkinter import filedialog, messagebox
import config  # Import config file for paths
import Text_Extract  # Importing your existing scripts
import Divide_Chunk
import Embedding_and_vector
import Query_Database

class PDFProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Processor")

        # Initialize paths
        self.input_pdf = config.PDF_INPUT_PATH  # Default PDF input from config
        self.output_txt = config.EXTRACTED_TEXT_PATH
        self.chunk_folder = config.TEXT_CHUNKS_FOLDER
        self.index_path = config.FAISS_INDEX_PATH

        # GUI Layout
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="PDF Processor", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Load PDF Button
        self.load_pdf_button = tk.Button(self.root, text="Load PDF", command=self.load_pdf)
        self.load_pdf_button.pack(pady=10)

        # Extract Text Button
        self.extract_text_button = tk.Button(self.root, text="Extract Text", command=self.extract_text)
        self.extract_text_button.pack(pady=10)

        # Chunk Text Button
        self.chunk_text_button = tk.Button(self.root, text="Chunk Text", command=self.chunk_text)
        self.chunk_text_button.pack(pady=10)

        # Generate Embeddings Button
        self.generate_embeddings_button = tk.Button(self.root, text="Generate Embeddings", command=self.generate_embeddings)
        self.generate_embeddings_button.pack(pady=10)

        # Query the Database Button
        self.query_database_button = tk.Button(self.root, text="Query Database", command=self.query_database)
        self.query_database_button.pack(pady=10)

        # Quit Button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=20)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.input_pdf = file_path
            messagebox.showinfo("PDF Loaded", f"PDF file loaded: {file_path}")
        else:
            messagebox.showwarning("No File", "No PDF file selected.")

    def extract_text(self):
        if not self.input_pdf:
            messagebox.showwarning("No PDF", "Please load a PDF file first.")
            return

        try:
            Text_Extract.extract_and_save_text(self.input_pdf, self.output_txt)
            messagebox.showinfo("Extraction Completed", f"Text extracted to: {self.output_txt}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during text extraction: {str(e)}")

    def chunk_text(self):
        try:
            Divide_Chunk.chunk_and_save(input_file=self.output_txt, chunk_size=2000, overlap=200, output_dir=self.chunk_folder)
            messagebox.showinfo("Chunking Completed", f"Text chunked and saved in: {self.chunk_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during text chunking: {str(e)}")

    def generate_embeddings(self):
        try:
            Embedding_and_vector.generate_embeddings_and_index(chunk_folder=self.chunk_folder, index_path=self.index_path)
            messagebox.showinfo("Embedding Generation", f"Embeddings generated and saved to: {self.index_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during embedding generation: {str(e)}")

    def query_database(self):
        user_query = tk.simpledialog.askstring("Query", "Enter your query:")
        if user_query:
            try:
                response = Query_Database.query_faiss_snova(user_query, top_k=5, chunk_folder=self.chunk_folder, index_path=self.index_path)
                messagebox.showinfo("Query Response", f"Response: {response}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during querying: {str(e)}")
        else:
            messagebox.showwarning("No Query", "Please enter a query.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFProcessorApp(root)
    root.mainloop()
