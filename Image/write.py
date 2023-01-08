from PIL import Image
import logging
import sys


try:
    filename = sys.argv[1]
    img = Image.open(filename)
except IndexError:
    img = Image.open('Input-Images/swan.jpg')

im = img.load()

resolution = width, height = img.size

colour_depth = 8
if colour_depth > 8:
    logging.error(' Incorrect colour depth.')
    quit()
RGB_list = [list(im[x, y]) for y in range(height) for x in range(width)]

if colour_depth != 8:
    for i in range(width * height):
        for j in range(3):
            RGB_list[i][j] = (RGB_list[i][j] // (2 ** (8 - colour_depth)))
RGB_list = [bin(RGB_list[i][j]).replace('0b', '').zfill(colour_depth) for i in range(width * height) for j in range(3)]

metadata = bin(colour_depth).replace('0b', '').zfill(4)
metadata += bin(width).replace('0b', '').zfill(16)
metadata += bin(height).replace('0b', '').zfill(16)
raw_binary = metadata + ''.join(RGB_list)
with open('Binary/output.BIN', 'w') as f:
    f.write(raw_binary)
