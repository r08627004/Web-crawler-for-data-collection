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


# # 爬iCheer網站
# 網址：https://www.icheers.tw/iCheers/Wine

# In[106]:


# 商品分類清單獲得
BASE_URL = 'https://www.icheers.tw/iCheers/Wine'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
rsp = requests.get(BASE_URL, headers = headers)
rsp.encoding = 'utf8'
soup = BeautifulSoup(rsp.text, 'html.parser')
category_lst = []
cate_url_lst = []
for menu in soup.findAll('ul',{'id':'Menu_Type','class':'Left_Menu_options'}):
    for li in menu.findAll('li'):
        category = li.getText().replace('\n',"")
        for a in li.findAll('a'):
            cate_url = a.get('href')
            category_lst.append(category)
            cate_url_lst.append(cate_url)
category_lst = category_lst[:-1]
cate_url_lst = cate_url_lst[:-1]
print(category_lst, cate_url_lst)


# # 以第一頁為例
# 1. 網站被JavaScript渲染
# 2. 網址規則為品項是T1...T6
# 3. 每個品項頁數是網址wine_list/後面的數字
# 4. 排除無庫存品項：https://www.icheers.tw//iCheers/Wine/WineList/wine_list/1/40/0/T1/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0
# 5. 不排除無庫存品項：https://www.icheers.tw/iCheers/Wine/WineList/wine_list/1/40/0/T1/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0/0/0/0/0

# In[3]:


# 以紅酒第一頁為例

# 排除無庫存品項：https://www.icheers.tw//iCheers/Wine/WineList/wine_list/1/40/0/T1/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0
# 不排除無庫存品項：https://www.icheers.tw/iCheers/Wine/WineList/wine_list/1/40/0/T1/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0/0/0/0/0
# 頁數為網址wine_list/後面的數字

import time
tStart = time.time()#計時開始

URL = "https://www.icheers.tw/iCheers/Wine/WineList/wine_list/1/40/0/T2/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0/0/0/0/0"
chromedriver = '/usr/local/bin/chromedriver' #要用變數指定chromedriver的放置路徑
iCheers = webdriver.Chrome(chromedriver)
#rsp.encoding = 'utf8'
iCheers.get(URL)
soup = BeautifulSoup(iCheers.page_source, 'html.parser')
Name_CH = []
Name_EN = []
Area = []
Year = []
ID = []
URL = []
Award = []
Capacity = []
Discount = []
SellingPrice = []

#第一頁
for item in soup.findAll(name='div', attrs={'class':'ALL'}):
    for ul in item.findAll(name='ul',attrs={'class':'WineInformation'}):
        name_ch = item.find('h1').getText()
        name_en = item.find('h2').getText()
        area = item.find('h3').getText().replace('\n','').replace(' ','')
        lst = ul.findAll(name='li')
        addedid = lst[0].get('addedid')
        year = lst[0].getText()
        url = lst[0].find('a').get('href')
        award = lst[1].getText().replace('\n','')
        capacity = lst[2].getText().replace('\n','')
        discount = lst[3].getText().replace('\n','')
        price = lst[5].getText().replace('\n','')
        Name_CH.append(name_ch)
        Name_EN.append(name_en)
        Area.append(area)
        ID.append(addedid)
        Year.append(year)
        URL.append(url)
        Award.append(award)
        Capacity.append(capacity)
        Discount.append(discount)
        SellingPrice.append(price)

#計時結束
tEnd = time.time()
# #列印結果
tRun = tEnd - tStart
print('run time:%d'%tRun)


# In[ ]:


### 獲得最後一頁的頁碼
page_index = []
page_url = []
pg = soup.find(name='div', attrs={'class':'Wine_Search_List_Page'})
#print(pg)
for a in pg.findAll('a'):
    pg_idx = a.getText()
    pg_url = a.get('onclick')
    page_index.append(pg_idx)
    page_url.append(pg_url)
print(page_index,page_url)


# # 開始跑一種酒類的迴圈
# 1. 爬下各品項網站的資訊
# 2. time.sleep()可設定，爬比較多的時候設12秒，比較少的時候設20秒，其實12秒就足夠

# In[178]:


# 跑一種酒類迴圈

# 排除無庫存品項：https://www.icheers.tw//iCheers/Wine/WineList/wine_list/1/40/0/T1/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0
# 不排除無庫存品項：https://www.icheers.tw/iCheers/Wine/WineList/wine_list/1/40/0/T1/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0/0/0/0/0
# 頁碼為網址wine_list/後面的數字

import time
tStart = time.time()#計時開始


Name_CH = []
Name_EN = []
Area = []
Year = []
ID = []
URL = []
Award = []
Capacity = []
Discount = []
SellingPrice = []


a_URL = 'https://www.icheers.tw/iCheers/Wine/WineList/wine_list/'
b_URL = '/40/0/T6/0/0/-1/-1/0/0/-1/-1/0/0/0/0/3/0/0/0/0/0/0/0/0/0'

chromedriver = '/usr/local/bin/chromedriver' #要用變數指定chromedriver的放置路徑
iCheers = webdriver.Chrome(chromedriver)

try:
    for i in range(1,3,1):
        print('正在爬取：第 %s 頁' % i)
        last_URL = a_URL+str(i)+b_URL
        iCheers.get(last_URL)
        soup = BeautifulSoup(iCheers.page_source, 'html.parser')
        for item in soup.findAll(name='div', attrs={'class':'ALL'}):
            for ul in item.findAll(name='ul',attrs={'class':'WineInformation'}):
                name_ch = item.find('h1').getText()
                name_en = item.find('h2').getText()
                area = item.find('h3').getText().replace('\n','').replace(' ','')
                lst = ul.findAll(name='li')
                addedid = lst[0].get('addedid')
                year = lst[0].getText().replace('\n','')
                url = lst[0].find('a').get('href')
                award = lst[1].getText().replace('\n','')
                capacity = lst[2].getText().replace('\n','')
                discount = lst[3].getText().replace('\n','')
                price = lst[5].getText().replace('\n','')
                Name_CH.append(name_ch)
                Name_EN.append(name_en)
                Area.append(area)
                ID.append(addedid)
                Year.append(year)
                URL.append(url)
                Award.append(award)
                Capacity.append(capacity)
                Discount.append(discount)
                SellingPrice.append(price)
        print('資料總共有 %d 筆' %len(Name_CH))
        time.sleep(20)
except:
    print("哪一頁出錯了"+str(i))
finally:
    iCheers.close()

#計時結束
tEnd = time.time()
# #列印結果
tRun = tEnd - tStart
print('總共爬取時間：%d秒'%tRun)


# In[179]:


c={"Name_CH" : Name_CH,
   "Name_EN" : Name_EN,
   "Area" : Area,
   "Year" : Year,
   "ID" : ID,
   "URL" : URL,
   "Award" : Award,
   "Capacity" : Capacity,
   "Discound" : Discount,
   "SellingPrice" : SellingPrice}
df = pd.DataFrame(c)

#df = pd.DataFrame(df,columns=['Date','Class','Item', 'Price', 'URL'])
print(len(df))


# In[180]:


df


# In[181]:


# 第一次存新的檔案
df.to_csv('./iCheers_加烈酒.csv', index = False)


# # 資料合併
# 將下載下來的資料合併，取出編號list來爬。

# In[4]:


from glob import glob
 
files = glob('iCheers_data/iCheers_*.csv')
print(files)

df = pd.concat(
    (pd.read_csv(file, usecols=['Name_CH','Name_EN','ID'], dtype={'Name_CH': str,'Name_EN': str, 'ID':int}) for file in files), ignore_index=True)


# In[5]:


ID_lst = df['ID'].tolist()
print(len(ID_lst))


# In[6]:


ID_lst


# # 根據編號爬下每個酒的資訊
# 1. 網址：https://www.icheers.tw/iCheers/Wine/WineDetail/wine_detail/17132
# 2. 網址後面為編號
# 3. 沒有被JavaScript渲染
# 4. 依據ID_lst，用迴圈抓下每個酒的資訊
# 5. 欄位包括編號、中文名字、英文名字、容量、定價、酒窩價、產區、法定等級、酒莊、類型、品種、酒款介紹、品飲筆記

# In[46]:


# 跑一種酒
BASE_URL = 'https://www.icheers.tw/iCheers/Wine/WineDetail/wine_detail/17132'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
rsp = requests.get(BASE_URL, headers = headers)
rsp.encoding = 'utf8'
soup = BeautifulSoup(rsp.text, 'html.parser')

ID = []
Name_CH = []
Name_EN = []
Capacity = []
OriginalPrice = []
SellingPrice = []
Area = []
Level = []
Winery = []
Flavor = []
Grape = []
Intro = []
Note = []

for menu in soup.findAll('div',{'class':'wine_detail_wineinfo_layout'}):
    name_ch = menu.find('h2').getText().replace(' ','')
    name_en = menu.find('h1').getText().replace('\n','').replace(' ','')
    for ul in menu.findAll('ul',{'class':'Detail'}):
        lst = ul.findAll(name='li')
        bar0 = lst[0].getText().replace('#','').replace('\n','')
        if bar0 == str(17132):
            ori_price = lst[1].find('strong',{'class':'wine_detail_wineinfo_OrginalPrice'}).getText()
            sell_price = lst[1].find('span').getText().replace('\n',' ')
            area = lst[2].find('em',{'class':'Info'}).getText().replace('\n','')
            level = lst[3].find('em',{'class':'Info'}).getText().replace('\n','')
            winery = lst[4].find('em',{'class':'Info'}).getText().replace('\n','')
            flavor = lst[5].find('em',{'class':'Info'}).getText().replace('\n','')
            grape = lst[6].find('em',{'class':'Info'}).getText().replace(' ','').replace('，','')
        else:
            ori_price = lst[2].find('strong',{'class':'wine_detail_wineinfo_OrginalPrice'}).getText()
            sell_price = lst[2].find('span').getText().replace('\n',' ')
            area = lst[3].find('em',{'class':'Info'}).getText().replace('\n','')
            level = lst[4].find('em',{'class':'Info'}).getText().replace('\n','')
            winery = lst[5].find('em',{'class':'Info'}).getText().replace('\n','')
            flavor = lst[6].find('em',{'class':'Info'}).getText().replace('\n','')
            grape = lst[7].find('em',{'class':'Info'}).getText().replace(' ','').replace('，','')
        
for text in soup.findAll('div',{'class':'Part'}):
    h3 = text.find('h3').getText()
    if h3 == '酒款介紹：':
        intro = text.find('p').getText().replace(' ','').replace('\n','')
    if h3 == '品飲筆記：':
        note = text.find('p').getText().replace(' ','').replace('\n','')

print(f"定價：{ori_price}\n酒窩價：{sell_price}\n產區：{area}\n法定等級：{level}\n酒莊：{winery}\n類型：{flavor}\n品種：{grape}\n酒款介紹：{intro}\n")
print(f"品飲筆記：{note}")


# # 寫迴圈
# 1. 發現每個酒品的欄位不太一致，若用lst的index去抓的話，可能會有錯誤
# 2. 因此，找到所有可能的欄位，包括產區、法定等級、酒莊、類型、品種、建議適飲期
# 3. 先讓每個欄位的value=NA，再用elseif函數填充進去，沒有填到的值則為NA
# 4. 利用try使得遇到error不會停止迴圈
# 5. 每次迴圈就建立一個DataFrame，每次都合併，最後結果叫做df
# 6. 找出了四個不同的網站 #ID_try = ['17132','18570','8703','18539']

# In[15]:


# 檢查(或刪減)ID_lst
# for i in range(500):
#     ID_lst.pop(0)
print(len(ID_lst))
print(ID_lst[976])


# In[8]:


# 迴圈跑ID_lst的每個ID

# ID_try = ['17132','18570','8703','18539','6098']
c = {}
df = pd.DataFrame()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
a_URL = 'https://www.icheers.tw/iCheers/Wine/WineDetail/wine_detail/'
for i in trange(9025,13641,1):
    URL = a_URL+str(ID_lst[i])
    rsp = requests.get(URL, headers = headers)
    rsp.encoding = 'utf8'
    soup = BeautifulSoup(rsp.text, 'html.parser')
    ID = 'NA'
    name_ch = 'NA'
    name_en = 'NA'
    ori_price = 'NA'
    sell_price = 'NA'
    area = 'NA'
    level = 'NA'
    winery = 'NA'
    flavor = 'NA'
    grape = 'NA'
    period = 'NA'
    ID = ID_lst[i]
    for menu in soup.findAll('div',{'class':'wine_detail_wineinfo_layout'}):
        name_ch = menu.find('h2').getText().replace(' ','').replace('\n','').replace('\r','')
        name_en = menu.find('h1').getText().replace('  ','').replace('\n','').replace('\r','')
        for ul in menu.findAll('ul',{'class':'Detail'}):
            lst = ul.findAll(name='li')
            bar0 = lst[0].getText().replace('#','').replace('\n','')
            try:
                if bar0 == str(ID_lst[i]):
                    ori_price = lst[1].find('strong',{'class':'wine_detail_wineinfo_OrginalPrice'}).getText()
                    sell_price = lst[1].find('span').getText().replace('\n',' ')
                else:
                    ori_price = lst[2].find('strong',{'class':'wine_detail_wineinfo_OrginalPrice'}).getText()
                    sell_price = lst[2].find('span').getText().replace('\n',' ')
            except:
                print('ID # %s 價格不存在(NA)' %ID_lst[i])
            try:
                em = ul.findAll('em')
                for j in range(0,11,2):
                    key = em[j].getText().replace('：','')
                    if key == '產區':
                        area = em[j+1].getText().replace('\n','')
                    elif key == '法定等級':
                        level = em[j+1].getText().replace('\n','')
                    elif key == '酒莊':
                        winery = em[j+1].getText().replace('\n','')
                    elif key == '類型':
                        flavor = em[j+1].getText().replace('\n','')
                    elif key == '品種':
                        grape = em[j+1].getText().replace('\n','').replace('\r','')
                    elif key == '建議適飲期':
                        period = em[j+1].getText().replace('\n','')
            except:
                print('ID # %s 有欄位產生缺值(NA)' %ID_lst[i])
    c = dict(ID=ID, Name_CH=name_ch, Name_EN=name_en, OriginalPrice=ori_price, SellingPrice=sell_price,
             Area=area, Level=level, Winery=winery, Flavor=flavor, Grape=grape, Period=period)
    df1 = pd.DataFrame(c, index=[0])
    df = pd.concat([df, df1], ignore_index=False)
#     if i == ID_lst[500]:
#         break


# In[9]:


df


# In[32]:


# 第一次存新的檔案
df.to_csv('./iCheers_data/酒品詳細資料.csv', index = False)
print(len(df))


# In[8]:


#之前存過一個CSV檔，想把之後爬的直接接在之前資料的後面
df.to_csv('./iCheers_data/酒品詳細資料.csv', index=False, mode='a', header=False)
print(len(df))


# In[9]:


# look up updates
k = pd.read_csv('./iCheers_data/酒品詳細資料.csv')
k

