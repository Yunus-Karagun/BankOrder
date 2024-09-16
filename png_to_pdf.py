import sys
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def images_to_pdf(output_dir, image_prefix, output_pdf):
    image_files = [os.path.join(output_dir, f) for f in sorted(os.listdir(output_dir)) if f.startswith(image_prefix) and f.endswith('.png')]
    
    if not image_files:
        print("No images found with the given prefix.")
        return
    
    # Create a canvas object using reportlab
    c = canvas.Canvas(output_pdf, pagesize=letter)
    
    for image_file in image_files:
        img = Image.open(image_file)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        pdf_width, pdf_height = letter

        # Calculate the image size to fit within the PDF page
        if aspect_ratio > 1:
            new_width = pdf_width
            new_height = pdf_width / aspect_ratio
        else:
            new_height = pdf_height
            new_width = pdf_height * aspect_ratio

        c.drawImage(image_file, 0, pdf_height - new_height, width=new_width, height=new_height)
        c.showPage()  # Create a new page in the PDF for each image

    c.save()  # Save the PDF

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python images_to_pdf.py <output_dir> <image_prefix> <output_pdf>")
        sys.exit(1)

    output_dir = sys.argv[1]
    image_prefix = sys.argv[2]
    output_pdf = sys.argv[3]

    images_to_pdf(output_dir, image_prefix, output_pdf)
