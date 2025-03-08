from PyPDF2 import PdfReader
import config

# Extract text from each page of the PDF
def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()  # Extract text from page
    return text

# Write the extracted text to a file
def write_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

# Extract text from PDF and save to a text file
def extract_and_save_text(input_pdf=None, output_txt=config.EXTRACTED_TEXT_PATH):
    input_pdf = input_pdf or config.PDF_INPUT_PATH  # Use provided path or default
    if input_pdf:
        pdf_text = extract_pdf_text(input_pdf)  # Extract text from the PDF
        write_text_to_file(pdf_text, output_txt)  # Save text to file
    else:
        pass
