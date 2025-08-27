from enum import Enum

from src.google_maps_tool.models.place import GMPlace


class GMListType(Enum):
    OTHER = 39790
    FAVORITE_PLACES = 39791,
    STARRED_PLACES = 39792,
    WANT_TO_GO = 39793,
    SAVED_PLACES = 39788,
    TRAVEL_PLANS = 131033,


class GMList:
    def __init__(self, id: str, name: str, places_count: int, index: int, service: 'GoogleMapsService'):
        self.id = id
        self.name = name
        self.index = index
        self.places_count = places_count
        self.type = self._get_list_type()
        self._places: list[GMPlace] | None = None
        self._service = service

    @classmethod
    def from_json(cls, json_data: dict, index: int, service: 'GoogleMapsService') -> 'GMList':
        id = json_data[0][0]
        name = json_data[4]
        places_count = json_data[12]

        return cls(id, name, places_count, index, service)

    @property
    def places(self) -> list[GMPlace]:
        if self._places is None:
            self.refresh()
        return self._places

    def refresh(self):
        """Force reload from service."""
        self._places = self._service.get_all_places(self)

    def filter_by_radius(self, center_lat, center_lon, radius_km) -> list[GMPlace]:
        """Return a list of GMPlace within radius_km of (center_lat, center_lon)."""
        return [
            place for place in self.places
            if place.coord.distance_to(center_lat, center_lon) <= radius_km
        ]

    def _get_list_type(self) -> GMListType:
        match self.name:
            case 'Favorite places':
                return GMListType.FAVORITE_PLACES
            case 'Want to go':
                return GMListType.WANT_TO_GO
            case 'Saved places':
                return GMListType.SAVED_PLACES
            case 'Travel plans':
                return GMListType.TRAVEL_PLANS
            case _:
                return GMListType.OTHER

    def __repr__(self):
        return f'[GMList] {str(self)}'

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, index: {self.index}, places: \n{str(self.places)}'
