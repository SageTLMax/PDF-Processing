import subprocess
import os
import ghostscript
import time

PATH_TO_MERGED_PDFS = "./MergedPDFs/"
PATH_TO_OUTPUT = "./CompressedPDFs/"

# Compression method #1.
def compress_with_pdfsizeopt():
    # Path names for PDFs to compress.
    pdfs_to_compress = ["." + PATH_TO_MERGED_PDFS + f for f in os.listdir(PATH_TO_MERGED_PDFS)]

    os.chdir("./pdfsizeopt/")
    for pdf_name in pdfs_to_compress:
        # Compress the PDF and save in the ExportedPDFs folder.
        # Add "--use-pngout=no" after "pdfsizeopt" if runtime is slow.
        subprocess.run(["cmd.exe", "/c", "pdfsizeopt", pdf_name, f"./{pdf_name}"])

# Compression method #2 (better).
def compress_with_ghostscript():
    # Path names for PDFs to compress.
    pdfs_to_compress = [PATH_TO_MERGED_PDFS + f for f in os.listdir(PATH_TO_MERGED_PDFS) if f != ".gitignore"]

    def compress_single_pdf(index):
        # Settings for Ghostscript compression.
        args = [
            "-q",
            "-dNOPAUSE",
            "-dBATCH",
            "-dSAFER",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/screen",
            "-dColorImageDownsampleType=/Bicubic",
            "-dColorImageResolution=144", 
            f"-sOutputFile={PATH_TO_OUTPUT}output{index}.pdf", # output file
            pdfs_to_compress[index],                           # input file
        ]

        # Compress with ghostscript.
        ghostscript.Ghostscript(*args)
    
    # #Initialize progress bar.
    # st.session_state["compression_progress"] = 0
    # compress_prog_bar  = st.progress(
    #     st.session_state["compression_progress"], 
    #     f"Compressing PDFs... ({st.session_state.compression_progress} of {len(pdfs_to_compress)} complete)"
    # )

    for pdf_num in range(len(pdfs_to_compress)):
        # Compress PDF
        compress_single_pdf(pdf_num)
        # # Update progress bar.
        # st.session_state["compression_progress"] += 1
        # compress_prog_bar.progress(
        #     st.session_state["compression_progress"] / len(pdfs_to_compress), 
        #     f"Compressing PDFs... ({st.session_state.compression_progress} of {len(pdfs_to_compress)} complete)"
        # )
    time.sleep(1)
    return 0
