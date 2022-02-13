import contextlib
from os import name
from bs4 import element
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

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

global driver
driver=webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe",options=options)
driver.maximize_window()

practo_specs = []

specialities_urls = ['https://www.practo.com/sitemap/specialities',
                     'https://www.practo.com/sitemap/specialities/page-2']

for url in specialities_urls:
    driver.get(url=url)
    wait = WebDriverWait(driver, 10)

    all_specialities = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]')
    specs = all_specialities.find_elements_by_tag_name('a')
    practo_specs.extend([i.text for i in specs])

pd.Series(practo_specs).to_csv('practo_specialities.csv', index=False, header=False)
print('Saved practo landing page specialities')

# PATIENT LINKS #############################################################################################
url = 'https://www.practo.com/doctors'

driver.get(url=url)
wait = WebDriverWait(driver, 10)

# XPATHS
search_box_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/input'
others_button_xpath = '/html/body/div[1]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div'
specs_list_xpath = '//*[@id="container"]/div[2]/div[1]/div[1]/div[3]/div[2]/div/div'
doctor_xpath = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[3]'
doctor_xpath2 = '/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[3]'

# select a speciality
others_button = driver.find_element_by_xpath(others_button_xpath)
others_button.click()

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, specs_list_xpath))
)
specs = element.find_elements_by_class_name('c-speciality__icons')
practo_specialities_name = [i.text for i in specs]
pd.Series(practo_specialities_name).to_csv('practo_main_specialities.csv', index=False, header=False)
print('Saved speciality names')

practo_specialities = [i.get_attribute('href') for i in specs]

stories_links = []
for i in practo_specialities:
    driver.get(i)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, doctor_xpath))
        )
        stories_links.append(element.find_element_by_xpath(
            '//*[@id="container"]/div[3]/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[3]/div/a[2]').get_attribute('href'))
    
    except:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, doctor_xpath2))
        )
        stories_links.append(element.find_element_by_xpath(
            '//*[@id="container"]/div[3]/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[3]/div/a[2]').get_attribute('href'))

pd.Series(stories_links).to_csv('practo_stories_links.csv', index=False, header=False)
print('Saved patient story links')

# GETTING ISSUES ###############################################################################################
urls = [i[0] for i in pd.read_csv('practo_stories_links.csv', header=None).values]

# XPATHS
issues_list_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div'
issue_inner_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div/div[2]'

all_issues = []
for url in urls:
    print()
    print(url)
    driver.get(url=url)
    wait = WebDriverWait(driver, 10)

    issues_button = driver.find_element_by_xpath(issues_list_xpath)
    issues_button.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, issue_inner_xpath))
    )
    element = element.find_elements_by_tag_name('div')
    issues = [i.text for i in element]
    all_issues.append(issues)

pd.DataFrame(all_issues).to_csv('practo_issues_list.csv', index=False, header=False)
print('Saved issues')
