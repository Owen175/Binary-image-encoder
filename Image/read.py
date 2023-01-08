import logging
import PIL
from PIL import Image
import sys

try:
    filename = sys.argv[1]
    raw_binary = open(filename, 'r').read()
except IndexError:
    raw_binary = open('Binary/output.BIN', 'r').read()

# First 8 bits are colour depth. PIL cap is 255, so should not go higher than 8
colour_depth = int(raw_binary[0:4], 2)
if colour_depth > 8:
    logging.error(' Colour depth too high.')
    exit()

# After the colour depth, 16 bits are for the x and 16 more for the y
resolution = width, height = int(raw_binary[4:20], 2), int(raw_binary[20:36], 2)

metadata_length = 36

# Stored as RGB

RGB_data = raw_binary[metadata_length:]

if len(RGB_data) % (colour_depth * 3) != 0:
    logging.error(' Incorrect colour depth in input image.')
    exit()

if len(RGB_data) != 3 * colour_depth * width * height:
    logging.error(' Incorrect length of binary.')
    exit()

# Forms a 1d list of the colour data
RGB_1d_list = [int(RGB_data[i * colour_depth: (i + 1) * colour_depth], 2) for i in
               range(int(len(RGB_data) / colour_depth))]

# Splits the 1d list into RGB
RGB_1d_list_segmented = [RGB_1d_list[i * 3: (i + 1) * 3] for i in range(int(len(RGB_1d_list) / 3))]

RGB_list = [RGB_1d_list_segmented[i * width: (i + 1) * width] for i in range(height)]

img = PIL.Image.new(mode="RGB", size=(width, height))
im = img.load()

if colour_depth != 8:
    for i in range(len(RGB_list)):
        for j in range(len(RGB_list[0])):
            for p in range(3):
                RGB_list[i][j][p] = round(RGB_list[i][j][p] * (2 ** (8 - colour_depth)))  # Adjusts the colour data
                # to the change in colour
                # depths

for y in range(height):
    for x in range(width):
        im[x, y] = tuple(RGB_list[y][x])  # Converts the list to a tuple and saves to the pre-built image

img.show()
img.save('Output-Images/output.jpg')

# Read an image file Store metadata first - colour depth, resolution, etc. Store in variables. Then, read the image
# data. Represent it in PIL format and display. Once this is done, do the reverse to convert file types into binary.
# Try to do this without PIL, search how to read pngs for example Work on compression - two consecutive bits of the
# same colour should be represented differently. Also do lossy compression by reducing the colour depth or
# resolution, maybe. Try to make a new file store type - .abc or something.
