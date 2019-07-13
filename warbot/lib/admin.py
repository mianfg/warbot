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
    handle_getusers(chat)
        Handles command /getusers
    handle_getuser(chat, attr)
        Handles command /getuser
    handle_getcandidates(chat)
        Handles command /getcandidates
    handle_adduser(chat, attr)
        Handles command /adduser
    handle_deleteuser(chat, attr)
        Handles command /deleteuser
    handle_addcandidate(chat, attr)
        Handles command /addcandidate
    handle_deletecandidate(chat, attr)
        Handles command /deletecandidate
    handle_revive(chat, attr)
        Handles command /revive
    handle_announceusers(chat)
        Handles command /announceusers
    handle_stopannounceusers(chat)
        Handles command /stopannounceusers
    handle_status(chat)
        Handles command /status
    handle_restart(chat, attr)
        Handles command /restart

    """


    def __init__(self, telegram_token, telegram_sleep_time, \
        database_route, database_filename, auth_id):
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
        auth_id : int
            Telegram ID of authorized user
        """

        super(WarBotAdmin, self).__init__(telegram_token, telegram_sleep_time)
        self.bot = WarBot(database_route, database_filename)
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
                    elif text.startswith('/getusers'):
                        self.handle_getusers(chat)
                    elif text.startswith('/getuser'):
                        self.handle_getuser(chat, text.split()[1:])
                    elif text.startswith('/getcandidates'):
                        self.handle_getcandidates(chat)
                    elif text.startswith('/adduser'):
                        self.handle_adduser(chat, text.split()[1:])
                    elif text.startswith('/deleteuser'):
                        self.handle_deleteuser(chat, text.split()[1:])
                    elif text.startswith('/addcandidate'):
                        self.handle_addcandidate(chat, text.split()[1:])
                    elif text.startswith('/deletecandidate'):
                        self.handle_deletecandidate(chat, text.split()[1:])
                    elif text.startswith('/revive'):
                        self.handle_revive(chat, text.split()[1:])
                    elif text.startswith('/announceusers'):
                        self.handle_announceusers(chat)
                    elif text.startswith('/stopannounceusers'):
                        self.handle_stopannounceusers(chat)
                    elif text.startswith('/status'):
                        self.handle_status(chat)
                    elif text.startswith('/restart'):
                        self.handle_restart(chat, text.split()[1:])
                    else:
                        self.send_message("Ninguna opción disponible. " \
                            + "Usa /help para ver todos los comandos.", chat)
                elif self.ask_status == "BUTTONS_GETUSER":
                    self.handle_getuser(chat, [text])
                elif self.ask_status == "BUTTONS_ADDUSER":
                    self.handle_adduser(chat, [text])
                elif self.ask_status == "BUTTONS_DELETEUSER":
                    self.handle_deleteuser(chat, [text])
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
            + "Diseñado por: Miguel Ángel Fernández Gutiérrez (@mianfg)\n\n" \
            + "*Comandos 👩‍💻👨‍💻*\n" \
            + "\n🔁 Sincronización:\n" \
            + "/runoptin · Permite a los usuarios de Twitter añadirse a la " \
            + "lista de candidatos 📬 mencionando a la cuenta\n" \
            + "/stopoptin · Paraliza la funcionalidad anterior 📭\n" \
            + "\n⚔️ Batallas:\n" \
            + "/nextbattle · Información de cuándo tendrá lugar la próxima " \
            + "batalla ⏰\n" \
            + "/schedulebattle `[dd/mm/aaaa hh:mm | hh:mm | stop]` · " \
            + "Configura cuándo tendrá lugar la próxima batalla ➡️⏰\n" \
            + "— `dd.mm.aaaa hh:mm` · Especificar el día y hora\n" \
            + "— `hh:mm` · Especificar la hora (si ha pasado se tomará el día siguiente)\n" \
            + "— `stop` · Parar batallas 🛑⏰\n" \
            + "/battlefrequency · Devuelve la frecuencia a la que se programarán las batallas ⏳\n" \
            + "/setbattlefrequency `[hours] [minutes]` · Configura la frecuencia a la que se programarán las batallas ➡️⏳\n" \
            + "/stopfrequency · Para las batallas automáticas 🛑⏳\n" \
            + "/forcebattle `(winner) (defeated)` · Forzar una batalla entre dos usuarios ➡️⚔️\n" \
            + "— `winner` · Usuario que ganará la batalla\n" \
            + "— `defeated` · Usuario que perderá la batalla\n" \
            + "— dejar en blanco para efectuar batalla aleatoria\n" \
            + "**Nota importante:** _al insertar usuarios, no incluir el @_\n" \
            + "\nℹ️ Información y estado:\n" \
            + "/getusers · Devuelve una lista completa de usuarios, junto a su estado en el juego 👥\n" \
            + "/getuser `[username]` · Devuelve información completa sobre un usuario 👥\n" \
            + "/getcandidates · Devuelve una lista completa de candidatos 🕵️\n" \
            + "\n➡️👥 Modificación de usuarios:\n" \
            + "/adduser `[username] (announce)` · Añade un usuario\n" \
            + "— `announce` · Añadir el string `announce` para publicar un tweet anunciando que el usuario ha sido añadido al juego 🔔\n" \
            + "/deleteuser `[username]` · Elimina un usuario (¡usar con precaución!)\n" \
            + "/addcandidate `[username]` · Añade un candidato\n" \
            + "/deletecandidate `[username]` · Elimina un candidato (¡usar con precaución!)\n" \
            + "/revive `[username]` · Revive un usuario 🧟\n" \
            + "\nInteractividad:\n" \
            + "/announceusers · Anunciar usuarios añadidos automáticamente 🔔\n" \
            + "/stopannounceusers · Sólo se anunciarán usuarios con atributo de anunciado 🛑🔔\n" \
            + "\n📈 Estado:\n" \
            + "/status · Recibir el estado del bot\n" \
            + "/restart `confirm` · Reiniciar base de datos"
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_help")
    

    def handle_unauthorized(self, chat):
        """Handles message sent by unauthorized user

        Sends a message to unauthorized user that interacts with the Telegram
        bot
        """

        text = "¡Buenas! Este bot ha sido diseñado para ser manipulado por un conjunto " \
            + "seleccionado de usuarios. Hable con el administrador de este bot para más información."
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

        text = '¡Bienvenido a *Bloomgogo War Bot*! Use el comando /help para más información'
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
            text = "El opt-in ya estaba ejecutándose."
        else:
            self.bot.set_optin_running(True)
            text = "El opt-in ha sido activado."
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
            text = "El opt-in se encontraba parado."
        else:
            self.bot.set_optin_running(False)
            text = "El opt-in ha sido desactivado."
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
            text = "No habrá próxima batalla. Use /schedulebattle para configurarla."
        else:
            date = self.bot.get_next_battle()
            text = "La próxima batalla se producirá a las: " \
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
            text = "Se ha parado la siguiente batalla. "
            self.bot.set_stop_next_battle(True)
        else:
            if result:
                text = "Modificado correctamente. "
                self.bot.set_stop_next_battle(False)
            else:
                text = "No modificado, el formato era erróneo. Debe insertar la fecha en el formato dd/mm/aa HH:MM. "

        if not self.bot.get_stop_next_battle():
            date = self.bot.get_next_battle()
            text += "La próxima batalla se producirá a las: " \
                + "{}/{}/{} {:02d}:{:02d}".format(date.day, date.month, date.year, date.hour, date.minute)
        else:
            text += "No habrá próxima batalla."
        
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
            text = "La frecuencia de batalla se encuentra pausada."
        else:
            f_h, f_m = self.bot.get_battle_frequency()
            text = "Frecuencia de batalla: {} horas y {} minutos.".format(f_h, f_m)
        
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
                    text = "Frecuencia de batalla cambiada a {} horas y {} minutos.".format(h, m)
                else:
                    text = "Debe insertar unas horas y minutos válidos."
            except ValueError:
                text = "Debe insertar unas horas y minutos válidos."
        else:
            text = "Número de argumentos incorrecto."

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
            text = "Las batallas automáticas se encontraban pausadas. Para reanudar, use /setbattlefrequency."
        else:
            self.bot.set_stop_frequency(True)
            text = "Se han pausado las batallas automáticas. Para reanudar, use /setbattlefrequency."
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
                text = 'Batalla efectuada: *' + winner + '* ha matado a *' + defeated + '*'
            else:
                text = "La batalla no pudo efectuarse."
        else:
            winner, defeated = self.bot.battle()
            if winner != None and defeated != None:
                text = 'Batalla efectuada: *' + winner + '* ha matado a *' + defeated + '*'
            else:
                text = 'La batalla no pudo efectuarse.'
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_forcebattle")
    

    def handle_getusers(self, chat):
        """Handles command /getusers

        Gives list of users

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /getusers*
        
        Where * is any string
        """

        text = '👥 *Lista de usuarios:*'
        i = 1
        for user in self.bot.get_users_extended():
            text += "\n" + str(i) + ". " + user["username"]
            if not user["alive"]:
                text += " 💀"
            if not user["show"]:
                text += " 👻"
            i += 1
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_getusers")


    def handle_getuser(self, chat, attr):
        """Handles command /getuser

        Gives all information about a specific user

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /getuser*
        
        Where * is any string. The use of this command is:

            Option 1.
                /getuser [username] *
                Will show info about username (rest of args ignored)
            Option 2.
                /getuser
                Will prompt button GUI with all users, selecting one of them
                or sending a message with the name of a user will do the same
                effect as Option 1 with the same user
        """

        items = []
        for user in self.bot.get_users_extended():
            items.append(user["username"])

        if len(attr) > 0:            
            if attr[0] in items:
                text = "👤 Usuario: *" + attr[0] + "*\n" \
                    + "\nEstado: "
                user = next(item for item in self.bot.get_users_extended() if item["username"] == attr[0])
                if user["alive"]:
                    text += " vivo"
                else:
                    text += " muerto 💀"
                text += "\nHa matado a: "
                if len(user["killed"]) > 0:
                    text += ', '.join(user["killed"])
                else:
                    text += "ningún usuario"
                text += "\nMostrar en lista: "
                if user['show']:
                    text += "sí"
                else:
                    text += "no 👻"
            else:
                text = "Usuario no encontrado."
            self.ask_status = "NONE"
            items = []
        else:
            text = "Inserta el nombre del usuario o usa el desplegable para seleccionarlo."
            self.ask_status = "BUTTONS_GETUSER"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("Telegram - sent WarBotAdmin.handle_getuser")
    

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

        text = '🕵️ *Lista de candidatos:*'
        i = 1
        for candidate in self.bot.get_candidates():
            text += "\n" + str(i) + ". " + candidate
            i += 1
        self.send_message(text, chat)
    
    def handle_adduser(self, chat, attr):
        """Handles command /adduser

        Adds one or more users

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /adduser*
        
        Where * is any string. The use of this command is:

            Option 1.
                /adduser [user1] [user2] ...
                Will add the users passed as args
            Option 2.
                /adduser
                Will display button GUI with candidates (so candidates can be
                switched to users)
        """

        items = []

        text = ""

        if len(attr) > 0:
            for username in attr:
                result = self.bot.add_user(username)
                if result:
                    text += "Se ha insertado el usuario *" + username + "*. "
                    if self.bot.get_user_announce():
                        self.bot.add_announce_queue(username)
                        text += "Será anunciado (activado por defecto, para desactivar use /stopannounceusers).\n"
                    else:
                        if len(attr) > 1:
                            if attr[1] == "announce":
                                self.bot.add_announce_queue(username)
                                text += "Será anunciado.\n"
                            else:
                                text += "\n"
                else:
                    text += "El usuario *"+username+"* ya se encontraba en la lista de usuarios.\n"
            
            self.ask_status = "NONE"
        else:
            items = self.bot.get_candidates()
            text = "Inserta el nombre del usuario a añadir, o usa el desplegable para añadir desde candidatos."
            self.ask_status = "BUTTONS_ADDUSER"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent handle_adduser")


    def handle_deleteuser(self, chat, attr):
        """Handles command /deleteuser

        Deletes one or more users

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /deleteuser*
        
        Where * is any string. The use of this command is:

            Option 1.
                /deleteuser [user1] [user2] ...
                Will delete the users passed as args
            Option 2.
                /deleteuser
                Will display button GUI with users
        """

        items = []

        text = ""

        if len(attr) > 0:
            for username in attr:
                result = self.bot.delete_user(username)
                if result:
                    text += "Se ha eliminado el usuario *" + username + "*.\n"
                else:
                    text += "El usuario *" + username + "* no estaba en la lista de usuarios, y por tanto no puede eliminarse.\n"

            self.ask_status = "NONE"
        else:
            items = self.bot.get_users()
            text = "Inserta el nombre del usuario que desea eliminar, o usa el desplegable."
            self.ask_status = "BUTTONS_DELETEUSER"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_deleteuser")

    
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
                    text += "Se ha insertado el candidato *" + username + "*.\n"
                else:
                    text += "El candidato *" + username + "* ya se encontraba en la lista de candidatos.\n"
        else:
            text = "No has insertado el candidato a añadir."
        
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
                    text += "Se ha eliminado el candidato *" + username + "*.\n"
                else:
                    text += "El candidato *" + username + "* no estaba en la lista de candidatos, y por tanto no puede eliminarse.\n"

            self.ask_status = "NONE"
        else:
            items = self.bot.get_candidates()
            text = "Inserta el nombre del candidato que desea eliminar, o usa el desplegable."
            self.ask_status = "BUTTONS_DELETECANDIDATE"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_deletecandidate")


    def handle_revive(self, chat, attr):
        """Handles command /revive
        
        Revives one or more users

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
                result = self.bot.revive_user(username)
                if result:
                    text = "Has revivido a *" + username + "*. 🧟\n"
                else:
                    text = "No hemos podido revivir a *" + username + "* porque no estaba en la lista de usuarios o ya estaba vivo.\n"

            self.ask_status = "NONE"
        else:
            items = self.bot.get_dead_users()
            text = "Inserta el nombre del usuario que desea revivir, o usa el desplegable."
            self.ask_status = "BUTTONS_REVIVE"

        keyboard = self.build_keyboard(items)
        self.send_message(text, chat, keyboard)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_revive")


    def handle_announceusers(self, chat):
        """Handles command /announceusers

        Activate announcing new users in Twitter automatically

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /announceusers*
        
        Where * is any string
        """

        if self.bot.get_user_announce():
            text = "Los usuarios ya se están anunciando por defecto. Para desactivarlo, use /stopannounceusers."
        else:
            self.bot.set_user_announce(True)
            text = "De ahora en adelante, los nuevos usuarios se anunciarán por defecto."
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_announceusers")
    

    def handle_stopannounceusers(self, chat):
        """Handles command /stopannounceusers

        Stops announcing new users in Twitter automatically

        Command call
        ------------
        This function is called whenever the authorized user sends a message
        to the Telegram bot of the form:

            /stopannounceusers*
        
        Where * is any string
        """

        if not self.bot.get_user_announce():
            text = "Los usuarios ya no se anunciaban por defecto. Use /announceusers para activarlo."
        else:
            self.bot.set_user_announce(False)
            text = "No se anunciarán los nuevos usuarios."
        
        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_stopannounceusers")
    
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

        text = "- Opt-in: "
        if self.bot.get_optin_running():
            text += "activado\n"
        else:
            text += "desactivado\n"
        text += "- Próxima batalla: "
        if self.bot.get_stop_next_battle():
            text += "no habrá\n"
        else:
            date = self.bot.get_next_battle()
            text += "{}/{}/{} {:02d}:{:02d}\n".format(date.day, date.month, date.year, date.hour, date.minute)
        text += "- Frecuencia de batalla: "
        f_h, f_m = self.bot.get_battle_frequency()
        text += "{} horas, {} minutos\n".format(f_h, f_m)
        text += "- Frecuencia activada: "
        if self.bot.get_stop_frequency():
            text += "no\n"
        else:
            text += "sí\n"
        text += "- Anuncio de usuarios: "
        if self.bot.get_user_announce():
            text += "automático\n"
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
                text = "La base de datos ha sido reiniciada."
            else:
                text = "La base de datos no pudo ser reiniciada."
        else:
            text = "Para poder realizar esta acción, debe confirmarla. Tenga " \
                + "en cuenta que esta acción no podrá recuperarse. Para " \
                + "confirmar, use /restart `confirm`."

        self.send_message(text, chat)
        log.send_message("[TELEGRAM] sent WarBotAdmin.handle_restart")
