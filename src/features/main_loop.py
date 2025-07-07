from src.common.askers import ask_url
from src.common.utils import determine_url_type
from .save_single import save_single
from .save_plist import save_plist



def main_loop():
    print()
    while True:
        print("=============================================================")
        print("=======================  Welcome to   =======================")
        print("======================= YT Downloader =======================")
        print("=============================================================\n")
        url = ask_url()
        if url == "exit":
            return
        url_type = determine_url_type(url)

        if url_type == 'plist':
            print()
            save_plist(url)
        elif url_type == "single":
            print()
            save_single(url)
