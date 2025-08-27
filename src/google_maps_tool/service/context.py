import json
import re
from enum import Enum

import requests


class ServiceToken(Enum):
    SESSION = 'session',
    ADD_TO_LIST = 'add_to_list'


class GoogleMapsContext:
    def __init__(self, session: requests.Session):
        self.session = session
        self.tokens: dict[ServiceToken, str] = {}

    def ensure_tokens(self):
        if not self.tokens:
            html = self.session.get("https://www.google.com/maps?hl=en&authuser=0").text
            self.tokens = get_service_tokens(html)

    def get_token(self, service: ServiceToken) -> str:
        self.ensure_tokens()
        return self.tokens[service]


def extract_app_options(html: str):
    m = re.search(r'window\.APP_OPTIONS\s*=\s*(\[.*?]]]);', html, re.S)
    if not m:
        raise RuntimeError("APP_OPTIONS not found in HTML")
    return json.loads(m.group(1))


def get_service_tokens(html: str) -> dict[ServiceToken, str]:
    app_options = extract_app_options(html)

    tokens: dict[ServiceToken, str] = {}

    try:
        tokens[ServiceToken.ADD_TO_LIST] = app_options[28][28]
        tokens[ServiceToken.SESSION] = app_options[11]
    except Exception as e:
        raise RuntimeError(f"Could not find token in APP_OPTIONS, {e}\nYour __Secure-1PSIDTS token may be expired.")

    return tokens
