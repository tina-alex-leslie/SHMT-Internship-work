import contextlib
from os import name
from bs4 import element
from pandas._libs import missing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
import requests
from bs4 import  BeautifulSoup
from datetime import date
from selenium.webdriver.firefox.webdriver import WebDriver
import pandas as pd
import numpy as np
import itertools
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

global driver
driver=webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe",options=options)
driver.maximize_window()
def issues(doc):
    issues_list_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div'
    issue_inner_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div/div[2]'
    all_issues=[]

   
    for li in doc:
        issues=[]
        if li!='-':
            for link in li:
                driver.implicitly_wait(3)
                driver.get(link)
                try:
                    issues_button = driver.find_element_by_xpath(issues_list_xpath)
                    issues_button.click()

                    element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, issue_inner_xpath))
                            )
                    element = element.find_elements_by_tag_name('div')
                    temp = [i.text for i in element]
                    temp2=[txt.replace("\n",',') for txt in temp]
                    temp3=[txt.split(',') for txt in temp2]
                    temp4=[]
                    for t in temp3:
                        temp4.extend(t)
                    issues.extend(temp4)
                    issues=list(set(issues))
                except:
                    pass
        all_issues.append(issues)
    return all_issues
#Occupational Therapy (specialty name and issue is same), Pediatric Ot, Pediatric Physiotherapy and Radiology

def extra_issues():
    link=["https://www.practo.com/occupational-therapy","https://www.practo.com/pediatric-ot","https://www.practo.com/pediatric-physiotherapy","https://www.practo.com/radiology"]
    doc=[]
    for l in ["https://www.practo.com/radiology"]:
        temp=[]
        driver.get(l)
        url=driver.find_element_by_id("doctors")
        doc_links = url.find_elements_by_tag_name('a')
        temp.extend([i.get_attribute('href')+"/recommended" for i in doc_links])
        temp=list(set(temp))
        doc.append(temp)

    
    print(issues(doc))
#extra_issues()


def make():
    df=pd.read_csv