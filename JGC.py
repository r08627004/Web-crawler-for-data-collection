#!/usr/bin/env python
# coding: utf-8

# # 載入套件
# BeautifulSoup、Selenium、time、pandas等等

# In[1]:


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import time
import re
import json
import sys
from tqdm.notebook import trange, tqdm #加進度條


# # 爬酒條通網站
# 網址：https://www.609.com.tw/Country

# In[2]:


# 爬葡萄酒
Base_url = 'https://www.609.com.tw/Country'
chromedriver = '/usr/local/bin/chromedriver' 
driver = webdriver.Chrome(chromedriver)

# # chrome_options.add_argument(‘–headless’)
# # chrome_options.add_argument(‘–disable-gpu’)
# # browser = webdriver.Chrome(options=chrome_options,executable_path=’chromedriver.exe’)

driver.get(Base_url) 


# 先點葡萄酒
element = driver.find_element_by_link_text("葡萄酒")
element.click()
time.sleep(0.5)
# 點品項
item = driver.find_element_by_xpath('//*[@id="list-13"]/div[4]/div[1]/a')
driver.execute_script("arguments[0].click();",item)
#item.click()
# 解析網站
soup = BeautifulSoup(driver.page_source, 'html.parser')
for menu in soup.findAll('div',{'class':'card mb-3 text-center'}):
    name = menu.find('h6').getText()
    url = menu.find('div',{'class':'mt-1'}).find('a').get('href')
    price = menu.find('div',{'class':'text-center'}).getText()
    print(f'酒名：{name}\n網址：{url}\n價格：{price}')


# In[3]:


# 定義函數
def test(self,xpath):
    element = self.find_element_by_link_text("葡萄酒")
    element.click()
    time.sleep(0.5)
    try:
        item = self.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].click();",item)
        time.sleep(0.3)
        # 解析網站
        soup = BeautifulSoup(self.page_source, 'html.parser')
        for menu in soup.findAll('div',{'class':'card mb-3 text-center'}):
            name = menu.find('h6').getText()
            url = menu.find('div',{'class':'mt-1'}).find('a').get('href')
            price = menu.find('div',{'class':'text-center'}).getText()
            Name.append(name)
            URL.append(url)
            Price.append(price)
        self.back()
    except:
        print(f'迴圈到{xpath}沒有資料')


# In[4]:


# 建立Xpath list
Xpath = []
num_lst = [18,6,3,3,6,6,
           4,6,3,3,3,2,4,2]
for i in range(14):
    for j in range(1,num_lst[i]):
        xpath = '//*[@id="list-13"]/div[%d]/div[%d]/a' % ((i+1)*2,j)
        Xpath.append(xpath)
print(Xpath)


# In[5]:


Base_url = 'https://www.609.com.tw/Country'
chromedriver = '/usr/local/bin/chromedriver' 
driver = webdriver.Chrome(chromedriver)


# # chrome_options.add_argument(‘–headless’)
# # chrome_options.add_argument(‘–disable-gpu’)
# # browser = webdriver.Chrome(options=chrome_options,executable_path=’chromedriver.exe’)

driver.get(Base_url)
Name = []
URL = []
Price = []
for i in Xpath:
    test(driver,i)


# In[9]:


len(Name)


# In[11]:


c = {'Name' : Name,
    'URL' : URL,
    'Price' : Price}
df = pd.DataFrame(c)
df


# In[12]:


# 第一次存新的檔案
df.to_csv('./酒條通/酒品編號.csv', index = False)
print(len(df))


# In[ ]:


#之前存過一個CSV檔，想把之後爬的直接接在之前資料的後面
df.to_csv('./酒條通/酒品編號.csv', index=False, mode='a', header=False)
print(len(df))


# In[3]:


# look up updates
k = pd.read_csv('./酒條通/酒品編號.csv')
k


# In[110]:


# 香檳氣泡酒
Name = []
URL = []
Price = []

chromedriver = '/usr/local/bin/chromedriver' 
driver = webdriver.Chrome(chromedriver)
Base_URL = 'https://www.609.com.tw/ProductList/'
item = ['香檳','氣泡酒']
for i in item:
    item_URL = Base_URL+str(i)
    driver.get(item_URL)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for menu in soup.findAll('div',{'class':'card mb-3 text-center'}):
        name = menu.find('h6').getText()
        url = menu.find('div',{'class':'mt-1'}).find('a').get('href')
        price = menu.find('div',{'class':'text-center'}).getText()
        Name.append(name)
        URL.append(url)
        Price.append(price)
    print('%s 資料總共有 %d 筆' %(str(i),len(Name)))


# In[111]:


c = {'Name' : Name,
     'URL' : URL,
     'Price' : Price}
df = pd.DataFrame(c)
df


# In[21]:


#之前存過一個CSV檔，想把之後爬的直接接在之前資料的後面
df.to_csv('./酒條通/酒品編號.csv', index=False, mode='a', header=False)
print(len(df))


# In[14]:


# look up updates
k = pd.read_csv('./酒條通/酒品編號.csv')
k


# # 抓取每個產品的資訊

# In[15]:


# 建立ID List
ID_lst = k['URL'].tolist()
print(len(ID_lst))


# In[16]:


# 用以整理文字的函數
def not_empty(s):
    return s and s.strip()


# In[17]:


df = pd.DataFrame()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
Base_URL = 'https://www.609.com.tw'
for i in trange(403):
    ID = ID_lst[i]
    URL = Base_URL + ID
    rsp = requests.get(URL, headers = headers)
    rsp.encoding = 'utf8'
    soup = BeautifulSoup(rsp.text, 'html.parser')
    # 中文與英文名字
    name_ch = soup.find('div',{'style':'font-size:20px;font-weight:400;'}).getText().strip()
    name_en = soup.find('div',{'style':'font-size:16px;color:#721c24;'}).getText().strip()
    # 品號、參考價、市場價
    info = soup.findAll('div',{'class':'col-sm-6'})
    info1 = info[0].getText().replace(' ','|').replace('\r','|').replace('\n','|').split('|')
    res = list(filter(not_empty, info1))
    
    c = dict(中文名稱=name_ch,英文名稱=name_en,品號=res[1],參考價=res[3],市場價=res[5])
    df1 = pd.DataFrame(c, index=[0])

    # 表格（酒精濃度、產地、容量）
    tb = pd.read_html(URL)
    df2 = tb[0]

    # 合併前兩者
    df_temp = df1.merge(df2, how='inner', left_index=True, right_index=True)

    # 產品介紹
    info3 = soup.find('div',{'style':'font-weight:300;'}).getText().strip()
    df_temp['產品介紹'] = info3
    df = pd.concat([df, df_temp], ignore_index=False)


# In[30]:


df_temp


# In[108]:


df


# In[109]:


# 存成excel
df.to_excel('./酒條通/各項酒品資訊.xlsx', index = False)


# 補充：上面沒用到的Selenium功能

# In[ ]:


# 隐式等待，等待时间内找出来就返回，找不出来就报错
driver.implicitly_wait(20)
# 捲頁
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


# In[ ]:





# In[ ]:




