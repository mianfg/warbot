#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WarBot
======

Main controller for Bloomgogo War Bot.

Note
----
Pay attention to the KILLFACTOR and threshold attributes.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



# application imports
from database import WarBotDB
from vars import route

# store dates
from datetime import datetime, timedelta
# numeric processing library
import numpy as np
import random


class WarBot:
    """
    Class used to control war bot's data and requests

    ...

    Attributes
    ----------
    KILLFACTOR : float
        See `get_random_fighters()` for more info.
    db : WarBotDB
        WarBot's database client
    show_threshold : int
        See `get_random_fighters()` for more info.

    Methods
    -------

    Game methods:
        get_random_fighters()
            See function for more info.
        force_battle(winner : str, defeated : str) : bool
            Forces battle between winner and defeated, returns if battle could
            be done
        battle() : winner : str, defeated : str
            Makes a battle, returns winner and defeated fighters

    Database methods:
        get_fighters_extended() : dict
            Returns dictionary with all fighter's information, in WarBotDB's format
        get_fighters() : list<str>
            Returns list with all fighters
        get_alive_fighters() : list<str>
            Returns list with all alive fighters
        get_dead_fighters() : list<str>
            Returns list with all dead fighters
        get_candidates() : list<str>
            Returns list with all candidates
        add_fighter(username : str) : bool
            Adds fighter, returns if it could be added
        delete_fighter(username : str) : bool
            Deletes fighter, returns if it could be deleted
        add_candidate(username : str) : bool
            Adds candidate, returns if it could be added
        delete_candidate(username : str) : bool
            Deletes candidate, returns if it could be deleted
        revive_fighter(username : str) : bool
            Revives fighter, returns if it could be revived
        restart : bool
            Restarts database
        
    Database variable methods:
        For variables:
            set_[name_of_variable]([value])
                Sets [name_of_variable] to [value]
            get_[name_of_variable]()
                Returns [name_of_variable]
        For queues:
            add_[name_of_queue]([item])
                Adds [item] to [name_of_queue]
            get_[name_of_queue]()
                Returns queue
            wipe_[name_of_queue]()
                Deletes queue
    """

    KILLFACTOR = 0.5

    def __init__(self, database_route, database_filename, \
        phrases_route, phrases_filename):
        """
        Parameters
        ----------
        database_route : str
            Folder route to database file
        database_filename : str
            Filename of JSON database for WarBotDB
        phrases_route : str
            Folder route to phrases file
        phrases_filename : str
            Filename of txt file containing battle phrases
        """

        self.db = WarBotDB(database_route, database_filename)
        self.phrases_file = route.paste(phrases_route, phrases_filename)
        self.show_threshold = 100


    def get_random_fighters(self):
        """See below for more info.

        Returns
        -------
        Option 1:
            winner : str, defeated : str
                winner and defeated fighters, if they could be picked
        Option 2:
            None, None
                If no fighters could be picked (less than 2 fighters alive)

        How it works
        ------------
        This function picks out two random fighters from the list of alive fighters,
        with a ponderated probability per fighter, that is calculated using the
        formula:

            PROB(fighter) = 1 + KILLFACTOR * number_of_fighters_killed_by(fighter)

        Then, the vector of alive fighters' probability is normalized so that it
        sums up to 1, setting the final probabilities.
        """
        
        fighters = []
        weight = []
        for fighter in self.db.get_fighters():
            if fighter["alive"]:
                fighters.append(fighter["username"])
                w = 1 + len(fighter["killed"]) * self.KILLFACTOR
                weight.append(w)
                
        if len(weight) >= 2:
            norm = [float(i)/sum(weight) for i in weight]

            random_result = np.random.choice(fighters, size=2, replace=False, \
                p=norm)

            winner = random_result[0]
            defeated = random_result[1]

            return winner, defeated
        else:
            return None, None


    def force_battle(self, winner, defeated):
        if winner in self.get_fighters() and defeated in self.get_fighters():
            self.db.insert_fighter_kill(winner, defeated)
            self.db.change_fighter_alive(defeated, False)
            self.add_battle_queue(winner, defeated)

            if len(self.get_alive_fighters()) >= self.show_threshold:
                self.db.change_fighter_show(defeated, False)

            return True
        else:
            return False


    def battle(self):
        winner, defeated = self.get_random_fighters()
        self.force_battle(winner, defeated)
        return winner, defeated

    
    def generate_battle_text(self, winner, defeated):
        phrases = []
        with open(self.phrases_file) as f:
            for line in f:
                line = line.replace("\n", "")
                if line != "" and (not line.startswith('#')):
                    phrases.append(line)

        phrase = random.choice(phrases)
        phrase = phrase.replace("{{WINNER}}", winner)
        phrase = phrase.replace("{{DEFEATED}}", defeated)
        return "☠️ " + phrase


    def get_fighters_extended(self):
        return self.db.get_fighters()

    def get_fighters(self):
        fighters = []
        for fighter in self.db.get_fighters():
            fighters.append(fighter["username"])
        return fighters

    def get_alive_fighters(self):
        alive = list(item["username"] for item in self.get_fighters_extended() \
            if item["alive"])
        return alive
    
    def get_dead_fighters(self):
        dead = list(item["username"] for item in self.get_fighters_extended() \
            if not item["alive"])
        return dead

    def get_candidates(self):
        candidates = []
        for candidate in self.db.get_candidates():
            candidates.append(candidate["username"])
        return candidates

    def add_announce_queue(self, username):
        self.db.add_announce_queue(username)
    
    def wipe_announce_queue(self):
        self.db.delete_announce_queue()
    
    def get_announce_queue(self):
        return self.db.get_announce_queue()

    def add_battle_queue(self, winner, defeated):
        self.db.add_battle_queue(winner, defeated)
    
    def wipe_battle_queue(self):
        self.db.delete_battle_queue()
    
    def get_battle_queue(self):
        return self.db.get_battle_queue()

    def add_fighter(self, username):
        if username in self.get_fighters():
            return False
        else:
            self.db.insert_fighter(username)
            return True
    
    def delete_fighter(self, username):
        if username in self.get_fighters():
            self.db.delete_fighter(username)
            return True
        else:
            return False

    def add_candidate(self, username):
        if username in self.get_candidates():
            return False
        else:
            self.db.insert_candidate(username)
            return True
    
    def delete_candidate(self, username):
        if username in self.get_candidates():
            self.db.delete_candidate(username)
            return True
        else:
            return False
    
    def revive_fighter(self, username):
        if username in self.get_fighters():
            fighter = next(item for item in self.get_fighters_extended() \
                if item["username"] == username)
            if not fighter["alive"]:
                self.db.change_fighter_alive(username, True)
                return True
            else:
                return False
        else:
            return False

    def set_next_battle(self, input):
        could_assign = True

        try:
            date = datetime.strptime(input, '%d/%m/%Y %H:%M')
        except:
            could_assign = False
        
        if could_assign:
            self.db.update_next_battle(date)
            return could_assign
        
        try:
            hour = datetime.strptime(input, '%H:%M')
            could_assign = True
        except:
            could_assign = False
        
        if could_assign:
            now = datetime.now()

            # if hour assigned has not passed, assign to the current day;
            # otherwise, asign to tomorrow
            if hour.hour < now.hour:
                date = now + timedelta(days=1)
            elif hour.hour == now.hour:
                if hour.minute < now.minute:
                    date = now + timedelta(days=1)
                else:
                    date = now
            else:
                date = now
            
            date = date.replace(hour=hour.hour, minute=hour.minute)

            self.db.update_next_battle(date)
        
        return could_assign

    def get_optin_running(self):
        return self.db.get_optin_running()
    
    def set_optin_running(self, b):
        self.db.update_optin_running(b)
    
    def get_stop_next_battle(self):
        return self.db.get_stop_next_battle()
    
    def get_next_battle(self):
        return self.db.get_next_battle()

    def set_stop_next_battle(self, b):
        self.db.update_stop_next_battle(b)
    
    def get_stop_frequency(self):
        return self.db.get_stop_frequency()
    
    def set_stop_frequency(self, b):
        self.db.update_stop_frequency(b)
    
    def get_battle_frequency(self):
        return self.db.get_battle_frequency()
    
    def set_battle_frequency(self, hours, minutes):
        return self.db.update_battle_frequency(hours, minutes)
    
    def get_fighter_announce(self):
        return self.db.get_fighter_announce()

    def set_fighter_announce(self, b):
        self.db.update_fighter_announce(b)

    def get_message_queue(self):
        return self.db.get_message_queue()
    
    def wipe_message_queue(self):
        return self.db.delete_message_queue()
    
    def add_message_queue(self, message):
        return self.db.add_message_queue(message)

    def restart(self):
        return self.db.restart()