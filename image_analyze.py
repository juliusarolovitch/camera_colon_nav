# Julius Arolovitch, for CMU Biorobotics
# Conversion of low-resolution digital intracolonic image into set of steering directions for MedSnake/HARP

from PIL import Image
from math import *
import numpy
import time

# Load the image
image_pil = Image.open('new_colon.png')

# Load individual pixels
pixels = image_pil.load()

# Get image dimensions
width, height = image_pil.size

# Initialize array of red values from RGB of every pixel in image
red_array = []

# Fetch all red values for every pixel, and append to red_array
for x in range(0, width):
    for y in range(0, height):
        red_array.append(pixels[x, y][0])

# Calculate average red value for image
avg_red = sum(red_array)/len(red_array)

# Initilize field of view consideration, an ellipse of diameters length and width of image


def ellipse_calculate_y(width, height, current_x):
    y = sqrt((1-((current_x-.5*width)/(.5*width))**2)*(.5*height)**2)+.5*height
    return int(y), int(height-y)


# Initilize arrays of x and y coordinates of pixels darker than average
passing_x = []
passing_y = []

# Calculate positions of x and y coordinates of pixels darker than average, change them to green
decimal_saturation_guess = 0
percent_saturation = 0

while percent_saturation < 15:
    for i in range(0, width):
        upper_bound, lower_bound = ellipse_calculate_y(width, height, i)
        for j in range(lower_bound, upper_bound):
            if pixels[i, j][0] < decimal_saturation_guess*avg_red:
                passing_x.append(i)
                passing_y.append(j)
                pixels[i, j] = (0, 255, 0)
    percent_saturation = len(passing_x)*100/(width*height)
    decimal_saturation_guess += .03
    print(percent_saturation)
    print(decimal_saturation_guess)

# Calculate average passing x and y coordinate
avg_passing_x = sum(passing_x)/len(passing_x)
avg_passing_y = sum(passing_y)/len(passing_y)

# Mark passing cordinate with blue pixel

for k in range(0, 20):
    for z in range(0, 20):
        x_coord = (round(avg_passing_x)-10+k)
        y_coord = (round(avg_passing_y)-10+z)
        pixels[x_coord, y_coord] = (0, 0, 255)


# Show image
image_pil.show()

# Diameter of camera view, link length
image_diameter = 6
link_length = 2

# # Distance between steering point and centerline
# pixel_distance = sqrt((round(avg_passing_x)-(width/2)) ^
#                       2 + (round(avg_passing_y)-(height/2)) ^ 2)
# real_distance = pixel_distance*image_diameter/height

# phi = numpy.arctan2(real_distance/link_length)
