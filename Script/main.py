import sys

import numpy as np

import matplotlib.pyplot as plt


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


def display_as_grayscale_image(array_2d):

    plt.imshow(array_2d, cmap='gray', interpolation='nearest')

    plt.title('Grayscale Image')

    plt.colorbar()

    plt.show()


def main():

    file_name = "Image0.bin"

    # Read data from the binary file

    data = read_binary_file(file_name)

    # Create a 2D array

    array_2d = create_2d_array(data)

    # Display the 2D array as a grayscale image

    display_as_grayscale_image(array_2d)

    #height, width = np.array(data.shape, dtype=float) / dpi

    fig = plt.figure(figsize=(385/10, 775/10), dpi=10)

    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis('off')

    ax.imshow(array_2d, interpolation='none')

    fig.savefig('test.tif', dpi=10)


if __name__ == "__main__":

    main()
