"""
WarBotAPI
=========

This module interacts with the Twitter API.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



from database import WarBotDB
from vars import route, log

import tweepy, urllib


class WarBotAPI:
    """
    Class used to interact with Twitter API

    ...

    Attributes
    ----------
    db : WarBotDB
        WarBot database
    api_auth : tweepy.OAuthHandler
        Handles Twitter's API OAuth
    api : tweepy.API
        Tweepy interface
    images_route : str
        Folder route to store images

    Methods
    -------
    get_mentions()
        Gets mentions from Twitter bot's account
    post_tweet(text, media=None)
        Post tweet in bot's timeline
    download_profilepic(username, filename)
        Download username's profile picture
    """

    def __init__(self, consumer_key, consumer_secret, \
        access_token, access_token_secret, \
        database_route, database_filename, images_route):
        """
        Parameters
        ----------
        consumer_key : str
            Twitter app consumer key
        consumer_secret : str
            Twitter app consumer secret
        access_token : str
            Twitter app access token
        access_token_secret : str
            Twitter app access token secret
        database_route : str
            Folder route to database file
        database_filename : str
            Filename of JSON database for WarBotDB
        images_route : str
            Folder route to store images.
                To avoid bugs, must be absolute path
        """

        self.db = WarBotDB(database_route, database_filename)
        self.api_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api_auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.api_auth)
        self.images_route = images_route


    def get_mentions(self):
        """Gets mentions from Twitter bot's account

        Returns
        -------
        list<Status># WIP check if this is the class, or it is not Status
            List of mentions
        """

        last_seen_id = self.db.get_last_seen_id()
        try:
            mentions = self.api.mentions_timeline(last_seen_id, tweet_mode='extended')
            if len(mentions) > 0:
                self.db.update_last_seen(mentions[0].id)
            
            return reversed(mentions)
        except Exception as e:
            log.send_message("[TWITTER API] ERROR - at api.mentions_timeline() -> " + str(e))
            return []


    def post_tweet(self, text, media=None):
        """Post tweet in bot's timeline

        Parameters
        ----------
        text : str
            Text of tweet
        media : list<str>
            List of filenames of media to be tweeted
        """

        mids = None
        if media != None:
            mids = []
            for filename in media:
                res = self.api.media_upload(filename)
                mids.append(res.media_id)
        
        try:
            self.api.update_status(status=text, media_ids=mids)
            log.send_message("[TWITTER API] tweet posted")
        except Exception as e:
            log.send_message("[TWITTER API] ERROR - at api.update_status() -> " + str(e))


    def download_profilepic(self, username, filename):
        """Download username's profile picture

        Parameters
        ----------
        username : str
            Twitter username whose picture wants to be downloaded
        filename : str
            Filename where picture will be saved

        Return
        ------
        Option 1: str
            File route to the downloaded pic
        Option 2: None
            In case download could not be done
        """

        file_download_route = route.paste(self.images_route, filename)
        try:
            url = self.api.get_user(screen_name=username).profile_image_url_https.replace('_normal', '')
            urllib.request.urlretrieve(url, file_download_route)
            return file_download_route
        except Exception as e:
            log.send_message("[TWITTER API] ERROR - at api.get_user -> " + str(e))
            return None
