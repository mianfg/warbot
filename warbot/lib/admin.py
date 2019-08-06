#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WarBotAdmin
===========

This module interacts with the Telegram bot.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



# WarBotAdmin inherits TelegramInterface
from telegram import TelegramInterface
from warbot import WarBot
from vars import log

from datetime import datetime   # store dates


class WarBotAdmin(TelegramInterface):
    """
    Class used to interact with Telegram bot

    ...

    Attributes
    ----------
    bot : WarBot
        WarBot controller instance
    __ask_status : str
        Environment variable to determine which output should be given
        (Used for Telegram buttons)
    _auth_id : int
        Telegram user authorized to interact with the bot
    
    Methods
    -------
    update_message_queue()
        Updates Telegram message queue. Messages in the queue will be sent
    handle_updates(updates)
        Handles the messages that users send to the bot
    handle_help(chat)
        Handles command /help
    handle_unauthorized(chat)
        Handles message sent by unauthorized user
    handle_start(chat)
        Handles command /start
    handle_runoptin(chat)
        Handles command /runoptin
    handle_stopoptin(chat)
        Handles command /stopoptin
    handle_nextbattle(chat)
        Handles command /nextbattle
    handle_schedulebattle(chat, attr)
        Handles command /schedulebattle
    handle_battlefrequency(chat)
        Handles command /battlefrequency
    handle_setbattlefrequency(chat, attr)
        Handles command /setbattlefrequency
    handle_stopfrequency(chat)
        Handles command /stopfrequency
    handle_forcebattle(chat, attr)
        Handles command /forcebattle
    handle_getfighters(chat)
        Handles command /getfighters
    handle_getfighter(chat, attr)
        Handles command /getfighter
    handle_getcandidates(chat)
        Handles command /getcandidates
    handle_addfighter(chat, attr)
        Handles command /addfighter
    handle_deletefighter(chat, attr)
        Handles command /deletefighter
    handle_addcandidate(chat, attr)
        Handles command /addcandidate
    handle_deletecandidate(chat, attr)
        Handles command /deletecandidate
    handle_revive(chat, attr)
        Handles command /revive
    handle_announcefighters(chat)
        Handles command /announcefighters
    handle_stopannouncefighters(chat)
        Handles command /stopannouncefighters
    handle_status(chat)
        Handles command /status
    handle_restart(chat, attr)
        Handles command /restart

    """


    def __init__(self, telegram_token, telegram_sleep_time, \
        database_route, database_filename, \
        phrases_route, phrases_filename, auth_id):
        """
        Parameters
        ----------
        telegram_token : str
            Telegram bot token
        telegram_sleep_time : int
            Update time, in seconds
        database_filename : str
            Filename of JSON database for WarBotDB.
                To avoid bugs, must be absolute path
        phrases_route : str
            Folder route to phrases file
        phrases_filename : str
            Filename of txt file containing battle phrases
        auth_id : int
            Telegram ID of authorized user
        """

        super(WarBotAdmin, self).__init__(telegram_token, telegram_sleep_time)
        self.bot = WarBot(database_route, database_filename, \
            phrases_route, phrases_filename)
        self.ask_status = "NONE"
        self.auth_id = auth_id


    def update_message_queue(self):
        """Updates Telegram message queue. Messages in the queue will be sent

        The rest of the classes interact with the database (WarBotDB) to send
        and delete message requests. Messages in the message queue are sent to
        the authorized user as soon as the bot updates.
        """

        messages = self.bot.get_message_queue()
        self.bot.wipe_message_queue()
        self.m_queue = messages
    

    def handle_updates(self, updates):
        """Handles the messages that users send to the bot

        This method calls the rest of the handle methods.

        Parameters
        ----------
        updates : list<dict>
            List of updates from Telegram's API
        """

        updates_list = super(WarBotAdmin, self).handle_updates(updates)

        for update in updates_list:
            user_id = update['user_id']
            chat = update['chat']
            text = update['text']

            if user_id == self.auth_id:
                if self.ask_status == "NONE":
                    if text.startswith('/start'):
                        self.handle_start(chat)
                    elif text.startswith('/help'):
                        self.handle_help(chat)
                    elif text.startswith('/runoptin'):
                        self.handle_runoptin(chat)
                    elif text.startswith('/stopoptin'):
                        self.handle_stopoptin(chat)
                    elif text.startswith('/nextbattle'):
                        self.handle_nextbattle(chat)
                    elif text.startswith('/schedulebattle'):
                        self.handle_schedulebattle(chat, text.split()[1:])
                    elif text.startswith('/battlefrequency'):
                        self.handle_battlefrequency(chat)
                    elif text.startswith('/setbattlefrequency'):
                        self.handle_setbattlefrequency(chat, text.split()[1:])
                    elif text.startswith('/stopfrequency'):
                        self.handle_stopfrequency(chat)
                    elif text.startswith('/forcebattle'):
                        self.handle_forcebattle(chat, text.split()[1:])
                    elif text.startswith('/getfighters'):
                        self.handle_getfighters(chat)
                    elif text.startswith('/getfighter'):
                        self.handle_getfighter(chat, text.split()[1:])
                    elif text.startswith('/getcandidates'):
                        self.handle_getcandidates(chat)
                    elif text.startswith('/addfighter'):
                        self.handle_addfighter(chat, text.split()[1:])
                    elif text.startswith('/deletefighter'):
                        self.handle_deletefighter(chat, text.split()[1:])
                    elif text.startswith('/addcandidate'):
                        self.handle_addcandidate(chat, text.split()[1:])
                    elif text.startswith('/deletecandidate'):
                        self.handle_deletecandidate(chat, text.split()[1:])
                    elif text.startswith('/revive'):
                        self.handle_revive(chat, text.split()[1:])
                    elif text.startswith('/announcefighters'):
                        self.handle_announcefighters(chat)
                    elif text.startswith('/stopannouncefighters'):
                        self.handle_stopannouncefighters(chat)
                    elif text.startswith('/status'):
                        self.handle_status(chat)
                    elif text.startswith('/restart'):
                        self.handle_restart(chat, text.split()[1:])
                    else:
                        self.send_message("No option available. " \
                            + "Use /help to see all the commands.", chat)
                elif self.ask_status == "BUTTONS_GETFIGHTER":
                    self.handle_getfighter(chat, [text])
                elif self.ask_status == "BUTTONS_ADDFIGHTER":
                    self.handle_addfighter(chat, [text])
                elif self.ask_status == "BUTTONS_DELETEFIGHTER":
                    self.handle_deletefighter(chat, [text])
                elif self.ask_status == "BUTTONS_DELETECANDIDATE":
                    self.handle_deletecandidate(chat, [text])
                elif self.ask_status == "BUTTONS_REVIVE":
                    self.handle_revive(chat, [text])
            else:
                log.send_message("[TELEGRAM] WARNING at WarBotAdmin." \
                    + "handle_updates: request not authorized")
                self.handle_unauthorized(chat)
    

    def handle_help(self, chat):
        """Handles command /help

        Outputs help message.

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /help*
        
        Where * is any string
        """

        text = "*Bloomgogo War Bot* v1.0\n" \
            + "Created by: Miguel Ángel Fernández Gutiérrez (@mianfg)\n\n" \
            + "*Commands 👩‍💻👨‍💻*\n" \
            + "\n🔁 Sync:\n" \
            + "/runoptin · Allows Twitter users to add themselves to the "\
            + "candidates list 📬 mentioning the account\n" \
            + "/stopoptin · Stops previous functionality 📭\n" \
            + "\n⚔️ Batallas:\n" \
            + "/nextbattle · Information about when the next battle will " \
            + "happen ⏰\n" \
            + "/schedulebattle `[dd/mm/aaaa hh:mm | hh:mm | stop]` · " \
            + "Configures when next battle will happen ➡️⏰\n" \
            + "— `dd.mm.aaaa hh:mm` · Specify day and hour\n" \
            + "— `hh:mm` · Specify hour (if passed, tomorrow will be assigned)\n" \
            + "— `stop` · Stop battles 🛑⏰\n" \
            + "/battlefrequency · Returns frequency in which battles will be programmed ⏳\n" \
            + "/setbattlefrequency `[hours] [minutes]` · Configures frequency in which battles will be programmed ➡️⏳\n" \
            + "/stopfrequency · Stop automatic battles 🛑⏳\n" \
            + "/forcebattle `(winner) (defeated)` · Force a battle ➡️⚔️\n" \
            + "— `winner` · Fighter that will win the battle\n" \
            + "— `defeated` · Fighter that will lose the battle\n" \
            + "— leave blank to inquire a random battle\n" \
            + "**Important notice:** _when adding usernames, do not include @_\n" \
            + "\nℹ️ Information and status:\n" \
            + "/getfighters · Returns a complete list of fighters, including their state in the game 👥\n" \
            + "/getfighter `[username]` · Return all information about a fighter 👥\n" \
            + "/getcandidates · Return complete list of candidates 🕵️\n" \
            + "\n➡️👥 Alter users:\n" \
            + "/addfighter `[username](!)` · Add a fighter\n" \
            + "— `!` · Add the sign `!` to publish a tweet announcing that the user has been added to the game as fighter 🔔\n" \
            + "/deletefighter `[username]` · Delete a fighter (use with caution!)\n" \
            + "/addcandidate `[username]` · Add a candidate\n" \
            + "/deletecandidate `[username]` · Delete a candidate (use with caution!)\n" \
            + "/revive `[username]` · Revive a fighter 🧟\n" \
            + "\nInteractivity:\n" \
            + "/announcefighters · Automatically announce added fighters 🔔\n" \
            + "/stopannouncefighters · New fighters will be announced only if specified when adding 🛑🔔\n" \
            + "\n📈 Estado:\n" \
            + "/status · Retrieve bot status\n" \
            + "/restart `confirm` · Restart database"
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_help")
    

    def handle_unauthorized(self, chat):
        """Handles message sent by unauthorized user

        Sends a message to unauthorized user that interacts with the Telegram
        bot
        """

        text = "Hi! This bot has been designed to be manipulated by a restrained " \
            + "set of users. Talk with this bot's administrator for more info."
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_unauthorized")
    

    def handle_start(self, chat):
        """Handles command /starts

        Sends start message

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /send*
        
        Where * is any string
        """

        text = 'Welcome to *Bloomgogo War Bot*! Use /help for more information'
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_start")


    def handle_runoptin(self, chat):
        """Handles command /runoptin

        Runs opt-in (if it was not running before)

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /runoptin*
        
        Where * is any string
        """

        if self.bot.get_optin_running():
            text = "Opt-in was already in execution."
        else:
            self.bot.set_optin_running(True)
            text = "Opt-in successfully activated."
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_runoptin")


    def handle_stopoptin(self, chat):
        """Handles command /stopoptin

        Stops opt-in (if it was not stopped before)

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /stopoptin*
        
        Where * is any string
        """

        if not self.bot.get_optin_running():
            text = "Opt-in was already stopped."
        else:
            self.bot.set_optin_running(False)
            text = "Opt-in successfully deactivated."
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_stopoptin")
    

    def handle_nextbattle(self, chat):
        """Handles command /nextbattle

        Returns when next battle will happen.

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /nextbattle*
        
        Where * is any string
        """

        if self.bot.get_stop_next_battle():
            text = "There will be no next battle. Use /schedulebattle to configure it."
        else:
            date = self.bot.get_next_battle()
            text = "Next battle is scheduled to happen at: " \
                + "{}/{}/{} {:02d}:{:02d}".format(date.day, date.month, date.year, date.hour, date.minute)
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_nextbattle")


    def handle_schedulebattle(self, chat, attr):
        """Handles command /schedulebattle

        Schedules when next battle will happen

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /schedulebattle*
        
        Where * is any string. The use of this command is:

            /schedulebattle [dd/mm/aaaa hh:mm | hh:mm | stop]
                - dd/mm/aaaa hh:mm · exact date
                - hh:mm · next hour
                - stop · stops battle scheduling
        """

        input = ' '.join(attr)
        result = self.bot.set_next_battle(input)

        if input.startswith('stop'):
            text = "Next battle has successfully been stopped. "
            self.bot.set_stop_next_battle(True)
        else:
            if result:
                text = "Successfully modified. "
                self.bot.set_stop_next_battle(False)
            else:
                text = "Not modified, wrong format. You must insert the date in the format dd/mm/yy HH:MM. "

        if not self.bot.get_stop_next_battle():
            date = self.bot.get_next_battle()
            text += "Next battle is scheduled to happen at: " \
                + "{}/{}/{} {:02d}:{:02d}".format(date.day, date.month, date.year, date.hour, date.minute)
        else:
            text += "There will be no next battle."
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_schedulebattle")


    def handle_battlefrequency(self, chat):
        """Handles command /battlefrequency

        Returns battle frequency (the amount of time after last battle in which
        the next battle will be programmed, if this option is active)

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /battlefrequency*
        
        Where * is any string
        """

        if self.bot.get_stop_frequency():
            text = "Battle frequency was already stopped."
        else:
            f_h, f_m = self.bot.get_battle_frequency()
            text = "Battle frequency: {} hours {} minutes.".format(f_h, f_m)
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_battlefrequency")


    def handle_setbattlefrequency(self, chat, attr):
        """Handles command /setbattlefrequency

        Sets battle frequency. See `handle_battlefrequency` for more info.

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /setbattlefrequency*
        
        Where * is any string. The use of this command is:

            /setbattlefrequency [hours] [minutes]
            (pretty self-explanatory...)
        """

        if len(attr) == 2:
            try:
                h = int(attr[0])
                m = int(attr[1])
                if h >= 0 and m > 0 and m < 60:
                    self.bot.set_battle_frequency(attr[0], attr[1])
                    self.bot.set_stop_frequency(False)
                    text = "Battle frequency successfully set to {} hours {} minutes.".format(h, m)
                else:
                    text = "You must insert a valid amount of hours and minutes."
            except ValueError:
                text = "You must insert a valid amount of hours and minutes."
        else:
            text = "Wrong number of arguments."

        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_setbattlefrequency")


    def handle_stopfrequency(self, chat):
        """Handles command /stopfrequency

        Stops battle frequency. See `handle_battlefrequency` for more info.

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /stopfrequency*
        
        Where * is any string
        """

        if self.bot.get_stop_frequency():
            text = "Automatic battles were alredy stopped. To resume, use /setbattlefrequency."
        else:
            self.bot.set_stop_frequency(True)
            text = "Automatic battles have successfully been stopped. To resume, use /setbattlefrequency."
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_stopfrequency")


    def handle_forcebattle(self, chat, attr):
        """Handles command /forcebattle
        
        Forces a battle, either randomly or between two specific users

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /forcebattle*
        
        Where * is any string. The use of this command is:

            /forcebattle (winner) (defeated)
                - if there are not 2 args, it forces a random battle
                - if both winner and defeated, winner defeats defeated
        """

        if len(attr) >= 2:
            winner = attr[0]
            defeated = attr[1]
            result = self.bot.force_battle(winner, defeated)
            if result:
                text = 'Battle executed: *' + winner + '* has killed *' + defeated + '*'
            else:
                text = "Battle could not be executed."
        else:
            winner, defeated = self.bot.battle()
            if winner != None and defeated != None:
                text = 'Battle executed: *' + winner + '* has killed *' + defeated + '*'
            else:
                text = 'Battle could not be executed.'
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_forcebattle")
    

    def handle_getfighters(self, chat):
        """Handles command /getfighters

        Gives list of fighters

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /getfighters*
        
        Where * is any string
        """

        text = '👥 *List of fighters:*'
        i = 0
        for fighter in self.bot.get_fighters_extended():
            text += "\n" + str(i+1) + ". `" + fighter["username"] + "`"
            if not fighter["alive"]:
                text += " 💀"
            if not fighter["show"]:
                text += " 👻"
            i += 1
            if i%5 == 0:
                self.send_message(text, chat)
                text = ""
        if text != "":
            self.send_message(text, chat)
        
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_getfighters")


    def handle_getfighter(self, chat, attr):
        """Handles command /getfighter

        Gives all information about a specific fighter

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /getfighter*
        
        Where * is any string. The use of this command is:

            Option 1.
                /getfighter [username] *
                Will show info about username (rest of args ignored)
            Option 2.
                /getfighter
                Will prompt button GUI with all fighters, selecting one of them
                or sending a message with the name of a fighter will do the same
                effect as Option 1 with the same fighter
        """

        items = []
        for fighter in self.bot.get_fighters_extended():
            items.append(fighter["username"])

        if len(attr) > 0:            
            if attr[0] in items:
                text = "👤 Fighter: *" + attr[0] + "*\n" \
                    + "\Status: "
                fighter = next(item for item in self.bot.get_fighters_extended() if item["username"] == attr[0])
                if fighter["alive"]:
                    text += " alive"
                else:
                    text += " dead 💀"
                text += "\nHas killed: "
                if len(fighter["killed"]) > 0:
                    text += ', '.join("`" + fighter["killed"] + "`")
                else:
                    text += "no other fighters"
                text += "\nShow in list: "
                if fighter['show']:
                    text += "yes"
                else:
                    text += "no 👻"
            else:
                text = "Fighter not found."
            self.ask_status = "NONE"
            items = []
        else:
            text = "Insert the name of the fighter, or use the buttons prompted."
            self.ask_status = "BUTTONS_GETFIGHTER"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("Telegram - sent WarBotAdmin.handle_getfighter")
    

    def handle_getcandidates(self, chat):
        """Handles command /getcandidates

        Gives list of candidates

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /getcandidates*
        
        Where * is any string
        """

        text = '🕵️ *List of candidates:*'
        i = 0
        for candidate in self.bot.get_candidates():
            text += "\n" + str(i+1) + ". `" + candidate + "`"
            i += 1
            if i%5 == 0:
                self.send_message(text, chat)
                text = ""
        if text != "":
            self.send_message(text, chat)
                
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_getcandidates")

    
    def handle_addfighter(self, chat, attr):
        """Handles command /addfighter

        Adds one or more fighters

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /addfighter*
        
        Where * is any string. The use of this command is:

            Option 1.
                /addfighter [user1](!) [user2](!) ...
                Will add the users passed as args
            Option 2.
                /addfighter
                Will display button GUI with candidates (so candidates can be
                switched to fighters)
            
            Note: passing a ! next to the username will announce the user
        """

        items = []

        text = ""

        if len(attr) > 0:
            for username in attr:
                announce = False
                if "!" in username:
                    announce = True

                username = username.replace("!", "")

                result = self.bot.add_fighter(username)
                if result:
                    text += "Fighter *" + username + "* has been added. "
                    if self.bot.get_fighter_announce():
                        self.bot.add_announce_queue(username)
                        text += "Will be announced (by default, to deactivate use /stopannouncefighters).\n"
                    else:
                        if announce:
                            self.bot.add_announce_queue(username)
                            text += "Will be announced.\n"
                        else:
                            text += "\n"
                else:
                    text += "Fighter *"+username+"* is already on the fighters list.\n"
            
            self.ask_status = "NONE"
        else:
            items = self.bot.get_candidates()
            text = "Insert the name of the fighter to add, or use the buttons prompted."
            self.ask_status = "BUTTONS_ADDFIGHTER"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent handle_addfighter")


    def handle_deletefighter(self, chat, attr):
        """Handles command /deleteuser

        Deletes one or more fighters

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /deletefighter*
        
        Where * is any string. The use of this command is:

            Option 1.
                /deletefighter [user1] [user2] ...
                Will delete the fighters passed as args
            Option 2.
                /deletefighter
                Will display button GUI with fighters
        """

        items = []

        text = ""

        if len(attr) > 0:
            for username in attr:
                result = self.bot.delete_fighter(username)
                if result:
                    text += "Fighter *" + username + "* has been deleted.\n"
                else:
                    text += "Fighter *" + username + "* not found, therefore cannot be deleted.\n"

            self.ask_status = "NONE"
        else:
            items = self.bot.get_fighters()
            text = "Insert the name of the fighter to delete, or use the buttons prompted."
            self.ask_status = "BUTTONS_DELETEFIGHTER"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_deletefighter")

    
    def handle_addcandidate(self, chat, attr):
        """Handles command /addcandidate

        Adds one or more candidates

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /addcandidate*
        
        Where * is any string. The use of this command is:

            /addcandidate [user1] [user2] ...
            (again, nothing else to say)
        """

        text = ""

        if len(attr) > 0:
            for username in attr:
                result = self.bot.add_candidate(username)
                if result:
                    text += "Candidate *" + username + "* has been added.\n"
                else:
                    text += "Candidate *" + username + "* is already on the candidates list.\n"
        else:
            text = "You did not insert the candidate to add."
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_addcandidate")

    
    def handle_deletecandidate(self, chat, attr):
        """Handles command /deletecandidate

        Deletes one or more candidates

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /deletecandidate*
        
        Where * is any string. The use of this command is:

            Option 1.
                /deletecandidate [user1] [user2] ...
                Will delete the candidates passed as args
            Option 2.
                /deletecandidate
                Will display button GUI with candidates
        """

        items = []

        text = ""

        if len(attr) > 0:
            for username in attr:
                result = self.bot.delete_candidate(username)
                if result:
                    text += "Candidate *" + username + "* has been deleted.\n"
                else:
                    text += "Candidate *" + username + "* not found, therefore cannot be deleted.\n"

            self.ask_status = "NONE"
        else:
            items = self.bot.get_candidates()
            text = "Insert the name of the candidate to delete, or use the buttons prompted."
            self.ask_status = "BUTTONS_DELETECANDIDATE"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_deletecandidate")


    def handle_revive(self, chat, attr):
        """Handles command /revive
        
        Revives one or more fighters

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /revive*
        
        Where * is any string. The use of this command is:

            /revive [user1] [user2] ...
            (this is getting a little repetitive...)
        """

        items = []

        text = ""

        if len(attr) > 0:
            for username in attr:
                result = self.bot.revive_fighter(username)
                if result:
                    text = "Fighter *" + username + "* has been revived. 🧟\n"
                else:
                    text = "We could not revive *" + username + "*: not found or already alive.\n"

            self.ask_status = "NONE"
        else:
            items = self.bot.get_dead_fighters()
            text = "Insert the name of the fighter to revive, or use the buttons prompted."
            self.ask_status = "BUTTONS_REVIVE"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_revive")


    def handle_announcefighters(self, chat):
        """Handles command /announcefighters

        Activate announcing new fighters in Twitter automatically

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /announcefighters*
        
        Where * is any string
        """

        if self.bot.get_fighter_announce():
            text = "Fighters are being announced by default. To deactivate, use /stopannouncefighters."
        else:
            self.bot.set_fighter_announce(True)
            text = "From now on, new fighters will be announced by default."
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_announcefighters")
    

    def handle_stopannouncefighters(self, chat):
        """Handles command /stopannouncefighters

        Stops announcing new fighters in Twitter automatically

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /stopannouncefighters*
        
        Where * is any string
        """

        if not self.bot.get_fighter_announce():
            text = "Fighters weren't being announced already. Use /announcefighters to activate."
        else:
            self.bot.set_fighter_announce(False)
            text = "New users won't be announced by default."
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_stopannouncefighters")
    
    def handle_status(self, chat):
        """Handles command /status

        Sends back bot status

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /status*
        
        Where * is any string
        """

        text = "- Number of fighters: "
        text += str(len(self.bot.get_fighters()))
        text += " ({} 💀)\n".format(str(len(self.bot.get_dead_fighters())))
        text += "- Number of candidates: "
        text += str(len(self.bot.get_candidates()))
        text += "\n- Opt-in: "
        if self.bot.get_optin_running():
            text += "activated\n"
        else:
            text += "deactivated\n"
        text += "- Next battle: "
        if self.bot.get_stop_next_battle():
            text += "won't be\n"
        else:
            date = self.bot.get_next_battle()
            text += "{}/{}/{} {:02d}:{:02d}\n".format(date.day, date.month, date.year, date.hour, date.minute)
        text += "- Battle frequency: "
        f_h, f_m = self.bot.get_battle_frequency()
        text += "{} hours {} minutes\n".format(f_h, f_m)
        text += "- Frequency active: "
        if self.bot.get_stop_frequency():
            text += "no\n"
        else:
            text += "yes\n"
        text += "- Fighter announce: "
        if self.bot.get_fighter_announce():
            text += "automatic\n"
        else:
            text += "manual\n"
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_status")
    
    def handle_restart(self, chat, attr):
        """Handles command /restart

        Restarts database

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /restart*
        
        Where * is any string. The database will be restarted iff the comand
        is followed by the "confirm" keyword
        """

        do_restart = False

        if len(attr) > 0:
            if attr[0] == "confirm":
                do_restart = True
        
        if do_restart:
            result = self.bot.restart()
            if result:
                text = "Database has been restarted."
            else:
                text = "Database could not be restarted."
        else:
            text = "To do this, you must confirm this action. Have in " \
                + "consideration this action is irreversible. TO confirm, " \
                + "use /restart `confirm`."

        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_restart")
