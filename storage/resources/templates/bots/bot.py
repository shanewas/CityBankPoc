# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- bot.py -*-

This module defines the flow of actions for the tasks within a bot. It would help
for the developer to imagine this as an interface that calls functions defined in
the controller. 

Example:
    
    The rest of the code in this file can be considered as an example to follow,
    and discarded while coding        

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 24/10/2019
"""
#Your code starts from here

# Imports
from .controller import *

class Bot:
    def __init__(self, botName):
        # Declare botName to be passed to the tasks defined in the controller
        # so that the logging is consistent
        self.botName = botName

    def onStart(self):
        loginToCBS()
