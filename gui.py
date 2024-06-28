import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

class CheckExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Check Extractor")
        
        # Create and place widgets
        self.label = tk.Label(root, text="Select PDF File:")
        self.label.pack()
        
        self.select_button = tk.Button(root, text="Browse", command=self.browse_pdf)
        self.select_button.pack()
        
        self.process_button = tk.Button(root, text="Process", command=self.extract_checks)
        self.process_button.pack()
        
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        
    def browse_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        
    def extract_checks(self):
        try:
            # Convert PDF to images
            images = convert_from_path(self.pdf_path)
            extracted_text = ""
            for img in images:
                # Convert image to text using OCR
                text = pytesseract.image_to_string(img)
                extracted_text += text + "\n\n"
            
            # Display extracted text
            self.result_label.config(text="Extracted Text:\n" + extracted_text)
        except Exception as e:
            self.result_label.config(text="Error: " + str(e))

# Create Tkinter application window
root = tk.Tk()
app = CheckExtractorApp(root)
root.mainloop()
