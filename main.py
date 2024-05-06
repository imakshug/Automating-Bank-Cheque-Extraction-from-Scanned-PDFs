import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pdf2image import convert_from_path  
import cv2 
from tqdm import tqdm 
import pandas as pd  
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\akarn\pytesseract-0.3.10\pytesseract'

def pdf_to_images(pdf_path, output_folder):
    # Open the PDF
    #hello
    pdf_document = fitz.open(pdf_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]
        
        # Convert the page to image
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save the image
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        img.save(image_path)

    # Close the PDF
    pdf_document.close()

def extract_text_from_images(image_folder):
    text = ""
    # Iterate over each image in the folder
    for image_path in os.listdir(image_folder):
        # Use PIL to open image
        with Image.open(os.path.join(image_folder, image_path)) as img:
            # Use pytesseract to extract text from image
            extracted_text = pytesseract.image_to_string(img)
            text += extracted_text + "\n"
    return text

# Path to your PDF file
pdf_path = r"C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\cheque1.pdf"
# Path to the folder where you want to save the images
output_folder = r"C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\output"

# Convert PDF to images
pdf_to_images(pdf_path, output_folder)

# Extract text from images
extracted_text = extract_text_from_images(output_folder)

# Print or use the extracted text
print(extracted_text)