from main.page import Table
from bs4 import BeautifulSoup
import pandas as pd
import traceback

from main.utils.time import getToday_s
import time


from main.page.dao import SaveFactory

from main.utils.log import FileLog
selenium_log=FileLog("selenium.log").logger


class SeleniumTableData(Table):
    driver=None
    def __init__(self,selector,nextButton,url,columns,fields,other_fields,save_config=None,*args,**kwargs):
        self.selector= selector
        self.nextButton = nextButton
        self.df = None
        self.url = url
        self.df = pd.DataFrame([])
        self.columns=columns
        self.fields=fields
        self.other_fields=other_fields
        self.save_config=save_config
        self.init_drive()



    def _bind_other_fields(self,df_temp):
        for field in self.other_fields.keys() or [] :
            opt=self.other_fields[field]
            field_data=[]
            if opt["ruleType"]=="row_index":

                for i in range(df_temp.shape[0]):
                    field_dom=self.driver.find_element_by_xpath(opt["xpath"].format(row_index=i+1))
                    if field_dom.get_attribute(opt["attr"]):
                        field_data.append(field_dom.get_attribute(opt["attr"]))
            df_temp[field]=pd.Series(field_data)
            pass

    def _start_table(self):
        soap = BeautifulSoup(self.driver.page_source, features="lxml")
        soap_dom = soap.find(**self.selector)
        if (soap_dom):
            df_temp = pd.read_html(str(soap_dom)) or None
            if len(df_temp) > 0:
                df_temp = df_temp[0]
                if self.other_fields:
                    self._bind_other_fields(df_temp)
                self.df = pd.concat([self.df, df_temp])

            next_dom = self.driver.find_element_by_xpath(self.nextButton["xpath"])
            if "disabled" not in next_dom.get_attribute("class"):
                next_dom.click()
                time.sleep(1)
                self._start_table()
        return self.df
    def start(self):
        try:
            self. driver.get(self.url)
            self._start_table()
            self._df_dispose() # 修改表头
            self.save()
        except Exception as err :

            selenium_log.error(f"{str(traceback.format_exc())}\n{err}")

        return "OK"
    def _df_dispose(self):
        self.df.columns = self.fields + list(self.other_fields.keys())
        self.df.reset_index()
    def getDf(self, ):
        return self.df

    def save(self, ):
        for conf in self.save_config or []:
            kwargs = dict({}, **conf)
            kwargs["df"] = self.df
            s=SaveFactory.init(tp=conf.get("tp")).from_yarm(**kwargs)
            s.save()
            print("OK")



class SeleniumTableTitle(Table):
    def __init__(self,selector,url,columns=None,fields=None,field_keys=None,save_config=None,*args,**kwargs):
        self.selector=selector
        self.url=url
        self.columns=columns
        self.fields=fields
        self.field_keys=field_keys
        self.save_config=save_config
        self.init_drive()

    def _start_table(self):
        soap = BeautifulSoup(self.driver.page_source, features="lxml")
        soap_dom = soap.find(**self.selector)
        a=[]
        for r in soap.find_all("th"):
            # 考虑写入磁盘
            if r.attrs.get("colspan")>1:
                pass
            o={
                "field_key":r.attrs.get("data-field") or "",
                "columns": r.text or ""
            }
            a.append(o)
        print (a )
        pass
    def start(self):
        try:
            self.driver.get(self.url)
            self._start_table()
        except Exception as err:

            selenium_log.error(f"{str(traceback.format_exc())}\n{err}")