import streamlit as st

PATH_TO_CSS = "./app_style.css"
folders_to_merge = "./FoldersForMerging"

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
        1. To get started, input the location of the folders you want to merge into PDFs:
        </h2>
""")
folders_to_merge = st.text_input(label="Input filepath of parent folder then hit ENTER:")

# STEP 2
st.html("""
        <h2> 
        2. Once you have chosen the location of folders you want to make PDFs for in Step 1, 
        hit the button below:
        </h2>
        <p>
        (If you encounter an error, please ensure that the filepath that you input is correct.)
        </p>
""")
st.button(label="Generate PDFs!", key="generate_button")

