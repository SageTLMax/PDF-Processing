from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QRunnable, pyqtSignal, pyqtSlot, QObject, QThreadPool
from PyQt6 import QtGui
from pathlib import Path

from merge_to_pdf import merge_to_pdf
from compress_pdf import compress_single_pdf_gs
from ocr_pdf import ocr_pdf
from clean_folders import clear_all_pdf_folders

import sys # Only needed for access to command line arguments


class WorkerSignals(QObject):
    merge_progress = pyqtSignal(int)
    compress_progress = pyqtSignal(int)
    ocr_progress = pyqtSignal(int)

    merge_finished = pyqtSignal(bool)
    compress_finished = pyqtSignal(bool)
    ocr_finished = pyqtSignal(bool)

class JobRunner(QRunnable):
    def __init__(self, folders_for_merging, category, save_path):
        super().__init__()

        self.folders = folders_for_merging
        self.category = category
        self.save_path = save_path
        self.progress = 0
        self.signals = WorkerSignals()

        # For obtaining data based on processing category.
        self.category_to_pdf_func = {
            "merge": merge_to_pdf,
            "compress": compress_single_pdf_gs,
            "ocr": ocr_pdf
        }

        self.update_signals = {
            "merge": self.signals.merge_progress,
            "compress": self.signals.compress_progress,
            "ocr": self.signals.ocr_progress,
        }

        self.finish_signals = {
            "merge": self.signals.merge_finished,
            "compress": self.signals.compress_finished,
            "ocr": self.signals.ocr_finished,
        }

    @pyqtSlot()
    def run(self):
        # Go through each file.
        for name, path in self.folders.items():
            self.process_pdf(name, path)

        # If done with all files, emit finished signal.
        self.finish_signals[self.category].emit(True)

    # Process a single PDF file.
    def process_pdf(self, name, path):
        # Apply processing function depending on category.
        if self.category == "ocr":
            self.category_to_pdf_func[self.category](name, self.save_path) 
        else:
            self.category_to_pdf_func[self.category](name, path)
        # Update progress and emit signal to change progress bar.
        self.progress += 1
        self.update_signals[self.category].emit(self.progress)


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
        self.setWindowIcon(QtGui.QIcon("app_icon.png"))

        self.parent_folder = ""
        self.save_path = "None (Please use the button below)"
        self.has_save_location = self.save_path != "None (Please use the button below)"
        self.folders_to_merge = []

        # Some progress bar variables.
        self.merge_msg = "Generating PDFs..."
        self.compress_msg = "Compressing PDFs..."
        self.ocr_msg = "Applying OCR to PDFs..."
        self.start_of_processing = True


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
        self.parent_folder_path = QLineEdit()
        self.folder_list = QLabel()
        self.parent_folder_path.setReadOnly(True)
        self.parent_folder_path.setVisible(False)
        self.folder_list.setObjectName("parentconf")
        self.folder_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Setup layout for inline elements.
        parent_layout = QHBoxLayout()
        parent_layout.addWidget(self.parent_folder_conf)
        parent_layout.addWidget(self.parent_folder_path)
        folder_parent_container = QWidget()
        folder_parent_container.setLayout(parent_layout)
        
        # Add widgets to page.
        self.widgets["Step 1"].append(folder_parent_container)
        self.widgets["Step 1"].append(self.folder_list)


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
        self.save_location_prefix = QLabel(f"Current save location: ")
        self.save_location_text = QLineEdit(f"{self.save_path}")
        self.save_location_text.setReadOnly(True)
        # Set layout for label
        save_location_layout = QHBoxLayout()
        save_location_layout.addWidget(self.save_location_prefix)
        save_location_layout.addWidget(self.save_location_text)
        # Apply layout for label
        save_location_container = QWidget()
        save_location_container.setLayout(save_location_layout)
        self.widgets["Step 2"].append(save_location_container)
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

        # Merge Progress Bar
        self.merge_progresslabel = QLabel("")
        self.merge_progressbar = QProgressBar()
        self.widgets["Step 2"].append(self.merge_progresslabel)
        self.widgets["Step 2"].append(self.merge_progressbar)
        self.merge_progressbar.setVisible(False)
        
        # Compress Progress Bar
        self.compress_progresslabel = QLabel("")
        self.compress_progressbar = QProgressBar()
        self.widgets["Step 2"].append(self.compress_progresslabel)
        self.widgets["Step 2"].append(self.compress_progressbar)
        self.compress_progressbar.setVisible(False)

        # OCR Progress Bar
        self.ocr_progresslabel = QLabel("")
        self.ocr_progressbar = QProgressBar()
        self.widgets["Step 2"].append(self.ocr_progresslabel)
        self.widgets["Step 2"].append(self.ocr_progressbar)
        self.ocr_progressbar.setVisible(False)
        
        
        # Done page header
        self.done_header = QLabel("Go to the previous pages to process PDFs!")
        self.done_header.setObjectName("header")
        self.widgets["Done"].append(self.done_header)

        # Done page description
        self.done_desc = QLabel("")
        self.done_desc.setObjectName("step1desc")
        self.widgets["Done"].append(self.done_desc)

        # Save location reminder:
        self.save_reminder = QLineEdit()
        self.save_reminder.setReadOnly(True)
        self.widgets["Done"].append(self.save_reminder)
        self.save_reminder.setVisible(False)

        # Cache clear header
        cache_header = QLabel("Options (Clear Cache):")
        cache_header.setObjectName("optionsheader")
        self.widgets["Done"].append(cache_header)

        # Cache clear description
        cache_desc = QLabel("The button below is not necessary, but cleans up some of the space used in making the PDFs.")
        cache_desc.setObjectName("step1desc")
        self.widgets["Done"].append(cache_desc)

        # Clear Cache Button
        cache_button = QPushButton("Remove Cached Files")
        cache_button.setObjectName("cachebutton")
        self.widgets["Done"].append(cache_button)
        # Add button functionality.
        cache_button.clicked.connect(self.cache_button_click)


        # Setup the window layout.
        
        # Initialize pages.
        self.pages = QTabWidget()
        self.pages.setTabPosition(QTabWidget.TabPosition.South)
        self.pages.setMovable(False)

        # Create page tabs.
        name_to_page = {
            "Home >": self.create_page("Home"),
            "Step 1 >": self.create_page("Step 1"),
            "Step 2 >": self.create_page("Step 2"),
            "Done!": self.create_page("Done"),
        }
        for name, page in name_to_page.items():
            self.pages.addTab(page, name)
        
        self.setCentralWidget(self.pages)
    

    # Create a dialogue window to ask for parent of folders to process.
    def step_1_button_click(self):
        # Open dialogue window.
        window_title = "Choose Parent Folder:"
        parent_directory = QFileDialog.getExistingDirectory(self, window_title, "")

        # Set self.parent_folder and self.folders_to_merge
        self.save_processing_folders_and_parent(parent_directory)

        # Step 2 button enabling/disabling
        self.check_can_process()

        # In line path confirmation for parent folder..
        self.parent_folder_conf.setText("Choosing all folders in: ")
        self.parent_folder_path.setText(f"{self.parent_folder}")
        self.parent_folder_path.setVisible(True)
        # List of folders in parent folder.
        bullets = ["<li>" + foldername + "</li>" for foldername in self.folders_to_merge.keys()]
        self.folder_list.setText(f"""<html>
            <ul>
                {"".join(bullets)}
            </ul>
        </html>""")
        

    def save_button_click(self):
        # Choose folder for saving PDFs
        window_title = "Choose Where to Save PDFs:"
        self.save_path = QFileDialog.getExistingDirectory(self, window_title, "")
        self.save_location_text.setText(f"{self.save_path}")
        
        # Step 2 button enabling/disabling
        self.has_save_location = True
        self.check_can_process()

    # Process chosen PDFs upon click.
    def step_2_button_click(self):
        # Thread runner
        self.threadpool = QThreadPool()

        # Create runner for PDF merging.
        self.mergeRunner = JobRunner(self.folders_to_merge, "merge", self.save_path)
        self.mergeRunner.signals.merge_progress.connect(self.update_func("merge"))
        self.mergeRunner.signals.merge_finished.connect(lambda _: self.threadpool.start(self.compressRunner))
        # Create runner for PDF compression.
        self.compressRunner = JobRunner(self.folders_to_merge, "compress", self.save_path)
        self.compressRunner.signals.compress_progress.connect(self.update_func("compress"))
        self.compressRunner.signals.compress_finished.connect(self.finish_compress)
        # Create runner for PDF OCR Scanninng.
        self.ocrRunner = JobRunner(self.folders_to_merge, "ocr", self.save_path)
        self.ocrRunner.signals.ocr_progress.connect(self.update_func("ocr"))
        self.ocrRunner.signals.ocr_finished.connect(self.finish_ocr)

        # Setup progressbar ranges and labels.
        self.setup_progress_bars()

        # Start running threads.
        self.threadpool.start(self.mergeRunner)

        
    # Clear cahced files upon click.
    def cache_button_click(self):
        clear_all_pdf_folders()
        self.reset_progress_bars()


    def save_processing_folders_and_parent(self, parent_directory):
        # Store the chosen parent folder.
        self.parent_folder = str(parent_directory)
        # Store the subdirectories as a dictionary of foldername : folderpath pairs.
        parent_path = Path(self.parent_folder)
        self.folders_to_merge = {
            str(filepath).split("\\")[-1] : str(filepath) 
                for filepath in parent_path.iterdir() if filepath.is_dir()
        }


    # Enable/Disable Step 2 button depending on if there is a valid save location
    # and that there's actual folders to process.
    def check_can_process(self):
        if(self.has_save_location and len(self.folders_to_merge) > 0):
            self.step_2_button.setEnabled(True)
        else:
            self.step_2_button.setEnabled(False)


    # Create the page layout for a given category ("home, step1, step2")
    def create_page_layout(self, category):
        main_layout = QVBoxLayout()
        for widget in self.widgets[category]:
            main_layout.addWidget(widget)
        return main_layout
    

    # Create the page for a given category and apply layout.
    def create_page(self, category):
        home_page = QWidget()
        home_page.setObjectName("page")
        home_page.setLayout(self.create_page_layout(category))
        return home_page

    
    # Set the label for a progress bar.
    def make_label(self, label, message, value, ocr_started=False):
        text = f"{message} ({value} of {len(self.folders_to_merge)} completed)"
        if(ocr_started):
            text += " - This may take a while..."
        label.setText(text)


    # Returns a function for updating a progress bar to use with signals
    def make_update_func(self, bar, label, message):
        # Function to activate upon receiving a signal.
        def update_progress_bar(value):
            bar.setValue(value)
            self.make_label(
                label, 
                message, 
                value, 
                message==self.ocr_msg and not self.start_of_processing
            )
        return update_progress_bar


    # Returns the function to update progress bar depending on category.
    def update_func(self, category):
        category_to_update_func = {
            "merge": self.make_update_func(
                    self.merge_progressbar, 
                    self.merge_progresslabel, 
                    self.merge_msg
                ),
            "compress": self.make_update_func(
                    self.compress_progressbar, 
                    self.compress_progresslabel, 
                    self.compress_msg
                ),
            "ocr": self.make_update_func(
                    self.ocr_progressbar, 
                    self.ocr_progresslabel, 
                    self.ocr_msg
                ),
        }
        return category_to_update_func[category]


    # Setup progressbar range and labels.
    def setup_progress_bars(self):
        # Update progressbar variables so they have valid range.
        self.merge_progressbar.setRange(0, len(self.folders_to_merge))
        self.compress_progressbar.setRange(0, len(self.folders_to_merge))
        self.ocr_progressbar.setRange(0, len(self.folders_to_merge))

        # Show progress bars.
        self.merge_progressbar.setVisible(True)
        self.compress_progressbar.setVisible(True)
        self.ocr_progressbar.setVisible(True)

        # Setup the labels for the progress bars.
        self.make_label(self.merge_progresslabel, self.merge_msg, 0)
        self.make_label(self.compress_progresslabel, self.compress_msg, 0)
        self.make_label(self.ocr_progresslabel, self.ocr_msg, 0)

        # Reinitialize bars to reapply QSS styling.
        self.update_func("merge")(0)
        self.update_func("compress")(0)
        self.update_func("ocr")(0)


    def reset_progress_bars(self):
        # Show progress bars.
        self.merge_progressbar.setVisible(False)
        self.compress_progressbar.setVisible(False)
        self.ocr_progressbar.setVisible(False)

        # Setup the labels for the progress bars.
        self.merge_progresslabel.setText("")
        self.compress_progresslabel.setText("")
        self.ocr_progresslabel.setText("")

        # Reinitialize bars to reapply QSS styling.
        self.update_func("merge")(0)
        self.update_func("compress")(0)
        self.update_func("ocr")(0)


    # Run upon finishing compression.
    def finish_compress(self):
        self.start_of_processing = False
        self.make_label(self.ocr_progresslabel, self.ocr_msg, 0, True)
        self.threadpool.start(self.ocrRunner)


    # Run upon finishing OCR.
    def finish_ocr(self):
        # Update Done Page header.
        self.done_header.setText("All of your PDFs are done!")
        # Update save location reminder.
        self.done_desc.setText("The OCR-processed PDFs are complete. You saved the PDFs at:")
        self.save_reminder.setVisible(True)
        self.save_reminder.setText(f"{self.save_path}")
        # Navigate to Done page.
        self.pages.setCurrentIndex(3)


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

