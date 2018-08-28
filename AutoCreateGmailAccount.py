# -*- coding: utf-8 -*-
# @Author: Chao
# @Date:   2018-08-23 22:57:28
# @Last Modified by:   Chao
# @Last Modified time: 2018-08-28 19:50:22
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import random
import time


class CreateGmail:
    """Auto Create Gmail Accounts with popular names"""
    def __init__(self, firstname, lastname, username, pswd):
        self._firstname = firstname
        self._lastname = lastname
        self._username = username
        self._pswd = pswd
        self._Donefile = open('./data/CreatedAccounts.csv', 'a')
        self.Initialize()

    def Initialize(self):
        self._browser = webdriver.Firefox()
        self._browser.delete_all_cookies()
        self._browser.get('https://accounts.google.com/SignUp?hl=en')
    
    def CreateAccount(self):
        self._browser.find_element_by_css_selector(r'input[id="firstName"]').send_keys(self._firstname)
        self._browser.find_element_by_css_selector(r'input[id="lastName"]').send_keys(self._lastname)
        time.sleep(1 + 3 * random.random())
        self._browser.find_element_by_css_selector(r'input[id="username"]').send_keys(self._username)
        self._browser.find_element_by_css_selector(r'input[name="Passwd"]').send_keys(self._pswd)
        time.sleep(1 + 3 * random.random())
        self._browser.find_element_by_css_selector(r'input[name="ConfirmPasswd"]').send_keys(self._pswd)
        self._browser.find_element_by_css_selector(r'div[id="accountDetailsNext"]').click()
        self._browser.implicitly_wait(10)
        time.sleep(1 + random.random())

        try:
            self._browser.find_element_by_css_selector('#month > option:nth-child(%d)'%random.randint(1, 13)).click()
        except:
            self._browser.quit()
            raise ValueError('IP Mac Limited. Stop the Script...')
        else:
            self._browser.find_element_by_css_selector(r'input[id="day"]').send_keys(random.randint(1, 28))
            self._browser.find_element_by_css_selector(r'input[id="year"]').send_keys(random.randint(1990, 2000))
            time.sleep(1 + 3 * random.random())
            self._browser.find_element_by_css_selector('#gender > option:nth-child(%d)'%random.randint(1, 4)).click()
            self._browser.find_element_by_css_selector(r'div[id="personalDetailsNext"]').click()
            self._browser.implicitly_wait(10)
            time.sleep(1)
            while True:
                try:
                    self._browser.find_element_by_css_selector('.mUbCce').click()
                    time.sleep(1)
                except Exception as e:
                    print(e)
                    break
            self._browser.find_element_by_css_selector('#termsofserviceNext').click()
            self._browser.implicitly_wait(10)

            self._Donefile.write(self._username + ',' + self._pswd + '\n')
            print(self._username + ': Success')
            self._browser.quit()

    @staticmethod
    def GetUserInfo(firstnamefile, lastnamefile):
        FirstName = pd.read_csv(firstnamefile).sample(frac=1)
        LastName = pd.read_csv(lastnamefile).sample(frac=1)
        num = min(len(FirstName), len(LastName))
        if len(FirstName) > len(LastName):
            UserInfo = LastName
            UserInfo['firstname'] = FirstName.values[:num]
        else:
            UserInfo = FirstName
            UserInfo['lastname'] = LastName.values[:num]
        UserInfo.index = range(num)
        UserInfo.dropna()
        UserInfo['username'] = UserInfo['firstname'] + UserInfo['lastname'] + '31578'
        UserInfo['pswd'] = 'super' + UserInfo['firstname'] + '233'
        return UserInfo



    def RunAppsScript(self, sharedlink):
        '''So far, cannot auto totally
        
        Open sharedlink and then, plz manually finish Install. 
        '''
        self._browser.get(sharedlink)



if __name__ == '__main__':
    SharedScript = 'https://script.google.com/d/1yihwFAHrV17XHYmnrOJxQasqWGourSD57Xi-oFYO3sgY-B1_inPt5Vkc/edit?usp=sharing'

    firstnamefile = './data/CSV_Database_of_First_Names.csv'
    lastnamefile = './data/CSV_Database_of_Last_Names.csv'
    UserInfoDF = CreateGmail.GetUserInfo(firstnamefile, lastnamefile)
    for num in range(len(UserInfoDF)):
        UserInfoSeries = UserInfoDF.loc[num]
        CGM = CreateGmail(*UserInfoSeries)
        CGM.CreateAccount()
        # CGM.RunAppsScript(SharedScript)

    


