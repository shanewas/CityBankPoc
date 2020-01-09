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
# import sys
# sys.path.append("..")

from ..NID.controller import *

import os
import csv
import time
import random
import pandas as pd
import numpy as np
# from bots.factory import broadcast_log
# from .src.bots.CIB.bot import gettinglogs
# import pytesseract
from selenium import webdriver
from datetime import datetime
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract as ptr

class Bot:
    def __init__(self, botName):
        # Declare botName to be passed to the tasks defined in the controller
        # so that the logging is consistent
        self.botName = botName

    def gettinglogs(self, entry):
        logs = []
        now = datetime.now()
        logs.append("{0}-{1}".format(now, entry))
        # broadcast_log(
        #     "<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(
        #         now.strftime("%m/%d/%Y %H:%M:%S"), entry))
    
    # def onStart(self):
    #     loginToCBS()
    def login_nid(self, driver):
        # self.gettinglogs("Logging in NID website")
        # driver.get(r'file:///C:\Users\Lenovo\Downloads\CITY_BANK_POC\CITY_BANK_POC\Bangladesh_Election_Commission.htm')
        # driver.get(r'file:///rpa/CITY_BANK_POC/Bangladesh_Election_Commission.htm')
        driver.get('https://192.168.249.10/partner/;BVRSPARTNERWEB=xJhbdT4ddrfnPrh5Swvs7Z61p1KWylTyphQl24LfdnjyNvPL4yxh!-1166847401?_adf.ctrl-state=eh4bar95v_1&_afrLoop=29698505854216796&_afrWindowMode=0&_afrWindowId=null')
        # driver.find_element_by_xpath('//*[@id="wrapper"]/h3/a').click()
        el_username = driver.find_element_by_xpath(
            '/html/body/div/form/div/div[2]/div/div/div/div/div/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input')
        el_password = driver.find_element_by_xpath(
            '/html/body/div/form/div/div[2]/div/div/div/div/div/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[4]/td[2]/input')
        el_btn_login = driver.find_element_by_xpath(
            '/html/body/div/form/div/div[2]/div/div/div/div/div/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[6]/td[2]/button')
        el_username.clear()
        el_password.clear()
        username, password = 'citybank13_city', '123456'
        el_username.send_keys(username)
        el_password.send_keys(password)

        el_btn_login.click()

        return True

    def get_nid_detail(self, driver, nid_data, dob):
        # driver.get(r'http://nid.techcomengine.com')
        # driver.get(r'file:///rpa/CITY_BANK_POC/Bangladesh_Election_Commission2.htm')
        driver.get(r'https://192.168.249.10/partner/faces/searchbynid?_adf.ctrl-state=mbfktqv6j_5')

        el_nid = driver.find_element_by_xpath('//*[@id="pt1:it1::content"]')
        el_nid.clear()

        el_dob = driver.find_element_by_xpath('//*[@id="pt1:id1::content"]')
        el_dob.clear()


        el_btn_verify = driver.find_element_by_xpath('//*[@id="pt1:cb3"]')
        el_nid.send_keys(int(nid_data))
        el_dob.send_keys(dob)
        # time.sleep(5)
        try:
            el_btn_verify.click()

            # gettinglogs("NID Data found for: " + str(nid_data))
            # time.sleep(1)

            image = driver.find_element_by_xpath(
                r'/html/body/div/form/div/div[2]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/table/tbody/tr/td[4]/div/div[1]/div/div[5]/table/tbody/tr/td/div/div/table/tbody/tr/td[2]/div/div/div/div[2]/img')
            image = image.get_attribute("src")
            self.gettinglogs("NID Data found for: " + str(nid_data))

            # image = 'https://192.168.249.10' + image
            # print(image)
            # dirname = os.path.dirname(__file__)
            # image = os.path.join(dirname, r'/html/body/div/form/div/div[2]/div/div/div/div/div/div[3]/div/div[1]/div/div[2]/table/tbody/tr/td[4]/div/div[1]/div/div[5]/table/tbody/tr/td/div/div/table/tbody/tr/td[2]/div/div/div/div[2]/img')
            # image = image.get_attribute("src")
            # print("before" + image)
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # print("after" + image)
            # image = image[26:]
            # dirname = os.path.dirname(__file__)

            # image = os.path.join(dirname, 'NIDS/NID1/Bangladesh_Election_Commission_files/19939111777000259_voterInfo.jpg')
            # image = os.path.join(dirname, image)
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--test-type")
            options.binary_location = "nid_images"
            image_url = image
            img_name = image_url.split('/')[-1]
            img_name = img_name[:-4]
            driver.get(image_url)
            driver.save_screenshot("nid_images/{}.png".format(img_name))
            image = r"nid_images/{}.png".format(img_name)
            # nid_data = ptr.image_to_string(Image.open(image, 'r'))
            nid_data = ptr.image_to_string(Image.open(image, 'r'))

            # import os
            # path1 = os.path.normpath("file:///C:/Users/vendor/Downloads/rpa/CITY_BANK_POC/NIDS/NID1/Bangladesh_Election_Commission_files/19939111777000259_voterInfo.jpg")
            # nid_data = ptr.image_to_string(Image.open(path1, 'r'))

            # nid_data = Image.open(image, 'r')
            # lang = 'eng', 'ben'
            lines = []
            cnt_space = 0
            line = ''
            for letter in nid_data:
                if letter == ' ':
                    cnt_space += 1
                if cnt_space >= 2 or letter == '\n':
                    if line:
                        lines.append(line)
                    line = ''
                    cnt_space = 0
                else:
                    cnt_space = 0
                    line += letter
            if line:
                lines.append(line)
            # print(lines)
            name, gender, dob, nid = '', '', '', ''
            for row in lines:
                if ':' in row:
                    # print(row)
                    if 'Name' in row:
                        name = row.split(':')[1]
                    elif 'Gender' in row:
                        gender = row.split(':')[1][1:]
                    elif 'Date' in row:
                        dob = row.split(':')[1]
                    elif 'ID' in row:
                        nid = row.split(':')[1]
                        break
            if ' ' in nid:
                a, b = nid.split(' ')
                nid = a + b
            print(name)
            print(gender)
            print(dob)
            print(nid)
            return nid, name, dob

        # // *[ @ id = "pt1:it1::conte
        #
        #
        # login_nid(driver)
        # get_nid_detail(driver, 19948118213000186, "1994/12/25")

        # return get_nid, get_name, get_dob

        except Exception as ex:
            self.gettinglogs("NID: " + str(nid_data) + " Not Found!")
            # raise ex
            return nid_data, "not found", dob

