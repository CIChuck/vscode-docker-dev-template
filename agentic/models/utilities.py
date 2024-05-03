import random

class LoremIpsumGenerator:
    def __init__(self):
        self.text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                     "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                     "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
                     "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
                     "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
                     "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
                     "culpa qui officia deserunt mollit anim id est laborum.")

    def generate(self, low=None, high=None):
        if low is None or high is None:
            # Generate a random length between 1 and the length of the text
            length = random.randint(1, len(self.text))
        else:
            # Ensure the specified range is within the bounds of the text length
            low = max(1, low)  # Prevent a low value less than 1
            high = min(len(self.text), high)  # Prevent a high value greater than the text length
            length = random.randint(low, high)

        if length <= len(self.text):
            return self.text[:length]
        else:
            # If the requested length is greater than the available text,
            # this will repeat the text until the length is met.
            repeated_text = self.text * (length // len(self.text) + 1)
            return repeated_text[:length]


import datetime
def time_stamp():
    current_date_and_time = datetime.datetime.now()
    # print(current_date_and_time)
    formatted_date_and_time = current_date_and_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"Current date and time:{formatted_date_and_time}"

import base64
from PIL import Image
import io

# Example usage (This will only work if you have a valid image path)
# try:
#     encoded_image = encode_image_to_base64('path_to_your_image.jpg')
#     print(encoded_image)
# except Exception as error:
#     print(f"An error occurred: {error}")

def encode_image_to_base64(image_filename):
    # Assert the filename ends with one of the accepted extensions
    assert image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')), "File format must be JPEG, GIF, or PNG"

    try:
        # Open the image file
        with Image.open(image_filename) as img:
            # Assert that the image is successfully loaded (not None)
            assert img is not None, "Image file could not be loaded"

            # Create a buffer to hold image bytes
            buffered = io.BytesIO()
            # Get the file format (JPEG, GIF, PNG) and assert it's valid
            img_format = img.format
            assert img_format in ['JPEG', 'GIF', 'PNG'], "Image format not recognized"

            # Save image to the buffer in its original format
            img.save(buffered, format=img_format)
            # Encode the buffer to Base64
            img_base64 = base64.b64encode(buffered.getvalue())
            # Decode and return the Base64 encoded string
            base64_string = img_base64.decode('utf-8')
            # Assert the result is a non-empty string
            assert base64_string, "Base64 string conversion failed"
            return base64_string
    except IOError:
        # Handle exceptions raised by PIL when it cannot open the image
        raise IOError("Failed to load the image. The file may be corrupted or the path is incorrect.")
    except Exception as e:
        # Handle other unforeseen exceptions during the image processing
        raise Exception(f"An error occurred while processing the image: {str(e)}")

# Example usage (This will only work if you have a valid image path)
# try:
#     encoded_image = encode_image_to_base64('path_to_your_image.jpg')
#     print(encoded_image)
# except Exception as error:
#     print(f"An error occurred: {error}")

from IPython.display import Markdown, display

def pretty_print(text, color, fontsize):
    d = f"""{fontsize} <p> <span style="color:{color}"><em>{text}</em></span></p>"""
    display(Markdown(d))

