import os
import sys
import zipfile
import matplotlib.pyplot as plt
import numpy as np


class Convertor:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.convert()

    def convert(self):
        if self.input_file[-4:] == "rasx":
            with zipfile.ZipFile(self.input_file, 'r') as zip_file:
                # Extract the Image.bin file to the current directory
                zip_file.extract("Data0/Image0.bin")
            self.input_file = os.path.join("Data0", "Image0.bin")
        # Read data from the binary file
        data = self.read_binary_file(self.input_file)

        # Create a 2D array
        array_2d = self.create_2d_array(data)

        fig = plt.figure(figsize=(775/10, 385/10), dpi=10)

        ax = fig.add_axes([0, 0, 1, 1])

        ax.axis('off')

        ax.imshow(array_2d, interpolation='none')

        fig.savefig(self.output_file, dpi=10)
        plt.close()


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


    def create_2d_array(self, data):

        # Reshape the 1D array into a 2D array of shape (200, 100)

        array_2d = data.reshape((385, 775))

        return array_2d


    def display_as_grayscale_image(self, array_2d):

        plt.imshow(array_2d, cmap='gray', interpolation='nearest')

        plt.title('Grayscale Image')

        plt.colorbar()

        plt.show()
