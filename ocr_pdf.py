import subprocess

# Set filepaths for pdfs to grab.
PATH_TO_COMPRESSED_PDFS = "./CompressedPDFs/"

# Apply OCR to a single pdf file from the CompressedPDFs folder
def ocr_pdf(pdfname, save_location):
    # Run OCR
    subprocess.run([
        "cmd.exe", 
        "/c", 
        "ocrmypdf", 
        f"{PATH_TO_COMPRESSED_PDFS}{pdfname}.pdf",     # Input file
        f"{save_location}/{pdfname}.pdf"               # Output file
    ])
