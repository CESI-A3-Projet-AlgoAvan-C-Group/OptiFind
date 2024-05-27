import numpy as np

class Delivery:
    def __init__(self, name, coordinates, is_start=False):
        self.name = name
        self.coordinates = coordinates
        self.is_start = is_start