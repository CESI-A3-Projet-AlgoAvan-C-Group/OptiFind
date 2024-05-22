import geojson
import json

# This class will be used to represent the delivery points
class DeliveryPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def __geo_interface__(self):
        return {
            "type": "Point",
            "coordinates": (self.x, self.y)
        }
    
    def __str__(self):
        return f"DeliveryPoint: {self.__geo_interface__}"
    
    def __repr__(self):
        return self.__str__()