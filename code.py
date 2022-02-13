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
driver.get("https://www.zocdoc.com/")

url_df=pd.DataFrame(columns=["URL"])

requirments=['Name','Specialties','Location','Overall Rating',"About","Office location",'Practice names', 'Hospital affiliations', 'Board certifications', 'Education and training', 'Professional memberships', 'Languages spoken', "Provider's gender", 'NPI number']
df=pd.DataFrame(columns=requirments)


def scrape_url(url):
    driver.get(url)
    content=driver.page_source
    soup = BeautifulSoup(content,'lxml')
    
    doc_url="https://www.zocdoc.com"
    body=soup.find(class_="wmjeqi-2 wmjeqi-3 edSdjs")
    try:
        docs=body.find_all(class_="sc-1wqwz07-5 jUsvLP")
    except:
        return
    for d in docs:
        url_df.loc[len(url_df)]=doc_url+d.a['href']

def scrape_pages():
    url=driver.page_source
    soup = BeautifulSoup(url,'lxml')

    doc_url="https://www.zocdoc.com"
    pages=[]
    body=soup.find(class_="sc-13a0bfj-0 jDHDDe wmjeqi-4 ggYHPn")
    for p in body.find_all('a'):
       pages.append(doc_url+p['href'])
    del pages[-1]

    for u in pages:
        scrape_url(u) 


   
def chrome(url):
    driver.get(url)
    driver.implicitly_wait(5)

    name=driver.find_element_by_xpath("./html/body/div/div/main/div[1]/div[1]/section/div[1]/div[2]/h1").text
    spec=driver.find_element_by_xpath("./html/body/div/div/main/div[1]/div[1]/section/div[1]/div[2]/h2[1]").text
    loc=driver.find_element_by_xpath("./html/body/div/div/main/div[1]/div[1]/section/div[1]/div[2]/h2[2]").text

    try:
        try:
            driver.find_element_by_xpath("/html/body/div/div/main/div[1]/div[3]/div[1]/section/section[1]/span/div/button").click()
            info=driver.find_element_by_xpath(".//html/body/div/div/main/div[1]/div[3]/div[1]/section/section[1]/span/div/span").text
        except:
            info=driver.find_element_by_xpath("./html/body/div/div/main/div[1]/div[3]/div[1]/section/section[1]/span/div/span").text
    except:
        info=np.nan

    content=driver.page_source
    soup = BeautifulSoup(content,'lxml')

    try:
        r=driver.find_element_by_xpath("/html/body/div/div/main/div[1]/section[1]/div[1]/div[1]/div/div[1]")
        rating=r.get_attribute('innerHTML')
    except:
        rating=np.nan
    
    if str(rating)[0].isdigit()==False:
        rating=np.nan
    
    body=soup.find(class_="sc-15hr7dd-3 rnKJZ")
    sections=body.find_all(class_="krbmlv-3 dOquxR")
    req=['Name','Specialties','Location','Overall Rating',"About","Office location"]
    for t in sections:
            if t.text not in req:
                req.append(t.text)

    div=body.find_all(class_="krbmlv-1 grdISf")
    

    oloc=[]
    try:
        odd=body.find(class_="g58yd9-6 hAgxrm")
        for t in odd.find_all("span"):
            oloc.append(t.text)
    except:
        oloc=[]
    
    address="".join(oloc)
    lang_t=[]
    for l in div[-3].find_all("li",class_="krbmlv-5 cpBnTD"):
        lang_t.append(l.text)
    lang=",".join(lang_t)

    i=[-1]*14
    for ind,x in zip(range(0,14),requirments):
        if x in req:
            i[ind]=req.index(x)
    
    pn_t=[]
    if i[6]!=-1:
        x=div[i[6]-6+1]
        for t in x.find_all("li",class_="krbmlv-5 cpBnTD"):
           pn_t.append(t.span.a.text)
    pn=",".join(pn_t)

    ha_t=[]
    if i[7]!=-1:
        x=div[i[7]-6+1]
        for t in x.find_all("li",class_="krbmlv-5 cpBnTD"):
            ha_t.append(t.text)
    ha=",".join(ha_t)  

    bc_t=[]
    if i[8]!=-1:
        x=div[i[8]-6+1]
        for t in x.find_all("li",class_="krbmlv-5 cpBnTD"):
            bc_t.append(t.text)
    bc=",".join(bc_t)

    edu_t=[]
    if i[9]!=-1:
        x=div[i[9]-6+1]
        for t in x.find_all("li",class_="krbmlv-5 cpBnTD"):
            edu_t.append(t.span.text)
    edu=",".join(edu_t)

    pm_t=[]
    if i[10]!=-1:
        x=div[i[10]-6+1]
        for t in x.find_all("li",class_="krbmlv-5 cpBnTD"):
            pm_t.append(t.text)
    pm=",".join(pm_t)
        
    npi=gender=np.nan
    if i[12]!=-1:
        npi=div[-1].p.text
    if i[13]!=-1:
        gender=div[-2].p.text
    
    quant=[name,spec,loc,rating,info,address,pn,ha,bc,edu,pm,lang,gender,npi]
    df.loc[len(df)]=quant
    print(name)
    #driver.execute_script("window.history.go(-1)")
    driver.implicitly_wait(2)


print(driver.title)

"""for i in range(8,13,1):
    path="/html/body/div/div[1]/div/footer/nav/section[4]/ul/li[{}]/span/a".format(i)
    driver.find_element_by_xpath(path).click()
    scrape_pages()      #---> to scrape url of doctors
    driver.get("https://www.zocdoc.com/")

url_df.replace(np.nan,'-',inplace=True)
print(url_df.shape)
url_df.drop_duplicates(inplace=True)
print(url_df.shape)
url_df.to_csv('urls.csv',index=False,header=True,encoding='utf-8-sig')
"""

url=pd.read_csv("urls.csv")
links=url["URL"]

for l in links:
    chrome(l)

df.replace(np.nan,'-',inplace=True)
df.replace('','-',inplace=True)
df.drop_duplicates(inplace=True)
df.to_csv('scraper_results.csv',index=False,header=True,encoding='utf-8-sig')
