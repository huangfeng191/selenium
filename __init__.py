from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
url="http://quote.eastmoney.com/center/boardlist.html#industry_board"
def get_selenium(url,browser=None ):
    if not browser :
        browser = webdriver.Chrome()  # Chrome浏览器
    browser.get(url)  # 打开url网页 比如 driver.get("http://www.baidu.com")
    soup = BeautifulSoup(browser.page_source)
    return soup

# $("a.next.paginate_button")
def get_table(browser,table_id,df=None):

    next_xpath = '//*[@id="main-table_paginate"]/a[2]'
    soap = BeautifulSoup(browser.page_source, features="lxml")
    soap_dom = soap.find(id=table_id)
    if (soap_dom):
        df_temp=html_to_df(str(soap_dom)) or None
        if len(df_temp)>0:
            df_temp=df_temp[0]
            df=pd.concat([df, df_temp])

        next_dom = browser.find_element_by_xpath(next_xpath)
        if "disabled" not in next_dom.get_attribute("class"):
            next_dom.click()
            get_table(browser,table_id,df)
    return df

def get_all_tables(baseUrl,table_id='table_wrapper-table'):
    next_xpath = '//*[@id="main-table_paginate"]/a[2]'
    df=pd.DataFrame([])
    browser = webdriver.Chrome()
    browser.get(baseUrl)
    df=get_table(browser,table_id,df)
    return df




def html_to_df(html):
    df=pd.read_html(html)
    return df



if __name__=="__main__":
    df= get_all_tables(url)
    pass


if __name__=="__main__1":
    soap= get_selenium(url)
    soap_dom=soap.find(id="table_wrapper-table")
    if(soap_dom):
        df=html_to_df(str(soap_dom))

    pass
# pd.concat([df[0].loc[0:,:],df[0].loc[0:,:]])

# 按面向对象实现, 会有很多的 benefit

