import geojson
import json

# This class will be used to represent the route to be followed by the delivery person
class Route:
    def __init__(self, points):
        self.points = points
    
    @property
    def __geo_interface__(self):
        return {
            "type": "LineString",
            "coordinates": [(point.x, point.y) for point in self.points]
        }
    
    def __str__(self):
        return f"Route: {self.__geo_interface__}"
    
    def __repr__(self):
        return self.__str__()