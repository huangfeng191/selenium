#!/usr/bin/python
#-*- coding: utf-8 -*-

from main.utils import yaml_loader
from main.utils.exception import UnrealizedException
TableConfig=yaml_loader("./table.yaml")


from selenium import webdriver






class Table:
    driver=None
    def __init__(self,*args,**kwargs):
        pass
    def start(self,):
        '''
        开始获取数据,并保存
        :return:
        '''
        pass

    @classmethod
    def init_drive(cls):
        if cls.driver == None:
            cls.driver = webdriver.Chrome()

    @classmethod
    def from_yaml(cls,name,tp):
        config=TableConfig[name][tp]
        return cls(**config)


class PageFactory:
    def __init__(self,source="yaml"):
        self.source= source


    def getTable(self, name,tp):
        if self.source=="yaml":
            config=TableConfig[name][tp]
            if tp=="rest":
                table=RestTable(**config)
            elif tp=="selenium":
                if config.get("tp")=="table_data":
                    table=SeleniumTableData(**config)
                elif config.get("tp")=="table_title":
                    table=SeleniumTableTitle(**config)
                else:
                    raise UnrealizedException()
        return table



from main.page.rest import RestTable
from main.page.selenium import SeleniumTableData, SeleniumTableTitle
