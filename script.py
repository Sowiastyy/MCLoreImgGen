import json
from PIL import Image
import numpy as np
import pyperclip as pc
def get_color(pixel):
    if len(pixel) == 4 and pixel[3] == 0:  # Check for transparency
        return '#0'  # Return a space if pixel is transparent
    return "#{:02x}{:02x}{:02x}".format(*pixel)

def convert_image_to_commands(image_file, output_file):
    image = Image.open(image_file)
    pixel_data = np.array(image)
    
    #command = '/give @p stone{display:{Lore:['
    command = '''Lore:['''
    for row in pixel_data:
        command+=''''{"extra":['''
        previous_color = None
        count = 0
        for i, pixel in enumerate(row):
            color = get_color(pixel)
            if color == previous_color:
                count += 1
            else:
                if previous_color is not None:
                    if i == count:  # first pixel in row
                        command += '{"text":"' + "█" * count + '","color":"' + previous_color + '"},'
                    else:
                        command += '{"text":"' + "█" * count + '","color":"' + previous_color + '"},'
                previous_color = color
                count = 1
        if count > 0:
            if len(row) == count:  # first and only pixel in row
                command += '{"text":"' + "█" * count + '","color":"' + previous_color + '"},'
            else:
                command += '{"text":"' + "█" * count + '","color":"' + previous_color + '"},'
        command = command[:-1]
        command+='''],"text":""}','''
    command = command[:-1]
    command += ''']'''

    pc.copy(command)
    print(len(command))
    #print(command)

convert_image_to_commands('input_img.png', 'output.txt')