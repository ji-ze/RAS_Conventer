import sys, math

import numpy as np

import matplotlib.pyplot as plt

from PIL import Image



def read_binary_file(file_name):

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


def create_2d_array(data):

    # Reshape the 1D array into a 2D array of shape (200, 100)

    array_2d = data.reshape((385, 775))

    return array_2d


def main():

    file_name = "Image0.bin"

    # Read data from the binary file

    data = read_binary_file(file_name)

    # Create a 2D array

    array_2d = create_2d_array(data)

    # Display the 2D array as a grayscale image

    image = (np.flipud(array_2d))

    pillow_image = Image.fromarray(image*2550)
    pillow_image.save('output.png')



if __name__ == "__main__":

    main()
