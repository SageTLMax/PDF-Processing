import subprocess

# Set filepaths for pdfs to grab.
PATH_TO_COMPRESSED_PDFS = "./CompressedPDFs/"

# Apply OCR to a single pdf file from the CompressedPDFs folder
def ocr_pdf(pdfname, save_location):
    # For preventing terminal window popups.
    CREATE_NO_WINDOW = 0x08000000

    # Run OCR
    subprocess.run(
        [
            "cmd.exe", 
            "/c", 
            "ocrmypdf", 
            f"{PATH_TO_COMPRESSED_PDFS}{pdfname}.pdf",     # Input file
            f"{save_location}/{pdfname}.pdf"               # Output file
        ],
        creationflags=CREATE_NO_WINDOW
    )
