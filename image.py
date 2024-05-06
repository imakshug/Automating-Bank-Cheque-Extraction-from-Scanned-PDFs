import pytesseract
from PIL import Image

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
    return text

# Example usage
image_path = "C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\output\cheque_1.jpg"  # Path to the image file
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)
