# Google Maps List Manager (Unofficial)

A Python CLI tool for **managing Google Maps saved places lists**.  
It lets you browse your lists, view details of places, and automatically organize items into location-based lists (e.g. move all places from list "Restaurants" that are located in Bucharest into a "Bucharest" list).

**Disclaimer:** This project uses *undocumented Google Maps APIs* that may change at any time. Use at your own risk. This project is not affiliated with or endorsed by Google.

---

## Features

- Browse all your Google Maps lists and saved places  
- Add places to lists manually or automatically (by city or radius)  
- View rich details about places (address, rating, hours, website, etc.)  
- Lazy loading of places for performance  
- Caching support (avoid repeated network calls)  
- Configurable location presets (cities, islands, etc.) via `locations.json`  
- Mock data mode for development without hitting the real API  

---

## Installation

```bash
git clone https://github.com/rvictorr/google-maps-list-manager.git
cd google-maps-list-manager
pip install -r requirements.txt
```

## Authentication (cookies.json)

This tool authenticates with your Google Maps cookies.
The file `cookies.json` lists the necessary cookies.

1. Open Google Maps in Chrome or Firefox.
2. Log in with your Google account.
3. Open DevTools → Application → Storage → Cookies.
4. Export cookies for google.com.
5. Add them to the `cookies.json` file


Required cookies include:
SID, SAPISID, APISID, HSID, SSID,
__Secure-1PSID, __Secure-1PAPISID, __Secure-1PSIDTS.

The cookie __Secure-1PSIDTS is short-lived and tends to expire quickly. If you see auth errors, refresh __Secure-1PSIDTS.

## Location Presets (locations.json)

The tool can automatically filter places by city or region, using coordinates and a radius.
These presets are stored in locations.json in the root directory.

Example locations.json:

```json
{
  "bucharest": { "lat": 44.4268, "lon": 26.1025, "radius_km": 10 },
  "corfu":     { "lat": 39.6243, "lon": 19.9217, "radius_km": 20 },
  "crete":     { "lat": 35.2401, "lon": 24.8093, "radius_km": 50 }
}
```


## Usage

Run the app:

```bash
python main.py
```

Example main menu:

```
=== Google Maps Saved Places manager ===

1. View lists & saved places
2. Add place manually
3. Add places automatically
0. Exit
```

## Development Notes

- Mock data: toggle `USE_MOCK_DATA = True` to develop without network calls.

- Lazy loading: lists and places are only fetched when needed.

- Caching: once loaded, lists can be reused without repeat API calls.

## Disclaimer

This project is for educational purposes only.

Respect Google’s Terms of Service.

Endpoints and tokens used here are undocumented and may break without notice.

## License

MIT License. See [LICENSE](LICENSE) for details.