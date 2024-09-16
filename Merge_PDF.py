import os
from PyPDF2 import PdfMerger

# Specify the directory where the PDF files are located
dir_path = r'd:\Talimat'

# Create a PdfMerger object
pdf_merger = PdfMerger()

# Loop through all PDF files in the directory and add them to the PdfMerger object
for filename in os.listdir(dir_path):
    if filename.endswith('.pdf'):
        pdf_merger.append(os.path.join(dir_path, filename))

# Specify the name of the merged PDF file and write it to disk
merged_file_path = os.path.join(dir_path, 'merged_file.pdf')
with open(merged_file_path, 'wb') as merged_file:
    pdf_merger.write(merged_file)

# Clean up the PdfMerger object
pdf_merger.close()

