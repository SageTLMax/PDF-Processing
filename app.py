from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import sys # Only needed for access to command line arguments

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kawaiaha'o Church Archives PDF Processor")

        # Style the font for a given widget.
        def apply_font_settings(widget, font_size=16, bold=False):
            # Setup the font styling.
            font = widget.font()
            font.setPointSize(font_size)
            font.setBold(bold)
            # Apply the font styling.
            widget.setFont(font)

        # Initialize title text
        title_text = QLabel("Welcome to the Kawaiaha'o Church Archives PDF Processor!")
        apply_font_settings(title_text, font_size=24, bold=True)
        # Set title alignment.
        title_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        apply_font_settings(app_desc_text, 16)

        # Setup the window layout.
        layout = QVBoxLayout()
        layout.addWidget(title_text)
        layout.addWidget(app_desc_text)

        main_container = QWidget()
        main_container.setLayout(layout)
        self.setCentralWidget(main_container)
        

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

