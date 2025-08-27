import json

from src.google_maps_parser.gmaps_data_parser import GoogleMapsDataParser
from src.google_maps_tool.service.context import GoogleMapsContext, ServiceToken
from src.google_maps_tool.mock_data import mock_get_all_lists_response, mock_get_list_response
from src.google_maps_tool.models.list import GMList
from src.google_maps_tool.models.place import GMPlace

USE_MOCK_DATA = False


class GoogleMapsService:
    def __init__(self, context: GoogleMapsContext):
        self.context = context
        self._cached_lists: list[GMList] = []

    def invalidate_cache(self) -> None:
        self._cached_lists = []

    def get_all_lists(self, use_cache=True) -> list[GMList]:
        if use_cache and self._cached_lists:
            return self._cached_lists

        url = 'https://www.google.com/locationhistory/preview/mas'
        protobuffer = {
            '2': {
                '1': f's{self.context.get_token(ServiceToken.SESSION)}',
                '7': 'e81',
                '15': 'i17409'
            },
            '7': {
                '1': 'i50'
            },
            '12': {
                '1': 'i50'
            },
            '15': {
                '1': 'i50'
            },
            '23': {
                '1': 'i50',
                '3': 'b1'
            },
            '24': {
                '1': 'i50',
                '3': 'b1'
            },
            '38': {
                '1': 'i50', '3': 'b1'
            }
        }
        payload = {'authuser': '0',
                   'hl': 'en',
                   'gl': 'ro',
                   'pb': GoogleMapsDataParser.encode(protobuffer)}

        response = None
        if USE_MOCK_DATA:
            response = mock_get_all_lists_response
        else:
            try:
                response = self.context.session.get(url, params=payload)
            except Exception as e:
                print(f"Failed to get all lists → {str(e)}")

        json_response = json.loads(response.text[4:])

        json_lists = json_response[29][3]
        lists: list[GMList] = []
        for index, json_list in enumerate(json_lists):
            lists.append(GMList.from_json(json_list, index, service=self))

        self._cached_lists = lists
        return lists

    def get_all_places(self, gmlist: GMList):
        url = 'https://www.google.com/maps/preview/entitylist/getlist'
        protobuffer = {
            '1': {
                '1': f's{gmlist.id}',
                '2': 'e1',
                '3': {
                    '1': 'e1'
                }
            },
            '2': 'e2',
            '3': 'e2',
            '4': 'i500',
            '6': {
                '1': f's{self.context.get_token(ServiceToken.SESSION)}',
                '7': 'e81',
                '28': 'e2'
            },
            '8': 'i3',
            '16': 'b1'
        }
        payload = {'authuser': '0',
                   'hl': 'en',
                   'gl': 'ro',
                   'pb': GoogleMapsDataParser.encode(protobuffer)}

        response = None
        if USE_MOCK_DATA:
            response = mock_get_list_response
        else:
            response = self.context.session.get(url, params=payload)

        json_response = json.loads(response.text[4:])

        json_places = json_response[0][8]

        places: list[GMPlace] = []

        if json_places is not None:
            for json_place in json_places:
                places.append(GMPlace.from_json(json_place, self))

        return places

    def get_place_details(self, gmplace: GMPlace) -> dict:
        url = 'https://www.google.com/maps/preview/place'

        protobuffer = gmplace.build_get_details_payload(self.context.get_token(ServiceToken.SESSION))

        payload = {'authuser': '0',
                   'hl': 'en',
                   'gl': 'ro',
                   'pb': GoogleMapsDataParser.encode(protobuffer),
                   'q': f'{gmplace.coord.lat},{gmplace.coord.long}'}

        response = self.context.session.get(url, params=payload)

        return json.loads(response.text[4:])

    def add_place_to_list(self, gmplace: GMPlace, gmlist: GMList) -> bool:
        url = 'https://www.google.com/maps/preview/entitylist/createitem'

        protobuffer = gmplace.build_add_payload(gmlist, self.context.get_token(ServiceToken.SESSION),
                                                self.context.get_token(ServiceToken.ADD_TO_LIST))

        payload = {'authuser': '0',
                   'hl': 'en',
                   'gl': 'ro',
                   'pb': GoogleMapsDataParser.encode(protobuffer)}

        if USE_MOCK_DATA:
            print(f"✅ Added {gmplace.name} to '{gmlist.name}'")
            return True
        else:
            try:
                response = self.context.session.get(url, params=payload)
                if response.ok:
                    # We invalidate the cache, since the order of the lists might have changed
                    self.invalidate_cache()
                    return True
            except Exception as e:
                print(f"Failed to add {gmplace.name} → {str(e)}")

            return False
