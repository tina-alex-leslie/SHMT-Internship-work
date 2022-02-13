#Occupational Therapy (specialty name and issue is same), Pediatric Ot, Pediatric Physiotherapy and Radiology
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


options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

global driver
driver=webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe",options=options)
driver.maximize_window()


spec_urls=["https://www.practo.com/occupational-therapy","https://www.practo.com/pediatric-ot",
    "https://www.practo.com/pediatric-physiotherapy","https://www.practo.com/radiology"]

for url in spec_urls:
    issues=[]
    driver.get(urk)
