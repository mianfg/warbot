"""
TelegramInterface
=================

This module interacts directly with the Telegram API.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



import json, requests, time, urllib
from vars import log


class TelegramInterface(object):
    def __init__(self, telegram_token, telegram_sleep_time):
        self.url = "https://api.telegram.org/bot{}/".format(telegram_token)
        self.sleep_time = telegram_sleep_time
        self.auth_id = None
        self.m_queue = []

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    def get_updates(self, offset=None):
        url = self.url + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)
    
    def handle_updates(self, updates):
        updates_list = []

        for update in updates["result"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            user_id = update["message"]["from"]["id"]

            updates_item = {'text': text, 'chat': chat, 'user_id': user_id}
            updates_list.append(updates_item)
        
        return updates_list

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)
    
    def message_queue(self):
        if self.auth_id != None:
            while len(self.m_queue) > 0:
                self.send_message(self.m_queue[0], self.auth_id)
                self.m_queue.pop(0)
    
    def update_message_queue(self):
        pass

    def build_keyboard(self, items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def send_message(self, text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = self.url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        self.get_url(url)

    def main(self):
        last_update_id = None
        while True:
            updates = self.get_updates(last_update_id)

            try:
                if len(updates["result"]) > 0:
                    last_update_id = self.get_last_update_id(updates) + 1
                    self.handle_updates(updates)
            except KeyError:
                log.send_message("[TELEGRAM API] Keyerror was produced. Retrying...")
            
            self.update_message_queue()

            self.message_queue()
            
            time.sleep(self.sleep_time)
