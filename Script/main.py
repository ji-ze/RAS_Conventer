# Import modules
from PyQt6.QtWidgets import QApplication, QSpinBox, QWidget, QFileDialog, QPushButton, QLabel, QComboBox, QGridLayout
from PyQt6.QtCore import Qt
from shutil import rmtree
from os import path
from platformdirs import user_pictures_dir
from convertor import Convertor as Convert

# version
ver = "0.0.3"


# Define a custom widget class
class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        # Set the window title and size
        self.setWindowTitle("Rasx Converter")
        self.resize(400, 300)

        # Create a grid layout
        self.layout = QGridLayout()

        # Create a info label
        self.info_label = QLabel("This is an images converter from the new Rigaku format to png, tiff and bmp.\n"
                                 "The application was developed by Jiri Zelenka in the Institute of Physics\n"
                                 "of the Czech Academy of Sciences in 2024.")
        # Add the label
        self.layout.addWidget(self.info_label, 0, 0, 1, 2)

        # Create a button for selecting files
        self.select_button = QPushButton('Select Files')
        # Connect the button to a function
        self.select_button.clicked.connect(self.select_files)
        # Add the button to the layout
        self.layout.addWidget(self.select_button, 1, 0, 1, 2)

        # Create a label for showing the selected files
        self.files_label = QLabel('No files selected')
        # Add the label to the layout
        self.layout.addWidget(self.files_label, 2, 0, 1, 2)

        # Create a button for choosing the output directory
        self.output_button = QPushButton('Choose Output Directory')
        # Connect the button to a function
        self.output_button.clicked.connect(self.choose_output)
        # Add the button to the layout
        self.layout.addWidget(self.output_button, 3, 0, 1, 2)

        # Create a label for showing the output directory
        self.output_label = QLabel('No output directory chosen')
        # Add the label to the layout
        self.layout.addWidget(self.output_label, 4, 0, 1, 2)

        # Create a label for choosing the output format
        self.format_label = QLabel('Choose Output Format')
        # Add the label to the layout
        self.layout.addWidget(self.format_label, 5, 0)

        # Create a combo box for choosing the output format
        self.format_combo = QComboBox()
        self.format_combo.setToolTip("Choose a format of output images")
        # Add some common image formats to the combo box
        self.format_combo.addItems(['PNG', 'TIFF', 'GIF'])
        # Add the combo box to the layout
        self.layout.addWidget(self.format_combo, 5, 1)

        self.label4 = QLabel('Contrast of image:')
        self.layout.addWidget(self.label4, 6, 0)

        self.spinbox = QSpinBox()

        self.spinbox.setRange(1, 10000)
        self.spinbox.setValue(3000)  # Set the default value
        self.spinbox.setToolTip("The signal is normally low. Write 1 for the original image.")
        self.layout.addWidget(self.spinbox, 6, 1)

        # Create a button for converting the files
        self.convert_button = QPushButton('Convert')
        # Connect the button to a function
        self.convert_button.clicked.connect(self.convert_files)
        # Add the button to the layout
        self.layout.addWidget(self.convert_button, 7, 0, 1, 2)

        # Create a label for showing the conversion status
        self.status_label = QLabel('Ready')
        # Add the label to the layout
        self.layout.addWidget(self.status_label, 8, 0, 1, 2)

        # Version of the app
        self.label5 = QLabel(f'Version {ver}')
        self.layout.addWidget(self.label5, 10, 0)

        # The webpage link to the project at GitHub
        self.weblink = QLabel(
            '<a href="https://github.com/ji-ze/RAS_Conventer/">Project webpage</a>')
        self.weblink.setOpenExternalLinks(True)
        self.weblink.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.weblink, 10, 1)

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Initialize some attributes
        self.files = []  # A list of file paths
        self.output_dir = ''  # The output directory path
        self.output_format = 'PNG'  # The output format
        self.converted = 0  # The number of converted files

    # Define a function for selecting files
    def select_files(self):
        # Use a file dialog to select one or more image files
        self.files, _ = QFileDialog.getOpenFileNames(self, 'Select Files', '',
                                                     'Image Files (*.rasx)')
        # Update the files label with the number of selected files
        self.files_label.setText(f'{len(self.files)} files selected')
        # Reset the conversion status
        self.status_label.setText('Ready')
        self.converted = 0

    # Define a function for choosing the output directory
    def choose_output(self):
        # Use a file dialog to select a directory
        self.output_dir = QFileDialog.getExistingDirectory(self, 'Choose Output Directory', '')
        # Update the output label with the output directory
        self.output_label.setText(self.output_dir)
        # Reset the conversion status
        self.status_label.setText('Ready')
        self.converted = 0

    # Define a function for converting the files
    def convert_files(self):
        # Check if any files are selected
        if not self.files:
            # Show a message
            self.status_label.setText('No files selected')
            return None

        # Check if an output directory is chosen
        if not self.output_dir:
            # Show a message
            self.status_label.setText('No output directory chosen')
            return None

        # Get the output format from the combo box
        self.output_format = self.format_combo.currentText()
        # Set contrast of output images (The signal in row data is too low)
        contrast = self.spinbox.value()

        # Loop through the selected files
        for file in self.files:
            # Try to convert the file
            try:
                # Get the file name without the extension
                file_name = file.split('/')[-1][:-4]
                # Construct the output file path
                output_file = f'{self.output_dir}/{file_name}.{self.output_format.lower()}'
                # Convert the rasx image to the output format
                Convert(file, output_file, contrast)
                # Increment the converted counter
                self.converted += 1
            # Handle any exceptions
            except Exception as e:
                # Show the error message
                self.status_label.setText(f'Error: {e}')
                return

        # Remove unziped files
        if path.exists(path.join(user_pictures_dir(), "Data0")):
            rmtree(path.join(user_pictures_dir(), "Data0"))
        # Show the conversion status
        self.status_label.setText(f'Converted {self.converted} files')


# Create a Qt application
app = QApplication([])
# Create an instance of the custom widget
converter = ImageConverter()
# Show the widget
converter.show()
# Run the application
app.exec()

