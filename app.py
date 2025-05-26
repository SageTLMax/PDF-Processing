import streamlit as st
import os
from full_execute import *
from merge_to_pdf import *
from compress_pdf import *
from ocr_pdf import *

PATH_TO_CSS = "./app_style.css"

# For loading CSS into the app.
def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")

load_css(PATH_TO_CSS)

# TITLE
st.header("Welcome to the Kawaiaha'o Archives PDF Merger and OCR Scanner!")

# ABOUT
st.html("""
        <h3>This application will do the following: </h3>
        <ul>
            <li>Grab a list of folders.</li>
            <li>For each folder, make a PDF of the merged images.</li>
            <li>For each PDF, try to compress it.</li>
            <li>For each PDF, add OCR capabilities to the document.</li>     
        </ul>  
""")


# STEP 1
st.html("""
        <h2> 
        1. To get started, click the button, which will open a folder. 
        Drag every folder you want to make a PDF for into this folder.
        </h2>
""")
def open_merge_folder():
    os.startfile("FoldersForMerging")
st.button(label="Step 1: Click me!", key="merge_folder_button", on_click=open_merge_folder)


# STEP 2
st.html("""
        <h2> 
        2. Once you have chosen the folders you want to make PDFs for in Step 1, 
        hit the button below:
        </h2>
        <ul>
            <li> Please be patient, as this step can take some time to complete.</li>
            <li> Once complete, the folder with OCR-processed PDFs will open automatically.</li>
        </el>
""")

# Initialize session state variables.
if "merge_progress" not in st.session_state:
    st.session_state["merge_progress"] = 0
if "compression_progress" not in st.session_state:
    st.session_state["compression_progress"] = 0
if "ocr_progress" not in st.session_state:
    st.session_state["ocr_progress"] = 0

# Button to generate PDFs.
if st.button(label="Step 2: Generate PDFs!", key="generate_button"):
    # Process each step with a loading prompt
    merge_compress_ocr()
    

# Cache Clearing
st.html("""
        <h2> 
        Press the button below to wipe the cache of stored PDFs (You will need
        to regenerate any PDFs unintentionally lost in this process):
        </h2>
""")
st.button(
    label="Clear Cache", 
    key="cache_delete_button", 
    on_click=clear_all_pdf_folders
)

