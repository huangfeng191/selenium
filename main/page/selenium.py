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
    def __init__(self,id,nextButton,url,columns=None,fields=None,other_fields=None,**kwargs):
        self.id = id
        self.nextButton = nextButton
        self.df = None
        self.url = url
        self.df = pd.DataFrame([])
        self.columns=columns
        self.fields=fields
        self.other_fields=other_fields
        self.t=getToday_s()
        self._init_browser(SeleniumTable)
    @staticmethod
    def _init_browser(cls):
        if cls.browser==None:
            cls.browser= webdriver.Chrome()
    def _bind_other_fields(self,df_temp):
        for field in self.other_fields.keys() or [] :
            opt=self.other_fields[field]
            field_data=[]
            if opt["ruleType"]=="row_index":

                for i in range(df_temp.shape[0]):
                    field_dom=self.browser.find_element_by_xpath(opt["xpath"].format(row_index=i+1))
                    if field_dom.get_attribute(opt["attr"]):
                        field_data.append(field_dom.get_attribute(opt["attr"]))
            df_temp[field]=pd.Series(field_data)
            pass

    def _start_table(self):
        soap = BeautifulSoup(self.browser.page_source, features="lxml")
        soap_dom = soap.find(id=self.id)
        if (soap_dom):
            df_temp = pd.read_html(str(soap_dom)) or None
            if len(df_temp) > 0:
                df_temp = df_temp[0]
                if self.other_fields:
                    self._bind_other_fields(df_temp)
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
        df1.columns = self.fields+list(self.other_fields.keys())
        df1["t"]=self.t
        df1.set_index("order", inplace=True)
        o=json.loads(df1.to_json(orient="records"))
        for r in o :
            treasure_industry.upsert(**r)
        print("OK")