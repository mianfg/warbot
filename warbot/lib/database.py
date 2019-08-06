#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WarBotDB
========

This module controls the database, in TinyDB.

"""

__author__      = "Miguel Ángel Fernández Gutiérrez (@mianfg)"
__copyright__   = "Copyright 2019, Bloomgogo"
__credits__     = ["Miguel Ángel Fernández Gutiérrez"]
__license__     = "GPL"
__version__     = "1.0"
__mantainer__   = "Miguel Ángel Fernández Gutiérrez"
__email__       = "mianfg@bloomgogo.com"
__status__      = "Production"



from tinydb import TinyDB, Query, where
from datetime import datetime
from vars import log, route

import os


class WarBotDB:
    """
    Class used to control the WarBot database

    ...

    Database model
    --------------
    This is the index of the database


    - candidates: Table to store candidates
        {'username': str}
        - username: username of candidate
    - fighters: Table to store fighters
        {'username': str, 'alive': bool, 'killed': list<str>, 'show': bool}
        - username: username of user
        - alive: is username alive
        - killed: list of fighters that fighter has killed
        - show: show in battle update list or not
    - vars: Table to store variables
        {'varname': str, 'value': _}
        - varname: name of the variable
        - value: value of the variable
        This stores the following variables:
            - last_seen_id : int
                Last seen ID for Telegram message reception
            - optin_running : bool
                Whether opt-in is active or not
            - next_battle_year : int
                Year of next battle
            - next_battle_month : int
                Month of next battle
            - next_battle_day : int
                Day of next battle
            - next_battle_hour : int
                Hour of next battle
            - next_battle_minute : int
                Minute of next battle
            - battle_frequency_hours : int
                Hours of battle frequency
            - battle_frequency_minutes : int
                Minutes of battle frequency
            - stop_frequency : bool
                If true, battle frequency is ignored
            - stop_next_battle : bool
                If true, no next battle will be programmed
            - fighter_announce : bool
                If true, fighters will be announced automatically
            - announce_queue : list<>
                Queue for fighter announce
            - battle_queue : list<> #WIP
                Queue for battle announce
            - message_queue : list<>
                Queue for Telegram bot feedback

    Attributes
    ----------
    db : TinyDB
        TinyDB main database
    db_candidates : TinyDB.table
        TinyDB database table for candidates
    db_fighters : TinyDB.table
        TinyDB database table for fighters
    db_vars : TinyDB.table
        TinyDB database table for variables
    
    Methods
    -------
    From fighters and candidates tables
        insert_fighter(username, alive=True)
            Inserts fighter in database
        insert_candidate(username)
            Inserts candidate in database
        insert_fighter_kill(username, killed)
            Insert kill in database: username killed killed
        change_fighter_alive(username, alive)
            Change username's life status to alive
        change_fighter_show(username, show)
            Change username's show status to show
        delete_fighter(username)
            Delete fighter from database
        delete_candidate(username)
            Delete candidate from database
        get_fighters() : list<str>
            Gets all fighters
        get_candidates() : list<str>
            Gets all candidates
    
    From vars table
        setup_vars()
            Sets up variables from vars table (generates them if not present)
        For variables:
            get_[name_of_variable]()
                Returns [name_of_variable]'s value
            update_[name_of_variable]([new_value])
                Updates [name_of_variable] to [new_value]
        For queues:
            get_[name_of_queue]()
                Returns queue's list
            update_[name_of_queue]([new_list])
                Update's queue to [new_list]
            add_[name_of_queue]([item])
                Appends [item] to queue
            delete_[name_of_queue]()
                Resets queue to empty list
    
    restart
        Wipes out all data from database, creates a new one
    """

    def __init__(self, database_route, database_filename):
        """
        Parameters
        ----------
        database_route : str
            Folder route to database file
        database_filename : str
            Filename of JSON database for TinyDB
        """

        self.db_route = route.paste(database_route, database_filename)
        self.db = TinyDB(self.db_route)
        self.db_candidates = self.db.table('candidates', cache_size=0)
        self.db_fighters = self.db.table('fighters', cache_size=0)
        self.db_vars = self.db.table('vars', cache_size=0)
        self.setup_vars()


    def insert_fighter(self, username, alive=True):
        # Check if fighter is already in the database
        User = Query()
        if len(self.db_fighters.search(User.username == username)) > 0:
            log.send_message("[DATABASE] Insertion error: fighter " + username + " is already on the database")
        else:
            new_fighter = {'username': username, 'alive': alive, 'killed': [], 'show': True}
            self.db_fighters.insert(new_fighter)
            log.send_message("[DATABASE] Insertion: fighter " + username + " added to the database")

        # Delete from candidates
        self.delete_candidate(username)


    def insert_candidate(self, username):
        # Check if candidate is already in the database
        Candidate = Query()
        if len(self.db_candidates.search(Candidate.username == username)) > 0:
            log.send_message("[DATABASE] Insertion error: Candidate " + username + " is already on the database")
        else:
            new_candidate = {'username': username}
            self.db_candidates.insert(new_candidate)
            log.send_message("[DATABASE] Insertion: Candidate " + username + " added to the database")


    def insert_fighter_kill(self, username, killed):
        User = Query()
        new_killed = self.db_fighters.search(User.username == username)
        if len(new_killed) > 0:
            new_killed = new_killed[0]['killed']
        else:
            log.send_message("[DATABASE] Update error: No ocurrences of " + username + " found trying to kill " + killed)
        if not killed in new_killed:
            new_killed.append(killed)
        
        self.db_fighters.update({'killed': new_killed}, User.username == username)
        log.send_message("[DATABASE] Update: " + username + " killed " + killed)


    def change_fighter_alive(self, username, alive):
        User = Query()
        self.db_fighters.update({'alive': alive}, User.username == username)
        if alive:
            log.send_message("[DATABASE] Update: " + username + " is now alive")
        else:
            log.send_message("[DATABASE] Update: " + username + " is now dead")


    def change_fighter_show(self, username, show):
        User = Query()
        self.db_fighters.update({'show': show}, User.username == username)
        if show:
            log.send_message("[DATABASE] Update: " + username + " is now showed")
        else:
            log.send_message("[DATABASE] Update: " + username + " is now hidden")


    def delete_fighter(self, username):
        self.db_fighters.remove(where('username') == username)
        log.send_message("[DATABASE] Removed: fighter " + username)


    def delete_candidate(self, username):
        self.db_candidates.remove(where('username') == username)
        log.send_message("[DATABASE] Removed: candidate " + username)


    def get_fighters(self):
        return self.db_fighters.all()


    def get_candidates(self):
        return self.db_candidates.all()


    def setup_vars(self):
        Vars = Query()
        if len(self.db_vars.search(Vars.varname == 'last_seen_id')) == 0:
            self.db_vars.insert({'varname': 'last_seen_id', 'value': 1})
        if len(self.db_vars.search(Vars.varname == 'optin_running')) == 0:
            self.db_vars.insert({'varname': 'optin_running', 'value': False})
        if len(self.db_vars.search(Vars.varname == 'next_battle_year')) == 0:
            self.db_vars.insert({'varname': 'next_battle_year', 'value': 2000})
        if len(self.db_vars.search(Vars.varname == 'next_battle_month')) == 0:
            self.db_vars.insert({'varname': 'next_battle_month', 'value': 12})
        if len(self.db_vars.search(Vars.varname == 'next_battle_day')) == 0:
            self.db_vars.insert({'varname': 'next_battle_day', 'value': 19})
        if len(self.db_vars.search(Vars.varname == 'next_battle_hour')) == 0:
            self.db_vars.insert({'varname': 'next_battle_hour', 'value': 0})
        if len(self.db_vars.search(Vars.varname == 'next_battle_minute')) == 0:
            self.db_vars.insert({'varname': 'next_battle_minute', 'value': 0})
        if len(self.db_vars.search(Vars.varname == 'battle_frequency_hours')) == 0:
            self.db_vars.insert({'varname': 'battle_frequency_hours', 'value': 6})
        if len(self.db_vars.search(Vars.varname == 'battle_frequency_minutes')) == 0:
            self.db_vars.insert({'varname': 'battle_frequency_minutes', 'value': 0})
        if len(self.db_vars.search(Vars.varname == 'stop_frequency')) == 0:
            self.db_vars.insert({'varname': 'stop_frequency', 'value': True})
        if len(self.db_vars.search(Vars.varname == 'stop_next_battle')) == 0:
            self.db_vars.insert({'varname': 'stop_next_battle', 'value': True})
        if len(self.db_vars.search(Vars.varname == 'fighter_announce')) == 0:
            self.db_vars.insert({'varname': 'fighter_announce', 'value': False})
        if len(self.db_vars.search(Vars.varname == 'announce_queue')) == 0:
            self.db_vars.insert({'varname': 'announce_queue', 'value': []})
        if len(self.db_vars.search(Vars.varname == 'battle_queue')) == 0:
            self.db_vars.insert({'varname': 'battle_queue', 'value': []})
        if len(self.db_vars.search(Vars.varname == 'message_queue')) == 0:
            self.db_vars.insert({'varname': 'message_queue', 'value': []})
        log.send_message("[DATABASE] Update: done setup_vars")


    def update_last_seen(self, last_seen_id):
        Vars = Query()
        self.db_vars.update({'value': last_seen_id}, Vars.varname == 'last_seen_id')
        log.send_message("[DATABASE] Update: last_seen_id set to " + str(last_seen_id))

    def get_last_seen_id(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'last_seen_id')[0]['value']

    def get_optin_running(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'optin_running')[0]['value']

    def update_optin_running(self, run):
        Vars = Query()
        self.db_vars.update({'value': run}, Vars.varname == 'optin_running')
        log.send_message("[DATABASE] Update: optin_running set to " + str(run))

    def get_next_battle(self):
        Vars = Query()
        year = self.db_vars.search(Vars.varname == 'next_battle_year')[0]['value']
        month = self.db_vars.search(Vars.varname == 'next_battle_month')[0]['value']
        day = self.db_vars.search(Vars.varname == 'next_battle_day')[0]['value']
        hour = self.db_vars.search(Vars.varname == 'next_battle_hour')[0]['value']
        minute = self.db_vars.search(Vars.varname == 'next_battle_minute')[0]['value']
        return datetime(year, month, day, hour, minute)

    def update_next_battle(self, date):
        Vars = Query()
        self.db_vars.update({'value': date.year}, Vars.varname == 'next_battle_year')
        self.db_vars.update({'value': date.month}, Vars.varname == 'next_battle_month')
        self.db_vars.update({'value': date.day}, Vars.varname == 'next_battle_day')
        self.db_vars.update({'value': date.hour}, Vars.varname == 'next_battle_hour')
        self.db_vars.update({'value': date.minute}, Vars.varname == 'next_battle_minute')
        log.send_message("[DATABASE] Update: next_battle set to {}/{}/{} {}:{}".format(date.year, date.month, date.day, date.hour, date.minute))

    def get_battle_frequency(self):
        Vars = Query()
        h = self.db_vars.search(Vars.varname == 'battle_frequency_hours')[0]['value']
        m = self.db_vars.search(Vars.varname == 'battle_frequency_minutes')[0]['value']
        return h, m

    def update_battle_frequency(self, hours, minutes):
        Vars = Query()
        self.db_vars.update({'value': hours}, Vars.varname == 'battle_frequency_hours')
        self.db_vars.update({'value': minutes}, Vars.varname == 'battle_frequency_minutes')

    def update_stop_frequency(self, set):
        Vars = Query()
        self.db_vars.update({'value': set}, Vars.varname == 'stop_frequency')

    def get_stop_frequency(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'stop_frequency')[0]['value']

    def update_stop_next_battle(self, set):
        Vars = Query()
        self.db_vars.update({'value': set}, Vars.varname == 'stop_next_battle')

    def get_stop_next_battle(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'stop_next_battle')[0]['value']

    def update_fighter_announce(self, set):
        Vars = Query()
        self.db_vars.update({'value': set}, Vars.varname == 'fighter_announce')

    def get_fighter_announce(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'fighter_announce')[0]['value']

    def add_announce_queue(self, username):
        list = self.get_announce_queue()
        list.append(username)
        list.sort
        self.update_announce_queue(list)

    def delete_announce_queue(self):
        self.update_announce_queue([])

    def update_announce_queue(self, list):
        Vars = Query()
        self.db_vars.update({'value': list}, Vars.varname == 'announce_queue')

    def get_announce_queue(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'announce_queue')[0]['value']

    def add_battle_queue(self, winner, defeated):
        list = self.get_battle_queue()
        list.append({'winner': winner, 'defeated': defeated})
        #list.sort
        self.update_battle_queue(list)

    def delete_battle_queue(self):
        self.update_battle_queue([])

    def update_battle_queue(self, list):
        Vars = Query()
        self.db_vars.update({'value': list}, Vars.varname == 'battle_queue')

    def get_battle_queue(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'battle_queue')[0]['value']

    def add_message_queue(self, message):
        list = self.get_message_queue()
        list.append(message)
        self.update_message_queue(list)

    def delete_message_queue(self):
        self.update_message_queue([])

    def update_message_queue(self, list):
        Vars = Query()
        self.db_vars.update({'value': list}, Vars.varname == 'message_queue')

    def get_message_queue(self):
        Vars = Query()
        return self.db_vars.search(Vars.varname == 'message_queue')[0]['value']

    def restart(self):
        could_wipe = True

        try:
            os.remove(self.db_route)
        except:
            could_wipe = False
        
        if could_wipe:
            self.db = TinyDB(self.db_route)
            self.db_candidates = self.db.table('candidates', cache_size=0)
            self.db_fighters = self.db.table('fighters', cache_size=0)
            self.db_vars = self.db.table('vars', cache_size=0)
            self.setup_vars()

        return could_wipe