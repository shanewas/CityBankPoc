# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- controller.py -*-

This module consists of the actual functions that "do" tasks. The developer
is expected to write all the functions (as modular as possible) in this file
 - including the logging to server and calling all checks etc. This is one of
the few files where the developer has complete control over. However, the 
actual calling of the functions written here are expected to be within the 
bot.py file i.e. the flow and logic required is to be within bot.py 

Example:
    
    The rest of the code in this file can be considered as an example to follow,
    and discarded while coding.       

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 24/10/2019
"""
#Your code starts from here

# Imports

# import sys
# sys.path.append("..") # Adds higher directory to python modules path.

from ....config import *
from ....definitions import *

def loginToCBS():

    driver = BROWSER
    driver.get(r'http://cbs.techcomengine.com/Login.html')

    try:
        driver.find_element_by_xpath(log_in_user).send_keys("user")
        driver.find_element_by_xpath(log_in_psw).send_keys("password")
        driver.find_element_by_xpath(captcha).send_keys("NNFA6")
        driver.find_element_by_xpath(log_in_button).click()
        print("First")
    except:
        driver.find_element_by_xpath(ok_button)
        driver.find_element_by_xpath(ok_button).click()

        driver.find_element_by_xpath(log_in_psw).send_keys("password")
        driver.find_element_by_xpath(captcha).send_keys("NNFA6")
        driver.find_element_by_xpath(log_in_button).click()
        print("Second")
