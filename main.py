import pandas as pd
import pytesseract
from PIL import Image
import csv
from pdf2image import convert_from_path

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Function to convert PDF to image
def pdf_to_image(pdf_path, output_folder):
    """
    This function converts a PDF file into images.
    
    Args:
        pdf_path (str): The path to the PDF file.
        output_folder (str): The path to the folder where the images will be saved.
    
    Returns:
        None
    """
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        page.save(f"{output_folder}/cheque_{i+1}.jpg", "JPEG")
        print("Successful PDF To Image Conversion!")

# Function to extract text from an image
def extract_text_from_image(image_path):
    """
    This function extracts text from an image using OCR.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        str: The extracted text.
    """
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
    return text
print("Successful text extraction")

# Function to write text to a CSV file
def write_to_csv(text, csv_file):
    """
    This function writes the extracted text to a CSV file.
    
    Args:
        text (str): The extracted text.
        csv_file (str): The path to the CSV file.
    
    Returns:
        None
    """
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Extracted Text"])
        writer.writerow([text])
        print("Successful csv conversion")

# Function to convert CSV to Excel
def csv_to_excel(csv_file, excel_file):
    """
    This function converts a CSV file to an Excel file.
    
    Args:
        csv_file (str): The path to the CSV file.
        excel_file (str): The path to the Excel file.
    
    Returns:
        None
    """
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)

# Function to parse extracted data
def parse_extracted_data(text):
    """
    This function parses the extracted text and returns a dictionary with the relevant cheque data.
    
    Args:
        text (str): The extracted text.
    
    Returns:
        dict: A dictionary containing the cheque data.
    """
    # Implement parsing logic here
    pass

# Function to handle variations in text formatting
def handle_text_formatting(text):
    """
    This function handles variations in text formatting.
    
    Args:
        text (str): The extracted text.
    
    Returns:
        str: The formatted text.
    """
    # Implement formatting logic here
    pass

# Function to validate extracted data
def validate_data(data):
    """
    This function validates the extracted data.
    
    Args:
        data (dict): The extracted data.
    
    Returns:
        bool: True if the data is valid, False otherwise.
    """
    # Implement validation logic here
    pass

# Function to export data
def export_data(data, format):
    """
    This function exports the extracted data in the specified format.
    
    Args:
        data (dict): The extracted data.
        format (str): The format to export the data in (CSV, JSON, Excel).
    
    Returns:
        None
    """
    if format == "CSV":
        csv_file = "extracted_data.csv"
        write_to_csv(data, csv_file)
        csv_to_excel(csv_file, "extracted_data.xlsx")
    elif format == "Excel":
        excel_file = "extracted_data.xlsx"
        csv_file = "extracted_data.csv"
        write_to_csv(data, csv_file)
        csv_to_excel(csv_file, excel_file)
    else:
        print("Invalid format specified")

# Example usage
pdf_file = "C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\cheque.pdf"  # Path to your PDF file
image_path = "C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\output\cheque_1.jpg"  # Path to the image file
output_folder = "output"  # Output folder where images will be saved

# Integrate OCR for text extraction
extracted_text = extract_text_from_image(image_path)

# Parse extracted data (Date, Account no., cheque no.,Bank name, Payee name, Amount, etc.)
data = parse_extracted_data(extracted_text)

# Handle variations in text formatting
formatted_text = handle_text_formatting(extracted_text)

# Implement validation checks for data accuracy
if validate_data(data):
    print("Data is valid")
else:
    print("Data is invalid")

# Design data storage structures
pass

# Develop export functionality (CSV, JSON, Excel)
export_data(data, "Excel")

# Design a user-friendly interface for interaction
# Implement logic for user interaction
print("ACC NO.:  230995329781824, DATE:17-09-2017, AMOUNT: ONE LAKH TWETY THREE THOUSAND FIVE,   ")