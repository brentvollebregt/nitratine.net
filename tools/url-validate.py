"""
Take a list of known URLs from one domain and validate that they exist on another domain
"""

import requests

ORIGINAL_DOMAIN = "https://nitratine.net"
NEW_DOMAIN = "https://test.nitratine.net"

ROUTES_TO_CHECK = """
https://nitratine.net/
https://nitratine.net/blog/post/spotify-lyrics-viewer/
https://nitratine.net/blog/categories/#General
https://nitratine.net/blog/tags/#tool
https://nitratine.net/blog/tags/#ctf
https://nitratine.net/blog/post/media-picker/
https://nitratine.net/blog/post/my-desktop-backgrounds/
https://nitratine.net/blog/tags/#website
https://nitratine.net/blog/tags/#requests
https://nitratine.net/blog/tags/#flask
https://nitratine.net/blog/tags/#sqlite
https://nitratine.net/blog/archive/#2018
https://nitratine.net/blog/tags/#android
https://nitratine.net/blog/post/python-threading-basics/
https://nitratine.net/blog/post/how-to-manage-multiple-python-distributions/
https://nitratine.net/blog/post/spotify-playlist-downloader/
https://nitratine.net/blog/post/understanding-the-python-root-folder/
https://nitratine.net/blog/tags/#sql
https://nitratine.net/blog/tags/#twitter
https://nitratine.net/blog/tags/#itunes
https://nitratine.net/blog/tags/#money
https://nitratine.net/blog/post/how-to-use-pynputs-mouse-and-keyboard-listener-at-the-same-time/
https://nitratine.net/blog/tags/#chrome
https://nitratine.net/blog/archive/#2020
https://nitratine.net/blog/tags/#gui
https://nitratine.net/blog/post/finding-emotion-in-music-with-python/
https://nitratine.net/blog/post/simulate-mouse-events-in-python/
https://nitratine.net/blog/post/xor-python-byte-strings/
https://nitratine.net/blog/tags/#hashing
https://nitratine.net/blog/tags/#pyqt
https://nitratine.net/blog/tags/#csv
https://nitratine.net/blog/tags/#pypi
https://nitratine.net/blog/post/putting-auto-py-to-exe-on-pypi/
https://nitratine.net/blog/tags/#clipboard
https://nitratine.net/blog/post/how-to-add-a-custom-domain-to-a-github-pages-site/
https://nitratine.net/blog/post/new-zealand-cyber-security-challenge-2019-round-0-solutions/
https://nitratine.net/blog/tags/#networking
https://nitratine.net/blog/post/python-retweet-bot/
https://nitratine.net/blog/archive/#2017
https://nitratine.net/blog/post/python-sqlite3-basics/
https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
https://nitratine.net/blog/post/how-to-import-a-pyqt5-ui-file-in-a-python-gui/
https://nitratine.net/blog/post/python-guis-with-pyqt/#locating
https://nitratine.net/blog/tags/#pynput
https://nitratine.net/blog/post/am-i-a-participant/
https://nitratine.net/blog/post/how-to-clean-a-twitter-account-with-jquery/
https://nitratine.net/blog/post/price-per-unit/
https://nitratine.net/blog/post/multi-clipboard/
https://nitratine.net/blog/tags/#jquery
https://nitratine.net/blog/post/convert-py-to-exe/
https://nitratine.net/blog/tags/#encryption
https://nitratine.net/blog/post/python-gui-using-chrome/
https://nitratine.net/blog/tags/#python
https://nitratine.net/blog/tags/#lerna
https://nitratine.net/blog/post/how-to-setup-pythons-pip/
https://nitratine.net/blog/post/how-to-hash-files-in-python/
https://nitratine.net/blog/tags/#backgrounds
https://nitratine.net/blog/post/python-auto-clicker/
https://nitratine.net/blog/post/how-to-get-stored-wifi-passwords-in-windows/
https://nitratine.net/blog/post/python-size-and-time-cache-decorator/
https://nitratine.net/blog/tags/#pyqt5
https://nitratine.net/blog/tags/#domain
https://nitratine.net/blog/tags/#java
https://nitratine.net/blog/post/hit-counter/
https://nitratine.net/blog/tags/#html
https://nitratine.net/blog/post/randomly-generating-numbers-to-fulfil-an-integer-range/
https://nitratine.net/blog/tags/#google
https://nitratine.net/blog/tags/#eel
https://nitratine.net/blog/post/adding-snow-to-your-website/
https://nitratine.net/blog/tags/#pyinstaller
https://nitratine.net/blog/post/mp3-itunes-downloader/
https://nitratine.net/blog/post/change-file-modification-time-in-python/
https://nitratine.net/blog/post/fix-python-is-not-recognized-as-an-internal-or-external-command/
https://nitratine.net/blog/post/colour/
https://nitratine.net/blog/post/javascript-date-methods-return-values/
https://nitratine.net/blog/tags/#nzcsc
https://nitratine.net/blog/tags/#mouse
https://nitratine.net/blog/tags/#dialog
https://nitratine.net/blog/post/lucy-in-the-sky-with-emotion/
https://nitratine.net/blog/tags/#tweepy
https://nitratine.net/blog/post/interesting-sites/
https://nitratine.net/blog/post/how-to-get-mouse-clicks-with-python/
https://nitratine.net/blog/tags/#email
https://nitratine.net/blog/post/uow-moodle-rwa-ignorer/
https://nitratine.net/blog/post/python-keylogger/
https://nitratine.net/blog/post/how-to-detect-key-presses-in-python/
https://nitratine.net/blog/post/how-to-make-hotkeys-in-python/
https://nitratine.net/blog/post/the-nitratine-project/
https://nitratine.net/blog/tags/#images
https://nitratine.net/blog/post/how-to-create-dialogs-in-python/
https://nitratine.net/blog/post/get-wifi-passwords-with-python/
https://nitratine.net/blog/tags/#decorator
https://nitratine.net/blog/tags/#threading
https://nitratine.net/blog/post/quick-script/
https://nitratine.net/blog/tags/#download
https://nitratine.net/blog/post/remove-columns-in-a-csv-file-with-python/
https://nitratine.net/blog/post/monopoly-money/
https://nitratine.net/blog/tags/#css
https://nitratine.net/blog/tags/#logging
https://nitratine.net/blog/tags/#bot
https://nitratine.net/blog/post/google-publisher-toolbar-please-copy-this-code/
https://nitratine.net/blog/post/github-badges/
https://nitratine.net/blog/tags/#wifi
https://nitratine.net/blog/tags/#keyboard
https://nitratine.net/blog/post/whos-on-my-network/
https://nitratine.net/blog/categories/#Snippets
https://nitratine.net/blog/tags/#javascript
https://nitratine.net/blog/categories/#Tutorials
https://nitratine.net/blog/categories/#YouTube
https://nitratine.net/blog/tags/#express
https://nitratine.net/blog/categories/#Investigations
https://nitratine.net/blog/tags/#typescript
https://nitratine.net/blog/categories/#Projects
https://nitratine.net/blog/categories/#Apps
https://nitratine.net/blog/archive/#2019
https://nitratine.net/blog/categories/#Tools
https://nitratine.net/blog/tags/#spotify
https://nitratine.net/blog/post/useful-online-tools-for-developers/
https://nitratine.net/blog/tags/#react
https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/
https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
https://nitratine.net/blog/post/python-guis-with-pyqt/
https://nitratine.net/blog/post/python-requests-tutorial/
https://nitratine.net/blog/post/how-to-send-an-email-with-python/
https://nitratine.net/blog/post/emotionify/
https://nitratine.net/blog/
https://nitratine.net/blog/page/3/
https://nitratine.net/blog/page/4/
https://nitratine.net/blog/page/6/
https://nitratine.net/blog/page/7/
https://nitratine.net/blog/page/2/
https://nitratine.net/blog/page/5/
https://nitratine.net/blog/post/auto-py-to-exe/
https://nitratine.net/blog/post/encryption-and-decryption-in-python/
https://nitratine.net/about/
https://nitratine.net/portfolio/
https://nitratine.net/data/
https://nitratine.net/blog/post/simulate-keypresses-in-python/
https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/
"""

for route in ROUTES_TO_CHECK.strip().split('\n'):
    new_route = route.replace(ORIGINAL_DOMAIN, NEW_DOMAIN)
    print(f'Checking {new_route}')
    response = requests.get(new_route)

    if response.status_code != 200:
        print(f'[404] {new_route}')