# Filelist QBitTorrent search plugin

#### Installation steps:
1. Copy the ``credentials.txt`` file to the search plugins directory:
    * On Windows, it's usually located at ``%localappdata%\qBittorrent\nova3\engines\``
    * On Linux, it should be under ``~/.local/share/qBittorrent/nova3/engines/`` or ``~/.local/share/qBittorrent/nova3/engines/``.
    * On Mac, 🤷
2. Enter the username and passkey of your filelist account into the ``credentials.txt`` file (**the passkey is not the password of your account, it's the API key that can be found by going to [your Filelist profile](https://filelist.io/my.php)**)
3. Import the latest version of the ``filelist`` search plugin directly into your QBitTorrent application by going to *Search plugins...* -> *Install a new one* -> *Web link* and add the plugin URL
``https://raw.githubusercontent.com/PricopeStefan/Filelist-QBitTorrent-Plugin/master/filelist.py``