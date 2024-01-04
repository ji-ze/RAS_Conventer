# Import PyQt6 modules
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QComboBox, QGridLayout

from convertor import Convertor as Convert


# Define a custom widget class
class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        # Set the window title and size
        self.setWindowTitle('Image Converter')
        self.resize(400, 300)
        # Create a grid layout
        self.layout = QGridLayout()
        # Create a button for selecting files
        self.select_button = QPushButton('Select Files')
        # Connect the button to a function
        self.select_button.clicked.connect(self.select_files)
        # Add the button to the layout
        self.layout.addWidget(self.select_button, 0, 0, 1, 2)
        # Create a label for showing the selected files
        self.files_label = QLabel('No files selected')
        # Add the label to the layout
        self.layout.addWidget(self.files_label, 1, 0, 1, 2)
        # Create a button for choosing the output directory
        self.output_button = QPushButton('Choose Output Directory')
        # Connect the button to a function
        self.output_button.clicked.connect(self.choose_output)
        # Add the button to the layout
        self.layout.addWidget(self.output_button, 2, 0, 1, 2)
        # Create a label for showing the output directory
        self.output_label = QLabel('No output directory chosen')
        # Add the label to the layout
        self.layout.addWidget(self.output_label, 3, 0, 1, 2)
        # Create a label for choosing the output format
        self.format_label = QLabel('Choose Output Format')
        # Add the label to the layout
        self.layout.addWidget(self.format_label, 4, 0)
        # Create a combo box for choosing the output format
        self.format_combo = QComboBox()
        # Add some common image formats to the combo box
        self.format_combo.addItems(['PNG', 'TIFF', 'GIF'])
        # Add the combo box to the layout
        self.layout.addWidget(self.format_combo, 4, 1)

        # Create a button for converting the files
        self.convert_button = QPushButton('Convert')
        # Connect the button to a function
        self.convert_button.clicked.connect(self.convert_files)
        # Add the button to the layout
        self.layout.addWidget(self.convert_button, 5, 0, 1, 2)
        # Create a label for showing the conversion status
        self.status_label = QLabel('Ready')
        # Add the label to the layout
        self.layout.addWidget(self.status_label, 6, 0, 1, 2)
        # Set the layout for the widget
        self.setLayout(self.layout)
        # Initialize some attributes
        self.files = []  # A list of file paths
        self.output_dir = ''  # The output directory path
        self.output_format = 'JPEG'  # The output format
        self.converted = 0  # The number of converted files

    # Define a function for selecting files
    def select_files(self):
        # Use a file dialog to select one or more image files
        self.files, _ = QFileDialog.getOpenFileNames(self, 'Select Files', '',
                                                     'Image Files (*.rasx *.bin)')
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
            return
        # Check if an output directory is chosen
        if not self.output_dir:
            # Show a message
            self.status_label.setText('No output directory chosen')
            return
        # Get the output format from the combo box
        self.output_format = self.format_combo.currentText()
        # Loop through the selected files
        for file in self.files:
            # Try to convert the file
            try:
                # Get the file name without the extension
                file_name = file.split('/')[-1]#.split('.')[0]
                # Construct the output file path
                output_file = f'{self.output_dir}/{file_name}.{self.output_format.lower()}'
                # Convert the image to the output format
                Convert(file, output_file)
                # Increment the converted counter
                self.converted += 1
            # Handle any exceptions
            except Exception as e:
                # Show the error message
                self.status_label.setText(f'Error: {e}')
                return
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

