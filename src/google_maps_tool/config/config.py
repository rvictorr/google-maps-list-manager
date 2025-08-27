import json

from requests.cookies import RequestsCookieJar


def load_location_presets(filename="locations.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_cookies(filename="cookies.json") -> RequestsCookieJar:
    """Load cookies from a simple {name: value} JSON into Requests session."""
    with open(filename, "r", encoding="utf-8") as f:
        cookie_dict = json.load(f)

    jar = RequestsCookieJar()
    for name, value in cookie_dict.items():
        jar.set(name, value, domain=".google.com", path="/")

    return jar
