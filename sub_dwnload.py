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
from opencc import OpenCC
from bs4 import BeautifulSoup

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
        download_subtitles(artist, song_name)

if __name__ == "__main__":
    main()
