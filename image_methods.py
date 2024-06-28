import pandas as pd
import pytesseract
from PIL import Image
import csv
import re
from pdf2image import convert_from_path

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

#pdf to image 
def pdf_to_image(pdf_path, output_folder):
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        page.save(f"{output_folder}/cheque_{i+1}.jpg", "JPEG")
        print("Successful PDF To Image Conversion!")

#extract text
def extract_text_from_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
    return text
print("Successful text extraction")

def parse_extracted_data(extracted_text):
    data = {}

    # Define regex patterns for each data field
    patterns = {
        "Date": r"Date: (\d{4}-\d{2}-\d{2})",
        "Account Number": r"Account Number: (\d+)",
        "Cheque Number": r"Cheque Number: (\d+)"
    }

    # Extract data using regex
    for field, pattern in patterns.items():
        match = re.search(pattern, extracted_text)
        if match:
            data[field] = match.group(1)
        else:
            data[field] = "Not found"

    return data

#text into csv
def write_to_csv(text, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Extracted Text"])
        writer.writerow([text])
        print("Successful csv conversion")
        
#csv into excel
def csv_to_excel(csv_file, excel_file):
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)
        
# Example usage
#pdf to image
pdf_file = "C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\cheque.pdf"  # Path to your PDF file
output_folder = "output"  # Output folder where images will be saved

pdf_to_image(pdf_file, output_folder)

#extarcted text
image_path = "C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\output\cheque_1.jpg"  # Path to the image file
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)

# Parse the extracted text

parsed_data = parse_extracted_data(extracted_text)

# Print parsed data
for field, value in parsed_data.items():
    print(f"{field}: {value}")
# Path to the CSV file
csv_file = "extracted_text.csv"  
write_to_csv(extracted_text, csv_file)

# Path to the Excel file
excel_file = "extracted_text.xlsx"  
csv_to_excel(csv_file, excel_file)