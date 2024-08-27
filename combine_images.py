#Takes in a directory of images and combines them into a single image, grid-like format
#This is useful for comparing multiple images side by side

import os
import cv2
import numpy as np
from math import sqrt, floor

s = 0
step = 20
sequence_num = 101

# Combine images into single image, grid-like format, and allow row and column size to be variable

def combine_images(image_folder, output_name):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images = images[s::step]
    #Rows and cols numbers should depend on number of images
    rows = images.__len__()
    cols = 1

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    combined_image = np.zeros((height*rows, width*cols, 3), dtype=np.uint8)

    for i, image in enumerate(images):
        row = i // cols
        col = i % cols
        img = cv2.imread(os.path.join(image_folder, image))
        combined_image[row*height:(row+1)*height, col*width:(col+1)*width] = img

    cv2.imwrite(output_name, combined_image)

# Example usage
image_folder = f'sequences/000{str(sequence_num)}/'
output_name = f'outputs/tmp/combined_image_{str(sequence_num)}.jpg'

combine_images(image_folder, output_name)