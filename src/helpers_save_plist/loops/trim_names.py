from src.helpers_save_plist.utils import list_vid_names
from src.helpers_save_plist.askers.trim_names import (ask_trim_names_main_menu,
                                                      ask_length_type,
                                                      ask_length_int,
                                                      ask_length_str,
                                                      ask_trim_front_back,
                                                      ask_el_name_trim,
                                                      ask_multiple_name_trim)



def trim_names_loop(plist_numbers: list, og_names: list) -> list:
    final_names = og_names
    while True:
        print("Current names:")
        list_vid_names(plist_numbers, final_names)
        print()

        action = ask_trim_names_main_menu()
        print()

        if action == "trim_all_elements":
            trim_len = get_trim_length_loop()
            print()
            if trim_len == None:
                continue

            trim_side = ask_trim_front_back()
            print()
            if trim_side == None:
                continue
            elif trim_side == "start":
                final_names = [el[trim_len:] for el in final_names]
            elif trim_side == "end":
                final_names = [el[:-trim_len] for el in final_names]

        elif action == "trim_specific":
            trim_len = get_trim_length_loop()
            print()
            if trim_len == None:
                continue

            trim_side = ask_trim_front_back()
            print()
            if trim_side == None:
                continue

            list_vid_names(plist_numbers, final_names)
            print()

            number_to_trim = ask_el_name_trim(plist_numbers)
            print()
            if number_to_trim == None:
                continue

            i = 0
            while i<len(final_names):
                if plist_numbers[i] == number_to_trim:
                    if trim_side == "start":
                        final_names[i] = final_names[i][trim_len:]
                    elif trim_side == "end":
                        final_names[i] = final_names[i][:-trim_len]
                    break
                i += 1

        elif action == "trim_range":
            trim_len = get_trim_length_loop()
            print()
            if trim_len == None:
                continue

            trim_side = ask_trim_front_back()
            print()
            if trim_side == None:
                continue

            list_vid_names(plist_numbers, final_names)
            print()

            range_to_trim = ask_multiple_name_trim(plist_numbers)
            print()
            if range_to_trim == None:
                continue

            i = 0
            while i<len(final_names):
                if plist_numbers[i] >= range_to_trim[0]:
                    if trim_side == "start":
                        final_names[i] = final_names[i][trim_len:]
                    elif trim_side == "end":
                        final_names[i] = final_names[i][:-trim_len]
                if plist_numbers[i] == range_to_trim[1]:
                    break
                i += 1
            # START WORK HERE
            # trim in a loop

        elif action == "original_names":
            final_names = og_names

        elif action == "save":
            return final_names


def get_trim_length_loop() -> int:
    trim_len = 0
    while True:
        input_type = ask_length_type()
        print()

        if input_type == "input_integer":
            trim_len = ask_length_int()
            if trim_len == None:
                return None
            return trim_len

        elif input_type == "input_string":
            trim_len = ask_length_str()
            if trim_len == None:
                return None
            return trim_len

        elif input_type == "return":
            return None
