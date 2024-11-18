# File and folder paths configuration

# Input and output paths for PDFs and text files
PDF_INPUT_PATH = ""  # Leave empty for manual input via GUI
EXTRACTED_TEXT_PATH = "extracted_text.txt"
TEXT_CHUNKS_FOLDER = "Text_chunks"
FAISS_INDEX_PATH = "faiss_index.bin"
ABOUT_PATH = "about.txt"

# API configuration
from dotenv import load_dotenv
import os

load_dotenv()
SAMBANOVA_API_URL = os.getenv('SAMBANOVA_API_URL')
SAMBANOVA_API_KEY = os.getenv('SAMBANOVA_API_KEY')


# System Prompt for the LLM
SYSTEM_PROMPT = """
    You are the personification of the provided document.
    Your task is to provide the best responses you can to the user's questions.
    You can also ask the user for clarifications if you think it's necessary.
    When asked, respond that 'I am the document' or something like that.
    Only answer the questions if it is about the provided document.
    If the question is not related to the document, respond that the question is out of document.
    """

# Model Name
MODEL = "Meta-Llama-3.1-405B-Instruct"
