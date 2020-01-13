# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- aiw.py -*-

This file is the starting point of the bots. The developer may think of it
as the trigger file. The Bot classes will be instantiated here and the onStart()
method will be called to start running the bots. 

Example:
    
    This file is auto-generated. It is recommended not to edit this file.
    Required changes may be made in the bot.py or controller.py files        

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 24/10/2019
"""
# Your code starts from here

# Imports
# from .src.bots.NID.bot import *
# from .src.bots.CIB.bot import *


# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpa.settings")
# django.setup()

import re
import os
import csv
import time
import random
import pandas as pd
import numpy as np

# selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .src.bots.NID.bot import Bot as bota
from .src.bots.CIB.bot import Bot as botb
from .config import config
# from bots.factory import broadcast_log
import smtplib
# from log.log_file import log,# push_data
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# processNID = NID.Bot('NID')
# processNID.onStart()

# processCIB = CIB.Bot('CIB')
# processCIB.onStart()

class aiw():
    def push_data(self, nid, task, result):
        nid = str(nid)
        if len(nid) < 2:
            nid = 'N/A'
        changes = [
            nid, task, result
        ]

        dirname = os.path.dirname(__file__)
        file = os.path.join(dirname, 'log/logs.csv')

        with open(file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(changes)

    def send_mail(self, email, nid, dob):
        try:
            s = smtplib.SMTP('smtp.gmail.com:587')
            s.ehlo()
            s.starttls()
            s.login(config.MY_ADDRESS, config.PASSWORD)

            # msg = MIMEMultipart()
            subject = 'NID and/or Date of Birth Exception'
            # msg['From'] = MY_ADDRESS
            # # msg['Reply-to'] = MY_ADDRESS
            # msg['To'] = email

            text = "NID: {} and/or Date of Birth: {} Did Not Match".format(nid, dob)
            message = 'Subject: {}\n\n{}'.format(subject, text)
            s.sendmail(config.MY_ADDRESS, email, message)
            # msg.attach(MIMEText(message, 'plain'))
            # s.send_message(msg)
            s.quit()

        except Exception as ex:
            print(ex)

    cib_logged_in = False
    nid_logged_in = False
    # data = pd.read_csv('C:\\Users\\Lenovo\\Desktop\\WORK IN PROGRESS\\rpa\\CITY_BANK_POC\\NID_test_data.csv')
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, 'NID_test_data_new1.csv')
    data = pd.read_csv(file)

    month_conv = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    def format_date(self, dob):
        # from 20/11/1996 to 20-11-1996
        day, month, year = dob.split('/')
        if len(year) < 4:
            year = "19" + year
        new_dob = day + '-' + month + '-' + year
        return new_dob

    def format_dob(self, dob):
        # 25 Jul 1965 to 1965/07/25
        day, month, year = dob.split('/')
        # if '.' or ',' in month:
        #     month = month[:-1]
        month_num = 1
        day = str(day)

        for key, value in self.month_conv.items():
            if month in key:
                month_num = value
        month = str(month_num)
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        new_dob = year + '/' + month + '/' + day
        return new_dob

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = config()
    # driver2 = config()
    def cib_loop(self):
        for index, row in self.data.iterrows():
            nid = row['nid']
            print('NID: ', nid)
            # dob = format_date(row['date_of_birth'])
            dob = row['date_of_birth']
            # if nid_logged_in:
            #     driver.get(r'/Users/macboookpro/Desktop/test/CITY_BANK_POC/Bangladesh_Election_Commission.htm')
            a_nid, a_name, a_dob = bota.get_nid_detail(self, config.NID_BROWSER, nid, dob)
            if a_name == "not found":
                print('NOT FOUND')
                continue

            # push_data(nid, "Get NID detail", "Successful")

            # if not flag:
                # driver2 = webdriver.Chrome(ChromeDriverManager().install())

                # options2 = Options()
                # options2.headless = True
                # options2.add_argument('--no-sandbox')
                # options2.add_argument('--disable-dev-shm-usage')
                # SELENIUM_GRID_URL = "http://selenium-hub:4444/wd/hub"
                # CAPABILITIES = DesiredCapabilities.CHROME.copy()
                # driver2 = webdriver.Remote(desired_capabilities=CAPABILITIES,
                #                           command_executor=SELENIUM_GRID_URL)

            #bota.gettinglogs("CIB Login SUCCESS")
                # flag = True
            # push_data(nid, "logging in CIB", "Successful")

            a_dob = self.format_dob(dob)
            # a_dob = format_date(a_dob)

            print(dob, a_dob)
            name = row['full_name']
            print("nid data: " + a_name.lower())
            print("csv data: " + name.lower())

            if a_name.lower() == name.lower():
                # self.push_data(nid, "NID Data Matched", "Successful")
                #bota.gettinglogs("NID Data Matched Successfully")
                # and dob == format_date(a_dob):
                botb.cib_fill_form(self, config.CIB_BROWSER, row, a_nid)
                # push_data(nid, "CIB Form Fill Up", "Successful")
                print('CIB FORM FILLED UP')
                config.CIB_BROWSER.get("https://cib.bb.org.bd/new_inquiry")
            else:
                # push_data(nid, "NID Data Matched", "Failed")
                #bota.gettinglogs("Mismatch Name and/or Date Of Birth!")
                email = 'rpatesta3@gmail.com'
                # self.send_mail(email, nid, dob)
                print('Mismatch Name and/or Date Of Birth!')

    def start_bot(self):
        # driver = webdriver.Chrome(ChromeDriverManager().install())

        # options = Options()
        # options.headless = True
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # driver = webdriver.Chrome(options=options, executable_path=r'/usr/lib64/chromium/chromedriver')
        # SELENIUM_GRID_URL = "http://selenium-hub:4444/wd/hub"
        # CAPABILITIES = DesiredCapabilities.CHROME.copy()
        # driver = webdriver.Remote(desired_capabilities=CAPABILITIES,
        #                         command_executor=SELENIUM_GRID_URL)

        if bota.login_nid(self, config.NID_BROWSER):
            # push_data("", "logging in NID", "Successful")
            print('NID LOGGED IN')
            nid_logged_in = True
            #bota.gettinglogs("NID Login SUCCESS")
        # if nid_logged_in == False:
        #     print('FAILED NID LOGIN')
        #    # push_data("", "logging in NID", "Failed")

        flag = False
        botb.cib_login(self, config.CIB_BROWSER)
        print('CIB LOGGED IN')
        self.cib_loop()

            #bota.gettinglogs("Job Done!")
            # config.CIB_BROWSER.get("https://cib.bb.org.bd/new_inquiry")



if __name__ == "__main__":
    aiw().start_bot()
