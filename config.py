# File and folder paths configuration

# Input and output paths for PDFs and text files
PDF_INPUT_PATH = ""  # Leave empty for manual input via GUI
EXTRACTED_TEXT_PATH = "extracted_text.txt"
TEXT_CHUNKS_FOLDER = "Text_chunks"
FAISS_INDEX_PATH = "faiss_index.bin"

# API configuration
from dotenv import load_dotenv
import os

# get your API Key and API Url from https://sambanova.ai/ and write the key and url in `.env` file
load_dotenv()
SAMBANOVA_API_URL = os.getenv('SAMBANOVA_API_URL')
SAMBANOVA_API_KEY = os.getenv('SAMBANOVA_API_KEY')
