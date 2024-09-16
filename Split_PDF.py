import os
from PyPDF2 import PdfReader, PdfWriter

# The path to the directory containing PDF files
directory_path = 'D:\\Talimat'

# Iterate over all the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.pdf'):
        # Create a PDF reader object
        reader = PdfReader(os.path.join(directory_path, filename))
        # Get the number of pages in the PDF
        num_pages = len(reader.pages)

        # Split each page into a separate PDF
        for i in range(num_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            output_filename = f"{filename[:-4]}_page_{i+1}.pdf"
            with open(os.path.join(directory_path, output_filename), 'wb') as output_pdf:
                writer.write(output_pdf)

        print(f"Split {filename} into {num_pages} pages.")
