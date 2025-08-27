from __future__ import annotations

import requests
import sys

from src.google_maps_tool.config.config import load_cookies
from src.google_maps_tool.service.context import GoogleMapsContext
from src.google_maps_tool.ui.menu import main_menu
from src.google_maps_tool.service.maps_service import GoogleMapsService

if __name__ == '__main__':
    current_session = requests.Session()
    current_session.cookies = load_cookies("cookies.json")
    current_session.headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ro-RO;q=0.6,ro;q=0.5,en-US;q=0.4",
        "priority": "u=1, i",
        "x-maps-diversion-context-bin": "CAE=",
        "Referer": "https://www.google.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    }

    context = GoogleMapsContext(current_session)
    service = GoogleMapsService(context)
    try:
        main_menu(service)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
