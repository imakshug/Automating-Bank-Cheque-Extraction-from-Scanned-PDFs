from pdf2image import convert_from_path  
import pytesseract  
import cv2 
from PIL import Image  
from tqdm import tqdm 
import pandas as pd  
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\akarn\pytesseract-0.3.10\pytesseract'

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

# Function to extract checks from a PDF
def extract_checks_from_pdf(pdf_path, image_dir):
    # Convert PDF to images
    pages = convert_from_path(pdf_path)
    
    checks_data = []

    # Extract text from each image
    for page_num, page in enumerate(tqdm(pages, desc='Processing PDF')):
        image_path = f"{image_dir}\\page_{page_num}.png"
        page.save(image_path, 'PNG')

        # Extract text from image
        text = extract_text_from_image(image_path)

        # Extract check details from text
        check_details = extract_check_details(text)

        checks_data.append(check_details)

    return checks_data

# Function to extract check details from text using regular expressions
def extract_check_details(text):
    check_details = {
        'Check_Number': '', 
        'Amount': '', 
        'Date': ''
    }

    # Example regular expressions to extract check details
    check_number_pattern = r'Check Number: (\d+)'
    amount_pattern = r'Amount: \$([0-9,\.]+)'
    date_pattern = r'Date: (\d{2}/\d{2}/\d{4})'

    # Use regular expressions to extract check details from text
    check_details['Check_Number'] = re.search(check_number_pattern, text).group(1) if re.search(check_number_pattern, text) else ''
    check_details['Amount'] = re.search(amount_pattern, text).group(1) if re.search(amount_pattern, text) else ''
    check_details['Date'] = re.search(date_pattern, text).group(1) if re.search(date_pattern, text) else ''

    return check_details

# Function to save extracted checks to Excel
def save_to_excel(data, output_path):
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)

if __name__ == "__main__":
    # Input PDF path
    pdf_path = "C:\\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\\check1.pdf"

    # Directory to save extracted images
    image_dir = "C:\\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024"

    # Extract checks from PDF
    checks_data = extract_checks_from_pdf(pdf_path, image_dir)

    # Save extracted checks to Excel
    output_excel_path = "extracted_checks.xlsx"
    save_to_excel(checks_data, output_excel_path)
