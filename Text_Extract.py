from PyPDF2 import PdfReader
import config  # Import the config file

def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def write_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def extract_and_save_text(input_pdf=None, output_txt=config.EXTRACTED_TEXT_PATH):
    # Use input_pdf from GUI or default path
    input_pdf = input_pdf or config.PDF_INPUT_PATH
    if input_pdf:
        pdf_text = extract_pdf_text(input_pdf)
        write_text_to_file(pdf_text, output_txt)
        print(f"Text has been extracted and written to '{output_txt}'")
    else:
        print("No PDF path provided!")
