"""
Todo list:
    - features
        -scan through target directories(default to cwd if not specified) and find those mp3 files which haven't had their subtitle files
        -search through source webpages by name of the song and artist(s)(currently vvlyrics.com)
            -find out ways to get name of the song and artist
        -download subtitle files to the target directories
        -program exits if everthing works properly, otherwise show relevant readable error messages

"""
import sys
import os
import requests
import colorama
from opencc import OpenCC
from colorama import Fore
colorama.init(autoreset = True)

def main():
    target_path = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()
    mp3_lst = collect_mp3(target_path) 
    get_subtitles(mp3_lst, target_path)
    return 0

def collect_mp3(path):
    """collect mp3 files from given path"""
    return [filename for filename in os.listdir(path) if filename[-4:] == ".mp3"]

def get_subtitles(audio_files, target_path):
    """Download subtitle files from source websites to target path"""
    file_info = [(f[0], f[1][:-4]) for f in map(lambda filename: filename.split('_'), audio_files)]
    for artist, song_name in file_info:
        download_subtitle(artist, song_name, target_path)

def download_subtitle(artist, song_name, target_path):
    """Download lrc file by given artist song name"""
    source_handlers = [vvl_handler]
    print(f"Downloading {artist}_{song_name}.lrc...")
    for handler in source_handlers:
        if handler(artist, song_name, target_path):
            print(Fore.GREEN + f"Download {artist}_{song_name}.lrc success")
            return True
    print(Fore.RED + f"Unable to Download {artist}_{song_name}.lrc")
    return False

def vvl_handler(artist, song_name, path, test_exausted = False):
    source = "https://vvlyrics.com"
    headers = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
               'Referer':"https://vvlyrics.com"}
    cc = OpenCC("t2s") # convert traditional chinese characters into simplified ones
    try:
        response = requests.get(f"{source}/artist/{artist}/{song_name}?download=1", headers = headers)
        if not response.ok :
            if not test_exausted:
                return vvl_handler(cc.convert(artist), cc.convert(song_name), path, test_exausted = True)
            else:
                return False
        if path[-1] == '/':
            path = path[:-1]
        with open(f"{path}/{artist}_{song_name}.lrc", "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(Fore.RED + f"something went wrong when downloading the file from {source}")
        print(Fore.RED + e)
        return False

if __name__ == "__main__":
    main()
