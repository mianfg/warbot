#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import os, sys
from multiprocessing import Process

from warbot.lib.vars import route, ROUTES


def telegram_service():
    telegram_bot_filename = route.paste(ROUTES['BOTS'], 'telegram_bot.py')
    telegram_log_filename = route.paste(ROUTES['LOGS'], 'logs_telegram.txt')
    os.system("python " + telegram_bot_filename + " >> " + telegram_log_filename)
def twitter_service():
    twitter_bot_filename = route.paste(ROUTES['BOTS'], 'twitter_bot.py')
    twitter_log_filename = route.paste(ROUTES['LOGS'], 'logs_twitter.txt')
    os.system("python " + twitter_bot_filename + " >> " + twitter_log_filename)

if __name__ == '__main__':
    p1 = Process(target=telegram_service)
    p2 = Process(target=twitter_service)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
