from yt_dlp import YoutubeDL
from math import ceil
from datetime import date
from time import localtime, strftime
from socket import create_connection
from os import chdir, mkdir, path, listdir



def IsInternetAvailable():
    """
    Checks internet availability.

    Returns:
        True:   Internet is available.
        False:  Internet is not available
    """
    try:
        create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def CharPolice(suspect_string):
    """
    Checks for chars that are illegal in naming a file.

    From given string, function removes \\, /, :, *, ?, ", <, >, | 
    (chars illegal in naming files) and returns it.

    Args:
        suspect_string (str): String with potenetial characters to remove.

    Returns:
        str: Argument string without signs illegal in filenaming.
    """
    charlist = [a for a in suspect_string]
    i = 0
    while i < len(charlist):
        if charlist[i] in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
            charlist.pop(i)
        else:
            i += 1
    
    policedstring = "".join(charlist)
    return policedstring

def IllegalToAscii(illegal_string):
    print("Why in the world did You do it? Maybe do something better with Your life than downloading stuff containing just illegal signs?")
    return "_".join((str(ord(char)) for char in illegal_string))

def ZerosAtBeginning(number, max_element_number):
    """
    Determines a number in name of element present in a playlist.

    Depending on number of max element, function will put an adequate number of 0's
    before the index.

    Examples:
        (plist_len = 4):        01, 02, 03, 04
        (plist_len = 64):    ...08, 09, 10, 11,...
        (plist_len = 128):   ...008, 009, 010, 011,..., 098, 099, 100, 101,...

    Args:
        number (int):               number of element in playlist.
        max_element_number (int):   max number that'll be used.

    Returns:
        str: zeros determined by function + number + ". "
    """
    return ((max_element_number < 10) * f"0{number}. ") + ((max_element_number >= 10) * (f"{(len(str(max_element_number)) - len(str(number))) * '0'}{number}. ")) # I'm really sorry. The same code is written below, but it's readable
    if max_element_number < 10:
        return f"0{number}. "
    digits_of_biggest_number    = len(str(max_element_number))
    digits_of_number            = len(str(number))
    gg                          = digits_of_biggest_number - digits_of_number
    return f"{gg * '0'}{number}. "

def Dots(integer):
    """
    Puts dots in long numbers.

    Between every 3 chars puts a dot.

    Args:
        integer (int): A number into which the function will put dots.

    Returns:
        str: Inputted integer with dots added    
    """
    integer = str(integer)
    result = ''
    while len(integer) > 3:
        result = "." + integer[-3:] + result
        integer = integer[:-3]

    result = integer + result 
    return result

def DelDuplicatesFromListOfLists(list_of_lists):
    """
    Deletes duplicate lists from a list of lists.

    Args:
        list_of_lists (list): Self explainatory.

    Returns:
        list: list_of_lists without duplicates.
    """
    curr_el = 0
    while curr_el + 1 < len(list_of_lists):
        a = curr_el + 1
        while a < len(list_of_lists):
            if list_of_lists[curr_el][0] == list_of_lists[a][0] and list_of_lists[curr_el][1] == list_of_lists[a][1]:
                list_of_lists.pop(a)
            else:
                a += 1
        curr_el += 1
    
    return list_of_lists

def GetUrlAndType():
    """
    Asks user for URL, checks if it's valid and determines action.

    Returns:
        list[a, b]:
            a (str): URL inputted by user
            b (str): Action type
    """
    url = str(input("Enter URL: \n>> "))
    if (len(url) > 34 and url[:34] == 'https://youtube.com/playlist?list='):
        inputDE = " "
        while inputDE not in ["", "d", "e"]:
            inputDE = input("What do You want to do with playlist? (Enter - download, e - extract playlist data)\n>>").lower()
        if inputDE == "e":
            return [url, "extract"]
        return [url, 'plist']
    
    elif (len(url) > 17 and url[:17] == 'https://youtu.be/')  \
    or (len(url) > 29 and url[:29] == 'https://www.youtube.com/watch'):
        if '&list=' in url:
            url = url[:url.find('&list=')]
        return [url, 'single']
    
    else:
        print("Invalid URL!\n")
        return [url, 'invalid']

def ReadSaveExtension():
    """
    Asks user for extension.

    In infinite loop, forces user to input either 4, 3 or f 
    to get proper extension.

    Returns:
        str: Extenstion chosen by user.
    """
    user_input = " "
    format_dict = {"4": "mp4", "3": "mp3", "f": "flac"}
    while user_input not in format_dict:
        user_input = input("What format do You want to save as? (4 - mp4, 3 - mp3, f - flac)\n>>").lower()
    
    return format_dict[user_input]

def ReadDelDuplicates():
    """
    Asks user what to do in case duplicates appear in playlist.

    Returns:
        boolean: True - delete duplicates, False - leave duplicates.
    """

    user_input = " "
    dupl_dict = {"": True, "d": True, "l": False}
    while user_input not in dupl_dict:
        user_input = input("Duplicates detected. What should be done about them? (Enter - delete, l - leave)\n>>").lower()
    
    return dupl_dict[user_input]

def ReadNumOfTracks(plist_len): 
    """
    Asks user which elements to download.

    If user presses enter, list from 0 to plist_len will be returned.
    If user inputs an integer, list from 0 to that integer will be returned.
    If user inputs c, they'll be asked to input number of first and last element. 
    [start-1, end] will be returned.
    Else, list from 0 to plist_len will be returned.
    When input is too big, small or incorrect, a default value will be assigned.

    Args:
        plist_len (int): Length of playlist considered.

    Returns:
        list[int, int]: Indexes of first and last element to be downloaded.
    """
    num = input("How to download the elements? (Enter - all, integer number - number of elements from start, c - custom settings...)\n>>").lower()
    if num == '':
        return [0, plist_len]
    
    elif num == 'c':
        start = input("Starting from element:\n>>")
        if not start.isdigit():
            print("Starting from the beginning.")
            start = 0
        elif int(start) > plist_len or int(start) < 1:
            print("Starting from the beginning.")
            start = 0
        else:
            start = int(start) - 1

        end = input("Ending on element:\n>>")  
        if not end.isdigit():
            print("Ending at the end.")
            end = plist_len
        elif int(end) < start or int(end) > plist_len:
            print("Ending at the end.")
            end = plist_len
        else:
            end = int(end)

        return [start, end]

        
    elif num.isdigit() and int(num) <= plist_len:
        return [0, int(num)]
    
    elif num.isdigit() and int(num) > plist_len:
        print("Number inputted by You is too big! Downloading all the tracks.\n")
        return [0, plist_len]
    
    else:
        print("Downloading whole playlist.\n")
        return [0, plist_len]
    
def ReadNumbered(min_el_index, max_el_index):
    """
    Determines numbering in filenames.

    In series of questions, function determines if elements should be numbered, 
    and if so, in what order and on what number will the numbering start.
    
    Args:
        min_el_index (int): Index of the first element to be numbered.
        max_el_index (int): Index of the last element to be numbered.

    Returns:
        list[a, b]: 
            a (str): Naming order ("asc", "desc", "not").
            b (int): Number of first downloaded element.
    """
    user_input = " "

    while True:
        user_input = input("Do You want elements to be numbered? (Enter - starting on 1, integer - starting on integer, n - no, c - custom...)\n>>").lower()

        if user_input == "" or user_input == "y":
            return ["asc", 1]
        if user_input.isdigit():
            return ["asc", int(user_input)]
        if user_input == "n":
            return ["not", -1]
        if user_input == "c":
            if min_el_index != 0:
                user_input_custom = input("Choose custom numbering option (starting from element's number in playlist [n - normal order, r - reverse order], d - descending from...):\n>>").lower()
                if user_input_custom == "n":
                    return ["asc", min_el_index+1]
            else:
                user_input_custom = input("Choose custom numbering option (r - reverse order, d - descending from...):\n>>").lower()

            if user_input_custom == "r":
                return ["desc", max_el_index+1]
            if user_input_custom == "d":
                number_of_elements = max_el_index - min_el_index + 1
                desc_from = input(f"Files will be numbered in reversed order, starting from (not lower than {number_of_elements}):\n>>")
                if desc_from.isdigit():
                    desc_from = int(desc_from)
                    if desc_from >= number_of_elements:
                        return ["desc", desc_from]

def ReadExtractWriteOrder():
    """
    Asks user for extract order.

    Returns:
        string: "asc" or "desc".
    """
    order = ""
    result_dict = {"a": "asc", "d": "desc"}
    while order not in result_dict:
        order = input("In what order do You want to write elements to file? (a - ascending, d - descending)\n>>").lower()
    return result_dict[order]

def ReadTrimLens():
    """
    Asks user about cutting names of the elements.

    Returns:
        list[a, b]:
            a (int): Number of letters cut from the start of filename.
            b (int): Number of letters cut from the end of filename.
    """
    inputSC = " "
    namecut_list = [0, 0]
    while inputSC not in ["", "s", "b", "e"]:
        inputSC = input("Do You want to trim names of all elements? (Enter - no, s - at the start, e - at the end, b - both)\n>>").lower()

    if inputSC == "s":
        namecut_list[0] = str(input("Input the string or length You want to trim at the start:\n>>"))
        if namecut_list[0].isdigit():
            namecut_list[0] = int(namecut_list[0])
        else:
            namecut_list[0] = len(namecut_list[0])

    elif inputSC == "e":
        namecut_list[1] = str(input("Input the string or length You want to trim at the ending:\n>>"))
        if namecut_list[1].isdigit():
            namecut_list[1] = int(namecut_list[1])
        else:
            namecut_list[1] = len(namecut_list[1])

    elif inputSC == "b":
        namecut_list[0] = str(input("Input the string or length You want to trim at the start:\n>>"))
        if namecut_list[0].isdigit():
            namecut_list[0] = int(namecut_list[0])
        else:
            namecut_list[0] = len(namecut_list[0])

        namecut_list[1] = str(input("Input the string or length You want to trim at the ending:\n>>"))
        if namecut_list[1].isdigit():
            namecut_list[1] = int(namecut_list[1])
        else:
            namecut_list[1] = len(namecut_list[1])

    return namecut_list

def NameYourFile(OGtitle, title_number, namecut_list):
    """
    Changes a string to match it with user's desired outcome.

    Trims the title if needed, removes illegal signs and adds index.
    Due to program's characteristics, function does not handle negative ints in namecut list.

    Args:
        title (str):                            Title of youtube video.
        titleindex (str):                       Numbering in filename (after adding zeros).
        namecut_list (list[a (int), b (int)]):  Number of characters to be cut from start end end of the title.

    Returns:
        str: Final name of a file.
    """
    lens = namecut_list[0]
    lene = namecut_list[1]
    policed_OGtitle = CharPolice(OGtitle)

    #nothing remains after policing
    if policed_OGtitle == "" and title_number == "":
        return IllegalToAscii(OGtitle)

    #nothing remains after trimming name
    if (lens + lene >= len(OGtitle) or lens >= len(OGtitle) or lene > len(OGtitle)) and title_number == "":
        if len(policed_OGtitle) != len(OGtitle):
            print(f"Length of a trim is larger than the title. Returning original title with illegal chars removed...")
        else:
            print("Length of a trim is larger than the title. Returning original title...")
        return policed_OGtitle
    
    if lene == 0:
        ret_title = OGtitle[lens:]
    else:
        ret_title = OGtitle[lens:-lene]
    policed_ret_title = CharPolice(ret_title)

    if policed_ret_title == "" and title_number == "": #nothing remains after trimming and policing
        print("After trimming, title contains only illegal signs")
        return IllegalToAscii(ret_title)

    if len(policed_OGtitle) != len(OGtitle):
        print(f"{OGtitle} - has been updated to not contain illegal characters")
    return title_number + policed_ret_title

def RoundOrExact():
    """
    Asks user if extracted video views should be exact or rounded.

    Returns:
        str: "round" or "exact".
    """
    input_RE = " "
    RE_dict = {"": "round", "r": "round", "e": "exact"}
    input_RE = input("Do You want viewcount on every video be exact or rounded? Extracting exact values will take significantly longer time. (Enter - rounded, e - exact)\n>>").lower()

    if input_RE in RE_dict:
        return RE_dict[input_RE]

def SaveSingle(url):
    """
    Downloads element from given URL

    Extracts video title from URL, checks if it's correct, adjusts YoutubeDL 
    object parameters and downloads.

    Args:
        url (str) - correct URL to youtube video
    """
    try:
        with YoutubeDL(ydl_getdata) as ydl:
            OGtitle = ydl.extract_info(url, download=False)["title"]
    except:
        if not IsInternetAvailable():
            print("Internet connection failed.\n\n")
            return
        else:
            print("Something went wrong")
        
    finalname = CharPolice(OGtitle)
    if finalname == "":
        finalname = IllegalToAscii(OGtitle)
    i = 1
    while path.exists(desktop_path + "/" + finalname):
        finalname += "_d"*i
        i += 1

    ydl_opts["outtmpl"] = finalname
    ydl_opts["paths"] = {"home": desktop_path}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n" + finalname + " has been successfully downloaded")
    except:
        if not IsInternetAvailable():
            print("Internet connection failed.\n\n")
            return
        else:
            print("Something went wrong")

def SavePlist(plist_url): 
    """
    Downloads elements from a youtube playlist.

    Gets a list of all urls and their respective names from a playlist, handles
    duplicates, reads number of tracks, numbering method and cutting names of 
    files. Then, makes a directory on desktop and starts downloading them, 
    assigning correct names to every file.

    Args:
        plist_url (str): URL of downloaded playlist.
    """
    try:
        with YoutubeDL(ydl_getdata) as ydl:
            plist_dict = ydl.extract_info(plist_url, download=False)
    except:
        if not IsInternetAvailable():
            print("Internet connection failed.\n\n")
            return
        else:
            print("Something went wrong")


    plist_title = plist_dict['title']
    print(plist_title)
    plist_list = [[el['url'], el['title']] for el in plist_dict['entries']] 

    plist_list_no_dupli = DelDuplicatesFromListOfLists(plist_list)
    if len(plist_list) != len(plist_list_no_dupli):
        if ReadDelDuplicates():
            plist_list = plist_list_no_dupli

    plist_len = plist_dict['playlist_count']
    index_range = ReadNumOfTracks(plist_len)
    numbered = ReadNumbered(index_range[0], index_range[1])
    if numbered[0] != "not":
        temp_filenum = numbered[1]
        if numbered[0] == "asc":
            last_num = index_range[0] + plist_len
        elif numbered[0] == "desc":
            last_num = index_range[0] - plist_len
    else:
        temp_filenum = ""

    namecut_list = ReadTrimLens()

    dir_name = CharPolice(plist_title)
    if dir_name == "":
        dir_name = IllegalToAscii(plist_title)

    while path.exists(desktop_path + "/" + dir_name):
        dir_name += "_d"
    mkdir(dir_name)
    chdir(dir_name)
    total_errors = 0
    fileindex = ""
    ydl_opts["paths"] = {"home": desktop_path + "/" + dir_name}
    print("Downloading...")


    
    for index in range(index_range[0], index_range[1]):
        vid_url = plist_list[index][0]
        vid_OGname = plist_list[index][1]
        
        if numbered[0] != "not":
            fileindex = ZerosAtBeginning(temp_filenum, last_num)
            
        finalfilename = NameYourFile(vid_OGname, fileindex, namecut_list)

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
            if not IsInternetAvailable():
                print("Internet connection failed.\n\n")
                return
            else:
                total_errors += 1
                print(f"{finalfilename} could not be downloaded. Here's link to this video: {vid_url}")
       

    if total_errors == 0:
        print("\n" + plist_title + " playlist has been successfully downloaded")
    elif total_errors == 1:
        print("\n" + "Downloading " + plist_title + " didn't go smooth. There has been 1 exception")
    else:
        print("\n" + "Downloading " + plist_title + " didn't go smooth. There have been " + str(total_errors) + " exceptions")

def ExtractPlistData(plist_url):
    """
    Extracts data from a playlist to a file.

    Downloads a playlist dictionary, asks for round or exact viewcount and write 
    order. Depending on viewcount options, either gets it for every video from 
    playlist dictionary or downloads it for every video separately. Then, creates
    a directory with playlist name on desktop if it doesn't exist and makes a file
    inside. Inside, puts playlist data, then data of every video in order
    established earlier. In the end, puts number of errors that have occurred 
    during the extract.

    Args:
        plist_url (str): url of a playlist.
    """
    
    try:
        with YoutubeDL(ydl_getdata) as ydl:
            plist_dict = ydl.extract_info(plist_url, download=False)
    except:
        if not IsInternetAvailable():
            print("Internet connection failed.\n\n")
            return
        else:
            print("Something went wrong")

    plist_title = plist_dict['title']
    dir_name = CharPolice(plist_title)
    if dir_name == "":
        dir_name = IllegalToAscii(plist_title)
    dirname += "_extracts"
    
    round_or_exact = RoundOrExact()
    write_order = ReadExtractWriteOrder()
    if round_or_exact == "round":
        plist_list = [[el["url"], el["title"], el["view_count"]] for el in plist_dict['entries']]
    elif round_or_exact == "exact":
        plist_list = [[el["url"], el["title"]] for el in plist_dict['entries']] 
        try:
            for el in plist_list:
                with YoutubeDL(ydl_getdata) as ydl:
                    temp_vid_dict = ydl.extract_info(el[0], download=False)
                el.append(temp_vid_dict["view_count"])
        except:
            if not IsInternetAvailable():
                print("Internet connection failed.\n\n")
                return
            else:
                print("Something went wrong")

    print("Data is extracted and it's almost time to write everything to a file")
    plist_len = plist_dict['playlist_count']

    if write_order == "asc":
        start_index = 0
        end_index   = plist_len
        first_quart = ceil(plist_len/4)
        third_quart = ceil((plist_len/4)*3)
        pop_index   = 0
    else:
        start_index = plist_len - 1
        end_index   = -1
        first_quart = ceil((plist_len/4)*3)
        third_quart = ceil(plist_len/4)
        pop_index   = -1

    halfway         = ceil(plist_len/2)
    quart_dict      = {first_quart: "One quarter down, three to go", halfway: "We're halfway there!", third_quart: "Just one more quarter..."}
    total_errors    = 0
    calendarium     = str(date.today())
    current_time    = strftime("%H:%M:%S", localtime())
    filename        = dir_name + "_extract_" + calendarium[:4] + calendarium[5:7] + calendarium[8:10] + current_time[:2] + current_time[3:5] + current_time[6:8] + write_order

    if not path.exists(desktop_path + "/" + dir_name):
        mkdir(dir_name)
    chdir(dir_name)

    with open(filename + ".txt", "w") as f:
        f.write(f"Playlist name: \t\t\t{plist_title}\n")
        f.write(f"Playlist's url:\t\t\t{plist_dict['original_url']}\n")
        f.write(f"Playlist's owner: \t\t{plist_dict['channel']}\n")
        f.write(f"Owner's URL: \t\t\t{plist_dict['channel_url']}\n")
        modified_date = plist_dict['modified_date']
        modified_date = modified_date[-2:] + "." + modified_date[4:6] + "." + modified_date[:4]
        f.write(f"Playlist last updated on: \t{modified_date}\n")
        f.write(f"Time of this data extract: \t{calendarium}, {current_time} \n")
        f.write(f"Playlist views so far: \t\t{Dots(plist_dict['view_count'])}\n")
        f.write(f"Current playlist length: \t{plist_len}\n\n\n\n")
        print("Downloading...")
        
        for index in range(start_index, end_index, 1-2*(end_index==-1)):
            if index in quart_dict:
                print(quart_dict.pop(index))

            try:
                f.write(f"{index + 1}. {plist_list[pop_index][1]}\n")
                f.write(f"Views: {Dots(plist_list[pop_index][2])}\n")
                f.write(f"{plist_list[pop_index][0]}\n\n") #URL
            except:
                total_errors += 1
                f.write(f"{plist_len - index}. An error has occurred when trying to download data of a video with URL: {plist_list[pop_index]}\n\n")
            plist_list.pop(pop_index)

        if total_errors == 0:
            f.write("\n\n\n\n\nNo errors have occurred during extraction")
        else:
            f.write(f"\n\n\n\n\nNumber of errors during extraction: {total_errors}")
    
    print("\n" + plist_title + " data has been successfully extracted to Your desktop!")
    if total_errors == 0:
        print("No errors have occurred during extraction")
    else:
        print(f"Number of errors during extraction: {total_errors}")