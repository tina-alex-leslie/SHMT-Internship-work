import contextlib
from os import name
from typing import final
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



def extract_issues():
    driver=webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe",options=options)
    driver.maximize_window()
    practo_specs = []
    spec_link=[]

    specialities_urls = ['https://www.practo.com/sitemap/specialities',
                     'https://www.practo.com/sitemap/specialities/page-2']

    for url in specialities_urls:
        driver.get(url=url)
        wait = WebDriverWait(driver, 10)

        all_specialities = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[3]')
        specs = all_specialities.find_elements_by_tag_name('a')
        practo_specs.extend([i.text for i in specs])
        spec_link.extend([i.get_attribute('href') for i in specs])

    print('Spec links- Done')

    doc=[]
        
    for i in spec_link:
        temp=[]
        driver.get(i)
        try:
            url=driver.find_element_by_id("doctors")
            doc_links = url.find_elements_by_tag_name('a')
            temp.extend([i.get_attribute('href')+"/recommended" for i in doc_links])
            temp=list(set(temp))
        except:
            temp='-'
        doc.append(temp)

    print("Doctor info- Done")

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
    print("Issues- Done")
    df=pd.DataFrame(list(zip(practo_specs,all_issues)))
    df.to_csv("issues.csv",index=False,header=False)


def remove_empty_issues():
    df=pd.read_csv("issues.csv")
    df.columns=[0,1]
    missing_issues=df[df[1]=='[]'][0]
    df=df[df[1]!='[]']
    df.to_csv("final.csv",index=False,header=False)
    missing_issues.to_csv("missing_issues.csv",index=False,header=False)


def camel_case():
    needed=['AIDS',"TREATMENT FOR DIABETES TYPE - II & I","TREATMENT FOR UTI (URINARY TRACT INFECTION)",'ARF','EVD','HIV','DES','HPV','CRE','COPD','COVID-19','MND','PRP','RCT','CABG','VEMP','II','UTI','MICS','TURP','2D','EVD','HAIs','HPV','LGV','MRSA','NSU','OCD','PID','PTSD','RHD','STIs',
            'NSU','MRSA','TB','VRE','ICSI','GYN','OBS','ECG','PCOD/PCOS','UI','UTI','MVR','CKD','C Section','Hepatitis B Treatment', 'ENT Emergency Visit', 'C3R for Keratoconus; RETINA - FFA/OCT', 'Pelvic Inflammatory Disease- PID', 'CHEMO', 'ENT Checkup (General)', 'TMJ Disorders', 'GERD', 'CT Scan Report - Lungs', 'ENT Follow Up','HPV Vaccination', 'ANXIETY', 'MRI Report - Foot and Ankle', 'Acute Kidney Disease ( AKI ) Treatment', 'HIV / AIDS', 'D J Stent Removal', 'Bypass Surgery Consultation - CABG', 'RCT - Root Canal Treatment', 'Diet For A Healthy Skin', 
    'GIC Tooth Fillings', 'PRP ( PLATELET RICH PLASMA ) for Hair Thinning', 'Neurostimulation / TENS', 'OCD', 'DEPRESSION', 'Elevated PSA', 'PRP for Hairfall',  'ENT Consultation', 'BIPOLAR', 'PET / CT Scan Report', 'Hepatitis C Treatment', 'ENT Problems', 'IVC Filter Insertion', 'Intermittant and Continuous-Cervical', 'PRP for Hair Loss', 'Pregnancy with PCOD', 'IUD placement', 'IUD Insertion', 'ECG / EKG', 'PCOD', 'Copper T Insertion', 'LASIK Eye Surgery', 'RCT - Single Sitting', 'Annual Pap Smear / GYN Exam', 'HIV AIDS',
     'TB', 'PCOS', 'UTI', 'HAIR CARE SERVICES', 'IUD Removal', 'MRI - Spinal Cord', 'PRP Treatment', 'Hepatitis B Vaccine', 'Hepatitis B', 'PRP for hair loss', 'Bone Density Measurement / DXA Scan', 'STD', 'Irritable Bowel Syndrome ( IBS ) Treatment', 'LGBT Care', 'MANIA', 'IFT', 'OCD Treatment', 'OB / GYN Emergency', 'CT Scan Report - Head', 'FUE Hair Transplant', 'CT Scan Report - Other', 'Copper T Insertion & Removal', 'HIV Pre-Exposure Prophylaxis (PrEP)', 'UTI (URINARY TRACT INFECTION)',  'Chest CT Scan Abnormalities', 'MRI Test - Brain', 'PCOD/ PCOS Diet Counselling', 'MRI Report - Breast', 'CORNEA - Transplant', 'MRI Report - Brain',
    'BPS Dentures Fixing', 'FUT Hair Transplant', 'Abnormal MRI', 'MRI Report - Back / Spine', 'Implant / RCT', 'CT Scan - Teeth (Dental Scan)', 'SLAP Tear / SLAP Lesion', 'Abnormal EMG', '(R/A)', 'LEEP Procedure (For Abnormal Pap Smear)', 'Chronic Kidney Disease ( CKD )', 'BERA Test', 'II', 'BTE and RIC Hearing Aids', 'UPJ Obstruction', 'PET Scan', 'COUNSELLING/ PSYCHOTHERAPY', 'TMJ Pain Management', 'PRP Hair Transplantation', 'MRI Report - Other'
            ]
    df=pd.read_csv("new.csv")
    df.columns=[0,1]
    #65
    for x in range(0,65):
        l=(df.iloc[x])[1]
        l=l[1:-1]
        l=l.replace("'","")
        issues_list=l.split(',')
        for i in range(0,len(issues_list)):
            issues_list[i]=issues_list[i].strip(' ')
            temp_res=[ele for ele in needed if(ele in issues_list[i])]
            if any(issues_list[i] in str for str in needed):
                continue
            elif bool(temp_res):
                continue
            else:
                temp=issues_list[i].split(' ')

                res=''
                res=res+' '.join(t.capitalize() for t in temp)
                issues_list[i]=res
        df.loc[x,1]=issues_list

    df.to_csv("extracted_issues.csv",header=False,index=False)


def make():
    df=pd.read_csv("extracted_issues.csv")
    df.columns=[0,1]

    col=df[0]
    cont=df[1]
    res=[]
    final_df=pd.DataFrame()
    for l in cont:
        l=l[1:-1]
        l=l.replace("'","")
        issues_list=l.split(',')
        
        for i in range(0,len(issues_list)):
            issues_list[i]=issues_list[i].strip(' ')
        
        res.append(issues_list)
        
    for name,r in zip(col,res):
        temp=pd.DataFrame()
        temp[name]=r
        final_df=pd.concat([final_df,temp],ignore_index=True, axis=1)
    
    final_df.columns=col
    final_df.to_csv("practo_issues_final.csv",index=False)


def temp():
    needed=['AIDS','ARF','EVD','HIV','DES','HPV','CRE','COPD','COVID-19','MND','PRP','RCT','CABG','VEMP','II','UTI','MICS','TURP','2D','EVD','HAIs','HPV','LGV','MRSA','NSU','OCD','PID','PTSD','RHD','STIs',
            'NSU','MRSA','TB','VRE','ICSI','GYN','OBS','ECG','PCOD/PCOS','UI','UTI','MVR','CKD','C Section','Hepatitis B Treatment', 'ENT Emergency Visit', 'C3R for Keratoconus; RETINA - FFA/OCT', 'Pelvic Inflammatory Disease- PID', 'CHEMO', 'ENT Checkup (General)', 'TMJ Disorders', 'GERD', 'CT Scan Report - Lungs', 'ENT Follow Up', 'ANTIAGEING SOLUTIONS', 'SPINE DISORDERS', 'HPV Vaccination', 'ANXIETY', 'MRI Report - Foot and Ankle', 'Acute Kidney Disease ( AKI ) Treatment', 'HIV / AIDS', 'D J Stent Removal', 'Bypass Surgery Consultation - CABG', 'RCT - Root Canal Treatment', 'Diet For A Healthy Skin', 
    'GIC Tooth Fillings', 'PRP ( PLATELET RICH PLASMA ) for Hair Thinning', 'Neurostimulation / TENS', 'OCD', 'DEPRESSION', 'Elevated PSA', 'PRP for Hairfall', 'PANIC ATTACKS', 'ENT Consultation', 'BIPOLAR', 'PET / CT Scan Report', 'Hepatitis C Treatment', 'ENT Problems', 'IVC Filter Insertion', 'intermittant and Continuous-Cervical', 'PRP for Hair Loss', 'Pregnancy with PCOD', 'IUD placement', 'IUD Insertion', 'TREATMENT FOR PSORIASIS & ECZEMA', 'ECG / EKG', 'PCOD', 'Copper T Insertion', 'LASIK Eye Surgery', 'RCT - Single Sitting', 'Annual Pap Smear / GYN Exam', 'HIV AIDS',
     'TB', 'PCOS', 'UTI', 'HAIR CARE SERVICES', 'IUD Removal', 'MRI - Spinal Cord', 'PRP Treatment', 'Hepatitis B Vaccine', 'Hepatitis B', 'PRP for hair loss', 'Bone Density Measurement / DXA Scan', 'STD check up & Treatment', 'Irritable Bowel Syndrome ( IBS ) Treatment', 'LGBT Care', 'MANIA', 'IFT', 'OCD Treatment', 'OB / GYN Emergency', 'CT Scan Report - Head', 'TREATMENT FOR SPINE PROBLEM', 'FUE Hair Transplant', 'CT Scan Report - Other', 'Copper T Insertion & Removal', 'HIV Pre-Exposure Prophylaxis (PrEP)', 'TREATMENT FOR UTI (URINARY TRACT INFECTION)', 'MENTAL RETARDATION/ BEHAVIORAL PROBLEMS', 'Chest CT Scan Abnormalities', 'TREATMENT FOR PCOD/PCOS', 'MRI Test - Brain', 'PCOD/ PCOS Diet Counselling', 'MRI Report - Breast', 'CORNEA - Transplant', 'MRI Report - Brain',
    'BPS Dentures Fixing', 'FUT Hair Transplant', 'Abnormal MRI', 'MRI Report - Back / Spine', 'Implant / RCT', 'CT Scan - Teeth (Dental Scan)', 'SLAP Tear / SLAP Lesion', 'SCHIZOPHRENIA', 'Abnormal EMG', 'TREATMENT FOR JOINT PAIN (R/A)', 'LEEP Procedure (For Abnormal Pap Smear)', 'TREATMENT FOR BACK ACHE', 'Chronic Kidney Disease ( CKD )', 'BERA Test', 'TREATMENT FOR DIABETES TYPE - II & I', 'BTE and RIC Hearing Aids', 'UPJ Obstruction', 'PET Scan', 'COUNSELLING/ PSYCHOTHERAPY', 'TMJ Pain Management', 'PRP Hair Transplantation', 'TREATMENT FOR PAIN & ACHES', 'MRI Report - Other'
            ]
    
    xls=pd.ExcelFile('final_conditions.xlsx')
    df = pd.read_excel(xls, 'merged')
    final=[]
    for col in df.columns:
        temp=df[col].tolist()
        final.append(temp)
    
    temp=pd.DataFrame(list(zip(df.columns,final)))
    temp.to_csv("new.csv",index=False,header=False)
    print(temp[:5])

def temp2():
    df=pd.read_csv('new.csv')
    df.columns=[0,1]
    list1=df[1]
    final=[]
    for t in list1:
        t=t[1:-1]
        t=t.replace("'","")
        issues_list=t.split(',')
        for i in range(0,len(issues_list)):
            issues_list[i]=issues_list[i].strip(' ')
        issues_list=list(set(issues_list))
        issues_list.remove('nan')
        final.append(issues_list)

    col=list(df[0])
    temp=pd.DataFrame(list(zip(col,final)))
    temp.to_csv("new.csv",index=False,header=False)
    print(temp[:5])

#87
def surgical():
    xls=pd.ExcelFile('final_conditions.xlsx')
    df = pd.read_excel(xls, 'Sheet1')
    col=df.columns
    terms=["Surgery","surgery","surgical","Surgical"]
    final=[]
    
    for i in col:
        temp=[]
        issues_list=df[i].tolist()
        try:
            lim=issues_list.index(np.nan)
        except:
            lim=len(issues_list)
        for j in issues_list[:lim]:
            if "Surgery" in j or "surgery" in j or "surgical" in j or "Surgical" in j:
                temp.append(j)
        final.append(temp)

    temp=pd.DataFrame(list(zip(col,final)))
    temp.to_csv("new.csv",index=False,header=False)
    print(temp[:5])
           


            


#temp2()
#temp()
#make()

#camel_case()
#extract_issues() #<---extract issues
#remove_empty_issues() #<--remove []

surgical()