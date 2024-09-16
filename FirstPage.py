import PyPDF2
from PyPDF2 import PdfReader
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import os

def read_first_page_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        first_page = reader.pages[0]
        text = first_page.extract_text()
        return text

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None

def save_first_page_as_image(pdf_path, image_path):
    from pdf2image import convert_from_path
    pages = convert_from_path(pdf_path, 300)
    first_page = pages[0]
    first_page.save(image_path, 'PNG')

def rename_pdf_with_qr(pdf_path):
    # Save first page as image
    image_path = 'first_page.png'
    save_first_page_as_image(pdf_path, image_path)

    # Read QR code from the image
    qr_code_text = read_qr_code(image_path)

    if qr_code_text:
        # Rename PDF file
        new_pdf_path = os.path.join(os.path.dirname(pdf_path), f"{qr_code_text}.pdf")
        os.rename(pdf_path, new_pdf_path)
        print(f"PDF renamed to: {new_pdf_path}")
    else:
        print("No QR code found on the first page.")

    # Clean up
    os.remove(image_path)

# Example usage
pdf_file_path = 'example.pdf'  # Replace with your PDF file path
rename_pdf_with_qr(pdf_file_path)
