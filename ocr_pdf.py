import subprocess
import stat
import os

# Set filepaths for pdfs to grab and where to send them.
PATH_TO_ORIGINAL_PDFs = "./MergedPDFs/"
PATH_TO_COMPRESSED_PDFS = "./CompressedPDFs/"
PATH_TO_PROCESSED_PDFS = "./OCRProcessedPDFs/" # Output folder

# Get file names of PDF files and set write permissions.
pdfs_to_compress = []
for file_name in os.listdir(PATH_TO_COMPRESSED_PDFS):
    os.chmod(PATH_TO_COMPRESSED_PDFS + file_name, stat.S_IWRITE)
    pdfs_to_compress.append(file_name)

original_pdf_names = [file for file in os.listdir(PATH_TO_ORIGINAL_PDFs)]

# Run OCR software on PDF files.
for ind in range(len(pdfs_to_compress)):
    subprocess.run([
        "cmd.exe", 
        "/c", 
        "ocrmypdf", 
        f"{PATH_TO_COMPRESSED_PDFS}{pdfs_to_compress[ind]}",     # Input file
        f"{PATH_TO_PROCESSED_PDFS}{original_pdf_names[ind]}"     # Output file
    ])

