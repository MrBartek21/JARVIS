import logging
from datetime import datetime

OWNER = "MrBartek21"

# Token to API
TOKEN_ADD_WORD = 'f9L7Gg9elNpSjKJnUG8p'
TOKEN_WEATHER = '4NFoW3yvFxsrkzlfS7sE'
TOKEN_STATUS = 'eCGHfy3dBxFrQQbt3KkQ'
TOKEN_UPDATE = 'tDoN9DKZcoWSu7jjpi9J'
TOKEN_ACTIVE = 'nmR3tWSEqXHTJvE1Fzv7'

# Link to main server
HEADURL = 'http'
IP = 'classicgames.sytes.net'

# Log formatting
LOG_FORMAT = "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s"
LOG_LEVEL = logging.INFO
LOG_FOLDER = 'Logs'
LOG_FILENAME = 'logs.log'
LOG_FILE = datetime.now().strftime('%Y-%m-%d_%H-%M_'+LOG_FILENAME)

# File and folder name
FILE_WORDS = "words.json"
FILE_USER = "user.json"


# Code to connect to account
CODE = "8520"


#SPEECH
NO_CONNECTION = "Nie mogę nawiązać połączenia, proszę zrestartuj urządzenie."
API_ERROR = "Nie mogę w tej chwili rozpoznać mowy, proszę spróbuj później."
NO_RESPONSE = "Przepraszam nie rozumiem."
RESPONSE = "Slucham."