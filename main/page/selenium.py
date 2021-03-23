from main.page import Table
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from main.page.service import treasure_industry

from main.utils.time import getToday_s
import time
class SeleniumTable(Table):
    browser=None
    def __init__(self,id,nextButton,url,columns=None,fields=None,**kwargs):
        self.id = id
        self.nextButton = nextButton
        self.df = None
        self.url = url
        self.df = pd.DataFrame([])
        self.columns=columns
        self.fields=fields
        self.t=getToday_s()
        self._init_browser(SeleniumTable)
    @staticmethod
    def _init_browser(cls):
        if cls.browser==None:
            cls.browser= webdriver.Chrome()

    def _start_table(self):
        soap = BeautifulSoup(self.browser.page_source, features="lxml")
        soap_dom = soap.find(id=self.id)
        if (soap_dom):
            df_temp = pd.read_html(str(soap_dom)) or None
            if len(df_temp) > 0:
                df_temp = df_temp[0]
                self.df = pd.concat([self.df, df_temp])

            next_dom = self.browser.find_element_by_xpath(self.nextButton["xpath"])
            if "disabled" not in next_dom.get_attribute("class"):
                next_dom.click()
                time.sleep(1)
                self._start_table()
        return self.df
    def start(self):
        self. browser.get(self.url)
        return self._start_table()
    def getDf(self, ):
        return self.df

    def save(self, ):
        treasure_industry.delete({"t":self.t},multi=True)
        df1=self.df.copy()
        df1.columns = self.fields
        df1["t"]=self.t
        df1.set_index("order", inplace=True)
        o=json.loads(df1.to_json(orient="records"))
        for r in o :
            treasure_industry.upsert(**r)
        print("OK")