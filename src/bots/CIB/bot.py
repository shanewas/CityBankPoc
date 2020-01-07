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
from ..CIB.controller import *

import re
import time
import random
#from bots.factory import broadcast_log #where is broadcast log??
from datetime import datetime
from selenium.webdriver.common.keys import Keys

from pathlib import Path
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Bot:
    def __init__(self, botName):
        # Declare botName to be passed to the tasks defined in the controller
        # so that the logging is consistent
        self.botName = botName

    # def onStart(self):
    #     loginToCBS()

    def gettinglogs(self, entry):
        logs = []
        now = datetime.now()
        logs.append("{0}-{1}".format(now, entry))
        # broadcast_log(
        #     "<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(
        #         now.strftime("%m/%d/%Y %H:%M:%S"), entry))

    def check(self, finance):
        type_one_financing = [
            'Bai-Muazzal (Instalment Payment)',
            'Bai-Muazzal (Real Estate)',
            'Demand Loan (Instalment repayment)',
            'Financial Leasing',
            'Hire-Purchase',
            'Hire-Purchase under shirkatul Meelk',
            'Ijara (Lease Finance)',
            'Mortgage loan',
            'Operational Leasing',
            'Other instalment contract',
            'Partially Secured Term Loan',
            'Term Loan',
            'Packing Credit (Instalment repayment)',
        ]

        if finance in type_one_financing:
            return True
        else:
            return False

    def format_date(self, dob):
        # 1994/12/25 to 25/12/1994
        day, month, year = dob.split('/')
        if len(year) < 4:
            year = "19" + year
        new_dob = day + '/' + month + '/' + year
        return new_dob

    def format_dob(self, dob):
        # 1994/12/25 to 25/12/1994
        year, month, day = dob.split('/')
        if len(year) < 4:
            year = "19" + year
        new_dob = day + '/' + month + '/' + year
        return new_dob

    def cib_login(self, driver):
        # gettinglogs("GETTING LOGS!")
        username, password = 'XGK044824', 'Cbl%10011'
        # driver.get(r'file:///C:\Users\Lenovo\Downloads\CITY_BANK_POC\CITY_BANK_POC\Bangladesh_Bank_Credit_Information_Bureau_Login.htm')
        # driver.get(r'file:///rpa/CITY_BANK_POC/Bangladesh_Bank_Credit_Information_Bureau_Login.htm')
        driver.get(r'https://cib.bb.org.bd/login')
        # el_username = driver.find_element_by_xpath(r'/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div[1]/div/div/input')
        el_username = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[1]/div/div/input')
        el_username.clear()
        el_password = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[2]/div/div/input')
        el_password.clear()
        el_captcha_ans = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[3]/div/div/input')
        el_captcha_ans.clear()
        # el_login_btn = driver.find_element_by_xpath(r'//*[@id="loginForm"]/a')

        el_username.send_keys(username)
        # gettinglogs("CIB Login: username")
        el_password.send_keys(password)
        # gettinglogs("CIB Login: password")

        el_question = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[3]/label')
        text = el_question.text
        num1, num2 = re.findall(r'\d+', text)
        num1, num2 = int(num1), int(num2)
        ans = 0
        if "Addition" in text or "Sum" in text:
            ans = num1 + num2
        elif "Substraction" in text or "Subtraction" in text:
            ans = num1 - num2
        elif "Multiplication" in text:
            ans = num1 * num2
        elif "Division" in text:
            ans = num1 / num2

        el_captcha_ans.send_keys(str(ans))
        # driver.refresh()
        # gettinglogs("CIB Login: Captcha")

        # el_login_btn.click()
        # driver.execute_script("arguments[0].click();", el_login_btn)

        # el_btn_login.click()
        el_captcha_ans.send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/a').click()
        # gettinglogs("CIB Login SUCCESS")

        return True

    def cib_fill_form(self, driver, row, a_nid):
        self.gettinglogs("Filling Up CIB Form for " + str(row['nid']))
        print('BEFORE FILL UP')


        try:
            el_type_of_financing_l1_1 = driver.find_element_by_xpath(
                r'//*[@id="individualInquiryForm"]/div[2]/div[2]/div/div/div/button').click()

            type_of_finance = row['type_of_financing_1']
            driver.find_element_by_link_text(type_of_finance).click()
            # type_of_finance = row['Type_of_financing']
            # el_type_of_financing_l1_1.send_keys(type_of_finance)
            # el_type_of_financing_l1_1.click()
            self.gettinglogs("Filling Up Type of Financing 1")

            if self.check(type_of_finance):
                # have those four fields
                # LAYER TWO::Installment Data
                try:
                    el_number_of_installment_l2 = driver.find_element_by_xpath(
                        r'//*[@id="individualInquiryForm"]/div[3]/div[1]/div[2]/div/div/input')
                    el_number_of_installment_l2.clear()
                    el_number_of_installment_l2.send_keys(row['no_of_installment'])
                    # el_number_of_installment_l2.send_keys(row['Number_Of_Installment'])
                    self.gettinglogs("Filling Up No of Installment")
                except Exception as ex:
                    print("No of Installment")
                    # gettinglogs("Exception in No of Installment")
                    # print(ex)

                installment_amount = row['installment_amount']
                print('Installment Amount: '+str(installment_amount))
                # el_installment_amount_l2 = driver.find_element_by_css_selector('#individualInquiryForm > div.install_form > div:nth-child(1) > div.col-sm-8 > div > div > input')
                el_installment_amount_l2 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[3]/div[1]/div[3]/div/div/input')
                el_installment_amount_l2.clear()
                el_installment_amount_l2.send_keys(str(int(installment_amount)))
                self.gettinglogs("Filling Up Installment Amount")


                try:
                    el_total_requested_amount_l2 = driver.find_element_by_xpath(
                        r'//*[@id="individualInquiryForm"]/div[3]/div[2]/div[1]/div/div/input')
                    el_total_requested_amount_l2.clear()
                    # el_total_requested_amount_l2.send_keys(row['Total_requested_amount'])
                    el_total_requested_amount_l2.send_keys(row['total_request_amount'])
                    self.gettinglogs("Filling Up Total Requested Amount")
                except Exception as ex:
                    print("Requested Amount")


                try:
                    el_periodicity_of_payment_l2_1 = driver.find_element_by_xpath(
                        r'//*[@id="individualInquiryForm"]/div[3]/div[2]/div[2]/div/div/div/button').click()

                    # el_periodicity_of_payment_l2_1.send_keys(row['periodicity_of_payment_1'])
                    driver.find_element_by_link_text(row['periodicity_of_payment_1']).click()
                    # driver.find_element_by_link_text(type_of_finance).click()
                    # el_periodicity_of_payment_l2_1.send_keys(row['Periodicity_of_payment'])
                    # time.sleep(1)
                    el_periodicity_of_payment_l2_1.click()
                    self.gettinglogs("Filling Up Periodicity of Payment 1")
                except Exception as ex:
                    print("Periodicity of Payment 1")

            else:
                # have credit limits only
                # LAYER TWO::Installment Data :: credit limits
                try:
                    el_credit_limit_l2 = driver.find_element_by_xpath(
                        r'//*[@id="individualInquiryForm"]/div[4]/div/div[2]/div/div/input')
                    el_credit_limit_l2.clear()
                    # el_credit_limit_l2.send_keys(row['credit_limit'])
                    el_credit_limit_l2.send_keys(row['Credit_Limit'])
                    self.gettinglogs("Filling Up Credit Limit")
                except Exception as ex:
                    print("Credit Limit")
                    self.gettinglogs("Exception in Credit Limit Exception")
                    # print(ex)

        except Exception as ex:
            print("Type of Finance 1")
        el_nid_l3 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[11]/div[1]/div/div/input')
        el_nid_l3.clear()
        el_date_of_birth_l3 = driver.find_element_by_xpath(r'//*[@id="datetimepicker-ind"]/input')
        el_date_of_birth_l3.clear()
        el_district_of_birth_l3 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[13]/div[1]/div/div/input')
        el_district_of_birth_l3.clear()

        el_name_l3 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[7]/div[2]/div/div/div/input')
        el_name_l3.clear()
        el_fathers_name_l3 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[8]/div[2]/div/div/div/input')
        el_fathers_name_l3.clear()
        el_mothers_name_l3 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[9]/div[2]/div/div/div/input')
        el_mothers_name_l3.clear()
        el_male_l3 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[12]/div[2]/div/div/label[1]/input[@name="gender" and @type="radio" and @value="M"]')
        el_female_l3 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[12]/div[2]/div/div/label[2]/input[@name="gender" and @type="radio" and @value="F"]')
        el_country_of_birth_l3_1 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[13]/div[2]/div/div/div/button')
        # LAYER FOUR::Permanent address data
        el_district_l4 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[15]/div[1]/div/div/input')
        el_district_l4.clear()
        el_postal_code_l4 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[16]/div[1]/div/div/input')
        el_postal_code_l4.clear()
        el_street_name_and_number_l4 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[15]/div[2]/div/div/input')
        el_street_name_and_number_l4.clear()
        el_country_l4_1 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[16]/div[2]/div/div/div/button')
        el_sector_type_public_l7 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[24]/div[1]/div/div/label[1]/input')
        el_sector_type_private_l7 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[24]/div[1]/div/div/label[2]/input')
        el_sector_code_l7 = driver.find_element_by_xpath(r'/html/body/div[2]/div[4]/div/div/div/div[2]/div/div[1]/form/div[24]/div[2]/div/div/select')
        el_contract_history_12_l8 = driver.find_element_by_xpath('//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[1]')
        el_contract_history_24_l8 = driver.find_element_by_xpath('//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[2]')
       
        el_new_person_inquiry = driver.find_element_by_xpath(
            r'/html/body/div[2]/div[4]/div/div/div/div[2]/div/div[1]/form/div[28]/div/div/div/button')


        nid = a_nid

        el_nid_l3.send_keys(nid)
        self.gettinglogs("Filling up NID")
        hold = self.format_dob(row['date_of_birth'])
        el_date_of_birth_l3.send_keys(self.format_date(hold))
        self.gettinglogs("Filling up Date of Birth")
        el_district_of_birth_l3.send_keys(row['district_of_birthl1'])
        self.gettinglogs("Filling up Distric of Birth")
        el_name_l3.send_keys(row['full_name'])
        self.gettinglogs("Filling up Full Name")
        el_fathers_name_l3.send_keys(row['father_name'])
        self.gettinglogs("Filling up Father's Name")
        el_mothers_name_l3.send_keys(row['mother_name'])
        self.gettinglogs("Filling up Mother's Name")

        try:
            gender = row['gender']
            print('GENDER: ' + gender)

            if gender == 'Male':
                # el_male_l3.click()
                driver.execute_script("arguments[0].click();", el_male_l3)
                self.gettinglogs("Filling up Gender: Male")
                # print('Male')
            elif gender == 'Female':
                # el_female_l3.click()
                driver.execute_script("arguments[0].click();", el_female_l3)
                # print('Female')
                self.gettinglogs("Filling up Gender: Female")
        except Exception as ex:
            self.gettinglogs("Exception in Gender")
            print(ex)

        # el_country_of_birth_l3_1.send_keys(row['country_of_birthl2'].upper())
        el_country_of_birth_l3_1.click()
        driver.find_element_by_link_text(row['country_of_birthl2'].upper()).click()
        self.gettinglogs("Filling up Country of Birth 1")
        # el_country_of_birth_l3_1.click()
        # el_country_of_birth_l3_2.send_keys(row['country_of_birthl2'].upper())
        self.gettinglogs("Filling up Country of Birth 2")
        # el_country_of_birth_l3_2.click()

        el_district_l4.send_keys(row['districtl2'])
        self.gettinglogs("Filling up District")
        el_street_name_and_number_l4.send_keys(row['street_name_and_numberl2'])
        self.gettinglogs("Filling up Street Name and Number")
        el_postal_code_l4.send_keys(row['postal_code'])
        self.gettinglogs("Filling up Postal Code")
        # el_country_l4_1.send_keys(row['country_of_birthll3'].upper())
        el_country_l4_1.click()
        driver.find_element_by_link_text(row['country_of_birthl2'].upper()).click()
        self.gettinglogs("Filling up Country of Birth 3")


        sector_type = row['sector_type']

        if sector_type == 'public':
            driver.execute_script("arguments[0].click();", el_sector_type_public_l7)
            self.gettinglogs("Filling up Sector Type: Public")
        else:
            # el_sector_type_private_l7.click()
            driver.execute_script("arguments[0].click();", el_sector_type_private_l7)
            self.gettinglogs("Filling up Sector Type: Private")


        from selenium.webdriver.support.ui import Select
        driver.execute_script("arguments[0].click();", el_sector_code_l7)
        select = Select(driver.find_element_by_id('individual_sector_code'))
        select.select_by_visible_text(row['sector_code'])


        contract_history = int(row['contract_history'])

        if contract_history == 12:
            driver.execute_script("arguments[0].click();", el_contract_history_12_l8)
            self.gettinglogs("Filling up Contract History: 12")
        elif contract_history == 24:
            driver.execute_script("arguments[0].click();", el_contract_history_24_l8)

            self.gettinglogs("Filling up Contract History: 24")


        time.sleep(1)
        print('CIB FORM END')
        self.gettinglogs("Form Fill Completed for NID:"+str(row['nid']))
        # el_new_person_inquiry.click()
        driver.execute_script("arguments[0].click();", el_new_person_inquiry)
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/a"))
            )
        finally:
            driver.execute_script("arguments[0].click();", 
                            driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a"))

        # from selenium import webdriver
        url = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a").get_attribute("href")

        image_url = url
        img_name = image_url.split('/')[-1]
        img_name = img_name[:-4]
        img_name = img_name[9:]
        # driver.get(url)
        # driver.save_screenshot("docker/Downloads{}.png".format(img_name))


        filename = Path("storage/output/docker/{}.pdf".format(img_name))
        url = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a").get_attribute("href")
        response = requests.get(url)
        filename.write_bytes(response.content)


        driver.get("https://cib.bb.org.bd/new_inquiry")