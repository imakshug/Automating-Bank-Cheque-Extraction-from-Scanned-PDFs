from pdf2image import convert_from_path

def pdf_to_image(pdf_path, output_folder):
    pages = convert_from_path(pdf_path)
    for i, page in enumerate(pages):
        page.save(f"{output_folder}/cheque_{i+1}.jpg", "JPEG")

# Example usage
pdf_file = "C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\cheque.pdf"  # Path to your PDF file
output_folder = "output"  # Output folder where images will be saved

pdf_to_image(pdf_file, output_folder)
