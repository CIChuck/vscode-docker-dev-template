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


