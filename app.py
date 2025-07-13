from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path

from merge_to_pdf import merge_to_pdf_all
from compress_pdf import compress_with_ghostscript
from ocr_pdf import ocr_pdf_all
from full_execute import clear_all_pdf_folders

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
        self.folders_to_merge = []


        # Initialize title text
        title_text = QLabel("Welcome to the Kawaiaha'o Church Archives PDF Processor!")
        self.widgets["Home"].append(title_text)
        # Style title text.
        self.apply_font_settings(title_text, 'xl', bold=True)
        title_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        self.widgets["Home"].append(app_desc_text)
        # Style the text.
        self.apply_font_settings(app_desc_text, 's')

        # Introduce Step 1 (choose folders to process).
        step_1_title = QLabel("STEP 1: Choose Folders to Process!")
        self.widgets["Step 1"].append(step_1_title)
        self.apply_font_settings(step_1_title, 'l', bold=True)

        # Explain Step 1.
        step_1_desc = QLabel("""<html>
            <p>First, click the button below. Then, choose the folder that
                contains all FA collections you want to make PDFs for.</p>
        </html>""")
        self.widgets["Step 1"].append(step_1_desc)
        self.apply_font_settings(step_1_desc, 's')

        # Step 1 Button.
        step_1_button = QPushButton("STEP 1: Location of Folders to Process")
        self.widgets["Step 1"].append(step_1_button)
        # Style the button.
        self.apply_font_settings(step_1_button, 's')
        # Add button functionality.
        step_1_button.clicked.connect(self.step_1_button_click)
        
        # Step 1 confirmation for folders to merge.
        self.parent_folder_conf = QLabel()
        self.widgets["Step 1"].append(self.parent_folder_conf)
        self.apply_font_settings(self.parent_folder_conf, 's')


        # Introduce Step 2 (Process the PDFs).
        step_2_title = QLabel("Step 2: Process PDFs!")
        self.widgets["Step 2"].append(step_2_title)
        self.apply_font_settings(step_2_title, 'l', bold=True)

        # Explain Step 2.
        step_2_desc = QLabel("""<html>
            <p>Next, we do all the processing automatically! This will
                make the PDFs, compress them, and apply OCR. 
                Just click the button below:</p>
        </html>""")
        self.widgets["Step 2"].append(step_2_desc)
        self.apply_font_settings(step_2_desc, 's')

        # Step 2 Button
        step_2_button = QPushButton("Step 2: Make PDFs!")
        self.widgets["Step 2"].append(step_2_button)
        # Style the button.
        self.apply_font_settings(step_2_button, 's')
        # Add button functionality.
        step_2_button.clicked.connect(self.step_2_button_click)


        # Clear Cache Button
        cache_button = QPushButton("Remove Cached Files")
        self.widgets["Done"].append(cache_button)
        # Style the button.
        self.apply_font_settings(step_2_button, 's')
        # Add button functionality.
        cache_button.clicked.connect(self.cache_button_click)


        # Setup the window layout.
        
        # Initialize pages.
        pages = QTabWidget()
        pages.setTabPosition(QTabWidget.TabPosition.South)
        pages.setMovable(True)

        # Arrange the page widgets.
        home_page = QWidget()
        home_page.setLayout(self.create_page_layout("Home"))

        step1_page = QWidget()
        step1_page.setLayout(self.create_page_layout("Step 1"))

        step2_page = QWidget()
        step2_page.setLayout(self.create_page_layout("Step 2"))

        done_page = QWidget()
        done_page.setLayout(self.create_page_layout("Done"))

        # Create page tabs.
        name_to_page = {
            "Home": home_page,
            "Step 1": step1_page,
            "Step 2": step2_page,
            "Done": done_page,
        }
        for name, page in name_to_page.items():
            pages.addTab(page, name)
        
        self.setCentralWidget(pages)
    

    # Create a dialogue window to ask for parent of folders to process.
    def step_1_button_click(self):
        # Open dialogue window.
        window_title = "Choose Parent Folder:"
        parent_directory = QFileDialog.getExistingDirectory(self, window_title, "")

        # Store the parent folder.
        self.parent_folder = str(parent_directory)
        # Store the subdirectories.
        parent_path = Path(self.parent_folder)
        self.folders_to_merge = [
            str(name) for name in parent_path.iterdir() if name.is_dir()
        ]

        # Show what user has chosen as a QLabel.
        bullets = ["<li>" + folder.split("\\")[-1] + "</li>" for folder in self.folders_to_merge]
        self.parent_folder_conf.setText(f"""<html>
            <p>Choosing all folders in {self.parent_folder.split("/")[-1]}:<p>
            <ul>
                {"".join(bullets)}
            </ul>
        </html>""")
        

    # Process chosen PDFs upon click.
    def step_2_button_click(self):
        merge_to_pdf_all(self.folders_to_merge)
        compress_with_ghostscript()
        ocr_pdf_all(self.folders_to_merge)

        
    # Clear cahced files upon click.
    def cache_button_click(self):
        clear_all_pdf_folders()

    
    # Create the page layout for a given category ("home, step1, step2")
    def create_page_layout(self, category):
        main_layout = QVBoxLayout()
        for widget in self.widgets[category]:
            main_layout.addWidget(widget)
        return main_layout


    # Style the font for a given widget.
    def apply_font_settings(self, widget, font_size='s', bold=False):
        font_sizes = {
            's': 14,
            'l': 22,
            'xl': 26,
        }
        # Setup the font styling.
        font = widget.font()
        font.setPointSize(font_sizes[font_size])
        font.setBold(bold)
        # Apply the font styling.
        widget.setFont(font)


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

