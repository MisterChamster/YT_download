from yt_dlp import YoutubeDL
from os import chdir, mkdir, path, listdir
from src.common.askers import (ask_save_ext,
                               ask_save_path)
from src.common.utils import (illegal_char_remover,
                              is_internet_available,
                              get_ydl_options)
from src.helpers_save_plist.askers_plist import (ask_del_duplicates,
                                                    ask_num_of_tracks,
                                                    ask_numbering,
                                                    ask_read_trim_lens,
                                                    ask_which_tracks)
from src.helpers_save_plist.save_plist_utils import (name_file_on_plist,
                                                     zeros_at_beginning,
                                                     get_indexes_of_duplicates,
                                                     are_duplicates,
                                                     del_indexes)
from src.common.ydl_support import get_plist_dict



def save_plist(plist_url): 
    """
    Downloads elements from a youtube playlist.

    Gets a list of all urls and their respective names from a playlist, handles
    duplicates, reads number of tracks, numbering method and cutting names of 
    files. Then, makes a directory on desktop and starts downloading them, 
    assigning correct names to every file.

    Args:
        plist_url (str): URL of downloaded playlist.
    """
    # Get playlist dictionary
    plist_dict = get_plist_dict(plist_url)
    if plist_dict == None:
        return

    # Get playlist title
    plist_title = plist_dict['title']
    print(f"Playlist: {plist_title}")
    print()

    # Get lists with videos data
    plist_urls = [el['url'] for el in plist_dict['entries']]
    plist_vid_titles = [el['title'] for el in plist_dict['entries']]

    # Check and handle duplicates
    if are_duplicates(plist_urls):
        if ask_del_duplicates():
            dupli_indexes = get_indexes_of_duplicates(plist_urls)

            plist_urls = del_indexes(plist_urls, dupli_indexes)
            plist_vid_titles = del_indexes(plist_vid_titles, dupli_indexes)
        print()
    # I don't care about indexing b4 deleting duplicates and neither should you

    # Get save extension from user and correct ydl options
    extension = ask_save_ext()
    print()
    ydl_opts = get_ydl_options(extension)


    # START WORK HERE
    # ask_which_tracks

    plist_len = len(plist_urls)
    index_range = ask_num_of_tracks(plist_len)
    print()
    numbered = ask_numbering(index_range[0], index_range[1])
    print()
    if numbered[0] != "not":
        temp_filenum = numbered[1]
        if numbered[0] == "asc":
            last_num = index_range[0] + plist_len
        elif numbered[0] == "desc":
            last_num = index_range[0] - plist_len
    else:
        temp_filenum = ""

    namecut_list = ask_read_trim_lens()
    print()

    dir_name = illegal_char_remover(plist_title)

    save_path = ask_save_path()
    if save_path == "":
        print("Empty path was chosen.")
        return
    chdir(save_path)

    while path.exists(save_path + "/" + dir_name):
        dir_name += "_d"
    mkdir(dir_name)
    chdir(dir_name)
    total_errors = 0
    fileindex = ""
    ydl_opts["paths"] = {"home": save_path + "/" + dir_name}
    print(f"Downloading {plist_title}...")

    for index in range(index_range[0], index_range[1]):
        vid_url = plist_urls[index]
        vid_og_name = plist_vid_titles[index]

        if numbered[0] != "not":
            fileindex = zeros_at_beginning(temp_filenum, last_num)

        finalfilename = name_file_on_plist(vid_og_name, fileindex, namecut_list)

        while finalfilename in listdir():
            finalfilename += "_d"
        ydl_opts["outtmpl"] = finalfilename

        if numbered[0] == "asc":
            temp_filenum += 1
        elif numbered[0] == "desc":
            temp_filenum -= 1

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([vid_url])
            print(finalfilename)
        except:
            if not is_internet_available():
                print("Internet connection failed.\n\n")
                return
            else:
                total_errors += 1
                print(f"{finalfilename} could not be downloaded. Here's link to this video: {vid_url}")

    if total_errors == 0:
        print("\n" + plist_title + " playlist has been successfully downloaded.\n\n")
    elif total_errors == 1:
        print("\n" + "Downloading " + plist_title + " didn't go smooth. There has been 1 exception.\n\n")
    else:
        print("\n" + "Downloading " + plist_title + " didn't go smooth. There have been " + str(total_errors) + " exceptions.\n\n")
