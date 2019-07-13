"""
Variables
=========

Variables used for running both Twitter and Telegram bots are stored here.

More information about the variables can be found as comments.


Very important information
--------------------------

`TWITTER_SLEEP_TIME` cannot be 60 seconds or more, otherwise the battle
scheduling won't work. Furthermore, times closer to 60 seconds might result
in failures.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



# Twitter API vars
TWITTER_VARS = {
    # Twitter consumer key
    'CONSUMER_KEY'          : "",

    # Twitter consumer secret
    'CONSUMER_SECRET'       : "",

    # Twitter access token
    'ACCESS_TOKEN'          : "",

    # Twitter access token secret
    'ACCESS_TOKEN_SECRET'   : "",

    # Sleep time for WarBotTwitter
    # IMPORTANT: see header
    'SLEEP_TIME'            : 7
}


# Telegram bot token and authorized ID
TELEGRAM_VARS = {
    # Telegram bot token
    'TELEGRAM_TOKEN'    : "",

    # Telegram's ID of authorized user (integer)
    'AUTH_ID'           : None,

    # Sleep time for WarBotAdmin
    'SLEEP_TIME'        : 3
}


from datetime import datetime

class log:
    """
    Class used to log bot status

    ...

    Attributes
    ----------
    SEND_LOG : bool
        Logs are send to stdout if SEND_LOG is True

    Methods
    -------
    send_message(text)
        Sends message with text `text` to stdout if `SEND_LOG`
    
    """

    SEND_LOG = True

    @classmethod
    def send_message(self, text):
        """Sends message with text `text` to stdout if `SEND_LOG`

        Parameters
        ----------
        text : str
            Text to be output to stdout
        """

        if log.SEND_LOG:
            print("(" + str(datetime.now()) + ") " + text)


# Folder routes
#   Specifies the routes to the folders where stuff will be stored
#   The folders must be subfolders of warbot's folder
ROUTES = {
    # Store database
    'DATABASE':     'database',

    # Store temporal images (images received from and sent to Twitter)
    'IMAGES':       'tmp',

    # Store image templates
    'RESOURCES':    'resources',

    # Store logs
    'LOGS':         'logs',

    # Bot scripts
    'BOTS':         'bots'
}


# Filename of database. Will be stored at ROUTES['DATABASE']/filename
DATABASE_FILENAME = 'warbot_db.json'


import os

class route:
    """
    Class to generate absolute file paths
    """

    @staticmethod
    def paste(folder, filename):
        """Generates the route folder/filename

        folder must be a folder on the warbot directory (parent directory of
        this file's parent directory, lib; in other words, must be a folder in
        ./.. -- from vars.py, this file)

        Parameters
        ----------
        folder : str
        filename : str
        """

        (f, _) = os.path.split(os.path.realpath(__file__))
        return os.path.join(os.path.dirname(f), folder + "/" + filename)
