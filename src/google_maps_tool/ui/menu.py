import sys
import time
from typing import Callable

from src.google_maps_tool import helpers
from src.google_maps_tool.config.config import load_location_presets
from src.google_maps_tool.models.list import GMList
from src.google_maps_tool.models.place import GMPlace
from src.google_maps_tool.service.maps_service import GoogleMapsService
from src.google_maps_tool.ui import ui

location_presets = load_location_presets()


def main_menu(service: GoogleMapsService):
    while True:
        helpers.clear_screen()
        print('\n====== Google Maps Saved Places manager ======\n')
        print('1. View my lists & saved places')
        print('2. Add places manually')
        print('3. Add places inside a specified radius automatically')
        print('0. Exit')

        choice = input("> ").strip()

        if choice == '1':
            view_lists_menu(service)
        if choice == '2':
            add_manually_menu(service)
        elif choice == '3':
            add_automatically_menu(service)
        elif choice == '0':
            break
        else:
            print('Invalid choice.')


def view_lists_menu(service: GoogleMapsService):
    def show_places(gmlist: GMList) -> None:
        def show_place_details(gmplace: GMPlace) -> None:
            helpers.clear_screen()

            ui.print_place_details(gmplace)
            input('\nPress Enter to return...')

        places_menu(gmlist, show_place_details)

    lists_menu(service, show_places)


def add_manually_menu(service: GoogleMapsService):
    def select_place(gmplace: GMPlace) -> None:
        def select_destination_list(destination_gmlist: GMList) -> None:
            service.add_place_to_list(gmplace, destination_gmlist)

            helpers.clear_screen()
            print(f'\nDone! Destination list `{destination_gmlist.name}` is now: \n')
            ui.print_places_for_user(destination_gmlist.places)
            input('\nPress Enter to return...')

        # 3. Print destination lists
        print(f'\nPlease choose a destination list for {gmplace.name}:')

        lists_menu(service, select_destination_list)

    def show_places(gmlist: GMList) -> None:
        places_menu(gmlist, select_place)

    lists_menu(service, show_places)


def add_automatically_menu(service: GoogleMapsService, debug=False):
    while True:
        helpers.clear_screen()
        print("\n--- Automatic Add ---")

        # 1) Get and print all lists
        lists = service.get_all_lists()
        print('Lists of saved places:\n')
        ui.print_lists_for_user(lists)
        print('0. Back')

        # 2) Choose source list
        src_idx = ui.handle_user_choice('\nChoose the SOURCE list: ', len(lists), allow_back=True)
        if src_idx == -1:
            return

        src_list = lists[src_idx]
        print(f'Chosen SOURCE list: `{src_list.name}`')
        dst_idx = ui.handle_user_choice('\nChoose the DESTINATION list: ', len(lists), allow_back=True)
        if dst_idx == -1:
            return

        dst_list = lists[dst_idx]
        print(f'Chosen DESTINATION list: `{dst_list.name}`')

        # 3) Location preset or custom coords
        use_location = input("\nUse a preset location? (y/N): ").strip().lower() == 'y'
        if use_location:
            locations = list(location_presets.keys())
            print('\nPresets:')
            for i, c in enumerate(locations):
                print(f"{i + 1}. {c}")

            location_idx = ui.handle_user_choice('\nChoose location preset: ', len(locations))
            location = location_presets[locations[location_idx]]
            center_lat, center_lon, radius_km = location["lat"], location["lon"], location["radius_km"]

            override = input(f'Default radius {radius_km} km. Override? (empty to keep): ')
            if override.strip():
                radius_km = float(override)
        else:
            center_lat = float(input('Enter center latitude: '))
            center_lon = float(input('Enter center longitude: '))
            radius_km = float(input('Enter radius (km): '))

        src_list.refresh()
        dst_list.refresh()
        # 4) Filter and add
        inside = src_list.filter_by_radius(center_lat, center_lon, radius_km)
        places_to_add = [place for place in inside if place not in dst_list.places]

        print(f"\nFound {len(places_to_add)} places within {radius_km} km.")
        ui.print_places_single_line(places_to_add)

        if input('Proceed? (y/N): ').lower() != 'y':
            print('Aborted.')
            return

        dst_list_len_before = len(dst_list.places)

        bar_length = 30  # length of the progress bar in characters

        for idx, p in enumerate(places_to_add):
            service.add_place_to_list(p, dst_list)
            time.sleep(0.25)

            progress = idx / len(places_to_add)
            filled_length = int(bar_length * progress)
            bar = '#' * filled_length + '-' * (bar_length - filled_length)

            # Print progress bar on the same line
            print(f"\r[{bar}] {idx}/{len(places_to_add)} done", end="")
            sys.stdout.flush()  # make sure it shows immediately

            if debug:
                updated_places = service.get_all_places(dst_list)
                print(f'len(updated_places): {len(updated_places)}, dst_list_len_before: {dst_list_len_before}')
                if idx + 1 != len(updated_places) - dst_list_len_before:
                    print(f'Failed to add {p} to list. Aborting.')
                    break

        dst_list.refresh()
        helpers.clear_screen()
        print(f'\nDone! Destination list `{dst_list.name}` is now: \n')
        ui.print_places_for_user(dst_list.places)
        if len(dst_list.places) != (dst_list_len_before + len(places_to_add)):
            places_not_added = [place for place in places_to_add if place not in dst_list.places]
            print('An error occurred while adding places. The following places were not added:')
            print(', '.join([place.name for place in places_not_added]))
            # print(f'dst_list: {dst_list.places}')
            # print(f'places_to_add: {places_to_add}')

        input('\nPress Enter to return...')


def lists_menu(service: GoogleMapsService, on_select: Callable[[GMList], None] = None):
    while True:
        helpers.clear_screen()
        print('\n--- Your lists ---')

        gmlists = service.get_all_lists()
        ui.print_lists_for_user(gmlists)
        print('0. Back')

        choice_list_idx = ui.handle_user_choice('> '.strip(), len(gmlists), allow_back=True)

        if choice_list_idx == -1:
            return

        chosen_gmlist = gmlists[choice_list_idx]

        if on_select:
            on_select(chosen_gmlist)
            return


def places_menu(gmlist: GMList, on_select: Callable[[GMPlace], None] = None) -> None:
    while True:
        helpers.clear_screen()
        print(f'List `{gmlist.name}`: \n')
        ui.print_places_for_user(gmlist.places)
        print('0. Back')

        choice_place_idx = ui.handle_user_choice('> '.strip(), len(gmlist.places), allow_back=True)

        if choice_place_idx == -1:
            return

        if on_select:
            on_select(gmlist.places[choice_place_idx])
            return
