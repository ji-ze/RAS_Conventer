# version: 0.0.2

# Import PyQt6 modules
from PyQt6.QtWidgets import QApplication, QSpinBox, QWidget, QFileDialog, QPushButton, QLabel, QComboBox, QGridLayout
import shutil, os
from platformdirs import user_pictures_dir
import os
import sys
import zipfile
import numpy as np
from PIL import Image
from platformdirs import user_pictures_dir


class Convertor:

    def __init__(self, input_file, output_file, contrast):
        self.input_file = input_file
        self.output_file = output_file
        self.contrast = contrast
        self.convert()

    def get_coordinates(self, filename):
        # open the file in read mode
        with open(filename, "r") as f:
            # loop through the lines until the 808th line
            for i in range(808):
                line = f.readline()
            # split the line by whitespace and convert to integers
            line = line.split(">")[1]
            line = line.split("<")[0]
            x, y = line.split(" ")
            # return the x and y values
            return int(x), int(y)

    def create_2d_array(self, data):

        # Reshape the 1D array into a 2D array of shape (200, 100)
        file = os.path.join(user_pictures_dir(), "Data0", "MesurementConditions0.xml")
        x, y = self.get_coordinates(file)
        array_2d = data.reshape((y, x))

        return array_2d

    def convert(self):
        if self.input_file[-4:] == "rasx":
            with zipfile.ZipFile(self.input_file, 'r') as zip_file:
                # Extract the Image.bin file to the current directory
                zip_file.extract("Data0/Image0.bin", user_pictures_dir())
                zip_file.extract("Data0/MesurementConditions0.xml", user_pictures_dir())
            self.input_file = os.path.join(user_pictures_dir(), "Data0", "Image0.bin")
            # resolution =  #MesurementConditions0 808 line

        # Read data from the binary file
        data = self.read_binary_file(self.input_file)

        # Create a 2D array
        array_2d = self.create_2d_array(data)

        # Display the 2D array as a grayscale image
        image = (np.flipud(array_2d))

        pillow_image = Image.fromarray(image * self.contrast)

        pillow_image.save(self.output_file)

    def read_binary_file(self, file_name):

        try:

            with open(file_name, 'rb') as file:

                # Read 20000 unsigned long integers

                data = np.fromfile(file, dtype=np.uint)

                return data

        except FileNotFoundError:

            print(f"Error: File '{file_name}' not found.")

            sys.exit(1)

        except Exception as e:

            print(f"Error reading file: {e}")

            sys.exit(1)



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
        self.format_combo.setToolTip("Choose a format of output images")
        # Add some common image formats to the combo box
        self.format_combo.addItems(['PNG', 'TIFF', 'GIF'])
        # Add the combo box to the layout
        self.layout.addWidget(self.format_combo, 4, 1)

        self.label4 = QLabel('Contrast of image:')
        self.layout.addWidget(self.label4, 5, 0)

        self.spinbox = QSpinBox()

        self.spinbox.setRange(1, 10000)
        self.spinbox.setValue(3000)  # Set the default value
        self.spinbox.setToolTip("The signal is normally low. Write 1 for the original image.")
        self.layout.addWidget(self.spinbox, 5, 1)



        # Create a button for converting the files
        self.convert_button = QPushButton('Convert')
        # Connect the button to a function
        self.convert_button.clicked.connect(self.convert_files)
        # Add the button to the layout
        self.layout.addWidget(self.convert_button, 6, 0, 1, 2)
        # Create a label for showing the conversion status
        self.status_label = QLabel('Ready')
        # Add the label to the layout
        self.layout.addWidget(self.status_label, 7, 0, 1, 2)
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
        contrast = self.spinbox.value()
        for file in self.files:
            # Try to convert the file
            try:
                # Get the file name without the extension
                file_name = file.split('/')[-1]#.split('.')[0]
                # Construct the output file path
                output_file = f'{self.output_dir}/{file_name}.{self.output_format.lower()}'
                # Convert the image to the output format
                Convertor(file, output_file, contrast)
                # Increment the converted counter
                self.converted += 1
            # Handle any exceptions
            except Exception as e:
                # Show the error message
                self.status_label.setText(f'Error: {e}')
                return
        if os.path.exists(os.path.join(user_pictures_dir(), "Data0")):
            shutil.rmtree(os.path.join(user_pictures_dir(), "Data0"))
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

