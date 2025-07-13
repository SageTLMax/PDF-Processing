from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path
import sys # Only needed for access to command line arguments

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kawaiaha'o Church Archives PDF Processor")
        self.widgets = []
        self.parent_folder = ""
        self.folders_to_merge = []


        # Initialize title text
        title_text = QLabel("Welcome to the Kawaiaha'o Church Archives PDF Processor!")
        self.widgets.append(title_text)
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
        self.widgets.append(app_desc_text)
        self.apply_font_settings(app_desc_text, 's')


        # Introduce Step 1 (choose folders to process).
        step_1_title = QLabel("STEP 1: Choose Folders to Process!")
        self.widgets.append(step_1_title)
        self.apply_font_settings(step_1_title, 'l', bold=True)

        # Explain Step 1.
        step_1_desc = QLabel("""<html>
            <p>First, click the button below. Then, choose the folder that
                contains all FA collections you want to make PDFs for.</p>
        </html>""")
        self.widgets.append(step_1_desc)
        self.apply_font_settings(step_1_desc, 's')

        # Step 1 Button.
        step_1_button = QPushButton("STEP 1: Location of Folders to Process")
        self.widgets.append(step_1_button)
        # Style the button.
        self.apply_font_settings(step_1_button, 's')
        # Add button functionality.
        step_1_button.clicked.connect(self.step_1_button_click)
        
        # Step 1 confirmation for folders to merge.
        self.parent_folder_conf = QLabel()
        self.widgets.append(self.parent_folder_conf)
        self.apply_font_settings(self.parent_folder_conf, 's')


        # Introduce Step 2 (Process the PDFs).
        step_2_title = QLabel("Step 2: Process PDFs!")
        self.widgets.append(step_2_title)
        self.apply_font_settings(step_2_title, 'l', bold=True)

        # Explain Step 2.
        step_2_desc = QLabel("""<html>
            <p>Next, we do all the processing automatically! This will
                make the PDFs, compress them, and apply OCR. 
                Just click the button below:</p>
        </html>""")
        self.widgets.append(step_2_desc)
        self.apply_font_settings(step_2_desc, 's')

        # Step 2 Button
        step_2_button = QPushButton("Step 2: Make PDFs!")
        self.widgets.append(step_2_button)
        # Style the button.
        self.apply_font_settings(step_2_button, 's')
        # Add button functionality.
        step_2_button.clicked.connect(self.step_2_button_click)
        self.apply_font_settings(step_2_button, 's')
        # Add button functionality.
        step_2_button.clicked.connect(self.step_2_button_click)


        # Setup the window layout.
        layout = QVBoxLayout()
        for widget in self.widgets:
            layout.addWidget(widget)

        main_container = QWidget()
        main_container.setLayout(layout)
        self.setCentralWidget(main_container)
    
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
        

    def step_2_button_click(self):
        print("Clicked.")



# For creating pop-up windows.
class CustomFileDialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kawaiaha'o Church Archives PDF Processor")

        self.setFileMode()

        # Setup confirmation buttons.
        button_options = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonBox = QDialogButtonBox(button_options)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Window Layout.
        layout = QVBoxLayout()
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

