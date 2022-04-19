#VERSION: 1.00
# AUTHORS: Stefan Pricoppe (scpricope@gmail.com)

# LICENSING INFORMATION

from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter

# some other imports if necessary
from urllib.parse import urlencode, unquote
import configparser
import json
import pathlib


class filelist(object):
    """
    `url`, `name`, `supported_categories` should be static variables of the engine_name class,
     otherwise qbt won't install the plugin.

    `url`: The URL of the search engine.
    `name`: The name of the search engine, spaces and special characters are allowed here.
    `supported_categories`: What categories are supported by the search engine and their corresponding id,
    possible categories are ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books').
    """
    url = 'https://filelist.io'
    name = 'FileList'
    supported_categories = {
        'all': '0',
        'movies': '1,2,3,4,6,7,12,15,18,19,20,24,25,26',
        'tv': '7,12,13,14,15,18,21,23,24,27',
        'music': '5,11,18,24',
        'games': '8,9,10,17,18,22',
        'anime': '15,18,24',
        'software': '8,9,10,16,17,18,22'
    }
    engines_dir = pathlib.Path(__file__).parent.resolve()

    def __init__(self):
        """
        some initialization
        """
        self.__config = configparser.ConfigParser()

        # Read the username and passkey for accessing the Filelist API
        credentials_file_path = self.engines_dir.joinpath('credentials.txt')
        self.__config.read(str(credentials_file_path))

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        """
        Here you can do what you want to get the result from the search engine website.
        Everytime you parse a result line, store it in a dictionary
        and call the prettyPrint(your_dict) function.

        `what` is a string with the search tokens, already escaped (e.g. "Ubuntu+Linux")
        `cat` is the name of a search category in ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books')
        """
        params = urlencode({
            'username': self.__config['filelist']['username'],
            'passkey': self.__config['filelist']['passkey'],
            'action': 'search-torrents',
            'output': 'json',
            'type': 'name',
            'query': unquote(what)
        })

        query_url = f'{self.url}/api.php?{params}'
        response = retrieve_url(query_url)
        json_response = json.loads(response)

        # if we didnt get a response or it is empty, just return
        if not json_response or not len(json_response):
            return
        
        for torrent in json_response:
            # for each torrent result, parse and print the data needed by qBitTorrent
            torrent_name = torrent['name']
            if torrent['freeleech']:
                torrent_name = '[FREELEECH]' + torrent_name
            if torrent['internal']:
                torrent_name = '[INTERNAL]' + torrent_name

            torrent_data = {
                'link': torrent['download_link'],
                'name': torrent_name,
                'size': str(torrent['size']),
                'seeds': torrent['seeders'],
                'leech': torrent['leechers'],
                'engine_url': self.url,
                'desc_link': torrent['small_description']
            }

            prettyPrinter(torrent_data)