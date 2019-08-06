#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
twitter_bot
===========

Executes Twitter bot's main handling function.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



# import from other folder
import os, sys
(folder, _) = os.path.split(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(folder), "lib"))

from twitter import WarBotTwitter
from vars import TWITTER_VARS, ROUTES, FILENAMES


t = WarBotTwitter(
    consumer_key        = TWITTER_VARS['CONSUMER_KEY'],
    consumer_secret     = TWITTER_VARS['CONSUMER_SECRET'],
    access_token        = TWITTER_VARS['ACCESS_TOKEN'],
    access_token_secret = TWITTER_VARS['ACCESS_TOKEN_SECRET'],
    twitter_sleep_time  = TWITTER_VARS['SLEEP_TIME'],
    database_route      = ROUTES['DATABASE'],
    database_filename   = FILENAMES['DATABASE'],
    phrases_route       = ROUTES['PHRASES'],
    phrases_filename    = FILENAMES['PHRASES'],
    ih_images_route     = ROUTES['IMAGES'],
    ih_resources_route  = ROUTES['RESOURCES'],
    ih_store_route      = ROUTES['IMAGES']
)

if __name__ == "__main__":
    t.main()