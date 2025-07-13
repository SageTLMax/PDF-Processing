import subprocess

# Set filepaths for pdfs to grab and where to send them.
PATH_TO_COMPRESSED_PDFS = "./CompressedPDFs/"
PATH_TO_PROCESSED_PDFS = "./OCRProcessedPDFs/" # Output folder

# Apply OCR to a single pdf file from the CompressedPDFs folder
def ocr_pdf(pdfname):
    # Run OCR
    subprocess.run([
        "cmd.exe", 
        "/c", 
        "ocrmypdf", 
        f"{PATH_TO_COMPRESSED_PDFS}{pdfname}.pdf",     # Input file
        f"{PATH_TO_PROCESSED_PDFS}{pdfname}.pdf"     # Output file
    ])

