import subprocess
import os
import ghostscript

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
def compress_single_pdf_gs(foldername, folderpath):
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
        f"-sOutputFile={PATH_TO_OUTPUT}{foldername}.pdf", # output file
        PATH_TO_MERGED_PDFS + foldername + ".pdf",     # input file
    ]

    # Compress with ghostscript.
    ghostscript.Ghostscript(*args)

    return 0
