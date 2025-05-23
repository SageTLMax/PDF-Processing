import streamlit as st
from full_execute import *
import os

PATH_TO_CSS = "./app_style.css"
folders_to_merge = "./FoldersForMerging/"

# For obtaining the filepath in other files.
def get_folders_to_merge_filepath():
    return folders_to_merge

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
st.button(label="Step 2: Generate PDFs!", key="generate_button", on_click=merge_compress_ocr)

