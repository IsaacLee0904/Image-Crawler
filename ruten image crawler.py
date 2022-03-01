# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
### import package for img crawler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib
from bs4 import BeautifulSoup
import requests
### import package for title crawler
import pandas as pd


### open chrome webdriver
driver = webdriver.Chrome('C:\chromedriver_win32/chromedriver.exe') # must change while using different PC
driver.get('https://www.google.com.tw/imghp?hl=zh-TW&ogbl')

### input keyword
box = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')  # must change while using different PC
keyword = input("請輸入關鍵字 : ")
box.send_keys(str(keyword)) ## input the keyword have to change into the input type!!!
box.send_keys(Keys.ENTER)

#Will keep scrolling down the webpage until it cannot scroll no more
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    new_height = driver.execute_script('return document.body.scrollHeight')
    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div[2]/div[1]/div[2]/div[2]/input').click() # must change while using different PC
        time.sleep(2)
    except:
        pass
    if new_height == last_height:
        break
    last_height = new_height
    
### set up for loading img
## set a empty foldername
foldername = keyword
if not os.path.isdir(foldername): 
        os.mkdir(foldername)   
## set up url 
url = "https://www.google.com.tw/search?q=" + keyword + "&hl=zh-TW&tbm=isch&source=hp&biw=1034&bih=576&ei=4AyOYc2HJZP_0ATv65aoDA&iflsig=ALs-wAMAAAAAYY4a8F76CY3N6-r1WyREtXjWGnW7hofy&oq=" + keyword + "&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMggIABCABBCxAzIFCAAQgAQyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyBQgAEIAEMgUIABCABDIFCAAQgARQAFg5YNUBaABwAHgBgAGLAYgBnwOSAQMxLjOYAQCgAQGqAQtnd3Mtd2l6LWltZw&sclient=img&ved=0ahUKEwjN9_ifnJL0AhWTP5QKHe-1BcUQ4dUDCAY&uact=5"
# print(url) # debug for checking url(OK)
## set up dic to check if the img url exist
img_url_dic = {}  
title_url_dic = {}
## set up dataframe for title
df = pd.DataFrame()
filenamelist = []
### start to load img
m = 1 # 圖片編號 
while m <= 20 : # 要抓的數量
    for element in driver.find_elements_by_xpath('//*[@id="islrg"]/div[1]/div['+ str(m) +']/a[1]/div[1]/img'):
        try:
            img_url = element.get_attribute('src')
            if img_url != None and not img_url in img_url_dic:
                    img_url_dic[img_url] = ''  
                    #print(img_url) # debug : check if url is load(OK)
                    filename = keyword + '(' + str(m) + ')' +'.jpg'
                    print(filename) # make sure how many images were loaded  
                    filenamelist.append(filename)
                    #print(filenamelist) # debug : check if filename add to filenamelist(ok)
                    urllib.request.urlretrieve(img_url,os.path.join(foldername, filename))
                    m += 1
                    df = pd.DataFrame(filenamelist)
### keep image to the folder                   
        except OSError:
            print('發生OSError!')
            break 
#print('ok') # for debug : if upper function non error
# output dataframe as csv file : 1.filename 2.imgname 3.label
df.to_csv('final.csv', index = False) # index = False to output without index
### close the web while finish download
print('完成下載')
#driver.close() # close the windows





   

    
    







