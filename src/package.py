from math import radians, sin, cos, sqrt, atan2

class Package:
    def __init__(self, package_id, weight, volume, latitude, longitude, city, package_type):
        self.id = package_id
        self.weight = weight
        self.volume = volume
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.type = package_type

    def calculate_distance(self, reference_position):
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(reference_position[0])
        lon2 = radians(reference_position[1])

        R = 6371.0

        dlat = abs(lat2 - lat1)
        dlon = abs(lon2 - lon1)

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance