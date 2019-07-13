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

# store dates
from datetime import datetime, timedelta
# numeric processing library
import numpy as np


class WarBot:
    """
    Class used to control war bot's data and requests

    ...

    Attributes
    ----------
    KILLFACTOR : float
        See `get_random_users()` for more info.
    db : WarBotDB
        WarBot's database client
    show_threshold : int
        See `get_random_users()` for more info.

    Methods
    -------

    Game methods:
        get_random_users()
            See function for more info.
        force_battle(winner : str, defeated : str) : bool
            Forces battle between winner and defeated, returns if battle could
            be done
        battle() : winner : str, defeated : str
            Makes a battle, returns winner and defeated users

    Database methods:
        get_users_extended() : dict
            Returns dictionary with all user's information, in WarBotDB's format
        get_users() : list<str>
            Returns list with all users
        get_alive_users() : list<str>
            Returns list with all alive users
        get_dead_users() : list<str>
            Returns list with all dead users
        get_candidates() : list<str>
            Returns list with all candidates
        add_user(username : str) : bool
            Adds user, returns if it could be added
        delete_user(username : str) : bool
            Deletes user, returns if it could be deleted
        add_candidate(username : str) : bool
            Adds candidate, returns if it could be added
        delete_candidate(username : str) : bool
            Deletes candidate, returns if it could be deleted
        revive_user(username : str) : bool
            Revives user, returns if it could be revived
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

    def __init__(self, database_route, database_filename):
        """
        Parameters
        ----------
        database_route : str
            Folder route to database file
        database_filename : str
            Filename of JSON database for WarBotDB
        """

        self.db = WarBotDB(database_route, database_filename)
        self.show_threshold = 100


    def get_random_users(self):
        """See below for more info.

        Returns
        -------
        Option 1:
            winner : str, defeated : str
                winner and defeated users, if they could be picked
        Option 2:
            None, None
                If no users could be picked (less than 2 users alive)

        How it works
        ------------
        This function picks out two random users from the list of alive users,
        with a ponderated probability per user, that is calculated using the
        formula:

            PROB(user) = 1 + KILLFACTOR * number_of_users_killed_by(user)

        Then, the vector of alive users' probability is normalized so that it
        sums up to 1, setting the final probabilities.
        """
        
        users = []
        weight = []
        for user in self.db.get_users():
            if user["alive"]:
                users.append(user["username"])
                w = 1 + len(user["killed"]) * self.KILLFACTOR
                weight.append(w)
                
        if len(weight) >= 2:
            norm = [float(i)/sum(weight) for i in weight]

            random_result = np.random.choice(users, size=2, replace=False, \
                p=norm)

            winner = random_result[0]
            defeated = random_result[1]

            return winner, defeated
        else:
            return None, None


    def force_battle(self, winner, defeated):
        if winner in self.get_users() and defeated in self.get_users():
            self.db.insert_user_kill(winner, defeated)
            self.db.change_user_alive(defeated, False)
            self.add_battle_queue(winner, defeated)

            if len(self.get_alive_users()) >= self.show_threshold:
                self.db.change_user_show(defeated, False)

            return True
        else:
            return False


    def battle(self):
        winner, defeated = self.get_random_users()
        self.force_battle(winner, defeated)
        return winner, defeated


    def get_users_extended(self):
        return self.db.get_users()

    def get_users(self):
        users = []
        for user in self.db.get_users():
            users.append(user["username"])
        return users

    def get_alive_users(self):
        alive = list(item["username"] for item in self.get_users_extended() \
            if item["alive"])
        return alive
    
    def get_dead_users(self):
        dead = list(item["username"] for item in self.get_users_extended() \
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

    def add_user(self, username):
        if username in self.get_users():
            return False
        else:
            self.db.insert_user(username)
            return True
    
    def delete_user(self, username):
        if username in self.get_users():
            self.db.delete_user(username)
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
    
    def revive_user(self, username):
        if username in self.get_users():
            user = next(item for item in self.get_users_extended() \
                if item["username"] == username)
            if not user["alive"]:
                self.db.change_user_alive(username, True)
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
    
    def get_user_announce(self):
        return self.db.get_user_announce()

    def set_user_announce(self, b):
        self.db.update_user_announce(b)

    def get_message_queue(self):
        return self.db.get_message_queue()
    
    def wipe_message_queue(self):
        return self.db.delete_message_queue()
    
    def add_message_queue(self, message):
        return self.db.add_message_queue(message)

    def restart(self):
        return self.db.restart()
