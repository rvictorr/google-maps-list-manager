import os
from math import radians, sin, cos, sqrt, atan2


# --- Distance helper (Haversine) ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def to_uint64(i) -> int:
    return i & 0xFFFFFFFFFFFFFFFF


def decimal_to_dms(lat, lon):
    def to_dms(value, is_lat=True):
        degrees = int(abs(value))
        minutes = int((abs(value) - degrees) * 60)
        seconds = (abs(value) - degrees - minutes / 60) * 3600
        direction = ''
        if is_lat:
            direction = 'N' if value >= 0 else 'S'
        else:
            direction = 'E' if value >= 0 else 'W'
        return f"{degrees}°{minutes}'{seconds:.1f}\"{direction}"

    return f"{to_dms(lat, True)} {to_dms(lon, False)}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def maybe(data, *keys):
    try:
        for k in keys:
            data = data[k]
    except (IndexError, TypeError, KeyError):
        return None
    return data
