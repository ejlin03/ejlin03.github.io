

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


def MomoSearch(str):
    SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[id="keyword"]')
    SearchTextBox.send_keys(str)
    SearchButton = driver.find_element(By.CSS_SELECTOR, 'button[title="搜尋"]')
    SearchButton.click()
    time.sleep(2)
    SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[id="keyword"]')
    SearchTextBox.clear()

def PchomeSearch(str):
    try:
        SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    except:
        SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[id="keyword"]')
    SearchTextBox.send_keys(str)
    try:
        SearchButton = driver.find_element(By.CSS_SELECTOR, 'button[data-regression="header_search_button"]')
    except:
        SearchButton = driver.find_element(By.CSS_SELECTOR, 'input[type="button"]')        
    SearchButton.click()
    time.sleep(2)
    SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[id="keyword"]')
    SearchTextBox.clear()    

def BookSearch(str):
    try:
        ad = driver.find_element(By.CSS_SELECTOR, 'a[title="關閉廣告"]')
        ad.click()
    except: pass
    SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    SearchTextBox.send_keys(str)
    time.sleep(1)
    SearchButton = driver.find_element(By.CSS_SELECTOR, 'button[title="搜尋"]')
    SearchButton.click()
    time.sleep(2)
    SearchTextBox = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
    SearchTextBox.clear()
    time.sleep(1)
    
def MomoGetProducts(target):
    ProductList = driver.find_elements(By.CSS_SELECTOR, 'div[class="listArea"] li')
    final_df = pd.DataFrame()
    count = 0
    for product in ProductList:
        count += 1
        name = product.find_element(By.CSS_SELECTOR,'div[class="prdNameTitle"]').text
        price = product.find_element(By.CSS_SELECTOR,'p[class="money"]').text
        if '(' in price:
            price = price.split('(')[0]
        price = price.replace(',','').replace('$','')
        if price == '':
            continue
        website = product.find_element(By.CSS_SELECTOR,'a[class="goodsUrl"]').get_attribute('href')
        df = pd.DataFrame({'查詢關鍵字':[target],
                           '商品名稱':[name],
                           '價格':[price],
                           '商品連結':[website]})
        final_df = pd.concat([final_df,df],axis=0)
        if count == 5: break
    if count == 0:
        df = pd.DataFrame({'查詢關鍵字':[target],
                           '商品名稱':['None'],
                           '價格':['None'],
                           '商品連結':['None']})
        final_df = pd.concat([final_df,df],axis=0)
    return final_df

def PchomeGetProducts(target):
    ProductList = driver.find_elements(By.CSS_SELECTOR, 'div[id="ItemContainer"] dl')
    final_df = pd.DataFrame()
    count = 0
    for product in ProductList:
        try:
            if driver.find_elements(By.CSS_SELECTOR, 'div[id="notMustfound"][style="display: block;"]'):
                break
        except: pass
        count += 1
        name = product.find_element(By.CSS_SELECTOR,'h5[class="prod_name"]').text
        price = product.find_element(By.CSS_SELECTOR,'span[class="price"]').text
        price = price.replace('$','')
        website = product.find_element(By.CSS_SELECTOR,'h5[class="prod_name"]>a').get_attribute('href')
        df = pd.DataFrame({'查詢關鍵字':[target],
                           '商品名稱':[name],
                           '價格':[price],
                           '商品連結':[website]})
        final_df = pd.concat([final_df,df],axis=0)
        if count == 5: break
    while count < 5:
        count += 1
        df = pd.DataFrame({'查詢關鍵字':[target],
                           '商品名稱':['None'],
                           '價格':['None'],
                           '商品連結':['None']})
        final_df = pd.concat([final_df,df],axis=0)
    return final_df

def BookGetProducts(target):
    Rows = driver.find_elements(By.CSS_SELECTOR,'div[class="table-searchbox clearfix"] div[class="mod2 table-container"]')
    final_df = pd.DataFrame()
    count = 0
    ProductList = Rows[0].find_elements(By.CSS_SELECTOR, 'div[class="table-td"]')
    for row in Rows:
        row = row.find_element(By.CSS_SELECTOR, 'div[class="table-tr"]')
        ProductList = row.find_elements(By.CSS_SELECTOR, 'div[class="table-td"]')
        for product in ProductList:
            count += 1
            name = product.find_element(By.CSS_SELECTOR,'h4>a').text
            price = product.find_element(By.CSS_SELECTOR,'ul[class="price clearfix"]>li>b').text
            website = product.find_element(By.CSS_SELECTOR,'h4>a').get_attribute('href')
            df = pd.DataFrame({'查詢關鍵字':[target],
                           '商品名稱':[name],
                           '價格':[price],
                           '商品連結':[website]})
            final_df = pd.concat([final_df,df],axis=0)
            if count == 5: break
        if count == 5: break
    while count < 5:
        count += 1
        df = pd.DataFrame({'查詢關鍵字':[target],
                           '商品名稱':['None'],
                           '價格':['None'],
                           '商品連結':['None']})
        final_df = pd.concat([final_df,df],axis=0)
    return final_df


target =  input("請輸入查詢關鍵字：")

driver_file = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_file))
url = "https://www.momoshop.com.tw/main/Main.jsp"
driver.get(url)
time.sleep(1)

MomoProducts = pd.DataFrame()
MomoSearch(target)
time.sleep(1)
Products = MomoGetProducts(target)
MomoProducts = pd.concat([MomoProducts,Products],axis=0)

driver.close()




driver_file = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_file))
url = "https://24h.pchome.com.tw/"
driver.get(url)
time.sleep(1)

PchomeProducts = pd.DataFrame()
PchomeSearch(target)
time.sleep(1)
Products = PchomeGetProducts(target)
PchomeProducts = pd.concat([PchomeProducts,Products],axis=0)

driver.close()




driver_file = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(driver_file))
url = "https://www.books.com.tw/"
driver.get(url)
time.sleep(1)

BookProducts = pd.DataFrame()
BookSearch(target)
time.sleep(1)
Products = BookGetProducts(target)
BookProducts = pd.concat([BookProducts,Products],axis=0)

driver.close()

SMomoProducts = MomoProducts.set_index('查詢關鍵字').add_suffix('_momo')
SPchomeProducts = PchomeProducts.set_index('查詢關鍵字').add_suffix('_pchome')
SBookProducts = BookProducts.set_index('查詢關鍵字').add_suffix('_book')
AllProduct = pd.concat([SMomoProducts, SPchomeProducts, SBookProducts], axis=1)
AllProduct.to_csv('Product.csv')


# In[ ]:





# In[ ]:





# In[ ]:




