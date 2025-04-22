#Takes in a directory of images and combines them into a single image, grid-like format
#This is useful for comparing multiple images side by side

#Most of this is taken from functions from this repo: https://github.com/mapluisch/LLaVA-CLI-with-multiple-images

# I needed just the combined images part, so I could feed them into LLaVA for fine-tuning, so this is modified just to do that

import os
from PIL import Image
from math import ceil, sqrt
import numpy as np
from math import sqrt, floor

import argparse

import requests
from io import BytesIO

s = 0
step = 20

sequence_start = 1
sequence_end = 200

def load_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        response = requests.get(image_file)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(image_file).convert('RGB')
    return image

def parse_resolution(resolution_str):
    # try to parse a string into a resolution tuple for the grid output
    try:
        width, height = map(int, resolution_str.split(','))
        return width, height
    except Exception as e:
        raise argparse.ArgumentTypeError("Resolution must be w,h.") from e

# Combine images into single image, grid-like format, and allow row and column size to be variable

def expand_image_range_paths(paths):
    expanded_paths = []
    # check if specified --images is range of imgs
    for path in paths:
        if "{" in path and "}" in path:
            pre, post = path.split("{", 1)
            range_part, post = post.split("}", 1)
            start, end = map(int, range_part.split("-"))

            for i in range(start, end + 1):
                expanded_paths.append(f"{pre}{i}{post}")
        else:
            expanded_paths.append(path)

    return expanded_paths

def concatenate_images_grid(images, dist_images, output_size, s1, s3):
    images = images[s1::s3]

    num_images = len(images)
    print(f"With slicing, there are now {num_images} images")
    # calc grid size based on amount of input imgs
    grid_size = max(2, ceil(sqrt(num_images)))

    cell_width = (output_size[0] - dist_images * (grid_size - 1)) // grid_size
    cell_height = (output_size[1] - dist_images * (grid_size - 1)) // grid_size

    # create new img with output_size, black bg
    new_img = Image.new('RGB', output_size, (0, 0, 0))

    for index, img in enumerate(images):
        # calc img aspect ratio
        img_ratio = img.width / img.height
        # calc target aspect ratio per cell
        target_ratio = cell_width / cell_height

        # resize img to fit in cell
        if img_ratio > target_ratio:
            new_width = cell_width
            new_height = int(cell_width / img_ratio)
        else:
            new_width = int(cell_height * img_ratio)
            new_height = cell_height

        # resize img using lanczos filter
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        row = index // grid_size
        col = index % grid_size

        # calc x, y offsets for img positioning
        x_offset = col * (cell_width + dist_images) + (cell_width - new_width) // 2
        y_offset = row * (cell_height + dist_images) + (cell_height - new_height) // 2

        # paste resized img in calc pos
        new_img.paste(resized_img, (x_offset, y_offset))

    return new_img, num_images

def concatenate_images(images, strategy, dist_images, grid_resolution, s1, s3):
    if strategy == 'grid':
        return concatenate_images_grid(images, dist_images, grid_resolution, s1, s3)
    else:
        raise ValueError("Invalid concatenation strategy specified")

num_images = []

for sequence_num in range(sequence_start, sequence_end + 1):
    image_folder = f'sequences/{sequence_num:06d}/'
    print(f"Processing {image_folder}")

    image_files = expand_image_range_paths([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))])

    images = [load_image(img_file) for img_file in image_files]
    print(f"Loaded {len(images)} images")
    image, num_image = concatenate_images(images, "grid", 20, parse_resolution('2560,1440'), s, step) if len(images) > 1 else images[0]
    num_images.append(num_image)
    image.save(f"outputs/tmp/{sequence_num:06d}.jpg")

#Save box and whisker plot of number of images per sequence
import matplotlib.pyplot as plt
import numpy as np

# remove outliers using 1.5xIQR rule
Q1 = np.percentile(list, 25)
Q3 = np.percentile(list, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
list = [x for x in list if x >= lower_bound and x <= upper_bound]

# boxplot of data

plt.boxplot(list)
plt.title('Number of Images Concatenated per Sequence')
plt.ylabel('Number of Images Concatenated')
plt.xlabel('All 200 Sequences (outliers removed)')
#plot the mean and the value of it

mean = np.mean(list)
plt.axhline(y=mean, color='r', linestyle='-', label='Mean')
plt.text(1.1, mean+0.3, f'Mean = {mean:.1f} images', color = 'red')

#Save
plt.savefig('outputs/num_images_per_sequence.png')
plt.show()