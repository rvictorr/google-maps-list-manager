import re


# Based on https://github.com/richardDobron/google-maps-data-parameter-parser


class GoogleMapsDataParser:
    def __init__(self):
        pass

    @staticmethod
    def decode(protocol_buffer: str) -> dict:
        messages = [t for t in protocol_buffer.split('!') if t]
        return GoogleMapsDataParser.parse(messages)

    @staticmethod
    def encode(messages: dict) -> str:
        return '!' + GoogleMapsDataParser._encode_impl(messages)

    @staticmethod
    def parse(messages: list) -> dict:
        count = len(messages)
        result = {}

        i = 0
        duplicate_index = 1

        while i < count:
            message = messages[i]
            if matches := re.search(r'^(\d+)m(\d+)', message):
                key = matches.group(1)
                length = int(matches.group(2))

                parsed = GoogleMapsDataParser.parse(messages[i + 1: i + 1 + length])

                if key in result:
                    result[f'{key}_{duplicate_index}'] = parsed
                    duplicate_index += 1
                else:
                    result[key] = parsed

                i += length
            elif matches := re.search(r'^(\d+)([bdefisuvxyz])(.*)$', message):
                key = matches.group(1)
                type = matches.group(2)
                value = matches.group(3)

                computed = type + value

                if key in result:
                    result[f'{key}_{duplicate_index}'] = computed
                    duplicate_index += 1
                else:
                    result[key] = computed
            else:
                raise Exception(f'Unknown param format: {message}')
            i += 1
        return result

    @staticmethod
    def count_elements(elements: dict, initial: int = 0) -> int:
        for value in elements.values():
            if isinstance(value, dict):
                if is_list(value):
                    initial += GoogleMapsDataParser.count_elements(value)
                else:
                    initial += GoogleMapsDataParser.count_elements(value, 1)
            else:
                initial += 1

        return initial

    @staticmethod
    def _encode_impl(messages: dict, real_key: int = None) -> str:
        def transform(key, message):
            if matches := re.match(r'^(\d+)_(\d+)', key):
                # Allow duplicate keys in encoded message
                key = matches.group(1)

            if isinstance(message, dict):
                if is_list(message):
                    return GoogleMapsDataParser._encode_impl(message, key)

                result = str(real_key or key) + 'm' + str(
                    GoogleMapsDataParser.count_elements(message))

                # Message could be empty
                if message:
                    result += '!' + GoogleMapsDataParser._encode_impl(message)

                return result

            return (real_key or key) + message

        segments = {key: transform(key, message)
                    for (key, message) in messages.items()}

        return '!'.join(segments.values())


def is_list(elements: dict) -> bool:
    if len(elements) == 0:
        return False
    return list(elements.keys()) == range(len(elements))
