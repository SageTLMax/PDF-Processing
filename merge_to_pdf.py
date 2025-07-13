from PIL import Image 
from pathlib import Path
import regex

PATH_TO_MERGED_PDFS = "./MergedPDFs/" # Output folder

# Regex used to check if file is an image.
IS_IMAGE_REGEX = "^\.pdf|\.jpg|\.jpeg|\.tif|\.png$"

# Make a merged PDF for each desired folder.
def merge_to_pdf_all(folders_to_merge):
    # Get the names of all folders which we want to create merged PDFs for.
    folder_names = [name.split("\\")[-1] for name in folders_to_merge]

    # Make a merged PDF of all images for a given folder.
    def merge_to_pdf(filepath, filename):
        # Returns a list of all the images in a given folder.
        image_names = [str(name).split("\\")[-1] for name in Path(filepath).iterdir()]
        images = [
            Image.open(filepath + "/" + file) for file in image_names
                # Only use the image if it has an image-type file extension (.jpg, .tif, etc.)
                if regex.findall(IS_IMAGE_REGEX, file, regex.IGNORECASE, overlapped=True)
        ]

        # Where to save the created PDF.
        pdf_path = PATH_TO_MERGED_PDFS + filename + ".pdf"
            
        # Merge images and save the PDF.
        images[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
    # # Initialize progress bar.
    # st.session_state["merge_progress"] = 0
    # merge_prog_bar  = st.progress(
    #     st.session_state["merge_progress"], 
    #     f"Generating PDFs... ({st.session_state.merge_progress} of {len(folder_paths)} complete)"
    # )

    for folder_ind in range(len(folder_names)):
        # Create PDF of merged images
        merge_to_pdf(folders_to_merge[folder_ind], folder_names[folder_ind])
        # # Update progress bar using session state variable.
        # st.session_state["merge_progress"] += 1
        # merge_prog_bar.progress(
        #     st.session_state["merge_progress"] / len(folder_paths), 
        #     f"Generating PDFs... ({st.session_state.merge_progress} of {len(folder_paths)} complete)"
        # )
    return 0