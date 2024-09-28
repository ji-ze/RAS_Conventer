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
            # loop through the lines to get size of image
            for line in f:
                if line.find("<string>PXD_DETECTOR_DIMENSIONS</string>") != -1:
                    line = f.readline()
                    break
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
        with zipfile.ZipFile(self.input_file, 'r') as zip_file:
            # Extract the Image.bin file to the current directory
            zip_file.extract("Data0/Image0.bin", user_pictures_dir())
            zip_file.extract("Data0/MesurementConditions0.xml", user_pictures_dir())
        self.input_file = os.path.join(user_pictures_dir(), "Data0", "Image0.bin")

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
