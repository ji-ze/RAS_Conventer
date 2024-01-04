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

    fig = plt.figure(figsize=(775/10, 385/10), dpi=10)

    ax = fig.add_axes([0, 0, 1, 1])

    ax.axis('off')

    ax.imshow(array_2d, interpolation='none')

    fig.savefig('test.png', dpi=10)
    plt.close()

    # Open the image using Pillow
    image = Image.open("test.png")
    img = image.load()
    for i in range(image.size[0] - 1):
        for j in range(image.size[1] - 1):
            R, G, B = (int(10**(img[i, j][0])), int(10**(img[i, j][1])), int(10**(img[i, j][2])))
            if R > 255:
                R = 255
            if G > 255:
                G = 255
            if B > 255:
                B = 255
            img[i, j] = (R, G, B)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save("test_upr.png")


if __name__ == "__main__":

    main()
