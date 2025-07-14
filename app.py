from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path

from merge_to_pdf import merge_to_pdf
from compress_pdf import compress_single_pdf_gs
from ocr_pdf import ocr_pdf
from clean_folders import clear_all_pdf_folders

import sys # Only needed for access to command line arguments

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kawaiaha'o Church Archives PDF Processor")
        self.widgets = {
            "Home": [],
            "Step 1": [],
            "Step 2": [],
            "Done": [],
        }
        self.parent_folder = ""
        self.save_location = "None (Please use the button below)"
        self.has_save_location = self.save_location != "None (Please use the button below)"
        self.folders_to_merge = []


        # Initialize title text
        title_text = QLabel("Welcome to the Kawaiaha'o Church Archives PDF Processor!")
        title_text.setObjectName("title")
        self.widgets["Home"].append(title_text)

        # Add the description for how the app works.
        app_desc_text = QLabel("""<html>
            <p>This is a program that does the following:</p>
            <ul>
                <li>Take all images from a given folder.</li>
                <li>Compile all the images into a single PDF file.</li>
                <li>Compress the PDF file.</li>
                <li>Apply OCR capability to the PDF file.</li>
                <li>Repeat process for as many folders as needed.</li>
            </ul>
        </html>""")
        app_desc_text.setObjectName("appdesc")
        app_desc_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widgets["Home"].append(app_desc_text)


        # Introduce Step 1 (choose folders to process).
        step_1_header = QLabel("STEP 1: Choose Folders to Process!")
        step_1_header.setObjectName("header")
        self.widgets["Step 1"].append(step_1_header)

        # Explain Step 1.
        step_1_desc = QLabel("""<html>
            <p>First, click the button below. Then, choose the folder that
                contains all FA collections you want to make PDFs for.</p>
        </html>""")
        step_1_desc.setObjectName("step1desc")
        self.widgets["Step 1"].append(step_1_desc)

        # Step 1 Button.
        step_1_button = QPushButton("STEP 1: Location of Folders to Process")
        self.widgets["Step 1"].append(step_1_button)
        # Add button functionality.
        step_1_button.clicked.connect(self.step_1_button_click)
        
        # Step 1 confirmation for folders to merge.
        self.parent_folder_conf = QLabel()
        self.parent_folder_conf.setObjectName("parentconf")
        self.parent_folder_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widgets["Step 1"].append(self.parent_folder_conf)

        # Introduce Step 2 (Process the PDFs).
        step_2_header = QLabel("STEP 2: Process PDFs!")
        step_2_header.setObjectName("header")
        self.widgets["Step 2"].append(step_2_header)

        # Explain Step 2.
        step_2_desc = QLabel("""<html>
            <p>Next, we do all the processing automatically! This will
                make the PDFs, compress them, and apply OCR. </p>
            <p>Before processing, choose where to save the PDFs:</p>
        </html>""")
        step_2_desc.setWordWrap = True
        step_2_desc.setObjectName("step2desc")
        self.widgets["Step 2"].append(step_2_desc)

        # Save location label
        self.save_location_text = QLabel(f"Current save location: {self.save_location}")
        self.widgets["Step 2"].append(self.save_location_text)
        self.save_location_text.setObjectName("savelocation")

        # Save location button
        save_location_button = QPushButton("Choose Save Location")
        self.widgets["Step 2"].append(save_location_button)
        # Add button functionality.
        save_location_button.clicked.connect(self.save_button_click)

        # Step 2 Button
        self.step_2_button = QPushButton("Step 2: Make PDFs!")
        self.step_2_button.setObjectName("step2button")
        self.widgets["Step 2"].append(self.step_2_button)
        # Add button functionality.
        self.step_2_button.setEnabled(self.has_save_location)
        self.step_2_button.clicked.connect(self.step_2_button_click)


        # Done page header
        done_header = QLabel("All of your PDFs are done!")
        done_header.setObjectName("header")
        self.widgets["Done"].append(done_header)

        # Clear Cache Button
        cache_button = QPushButton("Remove Cached Files")
        cache_button.setObjectName("cachebutton")
        self.widgets["Done"].append(cache_button)
        # Add button functionality.
        cache_button.clicked.connect(self.cache_button_click)


        # Setup the window layout.
        
        # Initialize pages.
        pages = QTabWidget()
        pages.setTabPosition(QTabWidget.TabPosition.South)
        pages.setMovable(True)

        # Arrange the page widgets.
        home_page = QWidget()
        home_page.setObjectName("page")
        home_page.setLayout(self.create_page_layout("Home"))

        step1_page = QWidget()
        step1_page.setObjectName("page")
        step1_page.setLayout(self.create_page_layout("Step 1"))

        step2_page = QWidget()
        step2_page.setObjectName("page")
        step2_page.setLayout(self.create_page_layout("Step 2"))

        done_page = QWidget()
        done_page.setObjectName("page")
        done_page.setLayout(self.create_page_layout("Done"))

        # Create page tabs.
        name_to_page = {
            "Home >": home_page,
            "Step 1 >": step1_page,
            "Step 2 >": step2_page,
            "Done!": done_page,
        }
        for name, page in name_to_page.items():
            pages.addTab(page, name)
        
        self.setCentralWidget(pages)
    

    # Create a dialogue window to ask for parent of folders to process.
    def step_1_button_click(self):
        # Open dialogue window.
        window_title = "Choose Parent Folder:"
        parent_directory = QFileDialog.getExistingDirectory(self, window_title, "")

        # Store the chosen parent folder.
        self.parent_folder = str(parent_directory)
        # Store the subdirectories as a dictionary of foldername : folderpath pairs.
        parent_path = Path(self.parent_folder)
        self.folders_to_merge = {
            str(filepath).split("\\")[-1] : str(filepath) 
                for filepath in parent_path.iterdir() if filepath.is_dir()
        }
        if(self.has_save_location):
            self.step_2_button.setEnabled(True)

        # Show what user has chosen as a QLabel.
        bullets = ["<li>" + foldername + "</li>" for foldername in self.folders_to_merge.keys()]
        self.parent_folder_conf.setText(f"""<html>
            <p>Choosing all folders in {self.parent_folder.split("/")[-1]}:<p>
            <ul>
                {"".join(bullets)}
            </ul>
        </html>""")
        

    def save_button_click(self):
        window_title = "Choose Where to Save PDFs:"
        self.save_location = QFileDialog.getExistingDirectory(self, window_title, "").split("/")[-1]
        self.save_location_text.setText(f"Current save location: {self.save_location}")
        self.has_save_location = True
        if(self.parent_folder != ""):
            self.step_2_button.setEnabled(True)

    # Process chosen PDFs upon click.
    def step_2_button_click(self):
        # Generate PDF of merged images.
        for foldername, folderpath in self.folders_to_merge.items():
            merge_to_pdf(folderpath, foldername)
        # Compress each PDF.
        for foldername in self.folders_to_merge.keys():
            compress_single_pdf_gs(foldername)
        # Apply OCR to each PDF.
        for foldername in self.folders_to_merge.keys():
            ocr_pdf(foldername, self.save_location)

        
    # Clear cahced files upon click.
    def cache_button_click(self):
        clear_all_pdf_folders()

    
    # Create the page layout for a given category ("home, step1, step2")
    def create_page_layout(self, category):
        main_layout = QVBoxLayout()
        for widget in self.widgets[category]:
            main_layout.addWidget(widget)
        return main_layout


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()

# Set stylesheet.
with open("app_style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

