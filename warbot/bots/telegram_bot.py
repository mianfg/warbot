#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
telegram_bot
============

Executes Telegram bot's main handling function.

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

from admin import WarBotAdmin
from vars import TELEGRAM_VARS, ROUTES, FILENAMES


a = WarBotAdmin(
    telegram_token      = TELEGRAM_VARS['TELEGRAM_TOKEN'],
    telegram_sleep_time = TELEGRAM_VARS['SLEEP_TIME'],
    database_route      = ROUTES['DATABASE'],
    database_filename   = FILENAMES['DATABASE'],
    phrases_route       = ROUTES['PHRASES'],
    phrases_filename    = FILENAMES['PHRASES'],
    auth_id             = TELEGRAM_VARS['AUTH_ID']
)

if __name__ == '__main__':
    a.main()
