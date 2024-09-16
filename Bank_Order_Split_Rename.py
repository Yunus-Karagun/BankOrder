import fitz  # PyMuPDF
import numpy as np
import cv2
import pyzxing
import os
import time
from PIL import Image

def detect_qr_code_pyzxing(img):
    reader = pyzxing.BarCodeReader()
    temp_image_path = "temp_image.png"
    Image.fromarray(img).save(temp_image_path)
    barcodes = reader.decode(temp_image_path)
    os.remove(temp_image_path)
    if barcodes:
        return barcodes[0].parsed
    return None

def detect_qr_code_opencv(img):
    decoded_text, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    if decoded_text:
        return decoded_text
    return None

def detect_qr_code(img):
    data = detect_qr_code_pyzxing(img)
    if not data:
        data = detect_qr_code_opencv(img)
    return data

# Define the directory where the PDF files are stored
pdf_dir = 'D:/Talimat/'

# Loop through each PDF file in the directory
for pdf_file in os.listdir(pdf_dir):
    if not pdf_file.endswith('.pdf'):
        continue

    print(f"Processing file: {pdf_file}")
    
    # Load the PDF document and get the number of pages
    pdf_path = os.path.join(pdf_dir, pdf_file)
    pdf_doc = fitz.open(pdf_path)
    num_pages = pdf_doc.page_count

    # Loop through each page of the PDF file
    for i in range(num_pages):
        # Load the page and define a matrix to transform the coordinates
        page = pdf_doc.load_page(i)
        mat = fitz.Matrix(4, 4)
        
        # Load the entire page as an image
        rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
        pix = page.get_pixmap(alpha=False, matrix=mat, clip=rect)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect QR codes
        qr_code_data = detect_qr_code(gray)
        
        if qr_code_data:
            new_filename = qr_code_data + '.pdf'
        else:
            new_filename = f'YK-{time.strftime("%Y%m%d")}-{i+1}.pdf'
        
        count = 1
        while os.path.exists(os.path.join(pdf_dir, new_filename)):
            if qr_code_data:
                new_filename = qr_code_data + str(count) + '.pdf'
            else:
                new_filename = f'YK-{time.strftime("%Y%m%d")}-{i+1}-{count}.pdf'
            count += 1
        
        new_path = os.path.join(pdf_dir, new_filename)
        pdf_writer = fitz.Document()
        pdf_writer.insert_pdf(pdf_doc, from_page=i, to_page=i)
        pdf_writer.save(new_path)
        
    pdf_doc.close()
    os.remove(pdf_path)

