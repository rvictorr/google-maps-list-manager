from src.google_maps_tool.models.list import GMList
from src.google_maps_tool.models.place import GMPlace


def print_all_lists(gmlists: list[GMList]) -> None:
    names = map(lambda x: x[4], gmlists)
    print(list(names))


def print_lists_for_user(gmlists: list[GMList]):
    for i, gmlist in enumerate(gmlists, start=1):
        print(f'{i}. {gmlist.name} ({gmlist.places_count} places)')


def print_places_for_user(gmplaces: list[GMPlace]):
    for i, gmplace in enumerate(gmplaces, start=1):
        print(f'{i}. {gmplace.name} @ {gmplace.coord}')


def print_places_single_line(gmplaces: list[GMPlace]):
    gmplaces = map(lambda x: x.name, gmplaces)
    print(','.join(gmplaces))


def print_place_details(gmplace: GMPlace) -> None:
    print(f"=== {gmplace.name or gmplace.details.short_name or 'Unnamed place'} ===\n")

    def line(label: str, value) -> None:
        if value not in (None, "", [], ()):
            print(f"{label:<15}: {value}")

    # Address
    line("Address", gmplace.details.full_address)

    # Core info
    line("Category", gmplace.details.category)
    line("Avg Rating", f"{gmplace.details.avg_rating:.1f}/5 ({gmplace.details.review_count} reviews)"
    if gmplace.details.avg_rating else None)
    line("Avg Price", gmplace.details.avg_price)

    # Contact & web
    line("Phone", gmplace.details.phone_number)
    line("Website", gmplace.details.website)

    # Location info
    line("Coordinates", gmplace.coord)
    line("Plus Code", gmplace.details.plus_code)

    # Lists & hours
    if gmplace.details.saved_in_lists:
        line("Saved In", gmplace.details.saved_in_lists)
    if gmplace.details.open_hours:
        print("\nOpening Hours:")
        for h in gmplace.details.open_hours:
            print(f"  - {h}")


def handle_user_choice(prompt: str, max: int, allow_back: bool = False) -> int:
    min = -1 if allow_back is True else 0

    while True:
        try:
            choice = input(prompt)
            choice_int = int(choice) - 1

            if min <= choice_int < max:
                # Valid choice.
                break
        except ValueError:
            pass

        print(f'\nError: Please choose a number between 1 and {max}!')

    return choice_int
