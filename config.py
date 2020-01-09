# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- config.py -*-

This module includes configurable settings that may differ from bot-to-bot or
from environment-to-environment e.g. settings that the developer may have to
change if they were working on Ubuntu as compared to working on Windows.

Example:
    
    The example below is what the contents of this file are expected to look like
    As aforementioned, only CONFIGURABLES may be added here (to be 
    used throughout the program)::

        $ WEBDRIVER_PATH = "/usr/lib64/chromium/chromedriver"

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 23/10/2019

"""
#Code starts from here
#Edit below variables according to requirements

# Imports
from selenium import webdriver
# Uncomment below block if using remote webdriver

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
class config:
    APP_NAME = 'CIB and NID automation'
    CLIENT_NAME = 'CBL'

    # In case of using local webdriver
    # WEBDRIVER_PATH = '/usr/lib64/chromium/chromedriver'
    options = webdriver.ChromeOptions()
    options.binary_location = 'citybank/chrome/chrome.exe'
    WEBDRIVER_PATH = 'citybank/chrome/chromedriver.exe'
    BROWSER = webdriver.Chrome(executable_path=WEBDRIVER_PATH, chrome_options=options)

    # Uncomment below block if using remote webdriver

    # SELENIUM_GRID_URL = "http://198.0.0.1:4444/wd/hub"
    # CAPABILITIES = DesiredCapabilities.CHROME.copy()
    # BROWSER = webdriver.Remote(desired_capabilities=CAPABILITIES,
    #                           command_executor=SELENIUM_GRID_URL)

    # If more browser instances are required, please add below here
    # Make sure to declare new variable for that instance i.e. BROWSER_TWO = ...

    AWS_ACCESS_TOKEN = ''
    NUMBER_OF_ENTRIES = ''

    LOGGING_SERVER_URL = 'wss://localhost:8765'

    MY_ADDRESS = 'rpatesta3@gmail.com'
    PASSWORD = 'rpa@test@1'