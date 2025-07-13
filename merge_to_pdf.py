from PIL import Image 
from pathlib import Path
import regex

PATH_TO_MERGED_PDFS = "./MergedPDFs/" # Output folder

# Regex used to check if file is an image.
IS_IMAGE_REGEX = "^\.pdf|\.jpg|\.jpeg|\.tif|\.png$"

def merge_to_pdf(filepath, pdfname):
    """
    Takes the images within the folder designated by filepath and compiles them
    into a signle PDF file named filename.
    PARAMETERS:
    filepath: str; filepath of the folder containing images.
    pdfname: str; name to use when saving the PDF.
    """
    # Returns a list of all the images in a given folder.
    image_names = [str(name).split("\\")[-1] for name in Path(filepath).iterdir()]
    images = [
        Image.open(filepath + "/" + file) for file in image_names
            # Only use the image if it has an image-type file extension (.jpg, .tif, etc.)
            if regex.findall(IS_IMAGE_REGEX, file, regex.IGNORECASE, overlapped=True)
    ]

    # Where to save the created PDF.
    pdf_path = PATH_TO_MERGED_PDFS + pdfname + ".pdf"
        
    # Merge images and save the PDF.
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
