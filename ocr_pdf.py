import subprocess
import stat
import os
import streamlit as st

# Set filepaths for pdfs to grab and where to send them.
PATH_TO_ORIGINAL_PDFs = "./MergedPDFs/"
PATH_TO_COMPRESSED_PDFS = "./CompressedPDFs/"
PATH_TO_PROCESSED_PDFS = "./OCRProcessedPDFs/" # Output folder

is_finished = False
def is_ocr_finished():
    return is_finished

# Get file names of PDF files and set write permissions.
pdfs_to_ocr = []
for file_name in os.listdir(PATH_TO_COMPRESSED_PDFS):
    os.chmod(PATH_TO_COMPRESSED_PDFS + file_name, stat.S_IWRITE)
    pdfs_to_ocr.append(file_name)

original_pdf_names = [file for file in os.listdir(PATH_TO_ORIGINAL_PDFs)]

# Run OCR software on PDF files.
def ocr_pdf_all():
    # Initialize progress bar.
    st.session_state["ocr_progress"] = 0
    ocr_prog_bar  = st.progress(
        st.session_state["ocr_progress"], 
        f"Adding OCR to PDFs... ({st.session_state.ocr_progress} of {len(pdfs_to_ocr)} complete)"
    )

    for ind in range(len(pdfs_to_ocr)):
        # Run OCR
        subprocess.run([
            "cmd.exe", 
            "/c", 
            "ocrmypdf", 
            f"{PATH_TO_COMPRESSED_PDFS}{pdfs_to_ocr[ind]}",     # Input file
            f"{PATH_TO_PROCESSED_PDFS}{original_pdf_names[ind]}"     # Output file
        ])
        # Update progress bar.
        st.session_state["ocr_progress"] += 1
        ocr_prog_bar.progress(
            st.session_state["ocr_progress"] / len(pdfs_to_ocr),
            f"Adding OCR to PDFs... ({st.session_state.ocr_progress} of {len(pdfs_to_ocr)} complete) - This step while take a while."
        )

    # Open folder with finalized PDFs once finished.
    os.startfile("OCRProcessedPDFs")
    is_finished = True
    return 0

