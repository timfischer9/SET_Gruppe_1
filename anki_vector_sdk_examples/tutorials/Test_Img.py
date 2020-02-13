#!/usr/bin/env python
# coding: utf-8

import time
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps


try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

with anki_vector.Robot() as robot:
    # Load an image
    image_file = Image.open('/home/kevin/Downloads/IMG-20200213-WA0001.jpg')

    # Convert the image to the format used by the Screen
    screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
    robot.screen.set_screen_with_image_data(screen_data, 4.0)
