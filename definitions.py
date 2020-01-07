# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- definitions.py -*-

This module includes variable definitions for XPath Selectors and 
arrays to be used throughout the bot.

Example:
    
    The example below is what the contents of this file are expected to look like
    As aforementioned, only XPath Selectors, arrays and other static variables (to be 
    used throughout the program)::

        $ variable_name = browser.find_element_by_xpath(r'//*[@id="P826_variable_name"]')
        $ array_name = []

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 23/10/2019
"""
#Your code starts from here

#Dummy XPath selectors for test run

log_in_user = r'//*[@id="P101_USERNAME"]'
log_in_psw = r'//*[@id="P101_PASS"]'
captcha = r'//*[@id="P101_CAPTCHA"]'
log_in_button = r'//*[@id="B72277838335750912"]'
ok_button = r'//*[@id="apexConfirmBtn"]/span'
