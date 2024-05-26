import numpy as np

class City:
    def __init__(self, name, coordinates, is_start=False):
        self.name = name
        self.coordinates = coordinates
        self.is_start = is_start