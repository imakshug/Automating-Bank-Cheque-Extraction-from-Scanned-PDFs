import PyPDF2 # type: ignore
from PIL import Image # type: ignore
import io

# Function to recursively extract XObjects from a PDF
def extract_xobjects(obj, images):
    if "/XObject" in obj:
        x_object = obj["/XObject"]
        for obj_name in x_object:
            obj_ref = x_object[obj_name]
            if obj_ref and obj_ref.__class__.__name__ == 'Stream':
                if obj_ref['/Subtype'] == '/Image':
                    images.append(obj_ref)
            elif obj_ref and obj_ref.__class__.__name__ == 'DecodedStreamObject':
                extract_xobjects(obj_ref, images)
            elif obj_ref and obj_ref.__class__.__name__ == 'IndirectObject':
                extract_xobjects(obj_ref.getObject(), images)

# PDF file path
pdf_path = 'C:\Automating-Bank-Check-Extraction-from-Scanned-PDFs_Apr_2024\check1.pdf'

# Open the PDF file in binary mode
with open(pdf_path, 'rb') as file:
    try:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Iterate through each page
        for page_num in range(len(pdf_reader.pages)):
            # Get the page object
            page_obj = pdf_reader.pages[page_num]

            # Extract XObjects (images) from the page
            images = []
            extract_xobjects(page_obj, images)

            # Iterate through extracted images
            for i, img_ref in enumerate(images):
                # Get the image data
                image_data = img_ref.get_data()

                # Create a PIL Image object from the image data
                img = Image.open(io.BytesIO(image_data))

                # Save the image to a file
                img.save(f'page_{page_num}_image_{i}.png')
                print(f'Saved image: page_{page_num}_image_{i}.png')
    except Exception as e:
        print(f'Error occurred: {e}')
