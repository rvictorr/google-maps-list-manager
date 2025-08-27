import math

from src.google_maps_tool.helpers import decimal_to_dms


class GMCoord:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def distance_to(self, lat: float, long: float) -> float:
        """
        Calculate distance in km between this coordinate and another (lat, lon).
        Uses the haversine formula.
        """
        R = 6371.0  # Earth radius in km

        lat1, lon1 = math.radians(self.lat), math.radians(self.long)
        lat2, lon2 = math.radians(lat), math.radians(long)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def __repr__(self):
        return f'[GMCoord] {str(self)}'

    def __str__(self):
        return decimal_to_dms(self.lat, self.long)

    def __eq__(self, other):
        if not isinstance(other, GMCoord):
            return False

        return (round(self.lat, 3) == round(other.lat, 3) and
                round(self.long, 3) == round(other.long, 3))

    def __hash__(self):
        return hash((round(self.lat, 3), round(self.long, 3)))
