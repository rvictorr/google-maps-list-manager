import base64
from dataclasses import dataclass

from src.google_maps_tool.helpers import maybe, to_uint64
from src.google_maps_tool.models.coord import GMCoord


@dataclass
class GMPlaceDetails:
    short_name: str
    _full_address: tuple[str, str, str]
    avg_price: str
    avg_rating: float
    review_count: int
    website: str
    category: str
    _saved_in_lists: list
    _open_hours: list
    phone_number: str
    plus_code: str

    @classmethod
    def from_json(cls, json_data: dict) -> 'GMPlaceDetails':
        return cls(
            short_name=maybe(json_data, 6, 11),
            _full_address=maybe(json_data, 6, 2),
            avg_price=maybe(json_data, 6, 4, 2),
            avg_rating=maybe(json_data, 6, 4, 7),
            review_count=maybe(json_data, 6, 4, 8),
            website=maybe(json_data, 6, 7, 1),
            category=maybe(json_data, 6, 13, 0),
            _saved_in_lists=maybe(json_data, 6, 25, 15),
            _open_hours=maybe(json_data, 6, 34, 1),
            phone_number=maybe(json_data, 6, 178, 0, 0),
            plus_code=maybe(json_data, 6, 183, 2, 2, 0)
        )

    @property
    def full_address(self) -> str:
        if not self._full_address or not any(self._full_address):
            return ''

        return ', '.join([p for p in self._full_address if p])

    @property
    def saved_in_lists(self) -> str:
        if not self._saved_in_lists or not any(self._saved_in_lists):
            return ''

        return ', '.join([p[0][1] for p in self._saved_in_lists if p])

    @property
    def open_hours(self) -> list[str]:
        if not self._open_hours or not any(self._open_hours):
            return []

        return [f'{p[0]}: {', '.join(p[1])}' for p in self._open_hours if p]


class GMPlace:
    def __init__(self, name, lat, long, secret_1, secret_2, service: 'GoogleMapsService'):
        self.name = name
        self.coord = GMCoord(lat, long)
        self.secret_1 = secret_1
        self.secret_2 = secret_2
        self._service = service
        self._details: GMPlaceDetails | None = None

    @classmethod
    def from_json(cls, json_data: dict, service: 'GoogleMapsService') -> 'GMPlace':
        name = json_data[2]
        lat = json_data[1][5][2]
        long = json_data[1][5][3]
        secret_1 = None
        secret_2 = None

        if json_data[8][1] is not None:
            # For places without a name (only coords)
            secret_1 = int(json_data[8][1][0])
            secret_2 = int(json_data[8][1][1])

        return cls(name, lat, long, secret_1, secret_2, service)

    @property
    def details(self) -> GMPlaceDetails:
        if self._details is None:
            self.load_details()
        return self._details

    @property
    def is_coords_only(self) -> bool:
        return not (self.secret_1 and self.secret_2)

    def load_details(self) -> None:
        place_details_json = self._service.get_place_details(self)
        self._details = GMPlaceDetails.from_json(place_details_json)

    def build_get_details_payload(self, session_id) -> dict:
        base: dict = {
            '1': {
                '4': {
                    '3': f'd{self.coord.lat}',
                    '4': f'd{self.coord.long}'}
            },
            '12': {
                '2': {
                    '1': 'i360',
                    '2': 'i120',
                    '4': 'i8'
                }
            },
            '13': {
                '2': {
                    '1': 'i203',
                    '2': 'i100'
                },
                '3': {
                    '2': 'i4',
                    '5': 'b1'
                },
                '6': {
                    '1': {
                        '1': 'i86',
                        '2': 'i86'
                    },
                    '1_1': {
                        '1': 'i408',
                        '2': 'i240'
                    }
                },
                '7': {
                    '1': {'1': 'e1', '2': 'b0', '3': 'e3'},
                    '1_1': {'1': 'e2', '2': 'b1', '3': 'e2'},
                    '1_2': {'1': 'e2', '2': 'b0', '3': 'e3'},
                    '1_3': {'1': 'e8', '2': 'b0', '3': 'e3'},
                    '1_4': {'1': 'e10', '2': 'b0', '3': 'e3'},
                    '1_5': {'1': 'e10', '2': 'b1', '3': 'e2'},
                    '1_6': {'1': 'e10', '2': 'b0', '3': 'e4'},
                    '1_7': {'1': 'e9', '2': 'b1', '3': 'e2'},
                    '2': 'b1'
                },
                '9': 'b0',
                '15': {
                    '1': {
                        '1': {
                            '1': {'1': 'e2'}
                        },
                        '2': {'1': 'i195', '2': 'i195'},
                        '3': 'i20'
                    }
                }
            },
            '14': {
                '1': f's{session_id}', '7': 'e81'
            },
            '15': {
                '1': {
                    '4': 'e2',
                    '13': {
                        '2': 'b1',
                        '3': 'b1',
                        '4': 'b1',
                        '6': 'i1',
                        '8': 'b1',
                        '9': 'b1',
                        '14': 'b1',
                        '20': 'b1',
                        '25': 'b1'
                    },
                    '18': {
                        '3': 'b1',
                        '4': 'b1',
                        '5': 'b1',
                        '6': 'b1',
                        '9': 'b1',
                        '12': 'b1',
                        '13': 'b1',
                        '14': 'b1',
                        '17': 'b1',
                        '20': 'b1',
                        '21': 'b1',
                        '22': 'b1',
                        '25': 'b1',
                        '27': {'1': 'b0'},
                        '28': 'b0',
                        '30': 'b1',
                        '32': 'b1',
                        '33': {'1': 'b1'},
                        '34': 'b1',
                        '36': 'e2'
                    }
                },
                '10': {'8': 'e3'},
                '11': {'3': 'e1'},
                '14': {'3': 'b0'},
                '17': 'b1',
                '20': {'1': 'e3', '1_1': 'e6'},
                '24': 'b1',
                '25': 'b1',
                '26': 'b1',
                '27': 'b1',
                '29': 'b1',
                '30': {'2': 'b1'},
                '36': 'b1',
                '37': 'b1',
                '39': {
                    '2': {'2': 'i1', '3': 'i1'}
                },
                '43': 'b1',
                '52': 'b1',
                '54': {'1': 'b1'},
                '55': 'b1',
                '56': {'1': 'b1'},
                '61': {
                    '1': {'1': 'e1'}
                },
                '65': {
                    '3': {
                        '1': {
                            '1': {'1': 'i224', '2': 'i298'}
                        }
                    }
                },
                '72': {
                    '1': {
                        '2': 'b1',
                        '5': 'b1',
                        '7': 'b1',
                        '12': {
                            '1': 'b1',
                            '2': 'b1',
                            '4': {'1': 'e1'}
                        }
                    },
                    '4': 'b1',
                    '8': {
                        '1': {
                            '4': {'1': 'e1'},
                            '4_1': {'1': 'e3'},
                            '4_2': {'1': 'e4'}
                        },
                        '3': 'sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts',
                        '6': {'1': 'e1'}
                    },
                    '9': 'b1'
                },
                '89': 'b1',
                '98': {'1': 'b1', '2': 'b1', '3': 'b1'},
                '103': 'b1',
                '113': 'b1',
                '114': {
                    '1': 'b1', '2': {
                        '1': 'b1'
                    }
                },
                '117': 'b1',
                '122': {'1': 'b1'},
                '125': 'b0',
                '126': 'b1',
                '127': 'b1'
            },
            '21': {},
            '22': {'1': 'e81'},
            '29': {},
            '30': {'3': 'b1', '6': {'2': 'b1'}, '7': {'2': 'b1'}, '9': 'b1'},
            '34': {'7': 'b1', '10': 'b1', '14': 'b1', '15': {'1': 'b0'}},
            '39': f's{self.name.replace(' ', '+')}'
        }

        payload: dict = base

        if not self.is_coords_only:
            payload['1'] = {
                '1': f's{hex(to_uint64(self.secret_1))}:{hex(to_uint64(self.secret_2))}',
                '4': {
                    '3': f'd{self.coord.lat}',
                    '4': f'd{self.coord.long}'}
            }
            payload['12']['2']['1'] = 'i360'
        else:
            payload['1'] = {
                '4': {
                    '3': f'd{self.coord.lat}',
                    '4': f'd{self.coord.long}'}
            }
            payload['12']['2']['1'] = 'i272'

        return payload

    def build_add_payload(self, gmlist: 'GMList', session_id: str, service_token: str) -> dict:
        base: dict = {
            '1': {
                '1': f's{gmlist.id}',
                '2': 'e1',
                '3': {
                    '1': 'e1'
                }
            },
            '2': {
                '2': {
                    '6': {
                        '3': f'd{self.coord.lat}',
                        '4': f'd{self.coord.long}'
                    }
                },
                '9': {
                    '1': {
                        '1': 'e1'
                    },
                }
            },
            '3': {
                '1': f's{session_id}:34',
                '2': f's1i:{gmlist.index + 1},t:{gmlist.type.value},e:{gmlist.index},p:{session_id}:34',
                '4': {
                    '2': f'i{gmlist.type.value}'
                },
                '7': 'e81',
                '28': 'e2'},
            '4': f's{service_token}'
        }

        payload: dict = base

        if not self.is_coords_only:
            payload['2']['2']['7'] = {
                '1': f'y{str(to_uint64(self.secret_1))}',
                '2': f'y{str(to_uint64(self.secret_2))}'
            }
            payload['2']['3'] = f's{self.name}'
            payload['2']['9']['2'] = {
                '1': f'y{str(to_uint64(self.secret_1))}',
                '2': f'y{str(to_uint64(self.secret_2))}'
            }
        else:
            def encode_name(name: str) -> str:
                # Convert to UTF-8 bytes
                utf8_bytes = name.encode('utf-8')
                # URL-safe Base64 encode (no padding)
                encoded = base64.urlsafe_b64encode(utf8_bytes).rstrip(b'=')
                # Return as string
                return encoded.decode('ascii')

            payload['2']['3'] = f'z{encode_name(self.details.short_name)}'
            payload['2']['9']['3'] = {
                '3': f'd{self.coord.lat}',
                '4': f'd{self.coord.long}'
            }

        return payload

    def __repr__(self):
        return f'[GMPlace] {str(self)}'

    def __str__(self):
        return f'name: {self.name}, coords: {self.coord}, secret_1: {self.secret_1}, secret_2: {self.secret_2}'

    def __eq__(self, other):
        return (self.name == other.name
                and self.coord == other.coord
                and self.secret_1 == other.secret_1
                and self.secret_2 == other.secret_2)
